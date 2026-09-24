namespace TestGround;

/// <summary>
/// The float on the end of the line: an ordinary body that falls, is picked up
/// by hand and thrown - and in the water carries itself so its waterline sits at
/// the surface, stands up in calm water and lies over when the line pulls it
/// sideways. A fish at the bait shows here: a nibble bobs it, a bite takes it
/// under - see <see cref="Dip"/>.
/// </summary>
/// <remarks>
/// The model gives it the attachments line (the bottom eye, where the main line
/// and the leader tie on) and waterline; without them the eye is the origin and
/// the waterline <see cref="DefaultWaterline"/> up it - see
/// ~/Documents/Blender/tools/fishing/SPEC.md.
/// </remarks>
[Title( "VR Fishing Float" )]
[Category( "Test Ground" )]
[Icon( "sailing" )]
public sealed class VrFishingFloat : Component
{
	[Property] public ModelRenderer Renderer { get; set; }
	[Property] public Rigidbody Body { get; set; }

	/// <summary>How high up the float the waterline is, when the model does not say.</summary>
	[Property] public float DefaultWaterline { get; set; } = 0.12f;

	/// <summary>
	/// The weight the float carries at its waterline, besides its own, in
	/// kilograms: the hook and shot hanging under it. More and it rides lower.
	/// </summary>
	[Property] public float Load { get; set; } = 0.03f;

	/// <summary>How hard it stands itself up in the water: turn a second squared, a radian off upright.</summary>
	[Property] public float Uprighting { get; set; } = 18.0f;

	/// <summary>How much of its speed the water takes a second.</summary>
	[Property] public float WaterDrag { get; set; } = 12.0f;

	/// <summary>How many times over the whole float, eye to its reserve above the waterline, carries it and its load.</summary>
	[Property] public float Reserve { get; set; } = 1.5f;

	/// <summary>The line pull, in newtons, at which it lies flat on the water.</summary>
	[Property] public float LieOverPull { get; set; } = 0.4f;

	public const string Tag = "vr_fishing";

	/// <summary>Where the line ties on, in the world.</summary>
	public Vector3 LinePoint => WorldTransform.PointToWorld( lineLocal );

	/// <summary>Whether it is in the water now.</summary>
	public bool InWater { get; private set; }

	public VrPond Pond { get; private set; }

	/// <summary>The line's pull on it, set by the line every step - it lies over towards it.</summary>
	public Vector3 LinePull { get; set; }

	private Vector3 lineLocal;
	private Vector3 waterlineLocal;
	private float dip, dipTime;

	protected override void OnStart()
	{
		Renderer ??= Components.Get<ModelRenderer>( FindMode.EverythingInSelfAndDescendants );
		Body ??= Components.Get<Rigidbody>();
		Tags.Add( Tag );

		var model = Renderer?.Model;
		lineLocal = model?.GetAttachment( "line" )?.Position ?? Vector3.Zero;
		waterlineLocal = model?.GetAttachment( "waterline" )?.Position ?? new Vector3( 0, DefaultWaterline, 0 );
	}

	/// <summary>
	/// Pulled down by a fish: <paramref name="strength"/> times what holds it up,
	/// for <paramref name="seconds"/> - a short one is a bob, a long hard one a bite.
	/// </summary>
	public void Dip( float strength, float seconds )
	{
		dip = strength;
		dipTime = seconds;
	}

	protected override void OnFixedUpdate()
	{
		if ( !Body.IsValid() || !Body.MotionEnabled ) return;

		Float( Time.Delta );
	}

	/// <summary>One step of the water carrying it, if it is in some.</summary>
	public void Float( float dt )
	{
		var bottom = LinePoint;
		var top = WorldTransform.PointToWorld( waterlineLocal * Reserve );
		Pond = VrPond.At( Scene, bottom ) ?? VrPond.At( Scene, top );

		// How much of the body - the eye up past the waterline, to the reserve - is
		// under, measured along it: either end can be the low one.
		var surface = Pond?.SurfaceHeight ?? float.MinValue;
		var low = System.MathF.Min( bottom.y, top.y );
		var high = System.MathF.Max( bottom.y, top.y );
		var under = high - low < 0.001f ? ( low < surface ? 1.0f : 0.0f ) : ( ( surface - low ) / ( high - low ) ).Clamp( 0, 1 );

		var wasInWater = InWater;
		InWater = Pond is not null && Pond.Covers( bottom ) && under > 0;

		if ( InWater && !wasInWater ) Pond.Splash( bottom, Body.Velocity.Length );
		if ( !InWater ) return;

		// All of it under holds up the float and its load Reserve times over, so it
		// rests with the waterline at the surface. The lift is at the middle of
		// the part that is under.
		var gravity = Scene.PhysicsWorld.Gravity;
		var weight = ( Body.Mass + Load ) * -gravity.y;
		// At the centre of mass: a lift off to one side spins the float over.
		Body.ApplyForce( Vector3.Up * weight * Reserve * under );

		// A fish: down, harder than the water holds it up.
		if ( dipTime > 0 )
		{
			dipTime -= dt;
			Body.ApplyForce( Vector3.Down * weight * dip );
		}

		// Up in calm water; towards lying over, bottom first, as the line pulls it along the surface.
		var flat = LinePull.WithY( 0 );
		var lean = ( flat.Length / LieOverPull ).Clamp( 0, 1 );
		var wanted = lean > 0.01f ? Vector3.Lerp( Vector3.Up, -flat.Normal, lean * 0.9f ).Normal : Vector3.Up;
		var axis = Vector3.Cross( WorldRotation.Up, wanted );
		Body.AngularVelocity += axis * Uprighting * System.MathF.Max( under, 0.3f ) * dt;

		var drag = System.MathF.Exp( -WaterDrag * dt * System.MathF.Max( under, 0.2f ) );
		Body.Velocity *= drag;
		Body.AngularVelocity *= drag;
	}
}
