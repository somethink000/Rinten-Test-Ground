namespace TestGround;

/// <summary>
/// Throws the object about on a fixed path so that whatever hangs off it swings.
/// </summary>
/// <remarks>
/// Jiggle bones react to acceleration, not to a held pose: a character standing
/// still with a spring in its hair is a character whose hair never moves, and
/// that is correct rather than broken. Something has to shake it, and a station
/// that can only be judged by shaking it by hand is a station nobody judges.
/// <para>
/// Each mode is a different input to the same spring - travel across the ground,
/// a turn on the spot, a drop. A chain that only fails on one of them says which
/// half of the simulation is wrong.
/// </para>
/// </remarks>
[Title( "Jiggle Shaker" )]
[Category( "Test Ground" )]
[Icon( "vibration" )]
public sealed class JiggleShaker : Component
{
	public enum Motion
	{
		/// <summary>Side to side across the floor - what World Motion answers to.</summary>
		Slide,
		/// <summary>Turning on the spot, so the tips are swung round.</summary>
		Spin,
		/// <summary>Up and down, which is the one gravity shows up in.</summary>
		Bounce,
		/// <summary>A hard stop at each end rather than a smooth turn.</summary>
		Jerk,
		/// <summary>Nothing at all, as the control.</summary>
		Still,
	}

	[Property] public Motion What { get; set; } = Motion.Slide;

	/// <summary>How far it goes, in metres, or degrees for <see cref="Motion.Spin"/>.</summary>
	[Property] public float Amount { get; set; } = 1.4f;

	/// <summary>Seconds for one there-and-back.</summary>
	[Property] public float Period { get; set; } = 2.0f;

	Vector3 rest;
	Rotation resting;
	TimeSince since;

	protected override void OnStart()
	{
		rest = LocalPosition;
		resting = LocalRotation;
		since = 0;
	}

	protected override void OnUpdate()
	{
		if ( Period <= 0.0f ) return;

		var t = ( since % Period ) / Period;
		var wave = System.MathF.Sin( t * System.MathF.Tau );

		switch ( What )
		{
			case Motion.Slide:
				LocalPosition = rest + Vector3.Right * ( wave * Amount );
				break;

			case Motion.Spin:
				LocalRotation = resting * Rotation.FromYaw( wave * Amount );
				break;

			case Motion.Bounce:
				// Squared and flipped, so it falls faster than it rises and the
				// chain is thrown rather than carried.
				LocalPosition = rest + Vector3.Up * ( ( 1.0f - System.MathF.Abs( wave ) ) * Amount );
				break;

			case Motion.Jerk:
				// A square wave: the whole of the motion happens in one frame,
				// twice a period, which is the worst thing a spring is asked for.
				LocalPosition = rest + Vector3.Right * ( wave >= 0.0f ? Amount : -Amount );
				break;
		}
	}
}
