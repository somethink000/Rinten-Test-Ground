using Rinten.VR;

namespace TestGround;

/// <summary>
/// A pistol. Taken with the grip it becomes the hand, as the bow does; the trigger
/// fires it, the lower face button (A or X) drops the magazine and the upper one
/// (B or Y) lets a locked slide forward. The other hand racks it by the back of
/// the slide, and feeds it magazines from the belt - see VrMagazine and VrBelt.
/// As a real one: it starts with an empty chamber, and has to be racked before it
/// fires; a new magazine does not chamber a round, the slide does.
/// </summary>
/// <remarks>
/// <para>
/// A shot is a trace from the muzzle, not a body: whatever it finds is pushed,
/// marked and told - a target scores it. The flash is the pistol's shot effect,
/// played at the muzzle; the case is a body of its own, thrown out of the port
/// (see VrShell) - and so is a whole round, racked out unfired.
/// </para>
/// <para>
/// Everything the pistol knows about its own shape comes from its model: the
/// attachments muzzle and magazine, the morphs slide, trigger and mag_release, and
/// the body group magazine (loaded, empty, none) - see ~/Documents/Blender/tools/weapons/build_pistol.py.
/// </para>
/// </remarks>
[Title( "VR Pistol" )]
[Category( "Test Ground" )]
[Icon( "gps_fixed" )]
public sealed class VrPistol : Component, IVrHoldable
{
	[Property] public SkinnedModelRenderer Renderer { get; set; }
	[Property] public Rigidbody Body { get; set; }

	/// <summary>The back of the slide, which the other hand racks - on only while the pistol is held.</summary>
	[Property] public VrPistolSlide Slide { get; set; }

	/// <summary>A turn on top of how the pistol sits in the hand, for tuning - see <see cref="InHand"/>.</summary>
	[Property, Category( "Hold" )] public Angles HoldAngles { get; set; }
	[Property, Category( "Hold" )] public Vector3 HoldOffset { get; set; }

	[Property, Category( "Ammunition" )] public PrefabFile MagazinePrefab { get; set; }

	/// <summary>Rounds in the magazine it starts with; below zero starts with none.</summary>
	[Property, Category( "Ammunition" )] public int StartRounds { get; set; } = 17;

	/// <summary>Whether it starts with a round in the chamber, or has to be racked first.</summary>
	[Property, Category( "Ammunition" )] public bool StartChambered { get; set; }

	/// <summary>What the port throws out: a fired case, and a round racked out unfired.</summary>
	[Property, Category( "Ammunition" )] public PrefabFile CasingPrefab { get; set; }
	[Property, Category( "Ammunition" )] public PrefabFile RoundPrefab { get; set; }

	[Property, Category( "Shooting" )] public ParticleDefinition ShotEffect { get; set; }
	[Property, Category( "Shooting" )] public ParticleDefinition ImpactEffect { get; set; }
	[Property, Category( "Shooting" )] public float Range { get; set; } = 150.0f;

	/// <summary>The push a round gives what it hits, in kilogram metres a second.</summary>
	[Property, Category( "Shooting" )] public float Impulse { get; set; } = 6.0f;

	/// <summary>How far the muzzle flips up on a shot, in degrees, before it settles.</summary>
	[Property, Category( "Shooting" )] public float Kick { get; set; } = 9.0f;

	[Property, Category( "Sounds" )] public SoundEvent ShotSound { get; set; }
	[Property, Category( "Sounds" )] public SoundEvent DryFireSound { get; set; }
	[Property, Category( "Sounds" )] public SoundEvent SlideBackSound { get; set; }
	[Property, Category( "Sounds" )] public SoundEvent SlideForwardSound { get; set; }
	[Property, Category( "Sounds" )] public SoundEvent MagazineOutSound { get; set; }
	[Property, Category( "Sounds" )] public SoundEvent MagazineInSound { get; set; }

	public const string Tag = "vr_pistol";

	/// <summary>Whether a hand has it, and which.</summary>
	public bool IsHeld => grabber is not null;
	public bool HeldLeft { get; private set; }

	public bool HasMagazine { get; private set; }

	/// <summary>Rounds left in the magazine, not counting the one in the chamber.</summary>
	public int Rounds { get; private set; }

	public bool Chambered { get; private set; }

	/// <summary>Held back on an empty magazine, until it is let forward.</summary>
	public bool SlideLocked { get; private set; }

	/// <summary>
	/// How the pistol sits in the grip's space for a tracked bare hand, which has
	/// no aim of its own to follow: its grip up the grip's tube, which runs up
	/// through a closed fist, and its barrel out past the trigger finger, the
	/// grip's down - the same frame the bow is held in.
	/// </summary>
	private Rotation InHand
	{
		get
		{
			var along = magazine.Rotation.Up;
			var barrel = ( Vector3.Forward - along * Vector3.Dot( Vector3.Forward, along ) ).Normal;
			var pistol = Rotation.LookAt( barrel, along );
			return Rotation.LookAt( new Vector3( 0, -1, 0 ), new Vector3( 0, 0, -1 ) ) * pistol.Inverse;
		}
	}

	private VrGrabber grabber;
	private Transform muzzle = new( new Vector3( 0, 0.0587f, -0.1534f ) );
	private Transform magazine = new( new Vector3( 0, -0.0514f, 0.0197f ), Rotation.FromPitch( 21 ) );
	private Transform port = new( new Vector3( 0.005f, 0.0683f, -0.0474f ) );
	private bool triggerReset = true;
	private bool wasRelease, wasSlideStop;
	private float cycle = 1.0f;   // how far through the slide's last trip, nought to one
	private float rack;           // how far back the other hand has the slide
	private float kick;           // how far up the muzzle has flipped, nought to one
	private float releasePulse;

	protected override void OnStart()
	{
		Renderer ??= Components.Get<SkinnedModelRenderer>();
		Body ??= Components.Get<Rigidbody>();
		Slide ??= Components.Get<VrPistolSlide>( FindMode.EverythingInDescendants );
		MagazinePrefab ??= PrefabFile.Load( "prefabs/vr/pistol/magazine.prefab" );
		CasingPrefab ??= PrefabFile.Load( "prefabs/vr/pistol/casing.prefab" );
		RoundPrefab ??= PrefabFile.Load( "prefabs/vr/pistol/round.prefab" );
		ShotEffect ??= ResourceLibrary.Get<ParticleDefinition>( "fx/weapons/pistol_shot.fx" );
		ShotSound ??= ResourceLibrary.Get<SoundEvent>( "sounds/weapons/pistol/shot.sound" );
		DryFireSound ??= ResourceLibrary.Get<SoundEvent>( "sounds/weapons/pistol/dry_fire.sound" );
		SlideBackSound ??= ResourceLibrary.Get<SoundEvent>( "sounds/weapons/pistol/slide_back.sound" );
		SlideForwardSound ??= ResourceLibrary.Get<SoundEvent>( "sounds/weapons/pistol/slide_forward.sound" );
		MagazineOutSound ??= ResourceLibrary.Get<SoundEvent>( "sounds/weapons/pistol/mag_out.sound" );
		MagazineInSound ??= ResourceLibrary.Get<SoundEvent>( "sounds/weapons/pistol/mag_in.sound" );
		ImpactEffect ??= ResourceLibrary.Get<ParticleDefinition>( "fx/combat/bullet_impact.fx" );
		Tags.Add( Tag );

		var model = Renderer?.Model;
		if ( model?.GetAttachment( "muzzle" ) is { } m ) muzzle = m;
		if ( model?.GetAttachment( "magazine" ) is { } g ) magazine = g;
		if ( model?.GetAttachment( "eject" ) is { } e ) port = e;

		HasMagazine = StartRounds >= 0;
		Rounds = System.Math.Max( StartRounds, 0 );
		Chambered = StartChambered;

		if ( Slide.IsValid() ) Slide.GameObject.Enabled = false;
		ShowMagazine();
	}

	/// <summary>The other hand, reaching for a held pistol, takes its slide.</summary>
	public IVrHoldable ReachedFor( bool isLeft )
		=> IsHeld && HeldLeft != isLeft && Slide.IsValid() ? Slide : this;

	public bool Grab( VrGrabber by, bool isLeft )
	{
		grabber = by;
		HeldLeft = isLeft;
		triggerReset = false; // the squeeze that may still be on is not a shot
		wasRelease = wasSlideStop = true;

		SetPhysics( false );

		var controllers = by.Components.Get<VrControllers>();
		controllers?.SetHidden( isLeft, true );
		controllers?.SetHolding( isLeft, true );

		Follow();
		return true;
	}

	public void Release( VrGrabber by, bool isLeft )
	{
		var controllers = by.Components.Get<VrControllers>();
		controllers?.SetHidden( isLeft, false );
		controllers?.SetHolding( isLeft, false );

		grabber = null;
		rack = 0;
		kick = 0;
		Slide?.LetGo();

		SetPhysics( true );
		if ( Body.IsValid() ) Body.Velocity = VrGrabber.Hand( isLeft ).Velocity.ClampLength( 10.0f );
	}

	/// <summary>
	/// Held, a body that stays where the hand puts it and does not collide - the
	/// other hand reaches the slide rather than the frame - and loose, one that falls.
	/// </summary>
	private void SetPhysics( bool loose )
	{
		if ( Body.IsValid() )
		{
			Body.MotionEnabled = loose;
			if ( loose ) Body.Velocity = 0;
		}

		foreach ( var collider in Components.GetAll<Collider>( FindMode.EverythingInSelfAndDescendants ) )
		{
			if ( Slide.IsValid() && collider.GameObject == Slide.GameObject ) continue;
			collider.Enabled = loose;
		}

		if ( Slide.IsValid() ) Slide.GameObject.Enabled = !loose;
	}

	protected override void OnUpdate()
	{
		if ( IsHeld && Game.IsRunningInVR && Input.VR is not null )
		{
			Controls();
			Follow();
		}

		Animate();
	}

	private void Controls()
	{
		var hand = VrGrabber.Hand( HeldLeft );

		// The trigger: a shot when it breaks, another only once it has come back.
		var pull = hand.IsHandTracked ? ( grabber.IsPressed( HeldLeft, VrButton.Trigger, false ) ? 1.0f : 0.0f ) : hand.Trigger.Value;
		Renderer?.Morphs.Set( "trigger", pull, 0 );

		if ( pull < 0.4f ) triggerReset = true;
		if ( pull > 0.85f && triggerReset )
		{
			triggerReset = false;
			Fire();
		}

		// Face buttons act as they go down.
		var release = hand.ButtonA.IsPressed;
		if ( release && !wasRelease ) DropMagazine();
		wasRelease = release;

		var slideStop = hand.ButtonB.IsPressed;
		if ( slideStop && !wasSlideStop ) LetSlideForward();
		wasSlideStop = slideStop;
	}

	/// <summary>
	/// The pistol where the hand holding it is: its grip in the fist and its barrel
	/// down the controller's aim, where a pointer from it would point - the muzzle
	/// flipped up by the last shot.
	/// </summary>
	private void Follow()
	{
		var hand = VrGrabber.Hand( HeldLeft );
		var frame = VrGrabber.HoldFrame( HeldLeft );
		Transform held;

		if ( hand.IsHandTracked )
		{
			held = frame.ToWorld( new Transform( HoldOffset, InHand * HoldAngles.ToRotation() ) );
		}
		else
		{
			var aim = hand.AimTransform.Rotation;
			var rotation = Rotation.LookAt( aim.Forward, aim.Up ) * HoldAngles.ToRotation();
			held = new Transform( frame.PointToWorld( HoldOffset ), rotation );
		}

		// Recoil: up about the grip, and a little back into the hand.
		var flip = Rotation.FromAxis( held.Rotation.Right, Kick * kick );
		held = held.WithRotation( flip * held.Rotation ).WithPosition( held.Position + held.Rotation.Backward * 0.012f * kick );
		WorldTransform = held;
	}

	private void Animate()
	{
		kick = MathX.Approach( kick, 0, Time.Delta * 9.0f );
		cycle = MathX.Approach( cycle, 1, Time.Delta / 0.09f );
		releasePulse = MathX.Approach( releasePulse, 0, Time.Delta * 6.0f );

		// Back fast and home a little slower; held back when locked, or where the hand has it.
		var trip = cycle < 0.35f ? cycle / 0.35f : 1.0f - ( cycle - 0.35f ) / 0.65f;
		var slide = SlideLocked ? 1.0f : trip;
		if ( rack > 0 ) slide = System.MathF.Max( slide, rack );

		Renderer?.Morphs.Set( "slide", slide, 0 );
		Renderer?.Morphs.Set( "mag_release", releasePulse, 0 );
		if ( !IsHeld ) Renderer?.Morphs.Set( "trigger", 0, 0 );
	}

	/// <summary>A pull of the trigger: a shot if there is a round in the chamber, a click if there is not.</summary>
	public void Fire()
	{
		if ( !Chambered || SlideLocked || rack > 0.1f )
		{
			// The striker falls on nothing - unless the slide is back, when it does not fall at all.
			if ( !SlideLocked && rack <= 0.1f ) Play( DryFireSound );
			Buzz( HapticEffect.SoftImpact, 0.1f, 0.2f );
			return;
		}

		Chambered = false;

		var from = WorldTransform.ToWorld( muzzle );
		Shoot( from.Position, from.Rotation.Forward );

		if ( ShotEffect is not null )
		{
			var fx = Scene.CreateObject();
			fx.Name = "Gunshot";
			fx.WorldTransform = from.WithScale( 1 );
			var player = fx.Components.Create<ParticlePlayer>();
			player.Definition = ShotEffect;
			player.PlayOnce = true;
			player.DestroyOnEnd = true;
		}

		Play( ShotSound );
		Eject( CasingPrefab );

		// The slide comes back, throws the case out and takes the next round up -
		// or stays back on an empty magazine.
		cycle = 0;
		kick = 1;
		Feed( lockWhenEmpty: true );

		Buzz( HapticEffect.HardImpact, 0.35f, 1.0f );
	}

	private void Play( SoundEvent sound )
	{
		if ( sound is not null ) Sound.Play( sound, WorldPosition );
	}

	/// <summary>
	/// A case or a round out of the port: to the right, up and a little back, with
	/// a tumble - and with the hand's own movement, so it leaves a swung pistol as
	/// it would.
	/// </summary>
	private void Eject( PrefabFile prefab )
	{
		if ( prefab is null ) return;

		var at = WorldTransform.ToWorld( port );
		var rotation = WorldRotation * Rotation.FromYaw( 90 + Game.Random.Float( -20, 20 ) );
		var go = GameObject.Clone( prefab, new Transform( at.Position, rotation ) );

		var body = go.Components.Get<Rigidbody>();
		if ( !body.IsValid() ) return;

		var carried = IsHeld && Input.VR is not null ? VrGrabber.Hand( HeldLeft ).Velocity : Vector3.Zero;
		body.Velocity = carried
			+ WorldRotation.Right * Game.Random.Float( 1.8f, 2.6f )
			+ WorldRotation.Up * Game.Random.Float( 1.2f, 1.9f )
			+ WorldRotation.Backward * Game.Random.Float( 0.2f, 0.6f );
		body.AngularVelocity = Vector3.Random * 40.0f;
	}

	/// <summary>A buzz in the hand holding it, if one is.</summary>
	private void Buzz( HapticEffect effect, float length, float amplitude )
	{
		if ( !IsHeld || Input.VR is null ) return;
		VrGrabber.Hand( HeldLeft ).TriggerHaptics( effect, lengthScale: length, amplitudeScale: amplitude );
	}

	/// <summary>The next round into the chamber, if the magazine has one; the slide held back if it is empty.</summary>
	private void Feed( bool lockWhenEmpty )
	{
		if ( HasMagazine && Rounds > 0 )
		{
			Rounds--;
			Chambered = true;
			SlideLocked = false;
		}
		else if ( HasMagazine && lockWhenEmpty )
		{
			SlideLocked = true;
		}

		ShowMagazine();
	}

	/// <summary>A round down the line from the muzzle: whatever it meets is pushed, marked and scored.</summary>
	private void Shoot( Vector3 from, Vector3 direction )
	{
		var hit = Scene.Trace.Ray( from, from + direction * Range )
			.IgnoreGameObjectHierarchy( GameObject )
			.WithoutTags( VrControllers.HandTag, VrMagazine.Tag )
			.Run();

		if ( !hit.Hit ) return;

		if ( hit.Body.IsValid() && hit.Body.BodyType == PhysicsBodyType.Dynamic )
			hit.Body.ApplyImpulseAt( hit.HitPosition, direction * Impulse );

		if ( ImpactEffect is not null )
		{
			var fx = Scene.CreateObject();
			fx.Name = "Bullet impact";
			fx.WorldPosition = hit.HitPosition;
			fx.WorldRotation = Rotation.LookAt( hit.Normal );
			var player = fx.Components.Create<ParticlePlayer>();
			player.Definition = ImpactEffect;
			player.PlayOnce = true;
			player.DestroyOnEnd = true;
		}

		VrBulletHoles.Mark( Scene, hit );
		hit.GameObject?.GetComponentInParent<VrTarget>()?.Hit( hit.HitPosition );
	}

	/// <summary>The magazine out of the grip, falling, with what is left in it.</summary>
	public void DropMagazine()
	{
		if ( !HasMagazine ) return;

		releasePulse = 1;

		if ( MagazinePrefab is not null )
		{
			var at = WorldTransform.ToWorld( magazine ).WithScale( 1 );
			var go = GameObject.Clone( MagazinePrefab, at );
			var dropped = go.Components.Get<VrMagazine>();
			dropped?.Fill( Rounds );

			var body = go.Components.Get<Rigidbody>();
			if ( body.IsValid() )
				body.Velocity = ( IsHeld ? VrGrabber.Hand( HeldLeft ).Velocity : Vector3.Zero ) + at.Rotation.Down * 0.6f;
		}

		HasMagazine = false;
		Rounds = 0;
		ShowMagazine();
		Play( MagazineOutSound );

		Buzz( HapticEffect.SoftImpact, 0.15f, 0.4f );
	}

	/// <summary>Where a magazine goes in, in the world: its base plate, pointing up the grip.</summary>
	public Transform MagazineWell => WorldTransform.ToWorld( magazine );

	/// <summary>Whether a magazine could go in now.</summary>
	public bool TakesMagazine => IsHeld && !HasMagazine;

	/// <summary>
	/// A magazine pushed home. Nothing is chambered by it: the slide does that,
	/// racked or let forward off the slide stop.
	/// </summary>
	public void Insert( int rounds )
	{
		HasMagazine = true;
		Rounds = rounds;

		ShowMagazine();
		Play( MagazineInSound );
		Buzz( HapticEffect.HardImpact, 0.15f, 0.6f );
	}

	/// <summary>A locked slide let forward, chambering a round if there is one.</summary>
	public void LetSlideForward()
	{
		if ( !SlideLocked ) return;

		SlideLocked = false;
		cycle = 0.35f; // from all the way back, home
		Feed( lockWhenEmpty: false );
		Play( SlideForwardSound );
	}

	/// <summary>How far back the other hand has the slide, nought to one - see VrPistolSlide.</summary>
	public void Rack( float amount ) => rack = amount.Clamp( 0, 1 );

	/// <summary>Let go short of all the way back: the slide goes home and nothing is fed - or, locked, it was never moved.</summary>
	public void RackedShort()
	{
		if ( rack > 0.2f && !SlideLocked ) Play( SlideForwardSound );
		rack = 0;
	}

	/// <summary>
	/// The slide pulled all the way back and let go: whatever was in the chamber
	/// is thrown out and the next round taken up.
	/// </summary>
	public void Racked()
	{
		rack = 0;
		cycle = 0.35f;

		if ( Chambered ) Eject( RoundPrefab );
		Chambered = false;
		SlideLocked = false;
		Feed( lockWhenEmpty: true );
		Play( SlideForwardSound );
	}

	/// <summary>The slide has come all the way back under the hand.</summary>
	public void RackedBack() => Play( SlideBackSound );

	/// <summary>The magazine in the grip as the body group has it: with rounds on top, without, or none.</summary>
	private void ShowMagazine()
	{
		Renderer?.SetBodyGroup( "magazine", !HasMagazine ? "none" : Rounds > 0 ? "loaded" : "empty" );
	}
}

/// <summary>
/// The back of a held pistol's slide, for the other hand: squeezed with the grip
/// and pulled back, then let go, it racks the pistol - see <see cref="VrPistol.Racked"/>.
/// </summary>
[Title( "VR Pistol Slide" )]
[Category( "Test Ground" )]
[Icon( "swipe_left" )]
public sealed class VrPistolSlide : Component, IVrHoldable
{
	[Property] public VrPistol Pistol { get; set; }

	/// <summary>How far the slide travels, in metres.</summary>
	[Property] public float Travel { get; set; } = 0.028f;

	private bool holding;
	private bool left;
	private Vector3 start;
	private bool back;

	protected override void OnStart()
	{
		Pistol ??= GameObject.Parent?.GetComponentInParent<VrPistol>();
	}

	public bool Grab( VrGrabber by, bool isLeft )
	{
		if ( !Pistol.IsValid() || !Pistol.IsHeld || Pistol.HeldLeft == isLeft ) return false;

		holding = true;
		left = isLeft;
		back = false;
		start = Pistol.WorldTransform.PointToLocal( VrGrabber.HoldFrame( isLeft ).Position );
		return true;
	}

	public void Release( VrGrabber by, bool isLeft )
	{
		if ( !holding ) return;

		holding = false;
		if ( !Pistol.IsValid() ) return;

		if ( back ) Pistol.Racked();
		else Pistol.RackedShort();
	}

	/// <summary>The pistol left the hand while the slide was held.</summary>
	public void LetGo()
	{
		holding = false;
		back = false;
	}

	protected override void OnUpdate()
	{
		if ( !holding || !Pistol.IsValid() ) return;

		// Back along the pistol's own length, in its space, so a pistol that turns
		// under the hand does not rack itself.
		var now = Pistol.WorldTransform.PointToLocal( VrGrabber.HoldFrame( left ).Position );
		var pulled = ( ( now.z - start.z ) / Travel ).Clamp( 0, 1 );
		Pistol.Rack( pulled );

		if ( pulled > 0.9f && !back )
		{
			back = true;
			Pistol.RackedBack();
			VrGrabber.Hand( left ).TriggerHaptics( HapticEffect.SoftImpact, lengthScale: 0.15f, amplitudeScale: 0.5f );
		}
	}
}
