using Rinten.VR;

namespace TestGround;

/// <summary>
/// Something on a firearm for the hand that is not holding it: a slide to rack,
/// a foregrip to steady it. It is on - its object and collider - only while the
/// firearm is held, so the free hand finds it and nothing else of the gun; see
/// <see cref="VrFirearm.ReachedFor"/>, which hands over the nearest one.
/// </summary>
public abstract class VrFirearmPart : Component, IVrHoldable
{
	[Property] public VrFirearm Firearm { get; set; }

	/// <summary>Whether a hand has it, and which.</summary>
	public bool IsHeld => Grabber is not null;
	public bool HeldLeft { get; private set; }

	protected VrGrabber Grabber { get; private set; }

	/// <summary>Where the hand on it is, in the world.</summary>
	public Vector3 HandPosition => VrGrabber.HoldFrame( HeldLeft ).Position;

	public bool Grab( VrGrabber by, bool isLeft )
	{
		Firearm ??= GameObject.Parent?.GetComponentInParent<VrFirearm>();
		if ( !Firearm.IsValid() || !Firearm.IsHeld || Firearm.HeldLeft == isLeft ) return false;

		Grabber = by;
		HeldLeft = isLeft;
		Taken();
		return true;
	}

	public void Release( VrGrabber by, bool isLeft )
	{
		if ( !IsHeld ) return;

		Grabber = null;
		Dropped( by, true );
	}

	/// <summary>The firearm left its hand while this was held: this hand lets go too, having done nothing.</summary>
	public void LetGo()
	{
		if ( !IsHeld ) return;

		var by = Grabber;
		Grabber = null;
		by.Forget( this );
		Dropped( by, false );
	}

	/// <summary>A hand has just taken it, the firearm held in the other.</summary>
	protected abstract void Taken();

	/// <summary>
	/// The hand has let it go - <paramref name="done"/> when that was its own
	/// release, not the firearm going.
	/// </summary>
	protected abstract void Dropped( VrGrabber by, bool done );
}

/// <summary>
/// The back of a held pistol's slide, for the other hand: squeezed with the grip
/// and pulled back, then let go, it racks the gun - see <see cref="VrFirearm.Racked"/>.
/// </summary>
[Title( "VR Firearm Slide" )]
[Category( "Test Ground" )]
[Icon( "swipe_left" )]
public sealed class VrFirearmSlide : VrFirearmPart
{
	/// <summary>How far the slide travels, in metres.</summary>
	[Property] public float Travel { get; set; } = 0.028f;

	private Vector3 start;
	private bool back;

	protected override void Taken()
	{
		back = false;
		start = Firearm.WorldTransform.PointToLocal( HandPosition );
	}

	protected override void Dropped( VrGrabber by, bool done )
	{
		if ( !Firearm.IsValid() ) return;

		if ( !done ) Firearm.Rack( 0 );
		else if ( back ) Firearm.Racked();
		else Firearm.RackedShort();

		back = false;
	}

	protected override void OnUpdate()
	{
		if ( !IsHeld || !Firearm.IsValid() ) return;

		// Back along the gun's own length, in its space, so a gun that turns under
		// the hand does not rack itself.
		var now = Firearm.WorldTransform.PointToLocal( HandPosition );
		var pulled = ( ( now.z - start.z ) / Travel ).Clamp( 0, 1 );
		Firearm.Rack( pulled );

		if ( pulled > 0.9f && !back )
		{
			back = true;
			Firearm.RackedBack();
			VrGrabber.Hand( HeldLeft ).TriggerHaptics( HapticEffect.SoftImpact, lengthScale: 0.15f, amplitudeScale: 0.5f );
		}
	}
}

/// <summary>
/// A rifle's handguard, for the other hand: held, the gun points from the grip
/// hand through this one, and kicks less - see <see cref="VrFirearm.Steadied"/>.
/// The controller is hidden while it is held, as the grip hand's is.
/// </summary>
[Title( "VR Firearm Foregrip" )]
[Category( "Test Ground" )]
[Icon( "pan_tool" )]
public sealed class VrFirearmForegrip : VrFirearmPart
{
	/// <summary>How far the hand can wander from where it took hold before it has let go.</summary>
	[Property] public float BreakDistance { get; set; } = 0.25f;

	/// <summary>Where the hand took hold, in the firearm's space - the point the gun keeps under it.</summary>
	public Vector3 Anchor { get; private set; }

	protected override void Taken()
	{
		Anchor = Firearm.WorldTransform.PointToLocal( HandPosition );

		var controllers = Grabber.Components.Get<VrControllers>();
		controllers?.SetHidden( HeldLeft, true );
		controllers?.SetHolding( HeldLeft, true );
		VrGrabber.Hand( HeldLeft ).TriggerHaptics( HapticEffect.SoftImpact, lengthScale: 0.2f, amplitudeScale: 0.35f );
	}

	protected override void Dropped( VrGrabber by, bool done )
	{
		var controllers = by.Components.Get<VrControllers>();
		controllers?.SetHidden( HeldLeft, false );
		controllers?.SetHolding( HeldLeft, false );
	}

	protected override void OnUpdate()
	{
		if ( !IsHeld || !Firearm.IsValid() ) return;

		// A hand pulled well off the handguard is not on it any more.
		var along = Firearm.WorldTransform.PointToLocal( HandPosition ) - Anchor;
		if ( along.Length > BreakDistance ) LetGo();
	}
}
