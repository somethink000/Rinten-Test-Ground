// An atmosphere: a shell a little bigger than its world, lit where the sun
// reaches it, thickest at the limb where the eye looks through the most of
// it, and warm at the terminator where the light comes in low. Drawn
// translucent over the planet; the numbers say what gas it is.

FEATURES
{
	// A shell of air is see-through by being one, so this is on to begin with
	// - blended over the world inside it, drawn after everything solid. See
	// CoreSceneRenderer.DrawFlags: the feature is the draw's state now, not a
	// blend mode the material carries beside it.
	Feature( F_TRANSLUCENT, 0..1, "Rendering" ) < Default( 1 ); >;
}

PARAMETERS
{
	// The colour of the sky seen from outside, and the colour of the low sun through it.
	float4 g_vColourA < Default4( 0.4, 0.65, 1.0, 1.0 ); UiGroup( "Atmosphere" ); >;
	float4 g_vColourB < Default4( 1.0, 0.55, 0.25, 1.0 ); UiGroup( "Atmosphere" ); >;

	// How much there is, and how tightly it hugs the limb.
	float g_flDensity < Default( 1.0 ); Range( 0, 4 ); UiGroup( "Atmosphere" ); >;
	float g_flFalloff < Default( 2.5 ); Range( 0.5, 8 ); UiGroup( "Atmosphere" ); >;

	// How far round the night side the glow reaches.
	float g_flWrap < Default( 0.25 ); Range( 0, 1 ); UiGroup( "Atmosphere" ); >;

	float4 g_vSunPosition < Default4( 0.0, 3.0, 0.0, 1.0 ); UiGroup( "Light" ); >;

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
	float3 n = normalize( i.normal );
	float3 toSun = normalize( g_vSunPosition.xyz - i.world );
	float3 toEye = normalize( g_frame[0].camera.xyz - i.world );

	// The limb: the less the surface faces the eye, the more air the eye
	// looks through.
	float facing = saturate( dot( n, toEye ) );
	float limb = pow( 1.0 - facing, g_flFalloff );

	// Lit where the sun is, and a little way round the night side.
	float ndl = dot( n, toSun );
	float lit = smoothstep( -g_flWrap, 0.4, ndl );

	// Low sun through the air is the warm colour: strongest at the terminator.
	float low = 1.0 - smoothstep( 0.0, 0.5, abs( ndl ) );
	float3 colour = lerp( g_vColourA.rgb, g_vColourB.rgb, low * 0.7 );

	float alpha = saturate( limb * lit * g_flDensity );

	Out o;
	o.colour = float4( colour * g_flEmission * g_tint.rgb, alpha * g_tint.a );

#ifdef TARGET_SCENE
	o.surface = float4( 0.0, 0.0, 0.0, 0.0 );
#endif

#ifdef TARGET_SCREEN
	o.colour = float4( FinishToScreen( o.colour.rgb ), o.colour.a );
#endif

	return o;
}
