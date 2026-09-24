using Rinten.VR;

namespace TestGround;

/// <summary>
/// Magazines from the belt. While one hand holds a firearm, the other reaches down
/// to the hip and squeezes the grip, and has a full magazine for it - whichever
/// its <see cref="VrFirearm.MagazinePrefab"/> is; see VrMagazine.
/// </summary>
[Title( "VR Belt" )]
[Category( "Test Ground" )]
[Icon( "work" )]
public sealed class VrBelt : Component
{
	/// <summary>How far below the head the belt is, from and to.</summary>
	[Property] public float Top { get; set; } = 0.4f;
	[Property] public float Bottom { get; set; } = 0.95f;

	/// <summary>How far out from the body, flat, a hand still counts as at the belt.</summary>
	[Property] public float Reach { get; set; } = 0.35f;

	private readonly bool[] inside = new bool[2];
	private readonly bool[] wasPressed = new bool[2];

	protected override void OnUpdate()
	{
		if ( !Game.IsRunningInVR || Input.VR is null ) return;

		var grabber = Components.Get<VrGrabber>();
		if ( grabber is null ) return;

		TakeMagazine( grabber, true );
		TakeMagazine( grabber, false );
	}

	/// <summary>Whether a hand is down at the hip, where the pouches are.</summary>
	public bool AtBelt( bool isLeft )
	{
		var head = Input.VR.Head.Position;
		var offset = VrGrabber.HoldFrame( isLeft ).Position - head;

		if ( offset.y > -Top || offset.y < -Bottom ) return false;
		return offset.WithY( 0 ).Length < Reach;
	}

	private void TakeMagazine( VrGrabber grabber, bool isLeft )
	{
		var i = isLeft ? 0 : 1;
		var pressed = grabber.IsPressed( isLeft, VrButton.Grip, false );
		var fresh = pressed && !wasPressed[i];
		wasPressed[i] = pressed;

		// Only a free hand, and only while the other one has a firearm - whose magazine it gets.
		var magazine = Scene.GetAllComponents<VrFirearm>().FirstOrDefault( x => x.IsHeld && x.HeldLeft != isLeft )?.MagazinePrefab;
		var here = !grabber.IsBusy( isLeft ) && magazine is not null && AtBelt( isLeft );

		if ( here && !inside[i] )
			VrGrabber.Hand( isLeft ).TriggerHaptics( HapticEffect.SoftImpact, lengthScale: 0.15f, amplitudeScale: 0.3f );

		inside[i] = here;

		if ( !here || !fresh ) return;

		var go = GameObject.Clone( magazine, VrGrabber.HoldFrame( isLeft ) );
		var taken = go.Components.Get<VrMagazine>();

		if ( taken is null || !grabber.Give( isLeft, taken, VrButton.Grip ) ) go.Destroy();
	}
}
