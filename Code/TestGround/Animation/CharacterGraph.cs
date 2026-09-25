namespace TestGround;

/// <summary>
/// Builds an animation graph in code and hands it to the character beside it -
/// a locomotion blend driven by a speed, inside a state machine that crosses
/// to a wave and back.
/// </summary>
/// <remarks>
/// A graph is usually drawn in the model editor and kept in the .mdl. Nothing
/// says it has to be: <see cref="AnimGraph.Builder"/> is the same description
/// the editor writes, so a game can assemble one and set it on a renderer. That
/// is what is worth having in a test ground - the graph the scene plays is
/// twenty readable lines rather than a document nobody can diff.
/// <para>
/// What it shows, in order: a blend space over three clips, a state machine,
/// a transition with a duration, and parameters set by name from a game.
/// </para>
/// </remarks>
[Title( "Character Graph" )]
[Category( "Test Ground" )]
[Icon( "account_tree" )]
public sealed class CharacterGraph : Component
{
	/// <summary>The character this animates. Itself, where nothing is given.</summary>
	[Property] public SkinnedModelRenderer Renderer { get; set; }

	/// <summary>How fast it is told it is going, at the top of the sweep.</summary>
	[Property] public float TopSpeed { get; set; } = 5.5f;

	/// <summary>Seconds for a whole sweep from standing to running and back.</summary>
	[Property] public float Sweep { get; set; } = 9.0f;

	/// <summary>Seconds between waves, or nought for none.</summary>
	[Property] public float WaveEvery { get; set; } = 0.0f;

	/// <summary>How long a wave is asked for.</summary>
	[Property] public float WaveFor { get; set; } = 2.2f;

	/// <summary>The sign this writes the parameters onto, if there is one.</summary>
	[Property] public TextRenderer Sign { get; set; }

	/// <summary>What the graph is being told, for anything that wants to say so.</summary>
	public float Speed { get; private set; }

	public bool Waving { get; private set; }

	TimeSince since;
	TimeSince sinceWave;
	AnimGraph graph;

	SkinnedModelRenderer Target => Renderer ?? GameObject.GetComponent<SkinnedModelRenderer>();

	protected override void OnStart()
	{
		since = 0;
		sinceWave = 0;

		var renderer = Target;
		if ( !renderer.IsValid() || !renderer.Model.IsValid() ) return;

		graph = Build( renderer.Model.Name );

		renderer.UseAnimGraph = true;
		renderer.AnimGraph = graph;
	}

	/// <summary>
	/// idle -> walk -> run on one number, and a wave laid beside it.
	/// </summary>
	static AnimGraph Build( string skeleton )
	{
		var builder = AnimGraph.Builder;
		builder.Skeleton = skeleton;

		var speed = builder.FloatParameter( "speed", 0.0f, 8.0f );
		var wave = builder.BoolParameter( "wave" );

		var looping = new AnimGraphBuilder.ClipSettings { Looping = true };

		// One axis, three clips, and where each sits on it. Between the stops
		// the graph blends, so there is no step from a walk into a run.
		var locomotion = builder.BlendSpace( speed,
			new[]
			{
				builder.Clip( "idle", looping ),
				builder.Clip( "walk", looping ),
				builder.Clip( "run", looping ),
			},
			new[] { 0.0f, 1.6f, 5.5f }, looping: true, synchronized: true );

		var waving = builder.Clip( "wave", looping );

		var machine = builder.StateMachine();

		var moving = machine.AddState( locomotion );
		var hello = machine.AddState( waving );

		// Both ways, so the wave is entered and left on the one parameter.
		machine.AddTransition( moving, hello,
			machine.CreateTransition( hello, new AnimGraphBuilder.TransitionSettings { Duration = 0.25f } ),
			new AnimGraphBuilder.StateMachineBuilder.TransitionRouteSettings { Condition = wave } );

		machine.AddTransition( hello, moving,
			machine.CreateTransition( moving, new AnimGraphBuilder.TransitionSettings { Duration = 0.35f } ),
			new AnimGraphBuilder.StateMachineBuilder.TransitionRouteSettings { Condition = builder.Not( wave ) } );

		machine.SetDefaultState( moving );

		return builder.Create( machine, "test ground locomotion" );
	}

	protected override void OnUpdate()
	{
		var renderer = Target;
		if ( !renderer.IsValid() || graph is null ) return;

		if ( Sweep > 0.0f )
		{
			// A triangle rather than a sine, so the character spends time at
			// every speed between the two ends instead of racing through them.
			var t = ( since % Sweep ) / Sweep;
			Speed = TopSpeed * ( 1.0f - System.MathF.Abs( t * 2.0f - 1.0f ) );
		}

		if ( WaveEvery > 0.0f )
		{
			var period = WaveEvery + WaveFor;
			Waving = sinceWave % period >= WaveEvery;
		}

		renderer.Set( "speed", Speed );
		renderer.Set( "wave", Waving );

		if ( Sign.IsValid() )
			Sign.Text = $"speed {Speed:0.0}\nwave {( Waving ? "on" : "off" )}";
	}
}
