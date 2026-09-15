// Stylised effect surface: a mesh drawn by a particle, unlit, coloured along a
// ramp, eaten away by noise. Fire on a flame mesh, a shield that breathes, a
// shard that dissolves - one shader with the knobs an effect turns.
//
// Everything a particle drives is declared with Attribute( … ) and arrives per
// draw, so a thousand of these each dissolve on their own clock - see
// MeshRenderModule, which reads these declarations and offers each as a row.
// Eight numbers a draw is the budget (CoreShaderParams.DrawSlots); the two
// ParticleAge / ParticleRandom rows the module writes count against it. What
// is not an Attribute - the ramp's two colours, the noise's shape - is the
// material's, and the same for every particle drawn with it.
//
// The mesh's blend shapes and skinning come through the same vertex stage
// the standard surface uses, so a flame with three shapes bends the way the
// module says.

FEATURES
{
	// Both sides drawn: a flame is a shell you look into, a shield is looked at
	// from inside as often as out.
	Feature( F_BACKFACES, 0..1, "Rendering" ) < Flag( TwoSided ); >;

	// Blended over what is behind it: the dissolve's holes and the fade at
	// the tip are alpha, and without this the draw is solid and they are not.
	Feature( F_TRANSLUCENT, 0..1, "Rendering" ) < Default( 1 ); >;
}

PARAMETERS
{
	// The ramp: what the surface is at the base and what it is at the tip,
	// with the noise deciding how far along it every pixel sits.
	float4 g_vColourA < Default4( 1.0, 0.85, 0.35, 1.0 ); UiGroup( "Ramp" ); >;
	float4 g_vColourB < Default4( 1.0, 0.2, 0.02, 1.0 ); UiGroup( "Ramp" ); >;

	// The noise: how many cells across the mesh, and how many layers of it.
	float g_flNoiseScale < Default( 3.0 ); Range( 0.5, 16 ); UiGroup( "Noise" ); >;
	float g_flNoiseOctaves < Default( 3.0 ); Range( 1, 4 ); UiGroup( "Noise" ); >;

	// Which way the noise runs over the mesh, in uv per second: up for fire,
	// sideways for a shield's shimmer.
	float2 g_vScrollDirection < Default2( 0.0, -1.0 ); UiGroup( "Noise" ); >;

	// The rest a particle turns.

	// How much of the surface is gone, nought to one. Noise below this is a
	// hole; noise just above it is the hot edge.
	float g_flDissolve < Attribute( "Dissolve" ); Default( 0.0 ); Range( 0, 1 ); UiGroup( "Effect" ); >;

	// How wide the hot edge of a hole is, in noise.
	float g_flEdge < Attribute( "Edge" ); Default( 0.08 ); Range( 0, 0.5 ); UiGroup( "Effect" ); >;

	// What the colour is multiplied by. Over one is what glows into the bloom.
	float g_flEmission < Attribute( "Emission" ); Default( 2.0 ); Range( 0, 8 ); UiGroup( "Effect" ); >;

	// How fast the noise scrolls, times the material's direction.
	float g_flScroll < Attribute( "Scroll" ); Default( 1.0 ); Range( 0, 8 ); UiGroup( "Effect" ); >;

	// How much the surface lights up where it turns away from the eye, and
	// how tight to the edge that is. Nought for fire; a shield is mostly rim.
	float g_flFresnel < Attribute( "Fresnel" ); Default( 0.0 ); Range( 0, 4 ); UiGroup( "Effect" ); >;

	// The two the mesh module writes for every draw, so a shader can animate
	// itself off a particle's life without a curve in the effect at all.
	float g_flParticleAge < Attribute( "ParticleAge" ); Default( 0.0 ); Range( 0, 1 ); UiGroup( "Particle" ); >;
	float g_flParticleRandom < Attribute( "ParticleRandom" ); Default( 0.0 ); Range( 0, 1 ); UiGroup( "Particle" ); >;
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

/// Value noise: a hash on the lattice, smoothed between. Cheap, no picture,
/// and at these scales as good as anything - see CurlNoiseModule for the
/// same bargain on the host.
float Hash( float2 p )
{
	float3 q = frac( float3( p.x, p.y, p.x ) * 0.1031 );
	q += dot( q, q.yzx + 33.33 );
	return frac( ( q.x + q.y ) * q.z );
}

float Noise( float2 p )
{
	float2 cell = floor( p );
	float2 f = frac( p );
	float2 u = f * f * ( 3.0 - 2.0 * f );

	return lerp(
		lerp( Hash( cell ), Hash( cell + float2( 1, 0 ) ), u.x ),
		lerp( Hash( cell + float2( 0, 1 ) ), Hash( cell + float2( 1, 1 ) ), u.x ),
		u.y );
}

float Fbm( float2 p, int octaves )
{
	float sum = 0.0;
	float amplitude = 0.5;
	float total = 0.0;

	for ( int i = 0; i < 4; i++ )
	{
		if ( i >= octaves ) break;

		sum += Noise( p ) * amplitude;
		total += amplitude;
		p = p * 2.03 + float2( 17.1, 9.7 );
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
	// The noise, scrolled by time and offset per particle so two flames drawn
	// with one material do not flicker in step.
	float time = g_frame[0].time.x;
	float2 uv = i.uv * g_flNoiseScale
		+ g_vScrollDirection * ( time * g_flScroll )
		+ g_flParticleRandom * 37.0;

	float mask = Fbm( uv, int( g_flNoiseOctaves ) );

	// Along the mesh, up is v: the ramp runs from the base to the tip, with
	// the noise pushing it about.
	float along = saturate( i.uv.y * 0.85 + ( mask - 0.5 ) * 0.5 );
	float3 colour = lerp( g_vColourA.rgb, g_vColourB.rgb, along );

	// The dissolve: holes where the noise is under the threshold, and a hot
	// edge just above it - the edge is the base colour pushed past white.
	float cut = mask - g_flDissolve;

	if ( cut <= 0.0 ) discard;

	float edge = 1.0 - saturate( cut / max( g_flEdge, 1e-4 ) );
	colour = lerp( colour, g_vColourA.rgb * 2.5 + 0.5, edge * edge );

	// The rim: brighter where the surface turns away, for a shield or a ghost.
	float3 toEye = normalize( g_frame[0].camera.xyz - i.world );
	float3 n = normalize( i.normal );
	float facing = 1.0 - saturate( abs( dot( n, toEye ) ) );
	float rim = pow( facing, 3.0 ) * g_flFresnel;

	colour += g_vColourA.rgb * rim;

	// Faded towards the tip and towards the holes, so a flame thins out
	// rather than ending in a cut edge.
	float alpha = saturate( cut * 4.0 ) * lerp( 1.0, 1.0 - along, 0.25 ) + rim * 0.5;

	Out o;
	o.colour = float4( colour * g_flEmission * g_tint.rgb, saturate( alpha ) * g_tint.a );

#ifdef TARGET_SCENE
	o.surface = float4( 0.0, 0.0, 0.0, 0.0 );
#endif

#ifdef TARGET_SCREEN
	o.colour = float4( FinishToScreen( o.colour.rgb ), o.colour.a );
#endif

	return o;
}
