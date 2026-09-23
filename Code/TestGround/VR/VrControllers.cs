using Rinten.VR;

namespace TestGround;

/// <summary>
/// Visible controllers and keyframed palm colliders. A controller is shown while
/// it is held; tracked bare hands keep their joint overlay instead. The model is
/// the one the headset says is in the hand, its buttons pressed as the hand
/// presses them - see VRModelRenderer - unless <see cref="UseHeadsetModel"/> is
/// off, which puts the prefabs back.
/// </summary>
[Title( "VR Controllers" )]
[Category( "Test Ground" )]
[Icon( "sports_esports" )]
public sealed class VrControllers : Component
{
	/// <summary>Draw the controller the headset reports rather than the prefabs below.</summary>
	[Property] public bool UseHeadsetModel { get; set; } = true;

	[Property, Category( "Prefabs" )] public PrefabFile LeftControllerPrefab { get; set; }
	[Property, Category( "Prefabs" )] public PrefabFile RightControllerPrefab { get; set; }

	private Avatar left;
	private Avatar right;

	protected override void OnStart()
	{
		LeftControllerPrefab ??= PrefabFile.Load( "prefabs/vr/quest_left.prefab" );
		RightControllerPrefab ??= PrefabFile.Load( "prefabs/vr/quest_right.prefab" );
		left = CreateAvatar( "Left", LeftControllerPrefab, new Color( 0.20f, 0.55f, 1.00f ) );
		right = CreateAvatar( "Right", RightControllerPrefab, new Color( 1.00f, 0.38f, 0.18f ) );
	}

	protected override void OnUpdate()
	{
		if ( !Game.IsRunningInVR || Input.VR is null ) return;
		UpdateAvatar( left, Input.VR.LeftHand );
		UpdateAvatar( right, Input.VR.RightHand );
	}

	/// <summary>
	/// While holding, the hand's colliders stand down: the held body is steered to
	/// the hand, and they would push it straight back out - see VrGrabber.
	/// </summary>
	public void SetHolding( bool isLeft, bool holding )
	{
		var avatar = isLeft ? left : right;
		if ( avatar is not null ) avatar.Holding = holding;
	}

	/// <summary>
	/// Hide a hand's controller while something takes its place - a bow held in
	/// it is the hand's model while it is there.
	/// </summary>
	public void SetHidden( bool isLeft, bool hidden )
	{
		var avatar = isLeft ? left : right;
		if ( avatar is not null ) avatar.Hidden = hidden;
	}

	/// <summary>What the hands' colliders are tagged, for a trace that should pass through them.</summary>
	public const string HandTag = "vr_hand";

	private Avatar CreateAvatar( string side, PrefabFile prefab, Color fallbackColour )
	{
		var contact = Contact( $"{side} palm physics", 0.052f );
		var thumb = Contact( $"{side} thumb physics", 0.016f );
		var index = Contact( $"{side} index physics", 0.016f );

		if ( UseHeadsetModel )
		{
			var go = Scene.CreateObject();
			go.Name = $"{side} controller";
			var vr = go.Components.Create<VRModelRenderer>();
			vr.ModelSource = side == "Left" ? VRModelRenderer.ModelSources.LeftHand : VRModelRenderer.ModelSources.RightHand;
			vr.ModelRenderer = go.Components.Create<SkinnedModelRenderer>();
			return new Avatar { Contact = contact, Thumb = thumb, Index = index, Visual = go, HeadsetModel = true };
		}

		var visual = prefab is not null
			? GameObject.Clone( prefab, new global::Transform( Vector3.Zero, Rotation.Identity ) )
			: FallbackVisual( $"{side} controller", fallbackColour );
		visual.Name = $"{side} controller placeholder";

		return new Avatar { Contact = contact, Thumb = thumb, Index = index, Visual = visual };
	}

	private SphereCollider Contact( string name, float radius )
	{
		var go = Scene.CreateObject();
		go.Name = name;
		go.Tags.Add( HandTag );
		var collider = go.Components.Create<SphereCollider>();
		collider.Radius = radius;
		collider.Static = false;
		collider.Friction = 0.8f;
		return collider;
	}

	private GameObject FallbackVisual( string name, Color tint )
	{
		var go = Scene.CreateObject();
		go.Name = name;
		// Quest Touch Plus is about 20 cm long. This only runs if the prefab is missing.
		go.WorldScale = new Vector3( 0.09f, 0.14f, 0.20f );
		var renderer = go.Components.Create<ModelRenderer>();
		renderer.Model = Model.Cube;
		renderer.Tint = tint;
		return go;
	}

	private static void UpdateAvatar( Avatar avatar, VRController hand )
	{
		if ( avatar is null ) return;

		var pose = PalmPose( hand );
		var showController = !hand.IsHandTracked;
		avatar.Contact.Enabled = !avatar.Holding;
		avatar.Contact.WorldTransform = pose;
		avatar.Thumb.Enabled = !showController && !avatar.Holding;
		avatar.Index.Enabled = !showController && !avatar.Holding;
		if ( !showController )
		{
			avatar.Thumb.WorldTransform = JointPose( hand, VRHandJoint.ThumbTip );
			avatar.Index.WorldTransform = JointPose( hand, VRHandJoint.IndexTip );
		}

		avatar.Visual.Enabled = showController && !avatar.Hidden;
		if ( !avatar.Visual.Enabled ) return;

		if ( avatar.HeadsetModel )
		{
			// The model is authored in metres around the grip, which is this pose.
			avatar.Visual.WorldTransform = hand.Transform.WithScale( Input.VR.Scale );
			return;
		}

		// pose comes from VR with unit scale; keep the authored physical size of
		// the prefab instead of replacing it with a one-metre cube.
		avatar.Visual.WorldTransform = pose.WithScale( avatar.Visual.WorldScale );
	}

	private static Transform PalmPose( VRController hand )
	{
		if ( !hand.IsHandTracked ) return hand.Transform;

		var joints = hand.GetJoints( MotionRange.Hand );
		if ( joints is null || joints.Length < 26 ) return hand.Transform;

		var local = joints[(int)VRHandJoint.Palm].Transform;
		return Input.VR.Anchor.ToWorld( local.WithPosition( local.Position * Input.VR.Scale ) );
	}

	private static Transform JointPose( VRController hand, VRHandJoint joint )
	{
		var joints = hand.GetJoints( MotionRange.Hand );
		if ( joints is null || joints.Length < 26 ) return hand.Transform;

		var local = joints[(int)joint].Transform;
		return Input.VR.Anchor.ToWorld( local.WithPosition( local.Position * Input.VR.Scale ) );
	}

	private sealed class Avatar
	{
		public SphereCollider Contact;
		public SphereCollider Thumb;
		public SphereCollider Index;
		public GameObject Visual;
		public bool HeadsetModel;
		public bool Holding;
		public bool Hidden;
	}
}
