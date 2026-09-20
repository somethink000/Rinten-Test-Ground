namespace TestGround;

/// <summary>
/// Turns the <see cref="TrailRenderer"/> beside it on and off on a clock, so
/// the trail is a dashed line: what stopping and starting emission looks like,
/// and whether an old trail is kept or thrown away when it starts again.
/// </summary>
[Title( "Trail Pulse" )]
[Category( "Test Ground" )]
[Icon( "more_horiz" )]
public sealed class TrailPulse : Component
{
	/// <summary>Seconds emitting.</summary>
	[Property] public float On { get; set; } = 1.0f;

	/// <summary>Seconds not.</summary>
	[Property] public float Off { get; set; } = 0.5f;

	TimeSince since;

	protected override void OnEnabled() => since = 0;

	protected override void OnUpdate()
	{
		var trail = GameObject.GetComponent<TrailRenderer>();
		if ( trail is null ) return;

		var cycle = On + Off;
		if ( cycle <= 0 ) return;

		var t = since % cycle;
		trail.Emitting = t < On;
	}
}
