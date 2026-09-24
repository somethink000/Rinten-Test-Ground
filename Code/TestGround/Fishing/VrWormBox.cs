using Rinten.VR;

namespace TestGround;

/// <summary>
/// A tin of worms that stays where it is put. A free hand coming near flips its
/// lid open; squeezed in over the worms, that hand has one - see
/// <see cref="VrWorm"/>, which goes on a hook it is brought to. The lid shuts
/// again once no hand is near.
/// </summary>
/// <remarks>
/// The box is a holdable that is never held: a hand reaching into it is given a
/// worm instead - as the belt hands out a magazine - and anywhere else it gives
/// nothing. The model gives it the graph parameter lid and the attachments worms and
/// lid (see ~/Documents/Blender/tools/fishing/SPEC.md); without them, a stand-in
/// lid object swings on <see cref="LidPivot"/> and the worms are
/// <see cref="DefaultWorms"/> up from the origin.
/// </remarks>
[Title( "VR Worm Box" )]
[Category( "Test Ground" )]
[Icon( "inventory_2" )]
public sealed class VrWormBox : Component, IVrHoldable
{
	[Property] public SkinnedModelRenderer Renderer { get; set; }

	/// <summary>What a hand takes out of it.</summary>
	[Property] public PrefabFile WormPrefab { get; set; }

	/// <summary>A stand-in lid's hinge, turned open about its X when the model has no graph for it.</summary>
	[Property] public GameObject LidPivot { get; set; }

	[Property] public Vector3 DefaultWorms { get; set; } = new( 0, 0.045f, 0 );

	/// <summary>How near a free hand has to come for the lid to open.</summary>
	[Property] public float LidReach { get; set; } = 0.22f;

	/// <summary>How near the worms a hand has to be to take one.</summary>
	[Property] public float TakeReach { get; set; } = 0.09f;

	/// <summary>How far the lid swings open, in degrees - for the stand-in.</summary>
	[Property] public float LidAngle { get; set; } = 110.0f;

	/// <summary>How open the lid is, nought to one.</summary>
	public float Open { get; private set; }

	/// <summary>The top of the pile inside, in the world.</summary>
	public Vector3 Worms => WorldTransform.PointToWorld( wormsLocal );

	private Vector3 wormsLocal;
	private Rotation lidRest;

	protected override void OnStart()
	{
		Renderer ??= Components.Get<SkinnedModelRenderer>();
		WormPrefab ??= PrefabFile.Load( "prefabs/vr/fishing/worm.prefab" );

		var model = Renderer?.Model;
		wormsLocal = model?.GetAttachment( "worms" )?.Position ?? DefaultWorms;
		if ( LidPivot.IsValid() ) lidRest = LidPivot.LocalRotation;
	}

	protected override void OnUpdate()
	{
		var wanted = HandNear() ? 1.0f : 0.0f;
		Open = MathX.Approach( Open, wanted, Time.Delta * ( wanted > Open ? 4.0f : 1.5f ) );

		if ( Renderer.IsValid() && Renderer.UseAnimGraph && Renderer.EffectiveAnimationGraph is not null ) Renderer.Set( "lid", Open );
		else if ( LidPivot.IsValid() ) LidPivot.LocalRotation = lidRest * Rotation.FromPitch( -LidAngle * Open );
	}

	/// <summary>Whether a free hand is near enough to want in.</summary>
	private bool HandNear()
	{
		if ( !Game.IsRunningInVR || Input.VR is null ) return false;

		var grabber = Scene.GetAllComponents<VrGrabber>().FirstOrDefault();
		if ( grabber is null ) return false;

		foreach ( var left in new[] { true, false } )
		{
			if ( grabber.IsBusy( left ) ) continue;
			if ( VrGrabber.HoldFrame( left ).Position.Distance( Worms ) < LidReach ) return true;
		}

		return false;
	}

	/// <summary>
	/// A hand squeezing in over the worms, the lid open, is given one and holds
	/// that - the box itself is never taken.
	/// </summary>
	public bool Grab( VrGrabber by, bool isLeft )
	{
		if ( Open < 0.5f || WormPrefab is null ) return false;
		if ( VrGrabber.HoldFrame( isLeft ).Position.Distance( Worms ) > TakeReach ) return false;

		var go = GameObject.Clone( WormPrefab, VrGrabber.HoldFrame( isLeft ) );
		var worm = go.Components.Get<VrWorm>();

		if ( worm is null || !by.Give( isLeft, worm, VrButton.Grip ) ) go.Destroy();
		else VrGrabber.Hand( isLeft ).TriggerHaptics( HapticEffect.SoftImpact, lengthScale: 0.15f, amplitudeScale: 0.25f );

		// False either way: this hand holds the worm, not the box.
		return false;
	}

	public void Release( VrGrabber by, bool isLeft )
	{
	}
}
