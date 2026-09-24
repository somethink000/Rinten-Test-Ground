namespace TestGround;

/// <summary>
/// A body of water: a box whose top face is the surface. The object sits at the
/// middle of that surface, and the water runs <see cref="Size"/> across and down
/// from there. Everything that swims or floats asks the pond it is in - see
/// <see cref="At"/> - how deep it is, rather than knowing about water itself.
/// </summary>
/// <remarks>
/// The walls, the bed and the water plane are ordinary children of the prefab;
/// this only answers questions and splashes.
/// </remarks>
[Title( "VR Pond" )]
[Category( "Test Ground" )]
[Icon( "water" )]
public sealed class VrPond : Component
{
	/// <summary>Width (x), depth (y) and length (z) of the water, in metres.</summary>
	[Property] public Vector3 Size { get; set; } = new( 4, 1, 3 );

	/// <summary>What a splash sounds like - something landing on the water.</summary>
	[Property] public SoundEvent SplashSound { get; set; }

	/// <summary>A splash slower than this, in metres a second, makes no sound.</summary>
	[Property] public float SplashSpeed { get; set; } = 1.5f;

	/// <summary>The height of the water surface in the world.</summary>
	public float SurfaceHeight => WorldPosition.y;

	/// <summary>The height of the bed in the world.</summary>
	public float BottomHeight => WorldPosition.y - Size.y;

	protected override void OnStart()
	{
		SplashSound ??= ResourceLibrary.Get<SoundEvent>( "sounds/water/water_splash_medium.sound" );
	}

	/// <summary>Whether the point is over or in the water, looking straight down - its height aside.</summary>
	public bool Covers( Vector3 point )
	{
		var local = WorldTransform.PointToLocal( point );
		return System.MathF.Abs( local.x ) <= Size.x * 0.5f && System.MathF.Abs( local.z ) <= Size.z * 0.5f;
	}

	/// <summary>Whether the point is inside the water.</summary>
	public bool IsUnderwater( Vector3 point ) => Covers( point ) && point.y < SurfaceHeight && point.y > BottomHeight - 0.05f;

	/// <summary>How far under the surface the point is: below nought it is above the water. Zero off the pond.</summary>
	public float Depth( Vector3 point ) => Covers( point ) ? SurfaceHeight - point.y : 0.0f;

	/// <summary>The point pulled inside the water, <paramref name="margin"/> in from every side, bed and surface.</summary>
	public Vector3 Clamp( Vector3 point, float margin )
	{
		var local = WorldTransform.PointToLocal( point );
		var x = Size.x * 0.5f - margin;
		var z = Size.z * 0.5f - margin;
		local = new Vector3( local.x.Clamp( -x, x ), local.y.Clamp( -Size.y + margin, -margin ), local.z.Clamp( -z, z ) );
		return WorldTransform.PointToWorld( local );
	}

	/// <summary>Somewhere in the water, <paramref name="margin"/> in from every side, between the depths given.</summary>
	public Vector3 RandomPoint( float margin, float minDepth, float maxDepth )
	{
		var x = Size.x * 0.5f - margin;
		var z = Size.z * 0.5f - margin;
		var depth = Game.Random.Float( minDepth, System.MathF.Min( maxDepth, Size.y - margin ) );
		return WorldTransform.PointToWorld( new Vector3( Game.Random.Float( -x, x ), -depth, Game.Random.Float( -z, z ) ) );
	}

	/// <summary>Something hit the water at <paramref name="point"/> going <paramref name="speed"/>: a splash, if it was fast enough.</summary>
	public void Splash( Vector3 point, float speed )
	{
		if ( speed < SplashSpeed || SplashSound is null ) return;

		var handle = Sound.Play( SplashSound, point.WithY( SurfaceHeight ) );
		if ( handle is not null ) handle.Volume = ( speed / ( SplashSpeed * 4.0f ) ).Clamp( 0.15f, 1.0f );
	}

	/// <summary>The pond whose water the point is over, if any; a little above the surface still counts.</summary>
	public static VrPond At( Scene scene, Vector3 point )
	{
		if ( scene is null ) return null;

		foreach ( var pond in scene.GetAllComponents<VrPond>() )
		{
			if ( pond.Covers( point ) && point.y > pond.BottomHeight - 0.1f && point.y < pond.SurfaceHeight + 2.0f )
				return pond;
		}

		return null;
	}
}
