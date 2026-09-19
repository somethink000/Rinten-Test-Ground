namespace TestGround;

/// <summary>
/// Draws one of each debug overlay primitive in rows, so a broken overlay
/// is a missing shape rather than a silent one.
/// </summary>
/// <remarks>
/// The front row is the plain shapes. The row behind it is the composite ones
/// - capsules, a cone, a frustum, a trace. The back row is the ways of drawing
/// rather than the shapes: from the fixed step, with a lifetime, through a
/// solid, a model, a copy of an object. The screen-space draws sit along the
/// bottom edge of the view, where nothing in the world can be mistaken for
/// them.
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
	[Property] public float RowRise { get; set; } = 1.0f;

	/// <summary>
	/// An object whose renderers are drawn again as an overlay, tinted, in the
	/// back row. Leave the object itself disabled so only the copy is seen.
	/// </summary>
	[Property] public GameObject Ghost { get; set; }

	/// <summary>Seconds the timed exhibit lives, and how often a new one is made.</summary>
	const float TimedLife = 3.0f;

	TimeSince sinceTimed = 999.0f;

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
		ScreenEdge();
	}

	/// <summary>
	/// The fixed step keeps its own list of single-frame overlays, emptied at
	/// the start of every fixed update rather than every frame. A shape drawn
	/// from here that flickers is that list being cleared by the wrong stage.
	/// </summary>
	protected override void OnFixedUpdate()
	{
		var fixedBox = At( 2, 4 );
		DebugOverlay.Box( BBox.FromPositionAndSize( fixedBox + Vector3.Up * 0.4f, 0.5f ), Color.Yellow );
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
		var points = new Vector3[13];
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

		// Straight down into the floor: white ray, red hit, red normal.
		var trace = At( 1, 6 );
		var hit = Scene.Trace.Ray( trace + Vector3.Up * 0.8f, trace + Vector3.Down * 0.5f )
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
		// copy is sized here rather than on the object.
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

		// A box swept sideways along the row: drawn where it started, in red,
		// and where it stopped, in green.
		var sweep = At( 2, 6 );
		var from = sweep + Vector3.Up * 0.4f + WorldRotation.Left * 0.5f;
		var to = sweep + Vector3.Up * 0.4f + WorldRotation.Right * 0.5f;
		var swept = Scene.Trace.Box( BBox.FromPositionAndSize( 0, 0.3f ), from, to )
			.IgnoreGameObjectHierarchy( GameObject )
			.Run();
		DebugOverlay.Trace( swept );
		Label( sweep, "Box Sweep" );
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

		if ( !pictureLooked )
		{
			pictureLooked = true;
			picture = Texture.Load( "textures/fx/ring.png" );
		}

		if ( picture is null || !picture.IsValid )
		{
			DebugOverlay.ScreenText( new Vector2( 72, 190 ), "Texture (missing)", size: 14, color: Color.Red );
			return;
		}

		DebugOverlay.ScreenText( new Vector2( 72, 190 ), "Texture", size: 14 );
		DebugOverlay.Texture( picture, new Rect( 24, 210, 96, 96 ), Color.Cyan );

		// A picture pinned to a world point: it should hang over the front row's
		// text and stay there as the camera moves.
		DebugOverlay.ScreenTexture( At( 0, 3 ) + Vector3.Up * 1.3f, picture, new Vector2( 48, 48 ) );
	}

	void Label( Vector3 pos, string text )
	{
		DebugOverlay.Text( pos + Vector3.Down * 0.15f, text, size: 16, color: Color.White.WithAlpha( 0.85f ) );
	}
}
