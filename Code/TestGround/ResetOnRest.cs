namespace TestGround;

/// <summary>
/// Puts a body back where it started once it has come to rest for a while. The
/// stand that ends in stillness - a ball that bounced out, a box that slid to
/// the bottom, a stack that was knocked over - runs again instead of sitting
/// there having proved its point once.
/// </summary>
[Title( "Reset On Rest" )]
[Category( "Test Ground" )]
[Icon( "replay" )]
public sealed class ResetOnRest : Component
{
	/// <summary>Seconds of rest before the body goes home.</summary>
	[Property] public float AfterSeconds { get; set; } = 3.0f;

	/// <summary>Below this speed the body counts as resting.</summary>
	[Property] public float RestSpeed { get; set; } = 0.05f;

	/// <summary>
	/// Only reset when the body has moved at least this far from home. Nought
	/// resets on every rest, which is what a drop test wants; a stack wants to be
	/// left alone until somebody knocks it over.
	/// </summary>
	[Property] public float MinDisplacement { get; set; } = 0.0f;

	private Transform start;
	private TimeSince sinceMoving;

	protected override void OnStart()
	{
		start = WorldTransform;
		sinceMoving = 0;
	}

	protected override void OnFixedUpdate()
	{
		var body = Components.Get<Rigidbody>();
		if ( !body.IsValid() ) return;

		var moving = body.Velocity.Length > RestSpeed || body.AngularVelocity.Length > RestSpeed;

		if ( moving )
		{
			sinceMoving = 0;
			return;
		}

		if ( sinceMoving < AfterSeconds ) return;
		sinceMoving = 0;

		if ( MinDisplacement > 0 && WorldPosition.Distance( start.Position ) < MinDisplacement )
			return;

		WorldTransform = start;
		body.Velocity = 0;
		body.AngularVelocity = 0;
	}
}
