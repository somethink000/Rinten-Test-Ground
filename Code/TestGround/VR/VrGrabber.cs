using Rinten.VR;

namespace TestGround;

/// <summary>
/// Picking things up. A controller grabs whatever is inside the blue sphere in
/// front of its trigger when the grip is squeezed; a tracked bare hand grabs
/// what its palm is on when it closes into a fist, or what its fingertips pinch.
/// </summary>
/// <remarks>
/// <para>
/// A held body is not joined to the hand. It is steered: every physics step its
/// velocity is set to reach the pose it should be in by the next one. So it
/// still collides - it stops against the table rather than going through it or
/// fighting a joint - and when it is let go it simply keeps the velocity it was
/// moving with, which is the throw.
/// </para>
/// <para>
/// Something with an <see cref="IVrHoldable"/> is handed over instead, and holds
/// itself - see VrBow and VrArrow. Those can also be given to a hand by
/// something other than a grab, with the button that lets them go: see
/// <see cref="Give"/>, which is how the quiver puts an arrow in it.
/// </para>
/// </remarks>
[Title( "VR Grabber" )]
[Category( "Test Ground" )]
[Icon( "back_hand" )]
public sealed class VrGrabber : Component
{
	[Property, Category( "Sphere" )] public float SphereRadius { get; set; } = 0.02f;

	/// <summary>
	/// Where the sphere sits in the left grip's own space: out in front of the
	/// trigger, where a finger would close on something. Placed by hand against
	/// the Touch Plus model, which is drawn in grip space. The right hand mirrors x.
	/// </summary>
	[Property, Category( "Sphere" )] public Vector3 SphereOffset { get; set; } = new( 0.0157f, -0.028f, -0.078f );

	[Property, Category( "Sphere" )] public Material SphereMaterial { get; set; }

	[Property, Category( "Buttons" )] public float Press { get; set; } = 0.6f;
	[Property, Category( "Buttons" )] public float Unpress { get; set; } = 0.35f;

	/// <summary>How far past the palm a closed hand reaches for something.</summary>
	[Property, Category( "Hands" )] public float PalmRadius { get; set; } = 0.06f;

	/// <summary>A held body further than this from where it should be has been wedged, and is let go.</summary>
	[Property] public float BreakDistance { get; set; } = 0.3f;

	private static readonly Color SphereIdle = new( 0.25f, 0.6f, 1.0f, 0.22f );
	private static readonly Color SphereHover = new( 0.35f, 0.75f, 1.0f, 0.5f );

	private readonly Grip left = new() { IsLeft = true };
	private readonly Grip right = new();

	private Grip Of( bool isLeft ) => isLeft ? left : right;

	/// <summary>The controller of a hand.</summary>
	public static VRController Hand( bool isLeft ) => isLeft ? Input.VR.LeftHand : Input.VR.RightHand;

	/// <summary>Whether a hand is holding anything at all.</summary>
	public bool IsBusy( bool isLeft ) => Of( isLeft ).Held.IsValid() || Of( isLeft ).Holdable is not null;

	/// <summary>What a hand is holding that holds itself, or null.</summary>
	public IVrHoldable Holding( bool isLeft ) => Of( isLeft ).Holdable;

	/// <summary>
	/// Put something in a hand that did not grab it, let go when <paramref name="button"/>
	/// comes up. Anything the hand held is dropped first.
	/// </summary>
	public bool Give( bool isLeft, IVrHoldable holdable, VrButton button )
	{
		var grip = Of( isLeft );
		LetGo( grip );

		if ( !holdable.Grab( this, isLeft ) ) return false;

		grip.Holdable = holdable;
		grip.Button = button;
		return true;
	}

	/// <summary>
	/// A holdable leaving a hand on its own - an arrow shot, a bow dropped by its
	/// other hand - without its release being called.
	/// </summary>
	public void Forget( IVrHoldable holdable )
	{
		foreach ( var grip in new[] { left, right } )
		{
			if ( grip.Holdable != holdable ) continue;

			grip.Holdable = null;
			grip.WasPressed = true; // the button still down is not a fresh grab
		}
	}

	protected override void OnStart()
	{
		SphereMaterial ??= Material.Load( "materials/vr/grab_sphere.mat" );
		left.Sphere = MakeSphere( "Left grab sphere" );
		right.Sphere = MakeSphere( "Right grab sphere" );
	}

	private ModelRenderer MakeSphere( string name )
	{
		var go = Scene.CreateObject();
		go.Name = name;
		go.Enabled = false;

		var renderer = go.Components.Create<ModelRenderer>();
		renderer.Model = Model.Sphere;
		renderer.MaterialOverride = SphereMaterial;
		renderer.RenderType = ModelRenderer.ShadowRenderType.Off;
		return renderer;
	}

	protected override void OnUpdate()
	{
		if ( !Game.IsRunningInVR || Input.VR is null ) return;

		UpdateGrip( left );
		UpdateGrip( right );
	}

	private void UpdateGrip( Grip grip )
	{
		var hand = Hand( grip.IsLeft );
		var frame = HoldFrame( grip.IsLeft );

		var busy = IsBusy( grip.IsLeft );
		var sphere = grip.Sphere;
		var showSphere = !hand.IsHandTracked && !busy;
		sphere.GameObject.Enabled = showSphere;

		if ( grip.Holdable is not null )
		{
			if ( !IsPressed( grip.IsLeft, grip.Button, true ) ) LetGo( grip );
			return;
		}

		if ( grip.Held.IsValid() )
		{
			if ( !IsPressed( grip.IsLeft, VrButton.Grip, true ) ) LetGo( grip );
			return;
		}

		var reach = GrabVolume( hand, frame );
		var (body, holdable) = Closest( reach );
		var any = body.IsValid() || holdable is not null;

		if ( showSphere )
		{
			sphere.WorldPosition = reach.Center;
			sphere.WorldRotation = Rotation.Identity;
			sphere.WorldScale = reach.Radius * 2.0f;
			sphere.Tint = any ? SphereHover : SphereIdle;
		}

		// Pressed now, not held down from before: squeezing on empty air and
		// sweeping into something should not pick it up.
		var wants = IsPressed( grip.IsLeft, VrButton.Grip, false );
		var pressed = wants && !grip.WasPressed;
		grip.WasPressed = wants;

		if ( !pressed || !any ) return;

		if ( holdable is not null )
		{
			// Something the other hand has changes hands.
			var other = Of( !grip.IsLeft );
			if ( other.Holdable == holdable ) LetGo( other );

			if ( !holdable.Grab( this, grip.IsLeft ) ) return;

			grip.Holdable = holdable;
			grip.Button = VrButton.Grip;
		}
		else
		{
			Take( grip, body, frame );
		}

		hand.TriggerHaptics( HapticEffect.SoftImpact, lengthScale: 0.3f, amplitudeScale: 0.35f );
	}

	private void Take( Grip grip, PhysicsBody body, Transform frame )
	{
		var other = Of( !grip.IsLeft );
		if ( other.Held == body ) LetGo( other );

		grip.Held = body;
		grip.Offset = frame.ToLocal( body.Transform );
		grip.HadGravity = body.GravityEnabled;
		body.GravityEnabled = false;
		body.Sleeping = false;

		Components.Get<VrControllers>()?.SetHolding( grip.IsLeft, true );
	}

	/// <summary>Whatever the hand has, let go of - a holdable told so, a body left its throw.</summary>
	private void LetGo( Grip grip )
	{
		if ( grip.Holdable is { } holdable )
		{
			grip.Holdable = null;
			holdable.Release( this, grip.IsLeft );
		}

		if ( grip.Held.IsValid() )
		{
			// The body keeps the velocity it was steered with: that is the throw.
			// Capped, because a hand lost for a frame can ask for anything.
			var body = grip.Held;
			body.Velocity = body.Velocity.ClampLength( 12.0f );
			body.AngularVelocity = body.AngularVelocity.ClampLength( 25.0f );
			body.GravityEnabled = grip.HadGravity;

			Components.Get<VrControllers>()?.SetHolding( grip.IsLeft, false );
		}

		grip.Held = null;

		// A button still down is not a fresh grab: an arrow let go with the
		// trigger while the grip is squeezed does not pick the next thing up.
		grip.WasPressed = true;
	}

	protected override void OnFixedUpdate()
	{
		if ( !Game.IsRunningInVR || Input.VR is null ) return;

		Steer( left );
		Steer( right );
	}

	/// <summary>The held body, sent towards where the hand says it should be.</summary>
	private void Steer( Grip grip )
	{
		var body = grip.Held;
		if ( !body.IsValid() ) return;

		var target = HoldFrame( grip.IsLeft ).ToWorld( grip.Offset );
		var step = Time.Delta;
		if ( step <= 0 ) return;

		var gap = target.Position - body.Position;

		if ( gap.Length > BreakDistance )
		{
			LetGo( grip );
			return;
		}

		body.Velocity = ( gap / step ).ClampLength( 20.0f );

		// Axis times radians per second. A quaternion and its negation are one
		// turn; the one with a positive w is the short way round.
		var delta = target.Rotation * body.Rotation.Inverse;
		if ( delta.w < 0 ) delta = new Rotation( -delta.x, -delta.y, -delta.z, -delta.w );

		var axis = new Vector3( delta.x, delta.y, delta.z );
		var angle = delta.Angle() * ( float.Pi / 180.0f );

		body.AngularVelocity = axis.Length > 0.0001f && angle > 0.0001f
			? ( axis.Normal * ( angle / step ) ).ClampLength( 40.0f )
			: Vector3.Zero;
	}

	/// <summary>
	/// Whether a hand is pressing a button, with room between press and release:
	/// <paramref name="holding"/> asks for the looser of the two.
	/// </summary>
	public bool IsPressed( bool isLeft, VrButton button, bool holding )
	{
		var hand = Hand( isLeft );

		if ( !hand.IsHandTracked )
		{
			var value = button == VrButton.Grip ? hand.Grip.Value : hand.Trigger.Value;
			return value > ( holding ? Unpress : Press );
		}

		var joints = hand.GetJoints( MotionRange.Hand );
		if ( joints is null || joints.Length < 26 ) return false;

		var palm = Joint( joints, VRHandJoint.Palm );
		var thumb = Joint( joints, VRHandJoint.ThumbTip );
		var index = Joint( joints, VRHandJoint.IndexTip );

		if ( button == VrButton.Trigger ) return thumb.Distance( index ) < ( holding ? 0.035f : 0.02f );

		// A fist: the long fingers' tips come back to the palm. A pinch holds as
		// well as a fist does, so a small thing can be picked up either way.
		var curl = ( palm.Distance( index ) + palm.Distance( Joint( joints, VRHandJoint.MiddleTip ) )
			+ palm.Distance( Joint( joints, VRHandJoint.RingTip ) ) ) / 3.0f;

		return curl < ( holding ? 0.085f : 0.065f ) || thumb.Distance( index ) < ( holding ? 0.035f : 0.02f );
	}

	/// <summary>The frame a held thing rides in: the grip, or the palm.</summary>
	public static Transform HoldFrame( bool isLeft )
	{
		var hand = Hand( isLeft );
		if ( !hand.IsHandTracked ) return hand.Transform.WithScale( 1 );

		var joints = hand.GetJoints( MotionRange.Hand );
		if ( joints is null || joints.Length < 26 ) return hand.Transform.WithScale( 1 );

		var palm = joints[(int)VRHandJoint.Palm].Transform;
		return Input.VR.Anchor.ToWorld( palm.WithPosition( palm.Position * Input.VR.Scale ) ).WithScale( 1 );
	}

	/// <summary>Where a grab looks for something: the sphere, the closing palm, or the pinch.</summary>
	private Sphere GrabVolume( VRController hand, Transform frame )
	{
		if ( !hand.IsHandTracked )
		{
			var offset = hand == Input.VR.LeftHand ? SphereOffset : SphereOffset.WithX( -SphereOffset.x );
			return new Sphere( frame.PointToWorld( offset ), SphereRadius );
		}

		var joints = hand.GetJoints( MotionRange.Hand );
		if ( joints is null || joints.Length < 26 ) return new Sphere( frame.Position, PalmRadius );

		var thumb = Joint( joints, VRHandJoint.ThumbTip );
		var index = Joint( joints, VRHandJoint.IndexTip );

		// A pinch is small and exact; a fist takes what the palm is on.
		if ( thumb.Distance( index ) < 0.035f ) return new Sphere( ( thumb + index ) * 0.5f, 0.03f );

		var middle = Joint( joints, VRHandJoint.MiddleProximal );
		return new Sphere( ( frame.Position + middle ) * 0.5f, PalmRadius );
	}

	/// <summary>
	/// The nearest thing inside the volume, by the point of it nearest the centre:
	/// a holdable whatever its body is doing, or a dynamic body to steer.
	/// </summary>
	private (PhysicsBody Body, IVrHoldable Holdable) Closest( Sphere volume )
	{
		PhysicsBody best = null;
		IVrHoldable bestHoldable = null;
		var bestDistance = float.MaxValue;

		foreach ( var go in Scene.FindInPhysics( volume ) )
		{
			var body = go.GetComponentInParent<Rigidbody>()?.PhysicsBody;
			if ( !body.IsValid() ) continue;
			if ( body == left.Held || body == right.Held ) continue;

			var holdable = go.GetComponentInParent<IVrHoldable>();
			if ( holdable is not null && ( holdable == left.Holdable || holdable == right.Holdable ) ) continue;
			if ( holdable is null && body.BodyType != PhysicsBodyType.Dynamic ) continue;

			var distance = body.FindClosestPoint( volume.Center ).DistanceSquared( volume.Center );
			if ( distance >= bestDistance ) continue;

			best = body;
			bestHoldable = holdable;
			bestDistance = distance;
		}

		return (bestHoldable is null ? best : null, bestHoldable);
	}

	private static Vector3 Joint( VRHandJointData[] joints, VRHandJoint joint )
	{
		var local = joints[(int)joint].Transform;
		return Input.VR.Anchor.ToWorld( local.WithPosition( local.Position * Input.VR.Scale ) ).Position;
	}

	private sealed class Grip
	{
		public bool IsLeft;
		public PhysicsBody Held;
		public Transform Offset;
		public bool HadGravity;
		public IVrHoldable Holdable;
		public VrButton Button;
		public bool WasPressed;
		public ModelRenderer Sphere;
	}
}
