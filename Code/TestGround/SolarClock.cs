namespace TestGround;

/// <summary>
/// The system's clock: how fast it runs against real time, how long it has
/// run, and what date that is. Every Orbit reads its time from here, and
/// every effect's Speed parameter follows it, so one number moves the lot.
/// </summary>
[Title( "Solar Clock" )]
[Category( "Test Ground" )]
[Icon( "schedule" )]
public sealed class SolarClock : Component, Component.ExecuteInEditor
{
	/// <summary>How many system seconds pass a real second. Nought is paused.</summary>
	[Property, Range( 0.0f, 500.0f )] public float Scale { get; set; } = 1.0f;

	/// <summary>Seconds of system time one Earth year takes - the Earth's Orbit period.</summary>
	[Property] public float SecondsPerYear { get; set; } = 60.0f;

	/// <summary>The date at time nought.</summary>
	[Property] public string Epoch { get; set; } = "2026-01-01";

	/// <summary>System seconds since the scene started, at the scale it ran at.</summary>
	public float Elapsed { get; private set; }

	public static SolarClock Current { get; private set; }

	/// <summary>The system's own time, for anything that orbits: scaled seconds.</summary>
	public static float Now => Current.IsValid() ? Current.Elapsed : Time.Now;

	/// <summary>The scale everything else multiplies its own speed by.</summary>
	public static float Rate => Current.IsValid() ? Current.Scale : 1.0f;

	/// <summary>Days since the epoch, on the Earth's orbit.</summary>
	public float Days => Elapsed / SecondsPerYear * 365.25f;

	public string DateText
	{
		get
		{
			if ( !System.DateTime.TryParse( Epoch, out var epoch ) ) epoch = new System.DateTime( 2026, 1, 1 );

			return epoch.AddDays( Days ).ToString( "d MMM yyyy" );
		}
	}

	float _applied = -1.0f;

	protected override void OnEnabled()
	{
		Current = this;
		Elapsed = 0.0f;
	}

	protected override void OnUpdate()
	{
		Current = this;
		Elapsed += Time.Delta * Scale;

		if ( Scale == _applied ) return;

		_applied = Scale;

		// Every effect in the scene takes the same Speed, so the moons, the
		// rings, the comet and the probes keep pace with the orbits.
		foreach ( var player in Scene.GetAllComponents<ParticlePlayer>() )
			player.Set( "Speed", Scale );
	}

	/// <summary>The next step up or down the ladder of speeds.</summary>
	public void Step( int direction )
	{
		float[] ladder = { 0.0f, 0.1f, 0.25f, 0.5f, 1.0f, 2.0f, 5.0f, 10.0f, 25.0f, 50.0f, 100.0f };
		var at = 0;

		for ( var i = 0; i < ladder.Length; i++ )
		{
			if ( ladder[i] <= Scale + 1e-4f ) at = i;
		}

		at = System.Math.Clamp( at + direction, 0, ladder.Length - 1 );
		Scale = ladder[at];
	}
}
