namespace TestGround;

/// <summary>
/// Stocks a pond: <see cref="Count"/> fish of the prefab at the start, somewhere
/// in the water, and another now and then for each one taken out and not put back.
/// </summary>
[Title( "VR Fish Spawner" )]
[Category( "Test Ground" )]
[Icon( "set_meal" )]
public sealed class VrFishSpawner : Component
{
	[Property] public VrPond Pond { get; set; }

	/// <summary>The fish, one picked at random for each - a species is a prefab's numbers and model. List one twice for more of it.</summary>
	[Property] public List<PrefabFile> FishPrefabs { get; set; } = new();

	[Property] public int Count { get; set; } = 4;

	/// <summary>Seconds before a fish taken out is made up for.</summary>
	[Property] public float RestockDelay { get; set; } = 30.0f;

	private readonly List<VrFish> fish = new();
	private TimeSince sinceShort;
	private bool wasShort;

	protected override void OnStart()
	{
		Pond ??= Components.Get<VrPond>();
		for ( var i = 0; i < Count; i++ ) Spawn();
	}

	/// <summary>One more fish, somewhere in the water, facing anywhere.</summary>
	public VrFish Spawn()
	{
		var prefabs = FishPrefabs?.Where( x => x is not null ).ToList();
		if ( prefabs is null || prefabs.Count == 0 || !Pond.IsValid() ) return null;

		var prefab = prefabs[Game.Random.Int( 0, prefabs.Count - 1 )];
		var at = Pond.RandomPoint( 0.3f, 0.2f, 0.8f );
		var go = GameObject.Clone( prefab, new Transform( at, Rotation.FromYaw( Game.Random.Float( 0, 360 ) ) ) );
		var one = go.Components.Get<VrFish>();
		if ( one is null ) return null;

		one.Pond = Pond;
		fish.Add( one );
		return one;
	}

	protected override void OnUpdate()
	{
		// The ones still in the pond - a fish on the bank, or gone, does not count.
		fish.RemoveAll( x => !x.IsValid() );
		var left = fish.Count( x => !x.Landed && Pond.Covers( x.WorldPosition ) );

		var isShort = left < Count;
		if ( isShort && !wasShort ) sinceShort = 0;
		wasShort = isShort;

		if ( isShort && sinceShort > RestockDelay )
		{
			sinceShort = 0;
			Spawn();
		}
	}
}
