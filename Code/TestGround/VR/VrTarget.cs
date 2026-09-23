namespace TestGround;

/// <summary>
/// An archery target: scores where an arrow went in, by how far from the centre
/// of its face that is, and says so over the hit for a few seconds.
/// </summary>
/// <remarks>
/// The face is the model's local XY plane, looking along +Z, its centre the
/// origin - see tools/archery/build_archery.py and its rings.json, which these
/// radii are.
/// </remarks>
[Title( "VR Target" )]
[Category( "Test Ground" )]
[Icon( "adjust" )]
public sealed class VrTarget : Component
{
	/// <summary>The outer radius of each ring, from the ten out to the five.</summary>
	[Property] public List<float> Rings { get; set; } = new() { 0.0667f, 0.1333f, 0.2f, 0.2667f, 0.3333f, 0.4f };

	/// <summary>The inner ten, which a tie is broken on.</summary>
	[Property] public float InnerTen { get; set; } = 0.0333f;

	[Property] public float ShowFor { get; set; } = 4.0f;

	/// <summary>The last score, and the total since the scene started.</summary>
	public int LastScore { get; private set; }
	public int Total { get; private set; }

	/// <summary>Ten for the middle down to five for the edge; nought off the face.</summary>
	public int Score( Vector3 world )
	{
		var local = WorldTransform.PointToLocal( world );
		var radius = new Vector2( local.x, local.y ).Length;

		for ( var i = 0; i < Rings.Count; i++ )
			if ( radius <= Rings[i] ) return 10 - i;

		return 0;
	}

	/// <summary>An arrow went in here - counted only on the face, not the rim, back or post.</summary>
	public void Hit( Vector3 world )
	{
		if ( System.MathF.Abs( WorldTransform.PointToLocal( world ).z ) > 0.02f ) return;

		LastScore = Score( world );
		Total += LastScore;

		var local = WorldTransform.PointToLocal( world );
		var inner = new Vector2( local.x, local.y ).Length <= InnerTen;
		var text = LastScore == 0 ? "miss" : inner ? "X" : LastScore.ToString();

		DebugOverlay.Text( world + WorldRotation.Forward * -0.05f + Vector3.Up * 0.08f, text, 48,
			TextFlag.Center, LastScore >= 9 ? Color.Yellow : Color.White, ShowFor );
	}
}
