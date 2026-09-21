// What the gallery scenes share: objects, components, the environment, a
// player, a HUD, and areas laid out in rows away from the spawn. Runs inside
// the editor through execute_code (see build.py), so the engine makes every
// object and writes the file - nothing here knows what a .scene looks like.
using System.IO;
using System.Security.Cryptography;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.Json.Nodes;
using TestGround;
using Template;

/// <summary>
/// One scene's worth of ids: every guid is a name under the scene's own root,
/// so a regenerated scene keeps its ids and the editor's references into it
/// stay good. The same uuid5 names the Python generators used, so a scene
/// rebuilt from here has the ids it had.
/// </summary>
class Gallery
{
	public readonly string Key;
	public readonly string Title;
	public readonly string Description;
	public readonly Scene Scene;

	readonly Dictionary<string, string> taken = new();

	public Gallery( string key, string title, string description )
	{
		Key = key;
		Title = title;
		Description = description;
		Scene = Scene.CreateEditorScene();
	}

	// -- ids ---------------------------------------------------------------

	static readonly Guid NamespaceUrl = new( "6ba7b811-9dad-11d1-80b4-00c04fd430c8" );

	public Guid Id( string name )
	{
		if ( taken.TryGetValue( name, out var first ) )
			throw new Exception( $"guid clash: '{name}' is already used by {first}" );

		taken[name] = name;

		var input = NamespaceUrl.ToByteArray( bigEndian: true )
			.Concat( Encoding.UTF8.GetBytes( $"rinten-gallery/{Key}/{name}" ) )
			.ToArray();

		var hash = SHA1.HashData( input );
		var bytes = hash[..16];
		bytes[6] = (byte)((bytes[6] & 0x0F) | 0x50);
		bytes[8] = (byte)((bytes[8] & 0x3F) | 0x80);

		return new Guid( bytes, bigEndian: true );
	}

	// -- values ------------------------------------------------------------

	public static Vector3 V( float x, float y, float z ) => new( x, y, z );

	/// <summary>A colour from "r,g,b,a".</summary>
	public static Color C( string rgba ) => (Color)Vector4.Parse( rgba );

	/// <summary>A rotation about Y.</summary>
	public static Rotation Yaw( float deg )
	{
		var h = deg.DegreeToRadian() / 2;
		return new Rotation( 0, MathF.Sin( h ), 0, MathF.Cos( h ) );
	}

	/// <summary>
	/// Pitch about X then yaw about Y. A negative pitch turns forward (-Z)
	/// downward: a sun or a spot pointing at the floor is PitchYaw( -90, 0 ).
	/// </summary>
	public static Rotation PitchYaw( float pitchDeg, float yawDeg )
	{
		float cp = MathF.Cos( pitchDeg.DegreeToRadian() / 2 ), sp = MathF.Sin( pitchDeg.DegreeToRadian() / 2 );
		float cy = MathF.Cos( yawDeg.DegreeToRadian() / 2 ), sy = MathF.Sin( yawDeg.DegreeToRadian() / 2 );
		return new Rotation( cy * sp, sy * cp, -sy * sp, cy * cp );
	}

	public static readonly Rotation Upright = new( 0.7071068f, 0, 0, 0.7071068f );

	// -- objects and components --------------------------------------------

	public GameObject Go( GameObject parent, string name, Vector3 pos = default, Rotation? rot = null, Vector3? scale = null, string tags = "", bool enabled = true )
	{
		var go = new GameObject( parent ?? Scene, enabled, name );
		go.SetDeterministicId( Id( "go/" + name ) );
		go.LocalPosition = pos;
		go.LocalRotation = rot ?? Rotation.Identity;
		go.LocalScale = scale ?? Vector3.One;

		if ( !string.IsNullOrEmpty( tags ) )
			go.Tags.Add( tags.Split( ',' ) );

		return go;
	}

	public T Comp<T>( GameObject go, string name ) where T : Component, new()
	{
		var c = go.Components.Create<T>();
		c.SetDeterministicId( Id( "comp/" + name ) );
		return c;
	}

	public ModelRenderer Model( GameObject go, string name, Color tint, string material = null, string model = "models/dev/box.mdl", ModelRenderer.ShadowRenderType render = ModelRenderer.ShadowRenderType.On )
	{
		var m = Comp<ModelRenderer>( go, "model/" + name );
		m.Model = Rinten.Model.Load( model );
		m.MaterialOverride = material is null ? null : Material.Load( material );
		m.Tint = tint;
		m.RenderType = render;
		return m;
	}

	public BoxCollider BoxCollider( GameObject go, string name, bool isStatic = true, bool trigger = false )
	{
		var c = Comp<BoxCollider>( go, "collider/" + name );
		c.Static = isStatic;
		c.IsTrigger = trigger;
		return c;
	}

	/// <summary>A box with a collider - the floors, walls and slabs.</summary>
	public GameObject Block( GameObject parent, string name, Vector3 pos, Vector3 scale, Color tint, string material = null, string model = "models/dev/box.mdl", string tags = "world", ModelRenderer.ShadowRenderType render = ModelRenderer.ShadowRenderType.On, bool collide = true, Rotation? rot = null )
	{
		var go = Go( parent, name, pos, rot, scale, tags );
		Model( go, name, tint, material, model, render );
		if ( collide ) BoxCollider( go, name );
		return go;
	}

	public static TextRendering.Scope TextScope( string text, Color? color = null, string font = "Poppins", float size = 50, int weight = 700, bool italic = false, float lineHeight = 1.1f, float letterSpacing = 0, bool shadow = true )
	{
		var scope = new TextRendering.Scope( text, color ?? C( "0.9,0.94,1,1" ), size, font, weight )
		{
			FontItalic = italic,
			LineHeight = lineHeight,
			LetterSpacing = letterSpacing,
			Shadow = new TextRendering.Shadow { Enabled = shadow, Size = 6, Color = C( "0,0,0,0.8" ), Offset = new Vector2( 3, 3 ) },
		};
		return scope;
	}

	public TextRenderer Text( GameObject go, string name, TextRendering.Scope scope, float scale = 0.26f, TextRenderer.BillboardMode billboard = TextRenderer.BillboardMode.YOnly )
	{
		var t = Comp<TextRenderer>( go, "text/" + name );
		t.TextScope = scope;
		t.Scale = scale;
		t.Billboard = billboard;
		t.HorizontalAlignment = TextRenderer.HAlignment.Center;
		t.VerticalAlignment = TextRenderer.VAlignment.Center;
		return t;
	}

	public GameObject Label( GameObject parent, string name, Vector3 pos, string text, float scale = 0.26f, Color? color = null, float size = 50 )
	{
		var go = Go( parent, "Label: " + name, pos );
		Text( go, "label/" + name, TextScope( text, color, size: size ), scale );
		return go;
	}

	// -- the furniture every scene has --------------------------------------

	public GameObject Environment( float sunBrightness = 1.2f, Rotation? sunRot = null, string sunColor = "1,0.95,0.88,1", string ambient = "0.2,0.22,0.3,1", string skyTint = "0.75,0.8,0.9,1", bool shadows = true, float shadowDetail = 64, float sourceRadius = 0.05f, bool skyIndirect = true, string skyMaterial = "materials/skybox/procedural.mat" )
	{
		var env = Go( Scene, "Environment" );

		var sunGo = Go( env, "Sun", rot: sunRot ?? new Rotation( -0.4508033f, 0.1919843f, 0.0999407f, 0.8659851f ), tags: "light_directional,light" );
		var sun = Comp<DirectionalLight>( sunGo, "sun" );
		sun.Attenuation = 1;
		sun.Brightness = sunBrightness;
		sun.LightColor = C( sunColor );
		sun.ShadowDetail = shadowDetail;
		sun.Shadows = shadows;
		sun.SkyColor = C( "0,0,0,0" );
		sun.SourceRadius = sourceRadius;

		Comp<AmbientLight>( Go( env, "Ambient" ), "ambient" ).Color = C( ambient );

		var sky = Comp<SkyBox2D>( Go( env, "2D Skybox", tags: "skybox" ), "sky" );
		sky.SkyIndirectLighting = skyIndirect;
		sky.SkyMaterial = Material.Load( skyMaterial );
		sky.Tint = C( skyTint );

		return env;
	}

	public GameObject Player( Vector3 pos, Rotation? pitchRot = null, float fov = 75, float speed = 7, bool bloom = true )
	{
		var player = Go( Scene, "Player", pos );
		var camGo = Go( player, "Camera", rot: pitchRot ?? new Rotation( -0.0697565f, 0, 0, 0.9975641f ), tags: "maincamera" );

		var cam = Comp<CameraComponent>( camGo, "camera" );
		cam.BackgroundColor = C( "0.05,0.06,0.08,1" );
		cam.ClearFlags = ClearFlags.All;
		cam.FieldOfView = fov;
		cam.IsMainCamera = true;
		cam.Priority = 1;
		cam.ZFar = 400;
		cam.ZNear = 0.05f;

		if ( bloom )
		{
			var b = Comp<Bloom>( camGo, "bloom" );
			b.Mode = Bloom.BloomMode.Additive;
			b.Spread = 0.6f;
			b.Strength = 0.6f;
			b.Threshold = 1;
		}

		var p = Comp<Template.Player>( player, "player" );
		p.Camera = cam;
		p.PitchClamp = 89;
		p.RunScale = 3;
		p.Speed = speed;

		return player;
	}

	public GameObject Hud( string note )
	{
		var hud = Go( Scene, "HUD" );
		Comp<ScreenPanel>( hud, "hud/panel" );
		var scene = Comp<SceneHud>( hud, "hud/scene" );
		scene.Note = note;
		scene.Title = Title;
		Comp<ReturnToMenu>( hud, "hud/return" ).Key = "Q";
		Comp<TestGround.FrameStats>( hud, "hud/stats" );
		return hud;
	}

	// -- areas: rows away from the spawn -----------------------------------

	public static readonly Color Slab = C( "0.34,0.36,0.4,1" );
	public static readonly Color Wall = C( "0.11,0.12,0.15,1" );

	public GameObject Area( GameObject parent, string title, string note, float z, float width, float depth = 14, bool wall = true, float wallHeight = 6, string slabMaterial = "materials/dev/grid.mat", Color? slabTint = null )
	{
		var area = Go( parent, "Area: " + title );
		Block( area, "Slab: " + title, V( 0, -0.2f, z ), V( width, 0.4f, depth ), slabTint ?? Slab, slabMaterial );

		if ( wall )
			Block( area, "Wall: " + title, V( 0, wallHeight / 2, z - depth / 2 ), V( width, wallHeight, 0.5f ), Wall );

		// Just over the wall: from the spawn's height the next row's title is
		// behind this row's wall rather than stacked over it.
		Label( area, "Area: " + title, V( 0, wallHeight + 0.9f, z - depth / 2 + 1 ), $"{title}\n{note}", scale: 0.9f );

		return area;
	}

	/// <summary>The slab a row of n stations wants.</summary>
	public static float RowWidth( int n, float spacing ) => n * spacing + 8;

	/// <summary>
	/// Stations along a row, centred on x = 0. make gets each item, its name
	/// with the row's tag in front, and where the station stands; what it
	/// makes comes back in order.
	/// </summary>
	public static List<GameObject> Row<T>( IReadOnlyList<T> items, float spacing, float z, string tag, Func<T, string> name, Func<T, string, Vector3, GameObject> make )
	{
		var n = items.Count;
		var stations = new List<GameObject>( n );

		for ( var i = 0; i < n; i++ )
		{
			var x = (i - (n - 1) / 2f) * spacing;
			stations.Add( make( items[i], $"{tag} {name( items[i] )}", V( x, 0, z ) ) );
		}

		return stations;
	}

	/// <summary>
	/// Every other station's sign a step higher, so two signs wider than the
	/// gap between their stands never sit side by side.
	/// </summary>
	public static void StaggerSigns( IEnumerable<GameObject> stations, float rise = 0.9f )
	{
		var i = 0;

		foreach ( var station in stations )
		{
			if ( i++ % 2 == 0 ) continue;

			foreach ( var child in station.Children )
			{
				if ( child.Name.StartsWith( "Label:" ) )
					child.LocalPosition += Vector3.Up * rise;
			}
		}
	}

	// -- out ------------------------------------------------------------------

	/// <summary>
	/// The scene as the editor would save it, at scenes/&lt;filename&gt;, and the
	/// scene torn down. The path comes back as the asset system knows it.
	/// </summary>
	public string Write( string filename )
	{
		Scene.SetDeterministicId( Id( "scene" ) );

		var file = Scene.CreateSceneFile();
		var path = Path.Combine( Project.Current.GetAssetsPath(), "scenes", filename );
		Directory.CreateDirectory( Path.GetDirectoryName( path ) );

		var asset = AssetSystem.CreateResource( "scene", path )
			?? throw new Exception( $"Couldn't make a scene asset at {path}" );

		asset.SaveToDisk( file, compile: false );
		Scene.Destroy();

		// A session with this scene open reloads from its Source, and every save
		// makes a new SceneFile for the path, so its Source is now the old one:
		// point it at what was just written, and open_scene {reload} shows it.
		foreach ( var session in SceneEditorSession.All )
		{
			if ( string.Equals( session.Scene?.Source?.ResourcePath, asset.Path, StringComparison.OrdinalIgnoreCase ) )
				session.Scene.Source = file;
		}

		Log.Info( $"wrote {asset.Path}" );
		return asset.Path;
	}

	/// <summary>
	/// The scene's card in the main menu, once, in place of an older card for
	/// the same file. Edits main.scene's text rather than loading it, so the
	/// rest of the menu comes out exactly as it went in.
	/// </summary>
	public static void RegisterInMenu( string sceneFile, string title, string category, string description )
	{
		var path = Path.Combine( Project.Current.GetAssetsPath(), "scenes/main.scene" );
		var main = JsonNode.Parse( File.ReadAllText( path ) ).AsObject();

		var entry = new JsonObject
		{
			["Scene"] = "scenes/" + sceneFile,
			["Title"] = title,
			["Category"] = category,
			["Description"] = description,
			["DisplayName"] = title,
		};

		bool Walk( JsonArray objects )
		{
			foreach ( var o in objects.OfType<JsonObject>() )
			{
				foreach ( var c in (o["Components"] as JsonArray ?? new JsonArray()).OfType<JsonObject>() )
				{
					if ( c["__type"]?.GetValue<string>() != "TestGround.SceneMenu" ) continue;

					var entries = c["Scenes"] as JsonArray;
					if ( entries is null ) c["Scenes"] = entries = new JsonArray();

					for ( var i = 0; i < entries.Count; i++ )
					{
						if ( string.Equals( entries[i]?["Scene"]?.GetValue<string>(), entry["Scene"].GetValue<string>(), StringComparison.OrdinalIgnoreCase ) )
						{
							entries[i] = entry;
							return true;
						}
					}

					entries.Add( entry );
					return true;
				}

				if ( o["Children"] is JsonArray children && Walk( children ) )
					return true;
			}

			return false;
		}

		if ( !Walk( main["GameObjects"].AsArray() ) )
			throw new Exception( "no SceneMenu in main.scene" );

		File.WriteAllText( path, main.ToJsonString( new JsonSerializerOptions { WriteIndented = true, Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping } ) );
		Log.Info( $"registered {title} in the menu" );
	}
}
