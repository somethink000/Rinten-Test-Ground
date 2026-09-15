namespace TestGround;

/// <summary>
/// Walks a <see cref="CharacterController"/> with the move keys, looks with the
/// mouse, jumps, and puts you back if you fall off. The fly camera is for
/// looking; this is for asking whether steps, slopes and gaps work.
/// </summary>
[Title( "Walker" )]
[Category( "Test Ground" )]
[Icon( "directions_walk" )]
public sealed class Walker : Component
{
	[Property] public CharacterController Controller { get; set; }
	[Property] public CameraComponent Camera { get; set; }

	/// <summary>Metres a second on the ground.</summary>
	[Property, Category( "Movement" )] public float Speed { get; set; } = 4.5f;

	/// <summary>What holding Run multiplies that by.</summary>
	[Property, Category( "Movement" )] public float RunScale { get; set; } = 1.8f;

	/// <summary>Upward punch of a jump, in metres a second.</summary>
	[Property, Category( "Movement" )] public float Jump { get; set; } = 5.5f;

	/// <summary>How hard the ground pulls, in metres a second squared.</summary>
	[Property, Category( "Movement" )] public float Gravity { get; set; } = 16.0f;

	/// <summary>How quickly the walk comes to a stop.</summary>
	[Property, Category( "Movement" )] public float Friction { get; set; } = 6.0f;

	/// <summary>How much of the wish you still get while in the air.</summary>
	[Property, Category( "Movement" ), Range( 0.0f, 1.0f )] public float AirControl { get; set; } = 0.35f;

	/// <summary>How far up the camera sits from the feet, in metres.</summary>
	[Property, Category( "Movement" )] public float EyeHeight { get; set; } = 1.5f;

	[Property, Range( 0, 90 ), Category( "Movement" )] public float PitchClamp { get; set; } = 89.0f;

	/// <summary>Below this height the walk starts again.</summary>
	[Property] public float FallHeight { get; set; } = -4.0f;

	Angles look;
	bool jump;
	Vector3 spawn;

	protected override void OnStart()
	{
		spawn = WorldPosition;
		if ( Camera.IsValid() )
			look = Camera.GameObject.LocalRotation.Angles();
	}

	protected override void OnUpdate()
	{
		if ( Camera.IsValid() )
		{
			look += Input.AnalogLook;
			look.pitch = look.pitch.Clamp( -PitchClamp, PitchClamp );
			look.roll = 0.0f;
			Camera.GameObject.LocalPosition = Vector3.Up * EyeHeight;
			Camera.GameObject.LocalRotation = look.ToRotation();
		}

		if ( Input.Pressed( "Jump" ) )
			jump = true;

		SceneNavigator.Flush( Scene );
	}

	protected override void OnFixedUpdate()
	{
		if ( !Controller.IsValid() ) return;

		if ( WorldPosition.y < FallHeight )
		{
			WorldPosition = spawn;
			Controller.Velocity = 0;
			jump = false;
			return;
		}

		var speed = Input.Down( "Run" ) ? Speed * RunScale : Speed;
		var wish = (Rotation.FromYaw( look.yaw ) * Input.AnalogMove.WithY( 0 )).ClampLength( 1.0f ) * speed;

		if ( Controller.IsOnGround )
		{
			Controller.ApplyFriction( Friction );
			Controller.Accelerate( wish );

			if ( jump )
				Controller.Punch( Vector3.Up * Jump );
		}
		else
		{
			Controller.Velocity += Vector3.Down * Gravity * Time.Delta;
			Controller.Accelerate( wish * AirControl );
		}

		jump = false;
		Controller.Move();
	}
}
