namespace TestGround;

/// <summary>
/// Sweeps a game object back and forth about an axis, easing at the ends -
/// a sword arm, a searchlight, a target on a stick for something to home on.
/// </summary>
/// <remarks>
/// Runs in the editor too, because the effects that ride it are previewed
/// there and an anchor that never moves shows nothing.
/// </remarks>
[Title( "Swing" )]
[Category( "Test Ground" )]
[Icon( "swap_horiz" )]
public sealed class Swing : Component, Component.ExecuteInEditor
{
	/// <summary>The axis swung about, in the parent's space.</summary>
	[Property] public Vector3 Axis { get; set; } = Vector3.Right;

	/// <summary>Degrees either side of the rest pose.</summary>
	[Property] public float Amplitude { get; set; } = 60.0f;

	/// <summary>Seconds for a full there-and-back.</summary>
	[Property] public float Period { get; set; } = 2.0f;

	/// <summary>Where in the cycle this starts, nought to one, so two swings can be out of step.</summary>
	[Property, Range( 0.0f, 1.0f )] public float Phase { get; set; }

	/// <summary>Seconds held still at each end of the sweep.</summary>
	[Property] public float Hold { get; set; } = 0.0f;

	Rotation _rest;
	bool _hasRest;

	protected override void OnEnabled()
	{
		_rest = LocalRotation;
		_hasRest = true;
	}

	protected override void OnUpdate()
	{
		if ( !_hasRest ) return;

		var period = ( Period + Hold * 2.0f ).Clamp( 0.01f, 3600.0f );
		var t = ( Time.Now / period + Phase ) % 1.0f;

		// Half the cycle out, half back, each with a hold at its end - eased
		// so the turn at the end is a turn and not a bounce.
		var half = period * 0.5f;
		var within = ( t * period ) % half;
		var moving = ( within / ( half - Hold ).Clamp( 0.01f, 3600.0f ) ).Clamp( 0.0f, 1.0f );
		var eased = moving * moving * ( 3.0f - 2.0f * moving );
		var swing = t < 0.5f ? MathX.Lerp( -1.0f, 1.0f, eased ) : MathX.Lerp( 1.0f, -1.0f, eased );

		var axis = Axis.IsNearZeroLength ? Vector3.Right : Axis.Normal;

		LocalRotation = Rotation.FromAxis( axis, swing * Amplitude ) * _rest;
	}
}
