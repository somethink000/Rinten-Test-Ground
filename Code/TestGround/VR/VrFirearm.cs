using Rinten.VR;

namespace TestGround;

/// <summary>How a firearm answers a trigger held down.</summary>
public enum VrFireMode
{
	/// <summary>One shot a pull; the trigger has to come back before the next.</summary>
	Semi,

	/// <summary>Shots for as long as the trigger is held, at <see cref="VrFirearm.RoundsPerMinute"/>.</summary>
	Auto,
}

/// <summary>
/// A firearm - the pistol and the AKM are both this, set up differently. Taken
/// by its grip it becomes the hand, as the bow does; the trigger fires it, the
/// lower face button (A or X) drops the magazine and the upper one (B or Y) lets
/// a locked action forward. The other hand works its parts - a slide to rack, a
/// foregrip to steady it - see <see cref="VrFirearmPart"/>; and feeds it
/// magazines of its own cartridge from the belt - see VrMagazine and VrBelt.
/// </summary>
/// <remarks>
/// <para>
/// A shot is a trace from the muzzle, not a body: whatever it finds is pushed,
/// marked and told - a target scores it. The flash is the shot effect, played at
/// the muzzle; the case is a body of its own, thrown out of the port (see
/// VrShell) - and so is a whole round, racked out unfired.
/// </para>
/// <para>
/// Everything a firearm knows about its own shape comes from its model: the
/// attachments muzzle, eject and magazine, the morphs slide, trigger and
/// mag_release, and the body group magazine (loaded, empty, none) - see
/// ~/Documents/Blender/tools/weapons/build_pistol.py and build_akm.py.
/// </para>
/// </remarks>
[Title( "VR Firearm" )]
[Category( "Test Ground" )]
[Icon( "gps_fixed" )]
public sealed class VrFirearm : Component, IVrHoldable
{
	[Property] public SkinnedModelRenderer Renderer { get; set; }
	[Property] public Rigidbody Body { get; set; }

	/// <summary>A turn on top of how it sits in the hand, for tuning - see <see cref="InHand"/>.</summary>
	[Property, Category( "Hold" )] public Angles HoldAngles { get; set; }
	[Property, Category( "Hold" )] public Vector3 HoldOffset { get; set; }

	/// <summary>How far the grip leans back from the bore's up, in degrees: a bare hand holds it along the grip.</summary>
	[Property, Category( "Hold" )] public float GripAngle { get; set; } = 21.0f;

	[Property, Category( "Action" )] public VrFireMode FireMode { get; set; } = VrFireMode.Semi;
	[Property, Category( "Action" )] public float RoundsPerMinute { get; set; } = 600.0f;

	/// <summary>Whether the action stays open on the last round, as a pistol's slide does and an AK's bolt does not.</summary>
	[Property, Category( "Action" )] public bool LocksOpenWhenEmpty { get; set; } = true;

	/// <summary>Whether a magazine pushed home chambers a round by itself - for a firearm with nothing to rack.</summary>
	[Property, Category( "Action" )] public bool ChambersOnInsert { get; set; }

	/// <summary>What it fires; only magazines of the same cartridge go in - see <see cref="VrMagazine.Cartridge"/>.</summary>
	[Property, Category( "Ammunition" )] public string Cartridge { get; set; } = "9x19";

	/// <summary>Its magazine: dropped out of it, and handed out by the belt while it is held.</summary>
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

	/// <summary>How much of the kick is left with the other hand on the foregrip.</summary>
	[Property, Category( "Shooting" )] public float SteadiedKick { get; set; } = 0.4f;

	[Property, Category( "Sounds" )] public SoundEvent ShotSound { get; set; }
	[Property, Category( "Sounds" )] public SoundEvent DryFireSound { get; set; }
	[Property, Category( "Sounds" )] public SoundEvent SlideBackSound { get; set; }
	[Property, Category( "Sounds" )] public SoundEvent SlideForwardSound { get; set; }
	[Property, Category( "Sounds" )] public SoundEvent MagazineOutSound { get; set; }
	[Property, Category( "Sounds" )] public SoundEvent MagazineInSound { get; set; }

	public const string Tag = "vr_firearm";

	/// <summary>Whether a hand has it by the grip, and which.</summary>
	public bool IsHeld => grabber is not null;
	public bool HeldLeft { get; private set; }

	public bool HasMagazine { get; private set; }

	/// <summary>Rounds left in the magazine, not counting the one in the chamber.</summary>
	public int Rounds { get; private set; }

	public bool Chambered { get; private set; }

	/// <summary>Held back on an empty magazine, until it is let forward.</summary>
	public bool SlideLocked { get; private set; }

	/// <summary>The other hand is on the foregrip, and aims it with the first.</summary>
	public bool Steadied => Parts.Any( x => x is VrFirearmForegrip { IsHeld: true } );

	/// <summary>What the other hand can take while it is held: a slide, a foregrip.</summary>
	public IEnumerable<VrFirearmPart> Parts => Components.GetAll<VrFirearmPart>( FindMode.EverythingInDescendants );

	/// <summary>
	/// How it sits in the grip's space for a tracked bare hand, which has no aim
	/// of its own to follow: its grip up the grip's tube, which runs up through a
	/// closed fist, and its barrel out past the trigger finger, the grip's down -
	/// the same frame the bow is held in.
	/// </summary>
	private Rotation InHand
	{
		get
		{
			var along = Rotation.FromPitch( GripAngle ).Up;
			var barrel = ( Vector3.Forward - along * Vector3.Dot( Vector3.Forward, along ) ).Normal;
			var gun = Rotation.LookAt( barrel, along );
			return Rotation.LookAt( new Vector3( 0, -1, 0 ), new Vector3( 0, 0, -1 ) ) * gun.Inverse;
		}
	}

	private VrGrabber grabber;
	private Transform muzzle;
	private Transform magazine;
	private Transform port;
	private bool triggerReset = true;
	private bool wasRelease, wasSlideStop;
	private float cycle = 1.0f;   // how far through the action's last trip, nought to one
	private float rack;           // how far back the other hand has the slide
	private float kick;           // how far up the muzzle has flipped, nought to one
	private float releasePulse;
	private TimeSince sinceShot = 10;

	protected override void OnStart()
	{
		Renderer ??= Components.Get<SkinnedModelRenderer>();
		Body ??= Components.Get<Rigidbody>();
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
		muzzle = model?.GetAttachment( "muzzle" ) ?? new Transform( Vector3.Zero );
		magazine = model?.GetAttachment( "magazine" ) ?? new Transform( Vector3.Zero );
		port = model?.GetAttachment( "eject" ) ?? new Transform( Vector3.Zero );

		HasMagazine = StartRounds >= 0;
		Rounds = System.Math.Max( StartRounds, 0 );
		Chambered = StartChambered;

		foreach ( var part in Parts ) part.GameObject.Enabled = false;
		ShowMagazine();
	}

	/// <summary>The other hand, reaching for it while it is held, takes whichever of its parts is nearest.</summary>
	public IVrHoldable ReachedFor( bool isLeft, Vector3 at )
	{
		if ( !IsHeld || HeldLeft == isLeft ) return this;

		return Parts.Where( x => !x.IsHeld )
			.OrderBy( x => x.WorldPosition.DistanceSquared( at ) )
			.FirstOrDefault() ?? (IVrHoldable)this;
	}

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

		// The other hand's part goes with it: a slide or a foregrip on a dropped gun is nothing to hold.
		foreach ( var part in Parts ) part.LetGo();

		grabber = null;
		rack = 0;
		kick = 0;

		SetPhysics( true );
		if ( Body.IsValid() ) Body.Velocity = VrGrabber.Hand( isLeft ).Velocity.ClampLength( 10.0f );
	}

	/// <summary>
	/// Held, a body that stays where the hand puts it and does not collide - so the
	/// other hand reaches only its parts - and loose, one that falls.
	/// </summary>
	private void SetPhysics( bool loose )
	{
		if ( Body.IsValid() )
		{
			Body.MotionEnabled = loose;
			if ( loose ) Body.Velocity = 0;
		}

		var parts = Parts.Select( x => x.GameObject ).ToHashSet();

		foreach ( var collider in Components.GetAll<Collider>( FindMode.EverythingInSelfAndDescendants ) )
		{
			if ( parts.Contains( collider.GameObject ) ) continue;
			collider.Enabled = loose;
		}

		foreach ( var part in parts ) part.Enabled = !loose;
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

		// The trigger: a shot when it breaks - and then, on automatic, one every
		// cycle while it is held; on semi, another only once it has come back.
		var pull = hand.IsHandTracked ? ( grabber.IsPressed( HeldLeft, VrButton.Trigger, false ) ? 1.0f : 0.0f ) : hand.Trigger.Value;
		Renderer?.Morphs.Set( "trigger", pull, 0 );

		if ( pull < 0.4f ) triggerReset = true;

		if ( pull > 0.85f )
		{
			var auto = FireMode == VrFireMode.Auto && Chambered && sinceShot >= 60.0f / RoundsPerMinute;
			if ( triggerReset || auto )
			{
				triggerReset = false;
				Fire();
			}
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
	/// It where the hand holding it is: its grip in the fist and its barrel down
	/// the controller's aim - or, with the other hand on the foregrip, towards that
	/// hand - the muzzle flipped up by the last shot.
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

		// Two hands: turned the shortest way so the point the other hand took lies
		// under it again. The grip hand keeps the roll.
		if ( Parts.OfType<VrFirearmForegrip>().FirstOrDefault( x => x.IsHeld ) is { } foregrip )
		{
			var now = held.Rotation * foregrip.Anchor;
			var wanted = foregrip.HandPosition - held.Position;

			if ( now.Length > 0.05f && wanted.Length > 0.05f )
				held = held.WithRotation( Rotation.FromToRotation( now.Normal, wanted.Normal ) * held.Rotation );
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
		sinceShot = 0;

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

		// The action comes back, throws the case out and takes the next round up -
		// or stays back on an empty magazine, if it is the kind that does.
		cycle = 0;
		kick = Steadied ? SteadiedKick : 1;
		Feed( lockWhenEmpty: LocksOpenWhenEmpty );

		Buzz( HapticEffect.HardImpact, 0.35f, 1.0f );
	}

	private void Play( SoundEvent sound )
	{
		if ( sound is not null ) Sound.Play( sound, WorldPosition );
	}

	/// <summary>
	/// A case or a round out of the port: to the right, up and a little back, with
	/// a tumble - and with the hand's own movement, so it leaves a swung gun as it
	/// would.
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

	/// <summary>The next round into the chamber, if the magazine has one; the action held back if it is empty and asked to.</summary>
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

	/// <summary>The magazine out of the well, falling, with what is left in it.</summary>
	public void DropMagazine()
	{
		if ( !HasMagazine ) return;

		releasePulse = 1;

		if ( MagazinePrefab is not null )
		{
			var at = MagazineWell.WithScale( 1 );
			var go = GameObject.Clone( MagazinePrefab, at );
			go.Components.Get<VrMagazine>()?.Fill( Rounds );

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

	/// <summary>
	/// Where a seated magazine is, in the world - its model's origin goes here, up
	/// pointing into the gun.
	/// </summary>
	public Transform MagazineWell => WorldTransform.ToWorld( magazine );

	/// <summary>Whether this magazine could go in now.</summary>
	public bool Takes( VrMagazine mag ) => IsHeld && !HasMagazine && mag.Cartridge == Cartridge;

	/// <summary>A magazine pushed home - which chambers nothing, unless this is a gun with nothing to rack.</summary>
	public void Insert( int rounds )
	{
		HasMagazine = true;
		Rounds = rounds;
		if ( ChambersOnInsert && !Chambered ) Feed( lockWhenEmpty: false );

		ShowMagazine();
		Play( MagazineInSound );
		Buzz( HapticEffect.HardImpact, 0.15f, 0.6f );
	}

	/// <summary>A locked action let forward, chambering a round if there is one.</summary>
	public void LetSlideForward()
	{
		if ( !SlideLocked ) return;

		SlideLocked = false;
		cycle = 0.35f; // from all the way back, home
		Feed( lockWhenEmpty: false );
		Play( SlideForwardSound );
	}

	/// <summary>How far back the other hand has the slide, nought to one - see VrFirearmSlide.</summary>
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
		Feed( lockWhenEmpty: LocksOpenWhenEmpty );
		Play( SlideForwardSound );
	}

	/// <summary>The slide has come all the way back under the hand.</summary>
	public void RackedBack() => Play( SlideBackSound );

	/// <summary>The magazine in the well as the body group has it: with rounds on top, without, or none.</summary>
	private void ShowMagazine()
	{
		Renderer?.SetBodyGroup( "magazine", !HasMagazine ? "none" : Rounds > 0 ? "loaded" : "empty" );
	}
}
