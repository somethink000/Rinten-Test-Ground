namespace TestGround;

/// <summary>
/// Puts its rigidbody back where it started and sends it off again with a set
/// velocity and spin, on a clock. A bullet, a thrown cube, a domino kicked over
/// - anything that has to start moving the same way every time.
/// </summary>
[Title( "Shooter" )]
[Category( "Test Ground" )]
[Icon( "rocket_launch" )]
public sealed class Shooter : Component
{
	/// <summary>Seconds between shots.</summary>
	[Property] public float Period { get; set; } = 3.0f;

	/// <summary>Metres a second, in this object's own axes at the time of the shot.</summary>
	[Property] public Vector3 Velocity { get; set; } = new Vector3( 0, 0, -10 );

	/// <summary>Radians a second, in this object's own axes.</summary>
	[Property] public Vector3 AngularVelocity { get; set; }

	private Transform start;
	private TimeSince sinceShot;

	protected override void OnStart()
	{
		start = WorldTransform;
		sinceShot = Period;
	}

	protected override void OnFixedUpdate()
	{
		if ( sinceShot < Period ) return;
		sinceShot = 0;

		var body = Components.Get<Rigidbody>();
		if ( !body.IsValid() ) return;

		WorldTransform = start;
		body.Velocity = start.Rotation * Velocity;
		body.AngularVelocity = start.Rotation * AngularVelocity;
	}
}
