namespace TestGround;

/// <summary>
/// Put this on a rigidbody to see what its surface properties are doing. Every
/// contact it starts is logged with the friction on both shapes and what the
/// solver will combine them into; every <see cref="Interval"/> seconds it reports
/// speed against spin, which is the difference between a ball that slides and a
/// ball that rolls; and when it comes to rest it says how long that took and how
/// far it got. Three of these on three ramps with different friction is the
/// friction test.
/// </summary>
[Title( "Surface Probe" )]
[Category( "Test Ground" )]
[Icon( "speed" )]
public sealed class SurfaceProbe : Component, Component.ICollisionListener
{
	/// <summary>Seconds between motion reports while moving, or zero for none.</summary>
	[Property] public float Interval { get; set; } = 0.5f;

	/// <summary>Below this speed, for a second, the body counts as settled.</summary>
	[Property] public float RestSpeed { get; set; } = 0.05f;

	private Rigidbody Body => body ??= Components.Get<Rigidbody>();
	private Rigidbody body;

	private Collider Collider => collider ??= Components.Get<Collider>( FindMode.EverythingInSelf );
	private Collider collider;

	private Vector3 start;
	private TimeSince sinceStart;
	private TimeSince sinceReport;
	private TimeSince sinceMoving;
	private bool settled;
	private float lastSpeed;

	private string Tag => $"[{GameObject.Name}]";

	protected override void OnStart()
	{
		start = WorldPosition;
		sinceStart = 0;
		sinceReport = 0;
		sinceMoving = 0;
		settled = false;

		var rigidbody = Body;
		var ownCollider = Collider;

		if ( !rigidbody.IsValid() )
		{
			Log.Warning( $"{Tag} no Rigidbody - nothing to measure" );
			return;
		}

		if ( !rigidbody.CollisionEventsEnabled )
			Log.Warning( $"{Tag} Rigidbody.CollisionEventsEnabled is off - contact lines will not appear" );

		var asked = ownCollider.IsValid() && ownCollider.Friction.HasValue ? ownCollider.Friction.Value.ToString( "0.###" ) : "surface";
		var shapes = rigidbody.PhysicsBody.IsValid()
			? string.Join( ", ", rigidbody.PhysicsBody.Shapes.Select( x => $"friction={x.Friction:0.###}{(x.IsTrigger ? " trigger" : "")}" ) )
			: "no body";

		var sleep = rigidbody.PhysicsBody.IsValid() ? rigidbody.PhysicsBody.SleepThreshold : float.NaN;

		Log.Info( $"{Tag} mass={rigidbody.Mass:0.##} sleepThreshold={rigidbody.SleepThreshold:0.###} (body holds {sleep:0.###}) {(ownCollider.IsValid() ? ownCollider.GetType().Name : "(no collider)")} asked friction {asked}, shapes [{shapes}]" );
	}

	void Component.ICollisionListener.OnCollisionStart( Collision collision )
	{
		var mine = collision.Self.Shape;
		var theirs = collision.Other.Shape;
		var other = collision.Other.Collider;

		var myFriction = mine.IsValid() ? mine.Friction : float.NaN;
		var theirFriction = theirs.IsValid() ? theirs.Friction : float.NaN;

		// Box3D's default mixing is the geometric mean, so this is what the
		// contact actually runs with.
		var combined = float.Sqrt( myFriction * theirFriction );

		var wanted = other.IsValid() && other.Friction.HasValue ? other.Friction.Value.ToString( "0.###" ) : "surface";
		var surface = collision.Other.Surface.IsValid() ? collision.Other.Surface.ResourceName : "(none)";

		var speed = collision.Contact.Speed;

		Log.Info( $"{Tag} contact with {(other.IsValid() ? other.GameObject.Name : "(no collider)")}: friction mine={myFriction:0.###} theirs={theirFriction:0.###} (collider asked {wanted}, surface '{surface}') -> combined {combined:0.###}, normal={collision.Contact.Normal:0.##} speed={speed:0.##}" );

		if ( other.IsValid() && other.Friction.HasValue && !other.Friction.Value.AlmostEqual( theirFriction, 0.001f ) )
			Log.Warning( $"{Tag} {other.GameObject.Name} asked for friction {other.Friction.Value:0.###} but its shape holds {theirFriction:0.###} - the override never reached the simulation" );
	}

	void Component.ICollisionListener.OnCollisionStop( CollisionStop collision )
	{
		var other = collision.Other.Collider;
		Log.Info( $"{Tag} contact ended with {(other.IsValid() ? other.GameObject.Name : "(no collider)")}" );
	}

	protected override void OnFixedUpdate()
	{
		var rigidbody = Body;
		if ( !rigidbody.IsValid() ) return;

		var speed = rigidbody.Velocity.Length;

		if ( speed > RestSpeed )
		{
			sinceMoving = 0;
			lastSpeed = speed;

			if ( settled )
			{
				settled = false;
				start = WorldPosition;
				sinceStart = 0;
				Log.Info( $"{Tag} moving again" );
			}
		}
		else if ( !settled && (rigidbody.Sleeping || sinceMoving > 1.0f) )
		{
			settled = true;

			// A body that slowed down and stopped has a small last speed. One the
			// solver put to sleep mid-slide still had pace when it stopped - that
			// is the sleep threshold, not friction.
			if ( rigidbody.Sleeping && lastSpeed > 0.5f )
				Log.Warning( $"{Tag} put to sleep while moving at {lastSpeed:0.00} m/s, at {WorldPosition} - sleep threshold {rigidbody.PhysicsBody.SleepThreshold:0.###} m/s" );
			else
				Log.Info( $"{Tag} settled after {sinceStart.Relative:0.00}s, travelled {WorldPosition.Distance( start ):0.00}m, at {WorldPosition}" );

			return;
		}

		if ( settled || Interval <= 0 || sinceReport < Interval ) return;
		sinceReport = 0;

		// For a rolling sphere the rim speed equals the ground speed; a sliding
		// one has speed and no spin. The ratio tells them apart without a
		// contact point.
		var spin = rigidbody.AngularVelocity.Length;
		var radius = Radius();
		var rim = spin * radius;
		var ratio = speed > 0.001f ? rim / speed : 0.0f;
		var mode = radius <= 0 ? "" : ratio > 0.9f ? " rolling" : ratio < 0.3f ? " sliding" : " slipping";
		var touching = string.Join( ",", rigidbody.Touching.Where( x => x.IsValid() ).Select( x => x.GameObject.Name ) );

		Log.Info( $"{Tag} t={sinceStart.Relative:0.0}s speed={speed:0.00} spin={spin:0.00}rad/s rim={rim:0.00} ratio={ratio:0.00}{mode} sleeping={rigidbody.Sleeping} at {WorldPosition} touching=[{touching}]" );
	}

	/// <summary>Radius of a sphere collider in world units, or zero for anything else.</summary>
	private float Radius()
	{
		if ( Collider is SphereCollider sphere )
			return sphere.Radius * WorldScale.x;

		return 0.0f;
	}
}
