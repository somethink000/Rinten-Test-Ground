using System.Text.Json.Serialization;

namespace TestGround;

/// <summary>
/// Makes a trigger visible: the renderer on this object takes one colour while
/// nothing is inside and another while something is, and the counts say how many
/// times the volume has been entered and left.
/// <para>
/// It also checks itself: every physics step it tests each rigidbody's centre
/// against its own volume, so a body that passes through with no enter event
/// is a warning with the body's name on it, not a shrug.
/// </para>
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

	/// <summary>Compare geometry against the events every step and warn when they disagree.</summary>
	[Property] public bool CheckGeometry { get; set; } = true;

	/// <summary>How many times anything has entered since the scene started.</summary>
	[Property, ReadOnly, JsonIgnore] public int EnterCount { get; private set; }

	/// <summary>How many times anything has left since the scene started.</summary>
	[Property, ReadOnly, JsonIgnore] public int ExitCount { get; private set; }

	/// <summary>How many colliders are inside right now.</summary>
	[Property, ReadOnly, JsonIgnore] public int InsideCount => inside.Count;

	private readonly HashSet<Collider> inside = new();

	private ModelRenderer Renderer => renderer ??= Components.Get<ModelRenderer>( FindMode.EverythingInSelfAndDescendants );
	private ModelRenderer renderer;

	private Collider Trigger => trigger ??= Components.Get<Collider>( FindMode.EverythingInSelf );
	private Collider trigger;

	/// <summary>A text renderer under this object shows the counts, so the numbers can be read off the scene.</summary>
	private TextRenderer Counter => counter ??= Components.Get<TextRenderer>( FindMode.EverythingInDescendants );
	private TextRenderer counter;

	/// <summary>Rigidbodies whose centre is inside the trigger's volume right now, by geometry alone.</summary>
	private readonly HashSet<GameObject> geometric = new();

	/// <summary>Objects an enter event has been heard for since they last left the volume.</summary>
	private readonly HashSet<GameObject> heard = new();

	private string Tag => $"[{GameObject.Name}]";

	protected override void OnEnabled()
	{
		inside.Clear();
		Recolour();
	}

	protected override void OnStart()
	{
		var collider = Trigger;

		if ( !collider.IsValid() )
		{
			Log.Warning( $"{Tag} no Collider on this object - nothing will ever enter" );
			return;
		}

		var rigidbody = collider.Rigidbody;
		var body = rigidbody.IsValid() ? "rigidbody" : (collider.Static ? "static keyframe" : "keyframe");

		Log.Info( $"{Tag} {collider.GetType().Name}: IsTrigger={collider.IsTrigger} Static={collider.Static} body={body} tags=[{string.Join( ",", GameObject.Tags.TryGetAll() )}]" );

		if ( !collider.IsTrigger )
			Log.Warning( $"{Tag} the collider is not a trigger - it will push things, not report them" );
	}

	void Component.ITriggerListener.OnTriggerEnter( Collider other )
	{
		inside.Add( other );
		heard.Add( other.GameObject );
		EnterCount++;

		if ( LogEvents )
			Log.Info( $"{Tag} enter: {Describe( other )} ({inside.Count} inside)" );

		Recolour();
	}

	void Component.ITriggerListener.OnTriggerExit( Collider other )
	{
		inside.Remove( other );
		ExitCount++;

		// A body that only grazed the volume never had its centre inside, so the
		// geometry side will not clear it; forget it here or its next pass is
		// taken on trust.
		if ( !geometric.Contains( other.GameObject ) )
			heard.Remove( other.GameObject );

		if ( LogEvents )
			Log.Info( $"{Tag} exit: {Describe( other )} ({inside.Count} inside)" );

		Recolour();
	}

	void Component.ITriggerListener.OnTriggerEnter( GameObject other )
	{
		if ( LogEvents )
			Log.Info( $"{Tag} object enter: {other.Name}" );
	}

	void Component.ITriggerListener.OnTriggerExit( GameObject other )
	{
		if ( LogEvents )
			Log.Info( $"{Tag} object exit: {other.Name}" );
	}

	protected override void OnUpdate()
	{
		// A body deleted while inside never sends its exit, so the set is swept
		// rather than trusted - otherwise the volume stays lit with nothing in it.
		if ( inside.RemoveWhere( x => !x.IsValid() ) > 0 )
			Recolour();
	}

	protected override void OnFixedUpdate()
	{
		if ( !CheckGeometry ) return;

		var collider = Trigger;
		if ( !collider.IsValid() ) return;

		// Every step rather than on a timer: a body falling at 14 m/s is in a
		// 2 m box for a seventh of a second.
		foreach ( var body in Scene.GetAllComponents<Rigidbody>() )
		{
			if ( !body.IsValid() || IsOwn( body ) ) continue;

			var go = body.GameObject;
			var now = Inside( body.WorldPosition );

			if ( now == geometric.Contains( go ) ) continue;

			if ( now )
			{
				geometric.Add( go );

				if ( LogEvents )
					Log.Info( $"{Tag} geometry: {go.Name} entered, enter event heard: {(heard.Contains( go ) ? "yes" : "not yet")}" );
			}
			else
			{
				geometric.Remove( go );

				if ( heard.Remove( go ) )
				{
					if ( LogEvents )
						Log.Info( $"{Tag} geometry: {go.Name} left" );
				}
				else
				{
					Log.Warning( $"{Tag} {go.Name} passed through with no enter event (entered {EnterCount} exited {ExitCount} so far)" );
				}
			}
		}
	}

	/// <summary>
	/// Whether a point is in the trigger's volume. Exact for a sphere, so a ball
	/// in the corner of its bounding box is not counted; the bounding box for
	/// everything else, which over-counts near the corners of a capsule.
	/// </summary>
	private bool Inside( Vector3 point )
	{
		var collider = Trigger;

		if ( collider is SphereCollider sphere )
		{
			var center = WorldTransform.PointToWorld( sphere.Center );
			var radius = sphere.Radius * WorldScale.x;
			return (point - center).LengthSquared <= radius * radius;
		}

		return collider.LocalBounds.Transform( WorldTransform ).Contains( point );
	}

	/// <summary>The body this trigger rides on, if any - a sensor never reports its own body.</summary>
	private bool IsOwn( Rigidbody body )
		=> body.GameObject == GameObject || (Trigger.IsValid() && Trigger.Rigidbody == body);

	private static string Describe( Collider other )
	{
		if ( !other.IsValid() ) return "(invalid)";

		var body = other.Rigidbody.IsValid() ? "rigidbody" : (other.Static ? "static" : "keyframe");
		return $"{other.GameObject.Name}/{other.GetType().Name} ({body}{(other.IsTrigger ? ", trigger" : "")})";
	}

	private void Recolour()
	{
		if ( Counter.IsValid() )
			Counter.Text = $"in {inside.Count}\n+{EnterCount} -{ExitCount}";

		if ( !Renderer.IsValid() ) return;

		Renderer.Tint = inside.Count > 0 ? HitColor : IdleColor;
	}
}
