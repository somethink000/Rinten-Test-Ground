namespace TestGround;

/// <summary>
/// Fires a physics trace from this object every frame and draws what it hit.
/// The scene that answers "does Scene.Trace actually hit things".
/// </summary>
[Title( "Trace Probe" )]
[Category( "Test Ground" )]
[Icon( "timeline" )]
public sealed class TraceProbe : Component, Component.ExecuteInEditor
{
	public enum Kind
	{
		Ray,
		Box,
		Sphere
	}

	/// <summary>The shape swept along the look.</summary>
	[Property] public Kind Type { get; set; } = Kind.Ray;

	/// <summary>Metres the trace travels.</summary>
	[Property] public float Length { get; set; } = 8.0f;

	/// <summary>Extents of the box, when Type is Box - the full size swept.</summary>
	[Property] public Vector3 BoxSize { get; set; } = new Vector3( 0.3f );

	/// <summary>Radius of the sphere, when Type is Sphere.</summary>
	[Property] public float Radius { get; set; } = 0.15f;

	/// <summary>Draw the miss as well as the hit, so a dead trace is visible.</summary>
	[Property] public bool DrawMiss { get; set; } = true;

	protected override void OnUpdate()
	{
		var start = WorldPosition;
		var end = start + WorldRotation.Forward * Length;
		var trace = Scene.Trace.Ray( start, end )
			.IgnoreGameObjectHierarchy( GameObject );

		if ( Type == Kind.Box )
			trace = trace.Size( BoxSize );

		if ( Type == Kind.Sphere )
			trace = trace.Radius( Radius );

		var hit = trace.Run();
		var color = hit.Hit ? new Color( 0.95f, 0.45f, 0.2f ) : new Color( 0.35f, 0.75f, 0.95f );

		if ( hit.Hit || DrawMiss )
			DebugOverlay.Line( start, hit.EndPosition, color );

		if ( Type == Kind.Box )
			DebugOverlay.Box( BBox.FromPositionAndSize( hit.EndPosition, BoxSize ), color );

		if ( Type == Kind.Sphere )
			DebugOverlay.Sphere( new Sphere( hit.EndPosition, Radius ), color );

		if ( hit.Hit )
		{
			DebugOverlay.Line( hit.EndPosition, hit.EndPosition + hit.Normal * 0.35f, Color.Yellow );
			DebugOverlay.Text( hit.EndPosition + Vector3.Up * 0.2f, hit.GameObject?.Name ?? "hit", size: 18, color: Color.White );
		}
	}
}
