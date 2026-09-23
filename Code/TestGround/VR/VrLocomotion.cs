using Rinten.VR;

namespace TestGround;

/// <summary>
/// Walking and turning with the sticks, for the room-scale player it sits on: the
/// left stick walks where the head faces, the right snaps the view round the head.
/// </summary>
[Title( "VR Locomotion" )]
[Category( "Test Ground" )]
[Icon( "directions_walk" )]
public sealed class VrLocomotion : Component
{
	[Property] public float MoveSpeed { get; set; } = 2.2f;
	[Property] public float SnapDegrees { get; set; } = 30.0f;
	[Property] public float SnapThreshold { get; set; } = 0.72f;

	private bool turnLatched;

	protected override void OnUpdate()
	{
		if ( !Game.IsRunningInVR || Input.VR is null ) return;

		Walk();
		Turn();
	}

	private void Walk()
	{
		var input = Input.VR;
		var stick = input.LeftHand.Joystick.Value;
		var facing = Rotation.FromYaw( input.Head.Rotation.Yaw() );
		var wish = facing * new Vector3( stick.x, 0, -stick.y );

		if ( wish.Length > 0.08f ) GameObject.WorldPosition += wish.ClampLength( 1.0f ) * MoveSpeed * Time.Delta;
	}

	/// <summary>A snap each time the stick goes past the threshold, about the head so it stays put.</summary>
	private void Turn()
	{
		var input = Input.VR;
		var turn = input.RightHand.Joystick.Value.x;

		if ( System.MathF.Abs( turn ) < 0.35f ) turnLatched = false;
		if ( turnLatched || System.MathF.Abs( turn ) < SnapThreshold ) return;

		turnLatched = true;

		var anchor = GameObject.WorldTransform;
		var head = input.Head.Position;
		var localHead = anchor.PointToLocal( head );
		var rotation = Rotation.FromYaw( turn > 0 ? -SnapDegrees : SnapDegrees ) * anchor.Rotation;

		GameObject.WorldRotation = rotation;
		GameObject.WorldPosition = head - rotation * localHead;
	}
}
