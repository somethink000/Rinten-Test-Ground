namespace TestGround;

/// <summary>
/// Puts a test scene one key away from the menu. Drop this on any scene you add
/// to the test ground.
/// </summary>
[Title( "Return To Menu" )]
[Category( "Test Ground" )]
[Icon( "keyboard_return" )]
public sealed class ReturnToMenu : Component
{
	/// <summary>
	/// The key that goes back. Raw keyboard rather than an input action, so a
	/// scene doesn't have to bind anything to take part.
	/// </summary>
	[Property] public string Key { get; set; } = "Q";

	/// <summary>
	/// Where back is. Leave this empty for <see cref="SceneNavigator.MenuScenePath"/>.
	/// </summary>
	[Property] public SceneFile MenuScene { get; set; }

	protected override void OnUpdate()
	{
		if ( Input.Keyboard.Pressed( Key ) )
		{
			SceneNavigator.GoToMenu( MenuScene );
		}

		SceneNavigator.Flush( Scene );
	}
}
