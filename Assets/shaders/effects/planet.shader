// A planet: a sphere lit by the sun, with a surface made of noise - land and
// sea for a rocky world, bands for a gas giant - clouds drifting over it,
// ice at the poles, a lit atmosphere at the rim, and the night side dark but
// for scattered city lights. Every look is the material's numbers; the sun
// is a world position the material knows, so one shader lights every world
// in the system from the one star.

FEATURES
{
}

PARAMETERS
{
	// The surface: what the high ground is, what the low ground (or sea) is,
	// and a third colour the bands and the clouds are tinted with.
	float4 g_vColourA < Default4( 0.55, 0.45, 0.35, 1.0 ); UiGroup( "Surface" ); >;
	float4 g_vColourB < Default4( 0.10, 0.25, 0.55, 1.0 ); UiGroup( "Surface" ); >;
	float4 g_vColourC < Default4( 0.90, 0.85, 0.75, 1.0 ); UiGroup( "Surface" ); >;

	// How many noise cells round the world, how many layers of it, and where
	// the sea line sits in the noise (nought is all land, one all sea).
	float g_flNoiseScale < Default( 4.0 ); Range( 1, 16 ); UiGroup( "Surface" ); >;
	float g_flNoiseOctaves < Default( 4.0 ); Range( 1, 5 ); UiGroup( "Surface" ); >;
	float g_flSeaLevel < Default( 0.5 ); Range( 0, 1 ); UiGroup( "Surface" ); >;

	// Bands: how many across the world pole to pole - nought is a rocky
	// world with land and sea; and how much the noise bends them.
	float g_flBands < Default( 0.0 ); Range( 0, 24 ); UiGroup( "Bands" ); >;
	float g_flTurbulence < Default( 0.15 ); Range( 0, 1 ); UiGroup( "Bands" ); >;

	// Clouds: how much of the sky they cover, and how fast they drift.
	float g_flClouds < Default( 0.4 ); Range( 0, 1 ); UiGroup( "Clouds" ); >;
	float g_flCloudSpeed < Default( 0.02 ); Range( 0, 0.5 ); UiGroup( "Clouds" ); >;

	// Ice at the poles, from nought to halfway down.
	float g_flPoles < Default( 0.08 ); Range( 0, 0.5 ); UiGroup( "Surface" ); >;

	// The atmosphere: its colour at the rim and how thick it reads.
	float4 g_vAtmosphere < Default4( 0.4, 0.6, 1.0, 1.0 ); UiGroup( "Atmosphere" ); >;
	float g_flAtmosphere < Default( 0.8 ); Range( 0, 4 ); UiGroup( "Atmosphere" ); >;

	// The night side: how bright the ground is with no sun, and how many
	// city lights speckle it.
	float g_flNight < Default( 0.03 ); Range( 0, 0.5 ); UiGroup( "Night" ); >;
	float g_flLights < Default( 0.0 ); Range( 0, 2 ); UiGroup( "Night" ); >;

	// How fast the surface turns under the clouds, in turns a second.
	float g_flSpin < Default( 0.01 ); Range( -0.5, 0.5 ); UiGroup( "Surface" ); >;

	// Where the sun is, in the world.
	float4 g_vSunPosition < Default4( 0.0, 3.0, 0.0, 1.0 ); UiGroup( "Light" ); >;

	// A storm that stays: where it sits (u, v), how wide it is (in uv), and how
	// strongly it shows. The Great Red Spot; the Great Dark Spot.
	float4 g_vSpot < Default4( 0.3, 0.62, 0.0, 0.0 ); UiGroup( "Storm" ); >;
	float4 g_vSpotColour < Default4( 0.8, 0.3, 0.2, 1.0 ); UiGroup( "Storm" ); >;

	// Craters on an airless world: how many across it, and how deep they read.
	float g_flCraters < Default( 0.0 ); Range( 0, 40 ); UiGroup( "Surface" ); >;
	float g_flCraterDepth < Default( 0.5 ); Range( 0, 1 ); UiGroup( "Surface" ); >;

	// Relief: how much the height bends the normal, so ridges and rims take
	// the light and cast their own shade at the terminator.
	float g_flRelief < Default( 0.6 ); Range( 0, 3 ); UiGroup( "Surface" ); >;

	// Maria: broad dark lowlands, the way the Moon's face is. Deserts: a
	// belt of the third colour either side of the equator on a living world.
	float g_flMaria < Default( 0.0 ); Range( 0, 1 ); UiGroup( "Surface" ); >;
	float g_flDeserts < Default( 0.0 ); Range( 0, 1 ); UiGroup( "Surface" ); >;

	// How much a second noise bends the bands' latitude - eddies and vortices.
	float g_flWarp < Default( 0.5 ); Range( 0, 3 ); UiGroup( "Bands" ); >;

	// A ring's shadow on the world: inner and outer radius in planet radii,
	// the ring's tilt in degrees, and how dark the band reads.
	float4 g_vRingShadow < Default4( 0.0, 0.0, 0.0, 0.0 ); UiGroup( "Light" ); >;

	// What a particle turns: an extra glow (a planet lit by a flare) and a
	// dissolve for one being born.
	float g_flEmission < Attribute( "Emission" ); Default( 1.0 ); Range( 0, 4 ); UiGroup( "Effect" ); >;
	float g_flDissolve < Attribute( "Dissolve" ); Default( 0.0 ); Range( 0, 1 ); UiGroup( "Effect" ); >;

	// What casts a shadow on this world: one body, wherever it is now (a
	// moon over a planet, the planet over its moon), and how big it is. A
	// radius of nought is no shadow.
	float3 g_vShadow < Attribute( "Shadow" ); Default3( 0.0, 0.0, 0.0 ); UiGroup( "Light" ); >;
	float g_flShadowRadius < Default( 0.0 ); Range( 0, 5 ); UiGroup( "Light" ); >;
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

/// Craters: a jittered grid of round pits, each with a bright rim - the
/// distance to the nearest feature point, shaped.
float Craters( float2 p, float scale, out float rim )
{
	float2 q = p * scale;
	float2 cell = floor( q );
	float best = 1e9;
	float period = 2.0 * scale;

	for ( int y = -1; y <= 1; y++ )
	for ( int x = -1; x <= 1; x++ )
	{
		float2 c = cell + float2( x, y );
		float2 cw = float2( c.x - period * floor( c.x / period ), c.y );
		float2 centre = c + float2( Hash( cw ), Hash( cw + 7.3 ) );
		float radius = 0.18 + Hash( c + 3.1 ) * 0.25;
		float d = length( q - centre ) / radius;

		best = min( best, d );
	}

	// Inside the rim is the pit; the rim itself is a thin bright ring.
	rim = smoothstep( 0.85, 1.0, best ) * ( 1.0 - smoothstep( 1.0, 1.18, best ) );

	return 1.0 - smoothstep( 0.0, 0.9, best );
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
	int octaves = int( g_flNoiseOctaves );

	// Longitude turns with the spin; latitude is v, top to bottom.
	float2 uv = i.uv;
	uv.x += time * g_flSpin;

	float2 p = uv * float2( g_flNoiseScale * 2.0, g_flNoiseScale );
	float height = Fbm( p, octaves, g_flNoiseScale * 2.0 );

	// The slope of the height, for the relief: the same noise a hair away
	// along and across, against a frame built from the sphere's own up.
	float3 n0 = normalize( i.normal );
	float3 tangent = normalize( cross( float3( 0.0, 1.0, 0.0 ), n0 ) + float3( 1e-4, 0.0, 0.0 ) );
	float3 bitangent = cross( n0, tangent );
	float e = 0.004;
	float hu = Fbm( p + float2( e * g_flNoiseScale * 2.0, 0.0 ), octaves, g_flNoiseScale * 2.0 );
	float hv = Fbm( p + float2( 0.0, e * g_flNoiseScale ), octaves, g_flNoiseScale * 2.0 );
	float3 bent = normalize( n0 - ( ( hu - height ) * tangent + ( hv - height ) * bitangent ) * g_flRelief * 12.0 );

	float3 colour;

	if ( g_flBands > 0.5 )
	{
		// A gas giant: stripes pole to pole, pushed about by the noise, in the
		// two colours - the third colour where the stripes are strongest.
		float warp = Fbm( p * 0.7 + 5.0, 3, g_flNoiseScale * 1.4 ) - 0.5;
		float band = sin( ( uv.y + ( height - 0.5 ) * g_flTurbulence + warp * g_flWarp * 0.12 ) * g_flBands * 3.14159 );
		float t = band * 0.5 + 0.5;

		colour = lerp( g_vColourB.rgb, g_vColourA.rgb, t );
		colour = lerp( colour, g_vColourC.rgb, saturate( ( t - 0.85 ) * 6.0 ) * 0.5 );

		// Storms: noise where a band bends hardest.
		float storm = smoothstep( 0.72, 0.85, Fbm( p * 1.7 + 41.0, 3, g_flNoiseScale * 3.4 ) );
		colour = lerp( colour, g_vColourC.rgb * 1.15, storm * 0.5 );
	}
	else
	{
		// A rocky world: land above the sea line, sea below, a shore between.
		float shore = smoothstep( g_flSeaLevel - 0.03, g_flSeaLevel + 0.03, height );
		float3 land = g_vColourA.rgb * ( 0.7 + 0.6 * height );
		float3 sea = g_vColourB.rgb * ( 0.8 + 0.4 * height );

		colour = lerp( sea, land, shore );

		// Deserts and forests: the third colour where the land is high, and
		// in a belt either side of the equator where a world has deserts.
		colour = lerp( colour, g_vColourC.rgb, shore * smoothstep( 0.62, 0.8, height ) * 0.6 );

		float la = abs( uv.y - 0.5 );
		float belt = smoothstep( 0.06, 0.12, la ) * ( 1.0 - smoothstep( 0.2, 0.28, la ) );
		colour = lerp( colour, g_vColourC.rgb * 1.05, shore * belt * g_flDeserts * smoothstep( 0.3, 0.6, Fbm( p * 1.3 + 9.0, 3, g_flNoiseScale * 2.6 ) ) );

		// Maria: broad dark plains where a low, slow noise dips.
		float maria = smoothstep( 0.52, 0.68, Fbm( p * 0.35 + 21.0, 3, g_flNoiseScale * 0.7 ) );
		colour *= 1.0 - maria * 0.45 * g_flMaria;
	}

	// Craters, where a world has them: darker floors, a lit rim round each.
	if ( g_flCraters > 0.5 )
	{
		float rim;
		float pit = Craters( uv * float2( 2.0, 1.0 ), g_flCraters, rim );

		colour *= 1.0 - pit * g_flCraterDepth * 0.6;
		colour += colour * rim * g_flCraterDepth * 0.8;
	}

	// A storm that stays put: an oval on the surface, stretched along the
	// bands, in its own colour, with an eye and a rim.
	if ( g_vSpot.w > 0.0 )
	{
		float2 d = ( uv - g_vSpot.xy );
		d.x = frac( d.x + 0.5 ) - 0.5;
		d.x /= max( g_vSpot.z, 1e-3 );
		d.y /= max( g_vSpot.z * 0.55, 1e-3 );
		float r = length( d );
		float oval = 1.0 - smoothstep( 0.6, 1.0, r );
		float swirl = 0.7 + 0.3 * sin( r * 9.0 + Fbm( uv * g_flNoiseScale * 4.0, 2, g_flNoiseScale * 4.0 ) * 4.0 );

		colour = lerp( colour, g_vSpotColour.rgb * swirl, oval * g_vSpot.w );
	}

	// Ice at the poles, feathered by the noise so the cap has an edge.
	float lat = abs( uv.y - 0.5 ) * 2.0;
	float ice = smoothstep( 1.0 - g_flPoles * 2.0, 1.0 - g_flPoles * 2.0 + 0.08, lat + ( height - 0.5 ) * 0.1 );
	colour = lerp( colour, float3( 0.95, 0.97, 1.0 ), ice );

	// Clouds over it all, drifting the other way.
	float2 cp = ( uv + float2( time * g_flCloudSpeed, 0.0 ) ) * float2( g_flNoiseScale * 3.0, g_flNoiseScale * 1.5 );
	float cloud = smoothstep( 1.0 - g_flClouds, 1.0 - g_flClouds + 0.35, Fbm( cp + 7.0, 4, g_flNoiseScale * 3.0 ) );
	colour = lerp( colour, float3( 1.0, 1.0, 1.0 ), cloud * 0.85 );

	// The sun: where it is against this point of the surface - the bent
	// normal for the light, the smooth one for the rim.
	float3 n = n0;
	float3 toSun = normalize( g_vSunPosition.xyz - i.world );
	float3 toEye = normalize( g_frame[0].camera.xyz - i.world );

	float ndl = dot( bent, toSun );
	float day = smoothstep( -0.08, 0.25, ndl ) * smoothstep( -0.15, 0.1, dot( n0, toSun ) );

	// The ring's shadow: the line to the sun crossing the ring's plane
	// between its inner and outer edge.
	if ( g_vRingShadow.y > g_vRingShadow.x )
	{
		float3 origin = mul( float4( 0.0, 0.0, 0.0, 1.0 ), g_modelToWorld ).xyz;
		float radius = 0.5 * length( g_modelToWorld[0].xyz );
		float tilt = radians( g_vRingShadow.z );
		float3 ringUp = float3( 0.0, cos( tilt ), sin( tilt ) );
		float3 local = i.world - origin;
		float denom = dot( toSun, ringUp );

		if ( abs( denom ) > 1e-4 )
		{
			float t = -dot( local, ringUp ) / denom;

			if ( t > 0.0 )
			{
				float r = length( local + toSun * t ) / max( radius, 1e-4 );
				float inRing = smoothstep( g_vRingShadow.x - 0.05, g_vRingShadow.x + 0.05, r ) * ( 1.0 - smoothstep( g_vRingShadow.y - 0.05, g_vRingShadow.y + 0.05, r ) );

				day *= 1.0 - inRing * g_vRingShadow.w;
			}
		}
	}

	// An eclipse: the line from here to the sun passing within the caster's
	// radius - an umbra, with a penumbra half as wide again round it.
	if ( g_flShadowRadius > 0.0 )
	{
		float3 toCaster = g_vShadow - i.world;
		float along = dot( toCaster, toSun );

		if ( along > 0.0 )
		{
			float miss = length( toCaster - toSun * along );
			float shade = 1.0 - smoothstep( g_flShadowRadius * 0.85, g_flShadowRadius * 1.35, miss );

			day *= 1.0 - shade * 0.92;
		}
	}

	// City lights on the dark side, on land, where the noise clusters.
	float lights = 0.0;

	if ( g_flLights > 0.0 && g_flBands < 0.5 )
	{
		float shoreMask = smoothstep( g_flSeaLevel, g_flSeaLevel + 0.05, height );
		float speck = smoothstep( 0.62, 0.75, Fbm( p * 6.0 + 3.0, 3, g_flNoiseScale * 12.0 ) );
		lights = speck * shoreMask * ( 1.0 - day ) * ( 1.0 - cloud ) * g_flLights;
	}

	float3 lit = colour * ( g_flNight + day * ( 0.85 + 0.15 * saturate( ndl ) ) );
	lit += float3( 1.0, 0.85, 0.6 ) * lights;

	// The atmosphere: a rim that is lit only where the sun reaches round.
	float facing = 1.0 - saturate( dot( n, toEye ) );
	float rim = pow( facing, 2.5 ) * g_flAtmosphere;
	float rimLit = 0.15 + 0.85 * smoothstep( -0.3, 0.3, ndl );

	lit += g_vAtmosphere.rgb * rim * rimLit;

	// Being born: eaten away by the same noise.
	if ( height - g_flDissolve <= 0.0 ) discard;

	Out o;
	o.colour = float4( lit * g_flEmission * g_tint.rgb, g_tint.a );

#ifdef TARGET_SCENE
	o.surface = float4( 0.0, 0.0, 0.0, 0.0 );
#endif

#ifdef TARGET_SCREEN
	o.colour = float4( FinishToScreen( o.colour.rgb ), o.colour.a );
#endif

	return o;
}
