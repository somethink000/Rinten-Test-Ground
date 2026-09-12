namespace Template;


public sealed partial class Player : Component
{
    [Property, Category( "Relatives" )] public CameraComponent Camera { get; set; }


	// Metres a second.
	[Property, Category( "Movement" )] public float Speed { get; set; } = 5.0f;

	// What holding Run multiplies that by.
	[Property, Category( "Movement" )] public float RunScale { get; set; } = 3.0f;

	// How far up and down you can look, in degrees.
	[Property, Range( 0, 90 ), Category( "Movement" )] public float PitchClamp { get; set; } = 90f;

	
	private Angles look;

	/// <summary>Held still: no looking, no moving - while a sheet has the mouse or something else has the camera.</summary>
	public bool Frozen { get; set; }

	/// <summary>Face this way, as if the mouse had been dragged there - so a hand-placed camera does not snap back.</summary>
	public void Face( Rotation rotation ) => look = rotation.Angles();



	protected override void OnStart()
	{
		look = Camera.GameObject.WorldRotation.Angles();
	}



	protected override void OnUpdate()
	{
		if ( Frozen ) return;

		look += Input.AnalogLook;
		look.pitch = look.pitch.Clamp( -PitchClamp, PitchClamp );
		look.roll = 0.0f;

		var rotation = look.ToRotation();

		var move = rotation * Input.AnalogMove;

		if ( Input.Down( "Jump" ) ) move += Vector3.Up;
		if ( Input.Down( "Duck" ) ) move += Vector3.Down;

		var speed = Input.Down( "Run" ) ? Speed * RunScale : Speed;

		Camera.GameObject.WorldRotation = rotation;

		WorldPosition += move.ClampLength( 1.0f ) * speed * Time.Delta;
	}
}
