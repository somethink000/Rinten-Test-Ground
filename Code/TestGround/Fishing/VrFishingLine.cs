namespace TestGround;

/// <summary>
/// The line from the rod tip to the float, and the leader from the float to the
/// hook. The main line is a verlet rope of points about <see cref="SegmentLength"/>
/// apart - more of them as line comes off the reel, fewer as it goes back on, the
/// new ones at the tip - which sags, drifts and lies on the water; the leader is
/// only a length the hook cannot hang further than.
/// </summary>
/// <remarks>
/// <para>
/// The line weighs nothing next to what is on it, so the rope's own points never
/// move the float: only the line pulled straight does. When the float is further
/// from the tip than there is line, it is put back on the line's length and loses
/// its speed away - and that, the pull it took, is the <see cref="Tension"/>, and
/// what the rod bends to. The reel may give line instead: all of it with the bail
/// open, and whatever is over the drag with it shut - see <see cref="VrFishingRod"/>.
/// </para>
/// <para>
/// A hooked fish in the water is its own end: it keeps itself on the line's
/// length and says how hard it pulls - see <see cref="Pull"/> and <see cref="Give"/>.
/// </para>
/// </remarks>
[Title( "VR Fishing Line" )]
[Category( "Test Ground" )]
[Icon( "timeline" )]
public sealed class VrFishingLine : Component
{
	[Property] public VrFishingRod Rod { get; set; }
	[Property] public VrFishingFloat Float { get; set; }
	[Property] public VrFishingHook Hook { get; set; }
	[Property] public LineRenderer Renderer { get; set; }

	/// <summary>Line out past the tip to begin with, in metres.</summary>
	[Property, Category( "Length" )] public float StartLength { get; set; } = 0.6f;
	[Property, Category( "Length" )] public float MinLength { get; set; } = 0.25f;
	[Property, Category( "Length" )] public float MaxLength { get; set; } = 40.0f;

	/// <summary>From the float's eye down to the hook, in metres.</summary>
	[Property, Category( "Length" )] public float LeaderLength { get; set; } = 0.5f;

	/// <summary>How far apart the drawn line's points are, in metres. The rope itself is solved coarser.</summary>
	[Property, Category( "Simulation" )] public float SegmentLength { get; set; } = 0.002f;
	[Property, Category( "Simulation" )] public int Iterations { get; set; } = 64;

	/// <summary>
	/// The solved rope's spacing. A point every couple of millimetres cannot be
	/// pulled onto the float in the iterations a frame has, so the end is pinned
	/// to the eye and the rest of the line hangs below it.
	/// </summary>
	private float SolvedSpacing => System.MathF.Max( SegmentLength, 0.025f );

	/// <summary>How much of the line's speed the air takes a second.</summary>
	[Property, Category( "Simulation" )] public float AirDrag { get; set; } = 0.6f;

	/// <summary>How much of the line's speed the water takes a second.</summary>
	[Property, Category( "Simulation" )] public float WaterDrag { get; set; } = 14.0f;

	/// <summary>How much of gravity is left for line under water - it sinks, slowly.</summary>
	[Property, Category( "Simulation" )] public float WaterGravity { get; set; } = 0.08f;

	/// <summary>How much of the speed of line running off an open spool its friction takes, a second.</summary>
	[Property, Category( "Simulation" )] public float SpoolFriction { get; set; } = 0.4f;

	/// <summary>How quickly the reading of the tension follows the pull, a second.</summary>
	[Property, Category( "Simulation" )] public float TensionSmoothing { get; set; } = 12.0f;

	[Property, Category( "Look" )] public Color Colour { get; set; } = new Color( 0.85f, 0.9f, 0.8f, 0.8f );

	/// <summary>Half the line's thickness as drawn, in metres - more than real, to be seen at all.</summary>
	[Property, Category( "Look" )] public float Width { get; set; } = 0.0008f;

	/// <summary>Line out past the tip, in metres - the leader not counted.</summary>
	public float Length { get; private set; }

	/// <summary>How hard the line pulls on the rod tip, in newtons.</summary>
	public float Tension { get; private set; }

	/// <summary>Which way the line leaves the tip.</summary>
	public Vector3 TipDirection { get; private set; } = Vector3.Down;

	/// <summary>Whether the line runs straight from the tip to the float, and pulls.</summary>
	public bool Taut { get; private set; }

	public IReadOnlyList<Vector3> Points => points;

	private readonly List<Vector3> points = new();
	private readonly List<Vector3> previous = new();
	private readonly List<Vector3> drawn = new();
	private float pulled;      // the tension the hooked fish says it pulls with, this step
	private float given;       // line given to the fish this step, in metres
	private int step;
	private bool started;

	protected override void OnStart()
	{
		Rod ??= Components.GetInAncestorsOrSelf<VrFishingRod>();
		Renderer ??= Components.Get<LineRenderer>();
		Length = StartLength;

		// The float and hook are bodies of their own: in the rod's hierarchy they
		// would be carried by it.
		Float?.GameObject.SetParent( null, true );
		Hook?.GameObject.SetParent( null, true );
		started = true;

		if ( Renderer.IsValid() )
		{
			Renderer.UseVectorPoints = true;
			Renderer.VectorPoints = drawn;
			Renderer.Color = Colour;
			Renderer.Width = Width;
			Renderer.Face = SceneLineObject.FaceMode.Cylinder;
			// The points are already the curve. The renderer's own spline bows past
			// the float's eye, so the line kinks under it and the float looks loose.
			Renderer.SplineInterpolation = 1;
			Renderer.CylinderSegments = 6;
			Renderer.CastShadows = false;
			Renderer.Opaque = false;
		}
	}

	protected override void OnDestroy()
	{
		// Only once they have been let go of the rod's hierarchy - otherwise they go with it anyway.
		if ( !started ) return;
		if ( Float.IsValid() ) Float.GameObject.Destroy();
		if ( Hook.IsValid() ) Hook.GameObject.Destroy();
	}

	protected override void OnFixedUpdate()
	{
		if ( !Rod.IsValid() || !Float.IsValid() ) return;

		Simulate( Time.Delta );
	}

	/// <summary>Line taken back onto the reel, in metres.</summary>
	public void Reel( float metres ) => Length = ( Length - metres ).Clamp( MinLength, MaxLength );

	/// <summary>Line let off the reel, in metres.</summary>
	public void PayOut( float metres ) => Length = ( Length + metres ).Clamp( MinLength, MaxLength );

	/// <summary>The float and the hook thrown - a cast, at the tip's speed.</summary>
	public void Throw( Vector3 velocity )
	{
		if ( Float.IsValid() && Float.Body.IsValid() ) Float.Body.Velocity = velocity;
		if ( Hook.IsValid() && Hook.Body.IsValid() && Hook.Fish is null ) Hook.Body.Velocity = velocity * 0.97f;
	}

	/// <summary>The hooked fish pulls the line with this many newtons, this step.</summary>
	public void Pull( float newtons ) => pulled = System.MathF.Max( pulled, newtons );

	/// <summary>
	/// A hooked fish is <paramref name="beyond"/> metres further out than the line
	/// reaches, pulling with <paramref name="newtons"/>: how much line the reel gives
	/// it - the rest it is held to.
	/// </summary>
	public float Give( float beyond, float newtons )
	{
		if ( beyond <= 0 ) return 0;

		Pull( newtons );

		var give = 0.0f;
		if ( Rod.FreeSpool ) give = beyond;
		else if ( newtons > Rod.Drag )
		{
			// A slip of the drag, not the whole gap. Moving the rod would otherwise
			// pay out every metre the tip travelled.
			var slip = ( newtons - Rod.Drag ) * 0.04f * Time.Delta;
			give = System.MathF.Min( beyond, slip );
		}

		give = System.MathF.Min( give, MaxLength - Length );
		Length += give;
		given += give;
		return give;
	}

	/// <summary>One step of the line: the rope, then the leader, then the line pulled straight.</summary>
	public void Simulate( float dt )
	{
		if ( dt <= 0 ) return;

		step++;
		var tip = Rod.Tip;
		var gravity = Scene.PhysicsWorld.Gravity;
		var pond = Float.Pond ?? VrPond.At( Scene, tip );

		Fit( tip );
		var last = points.Count - 1;
		points[0] = previous[0] = tip;

		// Carried: gravity, and the air or the water slowing it.
		for ( var i = 1; i < last; i++ )
		{
			var p = points[i];
			var velocity = p - previous[i];
			var wet = pond is not null && pond.IsUnderwater( p );
			velocity *= System.MathF.Exp( -( wet ? WaterDrag : AirDrag ) * dt );

			previous[i] = p;
			points[i] = p + velocity + gravity * ( wet ? WaterGravity : 1.0f ) * dt * dt;
		}

		Leader( dt );

		points[last] = Float.LinePoint;

		// The rope's points between the tip and the float, each end held.
		// Enough passes that the segment into the eye is actually one spacing
		// long - otherwise the line arrives from somewhere below the float.
		var rest = Length / last;
		var budget = System.Math.Clamp( System.Math.Max( Iterations, last / 2 ), Iterations, 400 );
		for ( var k = 0; k < budget; k++ )
		{
			for ( var i = 0; i < last; i++ )
			{
				var delta = points[i + 1] - points[i];
				var distance = delta.Length;
				if ( distance < 0.0001f ) continue;

				var error = ( distance - rest ) / distance;
				var wa = i == 0 ? 0.0f : 1.0f;
				var wb = i + 1 == last ? 0.0f : 1.0f;
				if ( wa + wb <= 0 ) continue;

				points[i] += delta * ( error * wa / ( wa + wb ) );
				points[i + 1] -= delta * ( error * wb / ( wa + wb ) );
			}

			if ( k + 1 >= Iterations && ( points[last] - points[last - 1] ).Length <= rest * 1.5f ) break;
		}

		points[last] = Float.LinePoint;

		Collide( pond );
		Straighten( tip, dt );

		// The water lays whatever is under it on the surface, near enough.
		if ( pond is not null )
		{
			for ( var i = 1; i < last; i++ )
			{
				var depth = pond.Depth( points[i] );
				if ( depth > 0.02f && !Taut ) points[i] = points[i].WithY( MathX.Lerp( points[i].y, pond.SurfaceHeight - 0.01f, dt * 2.0f ) );
			}
		}

		var first = points.Count > 1 ? points[1] - tip : Vector3.Down;
		if ( first.LengthSquared > 0.000001f ) TipDirection = first.Normal;

		pulled = 0;
		given = 0;
	}

	/// <summary>As many points as the line's length wants, new ones and spent ones at the tip end.</summary>
	private void Fit( Vector3 tip )
	{
		var wanted = System.Math.Clamp( (int)System.MathF.Ceiling( Length / SolvedSpacing ), 1, 500 ) + 1;

		if ( points.Count < 2 )
		{
			points.Clear();
			previous.Clear();
			var end = Float.LinePoint;
			for ( var i = 0; i < wanted; i++ )
			{
				var p = Vector3.Lerp( tip, end, i / (float)( wanted - 1 ) );
				points.Add( p );
				previous.Add( p );
			}
			return;
		}

		while ( points.Count < wanted )
		{
			points.Insert( 1, tip );
			previous.Insert( 1, tip );
		}

		while ( points.Count > wanted )
		{
			points.RemoveAt( 1 );
			previous.RemoveAt( 1 );
		}
	}

	/// <summary>
	/// The hook kept within the leader of the float. Each gives by the other's
	/// share of their weight - a fish in the water gives nothing.
	/// </summary>
	private void Leader( float dt )
	{
		if ( !Hook.IsValid() ) return;

		var fish = Hook.Fish;
		var hookEnd = fish.IsValid() ? fish.Mouth.Position : Hook.Eye;
		var floatEnd = Float.LinePoint;
		var delta = hookEnd - floatEnd;
		var distance = delta.Length;
		if ( distance <= LeaderLength ) return;

		var excess = distance - LeaderLength;
		var direction = delta / distance;

		Rigidbody hookBody = null;
		if ( fish.IsValid() ) hookBody = fish.Landed ? fish.Body : null;
		else if ( Hook.Body.IsValid() && Hook.Body.MotionEnabled ) hookBody = Hook.Body;

		var floatBody = Float.Body.IsValid() && Float.Body.MotionEnabled ? Float.Body : null;

		var mf = floatBody is null ? 0.0f : floatBody.Mass;
		var mh = hookBody is null ? 0.0f : hookBody.Mass;

		// Nothing to give: the float goes to a pinned hook, or the hook to a held float.
		var floatShare = hookBody is null ? 1.0f : floatBody is null ? 0.0f : mh / ( mf + mh );

		if ( floatBody is not null ) Correct( floatBody, direction * excess * floatShare, hookEnd );
		if ( hookBody is not null ) Correct( hookBody, -direction * excess * ( 1.0f - floatShare ), hookEnd );
	}

	/// <summary>
	/// The line pulled straight: a float further from the tip than there is line is
	/// put back on it, unless the reel gives - and what that took is the tension.
	/// </summary>
	private void Straighten( Vector3 tip, float dt )
	{
		var last = points.Count - 1;
		var end = points[last];
		var delta = end - tip;
		var distance = delta.Length;

		Taut = distance > Length * 0.98f;

		var raw = pulled;

		if ( distance > Length && distance > 0.0001f )
		{
			var direction = delta / distance;
			var excess = distance - Length;
			var body = Float.Body;
			var mass = Float.Body.IsValid() ? Float.Body.Mass : 0.05f;

			// What is under the float and hangs from it pulls through it too.
			if ( Hook.IsValid() && Hook.Fish is null && Hook.Body.IsValid() && Hook.Eye.Distance( end ) > LeaderLength * 0.95f ) mass += Hook.Body.Mass;
			if ( Hook.IsValid() && Hook.Fish.IsValid() && Hook.Fish.Landed ) mass += Hook.Fish.Weight;

			var outward = body.IsValid() ? System.MathF.Max( Vector3.Dot( body.Velocity, direction ), 0 ) : 0;
			var wanted = mass * outward / System.MathF.Max( dt, 0.001f );

			// A shut reel holds. The gap is the tip moving, and the tackle comes
			// with it - it is not new line. Only an open spool pays that out.
			var give = 0.0f;
			if ( Rod.FreeSpool ) give = excess;

			give = System.MathF.Min( give, MaxLength - Length );
			Length += give;
			given += give;
			var kept = excess > 0 ? give / excess : 0;
			excess -= give;

			raw = System.MathF.Max( raw, Rod.FreeSpool ? mass * outward * SpoolFriction : System.MathF.Min( wanted, Rod.Drag * 1.2f ) );

			// Line off an open spool: only the spool's friction holds it back.
			if ( Rod.FreeSpool && body.IsValid() && body.MotionEnabled && outward > 0 )
				body.Velocity -= direction * outward * ( 1.0f - System.MathF.Exp( -SpoolFriction * dt ) );

			if ( body.IsValid() && body.MotionEnabled )
			{
				// Open spool: ease it, or the float is thrown. Shut spool: the tackle
				// comes with the rod, the whole gap, or the line looks like it stretches.
				var step = Rod.FreeSpool ? System.MathF.Min( excess, 0.04f ) : excess;
				Correct( body, -direction * step, end, kept );
				var outwardNow = Vector3.Dot( body.Velocity, direction );
				if ( outwardNow > 0 ) body.Velocity -= direction * outwardNow;
				points[last] = Float.LinePoint;
			}
		}

		Float.LinePull = Taut ? -( points[last] - points[System.Math.Max( last - 1, 0 )] ).Normal * raw : Vector3.Zero;
		Tension = MathX.Lerp( Tension, raw, 1.0f - System.MathF.Exp( -TensionSmoothing * dt ) );

		if ( given > 0 ) Rod.LineGiven( given );
	}

	/// <summary>
	/// A body put back by <paramref name="move"/>, losing its speed the other way -
	/// all but the share <paramref name="kept"/> the reel let run.
	/// </summary>
	private static void Correct( Rigidbody body, Vector3 move, Vector3 at, float kept = 0 )
	{
		var length = move.Length;
		if ( length < 0.0000001f ) return;

		var normal = move / length;
		body.WorldPosition += move;

		var against = Vector3.Dot( body.Velocity, normal );
		if ( against < 0 ) body.ApplyImpulseAt( at, -normal * against * body.Mass * ( 1.0f - kept ) );
	}

	/// <summary>A few of the rope's points a step kept out of the world, each in turn - enough for a line.</summary>
	private void Collide( VrPond pond )
	{
		var last = points.Count - 1;
		for ( var i = 1 + step % 3; i < last; i += 3 )
		{
			var from = previous[i];
			var to = points[i];
			if ( from.DistanceSquared( to ) < 0.000001f ) continue;

			var hit = Scene.Trace.Ray( from, to )
				.WithoutTags( VrFishingFloat.Tag, VrControllers.HandTag, VrFish.Tag )
				.IgnoreGameObjectHierarchy( Rod.GameObject )
				.Run();

			if ( !hit.Hit ) continue;

			points[i] = hit.EndPosition + hit.Normal * 0.003f;
			previous[i] = points[i];
		}
	}

	/// <summary>
	/// Points of <paramref name="path"/> from <paramref name="first"/> on, spaced
	/// <paramref name="spacing"/> apart, starting from the point already last in <paramref name="dst"/>.
	/// </summary>
	private static void AppendEven( List<Vector3> dst, List<Vector3> path, int first, float spacing )
	{
		if ( dst.Count == 0 || path.Count <= first ) return;

		spacing = System.MathF.Max( spacing, 0.001f );
		var leftover = 0.0f;

		for ( var i = first; i < path.Count; i++ )
		{
			var a = i == first ? dst[^1] : path[i - 1];
			var b = path[i];
			var delta = b - a;
			var distance = delta.Length;
			if ( distance < 0.00001f ) continue;

			var dir = delta / distance;
			var t = spacing - leftover;
			while ( t <= distance )
			{
				dst.Add( a + dir * t );
				t += spacing;
			}

			leftover = t - distance;
		}
	}

	protected override void OnPreRender()
	{
		if ( !Renderer.IsValid() || !Rod.IsValid() || !Float.IsValid() ) return;

		drawn.Clear();
		Rod.AddLinePath( drawn );

		var floatEye = Float.LinePoint;
		if ( points.Count > 1 ) points[^1] = floatEye;

		// Rounded for drawing only. The ends stay, so the line still meets the eye.
		var smooth = new List<Vector3>( points );
		for ( var pass = 0; pass < 6; pass++ )
		{
			var prev = smooth.ToArray();
			for ( var i = 1; i < smooth.Count - 1; i++ )
				smooth[i] = Vector3.Lerp( prev[i], ( prev[i - 1] + prev[i + 1] ) * 0.5f, 0.7f );
		}

		AppendEven( drawn, smooth, 1, SegmentLength );
		if ( drawn.Count == 0 || drawn[^1].DistanceSquared( floatEye ) > 0.0000001f ) drawn.Add( floatEye );

		if ( Hook.IsValid() )
		{
			// The leader: straight when it pulls, a little sag when it does not.
			var hook = Hook.Eye;
			var slack = LeaderLength - floatEye.Distance( hook );
			if ( slack > 0.02f ) drawn.Add( Vector3.Lerp( floatEye, hook, 0.5f ) + Vector3.Down * slack * 0.4f );
			drawn.Add( hook );
		}

		Renderer.VectorPoints = drawn;
		WorldPosition = Rod.Tip;
	}
}
