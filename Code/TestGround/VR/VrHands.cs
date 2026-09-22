using Rinten.VR;

namespace TestGround;

/// <summary>Draws tracked hand joints, or controller axes when hands are not tracked.</summary>
[Title( "VR Hands" )]
[Category( "Test Ground" )]
[Icon( "pan_tool" )]
public sealed class VrHands : Component
{
	[Property, Range( 0.002f, 0.03f )] public float JointSize { get; set; } = 0.007f;

	private static readonly Color[] colours =
	[
		new( 1.00f, 0.65f, 0.25f ), new( 0.45f, 0.95f, 0.45f ), new( 0.40f, 0.85f, 1.00f ),
		new( 0.55f, 0.60f, 1.00f ), new( 1.00f, 0.50f, 0.85f )
	];

	private static readonly VRHandJoint[][] fingers =
	[
		[VRHandJoint.Wrist, VRHandJoint.ThumbMetacarpal, VRHandJoint.ThumbProximal, VRHandJoint.ThumbDistal, VRHandJoint.ThumbTip],
		[VRHandJoint.Wrist, VRHandJoint.IndexMetacarpal, VRHandJoint.IndexProximal, VRHandJoint.IndexIntermediate, VRHandJoint.IndexDistal, VRHandJoint.IndexTip],
		[VRHandJoint.Wrist, VRHandJoint.MiddleMetacarpal, VRHandJoint.MiddleProximal, VRHandJoint.MiddleIntermediate, VRHandJoint.MiddleDistal, VRHandJoint.MiddleTip],
		[VRHandJoint.Wrist, VRHandJoint.RingMetacarpal, VRHandJoint.RingProximal, VRHandJoint.RingIntermediate, VRHandJoint.RingDistal, VRHandJoint.RingTip],
		[VRHandJoint.Wrist, VRHandJoint.LittleMetacarpal, VRHandJoint.LittleProximal, VRHandJoint.LittleIntermediate, VRHandJoint.LittleDistal, VRHandJoint.LittleTip]
	];

	protected override void OnUpdate()
	{
		if ( !Game.IsRunningInVR || Input.VR is null ) return;
		DrawHand( Input.VR.LeftHand );
		DrawHand( Input.VR.RightHand );
	}

	private void DrawHand( VRController hand )
	{
		// Controller tracking returns a guessed hand too. The dedicated controller
		// placeholder is clearer, so draw joints only when the headset tracks a
		// real bare hand.
		if ( !hand.IsHandTracked ) return;

		var joints = hand.GetJoints( MotionRange.Hand );
		if ( joints is null || joints.Length < 26 ) return;
		for ( var finger = 0; finger < fingers.Length; finger++ )
		{
			Vector3 previous = default;
			for ( var index = 0; index < fingers[finger].Length; index++ )
			{
				var local = joints[(int)fingers[finger][index]].Transform;
				var point = Input.VR.Anchor.ToWorld( local.WithPosition( local.Position * Input.VR.Scale ) ).Position;
				if ( index > 0 ) DebugOverlay.Line( previous, point, colours[finger], 0, default, true );
				DebugOverlay.Sphere( new Sphere( point, JointSize ), colours[finger], 0, default, true );
				previous = point;
			}
		}
	}

}
