using System.Text;

namespace TestGround;

/// <summary>
/// Lists every collider in the scene with what it asked for and what its physics
/// shapes actually hold - friction, trigger flag, body kind - once when the scene
/// starts and again whenever any of that changes. A friction that reads back as
/// something else, or drifts during play, is a line here with the object's name
/// on it.
/// </summary>
[Title( "Collider Audit" )]
[Category( "Test Ground" )]
[Icon( "fact_check" )]
public sealed class ColliderAudit : Component
{
	/// <summary>Seconds between checks for changes, or zero to only list once.</summary>
	[Property] public float Interval { get; set; } = 1.0f;

	private readonly Dictionary<Collider, string> seen = new();
	private TimeSince sinceCheck;
	private bool listed;

	protected override void OnStart()
	{
		sinceCheck = 0;
		listed = false;
	}

	protected override void OnFixedUpdate()
	{
		// The first pass waits a step so every collider has built its shapes.
		if ( !listed )
		{
			listed = true;
			Log.Info( $"[ColliderAudit] {Scene.GetAllComponents<Collider>().Count()} colliders in '{Scene.Name}':" );
			Check( true );
			return;
		}

		if ( Interval <= 0 || sinceCheck < Interval ) return;
		sinceCheck = 0;
		Check( false );
	}

	private void Check( bool listAll )
	{
		foreach ( var collider in Scene.GetAllComponents<Collider>() )
		{
			if ( !collider.IsValid() ) continue;

			var line = Describe( collider );
			seen.TryGetValue( collider, out var previous );
			seen[collider] = line;

			if ( listAll )
				Log.Info( $"[ColliderAudit]   {line}" );
			else if ( previous is null )
				Log.Info( $"[ColliderAudit] new: {line}" );
			else if ( previous != line )
				Log.Warning( $"[ColliderAudit] changed: {line}\n    was: {previous}" );
		}

		foreach ( var gone in seen.Keys.Where( x => !x.IsValid() ).ToList() )
			seen.Remove( gone );
	}

#pragma warning disable CS0618 // KeyframeBody is the only public way at a keyframe collider's shapes
	private static PhysicsBody BodyOf( Collider collider )
		=> collider.Rigidbody.IsValid() ? collider.Rigidbody.PhysicsBody : collider.KeyframeBody;
#pragma warning restore CS0618

	private static string Describe( Collider collider )
	{
		var sb = new StringBuilder();

		sb.Append( collider.GameObject.Name ).Append( '/' ).Append( collider.GetType().Name );
		sb.Append( collider.IsTrigger ? " trigger" : " solid" );
		sb.Append( collider.Rigidbody.IsValid() ? " rigidbody" : collider.Static ? " static" : " keyframe" );
		sb.Append( " asked friction=" ).Append( collider.Friction.HasValue ? collider.Friction.Value.ToString( "0.###" ) : "surface" );

		if ( collider.Elasticity.HasValue ) sb.Append( " elasticity=" ).Append( collider.Elasticity.Value.ToString( "0.###" ) );
		if ( collider.RollingResistance.HasValue ) sb.Append( " rolling=" ).Append( collider.RollingResistance.Value.ToString( "0.###" ) );
		if ( collider.Surface.IsValid() ) sb.Append( " surface=" ).Append( collider.Surface.ResourceName );

		var body = BodyOf( collider );

		if ( !body.IsValid() )
		{
			sb.Append( " | NO BODY" );
			return sb.ToString();
		}

		sb.Append( " | body=" ).Append( body.BodyType.ToString().ToLowerInvariant() );

		// Only this collider's shapes - a rigidbody's body carries every child collider's too.
		var shapes = body.Shapes.Where( x => x.IsValid() && x.Collider == collider ).ToList();

		if ( shapes.Count == 0 )
		{
			sb.Append( " NO SHAPES" );
			return sb.ToString();
		}

		sb.Append( " shapes=[" );
		sb.Append( string.Join( ", ", shapes.Select( x => $"{(x.IsTrigger ? "trigger" : "solid")} friction={x.Friction:0.###} material={x.SurfaceMaterial}" ) ) );
		sb.Append( ']' );

		if ( collider.Friction is float asked && shapes.Any( x => !x.Friction.AlmostEqual( asked, 0.001f ) ) )
			sb.Append( " <-- FRICTION MISMATCH" );

		if ( shapes.Any( x => x.IsTrigger != collider.IsTrigger ) )
			sb.Append( " <-- TRIGGER MISMATCH" );

		return sb.ToString();
	}
}
