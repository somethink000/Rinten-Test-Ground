namespace TestGround;

/// <summary>
/// Carries a game object round a centre on a circle - a planet round its
/// star. Tilted, with a period, and a phase so two on one orbit are apart.
/// </summary>
/// <remarks>
/// Runs in the editor too: the effects riding it are previewed there, and a
/// planet that does not move shows nothing of its moons' motion.
/// </remarks>
[Title( "Orbit" )]
[Category( "Test Ground" )]
[Icon( "public" )]
public sealed class Orbit : Component, Component.ExecuteInEditor
{
	/// <summary>The object orbited, or the parent where none is given.</summary>
	[Property] public GameObject Centre { get; set; }

	/// <summary>Metres from the centre.</summary>
	[Property] public float Radius { get; set; } = 10.0f;

	/// <summary>Seconds for one lap. Negative goes the other way.</summary>
	[Property] public float Period { get; set; } = 60.0f;

	/// <summary>Degrees the orbit's plane is tilted from flat.</summary>
	[Property] public float Tilt { get; set; } = 0.0f;

	/// <summary>Where on the lap this starts, nought to one.</summary>
	[Property, Range( 0.0f, 1.0f )] public float Phase { get; set; }

	protected override void OnUpdate()
	{
		var period = Period == 0.0f ? 60.0f : Period;
		var t = ( SolarClock.Now / period + Phase ) * 6.2831853f;
		var flat = new Vector3( System.MathF.Cos( t ) * Radius, 0.0f, System.MathF.Sin( t ) * Radius );
		var tilted = Rotation.FromAxis( Vector3.Right, Tilt ) * flat;
		var origin = Centre.IsValid() ? Centre.WorldPosition : ( GameObject.Parent?.WorldPosition ?? Vector3.Zero );

		WorldPosition = origin + tilted;
	}
}
