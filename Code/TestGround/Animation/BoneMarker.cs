namespace TestGround;

/// <summary>
/// Rides a named bone or attachment of the character it is pointed at, so what
/// the pose is doing to that bone can be seen from outside the mesh.
/// </summary>
/// <remarks>
/// The two are not the same question and both go wrong on their own. A bone is
/// where the skeleton puts it, and reading one is
/// <see cref="SkinnedModelRenderer.TryGetBoneTransform"/>; an attachment is a
/// point the model declares on a bone, with its own offset and turn, and is
/// the thing a weapon or an effect is actually hung from. A marker that follows
/// the bone but not the attachment is an offset that did not survive the
/// compile.
/// </remarks>
[Title( "Bone Marker" )]
[Category( "Test Ground" )]
[Icon( "my_location" )]
public sealed class BoneMarker : Component
{
	public enum Follow
	{
		/// <summary>A bone of the skeleton, by name.</summary>
		Bone,
		/// <summary>A point the model declares, by name.</summary>
		Attachment,
	}

	/// <summary>The character followed.</summary>
	[Property] public SkinnedModelRenderer Renderer { get; set; }

	/// <summary>Which of the two is looked up.</summary>
	[Property] public Follow What { get; set; } = Follow.Bone;

	/// <summary>The name to look up. Case is not significant.</summary>
	[Property] public string Name { get; set; } = "";

	/// <summary>Where this sits relative to what it follows.</summary>
	[Property] public Vector3 Offset { get; set; }

	/// <summary>Take the turn as well as the place.</summary>
	[Property] public bool TakeRotation { get; set; } = true;

	/// <summary>
	/// Stop drawing where the name matched nothing, rather than sitting at the
	/// origin pretending to be a bone.
	/// </summary>
	[Property] public bool HideWhenMissing { get; set; } = true;

	/// <summary>Whether the last look-up found anything.</summary>
	public bool Found { get; private set; }

	protected override void OnUpdate()
	{
		if ( !Renderer.IsValid() || string.IsNullOrWhiteSpace( Name ) ) return;

		var at = What == Follow.Attachment ? Attachment() : Bone();

		Found = at.HasValue;

		if ( HideWhenMissing )
		{
			// The renderer rather than this component: switching itself off is
			// a marker that never looks again, so the first frame before the
			// model has loaded would hide it for good.
			var drawn = GameObject.GetComponent<ModelRenderer>();
			if ( drawn.IsValid() ) drawn.Enabled = Found;
		}

		if ( !Found ) return;

		var transform = at.Value;

		WorldPosition = transform.PointToWorld( Offset );

		if ( TakeRotation )
			WorldRotation = transform.Rotation;
	}

	Transform? Bone()
		=> Renderer.TryGetBoneTransform( Name, out var tx ) ? tx : null;

	Transform? Attachment()
		=> Renderer.GetAttachment( Name );
}
