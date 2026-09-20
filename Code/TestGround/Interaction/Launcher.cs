namespace TestGround;

/// <summary>
/// Clones a prefab in front of the camera and shoves it. The scene-system
/// test for "a prefab is a thing you can throw".
/// </summary>
[Title( "Launcher" )]
[Category( "Test Ground" )]
[Icon( "sports_baseball" )]
public sealed class Launcher : Component
{
	/// <summary>What to throw. Drop a .prefab here.</summary>
	[Property] public PrefabFile Prefab { get; set; }

	/// <summary>The key that throws.</summary>
	[Property, InputAction] public string Action { get; set; } = "Attack1";

	/// <summary>Metres in front of the camera the copy appears.</summary>
	[Property] public float Offset { get; set; } = 1.2f;

	/// <summary>Metres a second along the camera's look.</summary>
	[Property] public float Speed { get; set; } = 12.0f;

	/// <summary>
	/// Seconds the copy lives. Nought leaves the prefab's own
	/// <see cref="SelfDestruct"/> alone.
	/// </summary>
	[Property] public float Lifetime { get; set; } = 0.0f;

	protected override void OnUpdate()
	{
		if ( Prefab is null ) return;
		if ( !Input.Pressed( Action ) ) return;

		var camera = Scene.Camera;
		if ( !camera.IsValid() ) return;

		var origin = camera.WorldPosition + camera.WorldRotation.Forward * Offset;
		var copy = GameObject.Clone( Prefab, new Transform( origin, camera.WorldRotation ) );
		if ( !copy.IsValid() ) return;

		copy.Enabled = true;

		if ( copy.Components.Get<Rigidbody>( FindMode.EnabledInSelfAndDescendants ) is Rigidbody body )
			body.Velocity = camera.WorldRotation.Forward * Speed;

		if ( Lifetime > 0.0f )
		{
			var death = copy.GetOrAddComponent<SelfDestruct>();
			death.Seconds = Lifetime;
		}
	}
}
