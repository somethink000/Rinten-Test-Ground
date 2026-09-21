// Writes scenes/rendering/shadows.scene: the sun over a long field for its cascades and
// detail, every kind of caster, source radii, point and spot lights with their
// own shadows, lights and casters that move, and the surfaces shadows land on.
// The sun's own settings are on the number keys - see ShadowRack.
//
// Run with: python3 build.py shadows   (the editor must be open on Test Ground)
using TestGround;

var S = new Gallery( "shadows", "Shadows",
	"The sun's cascades and detail over a long field, every kind of caster, source radii, point and spot shadows, moving lights and casters, and the surfaces they land on." );

// Built with the scene pushed, so anything that asks for the active scene gets this one, not the editor's.
int objects;
using ( S.Scene.Push() )
{
	var PEDESTAL = Gallery.C( "0.2,0.22,0.26,1" );
	var FLOOR = Gallery.C( "0.62,0.6,0.56,1" );
	var DARK = Gallery.C( "0.12,0.12,0.14,1" );
	var GREY = Gallery.C( "0.6,0.6,0.6,1" );
	var BONE = Gallery.C( "0.85,0.8,0.7,1" );
	var WHITE = Color.White;

	Vector3 V( float x, float y, float z ) => Gallery.V( x, y, z );

	GameObject Sign( GameObject parent, string name, string text, Vector3 pos, float scale = 0.38f )
		=> S.Label( parent, name, pos, text, scale: scale, size: 44 );

	GameObject Station( GameObject parent, string name, string text, Vector3 pos, float signY = 3.0f, bool pedestal = true )
	{
		var station = S.Go( parent, "Station: " + name, pos );
		if ( pedestal ) S.Block( station, "Pedestal: " + name, V( 0, 0.1f, 0 ), V( 1.6f, 0.2f, 1.6f ), PEDESTAL );
		Sign( station, name, text, V( 0, signY, 0 ) );
		return station;
	}

	GameObject Cube( GameObject parent, string name, Vector3 pos, Vector3? size = null, Color? tint = null, string material = null,
		ModelRenderer.ShadowRenderType render = ModelRenderer.ShadowRenderType.On, Rotation? rot = null, string model = "models/dev/box.mdl" )
	{
		var go = S.Go( parent, name, pos, rot, size ?? V( 0.8f, 0.8f, 0.8f ) );
		S.Model( go, name, tint ?? BONE, material, model, render );
		return go;
	}

	// Brightness is what the Lights scene uses for a pool that reads: tens, with
	// the attenuation low, not the sun's ones.
	GameObject PointLight( GameObject parent, string name, Vector3 pos, Color? color = null, float brightness = 6, float radius = 8, bool shadows = true, float source = 0.05f )
	{
		var go = S.Go( parent, "Light: " + name, pos, tags: "light_point,light" );
		var l = S.Comp<PointLight>( go, "light/" + name );
		l.Attenuation = 0.15f;
		l.Brightness = brightness;
		l.LightColor = color ?? WHITE;
		l.Radius = radius;
		l.Shadows = shadows;
		l.SourceRadius = source;
		return go;
	}

	GameObject SpotLight( GameObject parent, string name, Vector3 pos, Rotation rot, Color? color = null, float brightness = 12, float radius = 12, float outer = 35, float inner = 25, bool shadows = true, string cookie = null, float source = 0.05f )
	{
		var go = S.Go( parent, "Light: " + name, pos, rot, tags: "light_spot,light" );
		var l = S.Comp<SpotLight>( go, "light/" + name );
		l.Attenuation = 0.15f;
		l.Brightness = brightness;
		l.ConeInner = inner;
		l.ConeOuter = outer;
		l.Cookie = cookie is null ? null : Texture.Load( cookie );
		l.LightColor = color ?? WHITE;
		l.Radius = radius;
		l.Shadows = shadows;
		l.SourceRadius = source;
		return go;
	}

	Spinner Spin( GameObject go, string name, Vector3 axis, float speed = 45 )
	{
		var s = S.Comp<Spinner>( go, "spin/" + name );
		s.Axis = axis;
		s.Speed = speed;
		s.Local = true;
		return s;
	}

	Oscillator Oscillate( GameObject go, string name, Vector3 axis, float amplitude = 1, float speed = 0.5f, float phase = 0 )
	{
		var o = S.Comp<Oscillator>( go, "osc/" + name );
		o.Axis = axis;
		o.Amplitude = amplitude;
		o.Speed = speed;
		o.Phase = phase;
		return o;
	}

	Orbit OrbitRound( GameObject go, string name, GameObject centre, float radius = 2, float period = 6, float tilt = 0 )
	{
		var o = S.Comp<Orbit>( go, "orbit/" + name );
		o.Centre = centre;
		o.Radius = radius;
		o.Period = period;
		o.Tilt = tilt;
		return o;
	}

	/// A slab over a row, so the sun stays out and the row's own lights are what shows; the row's own slab is dark.
	GameObject Roof( GameObject parent, string name, float z, float width )
		=> S.Block( parent, "Roof: " + name, V( 0, 7, z ), V( width, 0.3f, 16 ), Gallery.C( "0.25,0.26,0.3,1" ) );

	const float ROW_DEPTH = 20;
	var z = -8f;

	// ---------------------------------------------------------------- the scene, in the order its objects go

	// A sun from behind the spawn, high enough that shadows land on the slabs in front of the walls.
	S.Environment( sunBrightness: 1.6f, sunRot: Gallery.PitchYaw( -40, 210 ), ambient: "0.12,0.13,0.17,1", shadowDetail: 64, sourceRadius: 0.05f );
	S.Block( S.Scene, "Ground", V( 0, -0.7f, -110 ), V( 240, 0.5f, 320 ), FLOOR );

	// -- the field: posts every six metres out to the horizon ----------------------
	// A pale floor so the shadows read, posts and beams going away for the
	// cascades to hand over on, a tall gate at the far end. The keys change the
	// sun over all of it.
	var field = S.Go( S.Scene, "Field" );
	S.Block( field, "Field floor", V( 0, -0.15f, -60 ), V( 60, 0.3f, 140 ), FLOOR );
	for ( var i = 0; i < 20; i++ )
	{
		var zz = -6 - i * 6;
		Cube( field, $"Post {i}", V( -6, 1.5f, zz ), V( 0.4f, 3, 0.4f ) );
		Cube( field, $"Post R {i}", V( 6, 1.5f, zz ), V( 0.4f, 3, 0.4f ) );
		if ( i % 4 == 0 )
		{
			Cube( field, $"Beam {i}", V( 0, 3.2f, zz ), V( 12.4f, 0.4f, 0.4f ) );
			S.Label( field, $"Distance {i}", V( 0, 4.2f, zz ), $"{-zz} m", scale: 0.6f, size: 44 );
		}
	}
	Cube( field, "Gate L", V( -12, 6, -126 ), V( 1, 12, 1 ) );
	Cube( field, "Gate R", V( 12, 6, -126 ), V( 1, 12, 1 ) );
	Cube( field, "Gate top", V( 0, 12.5f, -126 ), V( 25, 1, 1 ) );
	Sign( field, "Field", "the field\nposts every 6 m, beams every 24 m, a gate at 120 m\nkeys 1-5 change the sun", V( 0, 5.6f, -6 ), scale: 0.6f );

	var areas = S.Go( S.Scene, "Areas" );

	// -- casters ---------------------------------------------------------------------
	const string CUT_LEAF = "materials/gallery/blend/leaf.mat";
	const string CUT_RING = "materials/gallery/blend/cut_05.mat";
	const string TRANS = "materials/gallery/blend/trans_05.mat";
	const string GLASS = "materials/common/glass.mat";
	const string ONE_SIDED = "materials/gallery/sides/one.mat";
	const string TWO_SIDED = "materials/gallery/sides/two.mat";
	var UPRIGHT = Gallery.Upright;
	const string PLANE = "models/dev/plane.mdl";
	const string SPHERE = "models/dev/sphere.mdl";
	const string URN = "models/props/urn_broken.mdl";

	var casters = new (string Name, string Text, Action<GameObject> Build)[]
	{
		("Cube", "RenderType On\nthe plain case", st => Cube( st, "Caster cube", V( 0, 1, 0 ) )),
		("Shadows only", "RenderType ShadowsOnly\na shadow with nothing over it", st => Cube( st, "Caster shadows only", V( 0, 1, 0 ), render: ModelRenderer.ShadowRenderType.ShadowsOnly )),
		("No shadow", "RenderType Off\na cube that casts nothing", st => Cube( st, "Caster off", V( 0, 1, 0 ), render: ModelRenderer.ShadowRenderType.Off )),
		("Sphere", "self-shadowing\nthe terminator", st => Cube( st, "Caster sphere", V( 0, 1, 0 ), V( 1, 1, 1 ), model: SPHERE )),
		("Leaf cutout", "a masked leaf slab\nthe shadow should be leaf-shaped", st => Cube( st, "Caster leaf", V( 0, 1.2f, 0 ), V( 1.4f, 1.4f, 0.02f ), material: CUT_LEAF )),
		("Ring cutout", "a masked ring, cutoff 0.5", st => Cube( st, "Caster ring", V( 0, 1.2f, 0 ), V( 1.4f, 1.4f, 0.02f ), material: CUT_RING )),
		("Translucent", "Translucent at alpha 0.5\ndoes it cast, and how dark", st => Cube( st, "Caster trans", V( 0, 1.2f, 0 ), V( 1.4f, 1.4f, 0.02f ), material: TRANS )),
		("Glass", "the project's glass", st => Cube( st, "Caster glass", V( 0, 1.2f, 0 ), V( 1.4f, 1.4f, 0.02f ), material: GLASS )),
		("One-sided away", "a plane facing away from the sun\ndoes its back cast", st => Cube( st, "Caster plane away", V( 0, 1.2f, 0 ), V( 1.4f, 1.4f, 1 ), rot: UPRIGHT, material: ONE_SIDED, model: PLANE )),
		("Two-sided", "the same plane, two-sided", st => Cube( st, "Caster plane two", V( 0, 1.2f, 0 ), V( 1.4f, 1.4f, 1 ), rot: UPRIGHT, material: TWO_SIDED, model: PLANE )),
		("Grazing", "a slab tilted 80 degrees to the sun\nacne or peter-panning shows here", st => Cube( st, "Caster grazing", V( 0, 0.5f, 0 ), V( 1.6f, 0.05f, 1.6f ), rot: Gallery.PitchYaw( -20, 0 ) )),
		("Contact", "a small cube on a big one\nthe join should be dark", st => { Cube( st, "Caster big", V( 0, 0.6f, 0 ), V( 1.2f, 0.8f, 1.2f ) ); Cube( st, "Caster small", V( 0, 1.15f, 0 ), V( 0.3f, 0.3f, 0.3f ) ); }),
		("High", "a cube 6 m up\nits shadow is far from it", st => Cube( st, "Caster high", V( 0, 6, 0 ), V( 0.8f, 0.8f, 0.8f ) )),
		("Thin", "a 2 cm rod\nit should keep a shadow at distance", st => Cube( st, "Caster rod", V( 0, 1.5f, 0 ), V( 0.02f, 3, 0.02f ) )),
		("Sprite", "a sprite with Shadows on", st =>
		{
			var go = S.Go( st, "Caster sprite", V( 0, 1.3f, 0 ) );
			var sprite = S.Comp<SpriteRenderer>( go, "sprite/caster" );
			sprite.Sprite = ResourceLibrary.Get<Sprite>( "sprites/ring.sprite" );
			sprite.StartingAnimationName = "Default";
			sprite.Size = new Vector2( 1.4f, 1.4f );
			sprite.Shadows = true;
		}),
		("Line", "a LineRenderer with CastShadows", st =>
		{
			// VectorPoints are world-space: the line is laid across the station where it stands.
			var p = st.WorldPosition;
			var go = S.Go( st, "Caster line" );
			var line = S.Comp<LineRenderer>( go, "line/caster" );
			line.UseVectorPoints = true;
			line.VectorPoints = new List<Vector3> { V( p.x - 0.8f, 1.6f, p.z ), V( p.x + 0.8f, 1.6f, p.z ) };
			line.Color = Color.White;
			line.Width = 0.25f;
			line.CastShadows = true;
			line.Lighting = true;
		}),
		("Model", "the urn, a real model", st => Cube( st, "Caster urn", V( 0, 0.2f, 0 ), V( 0.5f, 0.5f, 0.5f ), model: URN )),
	};

	{
		var rowZ = z - 130;
		var width = Gallery.RowWidth( casters.Length, 3.4f );
		var area = S.Area( areas, "Casters", "every kind of thing that can cast a shadow, and two that should not", rowZ, width, slabMaterial: null );
		var stations = Gallery.Row( casters, 3.4f, rowZ, "Caster", item => item.Name, ( item, name, pos ) =>
		{
			var st = Station( area, name, item.Text, pos );
			item.Build( st );
			return st;
		} );
		Gallery.StaggerSigns( stations );
		z -= 130 + ROW_DEPTH;
	}

	// -- source radius: coloured point lights with their own penumbrae --------------
	var radii = new (string Name, float R)[] { ("0", 0), ("0.05", 0.05f), ("0.3", 0.3f), ("1", 1), ("3", 3) };
	{
		var width = Gallery.RowWidth( radii.Length, 6 );
		var area = S.Area( areas, "Source Radius", "five point lights under a roof, the same but for the size of the source: the penumbra widens", z, width, wall: false, slabMaterial: null, slabTint: DARK );
		var stations = Gallery.Row( radii, 6, z, "Radius", item => item.Name, ( item, name, pos ) =>
		{
			var st = Station( area, name, $"point light, SourceRadius {item.R}\nthe edge of the shadow on the backdrop", pos, signY: 3.8f );
			Cube( st, $"{name} pillar", V( 0, 1.2f, 0 ), V( 0.3f, 2.4f, 0.3f ) );
			Cube( st, $"{name} backdrop", V( 0, 1.5f, -2.4f ), V( 5, 3, 0.2f ), tint: GREY );
			PointLight( st, name, V( 0, 2.5f, 2.5f ), Gallery.C( "1,0.9,0.8,1" ), brightness: 8, radius: 9, source: item.R );
			return st;
		} );
		Roof( area, "radius", z, width );
		Gallery.StaggerSigns( stations );
		z -= ROW_DEPTH;
	}

	// -- point and spot lights -----------------------------------------------------------
	void Cage( GameObject st, string name )
	{
		for ( var i = 0; i < 8; i++ )
		{
			var a = i / 8f * MathF.Tau;
			Cube( st, $"{name} bar {i}", V( MathF.Cos( a ) * 1.6f, 1.2f, MathF.Sin( a ) * 1.6f ), V( 0.15f, 2.4f, 0.15f ) );
		}
	}

	void Pillar( GameObject st, string name, Vector3 pos ) => Cube( st, name, pos, V( 0.4f, 1.6f, 0.4f ) );
	void SpotWall( GameObject st, string wall, string pillar ) { Cube( st, wall, V( 0, 1.5f, -2.5f ), V( 4, 3, 0.2f ), tint: GREY ); Cube( st, pillar, V( 0, 0.8f, -0.5f ), V( 0.3f, 1.6f, 0.3f ) ); }
	var down = Gallery.PitchYaw( -90, 0 );

	var lights = new (string Name, string Text, Action<GameObject> Build)[]
	{
		("Point in a cage", "a point light in eight bars\nshadows every way", st => { Cage( st, "Cage" ); PointLight( st, "Cage", V( 0, 1.2f, 0 ), brightness: 6, radius: 7 ); }),
		("Point no shadow", "the same, Shadows off", st => { Cage( st, "Cage off" ); PointLight( st, "Cage off", V( 0, 1.2f, 0 ), brightness: 6, radius: 7, shadows: false ); }),
		("Point radius 2", "Radius 2, cut off short", st => { Cage( st, "Cage short" ); PointLight( st, "Cage short", V( 0, 1.2f, 0 ), brightness: 8, radius: 2 ); }),
		("Four colours", "red, green, blue, yellow round one pillar\nfour coloured shadows", st =>
		{
			Cube( st, "Four pillar", V( 0, 1.2f, 0 ), V( 0.3f, 2.4f, 0.3f ) );
			PointLight( st, "Four R", V( 2, 1.5f, 0 ), Gallery.C( "1,0.2,0.2,1" ), 6, 7 );
			PointLight( st, "Four G", V( -2, 1.5f, 0 ), Gallery.C( "0.2,1,0.2,1" ), 6, 7 );
			PointLight( st, "Four B", V( 0, 1.5f, 2 ), Gallery.C( "0.3,0.4,1,1" ), 6, 7 );
			PointLight( st, "Four Y", V( 0, 1.5f, -2 ), Gallery.C( "1,0.9,0.2,1" ), 6, 7 );
		}),
		("Spot down", "a spot straight down, 35 degrees", st => { Pillar( st, "Spot pillar", V( 0, 0.8f, 0 ) ); SpotLight( st, "Spot down", V( 0, 4.5f, 0 ), down, brightness: 12 ); }),
		("Spot narrow", "ConeOuter 12, ConeInner 4", st => { Pillar( st, "Spot narrow pillar", V( 0, 0.8f, 0 ) ); SpotLight( st, "Spot narrow", V( 0, 4.5f, 0 ), down, brightness: 12, outer: 12, inner: 4 ); }),
		("Spot wide", "ConeOuter 70, ConeInner 60", st => { Pillar( st, "Spot wide pillar", V( 0, 0.8f, 0 ) ); SpotLight( st, "Spot wide", V( 0, 4.5f, 0 ), down, brightness: 12, outer: 70, inner: 60 ); }),
		("Spot cookie", "a ring cookie on the spot", st => { Pillar( st, "Spot cookie pillar", V( 0, 0.8f, 0 ) ); SpotLight( st, "Spot cookie", V( 0, 4.5f, 0 ), down, brightness: 12, cookie: "textures/fx/ring.png" ); }),
		("Spot sideways", "a spot along the floor onto a wall", st => { SpotWall( st, "Spot wall", "Spot side pillar" ); SpotLight( st, "Spot side", V( 0, 1.2f, 2.5f ), Rotation.Identity, brightness: 12, outer: 40, inner: 30 ); }),
		("Spot no shadow", "the same, Shadows off", st => { SpotWall( st, "Spot off wall", "Spot off pillar" ); SpotLight( st, "Spot off", V( 0, 1.2f, 2.5f ), Rotation.Identity, brightness: 12, outer: 40, inner: 30, shadows: false ); }),
	};

	{
		var width = Gallery.RowWidth( lights.Length, 6 );
		var area = S.Area( areas, "Point and Spot", "lights with their own shadow maps: cages, colours, cones, a cookie, and the same without shadows", z, width, wall: false, slabMaterial: null, slabTint: DARK );
		var stations = Gallery.Row( lights, 6, z, "Light", item => item.Name, ( item, name, pos ) =>
		{
			var st = Station( area, name, item.Text, pos, signY: 3.8f );
			item.Build( st );
			return st;
		} );
		Roof( area, "lights", z, width );
		Gallery.StaggerSigns( stations );
		z -= ROW_DEPTH;
	}

	// -- moving --------------------------------------------------------------------------
	var moving = new (string Name, string Text, Action<GameObject> Build)[]
	{
		("Propeller", "a cross on a Spinner\nthe shadow turns with it", st =>
		{
			var prop = S.Go( st, "Propeller", V( 0, 1.8f, 0 ) );
			Spin( prop, "propeller", V( 0, 0, 1 ), 60 );
			Cube( prop, "Blade A", V( 0, 0, 0 ), V( 2.4f, 0.2f, 0.1f ) );
			Cube( prop, "Blade B", V( 0, 0, 0 ), V( 0.2f, 2.4f, 0.1f ) );
		}),
		("Bobbing", "a cube on an Oscillator\nup and down 1.5 m", st => Oscillate( Cube( st, "Bob", V( 0, 1.5f, 0 ) ), "bob", V( 0, 1, 0 ), 1.5f, 0.4f )),
		("Sliding", "a cube sliding sideways", st => Oscillate( Cube( st, "Slide", V( 0, 0.6f, 0 ) ), "slide", V( 1, 0, 0 ), 1.5f, 0.3f )),
		("Turning spot", "a spot light on a Spinner", st =>
		{
			Cube( st, "Turn pillar A", V( 1.5f, 0.8f, 0 ), V( 0.3f, 1.6f, 0.3f ) );
			Cube( st, "Turn pillar B", V( -1.5f, 0.8f, 0 ), V( 0.3f, 1.6f, 0.3f ) );
			Cube( st, "Turn pillar C", V( 0, 0.8f, 1.5f ), V( 0.3f, 1.6f, 0.3f ) );
			Cube( st, "Turn pillar D", V( 0, 0.8f, -1.5f ), V( 0.3f, 1.6f, 0.3f ) );
			var turner = S.Go( st, "Spot turner", V( 0, 3, 0 ) );
			Spin( turner, "spot turner", V( 0, 1, 0 ), 30 );
			SpotLight( turner, "Turning", V( 0, 0, 0 ), Gallery.PitchYaw( -45, 0 ), brightness: 12, outer: 30, inner: 20 );
		}),
		("Orbiting point", "a point light on an Orbit round a pillar", st =>
		{
			Cube( st, "Orbit pillar", V( 0, 1.2f, 0 ), V( 0.3f, 2.4f, 0.3f ) );
			var centre = S.Go( st, "Orbit centre", V( 0, 1.5f, 0 ) );
			var light = PointLight( st, "Orbiting", V( 2, 1.5f, 0 ), Gallery.C( "1,0.8,0.5,1" ), 6, 7 );
			OrbitRound( light, "orbiting light", centre, 2, 5 );
		}),
		("Walking caster", "a cube orbiting in a point light", st =>
		{
			PointLight( st, "Walk light", V( 0, 3, 0 ), WHITE, 6, 8 );
			var centre = S.Go( st, "Walk centre", V( 0, 0.6f, 0 ) );
			OrbitRound( Cube( st, "Walker", V( 2, 0.6f, 0 ), V( 0.6f, 0.6f, 0.6f ) ), "walker", centre, 2, 6 );
		}),
	};

	{
		var width = Gallery.RowWidth( moving.Length, 6 );
		var area = S.Area( areas, "Moving", "casters that turn, bob and slide; a spot that turns; a point that orbits; a caster that orbits a light", z, width, wall: false, slabMaterial: null, slabTint: DARK );
		var stations = Gallery.Row( moving, 6, z, "Moving", item => item.Name, ( item, name, pos ) =>
		{
			var st = Station( area, name, item.Text, pos, signY: 3.8f );
			item.Build( st );
			return st;
		} );
		Roof( area, "moving", z, width );
		Gallery.StaggerSigns( stations );
		z -= ROW_DEPTH;
	}

	// -- receivers -----------------------------------------------------------------------
	var receivers = new (string Name, string Text, string Material)[]
	{
		("Rough", "the shadow on a rough pale slab", "materials/gallery/grid/r4_m0.mat"),
		("Chrome", "on chrome\na shadow on a mirror", "materials/gallery/surface/chrome.mat"),
		("Metal", "on brushed metal", "materials/gallery/surface/brushed.mat"),
		("Normal map", "on the bumps normal map", "materials/gallery/maps/normal.mat"),
		("Emissive", "on an emissive slab\nemission should not darken", "materials/gallery/emission/strength_2.mat"),
		("Translucent", "on a translucent slab", "materials/gallery/blend/trans_05.mat"),
		("Unlit", "on an unlit slab\nno shadow can land", "materials/gallery/shaders/unlit.mat"),
		("Dark", "on a nearly black slab", "materials/gallery/tint/dark.mat"),
	};

	{
		var width = Gallery.RowWidth( receivers.Length, 4 );
		var area = S.Area( areas, "Receivers", "the same cube's shadow on eight surfaces", z, width, wall: false );
		var stations = Gallery.Row( receivers, 4, z, "Receiver", item => item.Name, ( item, name, pos ) =>
		{
			var st = Station( area, name, item.Text, pos, pedestal: false );
			Cube( st, $"{name} slab", V( 0, 0.25f, 0 ), V( 2.4f, 0.1f, 2.4f ), tint: WHITE, material: item.Material );
			Cube( st, $"{name} caster", V( 0, 1.3f, 0 ), V( 0.6f, 0.6f, 0.6f ) );
			return st;
		} );
		Gallery.StaggerSigns( stations );
		z -= ROW_DEPTH;
	}

	// -- a room with a window ---------------------------------------------------------------
	{
		var room = S.Go( areas, "Room", V( 0, 0, z ) );
		Cube( room, "Room floor", V( 0, 0.1f, 0 ), V( 8, 0.2f, 8 ), tint: FLOOR );
		Cube( room, "Room roof", V( 0, 3.9f, 0 ), V( 8, 0.2f, 8 ) );
		Cube( room, "Room back", V( 0, 2, -4 ), V( 8, 4, 0.2f ) );
		Cube( room, "Room right", V( 4, 2, 0 ), V( 0.2f, 4, 8 ) );
		// the left wall faces the sun and has a lattice window: a frame of bars with gaps
		Cube( room, "Room left low", V( -4, 0.6f, 0 ), V( 0.2f, 1.2f, 8 ) );
		Cube( room, "Room left high", V( -4, 3.5f, 0 ), V( 0.2f, 1, 8 ) );
		for ( var i = 0; i < 5; i++ )
			Cube( room, $"Room bar {i}", V( -4, 2, -3.2f + i * 1.6f ), V( 0.2f, 1.8f, 0.3f ) );
		Cube( room, "Room sill", V( -4, 2, 0 ), V( 0.2f, 0.15f, 8 ) );
		Cube( room, "Room table", V( 0, 0.6f, 0 ), V( 1.5f, 0.1f, 1 ) );
		Cube( room, "Room vase", V( 0, 1, 0 ), V( 0.3f, 0.3f, 0.3f ), model: URN );
		Sign( room, "Room", "a room open on the front\nthe sun comes through the lattice on the left\ninside is what the ambient light gives", V( 0, 5.2f, 0 ), scale: 0.5f );
	}

	S.Player( V( 0, 2.6f, 6 ) );
	var hud = S.Hud( "The sun's field first; walk past the gate to the casters, radii, lights, movers, receivers and the room. Keys 1-5 change the sun. Q returns." );
	S.Comp<ShadowRack>( hud, "hud/rack" ).DaySpeed = 6;

	objects = S.Scene.Directory.AllGameObjects.Count();
}

var wrote = S.Write( "rendering/shadows.scene" );
Gallery.RegisterInMenu( "rendering/shadows.scene", "Shadows", "Rendering",
	"The sun over a long field, every kind of caster, source radii, point and spot shadows, moving lights, receivers and a room; keys change the sun" );

return new { Wrote = wrote, Objects = objects };
