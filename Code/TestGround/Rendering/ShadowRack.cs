namespace TestGround;

/// <summary>
/// The sun's shadow settings on the number keys, since a scene has one sun
/// and the settings on it are the ones that cannot be a station each: whether
/// it casts at all, how fine its pages are, how wide the source is, and the
/// time of day. What is set is written on the screen.
/// </summary>
[Title( "Shadow Rack" )]
[Category( "Test Ground" )]
[Icon( "wb_shade" )]
public sealed class ShadowRack : Component
{
	/// <summary>The sun. Empty finds the scene's directional light.</summary>
	[Property] public DirectionalLight Sun { get; set; }

	/// <summary>Degrees the sun turns a second while the day runs.</summary>
	[Property] public float DaySpeed { get; set; } = 6.0f;

	static readonly float[] Details = { 16.0f, 64.0f, 256.0f };
	static readonly float[] Radii = { 0.0f, 0.05f, 0.5f, 2.0f };

	int detail = 1;
	int radius = 1;
	bool day;
	Rotation dawn;

	DirectionalLight Light => Sun.IsValid() ? Sun : Scene.GetAllComponents<DirectionalLight>().FirstOrDefault();

	protected override void OnStart()
	{
		var sun = Light;
		if ( sun.IsValid() ) dawn = sun.WorldRotation;
	}

	protected override void OnUpdate()
	{
		var sun = Light;
		if ( !sun.IsValid() ) return;

		if ( Input.Pressed( "Slot1" ) ) sun.Shadows = !sun.Shadows;
		if ( Input.Pressed( "Slot2" ) ) { detail = ( detail + 1 ) % Details.Length; sun.ShadowDetail = Details[detail]; }
		if ( Input.Pressed( "Slot3" ) ) { radius = ( radius + 1 ) % Radii.Length; sun.SourceRadius = Radii[radius]; }
		if ( Input.Pressed( "Slot4" ) ) day = !day;
		if ( Input.Pressed( "Slot5" ) ) { day = false; sun.WorldRotation = dawn; }

		if ( day )
		{
			// Round the east-west axis, so noon is overhead and the shadows
			// swing from one side to the other.
			sun.WorldRotation = Rotation.FromAxis( Vector3.Right, DaySpeed * Time.Delta ) * sun.WorldRotation;
		}

		var lines = $"1  shadows  {( sun.Shadows ? "on" : "off" )}\n" +
			$"2  detail  {sun.ShadowDetail:0} texels/m\n" +
			$"3  source radius  {sun.SourceRadius:0.00}\n" +
			$"4  day  {( day ? "running" : "stopped" )}\n" +
			$"5  back to dawn\n" +
			$"sun  {sun.WorldRotation.Angles().pitch:0}° pitch";

		DebugOverlay.ScreenText( new Vector2( 24, 96 ), lines, 16, TextFlag.LeftTop, Color.White );
	}
}
