namespace TestGround;

/// <summary>Which button a hand holds something with - see <see cref="VrGrabber"/>.</summary>
public enum VrButton
{
	/// <summary>The grip, or a closed fist on a tracked hand.</summary>
	Grip,

	/// <summary>The trigger, or a pinch on a tracked hand.</summary>
	Trigger,

	/// <summary>Either of them: held until both are let go.</summary>
	Either,
}

/// <summary>
/// Something that decides for itself what being held means - a bow the hand
/// wields, an arrow it carries - rather than being steered to the hand like
/// anything else <see cref="VrGrabber"/> picks up.
/// </summary>
public interface IVrHoldable
{
	/// <summary>A hand has taken it. False refuses, and the hand holds nothing.</summary>
	bool Grab( VrGrabber grabber, bool isLeft );

	/// <summary>The button it was taken with came up.</summary>
	void Release( VrGrabber grabber, bool isLeft );

	/// <summary>
	/// What keeps it in the hand once taken with <paramref name="taken"/>. An
	/// arrow stays while either button is down, whichever took it.
	/// </summary>
	VrButton HeldWith( VrButton taken ) => taken;

	/// <summary>
	/// What a hand reaching for this actually takes. A pistol held in the other
	/// hand gives up its slide, to be racked, rather than itself.
	/// </summary>
	IVrHoldable ReachedFor( bool isLeft ) => this;
}
