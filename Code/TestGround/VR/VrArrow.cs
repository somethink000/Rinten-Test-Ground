using Rinten.VR;

namespace TestGround;

/// <summary>
/// An arrow: loose on the ground, in a hand, on a bow's string, in the air, or
/// stuck in something. Its origin is the nock and its point is along its forward.
/// </summary>
/// <remarks>
/// <para>
/// In the air it is not a physics body. It is flown here, a physics step at a
/// time - gravity on its velocity, its nose along its velocity - and the step
/// its point sweeps is traced before it is taken. So nothing thin is passed
/// through at speed, and where the trace stops is exactly where the point went
/// in: the arrow is put there, sunk a little, and fixed to what it hit.
/// </para>
/// <para>
/// A stuck arrow can be pulled out with the grip, and one lying about picked
/// up the same way - either is then in the hand, ready to nock.
/// </para>
/// </remarks>
[Title( "VR Arrow" )]
[Category( "Test Ground" )]
[Icon( "arrow_right_alt" )]
public sealed class VrArrow : Component, IVrHoldable
{
	public enum States { Loose, Held, Nocked, Flying, Stuck }

	[Property] public Rigidbody Body { get; set; }

	/// <summary>From nock to point, in metres.</summary>
	[Property] public float Length { get; set; } = 0.78f;

	/// <summary>How deep the point goes into what it hits.</summary>
	[Property] public float Penetration { get; set; } = 0.06f;

	/// <summary>Where the nock sits in the grip's space while the arrow is carried.</summary>
	[Property] public Vector3 HoldOffset { get; set; }

	/// <summary>How long a shot arrow flies before it is given up on, in seconds.</summary>
	[Property] public float FlightLife { get; set; } = 8.0f;

	public const string Tag = "vr_arrow";

	public States State { get; private set; } = States.Loose;

	/// <summary>Which hand has it, while one does.</summary>
	public bool HeldLeft { get; private set; }

	/// <summary>The nock, in the world.</summary>
	public Vector3 NockPosition => WorldPosition;

	/// <summary>The point, in the world.</summary>
	public Vector3 TipPosition => WorldPosition + WorldRotation.Forward * Length;

	private VrGrabber grabber;
	private VrBow bow;
	private Vector3 velocity;
	private TimeSince flying;

	protected override void OnStart()
	{
		Body ??= Components.Get<Rigidbody>();
		Tags.Add( Tag );
	}

	public bool Grab( VrGrabber by, bool isLeft )
	{
		if ( State == States.Flying ) return false;

		grabber = by;
		HeldLeft = isLeft;
		State = States.Held;

		// Out of whatever it was stuck in, and not a body while it is carried: it
		// would shove everything the hand swings it through.
		GameObject.SetParent( null, true );
		SetPhysics( false );

		Follow();
		return true;
	}

	public void Release( VrGrabber by, bool isLeft )
	{
		if ( State == States.Nocked && bow.IsValid() )
		{
			// Letting go of the string: the bow shoots it or drops it.
			bow.Loose();
			return;
		}

		Drop( VrGrabber.Hand( isLeft ).Velocity );
	}

	/// <summary>Let fall, as a body like any other, at a velocity.</summary>
	public void Drop( Vector3 at )
	{
		grabber?.Forget( this );
		grabber = null;
		bow = null;
		State = States.Loose;

		SetPhysics( true );
		if ( Body.IsValid() ) Body.Velocity = at.ClampLength( 10.0f );
	}

	/// <summary>Off the string and back in the hand that was drawing it - the bow was let go.</summary>
	public void Unnock()
	{
		if ( State != States.Nocked ) return;

		bow = null;
		State = States.Held;
	}

	/// <summary>Put on the string by the bow, which says where every frame from now on.</summary>
	public void PlaceOnString( Vector3 nock, Rotation rotation )
	{
		WorldPosition = nock;
		WorldRotation = rotation;
	}

	/// <summary>Shot: out of the hand and into the air at a velocity.</summary>
	public void Launch( Vector3 at, VrBow from )
	{
		grabber?.Forget( this );
		grabber = null;
		bow = from;
		velocity = at;
		flying = 0;
		State = States.Flying;

		SetPhysics( false );
	}

	protected override void OnUpdate()
	{
		if ( State != States.Held ) return;

		Follow();

		// Close enough to a drawn bow's string, held in the other hand, goes on it.
		foreach ( var candidate in Scene.GetAllComponents<VrBow>() )
		{
			if ( !candidate.TryNock( this, HeldLeft ) ) continue;

			bow = candidate;
			State = States.Nocked;
			break;
		}
	}

	/// <summary>Carried: the nock in the fingers, the point where the hand points.</summary>
	private void Follow()
	{
		var hand = VrGrabber.Hand( HeldLeft );
		var frame = VrGrabber.HoldFrame( HeldLeft );
		var aim = hand.AimTransform.Rotation;

		WorldPosition = frame.PointToWorld( HoldOffset );
		WorldRotation = Rotation.LookAt( aim.Forward, aim.Up );
	}

	protected override void OnFixedUpdate()
	{
		if ( State != States.Flying ) return;

		if ( flying > FlightLife )
		{
			GameObject.Destroy();
			return;
		}

		var step = Time.Delta;
		velocity += Scene.PhysicsWorld.Gravity * step;

		var from = TipPosition;
		var to = from + velocity * step;

		var hit = Scene.Trace.Ray( from, to )
			.IgnoreGameObjectHierarchy( GameObject )
			.WithoutTags( VrControllers.HandTag, VrBow.Tag, Tag )
			.Run();

		if ( hit.Hit )
		{
			Stick( hit );
			return;
		}

		var forward = velocity.Normal;
		WorldRotation = Rotation.LookAt( forward, WorldRotation.Up );
		WorldPosition = to - forward * Length;
	}

	/// <summary>In: the point sunk into what the trace found, and the arrow fixed to it.</summary>
	private void Stick( SceneTraceResult hit )
	{
		var forward = velocity.Normal;
		var tip = hit.HitPosition + forward * Penetration;

		WorldRotation = Rotation.LookAt( forward, WorldRotation.Up );
		WorldPosition = tip - forward * Length;
		State = States.Stuck;

		// Something that moves carries the arrow with it, and is pushed by it.
		if ( hit.Body.IsValid() && hit.Body.BodyType == PhysicsBodyType.Dynamic )
		{
			hit.Body.ApplyImpulseAt( hit.HitPosition, velocity * ( Body.IsValid() ? Body.Mass : 0.03f ) );
		}

		// Fixed to what carries what it hit: the body, where the hit thing moves,
		// or the root of it where nothing does. Not the collider's own object -
		// a post squashed to its shape by its scale would squash the arrow too.
		var mover = hit.GameObject?.GetComponentInParent<Rigidbody>() is { MotionEnabled: true } rb ? rb : null;
		var carrier = mover?.GameObject ?? hit.GameObject?.Root;
		if ( carrier.IsValid() ) GameObject.SetParent( carrier, true );

		// Grabbable where it stands - a collider on a body that does not move. On
		// something that moves the arrow is along for the ride and nothing more:
		// two bodies, one inside the other, fight.
		SetPhysics( false, collide: mover is null );

		hit.GameObject?.GetComponentInParent<VrTarget>()?.Hit( hit.HitPosition );
	}

	/// <summary>A body that falls, or one that stays where it is put - and whether it can be touched.</summary>
	private void SetPhysics( bool moving, bool collide = false )
	{
		// Asked before OnStart when the quiver hands over an arrow it has just made.
		Body ??= Components.Get<Rigidbody>();

		if ( Body.IsValid() )
		{
			Body.MotionEnabled = moving;
			if ( moving ) Body.Velocity = 0;
		}

		foreach ( var collider in Components.GetAll<Collider>( FindMode.EverythingInSelfAndDescendants ) )
			collider.Enabled = moving || collide;
	}
}
