namespace TestGround;

/// <summary>
/// Scene changes for the test ground, deferred by a frame.
/// </summary>
/// <remarks>
/// A button handler runs while the panel that owns it is being ticked, and a
/// scene load deletes that panel along with everything else in the scene. So
/// nothing loads a scene where it is asked for: the request is parked here and
/// <see cref="Flush"/> performs it from a component's update, which is where the
/// engine expects objects to come and go.
/// </remarks>
public static class SceneNavigator
{
	/// <summary>Where <see cref="GoToMenu"/> goes when nothing else is named.</summary>
	public const string MenuScenePath = "scenes/main.scene";

	private static SceneFile pending;

	/// <summary>The scene that will be loaded on the next update, if any.</summary>
	public static SceneFile Pending => pending;

	/// <summary>Ask for a scene. It loads on the next update.</summary>
	public static void Go( SceneFile scene )
	{
		if ( scene is null )
		{
			Log.Warning( "SceneNavigator: asked for a scene that isn't set" );
			return;
		}

		pending = scene;
	}

	/// <summary>Ask for the menu, falling back to <see cref="MenuScenePath"/>.</summary>
	public static void GoToMenu( SceneFile menu = null )
	{
		var scene = menu ?? SceneFile.Load( MenuScenePath );

		if ( scene is null )
		{
			Log.Warning( $"SceneNavigator: no menu scene at {MenuScenePath}" );
			return;
		}

		Go( scene );
	}

	/// <summary>
	/// Perform a parked request. Call this from a component's update - every test
	/// ground component that can ask for a scene also calls this, so whichever one
	/// is alive gets us there.
	/// </summary>
	public static void Flush( Scene scene )
	{
		if ( pending is null ) return;
		if ( !scene.IsValid() ) return;

		var next = pending;
		pending = null;

		scene.Load( next );
	}
}
