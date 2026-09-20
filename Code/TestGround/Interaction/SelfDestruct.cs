namespace TestGround;

/// <summary>
/// Deletes this object after a number of seconds. Spawned debris that never
/// goes away is a physics scene that fills up.
/// </summary>
[Title( "Self Destruct" )]
[Category( "Test Ground" )]
[Icon( "timer_off" )]
public sealed class SelfDestruct : Component
{
	/// <summary>Seconds to live once enabled. Nought or less means never.</summary>
	[Property] public float Seconds { get; set; } = 4.0f;

	TimeUntil die;

	protected override void OnEnabled()
	{
		die = Seconds;
	}

	protected override void OnUpdate()
	{
		if ( Seconds <= 0.0f ) return;
		if ( die ) GameObject.Destroy();
	}
}
