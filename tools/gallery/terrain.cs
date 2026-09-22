// Writes scenes/rendering/terrain.scene: a walk across a sculpted mesh - hills,
// painted layers, a cliff with an overhang, a cave, a hole, a rock set into the
// ground, clutter on the grass, and balls that roll on the collision mesh.
//
// Run with: python3 build.py terrain   (the editor must be open on Test Ground)
using Rinten.Resources;
using TestGround;

var S = new Gallery( "terrain", "Terrain",
	"A sculpted mesh: painted layers, an overhang, a cave, a hole, a rock set in, clutter on the grass, and balls rolling on the collision." );

int objects, triangles, vertices;
using ( S.Scene.Push() )
{
	const float SIZE = 72;
	const int RES = 96;
	const float RANGE = 32;
	const float HALF = SIZE / 2;

	Vector3 V( float x, float y, float z ) => Gallery.V( x, y, z );

	float Smooth( float t )
	{
		t = Math.Clamp( t, 0f, 1f );
		return t * t * ( 3 - 2 * t );
	}

	float Blob( float dx, float dz, float radius )
	{
		var t = 1 - MathF.Sqrt( dx * dx + dz * dz ) / MathF.Max( radius, 1e-4f );
		return t <= 0 ? 0 : Smooth( t );
	}

	/// Ground height in metres, in world XZ. The mesh is made from this, then
	/// the cave and the overhang are sculpted on top.
	float Ground( float wx, float wz )
	{
		var h = 0.45f
			+ 0.85f * MathF.Sin( wx * 0.11f ) * MathF.Cos( wz * 0.09f )
			+ 0.40f * MathF.Sin( wx * 0.27f + wz * 0.19f );

		// Spawn pad, south.
		if ( wz > 20 && MathF.Abs( wx ) < 16 )
			h = MathX.Lerp( h, 0.4f, Smooth( ( wz - 20 ) / 4 ) * Smooth( 1 - MathF.Abs( wx ) / 16 ) );

		// Hill the cave is dug into.
		h += 11.0f * Blob( wx + 10, wz + 14, 11 );

		// A smaller mound the sculpted hole punches through.
		h += 4.5f * Blob( wx - 10, wz - 6, 6 );

		// West cliff: a wall, later pulled into an overhang.
		if ( wx < -16 )
			h += 12.0f * Smooth( ( -16 - wx ) / 8 );

		// East ramp: high at the rim, down onto the path, balls roll west.
		if ( wx > 16 && wz > -10 && wz < 10 )
		{
			var across = Smooth( ( wx - 16 ) / 14 );
			var along = Smooth( 1 - MathF.Abs( wz ) / 10 );
			h = Math.Max( h, 0.5f + across * along * 6.5f );
		}

		return Math.Clamp( h, 0, RANGE - 0.5f );
	}

	float PathX( float wz ) => 1.4f * MathF.Sin( wz * 0.14f );

	ushort HeightBits( float metres ) => (ushort)Math.Clamp( metres / RANGE * 65535.0f, 0, 65535 );

	var storage = new TerrainStorage();
	storage.SetResolution( RES );
	storage.TerrainSize = SIZE;
	storage.TerrainHeight = RANGE;
	storage.Materials.Add( Material.Load( "materials/gallery/terrain/grass.mat" ) );
	storage.Materials.Add( Material.Load( "materials/gallery/terrain/dirt.mat" ) );
	storage.Materials.Add( Material.Load( "materials/gallery/terrain/rock.mat" ) );
	storage.Materials.Add( Material.Load( "materials/gallery/terrain/path.mat" ) );
	storage.EmbeddedResource = new EmbeddedResource { ResourceCompiler = "embed" };

	var unit = SIZE / RES;

	for ( var iz = 0; iz < RES; iz++ )
	{
		for ( var ix = 0; ix < RES; ix++ )
		{
			var wx = ( ix + 0.5f ) * unit - HALF;
			var wz = ( iz + 0.5f ) * unit - HALF;
			var at = iz * RES + ix;

			storage.HeightMap[at] = HeightBits( Ground( wx, wz ) );

			byte layer = 0;
			var slope = MathF.Abs( Ground( wx + 0.6f, wz ) - Ground( wx - 0.6f, wz ) )
				+ MathF.Abs( Ground( wx, wz + 0.6f ) - Ground( wx, wz - 0.6f ) );
			if ( slope > 1.8f ) layer = 2;
			else if ( slope > 0.55f ) layer = 1;
			if ( MathF.Abs( wx - PathX( wz ) ) < 1.7f && wz > -24 && wz < 30 ) layer = 3;

			var hole = MathF.Sqrt( ( wx - 16 ) * ( wx - 16 ) + ( wz + 22 ) * ( wz + 22 ) ) < 3.4f;
			storage.ControlMap[at] = new CompactTerrainMaterial( layer, 0, 0, hole ).Packed;
		}
	}

	var mesh = storage.Mesh;

	void PaintLayer( int v, int layer )
	{
		var vert = mesh.GetVertex( v );
		vert.Layers = new Color32(
			(byte)( layer == 0 ? 255 : 0 ),
			(byte)( layer == 1 ? 255 : 0 ),
			(byte)( layer == 2 ? 255 : 0 ),
			(byte)( layer == 3 ? 255 : 0 ) );
		vert.Layers2 = default;
		mesh.SetVertex( v, vert );
	}

	float LocalX( float wx ) => wx + HALF;
	float LocalZ( float wz ) => wz + HALF;

	mesh.BeginEdit();

	// Overhang: pull the top of the west wall east, over the path.
	for ( var i = 0; i < 8; i++ )
	{
		var wz = -8 + i * 2.2f;
		var centre = new Vector3( LocalX( -22 ), 10.5f, LocalZ( wz ) );
		mesh.Displace( centre, 5.5f, new Vector3( 1.0f, 0.12f, 0 ), 2.4f );
		mesh.Inflate( centre, 5.5f, -0.35f );
		mesh.Remesh( centre, 6.5f, storage.EdgeLength );
	}

	// Cave: bore north into the hill, facing the spawn.
	var mouth = new Vector3( LocalX( -10 ), 4.6f, LocalZ( -7.5f ) );
	var into = new Vector3( 0, 0.05f, -1 );
	for ( var i = 0; i < 12; i++ )
	{
		var centre = mouth + into * ( i * 0.75f );
		mesh.Displace( centre, 2.9f, into, 1.15f );
		mesh.Inflate( centre, 2.9f, -0.7f );
		mesh.Remesh( centre, 3.6f, storage.EdgeLength );
	}

	// Sculpted hole through the small mound - not the control-map hole.
	mesh.DeleteTriangles( new Vector3( LocalX( 10 ), 3.2f, LocalZ( 6 ) ), 2.6f );

	mesh.EndEdit();

	// After remesh: steep faces go to rock, the path stays the path.
	mesh.BeginEdit();
	for ( var v = 0; v < mesh.VertexSlots; v++ )
	{
		if ( !mesh.IsVertexAlive( v ) ) continue;

		var vert = mesh.GetVertex( v );
		if ( vert.Layers.a > 80 ) continue;

		var wx = vert.Position.x - HALF;
		var wz = vert.Position.z - HALF;
		if ( MathF.Abs( wx - PathX( wz ) ) < 1.7f && wz > -24 && wz < 30 )
		{
			PaintLayer( v, 3 );
			continue;
		}

		var steep = 1 - Math.Clamp( vert.Normal.y, 0, 1 );
		PaintLayer( v, steep > 0.38f ? 2 : steep > 0.14f ? 1 : 0 );
	}
	mesh.EndEdit();

	triangles = mesh.TriangleCount;
	vertices = mesh.VertexCount;

	S.Environment( sunBrightness: 1.7f, sunRot: Gallery.PitchYaw( -38, 200 ),
		ambient: "0.16,0.18,0.22,1", skyTint: "0.78,0.84,0.92,1", shadowDetail: 128, sourceRadius: 0.08f );

	var terrainGo = S.Go( S.Scene, "Terrain", V( -HALF, 0, 0 - HALF ), tags: "world" );
	var terrain = S.Comp<Terrain>( terrainGo, "terrain" );
	terrain.Storage = storage;
	terrain.ChunkSize = 64;
	terrain.RenderType = ModelRenderer.ShadowRenderType.On;
	terrain.EnableCollision = true;
	terrain.Friction = 0.72f;

	var clutter = S.Comp<TerrainClutter>( terrainGo, "clutter" );
	clutter.Seed = 7;
	clutter.Layers = new List<TerrainClutterLayer>
	{
		new()
		{
			Model = Model.Load( "models/jungle/grass_a.mdl" ),
			Density = 0.12f,
			Distance = 72,
			OnLayers = new List<int> { 0 },
			Scale = new RangedFloat( 0.7f, 1.15f ),
			MaxSlope = 28,
			RandomYaw = true,
		},
		new()
		{
			Model = Model.Load( "models/jungle/grass_b.mdl" ),
			Density = 0.06f,
			Distance = 64,
			OnLayers = new List<int> { 0 },
			Scale = new RangedFloat( 0.8f, 1.2f ),
			MaxSlope = 26,
			RandomYaw = true,
		},
		new()
		{
			Model = Model.Load( "models/jungle/pebbles_a.mdl" ),
			Density = 0.12f,
			Distance = 48,
			OnLayers = new List<int> { 2 },
			Scale = new RangedFloat( 0.55f, 1.05f ),
			MinSlope = 8,
			MaxSlope = 55,
			AlignToGround = true,
			RandomYaw = true,
		},
	};

	float At( float wx, float wz ) => terrain.HeightAt( new Vector2( LocalX( wx ), LocalZ( wz ) ) );
	Vector3 On( float wx, float wz, float lift = 0 ) => V( wx, At( wx, wz ) + lift, wz );

	GameObject Sign( string name, float wx, float wz, string text, float lift = 3.2f )
		=> S.Label( S.Scene, name, On( wx, wz, lift ), text, scale: 0.55f, size: 44 );

	Sign( "Pad", 0, 30, "terrain\nwalk north along the path\nQ returns" );
	Sign( "Hills", 0, 16, "hills\nfrom a height map, then sculpted" );
	Sign( "Layers", 8, 8, "layers\ngrass, dirt, rock by slope\nchecker is painted on" );
	Sign( "Ramp", 22, 2, "ramp\nballs roll on the mesh collider" );
	Sign( "Cliff", -18, 0, "overhang\ndisplace + inflate\nlook up from the path" );
	Sign( "Cave", -10, -6, "cave\ndig along the view\nroof collides" );
	Sign( "Sculpted hole", 10, 8, "sculpted hole\nDeleteTriangles" );
	Sign( "Imported hole", 16, -18, "imported hole\ncontrol map, no triangles" );
	Sign( "Insert", 8, -4, "mesh insert\na boulder still an object" );
	Sign( "Mesh", 0, -28, $"mesh\n{triangles:n0} triangles, {vertices:n0} vertices" );

	var boulder = S.Go( S.Scene, "Boulder", On( 7, -5, 0.15f ), scale: V( 1.15f, 1.15f, 1.15f ), tags: "world" );
	S.Model( boulder, "boulder", Color.White, null, "models/jungle/boulder_a.mdl" );
	var insert = S.Comp<TerrainMeshInsert>( boulder, "insert/boulder" );
	insert.Model = Model.Load( "models/jungle/boulder_a.mdl" );
	insert.Mode = TerrainMeshInsert.InsertMode.Embed;

	var balls = S.Go( S.Scene, "Balls" );
	var cycle = S.Comp<CycleReset>( balls, "cycle" );
	cycle.Period = 9;
	cycle.KickVelocity = V( -3.5f, 0.4f, 0 );

	GameObject Ball( string name, float wx, float wz, float lift, Color tint )
	{
		var go = S.Go( balls, name, On( wx, wz, lift ), scale: V( 0.45f, 0.45f, 0.45f ) );
		S.Model( go, name, tint, null, "models/dev/sphere.mdl" );
		var col = S.Comp<SphereCollider>( go, "collider/" + name );
		col.Static = false;
		col.Radius = 0.5f;
		var body = S.Comp<Rigidbody>( go, "body/" + name );
		body.Gravity = true;
		body.MotionEnabled = true;
		S.Comp<ResetOnFall>( go, "reset/" + name ).Height = -8;
		return go;
	}

	var first = Ball( "Ball 1", 26, -2, 0.5f, Gallery.C( "0.95,0.45,0.2,1" ) );
	Ball( "Ball 2", 27, 0, 0.5f, Gallery.C( "0.25,0.55,0.95,1" ) );
	Ball( "Ball 3", 26.5f, 2, 0.5f, Gallery.C( "0.3,0.8,0.45,1" ) );
	Ball( "Ball 4", 25, 1, 0.5f, Gallery.C( "0.95,0.8,0.25,1" ) );
	cycle.Kick = first;

	var probe = S.Go( S.Scene, "Trace Probe", On( 4, 22, 5.5f ), Gallery.PitchYaw( -58, 180 ) );
	S.Model( probe, "trace-mark", Gallery.C( "0.95,0.45,0.2,1" ), null, "models/dev/sphere.mdl" );
	probe.LocalScale = V( 0.18f, 0.18f, 0.18f );
	var trace = S.Comp<TraceProbe>( probe, "trace" );
	trace.Type = TraceProbe.Kind.Ray;
	trace.Length = 18;
	trace.DrawMiss = true;

	var player = S.Go( S.Scene, "Player", On( 0, 28, 0.05f ) );
	var camGo = S.Go( player, "Camera", V( 0, 1.5f, 0 ), Gallery.Yaw( 180 ), tags: "maincamera" );
	var cam = S.Comp<CameraComponent>( camGo, "camera" );
	cam.BackgroundColor = Gallery.C( "0.05,0.06,0.08,1" );
	cam.ClearFlags = ClearFlags.All;
	cam.FieldOfView = 75;
	cam.IsMainCamera = true;
	cam.Priority = 1;
	cam.ZFar = 400;
	cam.ZNear = 0.05f;
	var bloom = S.Comp<Bloom>( camGo, "bloom" );
	bloom.Mode = Bloom.BloomMode.Additive;
	bloom.Spread = 0.6f;
	bloom.Strength = 0.6f;
	bloom.Threshold = 1;

	var body = S.Go( player, "Body", V( 0, 0.78f, 0 ), scale: V( 0.7f, 1.55f, 0.7f ) );
	S.Model( body, "body", Gallery.C( "0.25,0.55,0.95,0.7" ) );

	var cc = S.Comp<CharacterController>( player, "controller" );
	cc.Height = 1.6f;
	cc.Radius = 0.4f;
	cc.StepHeight = 0.45f;
	cc.GroundAngle = 50;
	cc.Acceleration = 10;

	var walker = S.Comp<Walker>( player, "walker" );
	walker.Controller = cc;
	walker.Camera = cam;
	walker.Speed = 5.0f;
	walker.RunScale = 1.8f;
	walker.Jump = 5.5f;
	walker.FallHeight = -8;
	walker.EyeHeight = 1.5f;

	S.Hud( "Walk north along the path: hills, painted layers, a ramp of balls, an overhang, a cave, two holes. Fall resets. Q returns." );

	objects = S.Scene.Directory.AllGameObjects.Count();
}

var wrote = S.Write( "rendering/terrain.scene" );
Gallery.RegisterInMenu( "rendering/terrain.scene", "Terrain", "Rendering",
	"A sculpted mesh: painted layers, an overhang, a cave, a hole, a rock set in, clutter on the grass, balls on the collider" );

return new { Wrote = wrote, Objects = objects, Triangles = triangles, Vertices = vertices };
