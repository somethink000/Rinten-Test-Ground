namespace TestGround;

/// <summary>
/// Plays the model's clips one after another, straight off the sequence
/// accessor, and says which one is up.
/// </summary>
/// <remarks>
/// The path a game takes when it has no graph: name a clip, let it run, name
/// the next. Setting <see cref="SkinnedModelRenderer.SequenceAccessor.Name"/>
/// turns the graph off by itself, which is worth seeing on its own - a
/// character standing in its bind pose is nearly always a clip name nothing
/// matched, and the label beside this one says which name was asked for.
/// </remarks>
[Title( "Clip Rack" )]
[Category( "Test Ground" )]
[Icon( "playlist_play" )]
public sealed class ClipRack : Component
{
	/// <summary>Which character this drives. Itself, where nothing is given.</summary>
	[Property] public SkinnedModelRenderer Renderer { get; set; }

	/// <summary>
	/// The clips to walk through, or nothing for every clip the model carries.
	/// </summary>
	[Property] public List<string> Clips { get; set; } = new();

	/// <summary>How long each one is left running.</summary>
	[Property] public float Seconds { get; set; } = 3.0f;

	/// <summary>Stay on one clip instead of moving on.</summary>
	[Property] public bool Hold { get; set; }

	/// <summary>The sign this writes what is playing onto, if there is one.</summary>
	[Property] public TextRenderer Sign { get; set; }

	/// <summary>What is playing, for anything else that wants to say so.</summary>
	public string Current { get; private set; } = "";

	TimeSince since;
	int at;

	SkinnedModelRenderer Target => Renderer ?? GameObject.GetComponent<SkinnedModelRenderer>();

	protected override void OnStart()
	{
		since = 0;
		Play( 0 );
	}

	protected override void OnUpdate()
	{
		var names = Names();
		if ( names.Count == 0 ) return;

		if ( !Hold && Seconds > 0.0f && since >= Seconds )
		{
			since = 0;
			Play( ( at + 1 ) % names.Count );
		}

		Write();
	}

	/// <summary>The clips asked for, or the model's own list.</summary>
	IReadOnlyList<string> Names()
	{
		if ( Clips is { Count: > 0 } ) return Clips;

		var renderer = Target;

		return renderer?.Model.IsValid() == true
			? renderer.Model.AnimationNames
			: System.Array.Empty<string>();
	}

	void Play( int index )
	{
		var names = Names();
		if ( names.Count == 0 ) return;

		at = index % names.Count;

		var renderer = Target;
		if ( !renderer.IsValid() ) return;

		Current = names[at];

		renderer.UseAnimGraph = false;
		renderer.Sequence.Looping = true;
		renderer.Sequence.Name = Current;
	}

	void Write()
	{
		if ( !Sign.IsValid() ) return;

		var renderer = Target;
		var time = renderer.IsValid() && !renderer.UseAnimGraph ? renderer.Sequence.TimeNormalized : 0.0f;

		Sign.Text = $"{Current}\n{time * 100.0f:0}%";
	}
}
