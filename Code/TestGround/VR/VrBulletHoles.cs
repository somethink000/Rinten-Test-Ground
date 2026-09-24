namespace TestGround;

/// <summary>
/// Where rounds went in: a small dark mark flat on the surface, carried by what
/// was hit. The oldest go once there are too many.
/// </summary>
public static class VrBulletHoles
{
	public const int Limit = 96;

	private static readonly Queue<GameObject> holes = new();

	public static void Mark( Scene scene, SceneTraceResult hit )
	{
		if ( hit.GameObject is null ) return;

		var go = scene.CreateObject();
		go.Name = "Bullet hole";
		go.WorldPosition = hit.HitPosition + hit.Normal * 0.0015f;
		go.WorldRotation = Rotation.LookAt( hit.Normal );
		go.WorldScale = new Vector3( 0.011f, 0.011f, 0.002f );

		var renderer = go.Components.Create<ModelRenderer>();
		renderer.Model = Model.Sphere;
		renderer.Tint = new Color( 0.03f, 0.03f, 0.03f );
		renderer.RenderType = ModelRenderer.ShadowRenderType.Off;

		// On whatever carries what was hit, as an arrow is.
		var mover = hit.GameObject.GetComponentInParent<Rigidbody>() is { MotionEnabled: true } rb ? rb.GameObject : null;
		var carrier = mover ?? hit.GameObject.Root;
		if ( carrier.IsValid() ) go.SetParent( carrier, true );

		holes.Enqueue( go );
		while ( holes.Count > Limit )
		{
			var old = holes.Dequeue();
			if ( old.IsValid() ) old.Destroy();
		}
	}
}
