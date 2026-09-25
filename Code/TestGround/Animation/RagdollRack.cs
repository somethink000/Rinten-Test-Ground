namespace TestGround;

/// <summary>
/// Drops a character into its ragdoll, shoves it, lets it settle, and stands it
/// back up - over and over, so the whole round trip is on show rather than the
/// one frame a game usually spends on it.
/// </summary>
/// <remarks>
/// The switch is two things at once and both have to happen: the physics
/// bodies are turned on, and the animation is turned off. A ragdoll with the
/// graph still running is a character being posed and shoved by turns, which
/// looks like the joints are broken and is not.
/// <para>
/// Standing back up is the other way about, and needs the renderer told to
/// take its bones back - see <see cref="ModelPhysics.CopyBonesFrom"/> for the
/// case where the pose is kept instead.
/// </para>
/// </remarks>
[Title( "Ragdoll Rack" )]
[Category( "Test Ground" )]
[Icon( "airline_seat_flat" )]
public sealed class RagdollRack : Component
{
	/// <summary>The character. Itself, where nothing is given.</summary>
	[Property] public SkinnedModelRenderer Renderer { get; set; }

	/// <summary>Its bodies. Itself, where nothing is given.</summary>
	[Property] public ModelPhysics Physics { get; set; }

	/// <summary>Seconds it stands and animates before going down.</summary>
	[Property] public float Standing { get; set; } = 3.0f;

	/// <summary>Seconds it lies there before getting up.</summary>
	[Property] public float Down { get; set; } = 5.0f;

	/// <summary>How hard it is shoved as it goes down. Nought just drops it.</summary>
	[Property] public float Shove { get; set; } = 3.0f;

	/// <summary>Which way the shove goes, in this object's own space.</summary>
	[Property] public Vector3 ShoveDirection { get; set; } = new( 0, 0.35f, -1 );

	/// <summary>Stay a ragdoll and never get up.</summary>
	[Property] public bool StayDown { get; set; }

	/// <summary>The sign this writes onto, if there is one.</summary>
	[Property] public TextRenderer Sign { get; set; }

	/// <summary>Whether it is a ragdoll right now.</summary>
	public bool IsRagdoll { get; private set; }

	TimeSince since;
	Transform home;

	SkinnedModelRenderer Character => Renderer ?? GameObject.GetComponent<SkinnedModelRenderer>();
	ModelPhysics Bodies => Physics ?? GameObject.GetComponent<ModelPhysics>();

	protected override void OnStart()
	{
		home = WorldTransform;
		since = 0;

		Animate();
	}

	protected override void OnUpdate()
	{
		if ( IsRagdoll )
		{
			if ( !StayDown && since >= Down ) Animate();
		}
		else if ( since >= Standing )
		{
			Collapse();
		}

		if ( Sign.IsValid() )
			Sign.Text = IsRagdoll ? $"ragdoll\n{Pieces()} bodies" : "animated";
	}

	/// <summary>Bones back under the animation, and the object back where it started.</summary>
	void Animate()
	{
		var character = Character;
		var bodies = Bodies;

		IsRagdoll = false;
		since = 0;

		if ( bodies.IsValid() ) bodies.Enabled = false;

		// The physics drove this object about while it was down, so standing up
		// is also putting it back - otherwise each cycle starts wherever the
		// last one finished and the rack walks out of its own station.
		WorldTransform = home;

		if ( character.IsValid() ) character.UseAnimGraph = true;
	}

	/// <summary>Physics on, animation off, and a push.</summary>
	void Collapse()
	{
		var character = Character;
		var bodies = Bodies;

		IsRagdoll = true;
		since = 0;

		if ( character.IsValid() ) character.UseAnimGraph = false;

		if ( !bodies.IsValid() ) return;

		bodies.Enabled = true;

		if ( Shove <= 0.0f ) return;

		var push = WorldRotation * ShoveDirection.Normal * Shove;

		bodies.PhysicsGroup?.ApplyImpulse( push, withMass: true );
	}

	int Pieces()
	{
		var bodies = Bodies;

		return bodies.IsValid() ? bodies.PhysicsGroup?.BodyCount ?? 0 : 0;
	}
}
