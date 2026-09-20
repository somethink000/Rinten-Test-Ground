namespace TestGround;

/// <summary>
/// Changes the material of the renderer beside it while the scene runs, one
/// way per <see cref="Mode"/>: the tint, a copied material's numbers, a
/// swap between two materials, or the accessor's per-slot override. Each is
/// a path a game takes to change how something looks, and each can be broken
/// on its own.
/// </summary>
[Title( "Material Probe" )]
[Category( "Test Ground" )]
[Icon( "palette" )]
public sealed class MaterialProbe : Component
{
	public enum Mode
	{
		/// <summary>ModelRenderer.Tint cycles through the hues.</summary>
		Tint,
		/// <summary>A copy of the material has its Roughness swept nought to one and back.</summary>
		Roughness,
		/// <summary>A copy of the material has its Tint value (not the renderer's) cycled.</summary>
		MaterialTint,
		/// <summary>MaterialOverride flips between the two materials every second.</summary>
		Swap,
		/// <summary>Materials.SetOverride( 0, ... ) flips between the two materials.</summary>
		Accessor,
		/// <summary>IMaterialSetter.SetMaterial flips between the two materials.</summary>
		Setter,
	}

	[Property] public Mode What { get; set; } = Mode.Tint;

	/// <summary>The first material, and the one that is copied.</summary>
	[Property] public Material A { get; set; }

	/// <summary>The other, for the modes that swap.</summary>
	[Property] public Material B { get; set; }

	/// <summary>Seconds a full cycle takes.</summary>
	[Property] public float Period { get; set; } = 4.0f;

	Material copy;
	TimeSince since;

	protected override void OnStart()
	{
		since = 0;

		if ( What is Mode.Roughness or Mode.MaterialTint )
		{
			copy = A?.CreateCopy( $"{GameObject.Name} copy" );
			var renderer = GameObject.GetComponent<ModelRenderer>();
			if ( renderer is not null && copy is not null ) renderer.MaterialOverride = copy;
		}
	}

	protected override void OnUpdate()
	{
		var renderer = GameObject.GetComponent<ModelRenderer>();
		if ( renderer is null || Period <= 0 ) return;

		var t = ( since % Period ) / Period;
		var hue = new ColorHsv( t * 360.0f, 0.8f, 1.0f ).ToColor();
		var flip = ( (int)( since / ( Period * 0.25f ) ) & 1 ) == 0;

		switch ( What )
		{
			case Mode.Tint:
				renderer.Tint = hue;
				break;

			case Mode.Roughness:
				// A triangle wave: up for half the period, down for the other.
				copy?.Set( "Roughness", t < 0.5f ? t * 2.0f : 2.0f - t * 2.0f );
				break;

			case Mode.MaterialTint:
				copy?.Set( "Tint", hue );
				break;

			case Mode.Swap:
				renderer.MaterialOverride = flip ? A : B;
				break;

			case Mode.Accessor:
				renderer.Materials.SetOverride( 0, flip ? A : B );
				break;

			case Mode.Setter:
				( (Component.IMaterialSetter)renderer ).SetMaterial( flip ? A : B );
				break;
		}
	}
}
