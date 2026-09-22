using Rinten.VR;

namespace TestGround;

/// <summary>A small room-scale playground for testing controller locomotion and physics grabs.</summary>
[Title( "VR Lab" )]
[Category( "Test Ground" )]
[Icon( "vrpano" )]
public sealed class VrLab : Component
{
	[Property, Category( "Locomotion" )] public float MoveSpeed { get; set; } = 2.2f;
	[Property, Category( "Locomotion" )] public float SnapDegrees { get; set; } = 30.0f;
	[Property, Category( "Locomotion" )] public float SnapThreshold { get; set; } = 0.72f;
	[Property, Category( "Hands" )] public float GrabReach { get; set; } = 0.16f;

	private readonly HandGrab left = new() { IsLeft = true };
	private readonly HandGrab right = new();
	private bool turnLatched;

	protected override void OnUpdate()
	{
		if ( !Game.IsRunningInVR || Input.VR is null ) return;
		Walk();
		Grab( Input.VR.LeftHand, left );
		Grab( Input.VR.RightHand, right );
	}

	private void Walk()
	{
		var input = Input.VR;
		var anchor = GameObject.WorldTransform;
		var stick = input.LeftHand.Joystick.Value;
		var facing = Rotation.FromYaw( input.Head.Rotation.Yaw() );
		var wish = facing * new Vector3( stick.x, 0, -stick.y );
		if ( wish.Length > 0.08f ) GameObject.WorldPosition += wish.ClampLength( 1.0f ) * MoveSpeed * Time.Delta;

		var turn = input.RightHand.Joystick.Value.x;
		if ( System.MathF.Abs( turn ) < 0.35f ) turnLatched = false;
		if ( turnLatched || System.MathF.Abs( turn ) < SnapThreshold ) return;

		turnLatched = true;
		var head = input.Head.Position;
		var localHead = anchor.PointToLocal( head );
		var rotation = Rotation.FromYaw( turn > 0 ? -SnapDegrees : SnapDegrees ) * anchor.Rotation;
		GameObject.WorldRotation = rotation;
		GameObject.WorldPosition = head - rotation * localHead;
	}

	private void Grab( VRController hand, HandGrab state )
	{
		var held = IsGrabbing( hand );
		if ( state.Body.IsValid() )
		{
			if ( held ) return;
			state.Joint?.Remove();
			Components.Get<VrControllers>()?.SetHolding( state.IsLeft, false );
			state.Body.Velocity = hand.Velocity.ClampLength( 8.0f );
			var spin = hand.AngularVelocity;
			state.Body.AngularVelocity = new Vector3( spin.pitch, spin.yaw, spin.roll ).ClampLength( 20.0f );
			state.Body = null;
			state.Joint = null;
			state.Triggered = false;
			return;
		}

		if ( !held || state.Triggered ) { state.Triggered = held; return; }
		state.Triggered = true;
		var pose = GripPose( hand );
		var body = ClosestBody( pose.Position );
		if ( !body.IsValid() ) return;
		var controllers = Components.Get<VrControllers>();
		var anchor = controllers?.GrabAnchor( state.IsLeft, hand.IsHandTracked );
		if ( !anchor.IsValid() ) return;

		state.Body = body;
		state.Joint = Rinten.Physics.PhysicsJoint.CreateFixed(
			Rinten.Physics.PhysicsPoint.World( anchor, pose.Position, pose.Rotation ),
			Rinten.Physics.PhysicsPoint.World( body, pose.Position, body.Transform.Rotation ) );
		// The hand collider must not constantly push the object it is holding.
		state.Joint.Collisions = false;
		controllers.SetHolding( state.IsLeft, true );
		hand.TriggerHaptics( HapticEffect.SoftImpact, lengthScale: 0.3f, amplitudeScale: 0.35f );
	}

	private PhysicsBody ClosestBody( Vector3 at )
	{
		PhysicsBody best = null;
		var bestDistance = float.MaxValue;

		foreach ( var go in Scene.FindInPhysics( new Sphere( at, GrabReach ) ) )
		{
			var rigidbody = go.GetComponentInParent<Rigidbody>();
			var body = rigidbody?.PhysicsBody;
			if ( !body.IsValid() || body.BodyType != PhysicsBodyType.Dynamic ) continue;

			var distance = go.WorldPosition.DistanceSquared( at );
			if ( distance >= bestDistance ) continue;

			best = body;
			bestDistance = distance;
		}

		return best;
	}

	private static bool IsGrabbing( VRController hand )
	{
		if ( !hand.IsHandTracked ) return hand.Trigger.Value > 0.55f;

		var joints = hand.GetJoints( MotionRange.Hand );
		if ( joints is null || joints.Length < 26 ) return false;

		var thumb = HandJointWorld( joints, VRHandJoint.ThumbTip );
		var index = HandJointWorld( joints, VRHandJoint.IndexTip );
		return thumb.DistanceSquared( index ) < 0.0016f;
	}

	private static Transform GripPose( VRController hand )
	{
		if ( !hand.IsHandTracked ) return hand.Transform;

		var joints = hand.GetJoints( MotionRange.Hand );
		if ( joints is null || joints.Length < 26 ) return hand.Transform;

		var thumb = HandJointWorld( joints, VRHandJoint.ThumbTip );
		var index = HandJointWorld( joints, VRHandJoint.IndexTip );
		return new Transform( (thumb + index) * 0.5f, hand.Transform.Rotation );
	}

	private static Vector3 HandJointWorld( VRHandJointData[] joints, VRHandJoint joint )
	{
		var local = joints[(int)joint].Transform;
		return Input.VR.Anchor.ToWorld( local.WithPosition( local.Position * Input.VR.Scale ) ).Position;
	}

	private sealed class HandGrab
	{
		public PhysicsBody Body;
		public Rinten.Physics.FixedJoint Joint;
		public bool Triggered;
		public bool IsLeft;
	}
}
