namespace TestGround;

/// <summary>
/// Draws one of each debug overlay primitive in a row, so a broken overlay
/// is a missing shape rather than a silent one.
/// </summary>
[Title( "Overlay Gallery" )]
[Category( "Test Ground" )]
[Icon( "square_foot" )]
public sealed class OverlayGallery : Component, Component.ExecuteInEditor
{
	/// <summary>Metres between exhibits.</summary>
	[Property] public float Spacing { get; set; } = 1.6f;

	protected override void OnUpdate()
	{
		var origin = WorldPosition + Vector3.Up * 1.2f;
		var step = WorldRotation.Right * Spacing;
		var i = 0;

		void Next( out Vector3 pos )
		{
			pos = origin + step * i;
			i++;
		}

		Next( out var line );
		DebugOverlay.Line( line, line + Vector3.Up * 0.8f, Color.White );
		Label( line, "Line" );

		Next( out var timed );
		DebugOverlay.Line( timed, timed + Vector3.Up * 0.8f + WorldRotation.Right * 0.2f, Color.White * System.Random.Shared.Float( 0.5f, 1.0f ), duration: 1.0f );
		Label( timed, "1s Line" );

		Next( out var overlay );
		DebugOverlay.Line( overlay, overlay + Vector3.Up * 0.8f, Color.Green, overlay: true );
		Label( overlay, "Overlay" );

		Next( out var text );
		DebugOverlay.Text( text + Vector3.Up * 0.4f, "Hello", size: 28 );
		Label( text, "Text" );

		Next( out var sphere );
		DebugOverlay.Sphere( new Sphere( sphere + Vector3.Up * 0.4f, 0.3f ), Color.Cyan );
		Label( sphere, "Sphere" );

		Next( out var box );
		DebugOverlay.Box( BBox.FromPositionAndSize( box + Vector3.Up * 0.4f, 0.5f ), Color.Orange );
		Label( box, "Box" );

		Next( out var spin );
		var spinTx = new Transform( spin + Vector3.Up * 0.4f, new Angles( Time.Now * 90.0f, Time.Now * 120.0f, 0 ) );
		DebugOverlay.Box( BBox.FromPositionAndSize( 0, 0.45f ), Color.Magenta, transform: spinTx );
		Label( spin, "Rotated Box" );
	}

	void Label( Vector3 pos, string text )
	{
		DebugOverlay.Text( pos + Vector3.Down * 0.15f, text, size: 16, color: Color.White.WithAlpha( 0.85f ) );
	}
}
