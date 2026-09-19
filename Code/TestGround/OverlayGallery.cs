namespace TestGround;

/// <summary>
/// Draws one of each debug overlay primitive in rows, so a broken overlay
/// is a missing shape rather than a silent one.
/// </summary>
/// <remarks>
/// Front to back: the plain shapes; the composite ones - capsules, a cone, a
/// frustum, a trace; the ways of drawing rather than the shapes - from the
/// fixed step, with a lifetime, through a solid, a model, a copy of an object;
/// the edges - empty and zero-sized input, text anchors and sizes, alpha, a
/// shared transform, a trail of timed shapes; a wall with every overlay shape
/// behind it; and the swept traces. The screen-space draws sit down the left
/// edge of the view, where nothing in the world can be mistaken for them, and
/// a dim box stands around the whole gallery and the player, so the near
/// plane has something to clip.
/// </remarks>
[Title( "Overlay Gallery" )]
[Category( "Test Ground" )]
[Icon( "square_foot" )]
public sealed class OverlayGallery : Component, Component.ExecuteInEditor
{
	/// <summary>Metres between exhibits along a row.</summary>
	[Property] public float Spacing { get; set; } = 1.6f;

	/// <summary>Metres between rows, going away from the front.</summary>
	[Property] public float RowSpacing { get; set; } = 2.5f;

	/// <summary>Metres each row stands above the one in front, so the back rows show over it.</summary>
	[Property] public float RowRise { get; set; } = 0.8f;

	/// <summary>
	/// An object whose renderers are drawn again as an overlay, tinted, in the
	/// back row. Leave the object itself disabled so only the copy is seen.
	/// </summary>
	[Property] public GameObject Ghost { get; set; }

	/// <summary>Seconds the timed exhibit lives, and how often a new one is made.</summary>
	const float TimedLife = 3.0f;

	TimeSince sinceTimed = 999.0f;
	TimeSince sinceTrail = 999.0f;
	TimeSince sinceBlink = 999.0f;

	Texture picture;
	bool pictureLooked;

	/// <summary>Where an exhibit stands: a column along the row, a row away from the front.</summary>
	Vector3 At( int row, int column )
		=> WorldPosition + Vector3.Up * ( 1.2f + RowRise * row )
			+ WorldRotation.Right * ( Spacing * column )
			+ WorldRotation.Forward * ( RowSpacing * row );

	protected override void OnUpdate()
	{
		FrontRow();
		MiddleRow();
		BackRow();
		EdgeRow();
		WallRow();
		SweepRow();
		Surroundings();
		ScreenEdge();
	}

	/// <summary>
	/// The fixed step keeps its own list of single-frame overlays, emptied at
	/// the start of every fixed update rather than every frame. A shape drawn
	/// from here that flickers is that list being cleared by the wrong stage;
	/// a timed one from here that vanishes early is the other list.
	/// </summary>
	protected override void OnFixedUpdate()
	{
		var fixedBox = At( 2, 4 );
		DebugOverlay.Box( BBox.FromPositionAndSize( fixedBox + Vector3.Up * 0.4f, 0.5f ), Color.Yellow );
		DebugOverlay.Line( fixedBox + Vector3.Up * 0.4f, fixedBox + Vector3.Up * 0.4f + WorldRotation.Right * 0.4f, Color.Yellow, duration: 0.5f );
	}

	/// <summary>
	/// Drawn as the frame is about to render rather than in the update: a
	/// shape from here that is missing is the stage that runs after the
	/// single-frame list was swept.
	/// </summary>
	protected override void OnPreRender()
	{
		var pre = At( 5, 6 );
		DebugOverlay.Sphere( new Sphere( pre + Vector3.Up * 0.4f, 0.25f ), Color.Cyan );
	}

	void FrontRow()
	{
		var line = At( 0, 0 );
		DebugOverlay.Line( line, line + Vector3.Up * 0.8f, Color.White );
		Label( line, "Line" );

		var timed = At( 0, 1 );
		DebugOverlay.Line( timed, timed + Vector3.Up * 0.8f + WorldRotation.Right * 0.2f, Color.White * System.Random.Shared.Float( 0.5f, 1.0f ), duration: 1.0f );
		Label( timed, "1s Line" );

		var overlay = At( 0, 2 );
		DebugOverlay.Line( overlay, overlay + Vector3.Up * 0.8f, Color.Green, overlay: true );
		Label( overlay, "Overlay" );

		var text = At( 0, 3 );
		DebugOverlay.Text( text + Vector3.Up * 0.4f, "Hello", size: 28 );
		Label( text, "Text" );

		var sphere = At( 0, 4 );
		DebugOverlay.Sphere( new Sphere( sphere + Vector3.Up * 0.4f, 0.3f ), Color.Cyan );
		Label( sphere, "Sphere" );

		var box = At( 0, 5 );
		DebugOverlay.Box( BBox.FromPositionAndSize( box + Vector3.Up * 0.4f, 0.5f ), Color.Orange );
		Label( box, "Box" );

		var spin = At( 0, 6 );
		var spinTx = new Transform( spin + Vector3.Up * 0.4f, new Angles( Time.Now * 90.0f, Time.Now * 120.0f, 0 ) );
		DebugOverlay.Box( BBox.FromPositionAndSize( 0, 0.45f ), Color.Magenta, transform: spinTx );
		Label( spin, "Rotated Box" );
	}

	void MiddleRow()
	{
		var normal = At( 1, 0 );
		DebugOverlay.Normal( normal + Vector3.Up * 0.2f, ( Vector3.Up + WorldRotation.Right ).Normal * 0.6f, Color.Yellow );
		Label( normal, "Normal" );

		// A strip rather than a list of pairs: a renderer that draws every
		// strip as pairs shows every other segment of this wave.
		var polyline = At( 1, 1 );
		var points = new Vector3[49];
		for ( var i = 0; i < points.Length; i++ )
		{
			var f = i / (float)( points.Length - 1 );
			var wave = ( f * 4.0f + Time.Now * 2.0f ) * 3.14159f;
			points[i] = polyline + WorldRotation.Right * ( f - 0.5f ) + Vector3.Up * ( 0.4f + 0.25f * float.Sin( wave ) );
		}
		DebugOverlay.Line( points, Color.Cyan );
		Label( polyline, "Polyline" );

		var capsule = At( 1, 2 );
		DebugOverlay.Capsule( new Capsule( capsule + Vector3.Up * 0.2f, capsule + Vector3.Up * 0.7f, 0.2f ), Color.Orange );
		Label( capsule, "Capsule" );

		var cylinder = At( 1, 3 );
		DebugOverlay.Cylinder( new Capsule( cylinder + Vector3.Up * 0.1f, cylinder + Vector3.Up * 0.7f, 0.25f ), Color.Magenta );
		Label( cylinder, "Cylinder" );

		var cone = At( 1, 4 );
		DebugOverlay.TaperedCylinder( cone + Vector3.Up * 0.1f, cone + Vector3.Up * 0.8f, 0.3f, 0.0f, Color.Green );
		Label( cone, "Cone" );

		// A little camera's worth of view, swinging about the row so its far
		// end fans out to the side rather than into the next exhibit.
		var frustum = At( 1, 5 );
		var eye = frustum + Vector3.Up * 0.4f;
		var rot = WorldRotation * Rotation.FromYaw( 90.0f + 30.0f * float.Sin( Time.Now ) );
		var frustumShape = Frustum.FromCorners(
			new Ray( eye, ( rot.Forward + rot.Left * 0.4f + rot.Up * 0.3f ).Normal ),
			new Ray( eye, ( rot.Forward + rot.Right * 0.4f + rot.Up * 0.3f ).Normal ),
			new Ray( eye, ( rot.Forward + rot.Right * 0.4f + rot.Down * 0.3f ).Normal ),
			new Ray( eye, ( rot.Forward + rot.Left * 0.4f + rot.Down * 0.3f ).Normal ),
			0.1f, 0.7f );
		DebugOverlay.Frustum( frustumShape, Color.White );
		Label( frustum, "Frustum" );

		// Straight down into the floor: white ray, red hit, red normal. The row
		// stands a way above the floor, so the ray is long enough to reach it.
		var trace = At( 1, 6 );
		var hit = Scene.Trace.Ray( trace + Vector3.Up * 0.8f, trace + Vector3.Down * 4.0f )
			.IgnoreGameObjectHierarchy( GameObject )
			.Run();
		DebugOverlay.Trace( hit );
		Label( trace, "Trace" );
	}

	void BackRow()
	{
		var model = At( 2, 0 );
		var modelTx = new Transform( model + Vector3.Up * 0.05f, Rotation.FromYaw( Time.Now * 45.0f ), 0.4f );
		DebugOverlay.Model( Model.Cube, Color.Cyan, transform: modelTx );
		Label( model, "Model" );

		// The transform stands in for the object's own, scale included, so the
		// copy is sized here rather than on the object. The object has a child
		// of its own, so the copy is two renderers standing the right way apart.
		var ghost = At( 2, 1 );
		if ( Ghost.IsValid() )
		{
			var ghostTx = new Transform( ghost + Vector3.Up * 0.05f, Rotation.FromYaw( Time.Now * -45.0f ), 0.3f );
			DebugOverlay.GameObject( Ghost, Color.Orange, transform: ghostTx );
			Label( ghost, "GameObject" );
		}
		else
		{
			Label( ghost, "GameObject (set Ghost)" );
		}

		// A scope with its own font, weight and outline, not the defaults.
		var rich = At( 2, 2 );
		var scope = new TextRendering.Scope( "Rich", Color.Yellow, 40, "Roboto", 800 )
		{
			Outline = new TextRendering.Outline { Enabled = true, Color = Color.Black, Size = 3 },
		};
		DebugOverlay.Text( rich + Vector3.Up * 0.4f, scope );
		Label( rich, "Rich Text" );

		// A solid cube with an overlay sphere and a word inside it. Seen at all
		// only because they ignore depth; a cube with nothing showing through
		// it is an overlay that is being depth tested after all.
		var inside = At( 2, 3 );
		var core = inside + Vector3.Up * 0.4f;
		DebugOverlay.Model( Model.Cube, Color.Gray, transform: new Transform( core, Rotation.Identity, 0.5f ) );
		DebugOverlay.Sphere( new Sphere( core, 0.18f ), Color.Green, overlay: true );
		DebugOverlay.Text( core, "Inside", size: 20, color: Color.Green, overlay: true );
		Label( inside, "Overlay (in cube)" );

		// Column 4 is drawn from OnFixedUpdate.
		Label( At( 2, 4 ), "Fixed Update" );

		// One sphere every few seconds, kept for that long: there is never more
		// than one, and the label counts it down.
		var timed = At( 2, 5 );
		if ( sinceTimed > TimedLife )
		{
			sinceTimed = 0;
			DebugOverlay.Sphere( new Sphere( timed + Vector3.Up * 0.4f, 0.3f ), Color.Red, duration: TimedLife );
		}
		Label( timed, $"{TimedLife:0}s Sphere ({TimedLife - sinceTimed:0.0})" );

		// A box swept sideways along the row into nothing: drawn where it
		// started and where it stopped, both red for a miss.
		var sweep = At( 2, 6 );
		var from = sweep + Vector3.Up * 0.4f + WorldRotation.Left * 0.5f;
		var to = sweep + Vector3.Up * 0.4f + WorldRotation.Right * 0.5f;
		var swept = Scene.Trace.Box( BBox.FromPositionAndSize( 0, 0.3f ), from, to )
			.IgnoreGameObjectHierarchy( GameObject )
			.Run();
		DebugOverlay.Trace( swept );
		Label( sweep, "Box Sweep (miss)" );
	}

	/// <summary>The input nobody means to give, and the options nobody tries.</summary>
	void EdgeRow()
	{
		// Nothing, one point, two of the same point, no words, no size, no
		// length. None of these may throw, and the capsule with no length is
		// drawn as the sphere it is - the one thing here that should show.
		var empty = At( 3, 0 );
		DebugOverlay.Line( System.Array.Empty<Vector3>(), Color.White );
		DebugOverlay.Line( new[] { empty + Vector3.Up * 0.4f }, Color.White );
		DebugOverlay.Line( empty + Vector3.Up * 0.4f, empty + Vector3.Up * 0.4f, Color.White );
		DebugOverlay.Text( empty + Vector3.Up * 0.4f, "", size: 28 );
		DebugOverlay.Box( BBox.FromPositionAndSize( empty + Vector3.Up * 0.4f, 0.0f ), Color.White );
		DebugOverlay.Sphere( new Sphere( empty + Vector3.Up * 0.4f, 0.0f ), Color.White );
		DebugOverlay.Capsule( new Capsule( empty + Vector3.Up * 0.4f, empty + Vector3.Up * 0.4f, 0.2f ), Color.Orange );
		Label( empty, "Degenerate" );

		// Four words hung off one point by their corners, and a cross at the
		// point. Each should sit in its own quadrant.
		var anchors = At( 3, 1 );
		var pin = anchors + Vector3.Up * 0.4f;
		DebugOverlay.Line( pin + WorldRotation.Left * 0.1f, pin + WorldRotation.Right * 0.1f, Color.Red );
		DebugOverlay.Line( pin + Vector3.Down * 0.1f, pin + Vector3.Up * 0.1f, Color.Red );
		DebugOverlay.Text( pin, "LT", size: 20, flags: TextFlag.LeftTop );
		DebugOverlay.Text( pin, "RT", size: 20, flags: TextFlag.RightTop );
		DebugOverlay.Text( pin, "LB", size: 20, flags: TextFlag.LeftBottom );
		DebugOverlay.Text( pin, "RB", size: 20, flags: TextFlag.RightBottom );
		Label( anchors, "Text Anchors" );

		var lines = At( 3, 2 );
		DebugOverlay.Text( lines + Vector3.Up * 0.4f, "Two\nlines", size: 24 );
		Label( lines, "Multiline" );

		// A size under the floor of thirty-two is scaled down rather than
		// rasterised small; a big one is rasterised big.
		var sizes = At( 3, 3 );
		DebugOverlay.Text( sizes + Vector3.Up * 0.15f, "tiny", size: 8 );
		DebugOverlay.Text( sizes + Vector3.Up * 0.5f, "BIG", size: 64 );
		Label( sizes, "Sizes 8 / 64" );

		// See-through shapes: the floor should show through all three.
		var alpha = At( 3, 4 );
		var faint = Color.White.WithAlpha( 0.3f );
		DebugOverlay.Line( alpha, alpha + Vector3.Up * 0.8f, faint );
		DebugOverlay.Box( BBox.FromPositionAndSize( alpha + Vector3.Up * 0.4f, 0.5f ), Color.Orange.WithAlpha( 0.3f ) );
		DebugOverlay.Sphere( new Sphere( alpha + Vector3.Up * 0.4f, 0.3f ), Color.Cyan.WithAlpha( 0.3f ) );
		Label( alpha, "Alpha 0.3" );

		// One turning transform, four shapes given in its space: they should
		// turn together as one thing.
		var shared = At( 3, 5 );
		var sharedTx = new Transform( shared + Vector3.Up * 0.4f, Rotation.FromYaw( Time.Now * 60.0f ) * Rotation.FromPitch( 30.0f ), 0.8f );
		DebugOverlay.Line( 0, Vector3.Up * 0.5f, Color.White, transform: sharedTx );
		DebugOverlay.Box( BBox.FromPositionAndSize( Vector3.Right * 0.3f, 0.2f ), Color.Orange, transform: sharedTx );
		DebugOverlay.Sphere( new Sphere( Vector3.Left * 0.3f, 0.12f ), Color.Cyan, transform: sharedTx );
		DebugOverlay.Capsule( new Capsule( Vector3.Forward * 0.3f, Vector3.Forward * 0.3f + Vector3.Up * 0.3f, 0.08f ), Color.Magenta, transform: sharedTx );
		Label( shared, "Shared Transform" );

		// A point going round, leaving a box behind every tenth of a second
		// that lives for one: a tail of ten, the oldest fading out as the
		// newest appears. A tail that jumps in length is expiry going wrong.
		var trail = At( 3, 6 );
		var angle = Time.Now * 2.0f;
		var head = trail + Vector3.Up * 0.4f + WorldRotation.Right * ( 0.35f * float.Cos( angle ) ) + Vector3.Up * ( 0.3f * float.Sin( angle ) );
		DebugOverlay.Sphere( new Sphere( head, 0.05f ), Color.Yellow );
		if ( sinceTrail > 0.1f )
		{
			sinceTrail = 0;
			DebugOverlay.Box( BBox.FromPositionAndSize( head, 0.06f ), Color.Yellow.WithAlpha( 0.6f ), duration: 1.0f );
		}
		Label( trail, "Trail (1s)" );
	}

	/// <summary>
	/// A solid wall across the row with one of each shape behind it, all
	/// drawn as overlays. Every one should show through; the model is the
	/// one that is not expected to yet, since models are drawn by the queue
	/// and the queue does not read the layer.
	/// </summary>
	void WallRow()
	{
		var middle = At( 4, 3 ) + Vector3.Up * 0.5f;
		var wallSize = new Vector3( Spacing * 7.2f, 0.8f, 0.05f );
		DebugOverlay.Model( Model.Cube, Color.Gray.Darken( 0.3f ), transform: new Transform( middle, WorldRotation, wallSize ) );

		Vector3 Behind( int column ) => At( 4, column ) + Vector3.Up * 0.4f + WorldRotation.Forward * 0.5f;

		var line = Behind( 0 );
		DebugOverlay.Line( line + Vector3.Down * 0.3f, line + Vector3.Up * 0.3f, Color.Green, overlay: true );
		Label( At( 4, 0 ), "Line" );

		DebugOverlay.Box( BBox.FromPositionAndSize( Behind( 1 ), 0.4f ), Color.Green, overlay: true );
		Label( At( 4, 1 ), "Box" );

		DebugOverlay.Sphere( new Sphere( Behind( 2 ), 0.25f ), Color.Green, overlay: true );
		Label( At( 4, 2 ), "Sphere" );

		var capsule = Behind( 3 );
		DebugOverlay.Capsule( new Capsule( capsule + Vector3.Down * 0.15f, capsule + Vector3.Up * 0.15f, 0.15f ), Color.Green, overlay: true );
		Label( At( 4, 3 ), "Capsule" );

		DebugOverlay.Text( Behind( 4 ), "Behind", size: 24, color: Color.Green, overlay: true );
		Label( At( 4, 4 ), "Text" );

		DebugOverlay.Model( Model.Cube, Color.Green, transform: new Transform( Behind( 5 ), Rotation.FromYaw( Time.Now * 45.0f ), 0.3f ), overlay: true );
		Label( At( 4, 5 ), "Model (not yet)" );

		var cylinder = Behind( 6 );
		DebugOverlay.Cylinder( new Capsule( cylinder + Vector3.Down * 0.25f, cylinder + Vector3.Up * 0.25f, 0.2f ), Color.Green, overlay: true );
		Label( At( 4, 6 ), "Cylinder" );

		Label( At( 4, 3 ) + Vector3.Down * 0.35f, "- overlay shapes behind a wall -" );
	}

	/// <summary>
	/// Every shape a trace can be swept as, down into the floor, so each ends
	/// green where it stopped - and a ray into the sky that stops red.
	/// </summary>
	void SweepRow()
	{
		SceneTraceResult Down( SceneTrace trace ) => trace.IgnoreGameObjectHierarchy( GameObject ).Run();

		var ray = At( 5, 0 );
		DebugOverlay.Trace( Down( Scene.Trace.Ray( ray + Vector3.Up * 0.1f, ray + Vector3.Up * 0.9f ) ) );
		Label( ray, "Ray (miss)" );

		var sphere = At( 5, 1 );
		DebugOverlay.Trace( Down( Scene.Trace.Sphere( 0.15f, sphere + Vector3.Up * 0.8f, sphere + Vector3.Down * 6.0f ) ) );
		Label( sphere, "Sphere Sweep" );

		var capsule = At( 5, 2 );
		DebugOverlay.Trace( Down( Scene.Trace.Capsule( new Capsule( Vector3.Down * 0.15f, Vector3.Up * 0.15f, 0.1f ), capsule + Vector3.Up * 0.8f, capsule + Vector3.Down * 6.0f ) ) );
		Label( capsule, "Capsule Sweep" );

		var cylinder = At( 5, 3 );
		DebugOverlay.Trace( Down( Scene.Trace.Cylinder( 0.3f, 0.12f, cylinder + Vector3.Up * 0.8f, cylinder + Vector3.Down * 6.0f ) ) );
		Label( cylinder, "Cylinder Sweep" );

		var box = At( 5, 4 );
		DebugOverlay.Trace( Down( Scene.Trace.Box( BBox.FromPositionAndSize( 0, 0.25f ), box + Vector3.Up * 0.8f, box + Vector3.Down * 6.0f ) ) );
		Label( box, "Box Sweep" );

		// The same ray as the middle row's, drawn over everything: its hit
		// point is a whole square rather than the half the floor leaves.
		var overlay = At( 5, 5 );
		DebugOverlay.Trace( Down( Scene.Trace.Ray( overlay + Vector3.Up * 0.8f, overlay + Vector3.Down * 6.0f ) ), overlay: true );
		Label( overlay, "Overlay Trace" );

		// Column 6 is drawn from OnPreRender.
		Label( At( 5, 6 ), "PreRender" );
	}

	/// <summary>
	/// A dim box around the gallery and the player, and a line past the
	/// player's shoulder: geometry that crosses the near plane, which is
	/// where clipping goes wrong.
	/// </summary>
	void Surroundings()
	{
		var dim = Color.White.WithAlpha( 0.15f );

		DebugOverlay.Box( new BBox( WorldPosition + new Vector3( -1.0f, -0.4f, -RowSpacing * 6.0f ), WorldPosition + new Vector3( Spacing * 7.0f, 7.0f, 12.0f ) ), dim );

		var beside = WorldPosition + WorldRotation.Right * ( Spacing * 3.0f + 0.4f ) + Vector3.Up * 1.5f;
		DebugOverlay.Line( beside + WorldRotation.Backward * 30.0f, beside + WorldRotation.Forward * 30.0f, dim );
	}

	/// <summary>
	/// The draws that are in the pixels of the screen rather than the world,
	/// down the left edge under the hint panel, where no world exhibit stands.
	/// </summary>
	/// <remarks>
	/// Measured from the top left rather than the bottom right: what
	/// <c>Screen.Size</c> says is the window, and a view that is not the window
	/// - a screenshot, a smaller viewport - would put anything hung off the far
	/// edges out of its own frame.
	/// </remarks>
	void ScreenEdge()
	{
		DebugOverlay.ScreenText( new Vector2( 130, 150 ), "DebugOverlay.ScreenText", size: 18, flags: TextFlag.Center );
		DebugOverlay.ScreenText( new Vector2( 24, 170 ), "left top\nsecond line", size: 14, flags: TextFlag.LeftTop, color: Color.Cyan );

		// On for half a second in every second: a timed screen label.
		if ( sinceBlink > 1.0f ) sinceBlink = 0;
		if ( sinceBlink < 0.05f )
			DebugOverlay.ScreenText( new Vector2( 130, 215 ), "blink (0.5s)", size: 14, color: Color.Yellow, duration: 0.5f );

		if ( !pictureLooked )
		{
			pictureLooked = true;
			picture = Texture.Load( "textures/fx/ring.png" );
		}

		if ( picture is null || !picture.IsValid )
		{
			DebugOverlay.ScreenText( new Vector2( 72, 250 ), "Texture (missing)", size: 14, color: Color.Red );
			return;
		}

		DebugOverlay.ScreenText( new Vector2( 130, 250 ), "Texture: rect / at / shader", size: 14 );
		DebugOverlay.Texture( picture, new Rect( 24, 270, 64, 64 ), Color.Cyan );
		DebugOverlay.Texture( picture, new Vector2( 100, 270 ), Color.Orange.WithAlpha( 0.5f ) );
		DebugOverlay.Texture( new Vector2( 176, 270 ), picture, new Vector2( 64, 64 ) );

		// A picture pinned to a world point: it should hang over the front row's
		// text and stay there as the camera moves.
		DebugOverlay.ScreenTexture( At( 0, 3 ) + Vector3.Up * 1.3f, picture, new Vector2( 48, 48 ) );
	}

	void Label( Vector3 pos, string text )
	{
		DebugOverlay.Text( pos + Vector3.Down * 0.15f, text, size: 16, color: Color.White.WithAlpha( 0.85f ) );
	}
}
