namespace TestGround;

/// <summary>
/// Puts a body back where it started once it falls past a height. A physics test
/// scene you can push things around in is a physics test scene you can push
/// things out of, and an empty one tests nothing.
/// </summary>
[Title( "Reset On Fall" )]
[Category( "Test Ground" )]
[Icon( "restart_alt" )]
public sealed class ResetOnFall : Component
{
	/// <summary>Below this world height, the body goes home.</summary>
	[Property] public float Height { get; set; } = -10.0f;

	/// <summary>
	/// Where home is. Left empty, it's wherever the object was when the scene
	/// started, which is what you want for a body that was placed by hand.
	/// </summary>
	[Property] public GameObject SpawnPoint { get; set; }

	private Transform start;

	protected override void OnStart()
	{
		start = WorldTransform;
	}

	protected override void OnFixedUpdate()
	{
		if ( WorldPosition.y > Height )
			return;

		var target = SpawnPoint.IsValid() ? SpawnPoint.WorldTransform : start;

		WorldTransform = target;

		if ( Components.Get<Rigidbody>() is Rigidbody body )
		{
			body.Velocity = 0;
			body.AngularVelocity = 0;
		}
	}
}
