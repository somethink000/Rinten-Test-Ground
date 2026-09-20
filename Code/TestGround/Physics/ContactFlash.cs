namespace TestGround;

/// <summary>
/// Shows collision events on the body itself: the renderer takes
/// <see cref="TouchColor"/> while anything is in contact and goes back to its
/// own tint when the last contact ends. A stack that stays lit is resting
/// contacts working; a bouncing ball that blinks on each hit is start/stop
/// events working.
/// </summary>
[Title( "Contact Flash" )]
[Category( "Test Ground" )]
[Icon( "highlight" )]
public sealed class ContactFlash : Component, Component.ICollisionListener
{
	/// <summary>Tint while touching something.</summary>
	[Property] public Color TouchColor { get; set; } = new Color( 1.0f, 0.85f, 0.2f, 1.0f );

	/// <summary>Write each start and stop to the console.</summary>
	[Property] public bool LogEvents { get; set; } = false;

	private readonly HashSet<Collider> touching = new();
	private Color idle;
	private bool hasIdle;

	private ModelRenderer Renderer => renderer ??= Components.Get<ModelRenderer>( FindMode.EverythingInSelfAndDescendants );
	private ModelRenderer renderer;

	protected override void OnEnabled()
	{
		touching.Clear();

		if ( Renderer.IsValid() && !hasIdle )
		{
			idle = Renderer.Tint;
			hasIdle = true;
		}
	}

	void Component.ICollisionListener.OnCollisionStart( Collision collision )
	{
		var other = collision.Other.Collider;
		if ( !other.IsValid() ) return;

		touching.Add( other );

		if ( LogEvents )
			Log.Info( $"[{GameObject.Name}] touch: {other.GameObject.Name} ({touching.Count} touching)" );

		Recolour();
	}

	void Component.ICollisionListener.OnCollisionStop( CollisionStop collision )
	{
		var other = collision.Other.Collider;
		if ( !other.IsValid() ) return;

		touching.Remove( other );

		if ( LogEvents )
			Log.Info( $"[{GameObject.Name}] release: {other.GameObject.Name} ({touching.Count} touching)" );

		Recolour();
	}

	protected override void OnUpdate()
	{
		if ( touching.RemoveWhere( x => !x.IsValid() ) > 0 )
			Recolour();
	}

	private void Recolour()
	{
		if ( !Renderer.IsValid() || !hasIdle ) return;

		Renderer.Tint = touching.Count > 0 ? TouchColor : idle;
	}
}
