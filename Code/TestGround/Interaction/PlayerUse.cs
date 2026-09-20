namespace TestGround;

/// <summary>
/// Presses whatever <see cref="Component.IPressable"/> the camera is looking
/// at. Drop this on the player; drop <see cref="Door"/> (or anything else
/// that can be pressed) on the thing being used.
/// </summary>
[Title( "Player Use" )]
[Category( "Test Ground" )]
[Icon( "touch_app" )]
public sealed class PlayerUse : Component
{
	/// <summary>The key that uses.</summary>
	[Property, InputAction] public string Action { get; set; } = "Use";

	/// <summary>How far the use ray reaches, in metres.</summary>
	[Property] public float Reach { get; set; } = 3.0f;

	protected override void OnUpdate()
	{
		if ( !Input.Pressed( Action ) ) return;

		var camera = Scene.Camera;
		if ( !camera.IsValid() ) return;

		var start = camera.WorldPosition;
		var end = start + camera.WorldRotation.Forward * Reach;
		var hit = Scene.Trace.Ray( start, end )
			.IgnoreGameObjectHierarchy( GameObject.Root )
			.Run();

		if ( !hit.Hit ) return;

		var target = hit.Collider?.GameObject ?? hit.GameObject;
		if ( !target.IsValid() ) return;

		var pressable = target.GetComponentInParent<Component.IPressable>( includeSelf: true );
		if ( pressable is null ) return;

		pressable.Press( new Component.IPressable.Event( this, new Ray( start, camera.WorldRotation.Forward ) ) );
	}
}
