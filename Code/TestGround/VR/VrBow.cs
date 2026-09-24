using Rinten.VR;

namespace TestGround;

/// <summary>
/// A bow. Taken with the grip it becomes the hand - the controller hides and the
/// bow rides the grip - and an arrow brought to its string by the other hand is
/// nocked. It sits on the string until that hand's trigger is squeezed, is drawn
/// as far as the hand pulls back while it is, and is loosed when it comes up.
/// </summary>
/// <remarks>
/// Everything the bow knows about its own shape comes from its model: the
/// attachments nock_rest, nock_drawn and arrow_rest, and the morph "draw" - see
/// ~/Documents/Blender/tools/archery/build_archery.py, which makes them.
/// </remarks>
[Title( "VR Bow" )]
[Category( "Test Ground" )]
[Icon( "sports_martial_arts" )]
public sealed class VrBow : Component, IVrHoldable
{
	[Property] public SkinnedModelRenderer Renderer { get; set; }
	[Property] public Rigidbody Body { get; set; }

	/// <summary>
	/// A turn on top of how the bow sits in the hand, for tuning - see <see cref="InHand"/>.
	/// </summary>
	[Property, Category( "Hold" )] public Angles HoldAngles { get; set; }
	[Property, Category( "Hold" )] public Vector3 HoldOffset { get; set; }

	/// <summary>
	/// How the bow sits in the grip's space: its handle up the grip's tube - the
	/// grip's forward, which runs up through a closed fist - and its front, where
	/// the arrow flies, out past the trigger finger, the grip's down.
	/// </summary>
	private static readonly Rotation InHand = Rotation.LookAt( new Vector3( 0, -1, 0 ), new Vector3( 0, 0, -1 ) );

	/// <summary>How near the string an arrow's nock has to come to be nocked.</summary>
	[Property, Category( "Shooting" )] public float NockRadius { get; set; } = 0.09f;

	/// <summary>How fast an arrow leaves at full draw, in metres a second.</summary>
	[Property, Category( "Shooting" )] public float MaxSpeed { get; set; } = 55.0f;

	/// <summary>Less draw than this and the arrow just drops off the string.</summary>
	[Property, Category( "Shooting" )] public float MinDraw { get; set; } = 0.15f;

	[Property, Category( "Sounds" )] public SoundEvent NockSound { get; set; }
	[Property, Category( "Sounds" )] public SoundEvent DrawSound { get; set; }
	[Property, Category( "Sounds" )] public SoundEvent ReleaseSound { get; set; }

	public const string Tag = "vr_bow";

	/// <summary>Whether a hand has it, and which.</summary>
	public bool IsHeld => grabber is not null;
	public bool HeldLeft { get; private set; }

	/// <summary>The arrow on the string, or null.</summary>
	public VrArrow Nocked { get; private set; }

	/// <summary>How far the string is drawn, nought to one.</summary>
	public float Draw { get; private set; }

	private VrGrabber grabber;
	private Vector3 nockRest, nockDrawn, arrowRest;
	private float lastBuzz;
	private bool drawing;

	protected override void OnStart()
	{
		Renderer ??= Components.Get<SkinnedModelRenderer>();
		Body ??= Components.Get<Rigidbody>();
		Tags.Add( Tag );

		NockSound ??= ResourceLibrary.Get<SoundEvent>( "sounds/weapons/bow/nock.sound" );
		DrawSound ??= ResourceLibrary.Get<SoundEvent>( "sounds/weapons/bow/draw.sound" );
		ReleaseSound ??= ResourceLibrary.Get<SoundEvent>( "sounds/weapons/bow/release.sound" );

		var attachments = Renderer?.Model?.Attachments;
		nockRest = Point( attachments, "nock_rest", new Vector3( 0, 0.06f, 0.18f ) );
		nockDrawn = Point( attachments, "nock_drawn", new Vector3( 0, 0.06f, 0.70f ) );
		arrowRest = Point( attachments, "arrow_rest", new Vector3( -0.021f, 0.058f, 0 ) );
	}

	private static Vector3 Point( ModelAttachments attachments, string name, Vector3 fallback )
		=> attachments?.All?.FirstOrDefault( x => x.Name == name ) is { } found ? found.LocalTransform.Position : fallback;

	/// <summary>Where the string is at rest, in the world.</summary>
	public Vector3 NockRest => WorldTransform.PointToWorld( nockRest );

	private Vector3 NockDrawn => WorldTransform.PointToWorld( nockDrawn );
	private Vector3 ArrowRest => WorldTransform.PointToWorld( arrowRest );

	public bool Grab( VrGrabber by, bool isLeft )
	{
		grabber = by;
		HeldLeft = isLeft;

		if ( Body.IsValid() ) Body.MotionEnabled = false;

		var controllers = by.Components.Get<VrControllers>();
		controllers?.SetHidden( isLeft, true );
		controllers?.SetHolding( isLeft, true );

		Follow();
		return true;
	}

	public void Release( VrGrabber by, bool isLeft )
	{
		// An arrow on the string stays in the hand that holds it.
		Nocked?.Unnock();
		Nocked = null;
		drawing = false;

		var controllers = by.Components.Get<VrControllers>();
		controllers?.SetHidden( isLeft, false );
		controllers?.SetHolding( isLeft, false );

		grabber = null;

		if ( Body.IsValid() )
		{
			var hand = VrGrabber.Hand( isLeft );
			Body.MotionEnabled = true;
			Body.Velocity = hand.Velocity.ClampLength( 10.0f );
		}
	}

	protected override void OnUpdate()
	{
		if ( IsHeld ) Follow();

		if ( Nocked.IsValid() ) Nock();
		else Draw = MathX.Approach( Draw, 0, Time.Delta * 12.0f ); // the string snaps back

		Renderer?.Morphs.Set( "draw", Draw, 0 );
	}

	/// <summary>The bow where the hand holding it is.</summary>
	private void Follow()
	{
		var frame = VrGrabber.HoldFrame( HeldLeft );
		var local = new Transform( HoldOffset, InHand * HoldAngles.ToRotation() );
		WorldTransform = frame.ToWorld( local );
	}

	/// <summary>Whether this arrow, held in the other hand, is close enough to the string to go on it.</summary>
	public bool TryNock( VrArrow arrow, bool arrowHandLeft )
	{
		if ( !IsHeld || Nocked.IsValid() || arrowHandLeft == HeldLeft ) return false;
		if ( arrow.NockPosition.Distance( NockRest ) > NockRadius ) return false;

		Nocked = arrow;
		lastBuzz = 0;
		drawing = false;
		Play( NockSound );
		VrGrabber.Hand( arrowHandLeft ).TriggerHaptics( HapticEffect.SoftImpact, lengthScale: 0.2f, amplitudeScale: 0.5f );
		return true;
	}

	/// <summary>
	/// The arrow on the string: drawn while its hand's trigger is down, loosed
	/// when it comes up, and resting on the string until then - off it again if
	/// the hand carries it away without drawing.
	/// </summary>
	private void Nock()
	{
		var left = Nocked.HeldLeft;
		var trigger = grabber is not null && grabber.IsPressed( left, VrButton.Trigger, drawing );

		if ( trigger )
		{
			if ( !drawing ) Play( DrawSound );
			drawing = true;
			Pull( VrGrabber.HoldFrame( left ).Position );
			return;
		}

		if ( drawing )
		{
			Loose();
			return;
		}

		if ( VrGrabber.HoldFrame( left ).Position.Distance( NockRest ) > NockRadius * 2.0f )
		{
			var arrow = Nocked;
			Nocked = null;
			arrow.Unnock();
			return;
		}

		Pull( NockRest );
	}

	/// <summary>
	/// The nocked arrow on the line from the string at rest to full draw, as far
	/// back as <paramref name="hand"/> is, pointing through the arrow rest.
	/// </summary>
	private void Pull( Vector3 hand )
	{
		var rest = NockRest;
		var back = NockDrawn - rest;
		var length = back.Length;
		var along = back / length;

		var pulled = Vector3.Dot( hand - rest, along ).Clamp( 0, length );
		Draw = pulled / length;

		var nock = rest + along * pulled;
		var aim = ( ArrowRest - nock ).Normal;
		Nocked.PlaceOnString( nock, Rotation.LookAt( aim, WorldRotation.Up ) );

		// A tick in the drawing hand every tenth of the draw.
		if ( System.MathF.Abs( Draw - lastBuzz ) >= 0.1f )
		{
			lastBuzz = Draw;
			VrGrabber.Hand( Nocked.HeldLeft ).TriggerHaptics( HapticEffect.SoftImpact, lengthScale: 0.1f, amplitudeScale: 0.15f + Draw * 0.3f );
		}
	}

	/// <summary>The string let go: the arrow shot if it was drawn, dropped if it was not.</summary>
	public void Loose()
	{
		var arrow = Nocked;
		Nocked = null;
		drawing = false;
		if ( !arrow.IsValid() ) return;

		if ( Draw < MinDraw )
		{
			arrow.Drop( Vector3.Zero );
			return;
		}

		var aim = arrow.WorldRotation.Forward;
		arrow.Launch( aim * MaxSpeed * Draw, this );
		Play( ReleaseSound );

		VrGrabber.Hand( arrow.HeldLeft ).TriggerHaptics( HapticEffect.HardImpact, lengthScale: 0.4f, amplitudeScale: 0.9f );
		VrGrabber.Hand( HeldLeft ).TriggerHaptics( HapticEffect.HardImpact, lengthScale: 0.3f, amplitudeScale: 0.6f );
	}

	private void Play( SoundEvent sound )
	{
		if ( sound is not null ) Sound.Play( sound, WorldPosition );
	}
}
