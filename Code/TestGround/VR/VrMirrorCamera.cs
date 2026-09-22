using Rinten.VR;

namespace TestGround;

/// <summary>
/// Makes the normal editor/game camera follow the HMD's centre pose while VR is
/// running. The OpenXR renderer still uses VRAnchor for the headset eyes; this
/// component only supplies the matching desktop mirror view.
/// </summary>
[Title( "VR Mirror Camera" )]
[Category( "Test Ground" )]
[Icon( "videocam" )]
public sealed class VrMirrorCamera : Component
{
	protected override void OnUpdate() => FollowHead();
	protected override void OnPreRender() => FollowHead();

	private void FollowHead()
	{
		if ( !Game.IsRunningInVR || Input.VR is null ) return;
		GameObject.WorldTransform = Input.VR.Head;
	}
}
