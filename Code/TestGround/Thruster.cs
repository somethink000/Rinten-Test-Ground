namespace TestGround;

/// <summary>
/// Pushes its rigidbody up every step with a force set as a fraction of its own
/// weight, so the number reads directly: 1 hovers, less sinks, more climbs. Goes
/// home when it drifts past <see cref="Ceiling"/> or <see cref="Floor"/>.
/// </summary>
[Title( "Thruster" )]
[Category( "Test Ground" )]
[Icon( "local_fire_department" )]
public sealed class Thruster : Component
{
	/// <summary>Upward force as a multiple of the body's weight.</summary>
	[Property] public float WeightFraction { get; set; } = 1.0f;

	/// <summary>World height above which the body is put back at its start.</summary>
	[Property] public float Ceiling { get; set; } = 9.0f;

	/// <summary>World height below which the body is put back at its start.</summary>
	[Property] public float Floor { get; set; } = 0.5f;

	private Transform start;

	protected override void OnStart()
	{
		start = WorldTransform;
	}

	protected override void OnFixedUpdate()
	{
		var body = Components.Get<Rigidbody>();
		if ( !body.IsValid() ) return;

		if ( WorldPosition.y > Ceiling || WorldPosition.y < Floor )
		{
			WorldTransform = start;
			body.Velocity = 0;
			body.AngularVelocity = 0;
			return;
		}

		var gravity = Scene.PhysicsWorld.Gravity.Length;
		body.ApplyForce( Vector3.Up * body.Mass * gravity * WeightFraction );
	}
}
