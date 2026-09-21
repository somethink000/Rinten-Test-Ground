// Writes scenes/rendering/jungle.scene: the jungle, laid out on the ground
// grow.py cut - a stream down the middle, a path beside it, and everything
// from the catalogue placed as an object of its own. Every thing stands on
// the ground at the ground's height, tilted to its slope where it should be,
// sunk into it where it should be; a vine hangs from a limb the tree really
// has, an arch runs from one trunk's bark to another's, a log lies along the
// slope it fell on.
//
// Positions are worked out in Blender's frame, the one grow.py thinks in (x, y
// along the ground, z up), and turned into the engine's (x, up, -y) on the
// way out. tools/jungle/ground.json is the ground's height grid and the lines
// of the stream and the path; tools/jungle/sockets.json is what grow.py wrote
// about each model - its box, and for a tree the frames of its trunk and
// limbs. Both are read here.
//
// Run with: python3 build.py jungle   (the editor must be open on Test Ground)
using System.IO;
using System.Text.Json;
using System.Text.Json.Nodes;

var S = new Gallery( "jungle", "Jungle",
	"A rainforest: a stream, a path, giants with buttresses and roots, stranglers, banyans, palms, bamboo, ferns and litter everywhere, dead wood, moss, and the fog that hides the rest." );

var tools = Path.GetFullPath( Path.Combine( Project.Current.GetAssetsPath(), "..", "tools", "jungle" ) );
var modelsDir = Path.Combine( Project.Current.GetAssetsPath(), "models", "jungle" );

// ---------------------------------------------------------------------------
// The ground: heights, slopes and the two lines through it
// ---------------------------------------------------------------------------

var ground = JsonNode.Parse( File.ReadAllText( Path.Combine( tools, "ground.json" ) ) ).AsObject();
int gn = ground["n"].GetValue<int>();
float gstep = ground["step"].GetValue<float>(), gsize = ground["size"].GetValue<float>();
var heights = new float[gn, gn];
{
	var rows = ground["heights"].AsArray();
	for ( var iy = 0; iy < gn; iy++ )
	{
		var row = rows[iy].AsArray();
		for ( var ix = 0; ix < gn; ix++ ) heights[iy, ix] = row[ix].GetValue<float>();
	}
}
var streamX = ground["stream_x"].AsArray().Select( v => v.GetValue<float>() ).ToArray();
var pathX = ground["path_x"].AsArray().Select( v => v.GetValue<float>() ).ToArray();

const float SCENE = 60;   // the square the walk is laid out on; the apron beyond it rises into the valley's sides
float APRON = gsize;

/// Bilinear height of the ground at Blender (x, y).
float Height( float x, float y )
{
	var fx = (x + gsize / 2) / gstep;
	var fy = (y + gsize / 2) / gstep;
	var ix = Math.Clamp( (int)MathF.Floor( fx ), 0, gn - 2 );
	var iy = Math.Clamp( (int)MathF.Floor( fy ), 0, gn - 2 );
	var tx = Math.Clamp( fx - ix, 0f, 1f );
	var ty = Math.Clamp( fy - iy, 0f, 1f );
	var a = heights[iy, ix] * (1 - tx) + heights[iy, ix + 1] * tx;
	var b = heights[iy + 1, ix] * (1 - tx) + heights[iy + 1, ix + 1] * tx;
	return a * (1 - ty) + b * ty;
}

/// The ground's normal at (x, y), Blender frame, unit length.
(float x, float y, float z) Normal( float x, float y )
{
	const float d = 0.4f;
	var dx = (Height( x + d, y ) - Height( x - d, y )) / (2 * d);
	var dy = (Height( x, y + d ) - Height( x, y - d )) / (2 * d);
	var L = MathF.Sqrt( dx * dx + dy * dy + 1 );
	return (-dx / L, -dy / L, 1 / L);
}

/// Degrees off level.
float Slope( float x, float y ) => MathF.Acos( Math.Clamp( Normal( x, y ).z, -1f, 1f ) ).RadianToDegree();

float LineAt( float[] xs, float y )
{
	var fy = (y + gsize / 2) / gstep;
	var iy = Math.Clamp( (int)MathF.Floor( fy ), 0, gn - 2 );
	var t = Math.Clamp( fy - iy, 0f, 1f );
	return xs[iy] * (1 - t) + xs[iy + 1] * t;
}

float Sx( float y ) => LineAt( streamX, y );
float Px( float y ) => LineAt( pathX, y );
bool OnPath( float x, float y, float margin = 0 ) => MathF.Abs( x - Px( y ) ) < 1.6f + margin;
bool InStream( float x, float y, float margin = 0 ) => MathF.Abs( x - Sx( y ) ) < 1.8f + margin;
bool Inside( float x, float y, float edge = 0.5f )
{
	var half = SCENE / 2 - edge;
	return -half < x && x < half && -half < y && y < half;
}

// ---------------------------------------------------------------------------
// Rotations: yaw about up, then the tilt that lays a thing on a slope
// ---------------------------------------------------------------------------

(float x, float y, float z, float w) QMul( (float x, float y, float z, float w) a, (float x, float y, float z, float w) b )
	=> (a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y,
		a.w * b.y - a.x * b.z + a.y * b.w + a.z * b.x,
		a.w * b.z + a.x * b.y - a.y * b.x + a.z * b.w,
		a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z);

(float x, float y, float z, float w) QYaw( float deg )
{
	var h = deg.DegreeToRadian() / 2;
	return (0, MathF.Sin( h ), 0, MathF.Cos( h ));
}

/// The rotation that takes the engine's up onto a normal.
(float x, float y, float z, float w) QTiltTo( float nx, float ny, float nz )
{
	var c = Math.Clamp( ny, -1f, 1f );
	if ( c > 0.99999f ) return (0, 0, 0, 1);
	// axis = up x n = (0,1,0) x (nx,ny,nz) = (nz, 0, -nx)
	float ax = nz, az = -nx;
	var L = MathF.Sqrt( ax * ax + az * az );
	if ( L == 0 ) L = 1;
	var ang = MathF.Acos( c );
	var s = MathF.Sin( ang / 2 );
	return (ax / L * s, 0, az / L * s, MathF.Cos( ang / 2 ));
}

/// Yaw, and `align` (0..1) of the ground's tilt at (x, y).
Rotation RotationAt( float turn, float x, float y, float align )
{
	var q = QYaw( turn );
	if ( align > 0 )
	{
		var nb = Normal( x, y );
		float ex = nb.x * align, ey = nb.z, ez = -nb.y * align;
		var L = MathF.Sqrt( ex * ex + ey * ey + ez * ez );
		q = QMul( QTiltTo( ex / L, ey / L, ez / L ), q );
	}
	return new Rotation( q.x, q.y, q.z, q.w );
}

// ---------------------------------------------------------------------------
// The dice: one seeded generator for the whole layout, so the same file comes
// out every time this runs. Its own rather than System.Random so the sequence
// is the same on every runtime.
// ---------------------------------------------------------------------------

ulong seed = 0x9E3779B97F4A7C15UL ^ 7;
float Rand()
{
	seed ^= seed << 13; seed ^= seed >> 7; seed ^= seed << 17;
	return (seed >> 40) / 16777216f;
}
float Uniform( float a, float b ) => a + (b - a) * Rand();
T Choice<T>( IReadOnlyList<T> items ) => items[Math.Min( (int)(Rand() * items.Count), items.Count - 1 )];
T Weighted<T>( IReadOnlyList<T> items, float[] weights )
{
	var r = Rand() * weights.Sum();
	for ( var i = 0; i < items.Count; i++ )
	{
		r -= weights[i];
		if ( r <= 0 ) return items[i];
	}
	return items[^1];
}
List<T> Sample<T>( IEnumerable<T> items, int k )
{
	var pool = items.ToList();
	var picked = new List<T>();
	while ( picked.Count < k && pool.Count > 0 )
	{
		var i = Math.Min( (int)(Rand() * pool.Count), pool.Count - 1 );
		picked.Add( pool[i] );
		pool.RemoveAt( i );
	}
	return picked;
}

// ---------------------------------------------------------------------------
// Sockets: what grow.py wrote about each model - its box, its trunk and limb frames
// ---------------------------------------------------------------------------

var sockets = JsonNode.Parse( File.ReadAllText( Path.Combine( tools, "sockets.json" ) ) ).AsObject();

float[] BoundsOf( string model )
{
	var b = sockets[model]?["bounds"]?.AsArray();
	return b is null ? new float[] { -0.5f, -0.5f, 0, 0.5f, 0.5f, 1 } : b.Select( v => v.GetValue<float>() ).ToArray();
}

/// A frame of a swept tube: where, which way, how thick, how far along.
List<float[]> Frames( JsonArray rows ) => rows.Select( r => r.AsArray().Select( v => v.GetValue<float>() ).ToArray() ).ToList();

// ---------------------------------------------------------------------------
// Collision in the .mdl files: a triangle mesh for what is walked on, a
// capsule up the trunk of a tree. Written only where the file differs.
// ---------------------------------------------------------------------------

string[] meshColliders = { "ground", "ground_apron", "log_a", "log_b", "logmossy_a", "logmossy_b", "logmossy_c", "uprooted_a", "uprooted_b",
	"rootmat_a", "rootmat_b", "stump_a", "stump_b", "stump_c", "broken_a", "broken_b",
	"rock_a", "rock_b", "rock_c", "rockflat_a", "rockflat_b", "rockflat_c", "rockflat_d", "rockslab_a",
	"boulder_a", "boulder_b", "rockmid_a", "rockmid_b", "rockmid_c", "rockbig_a", "rockbig_b", "rockbig_c",
	"cliff_a", "cliff_b", "streamstone_a", "streamstone_b", "streamstone_c", "rockstack_a", "rockstack_b" };

var trunkCapsules = new Dictionary<string, (float r, float h)>
{
	["tree_giant_a"] = (1.5f, 10), ["tree_giant_b"] = (1.8f, 9), ["tree_giant_c"] = (1.3f, 9), ["mossy_giant"] = (1.4f, 9),
	["tree_winding_a"] = (0.8f, 6), ["tree_winding_b"] = (0.7f, 5), ["tree_winding_c"] = (0.9f, 6),
	["tree_lean_a"] = (1.1f, 3), ["tree_lean_b"] = (0.9f, 3), ["tree_forked_a"] = (0.7f, 3), ["tree_forked_b"] = (0.8f, 3),
	["tree_tall_a"] = (0.35f, 12), ["tree_tall_b"] = (0.3f, 12), ["tree_tall_c"] = (0.4f, 10), ["tree_tall_d"] = (0.32f, 14),
	["strangler_a"] = (1.0f, 12), ["strangler_b"] = (0.9f, 10), ["banyan_a"] = (1.4f, 8), ["banyan_b"] = (1.1f, 7),
	["climbed_a"] = (0.5f, 9), ["climbed_b"] = (0.7f, 7), ["palm_a"] = (0.2f, 7), ["palm_b"] = (0.18f, 5), ["palm_c"] = (0.22f, 10),
	["palm_fan_a"] = (0.16f, 4), ["palm_fan_b"] = (0.14f, 2.5f), ["snag_a"] = (0.5f, 8), ["snag_b"] = (0.7f, 12), ["snag_c"] = (0.4f, 5),
	["treefern_a"] = (0.16f, 2.3f), ["treefern_b"] = (0.16f, 3.2f), ["cycad_a"] = (0.3f, 0.8f), ["cycad_b"] = (0.3f, 1.5f),
};

JsonObject Hull( string type ) => new()
{
	["__type"] = type, ["Name"] = "", ["Enabled"] = true, ["Bone"] = "", ["Surface"] = "", ["Tags"] = "", ["Folder"] = "",
};

int hullsWritten = 0;
void SetHulls( string model, JsonArray hulls )
{
	var path = Path.Combine( modelsDir, model + ".mdl" );
	var mdl = JsonNode.Parse( File.ReadAllText( path ) ).AsObject();
	if ( mdl["Hulls"] is JsonArray had && JsonNode.DeepEquals( had, hulls ) ) return;
	mdl["Hulls"] = hulls;
	File.WriteAllText( path, mdl.ToJsonString( new JsonSerializerOptions { WriteIndented = true } ) + "\n" );
	hullsWritten++;
}

foreach ( var model in meshColliders )
	SetHulls( model, new JsonArray( Hull( "RenderMesh" ) ) );
foreach ( var (model, (r, h)) in trunkCapsules )
{
	var capsule = Hull( "CapsuleHull" );
	capsule["PointA"] = "0,0,0";
	capsule["PointB"] = $"0,{h},0";
	capsule["Radius"] = r;
	SetHulls( model, new JsonArray( capsule ) );
}

// ---------------------------------------------------------------------------
// The layout
// ---------------------------------------------------------------------------

int objects;
using ( S.Scene.Push() )
{
	var world = S.Scene;

	var placed = new List<(float x, float y, float r)>();   // what takes room, so the scatter keeps clear
	var names = new HashSet<string>();
	var treePlace = new Dictionary<string, (float x, float y, float turn, float scale)>();
	var treeModel = new Dictionary<string, string>();

	/// A model at Blender (x, y). It stands at the ground's height there, less
	/// `sink` (a fraction of its own height buried) plus `lift` metres; `align`
	/// tilts it to the slope, one being flat against it. `collide` adds a
	/// ModelCollider - the model's .mdl must carry a hull for that to do
	/// anything. `clear` reserves a footprint the scatter keeps out of.
	GameObject Put( string model, float x, float y, float turn = 0, float scale = 1, float lift = 0, float sink = 0, float align = 0,
		bool onGround = true, bool collide = false, float clear = 0, string name = null )
	{
		var bb = BoundsOf( model );
		var tall = (bb[5] - bb[2]) * scale;
		var z = (onGround ? Height( x, y ) : 0) + lift - sink * tall;
		name ??= $"{model} @ {x:0.0},{y:0.0}";
		while ( !names.Add( name ) ) name += "'";
		var path = $"models/jungle/{model}.mdl";
		var go = S.Go( world, name, Gallery.V( x, z, -y ), RotationAt( turn, x, y, align ), new Vector3( scale ), "world" );
		S.Model( go, name, Color.White, null, path );
		if ( collide )
		{
			var c = S.Comp<ModelCollider>( go, "collider/" + name );
			c.Model = Rinten.Model.Load( path );
			c.Static = true;
		}
		if ( clear > 0 ) placed.Add( (x, y, clear) );
		return go;
	}

	bool Clear( float x, float y, float radius ) => placed.All( p => MathF.Sqrt( (x - p.x) * (x - p.x) + (y - p.y) * (y - p.y) ) > p.r + radius );

	/// Clear of the path, the stream and everything placed.
	bool Free( float x, float y, float radius, float pathMargin = 0, float streamMargin = 0 )
	{
		if ( !Inside( x, y, radius ) ) return false;
		if ( OnPath( x, y, pathMargin + radius * 0.5f ) || InStream( x, y, streamMargin + radius * 0.5f ) ) return false;
		return Clear( x, y, radius );
	}

	/// How far the nearest big trunk is - the shade a plant stands in.
	float NearestTree( float x, float y )
	{
		var best = 99f;
		foreach ( var (_, p) in treePlace )
			best = MathF.Min( best, MathF.Sqrt( (x - p.x) * (x - p.x) + (y - p.y) * (y - p.y) ) );
		return best;
	}

	/// `count` models dropped where Free says, `prefer(x, y)` (0..1) thinning
	/// the ones the dice put where they do not belong.
	void Scatter( string[] models, int count, float radius, int tries = 60, float scaleLo = 0.85f, float scaleHi = 1.15f, bool collide = false,
		float clear = -1, float sink = 0, float align = 0, float pathMargin = 0, float streamMargin = 0, Func<float, float, float> prefer = null,
		float[] weights = null, float maxSlope = 45, bool allowPath = false, bool allowStream = false )
	{
		for ( var n = 0; n < count; n++ )
		{
			for ( var t = 0; t < tries; t++ )
			{
				float x = Uniform( -29.5f, 29.5f ), y = Uniform( -29.5f, 29.5f );
				if ( !Inside( x, y, radius ) ) continue;
				if ( !allowPath && OnPath( x, y, pathMargin + radius * 0.5f ) ) continue;
				if ( !allowStream && InStream( x, y, streamMargin + radius * 0.5f ) ) continue;
				if ( !Clear( x, y, radius ) ) continue;
				if ( Slope( x, y ) > maxSlope ) continue;
				if ( prefer is not null && Rand() > prefer( x, y ) ) continue;
				var m = weights is null ? Choice( models ) : Weighted( models, weights );
				Put( m, x, y, Uniform( 0, 360 ), Uniform( scaleLo, scaleHi ), sink: sink, align: align, collide: collide, clear: clear < 0 ? radius : clear );
				break;
			}
		}
	}

	// -- sockets: where on a placed tree a thing can hang ---------------------

	/// A point in a placed tree's own (Blender) frame into the scene's Blender frame.
	(float x, float y, float z) ToWorld( string tree, float lx, float ly, float lz )
	{
		var (x, y, turn, scale) = treePlace[tree];
		float c = MathF.Cos( turn.DegreeToRadian() ), s = MathF.Sin( turn.DegreeToRadian() );
		lx *= scale; ly *= scale; lz *= scale;
		return (x + lx * c - ly * s, y + lx * s + ly * c, Height( x, y ) + lz);
	}

	/// Points on a placed tree's limbs, high enough and thick enough, with the
	/// world point on the limb's underside and the limb's radius.
	List<((float x, float y, float z) p, float r)> LimbPoints( string tree, float minZ = 4, float minR = 0 )
	{
		var found = new List<((float x, float y, float z) p, float r)>();
		var limbs = sockets[treeModel[tree]]?["limbs"]?.AsArray();
		if ( limbs is null ) return found;
		foreach ( var limb in limbs )
		{
			var frames = Frames( limb.AsArray() );
			for ( var i = 1; i < frames.Count - 1; i++ )
			{
				var fr = frames[i];
				if ( fr[2] < minZ || fr[6] < minR ) continue;
				var w = ToWorld( tree, fr[0], fr[1], fr[2] );
				found.Add( ((w.x, w.y, w.z - fr[6] * treePlace[tree].scale), fr[6]) );
			}
		}
		return found;
	}

	/// The trunk's centre and radius at about height z (the tree's own frame), in the world.
	((float x, float y, float z) p, float r) TrunkPoint( string tree, float z )
	{
		var trunk = sockets[treeModel[tree]]?["trunk"]?.AsArray();
		if ( trunk is null || trunk.Count == 0 )
		{
			var (x, y, _, _) = treePlace[tree];
			return ((x, y, Height( x, y ) + z), 0.5f);
		}
		var best = Frames( trunk ).MinBy( fr => MathF.Abs( fr[2] - z ) );
		return (ToWorld( tree, best[0], best[1], best[2] ), best[6] * treePlace[tree].scale);
	}

	GameObject Tree( string model, float x, float y, float turn, float clear, float scale = 1, string name = null )
	{
		name ??= model;
		var o = Put( model, x, y, turn, scale, collide: true, clear: clear, name: name );
		treePlace[name] = (x, y, turn, scale);
		treeModel[name] = model;
		return o;
	}

	Put( "ground", 0, 0, onGround: false, collide: true, name: "Ground" );
	Put( "ground_apron", 0, 0, onGround: false, collide: true, name: "Ground apron" );
	Put( "water", 0, 0, onGround: false, name: "Stream" );

	// -- the big trees, by hand: the composition the references have ----------
	Tree( "tree_lean_a", Px( -8 ) - 3.5f, -8, 15, 2.5f );           // the trunk over the path
	Tree( "tree_giant_b", Px( -2 ) + 9, -2, 40, 4 );
	Tree( "mossy_giant", Px( 8 ) - 12, 8, 200, 4 );
	Tree( "tree_giant_a", Sx( 16 ) - 9, 16, 110, 4 );
	Tree( "tree_giant_c", Px( -27 ) + 9, -27, 300, 3.5f );
	Tree( "banyan_a", Px( 20 ) + 13, 20, 70, 6 );
	Tree( "banyan_b", Px( -24 ) + 12, -24, 250, 5 );
	Tree( "strangler_a", Px( -16 ) - 8, -16, 0, 2.5f );
	Tree( "strangler_b", Sx( 4 ) - 14, 4, 130, 2.5f );
	Tree( "tree_winding_a", Px( 2 ) + 5, 2, 170, 2.5f );
	Tree( "tree_winding_b", Sx( -12 ) - 6, -12, 20, 2.5f );
	Tree( "tree_winding_c", Px( 26 ) - 6, 26, 95, 2.5f );
	Tree( "tree_lean_b", Sx( 24 ) - 5, 24, 60, 2.5f );
	Tree( "tree_forked_a", Px( 14 ) + 6, 14, 210, 2 );
	Tree( "tree_forked_b", Sx( -22 ) - 9, -22, 340, 2 );
	Tree( "climbed_a", Px( -12 ) + 7, -12, 0, 2 );
	Tree( "climbed_b", Sx( 12 ) - 4, 12, 45, 2 );

	// -- the picket behind: tall trunks that go into the fog ------------------
	string[] tallKinds = { "tree_tall_a", "tree_tall_b", "tree_tall_c", "tree_tall_d" };
	for ( var i = 0; i < 34; i++ )
	{
		for ( var t = 0; t < 80; t++ )
		{
			float x = Uniform( -29, 29 ), y = Uniform( -29, 29 );
			if ( Free( x, y, 2.2f, 1.5f, 1.0f ) && Slope( x, y ) < 30 )
			{
				var m = Choice( tallKinds );
				Tree( m, x, y, Uniform( 0, 360 ), 2.2f, Uniform( 0.85f, 1.15f ), $"{m} #{i}" );
				break;
			}
		}
	}

	// -- the wall of forest on the valley's sides, beyond the walk: what the
	// fog shows as silhouettes and what fills the horizon ---------------------
	var wall = new List<(float x, float y, float r)>();
	string[] big = { "tree_giant_a", "tree_giant_b", "tree_giant_c", "banyan_a", "strangler_a", "mossy_giant" };
	string[] wallKinds = { "tree_tall_a", "tree_tall_b", "tree_tall_c", "tree_tall_d", "tree_tall_b", "palm_c", "tree_arch_a" };
	for ( var i = 0; i < 150; i++ )
	{
		for ( var t = 0; t < 60; t++ )
		{
			float x = Uniform( -APRON / 2 + 6, APRON / 2 - 6 ), y = Uniform( -APRON / 2 + 6, APRON / 2 - 6 );
			var d = MathF.Max( MathF.Abs( x ), MathF.Abs( y ) );
			if ( d < SCENE / 2 + 1.5f || (x < 0 && y > 0 && Rand() < 0.5f) ) continue;
			var r = d < 42 ? 3f : 5f;
			if ( !wall.All( w => MathF.Sqrt( (x - w.x) * (x - w.x) + (y - w.y) * (y - w.y) ) > r ) ) continue;
			var m = d < 45 && Rand() < 0.3f ? Choice( big ) : Choice( wallKinds );
			wall.Add( (x, y, r) );
			Put( m, x, y, Uniform( 0, 360 ), Uniform( 0.9f, 1.3f ), name: $"wall {m} #{i}" );
			break;
		}
	}
	string[] wallUnder = { "bush_a", "bush_b", "fern_a", "fern_c", "broadleaf_a", "palm_fan_a", "treefern_a", "banana_b", "elephant_a" };
	for ( var i = 0; i < 90; i++ )
	{
		for ( var t = 0; t < 40; t++ )
		{
			float x = Uniform( -APRON / 2 + 4, APRON / 2 - 4 ), y = Uniform( -APRON / 2 + 4, APRON / 2 - 4 );
			if ( MathF.Max( MathF.Abs( x ), MathF.Abs( y ) ) < SCENE / 2 + 1 ) continue;
			var m = Choice( wallUnder );
			Put( m, x, y, Uniform( 0, 360 ), Uniform( 1.2f, 2.2f ), sink: 0.03f, align: 0.5f, name: $"wall {m} #{i}" );
			break;
		}
	}

	// -- palms, tree ferns, bamboo, the odd ones, by hand near the walk -------
	Tree( "palm_a", Px( -12 ) + 4, -12, 30, 1.5f );
	Tree( "palm_c", Sx( -5 ) - 5, -5, 200, 1.5f );
	Tree( "palm_b", Px( 12 ) + 4, 12, 110, 1.5f );
	Tree( "palm_fan_a", Px( 4 ) - 5, 4, 0, 1.5f );
	Tree( "palm_fan_b", Sx( -14 ) + 4, -14, 80, 1.2f );
	Tree( "treefern_a", Sx( -8 ) + 3.5f, -8, 0, 1.2f );
	Tree( "treefern_b", Sx( 6 ) + 3.5f, 6, 140, 1.2f );
	Put( "bambooclump_a", Px( -18 ) + 4, -18, 0, clear: 1.5f, sink: 0.01f );
	Put( "bambooclump_b", Px( -26 ) - 4, -26, 60, clear: 1.8f, sink: 0.01f );
	Put( "bambooclump_a", Px( -20 ) - 4.5f, -20, 200, 0.9f, clear: 1.5f, sink: 0.01f );
	Put( "bamboo_b", Px( -15 ) - 3.5f, -15, 0, clear: 0.5f, sink: 0.01f );
	Put( "bamboo_c", Px( -22 ) + 3.5f, -22, 90, clear: 0.5f, sink: 0.01f );
	Put( "stilt_a", Sx( 10 ) + 4, 10, 0, clear: 1.5f, sink: 0.02f );
	Put( "stilt_b", Sx( -20 ) - 4, -20, 120, clear: 1.5f, sink: 0.02f );
	Put( "stilt_c", Px( 28 ) + 6, 28, 0, clear: 1.5f, sink: 0.02f );
	Put( "cycad_a", Px( 0 ) - 4, 0, 40, clear: 1, sink: 0.03f, align: 0.5f );
	Put( "cycad_b", Px( 24 ) + 5, 24, 0, clear: 1.2f, sink: 0.03f, align: 0.5f );
	Put( "banana_a", Px( 14 ) - 5, 14, 0, clear: 1.5f, sink: 0.02f );
	Put( "banana_b", Sx( 22 ) + 5, 22, 180, clear: 1.8f, sink: 0.02f );
	Put( "reeds_a", Sx( -16 ) + 2.6f, -16, clear: 0.5f, sink: 0.03f, align: 0.6f );
	Put( "reeds_b", Sx( 2 ) - 2.6f, 2, 50, clear: 0.5f, sink: 0.03f, align: 0.6f );
	Put( "reeds_a", Sx( 20 ) + 2.6f, 20, 120, clear: 0.5f, sink: 0.03f, align: 0.6f );

	// -- the bamboo grove: the path's southern reach runs through a stand of
	// culms, thick on both sides, thinning out to the north -------------------
	string[] culms = { "bamboo_a", "bamboo_b", "bamboo_c", "bamboo_a", "bamboo_b" };
	for ( var i = 0; i < 70; i++ )
	{
		for ( var t = 0; t < 40; t++ )
		{
			var y = Uniform( -28.5f, -13 );
			var side = Rand() < 0.5f ? -1 : 1;
			var x = Px( y ) + side * Uniform( 1.9f, 7.5f );
			// thick at the south end, thinning north
			if ( Rand() > 1 - (y + 13) / -15.5f * 0.6f ) continue;
			if ( !Free( x, y, 0.35f, 0.2f, 0.5f ) ) continue;
			var m = Choice( culms );
			Put( m, x, y, Uniform( 0, 360 ), Uniform( 0.8f, 1.25f ), sink: 0.01f, clear: 0.3f, name: $"grove {m} #{i}" );
			break;
		}
	}
	string[] clumps = { "bambooclump_a", "bambooclump_b" };
	for ( var i = 0; i < 4; i++ )
	{
		for ( var t = 0; t < 30; t++ )
		{
			var y = Uniform( -27, -16 );
			var x = Px( y ) + (Rand() < 0.5f ? -1 : 1) * Uniform( 3, 6.5f );
			if ( Free( x, y, 1.4f, 0.5f, 0.5f ) )
			{
				Put( Choice( clumps ), x, y, Uniform( 0, 360 ), Uniform( 0.85f, 1.1f ), sink: 0.01f, clear: 1.4f, name: $"grove clump #{i}" );
				break;
			}
		}
	}

	// more palms and tree ferns, scattered where the walk can see them
	Scatter( new[] { "palm_a", "palm_b", "palm_fan_a", "palm_fan_b", "treefern_a", "treefern_b", "cycad_b", "banana_a" }, 14, 1.5f,
		collide: true, sink: 0.02f, pathMargin: 1, streamMargin: 0.5f, maxSlope: 30 );
	Scatter( new[] { "tree_thin_a", "tree_thin_b", "tree_arch_a", "tree_arch_b" }, 26, 1, sink: 0.02f, pathMargin: 1, streamMargin: 0.5f, maxSlope: 35 );

	// -- dead wood: logs lie along the slope, sunk a little; stumps and snags stand
	Put( "logmossy_a", Px( 6 ) + 2, 6, 70, collide: true, clear: 1.5f, sink: 0.12f, align: 1 );
	Put( "logmossy_b", Sx( -2 ) + 6, -2, 20, collide: true, clear: 2, sink: 0.12f, align: 1 );
	Put( "log_a", Px( -28 ) + 6, -28, 150, collide: true, clear: 1.5f, sink: 0.12f, align: 1 );
	Put( "log_b", Sx( 28 ) - 7, 28, 100, collide: true, clear: 2, sink: 0.12f, align: 1 );
	Put( "logmossy_c", Px( 18 ) - 4, 18, 10, collide: true, clear: 1, sink: 0.15f, align: 1 );
	Put( "uprooted_a", Sx( 28 ) - 4, 28, 30, collide: true, clear: 3, sink: 0.05f, align: 0.6f );
	Put( "uprooted_b", Px( -30 ) + 10, -29, 200, collide: true, clear: 2.5f, sink: 0.05f, align: 0.6f );
	Tree( "snag_a", Px( 18 ) - 7, 18, 0, 1.2f );
	Tree( "snag_b", Sx( -10 ) - 8, -10, 90, 1.5f );
	Tree( "snag_c", Px( -4 ) + 7, -4, 200, 1 );
	Put( "stump_a", Px( 10 ) - 3.5f, 10, 0, collide: true, clear: 1, sink: 0.06f, align: 0.7f );
	Put( "stump_b", Sx( -24 ) + 5, -24, 90, collide: true, clear: 1.2f, sink: 0.06f, align: 0.7f );
	Put( "stump_c", Px( -8 ) + 4, -8, 180, collide: true, clear: 0.8f, sink: 0.06f, align: 0.7f );
	Put( "broken_a", Px( 26 ) - 9, 26, 250, collide: true, clear: 2, sink: 0.03f );
	Put( "broken_b", Sx( -28 ) - 6, -28, 30, collide: true, clear: 2, sink: 0.03f );
	Put( "rootmat_a", treePlace["mossy_giant"].x, treePlace["mossy_giant"].y, 20, collide: true, sink: 0.15f, align: 1 );
	Put( "rootmat_b", treePlace["tree_giant_a"].x, treePlace["tree_giant_a"].y, 70, collide: true, sink: 0.15f, align: 1 );
	Put( "vinetangle_b", Px( 10 ) - 4.5f, 10.8f, sink: 0.05f, align: 1 );
	Scatter( new[] { "debris_a", "debris_b", "debris_c" }, 30, 0.8f, sink: 0.25f, align: 1, pathMargin: 0.5f );
	Scatter( new[] { "fallenfrond_a", "fallenfrond_b" }, 14, 0.6f, sink: 0, align: 1, allowPath: true );

	// -- the stream: stones in the bed, sunk and tilted with it; boulders on the banks
	string[] bed = { "streamstone_a", "streamstone_b", "streamstone_c", "rockflat_a", "rockflat_b", "rockflat_d", "rock_b", "streamstone_b" };
	string[] bank = { "boulder_a", "boulder_b", "rockbig_a", "rockmid_a", "rockmid_b", "rockmid_c", "rockstack_a", "rockflat_c", "rockslab_a" };
	{
		var y = -29f;
		var i = 0;
		while ( y < 29 )
		{
			var x = Sx( y ) + Uniform( -1.3f, 1.3f );
			Put( bed[i % bed.Length], x, y, Uniform( 0, 360 ), Uniform( 0.7f, 1.2f ), sink: 0.3f, align: 1, collide: true, clear: 0.8f );
			if ( i % 3 != 2 )
			{
				var x2 = Sx( y ) + Uniform( -1.5f, 1.5f );
				Put( "streamstone_a", x2, y + 1.2f, Uniform( 0, 360 ), Uniform( 0.5f, 0.9f ), sink: 0.35f, align: 1, clear: 0.4f );
			}
			if ( i % 2 == 0 )
			{
				var side = i % 4 == 0 ? 1 : -1;
				float bx = Sx( y ) + side * Uniform( 2.6f, 4 ), by = y + Uniform( -1, 1 );
				Put( bank[(i / 2) % bank.Length], bx, by, Uniform( 0, 360 ), sink: 0.25f, align: 0.9f, collide: true, clear: 1.5f );
			}
			y += Uniform( 2, 3.2f );
			i++;
		}
	}
	Put( "cliff_a", -26, 10, 20, collide: true, clear: 5, sink: 0.2f, align: 0.5f );
	Put( "cliff_b", 27, -14, 110, collide: true, clear: 6, sink: 0.2f, align: 0.5f );
	Put( "rockbig_b", -22, -6, 60, collide: true, clear: 3, sink: 0.25f, align: 0.8f );
	Put( "rockbig_c", 24, 6, 300, collide: true, clear: 3.5f, sink: 0.25f, align: 0.8f );
	Put( "rockstack_b", Px( -6 ) + 10, -6, 0, collide: true, clear: 1.5f, sink: 0.1f, align: 0.8f );
	Scatter( new[] { "rock_a", "rock_b", "rockmid_a", "rockflat_a" }, 24, 0.8f, sink: 0.3f, align: 1, collide: true, pathMargin: 0.3f,
		weights: new[] { 3f, 2, 1, 1 } );
	Scatter( new[] { "pebbles_a", "pebbles_b" }, 20, 0.8f, sink: 0.35f, align: 1, allowPath: true, allowStream: true,
		prefer: ( x, y ) => InStream( x, y, 3 ) ? 1 : 0.25f );

	// -- vines: hung from limbs the trees have, strung from bark to bark -------

	/// A model whose origin is its top, at a limb's underside.
	GameObject Hang( string model, string tree, Func<List<((float x, float y, float z) p, float r)>, ((float x, float y, float z) p, float r)> choose,
		float? turn = null, float scale = 1, float lift = 0, string name = null )
	{
		var points = LimbPoints( tree, 4.5f, 0.12f );
		if ( points.Count == 0 ) return null;
		var (p, _) = choose( points );
		return Put( model, p.x, p.y, turn ?? Uniform( 0, 360 ), scale, lift: p.z - Height( p.x, p.y ) + lift, name: name );
	}

	/// An arch from tree a's bark to tree b's, at about height z.
	GameObject Strung( string model, float span, string a, string b, float z )
	{
		var (pa, ra) = TrunkPoint( a, z );
		var (pb, rb) = TrunkPoint( b, z );
		var d = MathF.Sqrt( (pb.x - pa.x) * (pb.x - pa.x) + (pb.y - pa.y) * (pb.y - pa.y) );
		float ux = (pb.x - pa.x) / d, uy = (pb.y - pa.y) / d;
		float ax = pa.x + ux * ra, ay = pa.y + uy * ra;
		float bx = pb.x - ux * rb, by = pb.y - uy * rb;
		var dist = MathF.Sqrt( (bx - ax) * (bx - ax) + (by - ay) * (by - ay) );
		var turn = MathF.Atan2( by - ay, bx - ax ).RadianToDegree();
		return Put( model, ax, ay, turn, dist / span, lift: pa.z - Height( ax, ay ), name: $"{model} {a}-{b}" );
	}

	Func<List<((float x, float y, float z) p, float r)>, ((float x, float y, float z) p, float r)> Pick( int k )
		=> points => points.OrderByDescending( p => p.p.z ).ElementAt( Math.Min( k, points.Count - 1 ) );

	Func<List<((float x, float y, float z) p, float r)>, ((float x, float y, float z) p, float r)> Outermost( string tree )
	{
		var (x0, y0, _, _) = treePlace[tree];
		return points => points.MaxBy( p => MathF.Sqrt( (p.p.x - x0) * (p.p.x - x0) + (p.p.y - y0) * (p.p.y - y0) ) );
	}

	Hang( "vinehang_b", "tree_giant_b", Outermost( "tree_giant_b" ) );
	Hang( "vinehang_a", "tree_giant_b", Pick( 3 ) );
	Hang( "mossdrape_b", "tree_giant_b", Pick( 6 ) );
	Hang( "vinehang_a", "mossy_giant", Outermost( "mossy_giant" ) );
	Hang( "mossdrape_b", "mossy_giant", Pick( 4 ) );
	Hang( "vinehang_c", "tree_lean_a", Outermost( "tree_lean_a" ) );
	Hang( "mossdrape_a", "tree_lean_a", Pick( 2 ) );
	Hang( "vinehang_b", "banyan_a", Outermost( "banyan_a" ), scale: 0.8f );
	Hang( "vinerope_a", "banyan_a", Pick( 2 ) );
	Hang( "aerialroots_a", "banyan_b", Outermost( "banyan_b" ) );
	Hang( "vinerope_b", "tree_giant_a", Outermost( "tree_giant_a" ) );
	Hang( "mossdrape_a", "tree_giant_a", Pick( 3 ) );
	Hang( "aerialroots_b", "strangler_a", Pick( 1 ) );
	Hang( "mossdrape_a", "tree_winding_c", Pick( 1 ) );
	Hang( "vinehang_c", "tree_winding_a", Pick( 1 ) );
	Hang( "mossdrape_b", "tree_giant_c", Pick( 2 ) );
	Hang( "vinehang_a", "climbed_b", Pick( 1 ) );
	Strung( "vinearch_a", 8, "tree_lean_a", "tree_giant_b", 7 );
	Strung( "vinearch_b", 12, "mossy_giant", "strangler_b", 8 );
	Strung( "vinearch_a", 8, "tree_winding_a", "tree_forked_a", 6.5f );
	Strung( "vinearch_b", 12, "tree_giant_a", "climbed_b", 7.5f );
	// and a curtain from a few of the tall picket trees
	string[] curtain = { "vinehang_a", "vinehang_c", "mossdrape_a" };
	foreach ( var n in Sample( treePlace.Keys.Where( k => k.StartsWith( "tree_tall" ) ), 8 ) )
		Hang( Choice( curtain ), n, Pick( 0 ), scale: Uniform( 0.7f, 1 ), name: $"vines on {n}" );
	// lianas coiled on the ground, where it is nearly level
	Scatter( new[] { "liana_a", "liana_b", "liana_c" }, 6, 2.5f, sink: 0.02f, align: 1, maxSlope: 8, pathMargin: 1 );
	Scatter( new[] { "vinetangle_a", "vinetangle_b" }, 8, 1.2f, sink: 0.05f, align: 1, maxSlope: 15, pathMargin: 0.5f );

	// -- shelf fungi on the dead wood, facing out of the bark -----------------
	string[] brackets = { "brackets_a", "brackets_b" };
	foreach ( var (snag, z) in new[] { ("snag_a", 1.6f), ("snag_b", 1.2f), ("snag_c", 0.9f), ("snag_b", 3.0f) } )
	{
		var (c, r) = TrunkPoint( snag, z );
		var a = Uniform( 0, 360 );
		float fx = c.x + MathF.Cos( a.DegreeToRadian() ) * r * 0.95f, fy = c.y + MathF.Sin( a.DegreeToRadian() ) * r * 0.95f;
		Put( Choice( brackets ), fx, fy, a, lift: c.z - Height( fx, fy ), name: $"brackets on {snag} {z:0.0}" );
	}

	// -- the understory, by rule rather than by volume ------------------------
	float Shade( float x, float y ) { var d = NearestTree( x, y ); return d < 5 ? 1 : d < 9 ? 0.75f : 0.45f; }
	float Damp( float x, float y ) { var d = MathF.Abs( x - Sx( y ) ); return d < 6 ? 1 : d < 10 ? 0.5f : 0.2f; }

	Scatter( new[] { "fern_a", "fern_b", "fern_c", "fern_d" }, 520, 0.55f, sink: 0.04f, align: 0.8f, prefer: Shade, weights: new[] { 3f, 2, 3, 1 }, pathMargin: 0.4f, maxSlope: 40 );
	Scatter( new[] { "broadleaf_a", "broadleaf_b", "elephant_a", "elephant_b" }, 90, 0.7f, sink: 0.03f, align: 0.5f, prefer: Damp, weights: new[] { 3f, 3, 1, 1 }, pathMargin: 0.6f );
	Scatter( new[] { "lily_a", "lily_b", "fanplant_a", "fanplant_b" }, 70, 0.6f, sink: 0.03f, align: 0.6f, pathMargin: 0.4f );
	Scatter( new[] { "bush_a", "bush_b" }, 40, 1, sink: 0.03f, align: 0.4f, prefer: Shade, pathMargin: 0.8f );
	Scatter( new[] { "sapling_a", "sapling_b" }, 60, 0.4f, sink: 0.03f, align: 0.3f, pathMargin: 0.5f );
	Scatter( new[] { "grass_a", "grass_b" }, 260, 0.45f, sink: 0.04f, align: 0.9f, scaleLo: 0.6f, scaleHi: 0.95f, pathMargin: 0.2f,
		prefer: ( x, y ) => OnPath( x, y, 2.5f ) || InStream( x, y, 3.5f ) ? 0.9f : 0.3f );
	Scatter( new[] { "mosscushion_a", "mosscushion_b", "mosscushion_c", "mosscarpet_a" }, 120, 0.5f, sink: 0.12f, align: 1,
		prefer: ( x, y ) => MathF.Min( 1, 0.5f * Shade( x, y ) + 0.5f * Damp( x, y ) ), pathMargin: 0.3f );
	Scatter( new[] { "litter_a", "litter_b" }, 200, 0.4f, sink: 0.02f, align: 1, allowPath: true, prefer: Shade, clear: 0, scaleLo: 0.5f, scaleHi: 0.85f );

	// -- light, fog, the player, the HUD --------------------------------------
	// The sun low, from behind and to the left of the walk, so trunks are lit
	// on their edges and the fog glows between them. An overcast sky -
	// materials/skybox/overcast.mat, the engine's sky shader with its cloud
	// cover nearly full - and the distance fog takes its colour from that sky,
	// so what is far away sinks into the same white the sky is.
	S.Environment( sunBrightness: 0.7f, sunRot: Gallery.PitchYaw( -34, 155 ), sunColor: "1,0.96,0.9,1", ambient: "0.16,0.22,0.18,1",
		skyTint: "0.9,0.93,0.92,1", shadowDetail: 96, skyMaterial: "materials/skybox/overcast.mat" );

	var fog = S.Comp<CubemapFog>( S.Go( world, "Distance Fog" ), "fog/distance" );
	fog.Tint = Gallery.C( "0.86,0.88,0.84,0.85" );
	fog.StartDistance = 6;
	fog.EndDistance = 60;
	fog.FalloffExponent = 1.25f;
	fog.HeightStart = -6;
	fog.HeightWidth = 26;
	fog.HeightExponent = 1.1f;

	var volume = S.Comp<VolumetricFogVolume>( S.Go( world, "Volume Fog", Gallery.V( 0, 4, 0 ) ), "fog/volume" );
	volume.Bounds = new BBox( Gallery.V( -32, -6, -32 ), Gallery.V( 32, 10, 32 ) );
	volume.Strength = 0.08f;
	volume.FalloffExponent = 0.8f;
	volume.Color = Gallery.C( "0.68,0.78,0.74,1" );

	// The camera keeps a picture of the depth for the water to read the bed
	// through - see DepthPicture - and darkens the corners with occlusion. The
	// grade: a little less saturated and a touch more contrast than the raw
	// render - the look of the references, which are overcast and damp. The
	// cool of them is the sky's own, not a grade.
	var player = S.Player( Gallery.V( Px( -23 ), Height( Px( -23 ), -23 ) + 1.15f, 23 ), speed: 4.5f );
	player.LocalRotation = Gallery.Yaw( 22 );
	var camera = player.Children.First( c => c.Name == "Camera" );
	S.Comp<DepthPicture>( camera, "depthpicture" );
	S.Comp<AmbientOcclusion>( camera, "ssao" ).Intensity = 0.8f;
	var adjust = S.Comp<ColorAdjustments>( camera, "adjust" );
	adjust.Saturation = 0.95f;
	adjust.Contrast = 1.03f;

	S.Hud( "The jungle. Walk the path north along the stream. Q returns." );

	objects = S.Scene.Directory.AllGameObjects.Count();
}

var wrote = S.Write( "rendering/jungle.scene" );
Gallery.RegisterInMenu( "rendering/jungle.scene", "Jungle", "Rendering",
	"A rainforest: stream, path, giants, stranglers, banyans, palms, bamboo, ferns, dead wood, moss and fog" );

return new { Wrote = wrote, Objects = objects, HullsWritten = hullsWritten };
