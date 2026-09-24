using Rinten.VR;

namespace TestGround;

/// <summary>
/// Arrows from over the shoulder. While one hand holds a bow, the other reaches
/// behind the head and squeezes the grip or the trigger, and has an arrow - held
/// until both are let go, nocked if it is brought to the string first.
/// </summary>
[Title( "VR Quiver" )]
[Category( "Test Ground" )]
[Icon( "vertical_split" )]
public sealed class VrQuiver : Component
{
	[Property] public PrefabFile Arrow { get; set; }

	/// <summary>How far behind the head's centre a hand has to be, flat, facing where the head faces.</summary>
	[Property] public float Behind { get; set; } = 0.05f;

	/// <summary>How far below the head a hand still counts - the shoulder, not the hip.</summary>
	[Property] public float Below { get; set; } = 0.35f;

	/// <summary>How far to either side of the head, and above it.</summary>
	[Property] public float Reach { get; set; } = 0.45f;

	private readonly bool[] inside = new bool[2];
	private readonly bool[] wasPressed = new bool[2];

	protected override void OnStart()
	{
		Arrow ??= PrefabFile.Load( "prefabs/vr/archery/arrow.prefab" );
	}

	protected override void OnUpdate()
	{
		if ( !Game.IsRunningInVR || Input.VR is null ) return;

		var grabber = Components.Get<VrGrabber>();
		if ( grabber is null ) return;

		TakeArrow( grabber, true );
		TakeArrow( grabber, false );
	}

	/// <summary>Whether a hand is behind the head, where the arrows are.</summary>
	public bool InQuiver( bool isLeft )
	{
		var head = Input.VR.Head;
		var hand = VrGrabber.HoldFrame( isLeft ).Position;
		var facing = head.Rotation.Forward.WithY( 0 ).Normal;
		var offset = hand - head.Position;

		if ( Vector3.Dot( offset, facing ) > -Behind ) return false;
		if ( offset.y < -Below || offset.y > Reach ) return false;

		return offset.WithY( 0 ).Length < Reach;
	}

	private void TakeArrow( VrGrabber grabber, bool isLeft )
	{
		var i = isLeft ? 0 : 1;
		var pressed = grabber.IsPressed( isLeft, VrButton.Either, false );
		var fresh = pressed && !wasPressed[i];
		wasPressed[i] = pressed;

		// Only a free hand, and only while the other one has a bow.
		var bowInOtherHand = Scene.GetAllComponents<VrBow>().Any( x => x.IsHeld && x.HeldLeft != isLeft );
		var here = !grabber.IsBusy( isLeft ) && bowInOtherHand && InQuiver( isLeft );

		// A touch on the way in, so the hand knows it is there without looking.
		if ( here && !inside[i] )
			VrGrabber.Hand( isLeft ).TriggerHaptics( HapticEffect.SoftImpact, lengthScale: 0.15f, amplitudeScale: 0.3f );

		inside[i] = here;

		if ( !here || !fresh || Arrow is null ) return;

		var go = GameObject.Clone( Arrow, VrGrabber.HoldFrame( isLeft ) );
		var arrow = go.Components.Get<VrArrow>();

		if ( arrow is null || !grabber.Give( isLeft, arrow, VrButton.Either ) ) go.Destroy();
	}
}
