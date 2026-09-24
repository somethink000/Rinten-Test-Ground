namespace TestGround;

/// <summary>
/// The hook on the end of the leader: an ordinary body that sinks slowly in the
/// water and hangs under the float, with a worm on it or not. A fish that finds
/// it baited takes it - see <see cref="VrFish"/> - and once struck the hook is in
/// its mouth and goes where the fish goes until a hand takes the fish off it.
/// </summary>
/// <remarks>
/// The model's attachments eye and point, and its body group bait (none, worm),
/// are what it knows about its shape; without them the eye is the origin.
/// </remarks>
[Title( "VR Fishing Hook" )]
[Category( "Test Ground" )]
[Icon( "phishing" )]
public sealed class VrFishingHook : Component
{
	[Property] public ModelRenderer Renderer { get; set; }
	[Property] public Rigidbody Body { get; set; }

	/// <summary>How much of its speed the water takes a second.</summary>
	[Property] public float WaterDrag { get; set; } = 8.0f;

	/// <summary>How much of its weight the water holds up - a worm on a light hook sinks slowly.</summary>
	[Property] public float Buoyancy { get; set; } = 0.6f;

	/// <summary>Whether there is a worm on it, which is what a fish comes for - a bare hook it ignores.</summary>
	[Property] public bool Baited { get; set; }

	/// <summary>Where the leader ties on, in the world.</summary>
	public Vector3 Eye => WorldTransform.PointToWorld( eyeLocal );

	/// <summary>The hook's point, where a worm goes on, in the world.</summary>
	public Vector3 Point => WorldTransform.PointToWorld( pointLocal );

	public bool InWater { get; private set; }

	/// <summary>The fish that has taken an interest in it - only one comes to a hook at a time.</summary>
	public VrFish Claimant { get; set; }

	/// <summary>The fish it is in, if one is hooked.</summary>
	public VrFish Fish { get; private set; }

	/// <summary>The rod has been jerked up: whichever fish is at the bait finds out.</summary>
	public void Struck() => Claimant?.Struck( this );

	private Vector3 eyeLocal, pointLocal;
	private GameObject worm;   // a worm carried on the point, when the model has none of its own to show

	protected override void OnStart()
	{
		Renderer ??= Components.Get<ModelRenderer>( FindMode.EverythingInSelfAndDescendants );
		Body ??= Components.Get<Rigidbody>();
		Tags.Add( VrFishingFloat.Tag );

		eyeLocal = Renderer?.Model?.GetAttachment( "eye" )?.Position ?? Vector3.Zero;
		pointLocal = Renderer?.Model?.GetAttachment( "point" )?.Position ?? new Vector3( 0, -0.0125f, -0.012f );
		ShowBait();
	}

	/// <summary>
	/// A worm brought to the point goes on. The model's own worm shows, if it has
	/// one - the bait body group - and the one from the hand goes; otherwise that
	/// one is carried on the point.
	/// </summary>
	public void Bait( VrWorm fresh )
	{
		if ( Baited )
		{
			fresh.GameObject.Destroy();
			return;
		}

		var own = Renderer?.Model?.Parts?.Get( "bait" ) is not null;
		if ( own )
		{
			fresh.GameObject.Destroy();
		}
		else
		{
			worm = fresh.GameObject;
			worm.SetParent( GameObject, true );
			worm.LocalRotation = Rotation.Identity;
			worm.LocalPosition = pointLocal - fresh.Spot;
		}

		SetBaited( true );
	}

	/// <summary>A worm on, or off - eaten, stolen, or put on fresh.</summary>
	public void SetBaited( bool baited )
	{
		Baited = baited;
		if ( !baited && worm.IsValid() ) worm.Destroy();
		if ( !baited ) worm = null;
		ShowBait();
	}

	private void ShowBait()
	{
		Renderer?.SetBodyGroup( "bait", Baited ? "worm" : "none" );
	}

	/// <summary>In a fish's mouth: carried by it, not falling, not colliding.</summary>
	public void Attach( VrFish fish )
	{
		Fish = fish;
		SetLoose( false );
	}

	/// <summary>Out of the fish's mouth, and a body again.</summary>
	public void Detach()
	{
		Fish = null;
		SetLoose( true );
	}

	private void SetLoose( bool loose )
	{
		if ( Body.IsValid() )
		{
			Body.MotionEnabled = loose;
			Body.Velocity = 0;
		}

		foreach ( var collider in Components.GetAll<Collider>( FindMode.EverythingInSelfAndDescendants ) )
			collider.Enabled = loose;
	}

	protected override void OnUpdate()
	{
		// In a mouth: the eye on the lip, the point in.
		if ( Fish.IsValid() )
		{
			var mouth = Fish.Mouth;
			WorldRotation = mouth.Rotation;
			WorldPosition = mouth.Position - WorldRotation * eyeLocal;
		}
		else if ( Fish is not null )
		{
			Detach();
		}
	}

	protected override void OnFixedUpdate()
	{
		if ( !Body.IsValid() || !Body.MotionEnabled ) return;

		var pond = VrPond.At( Scene, Eye );
		var was = InWater;
		InWater = pond is not null && pond.IsUnderwater( Eye );

		if ( InWater && !was ) pond.Splash( Eye, Body.Velocity.Length * 0.5f );
		if ( !InWater ) return;

		var dt = Time.Delta;
		Body.ApplyForce( -Scene.PhysicsWorld.Gravity * Body.Mass * Buoyancy );
		Body.Velocity *= System.MathF.Exp( -WaterDrag * dt );
		Body.AngularVelocity *= System.MathF.Exp( -WaterDrag * dt );
	}
}
