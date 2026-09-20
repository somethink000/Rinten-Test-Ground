using Rinten.Clutter;

namespace TestGround;

/// <summary>
/// Fills the <see cref="ClutterComponent"/> beside it when the scene starts
/// and says, over the volume, what it asked for and what it got: how many
/// instances the density promised, how many were placed, how high and low
/// they landed. A volume only fills when its Generate button is pressed, so
/// a scene written by a script would stand empty without this.
/// </summary>
[Title( "Clutter Probe" )]
[Category( "Test Ground" )]
[Icon( "grass" )]
public sealed class ClutterProbe : Component, Component.ExecuteInEditor
{
	/// <summary>Seconds between regenerations with a new seed. Nought fills once and leaves it.</summary>
	[Property] public float Churn { get; set; } = 0.0f;

	/// <summary>What the sign says the station is testing.</summary>
	[Property, TextArea] public string Note { get; set; }

	bool filled;
	int frames;
	TimeSince sinceFilled;

	protected override void OnEnabled()
	{
		filled = false;
		frames = 0;
	}

	protected override void OnUpdate()
	{
		var clutter = GameObject.GetComponent<ClutterComponent>();
		if ( clutter is null ) return;

		// Not on the first frame: the ground the scatterer traces against has
		// to be in the physics world first.
		frames++;
		if ( !filled && frames > 2 )
		{
			if ( clutter.Storage is null || clutter.Storage.TotalCount == 0 ) clutter.Generate();
			filled = true;
			sinceFilled = 0;
		}

		if ( filled && Churn > 0 && sinceFilled > Churn )
		{
			clutter.Seed++;
			clutter.Generate();
			sinceFilled = 0;
		}

		Report( clutter );
	}

	void Report( ClutterComponent clutter )
	{
		var bounds = clutter.Bounds;
		var top = WorldTransform.PointToWorld( new Vector3( 0, bounds.Maxs.y, 0 ) ) + Vector3.Up * 1.0f;

		var expected = "?";
#pragma warning disable CS0618 // the definition still holds its scatterer in AnyOfType
		if ( clutter.Clutter?.Scatterer.Value is SimpleScatterer simple )
#pragma warning restore CS0618
		{
			var area = bounds.Size.x * bounds.Size.z;
			expected = $"{area * simple.Density / 10.0f:0.#}";
		}

		var placed = clutter.Storage?.TotalCount ?? 0;
		var low = float.MaxValue;
		var high = float.MinValue;

		if ( clutter.Storage is not null )
		{
			foreach ( var (_, list) in clutter.Storage.GetAllInstances() )
			{
				foreach ( var instance in list )
				{
					low = System.Math.Min( low, instance.Position.y );
					high = System.Math.Max( high, instance.Position.y );
				}
			}
		}

		var heights = placed > 0 ? $"y {low:0.00} .. {high:0.00}" : "nothing placed";
		var text = $"{Note}\nexpected ~{expected}   placed {placed}\n{heights}";
		var colour = placed == 0 ? Color.Red : Color.White;

		DebugOverlay.Text( top, text, size: 36, color: colour );
	}
}
