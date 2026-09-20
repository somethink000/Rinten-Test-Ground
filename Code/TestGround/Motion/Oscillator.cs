namespace TestGround;

/// <summary>
/// Slides a game object back and forth along an axis. A platform, a target,
/// anything that should move without being a rigidbody.
/// </summary>
/// <remarks>
/// Fixed update, same as <see cref="Spinner"/>: a collider riding this is
/// keyframed, and keyframed colliders have to move in step with the solver
/// or they pass through the things they should shove.
/// </remarks>
[Title( "Oscillator" )]
[Category( "Test Ground" )]
[Icon( "swap_vert" )]
public sealed class Oscillator : Component
{
	/// <summary>The axis travelled along, in the parent's space.</summary>
	[Property] public Vector3 Axis { get; set; } = Vector3.Up;

	/// <summary>Metres either side of the rest pose.</summary>
	[Property] public float Amplitude { get; set; } = 1.0f;

	/// <summary>Cycles a second.</summary>
	[Property] public float Speed { get; set; } = 0.5f;

	/// <summary>Where in the cycle this starts, nought to one.</summary>
	[Property, Range( 0.0f, 1.0f )] public float Phase { get; set; }

	Vector3 rest;
	bool hasRest;

	protected override void OnEnabled()
	{
		rest = LocalPosition;
		hasRest = true;
	}

	protected override void OnFixedUpdate()
	{
		if ( !hasRest ) return;

		var axis = Axis.IsNearZeroLength ? Vector3.Up : Axis.Normal;
		var t = (Time.Now * Speed + Phase) * 6.2831853f;
		LocalPosition = rest + axis * (System.MathF.Sin( t ) * Amplitude);
	}
}
