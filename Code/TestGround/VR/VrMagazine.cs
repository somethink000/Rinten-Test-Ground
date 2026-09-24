using Rinten.VR;

namespace TestGround;

/// <summary>
/// A magazine: lying about, carried, or pushed into the well of a firearm held in
/// the other hand - one of its own cartridge only. It knows how many rounds it
/// has, and shows it - rounds on top, or the follower.
/// </summary>
/// <remarks>
/// Its model's origin is where it sits once seated: the firearm's magazine
/// attachment - see <see cref="VrFirearm.MagazineWell"/>. It goes in when that
/// origin comes up into a short column under the well, pointing roughly the
/// well's way.
/// </remarks>
[Title( "VR Magazine" )]
[Category( "Test Ground" )]
[Icon( "view_agenda" )]
public sealed class VrMagazine : Component, IVrHoldable
{
	[Property] public ModelRenderer Renderer { get; set; }
	[Property] public Rigidbody Body { get; set; }

	[Property] public Model Loaded { get; set; }
	[Property] public Model Empty { get; set; }

	/// <summary>What it holds - it only goes into a firearm of the same <see cref="VrFirearm.Cartridge"/>.</summary>
	[Property] public string Cartridge { get; set; } = "9x19";

	[Property] public int Capacity { get; set; } = 17;

	/// <summary>Where the magazine sits in the grip's space while it is carried.</summary>
	[Property, Category( "Hold" )] public Vector3 HoldOffset { get; set; } = new( 0, 0, 0.035f );
	[Property, Category( "Hold" )] public Angles HoldAngles { get; set; }

	/// <summary>How far off the well's line it can be and still go in.</summary>
	[Property, Category( "Insert" )] public float InsertRadius { get; set; } = 0.045f;

	/// <summary>How far short of seated it goes in: about as far as its top is up from its origin.</summary>
	[Property, Category( "Insert" )] public float InsertDepth { get; set; } = 0.1f;

	public const string Tag = "vr_magazine";

	public int Rounds { get; private set; } = -1;

	/// <summary>Carried as a pistol's grip is: up the grip's tube, its front out past the fingers.</summary>
	private static readonly Rotation InHand = Rotation.LookAt( new Vector3( 0, -1, 0 ), new Vector3( 0, 0, -1 ) );

	private VrGrabber grabber;
	private bool heldLeft;

	protected override void OnStart()
	{
		Renderer ??= Components.Get<ModelRenderer>();
		Body ??= Components.Get<Rigidbody>();
		Tags.Add( Tag );

		if ( Rounds < 0 ) Fill( Capacity );
	}

	/// <summary>So many rounds in it, and the model to match.</summary>
	public void Fill( int rounds )
	{
		Rounds = rounds.Clamp( 0, Capacity );

		// Asked before OnStart when a firearm drops one it has just made.
		Renderer ??= Components.Get<ModelRenderer>();
		var model = Rounds > 0 ? Loaded : Empty;
		if ( Renderer.IsValid() && model is not null ) Renderer.Model = model;
	}

	public bool Grab( VrGrabber by, bool isLeft )
	{
		grabber = by;
		heldLeft = isLeft;
		SetPhysics( false );
		Follow();
		return true;
	}

	public void Release( VrGrabber by, bool isLeft )
	{
		grabber = null;
		SetPhysics( true );
		if ( Body.IsValid() ) Body.Velocity = VrGrabber.Hand( isLeft ).Velocity.ClampLength( 10.0f );
	}

	protected override void OnUpdate()
	{
		if ( grabber is null ) return;

		Follow();

		foreach ( var firearm in Scene.GetAllComponents<VrFirearm>() )
		{
			if ( firearm.HeldLeft == heldLeft || !firearm.Takes( this ) || !InWell( firearm.MagazineWell ) ) continue;

			grabber.Forget( this );
			grabber = null;
			firearm.Insert( Rounds );
			GameObject.Destroy();
			return;
		}
	}

	/// <summary>Whether it is under the well and far enough up into it, pointing the well's way.</summary>
	private bool InWell( Transform well )
	{
		if ( Vector3.Dot( WorldRotation.Up, well.Rotation.Up ) < 0.6f ) return false;

		var local = well.WithScale( 1 ).PointToLocal( WorldPosition );
		var below = -local.y;
		return below > -0.01f && below < InsertDepth && local.WithY( 0 ).Length < InsertRadius;
	}

	private void Follow()
	{
		var frame = VrGrabber.HoldFrame( heldLeft );
		WorldTransform = frame.ToWorld( new Transform( HoldOffset, InHand * HoldAngles.ToRotation() ) );
	}

	private void SetPhysics( bool loose )
	{
		Body ??= Components.Get<Rigidbody>();

		if ( Body.IsValid() )
		{
			Body.MotionEnabled = loose;
			if ( loose ) Body.Velocity = 0;
		}

		foreach ( var collider in Components.GetAll<Collider>( FindMode.EverythingInSelfAndDescendants ) )
			collider.Enabled = loose;
	}
}
