namespace TestGround;

/// <summary>
/// Holds a dynamic body in front of the camera while a key is down, and
/// lets go when it is not. A physics scene you can only look at is a
/// picture; this makes it a sandbox.
/// </summary>
[Title( "Grabber" )]
[Category( "Test Ground" )]
[Icon( "pan_tool" )]
public sealed class Grabber : Component
{
	/// <summary>The key that holds. Release lets go.</summary>
	[Property, InputAction] public string Action { get; set; } = "Attack1";

	/// <summary>How far the grab ray reaches, in metres.</summary>
	[Property] public float Reach { get; set; } = 8.0f;

	/// <summary>
	/// How loosely the body follows. One is glued; higher is a heavier lag.
	/// </summary>
	[Property, Range( 1.0f, 16.0f )] public float Smoothness { get; set; } = 4.0f;

	PhysicsBody grabbed;
	Transform offset;
	Vector3 localHit;

	protected override void OnUpdate()
	{
		var camera = Scene.Camera;
		if ( !camera.IsValid() ) return;

		if ( grabbed.IsValid() )
		{
			if ( !Input.Down( Action ) )
			{
				grabbed = null;
				return;
			}

			DrawTether( camera );
			return;
		}

		if ( !Input.Pressed( Action ) ) return;

		var start = camera.WorldPosition;
		var end = start + camera.WorldRotation.Forward * Reach;
		var hit = Scene.Trace.Ray( start, end )
			.IgnoreGameObjectHierarchy( GameObject.Root )
			.Run();

		if ( !hit.Hit || hit.Body is null ) return;
		if ( hit.Body.BodyType != PhysicsBodyType.Dynamic ) return;

		grabbed = hit.Body;
		grabbed.MotionEnabled = true;
		localHit = grabbed.Transform.PointToLocal( hit.EndPosition );
		offset = camera.WorldTransform.ToLocal( grabbed.Transform );
	}

	protected override void OnFixedUpdate()
	{
		if ( !grabbed.IsValid() ) return;
		if ( !Input.Down( Action ) ) return;

		var camera = Scene.Camera;
		if ( !camera.IsValid() ) return;

		var target = camera.WorldTransform.ToWorld( offset );
		var now = grabbed.GetLerpedTransform( Time.Now );
		var from = now.PointToWorld( localHit );
		var to = target.PointToWorld( localHit );
		var delta = to - from;

		grabbed.Velocity = delta * (20.0f / Smoothness);
		grabbed.AngularVelocity = 0;
	}

	void DrawTether( CameraComponent camera )
	{
		if ( !grabbed.IsValid() ) return;

		var from = grabbed.GetLerpedTransform( Time.Now ).PointToWorld( localHit );
		var to = camera.WorldTransform.ToWorld( offset ).PointToWorld( localHit );
		DebugOverlay.Line( from, to, Color.Cyan );
		DebugOverlay.Sphere( new Sphere( from, 0.04f ), Color.Cyan );
	}
}
