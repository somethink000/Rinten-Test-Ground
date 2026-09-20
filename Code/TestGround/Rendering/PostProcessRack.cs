namespace TestGround;

/// <summary>
/// Turns the post-process effects on the camera on and off with the number
/// keys, so a gallery is something you can isolate rather than a soup.
/// </summary>
[Title( "Post Process Rack" )]
[Category( "Test Ground" )]
[Icon( "movie_filter" )]
public sealed class PostProcessRack : Component
{
	/// <summary>Whose effects to toggle. The scene camera where none is set.</summary>
	[Property] public CameraComponent Camera { get; set; }

	const int Slots = 8;

	protected override void OnStart()
	{
		foreach ( var effect in Effects() )
			effect.Enabled = false;
	}

	protected override void OnUpdate()
	{
		var list = Effects();
		for ( var i = 0; i < list.Count && i < Slots; i++ )
		{
			if ( Input.Pressed( $"Slot{i + 1}" ) )
				list[i].Enabled = !list[i].Enabled;
		}

		Draw();
		SceneNavigator.Flush( Scene );
	}

	List<BasePostProcess> Effects()
	{
		var camera = Camera.IsValid() ? Camera : Scene.Camera;
		if ( !camera.IsValid() ) return new();

		return camera.GameObject.GetComponents<BasePostProcess>( includeDisabled: true ).ToList();
	}

	void Draw()
	{
		var list = Effects();
		if ( list.Count == 0 ) return;

		var lines = new System.Text.StringBuilder();
		for ( var i = 0; i < list.Count && i < Slots; i++ )
		{
			var on = list[i].Enabled ? "on" : "off";
			lines.Append( i + 1 );
			lines.Append( "  " );
			lines.Append( list[i].GetType().Name );
			lines.Append( "  " );
			lines.Append( on );
			if ( i < list.Count - 1 ) lines.Append( '\n' );
		}

		DebugOverlay.ScreenText( new Vector2( 24, 96 ), lines.ToString(), 16, TextFlag.LeftTop, Color.White );
	}
}
