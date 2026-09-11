using System.Text.Json.Serialization;

namespace TestGround;

/// <summary>
/// Makes a trigger visible: the renderer on this object takes one colour while
/// nothing is inside and another while something is, and the counts say how many
/// times the volume has been entered and left.
/// </summary>
[Title( "Trigger Probe" )]
[Category( "Test Ground" )]
[Icon( "sensors" )]
public sealed class TriggerProbe : Component, Component.ITriggerListener
{
	/// <summary>What to tint while the volume is empty.</summary>
	[Property] public Color IdleColor { get; set; } = new Color( 0.20f, 0.55f, 0.90f, 0.25f );

	/// <summary>What to tint while something is inside.</summary>
	[Property] public Color HitColor { get; set; } = new Color( 1.00f, 0.45f, 0.15f, 0.55f );

	/// <summary>Write every enter and exit to the console.</summary>
	[Property] public bool LogEvents { get; set; } = true;

	/// <summary>How many times anything has entered since the scene started.</summary>
	[Property, ReadOnly, JsonIgnore] public int EnterCount { get; private set; }

	/// <summary>How many times anything has left since the scene started.</summary>
	[Property, ReadOnly, JsonIgnore] public int ExitCount { get; private set; }

	/// <summary>How many colliders are inside right now.</summary>
	[Property, ReadOnly, JsonIgnore] public int InsideCount => inside.Count;

	private readonly HashSet<Collider> inside = new();

	private ModelRenderer Renderer => renderer ??= Components.Get<ModelRenderer>( FindMode.EverythingInSelfAndDescendants );
	private ModelRenderer renderer;

	protected override void OnEnabled()
	{
		inside.Clear();
		Recolour();
	}

	void Component.ITriggerListener.OnTriggerEnter( Collider other )
	{
		inside.Add( other );
		EnterCount++;

		if ( LogEvents )
			Log.Info( $"[{GameObject.Name}] enter: {other.GameObject.Name} ({inside.Count} inside)" );

		Recolour();
	}

	void Component.ITriggerListener.OnTriggerExit( Collider other )
	{
		inside.Remove( other );
		ExitCount++;

		if ( LogEvents )
			Log.Info( $"[{GameObject.Name}] exit: {other.GameObject.Name} ({inside.Count} inside)" );

		Recolour();
	}

	protected override void OnUpdate()
	{
		// A body deleted while inside never sends its exit, so the set is swept
		// rather than trusted - otherwise the volume stays lit with nothing in it.
		if ( inside.RemoveWhere( x => !x.IsValid() ) > 0 )
			Recolour();
	}

	private void Recolour()
	{
		if ( !Renderer.IsValid() ) return;

		Renderer.Tint = inside.Count > 0 ? HitColor : IdleColor;
	}
}
