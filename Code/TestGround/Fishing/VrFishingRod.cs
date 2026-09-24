using Rinten.VR;

namespace TestGround;

/// <summary>
/// A spinning rod. Taken by its grip it becomes the hand, as a firearm does; the
/// lower face button (A or X) flips the bail open or shut, the trigger is the
/// finger on the line, and the thumbstick pushed forward reels. The other hand
/// takes the crank and turns it - see <see cref="VrFishingCrank"/> - which reels
/// too, and shuts an open bail.
/// </summary>
/// <remarks>
/// <para>
/// A cast: bail open, finger on the line, swing, and let go of the trigger on the
/// way forward - the float and hook leave at the tip's speed and line runs off the
/// open spool until the finger goes back on or the bail is shut. A strike is a
/// sharp lift of the tip - see <see cref="StrikeSpeed"/>. With the bail shut, a
/// pull over <see cref="Drag"/> takes line off anyway.
/// </para>
/// <para>
/// The blank bends to the line: the bones rod_1 .. rod_7 turn towards the pull,
/// more of it towards the tip, and spring behind a swing. Everything it knows
/// about its shape comes from the model - those bones, the graph parameter bail,
/// and the attachments reel_line, guide_0 .. guide_4, tip and crank_axle. The
/// crank is a model of its own on that axle. A model without
/// the bones gets a blank of boxes instead, so it can be played with before the
/// real one exists.
/// </para>
/// </remarks>
[Title( "VR Fishing Rod" )]
[Category( "Test Ground" )]
[Icon( "phishing" )]
public sealed class VrFishingRod : Component, IVrHoldable
{
	[Property] public SkinnedModelRenderer Renderer { get; set; }
	[Property] public Rigidbody Body { get; set; }
	[Property] public VrFishingLine Line { get; set; }

	/// <summary>A turn on top of how it sits in the hand, for tuning.</summary>
	[Property, Category( "Hold" )] public Angles HoldAngles { get; set; }
	[Property, Category( "Hold" )] public Vector3 HoldOffset { get; set; }

	/// <summary>Held still where it was put - on its rest - until a hand first takes it.</summary>
	[Property, Category( "Hold" )] public bool StartParked { get; set; } = true;

	/// <summary>Line back on the spool for each turn of the crank, in metres.</summary>
	[Property, Category( "Reel" )] public float RetrievePerTurn { get; set; } = 0.75f;

	/// <summary>How fast the thumbstick, all the way forward, reels, in metres a second.</summary>
	[Property, Category( "Reel" )] public float StickReelSpeed { get; set; } = 1.2f;

	/// <summary>Which way round the crank reels: one, or minus one for the other way.</summary>
	[Property, Category( "Reel" )] public float CrankDirection { get; set; } = -1.0f;

	/// <summary>The pull, in newtons, over which a shut reel gives line.</summary>
	[Property, Category( "Reel" )] public float Drag { get; set; } = 6.0f;

	[Property, Category( "Reel" )] public SoundEvent DragSound { get; set; }
	[Property, Category( "Reel" )] public SoundEvent BailSound { get; set; }

	/// <summary>How fast the tip has to be going for a let-go trigger to be a cast, in metres a second.</summary>
	[Property, Category( "Casting" )] public float CastSpeed { get; set; } = 2.0f;

	/// <summary>The tip's speed times this is what the float and hook leave with.</summary>
	[Property, Category( "Casting" )] public float CastBoost { get; set; } = 1.1f;

	/// <summary>How fast the tip has to go up for a strike, in metres a second.</summary>
	[Property, Category( "Casting" )] public float StrikeSpeed { get; set; } = 0.8f;

	/// <summary>Degrees of bend a newton of pull.</summary>
	[Property, Category( "Bend" )] public float BendPerNewton { get; set; } = 10.0f;
	[Property, Category( "Bend" )] public float MaxBend { get; set; } = 80.0f;

	/// <summary>How hard the blank springs back to where the pull puts it.</summary>
	[Property, Category( "Bend" )] public float Stiffness { get; set; } = 220.0f;
	[Property, Category( "Bend" )] public float Damping { get; set; } = 9.0f;

	/// <summary>Degrees the tip lags behind for each metre a second squared the rod is swung.</summary>
	[Property, Category( "Bend" )] public float Whip { get; set; } = 0.6f;

	/// <summary>How much more of the bend each bone further out takes - the butt is stiff.</summary>
	[Property, Category( "Bend" )] public float Taper { get; set; } = 1.8f;

	public const string Tag = "vr_fishing_rod";

	public bool IsHeld => grabber is not null;
	public bool HeldLeft { get; private set; }

	public bool BailOpen { get; private set; }

	/// <summary>The finger is on the line - the trigger held - and the open spool gives nothing.</summary>
	public bool LineHeld { get; private set; }

	/// <summary>Line runs off freely: the bail open, no finger on it, and the crank not held.</summary>
	public bool FreeSpool => BailOpen && !LineHeld && Crank is not { IsHeld: true };

	/// <summary>The tip-top ring, in the world.</summary>
	public Vector3 Tip { get; private set; }

	/// <summary>How fast the tip is going, in metres a second.</summary>
	public Vector3 TipVelocity { get; private set; }

	/// <summary>How far round the crank is, in degrees.</summary>
	public float CrankAngle { get; private set; }

	/// <summary>How far the blank is bent at the tip, in degrees.</summary>
	public float Bend => bend.Length;

	/// <summary>Whatever the other hand can take while it is held: the crank.</summary>
	public VrFishingCrank Crank => Components.Get<VrFishingCrank>( FindMode.EverythingInDescendants );

	private sealed class Link
	{
		public BoneCollection.Bone Bone;
		public Transform Rest;        // in the model's space
		public Transform Relative;    // to the link before
		public Transform Now;         // in the model's space, as bent
		public GameObject Piece;      // a box of the stand-in blank
		public float Share;           // how much of the bend is at its joint
	}

	/// <summary>Somewhere on the blank that moves with a link: a guide, the tip.</summary>
	private readonly record struct Mark( int Link, Vector3 Offset );

	private readonly List<Link> links = new();
	private readonly List<Mark> guides = new();
	private Mark tip;
	private Vector3 reelLine;
	private BoneCollection.Bone crankBone;
	private Transform crankRest;
	private Vector3 crankAxis;    // in the crank bone's own space
	private Transform axle;       // the crank's centre and axle (forward), in the model's space
	private Vector3 knobArm;      // from the axle out to the knob at rest, in the model's space
	private GameObject knobPiece;
	private Vector3 blank = Vector3.Forward;
	private bool procedural;

	private VrGrabber grabber;
	private bool wasBail, wasFinger, parked;
	private Vector3 bend, bendVelocity;   // in the model's space, degrees about the bend's axis
	private Vector3 lastTip, restTipVelocity;
	private bool rising;
	private TimeSince sinceStrike = 10;
	private float clicked;
	private TimeSince sinceClick = 10;

	protected override void OnStart()
	{
		Renderer ??= Components.Get<SkinnedModelRenderer>();
		Body ??= Components.Get<Rigidbody>();
		Line ??= Components.Get<VrFishingLine>( FindMode.EverythingInDescendants );
		DragSound ??= ResourceLibrary.Get<SoundEvent>( "sounds/weapons/pistol/dry_fire.sound" );
		Tags.Add( Tag );

		Build();
		Pose();
		lastTip = Tip;

		if ( Crank is { } crank )
		{
			crank.GameObject.LocalPosition = axle.Position;
			foreach ( var collider in crank.Components.GetAll<Collider>( FindMode.EverythingInSelf ) )
				collider.Enabled = false;
		}

		parked = StartParked;
		if ( parked && Body.IsValid() ) Body.MotionEnabled = false;
	}

	/// <summary>
	/// The blank's links as the model has them - or, without the bones, a stand-in
	/// of boxes laid out the same way - and the marks on it the line runs through.
	/// </summary>
	private void Build()
	{
		links.Clear();
		guides.Clear();

		var model = Renderer?.Model;
		var bones = model?.Bones;
		procedural = bones is null || !bones.HasBone( "rod_0" ) || !bones.HasBone( "rod_7" );

		if ( !procedural )
		{
			for ( var i = 0; i <= 7; i++ )
			{
				var bone = bones.GetBone( $"rod_{i}" );
				if ( bone is null ) break;
				links.Add( new Link { Bone = bone, Rest = BoneRest( bone ) } );
			}
		}
		else
		{
			// A 1.5 m stand-in: the handle about the grip, and seven lengths of
			// blank from the fore grip, shorter towards the tip.
			float[] lengths = { 0.25f, 0.26f, 0.22f, 0.19f, 0.17f, 0.15f, 0.14f, 0.12f };
			var z = 0.0f;
			for ( var i = 0; i <= 7; i++ )
			{
				links.Add( new Link { Rest = new Transform( new Vector3( 0, 0, -z ) ) } );
				z += lengths[i];
			}
		}

		for ( var i = 1; i < links.Count; i++ )
			links[i].Relative = links[i - 1].Rest.ToLocal( links[i].Rest );

		var first = links.Count > 1 ? links[1].Rest.Position : Vector3.Zero;
		var end = links[^1].Rest.Position;
		if ( end.Distance( first ) > 0.01f ) blank = ( end - first ).Normal;

		// Stiff at the butt, soft at the tip.
		var total = 0.0f;
		for ( var i = 1; i < links.Count; i++ ) total += System.MathF.Pow( i, Taper );
		for ( var i = 1; i < links.Count; i++ ) links[i].Share = System.MathF.Pow( i, Taper ) / total;

		// The marks: from the model, or spread along the stand-in.
		var tipRest = AttachmentRest( "tip" ) ?? ( links[^1].Rest.Position + blank * ( procedural ? 0.12f : 0.0f ) );
		tip = MarkAt( tipRest );

		for ( var g = 0; g < 5; g++ )
		{
			var at = AttachmentRest( $"guide_{g}" );
			if ( at is null && !procedural ) continue;

			var along = new[] { 0.36f, 0.52f, 0.66f, 0.8f, 0.92f }[g];
			guides.Add( MarkAt( at ?? Vector3.Lerp( first, tipRest, along ) + Vector3.Down * 0.015f ) );
		}

		reelLine = AttachmentRest( "reel_line" ) ?? new Vector3( 0, -0.055f, -0.07f );

		// The crank is its own model, origin on the axle, axle along its local X.
		// crank_axle is where that origin sits on the rod.
		crankBone = bones?.GetBone( "reel_crank" );
		var knob = AttachmentRest( "crank_knob" );

		if ( AttachmentRest( "crank_axle" ) is { } axleAt )
			axle = new Transform( axleAt, Rotation.LookAt( Vector3.Left ) );
		else if ( crankBone is not null )
		{
			crankRest = BoneRest( crankBone );
			var candidates = new[] { Vector3.Right, Vector3.Up, Vector3.Forward };
			crankAxis = candidates.OrderByDescending( x => System.MathF.Abs( Vector3.Dot( crankRest.Rotation * x, Vector3.Right ) ) ).First();
			axle = new Transform( crankRest.Position, Rotation.LookAt( crankRest.Rotation * crankAxis ) );
		}
		else
		{
			axle = new Transform( new Vector3( -0.045f, -0.075f, -0.05f ), Rotation.LookAt( Vector3.Left ) );
		}

		knobArm = knob is { } k ? k - axle.Position : Vector3.Down * 0.05f;
		knobArm -= axle.Rotation.Forward * Vector3.Dot( knobArm, axle.Rotation.Forward );
		if ( knobArm.Length < 0.01f ) knobArm = Vector3.Down * 0.05f;

		if ( procedural ) BuildStandIn();
	}

	/// <summary>
	/// Where a bone rests, in the model's space - asked of the placed model before
	/// anything has turned it, which is the bind pose. The model's own bone list
	/// has them relative to their parents instead.
	/// </summary>
	private Transform BoneRest( BoneCollection.Bone bone )
	{
		if ( !rests.TryGetValue( bone.Index, out var rest ) )
		{
			rest = Renderer.TryGetBoneTransformLocal( bone, out var tx ) ? tx : new Transform( Vector3.Zero );
			rests[bone.Index] = rest;
		}

		return rest;
	}

	private readonly Dictionary<int, Transform> rests = new();

	/// <summary>An attachment where it rests, in the model's space - null when the model has none.</summary>
	private Vector3? AttachmentRest( string name ) => procedural ? null : Renderer?.GetAttachment( name, false )?.Position;

	/// <summary>A point on the blank, kept as an offset from the link it lies along.</summary>
	private Mark MarkAt( Vector3 point )
	{
		var best = 0;
		for ( var i = 0; i < links.Count; i++ )
		{
			if ( Vector3.Dot( point - links[i].Rest.Position, blank ) >= -0.001f ) best = i;
		}

		return new Mark( best, links[best].Rest.PointToLocal( point ) );
	}

	/// <summary>Boxes for the handle, reel and blank, until the model has bones of its own.</summary>
	private void BuildStandIn()
	{
		GameObject Box( string name, Vector3 scale, Color tint )
		{
			var go = Scene.CreateObject();
			go.Name = name;
			go.Flags |= GameObjectFlags.NotSaved;
			go.SetParent( GameObject, false );
			go.LocalScale = scale;
			var renderer = go.Components.Create<ModelRenderer>();
			renderer.Model = Model.Cube;
			renderer.Tint = tint;
			return go;
		}

		var cork = new Color( 0.72f, 0.56f, 0.38f );
		var dark = new Color( 0.08f, 0.08f, 0.09f );

		Box( "Stand-in handle", new Vector3( 0.03f, 0.03f, 0.4f ), cork ).LocalPosition = new Vector3( 0, 0, 0.02f );
		Box( "Stand-in reel", new Vector3( 0.04f, 0.05f, 0.06f ), dark ).LocalPosition = new Vector3( 0, -0.06f, -0.05f );
		knobPiece = Box( "Stand-in crank knob", new Vector3( 0.015f, 0.015f, 0.025f ), new Color( 0.7f, 0.1f, 0.1f ) );

		for ( var i = 1; i < links.Count; i++ )
		{
			var length = i + 1 < links.Count ? links[i].Rest.Position.Distance( links[i + 1].Rest.Position ) : 0.12f;
			var thick = MathX.Lerp( 0.012f, 0.004f, i / 7.0f );
			links[i].Piece = Box( $"Stand-in blank {i}", new Vector3( thick, thick, length ), dark );
		}
	}

	/// <summary>The other hand, reaching for it while it is held, takes the crank.</summary>
	public IVrHoldable ReachedFor( bool isLeft, Vector3 at )
	{
		if ( !IsHeld || HeldLeft == isLeft ) return this;

		var crank = Crank;
		return crank is { IsHeld: false } ? crank : this;
	}

	public bool Grab( VrGrabber by, bool isLeft )
	{
		grabber = by;
		HeldLeft = isLeft;
		parked = false;
		wasBail = true;
		wasFinger = LineHeld = true; // taken with the finger on, not casting yet

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

		Crank?.LetGo();

		grabber = null;
		LineHeld = false;

		SetPhysics( true );
		if ( Body.IsValid() ) Body.Velocity = VrGrabber.Hand( isLeft ).Velocity.ClampLength( 10.0f );
	}

	/// <summary>Held, a body the hand puts where it likes that collides with nothing; loose, one that falls.</summary>
	private void SetPhysics( bool loose )
	{
		if ( Body.IsValid() )
		{
			Body.MotionEnabled = loose;
			if ( loose ) Body.Velocity = 0;
		}

		var crank = Crank?.GameObject;

		foreach ( var collider in Components.GetAll<Collider>( FindMode.EverythingInSelfAndDescendants ) )
		{
			if ( crank is not null && collider.GameObject == crank ) collider.Enabled = !loose;
			else collider.Enabled = loose;
		}

		if ( crank is not null ) crank.Enabled = true;
	}

	protected override void OnUpdate()
	{
		if ( IsHeld && Game.IsRunningInVR && Input.VR is not null )
		{
			Controls();
			Follow();
		}

		Pose();
		Watch( Time.Delta );
	}

	private void Controls()
	{
		var hand = VrGrabber.Hand( HeldLeft );

		// The bail flips as the button goes down.
		var bail = hand.ButtonA.IsPressed;
		if ( bail && !wasBail ) SetBail( !BailOpen );
		wasBail = bail;

		// The finger comes off the line: with the bail open and the tip moving, a cast.
		var finger = hand.IsHandTracked ? grabber.IsPressed( HeldLeft, VrButton.Trigger, false ) : hand.Trigger.Value > 0.5f;
		if ( wasFinger && !finger && BailOpen ) Cast();
		wasFinger = finger;
		LineHeld = finger;

		var stick = hand.Joystick.Value.y;
		if ( stick > 0.25f ) Reel( ( stick - 0.25f ) / 0.75f * StickReelSpeed * Time.Delta );
	}

	/// <summary>Where the hand has it: the grip in the fist and the blank along the controller, not its aim ray.</summary>
	private void Follow()
	{
		var frame = VrGrabber.HoldFrame( HeldLeft );

		// The aim ray on a controller is pitched up from the grip, so a rod laid
		// on it points back at the face. The blank follows the grip itself.
		var rotation = frame.Rotation * HoldAngles.ToRotation();
		WorldTransform = new Transform( frame.PointToWorld( HoldOffset ), rotation );
	}

	/// <summary>The bail flipped open, to cast, or shut, to fish.</summary>
	public void SetBail( bool open )
	{
		if ( BailOpen == open ) return;

		BailOpen = open;
		if ( Graphed ) Renderer.Set( "bail", open ? 1.0f : 0.0f );
		if ( BailSound is not null ) Sound.Play( BailSound, WorldPosition );
		Buzz( HapticEffect.SoftImpact, 0.1f, 0.3f );
	}

	/// <summary>The finger off the line on the way forward: the tackle thrown at the tip's speed.</summary>
	public void Cast()
	{
		if ( !Line.IsValid() ) return;
		if ( TipVelocity.Length < CastSpeed ) return;

		Line.Throw( TipVelocity * CastBoost );
	}

	/// <summary>Line wound back on, in metres - by the crank or the stick. It shuts an open bail first.</summary>
	public void Reel( float metres )
	{
		if ( metres <= 0 ) return;

		if ( BailOpen )
		{
			SetBail( false );
			return;
		}

		Line?.Reel( metres );
		CrankAngle += metres / RetrievePerTurn * 360.0f;
	}

	/// <summary>
	/// The crank turned by the other hand, in degrees around its axle, either way.
	/// The handle follows the whole turn. Line comes in only the reeling way.
	/// </summary>
	public void Turn( float degrees )
	{
		CrankAngle += degrees;

		var reeling = degrees * CrankDirection;
		if ( reeling <= 0 ) return;

		if ( BailOpen )
		{
			SetBail( false );
			return;
		}

		Line?.Reel( reeling / 360.0f * RetrievePerTurn );
	}

	/// <summary>The reel gave line - with the bail shut, that is the drag, and it clicks.</summary>
	public void LineGiven( float metres )
	{
		if ( FreeSpool ) return;

		clicked += metres;
		if ( clicked < 0.05f ) return;

		clicked = 0;
		if ( sinceClick > 0.04f && DragSound is not null )
		{
			sinceClick = 0;
			var handle = Sound.Play( DragSound, WorldPosition );
			if ( handle is not null ) handle.Volume = 0.3f;
		}

		Buzz( HapticEffect.SoftImpact, 0.05f, 0.25f );
	}

	/// <summary>
	/// The hand's angle round the crank's axle, in degrees - a point in the world,
	/// seen down the axle from the knob's side.
	/// </summary>
	public float AngleRoundAxle( Vector3 point )
	{
		var local = WorldTransform.PointToLocal( point ) - axle.Position;
		var axis = axle.Rotation.Forward;
		var a = knobArm.Normal;
		var b = Vector3.Cross( axis, a );
		return MathX.RadianToDegree( System.MathF.Atan2( Vector3.Dot( local, b ), Vector3.Dot( local, a ) ) );
	}

	/// <summary>The crank's centre, in the world.</summary>
	public Vector3 AxleCentre => WorldTransform.PointToWorld( axle.Position );

	/// <summary>
	/// The tip's speed, for a cast, and a strike when it goes up sharply.
	/// </summary>
	private void Watch( float dt )
	{
		if ( dt <= 0 ) return;

		var velocity = ( Tip - lastTip ) / dt;
		TipVelocity = Vector3.Lerp( TipVelocity, velocity, 0.5f );
		lastTip = Tip;

		// A strike: the tip snatched upward, once, not again for a moment.
		var up = IsHeld && TipVelocity.y > StrikeSpeed;
		if ( up && !rising && sinceStrike > 0.5f )
		{
			sinceStrike = 0;
			Line?.Hook?.Struck();
		}
		rising = up;
	}

	/// <summary>
	/// The blank bent to the line's pull, and the tip lagging a swing; the crank
	/// turned; the bail as it is.
	/// </summary>
	private void Pose()
	{
		var dt = Time.Delta;
		if ( links.Count < 2 ) return;

		// The rigid tip, to know how the rod is being swung.
		var restTip = WorldTransform.PointToWorld( links[tip.Link].Rest.PointToWorld( tip.Offset ) );
		var restVelocity = dt > 0 ? ( restTip - lastRestTip ) / dt : Vector3.Zero;
		var acceleration = dt > 0 ? ( restVelocity - restTipVelocity ) / dt : Vector3.Zero;
		restTipVelocity = restVelocity;
		lastRestTip = restTip;
		if ( acceleration.Length > 300.0f || !started ) acceleration = Vector3.Zero;
		started = true;
		swingAcceleration = Vector3.Lerp( swingAcceleration, acceleration, 0.3f );

		// Where the pull alone would hold it: towards the line, no further than the line lies.
		var target = Vector3.Zero;
		if ( Line.IsValid() && Line.Tension > 0.01f )
		{
			var pull = WorldRotation.Inverse * Line.TipDirection;
			var across = pull - blank * Vector3.Dot( pull, blank );
			if ( across.Length > 0.001f )
			{
				var most = MathX.RadianToDegree( System.MathF.Acos( Vector3.Dot( pull.Normal, blank ).Clamp( -1, 1 ) ) ) * 0.85f;
				var angle = System.MathF.Min( System.MathF.Min( Line.Tension * BendPerNewton, MaxBend ), most );
				target = across.Normal * angle;
			}
		}

		// A spring towards it, the tip thrown back against the swing.
		var swing = WorldRotation.Inverse * swingAcceleration;
		swing -= blank * Vector3.Dot( swing, blank );

		if ( dt > 0 )
		{
			var force = ( target - bend ) * Stiffness - bendVelocity * Damping - swing * Whip * Stiffness;
			bendVelocity += force * dt;
			bend += bendVelocity * dt;
			bend -= blank * Vector3.Dot( bend, blank );
			if ( bend.Length > MaxBend ) bend = bend.Normal * MaxBend;
		}

		// Each joint takes its share, about the one axis across the bend.
		var degrees = bend.Length;
		var axis = degrees > 0.01f ? Vector3.Cross( blank, bend / degrees ).Normal : Vector3.Right;

		links[0].Now = links[0].Rest;
		for ( var i = 1; i < links.Count; i++ )
		{
			var link = links[i];
			var parent = links[i - 1];
			var local = parent.Rest.Rotation.Inverse * axis;
			var relative = link.Relative.WithRotation( Rotation.FromAxis( local, degrees * link.Share ) * link.Relative.Rotation );
			link.Now = parent.Now.ToWorld( relative );

			if ( link.Bone is not null && Renderer.IsValid() )
			{
				// Handed over in the model's space and taken back through the parent
				// as it is posed now - so give it the parent as it is posed now.
				var posed = Renderer.TryGetBoneTransformLocal( parent.Bone, out var p ) ? p : parent.Now;
				Renderer.SetBoneTransform( link.Bone, posed.ToWorld( relative ) );
			}

			if ( link.Piece.IsValid() )
			{
				var length = link.Piece.LocalScale.z;
				link.Piece.LocalRotation = link.Now.Rotation;
				link.Piece.LocalPosition = link.Now.PointToWorld( Vector3.Forward * length * 0.5f );
			}
		}

		Tip = WorldTransform.PointToWorld( links[tip.Link].Now.PointToWorld( tip.Offset ) );

		Crank?.Pose();

		if ( knobPiece.IsValid() )
		{
			knobPiece.LocalPosition = axle.Position + Rotation.FromAxis( axle.Rotation.Forward, CrankAngle * CrankDirection ) * knobArm;
			knobPiece.LocalRotation = axle.Rotation;
		}
	}

	private Vector3 lastRestTip, swingAcceleration;
	private bool started;

	/// <summary>Whether the model has an animation graph for its bail and crank - a stand-in rod has neither.</summary>
	private bool Graphed => Renderer.IsValid() && Renderer.UseAnimGraph && Renderer.EffectiveAnimationGraph is not null;

	/// <summary>The crank knob, in the world.</summary>
	public Vector3 Knob
	{
		get
		{
			if ( !procedural && Renderer?.GetAttachment( "crank_knob" ) is { } knob ) return knob.Position;
			return WorldTransform.PointToWorld( axle.Position + Rotation.FromAxis( axle.Rotation.Forward, CrankAngle * CrankDirection ) * knobArm );
		}
	}

	/// <summary>The line's way from the spool to the tip: reel_line, the guides, the tip.</summary>
	public void AddLinePath( List<Vector3> path )
	{
		path.Add( WorldTransform.PointToWorld( reelLine ) );

		foreach ( var guide in guides )
			path.Add( WorldTransform.PointToWorld( links[guide.Link].Now.PointToWorld( guide.Offset ) ) );

		path.Add( Tip );
	}

	private void Buzz( HapticEffect effect, float length, float amplitude )
	{
		if ( !IsHeld || Input.VR is null ) return;
		VrGrabber.Hand( HeldLeft ).TriggerHaptics( effect, lengthScale: length, amplitudeScale: amplitude );
	}
}

/// <summary>
/// The reel's crank, for the hand not holding the rod: taken and wound round its
/// axle it reels in - see <see cref="VrFishingRod.Turn"/>. On only while the rod
/// is held, as a firearm's parts are.
/// </summary>
[Title( "VR Fishing Crank" )]
[Category( "Test Ground" )]
[Icon( "rotate_right" )]
public sealed class VrFishingCrank : Component, IVrHoldable
{
	[Property] public VrFishingRod Rod { get; set; }

	/// <summary>How far the hand can get from the axle before it has let go.</summary>
	[Property] public float BreakDistance { get; set; } = 0.2f;

	public bool IsHeld => grabber is not null;
	public bool HeldLeft { get; private set; }

	private VrGrabber grabber;
	private float angle;

	private Transform HandFrame => VrGrabber.HoldFrame( HeldLeft );

	public bool Grab( VrGrabber by, bool isLeft )
	{
		Rod ??= GameObject.Parent?.Components.GetInAncestorsOrSelf<VrFishingRod>();
		if ( !Rod.IsValid() || !Rod.IsHeld || Rod.HeldLeft == isLeft ) return false;

		grabber = by;
		HeldLeft = isLeft;
		angle = Rod.AngleRoundAxle( HandFrame.Position );
		Rod.SetBail( false );

		var controllers = by.Components.Get<VrControllers>();
		controllers?.SetHidden( isLeft, true );
		controllers?.SetHolding( isLeft, true );
		return true;
	}

	public void Release( VrGrabber by, bool isLeft )
	{
		if ( !IsHeld ) return;

		grabber = null;
		var controllers = by.Components.Get<VrControllers>();
		controllers?.SetHidden( isLeft, false );
		controllers?.SetHolding( isLeft, false );
	}

	/// <summary>The rod left its hand while this was held: this hand lets go too.</summary>
	public void LetGo()
	{
		if ( !IsHeld ) return;

		var by = grabber;
		by.Forget( this );
		Release( by, HeldLeft );
	}

	protected override void OnUpdate()
	{
		if ( IsHeld && Rod.IsValid() && Input.VR is not null )
		{
			if ( HandFrame.Position.Distance( Rod.AxleCentre ) > BreakDistance )
			{
				LetGo();
			}
			else
			{
				// A circle of the hand around the axle, the way a crank is turned.
				var now = Rod.AngleRoundAxle( HandFrame.Position );
				var turned = now - angle;
				if ( turned > 180 ) turned -= 360;
				if ( turned < -180 ) turned += 360;
				angle = now;

				Rod.Turn( turned );
			}
		}

		Pose();
	}

	/// <summary>The handle round its axle, the angle the rod has wound it to.</summary>
	public void Pose()
	{
		if ( !Rod.IsValid() ) return;
		LocalRotation = Rotation.FromAxis( Vector3.Left, Rod.CrankAngle );
	}
}
