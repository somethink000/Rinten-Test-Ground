namespace TestGround;

/// <summary>
/// Carries the object by whatever travel the clip had taken off it, and turns
/// it round at the end of its run.
/// </summary>
/// <remarks>
/// The walk and the run in <c>mannequin.mdl</c> are drawn travelling forwards
/// and have that travel lifted by <c>MotionBone</c>, so the clip plays on the
/// spot and the distance it would have covered comes out of
/// <see cref="SkinnedModelRenderer.RootMotion"/> instead. This is the other
/// half: something that puts it back.
/// <para>
/// It is worth a station of its own because the two halves fail separately.
/// A clip that kept its travel walks out of the character; a clip that lost it
/// with nothing reading the motion slides along the floor with its feet turning
/// underneath.
/// </para>
/// </remarks>
[Title( "Root Motion Mover" )]
[Category( "Test Ground" )]
[Icon( "directions_walk" )]
public sealed class RootMotionMover : Component
{
	/// <summary>The character whose motion is read. Itself, where nothing is given.</summary>
	[Property] public SkinnedModelRenderer Renderer { get; set; }

	/// <summary>How far it may get from where it started before turning back.</summary>
	[Property] public float Run { get; set; } = 4.0f;

	/// <summary>Ignore the clip's motion and stand still, for comparing the two.</summary>
	[Property] public bool Frozen { get; set; }

	/// <summary>How far it has travelled since it last turned, for a sign to read.</summary>
	public float Travelled { get; private set; }

	/// <summary>The sign this writes onto, if there is one.</summary>
	[Property] public TextRenderer Sign { get; set; }

	SkinnedModelRenderer Target => Renderer ?? GameObject.GetComponent<SkinnedModelRenderer>();

	protected override void OnUpdate()
	{
		var renderer = Target;
		if ( !renderer.IsValid() ) return;

		if ( !Frozen )
		{
			// The motion is in the character's own space: it walks along its
			// own forward, whichever way that has been turned to face.
			var step = renderer.RootMotion;

			WorldPosition += WorldRotation * step.Position;
			Travelled += step.Position.Length;
		}

		// Turned on distance covered rather than on where it has got to: the
		// clip is what carries it, so the clip is what the run is measured in.
		if ( Travelled > Run )
		{
			WorldRotation *= Rotation.FromYaw( 180.0f );
			Travelled = 0.0f;
		}

		if ( Sign.IsValid() )
			Sign.Text = Frozen ? "root motion off" : $"root motion\n{Travelled:0.0} m";
	}
}
