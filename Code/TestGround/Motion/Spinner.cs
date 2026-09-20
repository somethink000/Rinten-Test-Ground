namespace TestGround;

/// <summary>
/// Turns a game object at a constant rate.
/// </summary>
/// <remarks>
/// Turned in the fixed update rather than the frame update so that a collider
/// riding on it moves in step with the solver: a collider that is not
/// <see cref="Collider.Static"/> and has no rigidbody is keyframed, which means
/// it shoves dynamic bodies out of the way instead of passing through them. That
/// is what makes this a paddle rather than a decoration.
/// </remarks>
[Title( "Spinner" )]
[Category( "Test Ground" )]
[Icon( "rotate_right" )]
public sealed class Spinner : Component
{
	/// <summary>The axis turned about, in this object's own space.</summary>
	[Property] public Vector3 Axis { get; set; } = Vector3.Up;

	/// <summary>Degrees a second. Negative turns the other way.</summary>
	[Property] public float Speed { get; set; } = 120.0f;

	/// <summary>Turn about the parent's axes instead of this object's own.</summary>
	[Property] public bool Local { get; set; } = true;

	protected override void OnFixedUpdate()
	{
		var axis = Axis.IsNearZeroLength ? Vector3.Up : Axis.Normal;
		var step = Rotation.FromAxis( axis, Speed * Time.Delta );

		if ( Local )
		{
			LocalRotation *= step;
		}
		else
		{
			WorldRotation = step * WorldRotation;
		}
	}
}
