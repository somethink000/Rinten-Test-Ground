namespace TestGround;

/// <summary>
/// Clones a prefab on a clock, at this object's pose. The spawned copy can
/// take a lifetime of its own so the floor does not fill up.
/// </summary>
[Title( "Spawner" )]
[Category( "Test Ground" )]
[Icon( "add_box" )]
public sealed class Spawner : Component
{
	/// <summary>What to clone. Drop a .prefab here.</summary>
	[Property] public PrefabFile Prefab { get; set; }

	/// <summary>Seconds between copies.</summary>
	[Property] public float Interval { get; set; } = 1.0f;

	/// <summary>
	/// Seconds each copy lives. Nought leaves it alone - use this when the
	/// prefab already carries <see cref="SelfDestruct"/>, or when you want
	/// the copies to stay.
	/// </summary>
	[Property] public float Lifetime { get; set; } = 0.0f;

	TimeSince last;

	protected override void OnEnabled()
	{
		last = Interval;
	}

	protected override void OnUpdate()
	{
		if ( Prefab is null ) return;
		if ( last < Interval ) return;

		last = 0;

		var copy = GameObject.Clone( Prefab, WorldTransform );
		if ( !copy.IsValid() ) return;

		copy.Enabled = true;

		if ( Lifetime > 0.0f )
		{
			var death = copy.GetOrAddComponent<SelfDestruct>();
			death.Seconds = Lifetime;
		}
	}
}
