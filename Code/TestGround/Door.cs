namespace TestGround;

/// <summary>
/// A door that swings ninety degrees when used. The other half of
/// <see cref="PlayerUse"/> - look at it and press Use.
/// </summary>
[Title( "Door" )]
[Category( "Test Ground" )]
[Icon( "door_front" )]
public sealed class Door : Component, Component.IPressable
{
	/// <summary>Degrees swung about world up when open.</summary>
	[Property] public float Angle { get; set; } = 90.0f;

	/// <summary>How quickly it eases toward the target pose.</summary>
	[Property] public float Speed { get; set; } = 6.0f;

	[Property, ReadOnly] public bool Open { get; private set; }

	Rotation closed;
	Rotation opened;
	bool hasRest;

	protected override void OnStart()
	{
		closed = WorldRotation;
		opened = closed * Rotation.FromYaw( Angle );
		hasRest = true;
	}

	protected override void OnUpdate()
	{
		if ( !hasRest ) return;

		var target = Open ? opened : closed;
		WorldRotation = Rotation.Slerp( WorldRotation, target, Time.Delta * Speed );
	}

	bool Component.IPressable.Press( Component.IPressable.Event e )
	{
		Open = !Open;
		return true;
	}

	Component.IPressable.Tooltip? Component.IPressable.GetTooltip( Component.IPressable.Event e )
	{
		return new Component.IPressable.Tooltip( Open ? "Close" : "Open", "door_front", "Use" );
	}
}
