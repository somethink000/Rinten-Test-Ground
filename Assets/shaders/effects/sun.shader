// A star: a sphere that is nothing but light - granulation that boils, two
// layers of it drifting against each other, hotter at the middle and dark
// towards the limb the way a real photosphere is, with an Emission a particle
// can turn up for a flare.

FEATURES
{
}

PARAMETERS
{
	// The photosphere: its bright colour and its dark one, between which the
	// granulation runs.
	float4 g_vColourA < Default4( 1.0, 0.95, 0.75, 1.0 ); UiGroup( "Star" ); >;
	float4 g_vColourB < Default4( 1.0, 0.45, 0.1, 1.0 ); UiGroup( "Star" ); >;

	// How fine the granulation is and how fast it boils.
	float g_flNoiseScale < Default( 6.0 ); Range( 1, 24 ); UiGroup( "Star" ); >;
	float g_flBoil < Default( 0.08 ); Range( 0, 1 ); UiGroup( "Star" ); >;

	// How dark the limb goes, nought to one.
	float g_flLimb < Default( 0.55 ); Range( 0, 1 ); UiGroup( "Star" ); >;

	// Sunspots: how much of the surface the dark, cooler patches take.
	float g_flSpots < Default( 0.12 ); Range( 0, 1 ); UiGroup( "Star" ); >;

	// How bright the whole is - over one is what the bloom picks up.
	float g_flBrightness < Default( 3.0 ); Range( 0, 10 ); UiGroup( "Star" ); >;

	float g_flEmission < Attribute( "Emission" ); Default( 1.0 ); Range( 0, 4 ); UiGroup( "Effect" ); >;
}

// The vertex it reads is the engine's one - VIn, out of frame.slang below, which
// every surface shares since clusters build their corners from it.

struct V2F
{
	float4 position : SV_Position;
	float3 world : TEXCOORD2;
	float3 normal : NORMAL;
	float2 uv : TEXCOORD0;
};

#define ENGINE_WORLD_PUSH 1

#include "frame.slang"

[shader("vertex")]
V2F MainVs( VIn i )
{
	float3 position = i.position;
	float3 normal = i.normal;

#ifdef MORPHED
	uint count = min( i.morphRun.y, MorphsPerVertex );

	for ( uint d = 0; d < count; d++ )
	{
		MorphDelta delta = LoadMorphDelta( i.morphRun.x + d );
		float weight = g_morphWeights[min( delta.morph, MorphsPerObject - 1 )];

		position += delta.position * weight;
		normal += delta.normal * weight;
	}

	float along = dot( normal, normal );
	if ( along > 1e-8 ) normal *= rsqrt( along );
#endif

#ifdef SKINNED
	float4x4 skin = SkinAt( i.bones, i.weights );

	position = mul( float4( position, 1.0 ), skin ).xyz;
	normal = mul( float4( normal, 0.0 ), skin ).xyz;
#endif

	row_major float4x4 modelToWorld = g_modelToWorld;

	float3 world = mul( float4( position, 1.0 ), modelToWorld ).xyz;

	V2F o;
	o.position = mul( float4( world, 1.0 ), g_frame[0].worldToClip );
	o.world = world;
	o.normal = mul( float4( normal, 0.0 ), modelToWorld ).xyz;
	o.uv = i.texCoord0.xy;

	return o;
}

/// Value noise on a lattice, smoothed - see stylized.shader for the same.
float Hash( float2 p )
{
	float3 q = frac( float3( p.x, p.y, p.x ) * 0.1031 );
	q += dot( q, q.yzx + 33.33 );
	return frac( ( q.x + q.y ) * q.z );
}

/// Wrapped along x every `period` cells, so a surface that goes round a
/// sphere meets itself at the seam - the lattice is the same lattice there.
float Noise( float2 p, float period )
{
	float2 cell = floor( p );
	float2 f = frac( p );
	float2 u = f * f * ( 3.0 - 2.0 * f );

	float x0 = cell.x - period * floor( cell.x / period );
	float x1 = ( cell.x + 1.0 ) - period * floor( ( cell.x + 1.0 ) / period );

	return lerp(
		lerp( Hash( float2( x0, cell.y ) ), Hash( float2( x1, cell.y ) ), u.x ),
		lerp( Hash( float2( x0, cell.y + 1.0 ) ), Hash( float2( x1, cell.y + 1.0 ) ), u.x ),
		u.y );
}

/// Octaves doubled exactly, so every one of them wraps at the same seam.
float Fbm( float2 p, int octaves, float period )
{
	float sum = 0.0;
	float amplitude = 0.5;
	float total = 0.0;

	for ( int i = 0; i < 5; i++ )
	{
		if ( i >= octaves ) break;

		sum += Noise( p, period ) * amplitude;
		total += amplitude;
		p = p * 2.0 + float2( 0.0, 9.7 );
		period *= 2.0;
		amplitude *= 0.5;
	}

	return sum / max( total, 1e-4 );
}

struct Out
{
	float4 colour : SV_Target0;

#ifdef TARGET_SCENE
	float4 surface : SV_Target1;
#endif
};

[shader("fragment")]
Out MainPs( V2F i )
{
	float time = g_frame[0].time.x;

	// Two layers of granulation drifting against each other, so the surface
	// boils rather than slides.
	float2 uv = i.uv * float2( g_flNoiseScale * 2.0, g_flNoiseScale );
	float a = Fbm( uv + float2( time * g_flBoil, time * g_flBoil * 0.6 ), 4, g_flNoiseScale * 2.0 );
	float b = Fbm( uv * 1.7 - float2( time * g_flBoil * 0.8, -time * g_flBoil * 0.5 ) + 13.0, 3, g_flNoiseScale * 3.4 );
	float cell = a * 0.65 + b * 0.35;

	// Hot where the cells are bright, dark in the lanes between them.
	float heat = smoothstep( 0.25, 0.8, cell );
	float3 colour = lerp( g_vColourB.rgb, g_vColourA.rgb, heat );

	// Flares: the very brightest cells go white.
	colour = lerp( colour, float3( 1.0, 1.0, 0.95 ), smoothstep( 0.78, 0.95, cell ) * 0.6 );

	// Sunspots: slow, large, dark patches - an umbra with a lighter penumbra.
	float spotNoise = Fbm( i.uv * float2( 3.0, 1.5 ) + float2( time * 0.004, 0.0 ), 3, 3.0 );
	float penumbra = smoothstep( 0.62 - g_flSpots * 0.25, 0.7 - g_flSpots * 0.25, spotNoise );
	float umbra = smoothstep( 0.70 - g_flSpots * 0.25, 0.76 - g_flSpots * 0.25, spotNoise );
	colour *= 1.0 - penumbra * 0.45 - umbra * 0.4;

	// The limb: darker and redder towards the edge.
	float3 n = normalize( i.normal );
	float3 toEye = normalize( g_frame[0].camera.xyz - i.world );
	float facing = saturate( dot( n, toEye ) );
	float limb = lerp( 1.0 - g_flLimb, 1.0, pow( facing, 0.6 ) );

	colour = lerp( colour * g_vColourB.rgb * 1.2, colour, limb );

	Out o;
	o.colour = float4( colour * g_flBrightness * g_flEmission * g_tint.rgb, g_tint.a );

#ifdef TARGET_SCENE
	o.surface = float4( 0.0, 0.0, 0.0, 0.0 );
#endif

#ifdef TARGET_SCREEN
	o.colour = float4( FinishToScreen( o.colour.rgb ), o.colour.a );
#endif

	return o;
}
