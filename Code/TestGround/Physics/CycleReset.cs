namespace TestGround;

/// <summary>
/// Puts every rigidbody under this object back where it started, all in the
/// same step, on a clock - and then gives one of them a shove. A domino run
/// reset one piece at a time knocks itself over again; reset together it stands.
/// </summary>
[Title( "Cycle Reset" )]
[Category( "Test Ground" )]
[Icon( "restart_alt" )]
public sealed class CycleReset : Component
{
	/// <summary>Seconds between resets.</summary>
	[Property] public float Period { get; set; } = 12.0f;

	/// <summary>The body that gets the shove right after the reset, if any.</summary>
	[Property] public GameObject Kick { get; set; }

	/// <summary>Metres a second given to <see cref="Kick"/>, in its own axes.</summary>
	[Property] public Vector3 KickVelocity { get; set; }

	/// <summary>Radians a second given to <see cref="Kick"/>, in its own axes.</summary>
	[Property] public Vector3 KickAngularVelocity { get; set; }

	private readonly Dictionary<Rigidbody, Transform> homes = new();
	private TimeSince sinceReset;

	protected override void OnStart()
	{
		homes.Clear();

		foreach ( var body in Components.GetAll<Rigidbody>( FindMode.EverythingInSelfAndDescendants ) )
			homes[body] = body.WorldTransform;

		// The first cycle starts with the shove, not with a wait.
		sinceReset = Period;
	}

	protected override void OnFixedUpdate()
	{
		if ( sinceReset < Period ) return;
		sinceReset = 0;

		foreach ( var (body, home) in homes )
		{
			if ( !body.IsValid() ) continue;

			body.WorldTransform = home;
			body.Velocity = 0;
			body.AngularVelocity = 0;
		}

		if ( !Kick.IsValid() ) return;

		var kicked = Kick.Components.Get<Rigidbody>();
		if ( !kicked.IsValid() ) return;

		kicked.Velocity = Kick.WorldRotation * KickVelocity;
		kicked.AngularVelocity = Kick.WorldRotation * KickAngularVelocity;
	}
}
