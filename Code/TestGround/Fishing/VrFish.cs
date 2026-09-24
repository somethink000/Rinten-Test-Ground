using Rinten.VR;

namespace TestGround;

/// <summary>What a fish is up to - see <see cref="VrFish"/>.</summary>
public enum VrFishState
{
	/// <summary>Wandering the pond from one place to another.</summary>
	Swimming,

	/// <summary>A baited hook caught its eye; it is going to look.</summary>
	Approaching,

	/// <summary>Picking at the bait - the float bobs.</summary>
	Nibbling,

	/// <summary>It has the bait and is going with it - the float goes under. Strike now.</summary>
	Biting,

	/// <summary>Frightened, or away with the worm, fast.</summary>
	Fleeing,

	/// <summary>On the line in the water, fighting.</summary>
	Hooked,

	/// <summary>Out of the water: a body that flops, and a hand can take.</summary>
	Landed,
}

/// <summary>
/// A fish. In the water it moves itself - no physics - swimming from place to
/// place with its body waving; a baited hook near enough brings it over to
/// nibble, then bite, and a strike in that moment hooks it (see
/// <see cref="VrFishingRod.StrikeSpeed"/>). Hooked, it pulls away in bursts and
/// tires; reeled up out of the water it is a body again that hangs on the line,
/// flops, and can be taken by hand - which unhooks it. Dropped back in the pond
/// it swims off.
/// </summary>
/// <remarks>
/// The spine bones are rolled so their X is the fish's up, and turning them
/// about it swings the body side to side. The species is its numbers - <see cref="Weight"/>, <see cref="Strength"/>,
/// <see cref="Stamina"/> and the rest - and its model: the bones spine_0 .. spine_4
/// and tail it waves, its graph's parameter mouth (or the bone jaw), and the attachments mouth and hold (see
/// ~/Documents/Blender/tools/fishing/SPEC.md). Without them the head is taken to
/// be half of <see cref="BodyLength"/> forward and the whole model wags instead.
/// </remarks>
[Title( "VR Fish" )]
[Category( "Test Ground" )]
[Icon( "set_meal" )]
public sealed class VrFish : Component, IVrHoldable
{
	[Property] public SkinnedModelRenderer Renderer { get; set; }
	[Property] public Rigidbody Body { get; set; }

	/// <summary>The pond it lives in - the spawner sets it; otherwise whichever it starts in.</summary>
	[Property] public VrPond Pond { get; set; }

	[Property, Category( "Species" )] public string Species { get; set; } = "Perch";

	/// <summary>In kilograms.</summary>
	[Property, Category( "Species" )] public float Weight { get; set; } = 0.35f;

	/// <summary>Nose to tail, in metres.</summary>
	[Property, Category( "Species" )] public float BodyLength { get; set; } = 0.3f;

	/// <summary>How hard it pulls, fresh, in a burst, in newtons.</summary>
	[Property, Category( "Species" )] public float Strength { get; set; } = 7.0f;

	/// <summary>Seconds of pulling flat out before it is spent.</summary>
	[Property, Category( "Species" )] public float Stamina { get; set; } = 14.0f;

	/// <summary>Cruising speed, in metres a second.</summary>
	[Property, Category( "Species" )] public float SwimSpeed { get; set; } = 0.25f;

	/// <summary>Speed in a burst - fleeing, or fighting the line.</summary>
	[Property, Category( "Species" )] public float BurstSpeed { get; set; } = 1.3f;

	/// <summary>How near a baited hook has to be for it to notice.</summary>
	[Property, Category( "Feeding" )] public float NoticeRadius { get; set; } = 1.2f;

	/// <summary>The chance, having nibbled, that it takes the bait rather than wander off.</summary>
	[Property, Category( "Feeding" )] public float BiteChance { get; set; } = 0.75f;

	/// <summary>How long the float stays under - the time there is to strike.</summary>
	[Property, Category( "Feeding" )] public float BiteWindow { get; set; } = 1.8f;

	/// <summary>The chance that a bite not struck in time - or a strike too early - takes the worm with it.</summary>
	[Property, Category( "Feeding" )] public float StealChance { get; set; } = 0.6f;

	/// <summary>The chance that a single nibble takes the worm.</summary>
	[Property, Category( "Feeding" )] public float NibbleStealChance { get; set; } = 0.08f;

	/// <summary>Seconds after fleeing or feeding before it takes an interest again.</summary>
	[Property, Category( "Feeding" )] public float Wariness { get; set; } = 8.0f;

	/// <summary>Tail beats a second at cruising speed.</summary>
	[Property, Category( "Swimming" )] public float TailBeat { get; set; } = 2.2f;

	/// <summary>How far the tail swings, in degrees, at cruising speed.</summary>
	[Property, Category( "Swimming" )] public float Wag { get; set; } = 16.0f;

	/// <summary>How long it keeps flopping out of the water, in seconds.</summary>
	[Property, Category( "Swimming" )] public float FlopTime { get; set; } = 40.0f;

	public const string Tag = "vr_fish";

	public VrFishState State { get; private set; } = VrFishState.Swimming;

	/// <summary>Out of the water, a body.</summary>
	public bool Landed => State == VrFishState.Landed;

	/// <summary>Whether a hand has it.</summary>
	public bool IsHeld => grabber is not null;

	/// <summary>How much fight is left in it, nought to one.</summary>
	public float Energy { get; private set; } = 1.0f;

	/// <summary>The lip, where a hook sits, in the world - pointing the way the fish faces.</summary>
	public Transform Mouth
	{
		get
		{
			if ( Renderer.IsValid() && hasMouth && Renderer.GetAttachment( "mouth" ) is { } mouth ) return mouth.WithScale( 1 );
			return new Transform( WorldTransform.PointToWorld( mouthLocal ), WorldRotation );
		}
	}

	private sealed class Joint
	{
		public BoneCollection.Bone Bone;
		public Transform Relative;
		public float Amount;
	}

	private readonly List<Joint> spine = new();
	private Joint jaw;
	private Vector3 mouthLocal, holdLocal;
	private bool hasMouth;
	private Vector3 velocity;
	private Vector3 target;
	private TimeSince sinceTarget, sinceLook, sinceCalm = 100, sinceState, sinceFlop;
	private float nextFlop;
	private VrFishingHook hook;
	private int nibbles;
	private float nextNibble;
	private float phase, open, mouth;
	private bool gapes;
	private TimeSince sinceGape;
	private float nextGape = 4;
	private bool bursting;
	private float burstTime;
	private Vector3 burstDirection;
	private VrGrabber grabber;
	private bool heldLeft;
	private Transform heldOffset;
	private Rotation baseLook = Rotation.Identity;
	private GameObject wagged;

	protected override void OnStart()
	{
		Renderer ??= Components.Get<SkinnedModelRenderer>( FindMode.EverythingInSelfAndDescendants );
		Body ??= Components.Get<Rigidbody>();
		Pond ??= VrPond.At( Scene, WorldPosition );
		Tags.Add( Tag );

		var model = Renderer?.Model;
		var mouthRest = Renderer.IsValid() ? Renderer.GetAttachment( "mouth", false ) : null;
		hasMouth = mouthRest is not null;
		mouthLocal = mouthRest?.Position ?? Vector3.Forward * BodyLength * 0.5f;
		holdLocal = ( Renderer.IsValid() ? Renderer.GetAttachment( "hold", false )?.Position : null ) ?? Vector3.Zero;
		gapes = Renderer.IsValid() && Renderer.UseAnimGraph && Renderer.EffectiveAnimationGraph is not null;

		// The spine, head to tail, each further back swinging further.
		var bones = model?.Bones;
		string[] names = { "spine_0", "spine_1", "spine_2", "spine_3", "spine_4", "tail" };
		float[] amounts = { -0.12f, 0.1f, 0.25f, 0.45f, 0.7f, 1.0f };
		for ( var i = 0; i < names.Length; i++ )
		{
			var bone = bones?.GetBone( names[i] );
			if ( bone is null ) continue;
			spine.Add( new Joint { Bone = bone, Relative = Relative( bone ), Amount = amounts[i] } );
		}

		if ( bones?.GetBone( "jaw" ) is { } jawBone ) jaw = new Joint { Bone = jawBone, Relative = Relative( jawBone ) };

		// No bones: the whole model wags.
		if ( spine.Count == 0 && Renderer.IsValid() && Renderer.GameObject != GameObject )
		{
			wagged = Renderer.GameObject;
			baseLook = wagged.LocalRotation;
		}

		phase = Game.Random.Float( 0, 10 );
		SetBody( false );
		NewTarget();
	}

	/// <summary>
	/// A bone's rest on its parent, from the placed model before anything has
	/// turned it - in the model's space, where scale on the root comes out right.
	/// </summary>
	private Transform Relative( BoneCollection.Bone bone )
	{
		var rest = Rest( bone );
		return bone.Parent is null ? rest : Rest( bone.Parent ).ToLocal( rest );
	}

	private Transform Rest( BoneCollection.Bone bone ) =>
		Renderer.TryGetBoneTransformLocal( bone, out var tx ) ? tx : new Transform( Vector3.Zero );

	/// <summary>
	/// Swimming, it moves itself and touches nothing. Landed and loose, it falls.
	/// Touchable, it stays where it was put but the hand can still take it: a body
	/// with motion off is not in the physics query, so the collider has to stay live.
	/// </summary>
	private void SetBody( bool loose, bool touchable = false )
	{
		if ( Body.IsValid() )
		{
			Body.MotionEnabled = loose || touchable;
			Body.Gravity = loose;
			if ( loose ) Body.Velocity = velocity;
			else
			{
				Body.Velocity = 0;
				Body.AngularVelocity = 0;
			}
		}

		foreach ( var collider in Components.GetAll<Collider>( FindMode.EverythingInSelfAndDescendants ) )
			collider.Enabled = loose || touchable;
	}

	private void Enter( VrFishState state )
	{
		State = state;
		sinceState = 0;
	}

	protected override void OnUpdate()
	{
		var dt = Time.Delta;
		if ( dt <= 0 ) return;

		if ( IsHeld )
		{
			Held();
		}
		else if ( State == VrFishState.Landed )
		{
			Flop();
		}
		else if ( Pond.IsValid() )
		{
			Think( dt );
			Move( dt );
		}

		Animate( dt );
	}

	private void Think( float dt )
	{
		switch ( State )
		{
			case VrFishState.Swimming:
				if ( WorldPosition.Distance( target ) < 0.15f || sinceTarget > 8 ) NewTarget();
				if ( sinceLook > 0.5f ) Look();
				Steer( target, SwimSpeed, dt );
				break;

			case VrFishState.Approaching:
				if ( !Interested() ) { Flee( spooked: true ); break; }

				// Nose to the worm, slowing as it comes.
				var to = hook.Eye - WorldRotation * mouthLocal;
				var near = Mouth.Position.Distance( hook.Eye );
				Steer( to, SwimSpeed * ( near < 0.3f ? 0.4f : 0.8f ), dt );

				if ( near < 0.05f )
				{
					Enter( VrFishState.Nibbling );
					nibbles = Game.Random.Int( 2, 5 );
					nextNibble = Game.Random.Float( 0.3f, 0.8f );
				}
				else if ( sinceState > 12 ) Flee( spooked: false );
				break;

			case VrFishState.Nibbling:
				if ( !Interested() ) { Flee( spooked: true ); break; }
				Hold( dt );

				if ( sinceState > nextNibble )
				{
					sinceState = 0;
					nextNibble = Game.Random.Float( 0.5f, 1.2f );
					open = 1;
					Float?.Dip( 0.8f, 0.12f );

					if ( Game.Random.Float() < NibbleStealChance )
					{
						hook.SetBaited( false );
						Flee( spooked: false );
						break;
					}

					if ( --nibbles <= 0 )
					{
						if ( Game.Random.Float() < BiteChance ) Bite();
						else Flee( spooked: false );
					}
				}
				break;

			case VrFishState.Biting:
				if ( !Interested() ) { Flee( spooked: true ); break; }

				// Going with it, slowly down and away - the float under.
				Hold( dt );
				WorldPosition += ( WorldRotation.Forward + Vector3.Down * 0.5f ) * 0.05f * dt;

				if ( sinceState > BiteWindow )
				{
					if ( Game.Random.Float() < StealChance ) hook.SetBaited( false );
					Flee( spooked: false );
				}
				break;

			case VrFishState.Fleeing:
				Steer( target, BurstSpeed * ( sinceState < 1.0f ? 1.0f : 0.5f ), dt );
				if ( sinceState > 2.5f ) Enter( VrFishState.Swimming );
				break;

			case VrFishState.Hooked:
				Fight( dt );
				break;
		}
	}

	/// <summary>The float on the line this fish's hook hangs from.</summary>
	private VrFishingFloat Float => Line?.Float;

	private VrFishingLine Line => hook.IsValid()
		? Scene.GetAllComponents<VrFishingLine>().FirstOrDefault( x => x.Hook == hook )
		: null;

	/// <summary>Still worth it: the hook there, baited, in the water, not being dragged off.</summary>
	private bool Interested()
	{
		if ( !hook.IsValid() || hook.Claimant != this || !hook.Baited || !hook.InWater || hook.Fish is not null ) return false;

		// Already on the bait: the float going under is this fish pulling, not a reason to bolt.
		if ( State is VrFishState.Nibbling or VrFishState.Biting ) return true;

		return !hook.Body.IsValid() || hook.Body.Velocity.Length < 0.6f;
	}

	/// <summary>A look round for a baited hook, still in the water, that nobody else is after.</summary>
	private void Look()
	{
		sinceLook = 0;
		if ( sinceCalm < Wariness ) return;

		foreach ( var candidate in Scene.GetAllComponents<VrFishingHook>() )
		{
			if ( !candidate.Baited || !candidate.InWater || candidate.Claimant.IsValid() || candidate.Fish is not null ) continue;
			if ( candidate.Body.IsValid() && candidate.Body.Velocity.Length > 0.3f ) continue;
			if ( candidate.Eye.Distance( WorldPosition ) > NoticeRadius ) continue;

			hook = candidate;
			hook.Claimant = this;
			Enter( VrFishState.Approaching );
			return;
		}
	}

	/// <summary>The mouth kept on the hook, the fish turned a little about it.</summary>
	private void Hold( float dt )
	{
		var wanted = hook.Eye - WorldRotation * mouthLocal;
		WorldPosition = Vector3.Lerp( WorldPosition, wanted, 1.0f - System.MathF.Exp( -8.0f * dt ) );
		velocity = 0;
	}

	private void Bite()
	{
		Enter( VrFishState.Biting );
		open = 1;
		Float?.Dip( 3.0f, BiteWindow );
	}

	/// <summary>Off, fast, away from the hook - and not interested for a while.</summary>
	private void Flee( bool spooked )
	{
		if ( hook.IsValid() && hook.Claimant == this ) hook.Claimant = null;

		var from = hook.IsValid() ? hook.Eye : WorldPosition;
		var away = ( WorldPosition - from ).WithY( 0 );
		if ( away.Length < 0.01f ) away = WorldRotation.Forward;
		target = Pond.Clamp( WorldPosition + away.Normal * 2.0f + Vector3.Down * 0.2f, 0.15f );

		hook = null;
		sinceCalm = 0;
		sinceTarget = 0;
		Enter( spooked ? VrFishState.Fleeing : VrFishState.Swimming );
	}

	/// <summary>The rod jerked while this fish was at the bait: hooked if it was biting, off if it was only picking.</summary>
	public void Struck( VrFishingHook struck )
	{
		if ( struck != hook ) return;

		if ( State != VrFishState.Biting )
		{
			if ( Game.Random.Float() < StealChance ) hook.SetBaited( false );
			Flee( spooked: true );
			return;
		}

		// Caught: the worm is gone, whatever happens now.
		hook.Claimant = null;
		hook.SetBaited( false );
		hook.Attach( this );
		Float?.Dip( 0, 0 );
		Energy = 1;
		bursting = true;
		burstTime = 1.0f;
		burstDirection = AwayFromRod();
		Enter( VrFishState.Hooked );
	}

	private Vector3 AwayFromRod()
	{
		var rod = Line?.Rod;
		var away = rod.IsValid() ? ( WorldPosition - rod.Tip ).WithY( 0 ) : WorldRotation.Forward;
		if ( away.Length < 0.01f ) away = WorldRotation.Forward;
		return Rotation.FromYaw( Game.Random.Float( -70, 70 ) ) * away.Normal + Vector3.Down * Game.Random.Float( 0.1f, 0.5f );
	}

	/// <summary>
	/// On the line: runs away in bursts, weaker as it tires, held to the length of
	/// line out - which it takes more of when it pulls over the drag.
	/// </summary>
	private void Fight( float dt )
	{
		var line = Line;
		if ( !line.IsValid() || !hook.IsValid() || hook.Fish != this )
		{
			Unhook();
			Flee( spooked: true );
			return;
		}

		burstTime -= dt;
		if ( burstTime <= 0 )
		{
			bursting = !bursting && Game.Random.Float() < 0.3f + 0.7f * Energy;
			burstTime = bursting ? Game.Random.Float( 0.5f, 1.8f ) * ( 0.4f + Energy ) : Game.Random.Float( 0.8f, 2.5f );
			burstDirection = AwayFromRod();
		}

		var effort = 0.25f + 0.75f * Energy;
		var speed = ( bursting ? BurstSpeed : SwimSpeed * 1.5f ) * effort;
		velocity = Vector3.Lerp( velocity, burstDirection.Normal * speed, 1.0f - System.MathF.Exp( -3.0f * dt ) );

		var tip = line.Rod.IsValid() ? line.Rod.Tip : WorldPosition;
		var reeledIn = line.Length <= line.MinLength + 0.15f;

		// The pond keeps a swimming fish under the surface. A fish on a short line
		// is being lifted out, and that clamp was putting it straight back.
		var position = Pond.Clamp( WorldPosition + velocity * dt, 0.08f );
		if ( reeledIn ) position = position.WithY( ( WorldPosition + velocity * dt ).y );

		// Held to the line: whatever it cannot take off the reel it is pulled back.
		// Reeled right in, the leader no longer holds it half a metre under the
		// surface - it comes up to the tip.
		var mouth = position + WorldRotation * mouthLocal;
		var reach = line.Length + ( reeledIn ? 0.05f : line.LeaderLength );
		var delta = mouth - tip;
		var distance = delta.Length;

		if ( distance > reach )
		{
			var direction = delta / distance;
			var pull = Strength * effort * ( bursting ? 1.0f : 0.45f ) + Weight * 2.0f;
			var given = line.Give( distance - reach, pull );
			position -= direction * ( distance - reach - given );

			var outward = Vector3.Dot( velocity, direction );
			if ( outward > 0 ) velocity -= direction * outward;

			Energy -= dt / Stamina * ( bursting ? 1.0f : 0.4f );
		}
		else
		{
			Energy += dt / ( Stamina * 6.0f );
			if ( distance > reach - 0.1f ) line.Pull( Weight * 2.0f );
		}

		Energy = Energy.Clamp( 0, 1 );

		// Chosen in and under the rod: clear of the water in one step, not a climb
		// the next frame's clamp can undo.
		var underRod = ( position - tip ).WithY( 0 ).Length < 1.0f;
		if ( reeledIn && underRod )
			position = position.WithY( System.MathF.Max( position.y, Pond.SurfaceHeight + 0.15f ) );

		WorldPosition = position;

		// Head into the pull when it is not running, head away when it is.
		var facing = bursting ? velocity : -delta;
		if ( facing.Length > 0.01f ) Face( facing, dt, 6.0f );

		// Pulled up out of the water: landed, and a body on the line.
		if ( WorldPosition.y > Pond.SurfaceHeight + 0.02f )
		{
			Enter( VrFishState.Landed );
			// Still on the line, not a body that falls back into the pond. The
			// collider stays, so a hand can take it.
			SetBody( false, touchable: true );
			sinceFlop = 0;
			nextFlop = 0.4f;
		}
	}

	private void Unhook()
	{
		if ( hook.IsValid() && hook.Fish == this ) hook.Detach();
		hook = null;
	}

	private void NewTarget()
	{
		sinceTarget = 0;
		target = Pond.IsValid() ? Pond.RandomPoint( 0.25f, 0.15f, 0.85f ) : WorldPosition;
	}

	/// <summary>Towards a point at a speed, turning as a fish turns - not on the spot.</summary>
	private void Steer( Vector3 to, float speed, float dt )
	{
		var want = to - WorldPosition;
		var distance = want.Length;
		var desired = distance > 0.001f ? want / distance * System.MathF.Min( speed, distance * 2.0f ) : Vector3.Zero;
		velocity = Vector3.Lerp( velocity, desired, 1.0f - System.MathF.Exp( -2.0f * dt ) );
		if ( velocity.Length > 0.02f ) Face( velocity, dt, 3.0f );
	}

	private void Move( float dt )
	{
		if ( State is VrFishState.Hooked or VrFishState.Nibbling or VrFishState.Biting ) return;
		WorldPosition = Pond.Clamp( WorldPosition + velocity * dt, 0.08f );
	}

	/// <summary>Turned towards a direction, level-ish - a fish does not stand on its nose.</summary>
	private void Face( Vector3 direction, float dt, float rate )
	{
		var flat = direction.WithY( 0 );
		if ( flat.Length < 0.001f ) return;

		var pitch = System.MathF.Atan2( direction.y, flat.Length ).Clamp( -0.5f, 0.5f );
		var look = flat.Normal * System.MathF.Cos( pitch ) + Vector3.Up * System.MathF.Sin( pitch );
		WorldRotation = Rotation.Slerp( WorldRotation, Rotation.LookAt( look, Vector3.Up ), 1.0f - System.MathF.Exp( -rate * dt ) );
	}

	/// <summary>Out of the water: flops now and then, less as it goes - and back in the pond, swims off.</summary>
	private void Flop()
	{
		var pond = VrPond.At( Scene, WorldPosition );

		// Still hooked and reeled in: hang on the line, above the water. Falling
		// back in and being put on the hook again was the clip.
		if ( hook.IsValid() && hook.Fish == this && Line is { } held && held.Rod.IsValid() && held.Length <= held.MinLength + 0.3f )
		{
			var tip = held.Rod.Tip;
			var hang = tip + Vector3.Down * 0.3f;
			var surface = ( pond ?? Pond )?.SurfaceHeight ?? hang.y;
			if ( hang.y < surface + 0.12f ) hang = hang.WithY( surface + 0.15f );
			WorldPosition = hang;
			// Colliders stay on, or the hand has nothing to take. Motion stays off,
			// or it falls back into the pond.
			SetBody( false, touchable: true );
			return;
		}

		if ( pond is not null && pond.Depth( WorldPosition ) > 0.2f )
		{
			Pond = pond;
			SetBody( false );
			velocity = 0;

			if ( hook.IsValid() && hook.Fish == this )
			{
				Enter( VrFishState.Hooked );
				return;
			}

			pond.Splash( WorldPosition, 2.0f );
			Flee( spooked: true );
			return;
		}

		if ( !Body.IsValid() || sinceState > FlopTime ) return;

		if ( sinceFlop > nextFlop && Body.Velocity.Length < 0.5f )
		{
			sinceFlop = 0;
			nextFlop = Game.Random.Float( 0.5f, 1.5f ) * ( 1.0f + sinceState / FlopTime * 2.0f );
			var strength = 1.0f - sinceState / FlopTime;
			Body.ApplyImpulse( ( Vector3.Up * 1.6f + Vector3.Random.WithY( 0 ) * 0.5f ) * Body.Mass * strength );
			Body.AngularVelocity += WorldRotation.Forward * Game.Random.Float( -8, 8 ) * strength;
		}
	}

	/// <summary>Only out of the water; taken, it comes off the hook.</summary>
	public bool Grab( VrGrabber by, bool isLeft )
	{
		if ( State != VrFishState.Landed ) return false;

		Unhook();

		grabber = by;
		heldLeft = isLeft;
		SetBody( false );

		// Held where the hand closed on it, its belly in the palm.
		var frame = VrGrabber.HoldFrame( isLeft );
		heldOffset = frame.ToLocal( WorldTransform );
		heldOffset = heldOffset.WithPosition( -( heldOffset.Rotation * holdLocal ) );

		by.Components.Get<VrControllers>()?.SetHolding( isLeft, true );
		return true;
	}

	public void Release( VrGrabber by, bool isLeft )
	{
		by.Components.Get<VrControllers>()?.SetHolding( isLeft, false );
		grabber = null;

		Enter( VrFishState.Landed );
		velocity = Input.VR is not null ? VrGrabber.Hand( isLeft ).Velocity.ClampLength( 8.0f ) : Vector3.Zero;
		SetBody( true );
		sinceFlop = 0;
	}

	private void Held()
	{
		if ( Input.VR is null ) return;
		WorldTransform = VrGrabber.HoldFrame( heldLeft ).ToWorld( heldOffset );
	}

	/// <summary>The body waved: a wave down the spine, quicker and wider the faster it goes, wild in the air.</summary>
	private void Animate( float dt )
	{
		var speed = State == VrFishState.Landed ? 0 : ( Body.IsValid() && Body.MotionEnabled ? Body.Velocity.Length : velocity.Length );
		var effort = State switch
		{
			VrFishState.Landed => IsHeld ? 1.6f : ( sinceFlop < 0.4f ? 2.0f : 0.2f ),
			VrFishState.Hooked => 1.5f + ( bursting ? 1.0f : 0.0f ),
			VrFishState.Nibbling or VrFishState.Biting => 0.5f,
			_ => 0.4f + speed / System.MathF.Max( SwimSpeed, 0.01f ) * 0.6f,
		};

		phase += dt * TailBeat * System.MathF.PI * 2.0f * System.MathF.Min( effort, 3.0f );

		// The mouth: open on the bait and on the line and in the air, a gape now and then otherwise.
		if ( State is VrFishState.Biting or VrFishState.Hooked or VrFishState.Landed ) open = 1;
		else if ( sinceGape > nextGape )
		{
			sinceGape = 0;
			nextGape = Game.Random.Float( 3, 8 );
			open = 0.6f;
		}
		mouth = MathX.Lerp( mouth, open, 1.0f - System.MathF.Exp( -12.0f * dt ) );
		open = MathX.Approach( open, 0, dt * 2.5f );

		if ( gapes ) Renderer.Set( "mouth", mouth );
		var amplitude = Wag * System.MathF.Min( effort, 2.0f );

		if ( wagged.IsValid() )
		{
			wagged.LocalRotation = baseLook * Rotation.FromYaw( System.MathF.Sin( phase ) * amplitude * 0.3f );
			return;
		}

		if ( !Renderer.IsValid() ) return;

		for ( var i = 0; i < spine.Count; i++ )
		{
			var joint = spine[i];
			var angle = System.MathF.Sin( phase - i * 0.9f ) * amplitude * joint.Amount;
			Pose( joint, angle );
		}

		// No graph for it: the jaw drops about its X the negative way.
		if ( jaw is not null && !gapes ) Pose( jaw, -mouth * 34.0f );
	}

	/// <summary>A bone turned about its own X from where it rests on its parent.</summary>
	private void Pose( Joint joint, float degrees )
	{
		var relative = joint.Relative.WithRotation( joint.Relative.Rotation * Rotation.FromAxis( new Vector3( 1, 0, 0 ), degrees ) );
		var parentBone = joint.Bone.Parent;
		var parent = parentBone is not null && Renderer.TryGetBoneTransformLocal( parentBone, out var posed )
			? posed
			: new Transform( Vector3.Zero );
		Renderer.SetBoneTransform( joint.Bone, parent.ToWorld( relative ) );
	}
}
