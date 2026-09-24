namespace TestGround;

/// <summary>
/// A worm from the worm box, held between finger and thumb. Brought to a bare
/// hook - hanging from the line or held in the other hand - it goes on it: see
/// <see cref="VrFishingHook.Bait"/>. Let go anywhere else it falls, a small body,
/// and is gone after a while.
/// </summary>
/// <remarks>
/// The model's attachment hook is where the hook goes through it; without it,
/// its middle.
/// </remarks>
[Title( "VR Worm" )]
[Category( "Test Ground" )]
[Icon( "pest_control" )]
public sealed class VrWorm : Component, IVrHoldable
{
	[Property] public ModelRenderer Renderer { get; set; }
	[Property] public Rigidbody Body { get; set; }

	/// <summary>Where it sits in the grip's space while it is held.</summary>
	[Property, Category( "Hold" )] public Vector3 HoldOffset { get; set; } = new( 0, 0, -0.02f );
	[Property, Category( "Hold" )] public Angles HoldAngles { get; set; }

	/// <summary>How near the hook's point the worm's hook spot has to come for it to go on.</summary>
	[Property] public float BaitReach { get; set; } = 0.05f;

	/// <summary>Seconds a dropped worm lies about before it is gone.</summary>
	[Property] public float Lifetime { get; set; } = 90.0f;

	/// <summary>Where the hook goes through it, in the world.</summary>
	public Vector3 HookSpot => WorldTransform.PointToWorld( spot );

	private VrGrabber grabber;
	private bool heldLeft;
	private Vector3 spot;
	private TimeSince sinceDropped;
	private bool onHook;

	protected override void OnStart()
	{
		Renderer ??= Components.Get<ModelRenderer>( FindMode.EverythingInSelfAndDescendants );
		Body ??= Components.Get<Rigidbody>();
		spot = Renderer?.Model?.GetAttachment( "hook" )?.Position ?? Vector3.Zero;
		Tags.Add( VrFishingFloat.Tag );
	}

	public bool Grab( VrGrabber by, bool isLeft )
	{
		if ( onHook ) return false;

		grabber = by;
		heldLeft = isLeft;
		SetPhysics( false );
		Follow();
		return true;
	}

	public void Release( VrGrabber by, bool isLeft )
	{
		grabber = null;
		sinceDropped = 0;
		SetPhysics( true );
		if ( Body.IsValid() && Input.VR is not null ) Body.Velocity = VrGrabber.Hand( isLeft ).Velocity.ClampLength( 8.0f );
	}

	protected override void OnUpdate()
	{
		if ( onHook ) return;

		if ( grabber is null )
		{
			if ( sinceDropped > Lifetime ) GameObject.Destroy();
			return;
		}

		if ( Input.VR is not null ) Follow();

		foreach ( var hook in Scene.GetAllComponents<VrFishingHook>() )
		{
			if ( hook.Baited || hook.Fish is not null ) continue;
			if ( hook.Point.Distance( HookSpot ) > BaitReach ) continue;

			PutOn( hook );
			return;
		}
	}

	/// <summary>Onto the hook, out of the hand.</summary>
	public void PutOn( VrFishingHook hook )
	{
		if ( grabber is not null )
		{
			grabber.Forget( this );
			grabber.Components.Get<VrControllers>()?.SetHolding( heldLeft, false );
			grabber = null;
		}

		onHook = true;
		SetPhysics( false );
		hook.Bait( this );
	}

	private void Follow()
	{
		var frame = VrGrabber.HoldFrame( heldLeft );
		WorldTransform = frame.ToWorld( new Transform( HoldOffset, HoldAngles.ToRotation() ) );
	}

	private void SetPhysics( bool loose )
	{
		if ( Body.IsValid() )
		{
			Body.MotionEnabled = loose;
			if ( loose ) Body.Velocity = 0;
		}

		foreach ( var collider in Components.GetAll<Collider>( FindMode.EverythingInSelfAndDescendants ) )
			collider.Enabled = loose;
	}

	/// <summary>Where on the worm the hook goes through, in its own space.</summary>
	public Vector3 Spot => spot;
}
