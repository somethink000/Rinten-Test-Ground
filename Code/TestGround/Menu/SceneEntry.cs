namespace TestGround;

/// <summary>
/// How a test scene is filed in the main menu. Purely a label - it groups the
/// cards and gives the filter row something to filter by.
/// </summary>
public enum SceneCategory
{
	[Icon( "science" )] General,
	[Icon( "sports_volleyball" )] Physics,
	[Icon( "palette" )] Rendering,
	[Icon( "auto_awesome" )] FX,
	[Icon( "widgets" )] Interface,
	[Icon( "volume_up" )] Audio,
	[Icon( "hub" )] Networking,
	[Icon( "construction" )] Scratch,
}

/// <summary>
/// One scene in the menu's list. Drop a .scene on <see cref="Scene"/>, give it a
/// name and file it under a <see cref="Category"/>.
/// </summary>
/// <remarks>
/// A struct rather than a class so that the inspector's + button gives you a
/// filled-in row to edit: the list control only news up an entry for value types,
/// and a list of nulls is not something you can classify.
/// </remarks>
public record struct SceneEntry()
{
	/// <summary>The scene this card opens.</summary>
	[Property, KeyProperty] public SceneFile Scene { get; set; }

	/// <summary>What the card calls it. Falls back to the file name.</summary>
	[Property, KeyProperty] public string Title { get; set; }

	/// <summary>Which group the card is filed under.</summary>
	[Property, KeyProperty] public SceneCategory Category { get; set; }

	/// <summary>A line under the title saying what the scene is for.</summary>
	[Property, TextArea] public string Description { get; set; }

	/// <summary>The title, or the scene's own name where no title was given.</summary>
	public readonly string DisplayName
	{
		get
		{
			if ( !string.IsNullOrWhiteSpace( Title ) )
				return Title;

			if ( Scene is null )
				return "(no scene)";

			return string.IsNullOrWhiteSpace( Scene.ResourceName ) ? Scene.ResourcePath : Scene.ResourceName;
		}
	}
}
