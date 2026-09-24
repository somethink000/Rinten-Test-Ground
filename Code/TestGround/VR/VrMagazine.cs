using Rinten.VR;

namespace TestGround;

/// <summary>
/// A pistol magazine: lying about, carried, or pushed into a held pistol's grip
/// by the other hand. It knows how many rounds it has, and shows it - rounds on
/// top, or the follower.
/// </summary>
[Title( "VR Magazine" )]
[Category( "Test Ground" )]
[Icon( "view_agenda" )]
public sealed class VrMagazine : Component, IVrHoldable
{
	[Property] public ModelRenderer Renderer { get; set; }
	[Property] public Rigidbody Body { get; set; }

	[Property] public Model Loaded { get; set; }
	[Property] public Model Empty { get; set; }

	[Property] public int Capacity { get; set; } = 17;

	/// <summary>Where the magazine sits in the grip's space while it is carried.</summary>
	[Property, Category( "Hold" )] public Vector3 HoldOffset { get; set; } = new( 0, 0, 0.035f );
	[Property, Category( "Hold" )] public Angles HoldAngles { get; set; }

	/// <summary>How near the well its top has to come to go in.</summary>
	[Property] public float InsertRadius { get; set; } = 0.06f;

	public const string Tag = "vr_magazine";

	public int Rounds { get; private set; } = -1;

	/// <summary>Its top, where the rounds come out, in its own space.</summary>
	private static readonly Vector3 Top = new( 0, 0.087f, 0 );

	/// <summary>Carried as the pistol's grip is: up the grip's tube, its front out past the fingers.</summary>
	private static readonly Rotation InHand = Rotation.LookAt( new Vector3( 0, -1, 0 ), new Vector3( 0, 0, -1 ) );

	private VrGrabber grabber;
	private bool heldLeft;

	protected override void OnStart()
	{
		Renderer ??= Components.Get<ModelRenderer>();
		Body ??= Components.Get<Rigidbody>();
		Loaded ??= Model.Load( "models/weapons/pistol/magazine.mdl" );
		Empty ??= Model.Load( "models/weapons/pistol/magazine_empty.mdl" );
		Tags.Add( Tag );

		if ( Rounds < 0 ) Fill( Capacity );
	}

	/// <summary>So many rounds in it, and the model to match.</summary>
	public void Fill( int rounds )
	{
		Rounds = rounds.Clamp( 0, Capacity );

		// Asked before OnStart when a pistol drops one it has just made.
		Renderer ??= Components.Get<ModelRenderer>();
		Loaded ??= Model.Load( "models/weapons/pistol/magazine.mdl" );
		Empty ??= Model.Load( "models/weapons/pistol/magazine_empty.mdl" );

		if ( Renderer.IsValid() ) Renderer.Model = Rounds > 0 ? Loaded : Empty;
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

		// Top first into the grip of a pistol held in the other hand, roughly along it.
		var top = WorldTransform.PointToWorld( Top );

		foreach ( var pistol in Scene.GetAllComponents<VrPistol>() )
		{
			if ( !pistol.TakesMagazine || pistol.HeldLeft == heldLeft ) continue;

			var well = pistol.MagazineWell;
			if ( top.Distance( well.Position ) > InsertRadius ) continue;
			if ( Vector3.Dot( WorldRotation.Up, well.Rotation.Up ) < 0.6f ) continue;

			grabber.Forget( this );
			grabber = null;
			pistol.Insert( Rounds );
			GameObject.Destroy();
			return;
		}
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
