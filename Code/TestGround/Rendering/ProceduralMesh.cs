using HalfEdgeMesh;

namespace TestGround;

/// <summary>
/// Builds a <see cref="PolygonMesh"/> by hand and hands it to the
/// <see cref="MeshComponent"/> beside it, so the renderer scene has geometry
/// that was never a model file: a wedge, a flight of stairs, a prism, a
/// ring - the shapes a level's blockout is made of.
/// </summary>
/// <remarks>
/// Rebuilt whenever a property changes, in the editor too, so the inspector
/// is a way of trying shapes. The material goes on every face.
/// </remarks>
[Title( "Procedural Mesh" )]
[Category( "Test Ground" )]
[Icon( "change_history" )]
public sealed class ProceduralMesh : Component, Component.ExecuteInEditor
{
	public enum Kind
	{
		/// <summary>A wedge: flat on the floor, sloping up along +Z.</summary>
		Ramp,
		/// <summary>Steps climbing along +Z.</summary>
		Stairs,
		/// <summary>An upright prism with that many sides.</summary>
		Prism,
		/// <summary>A flat ring - a prism with the middle taken out, side by side.</summary>
		Ring,
		/// <summary>A box, for comparing against models/dev/box.mdl.</summary>
		Box,
	}

	[Property] public Kind Shape { get => shape; set { shape = value; Rebuild(); } }
	Kind shape = Kind.Ramp;

	/// <summary>Metres across, tall and deep.</summary>
	[Property] public Vector3 Size { get => size; set { size = value; Rebuild(); } }
	Vector3 size = new( 2.0f, 1.0f, 2.0f );

	/// <summary>Steps of a stair, sides of a prism or ring.</summary>
	[Property, Range( 3, 32 )] public int Segments { get => segments; set { segments = value; Rebuild(); } }
	int segments = 6;

	/// <summary>What every face wears. Empty leaves the mesh's own default.</summary>
	[Property] public Material Material { get => material; set { material = value; Rebuild(); } }
	Material material;

	/// <summary>Degrees under which neighbouring faces are shaded as one smooth surface.</summary>
	[Property, Range( 0, 180 )] public float SmoothingAngle { get => smoothing; set { smoothing = value; Rebuild(); } }
	float smoothing = 0.0f;

	protected override void OnEnabled() => Rebuild();

	void Rebuild()
	{
		if ( !Active ) return;

		var mesh = Build();
		var target = GameObject.Components.GetOrCreate<MeshComponent>();
		target.Mesh = mesh;
		target.SmoothingAngle = smoothing;
		target.Enabled = mesh is not null;
	}

	PolygonMesh Build()
	{
		var mesh = new PolygonMesh();
		var half = size * 0.5f;

		switch ( shape )
		{
			case Kind.Ramp:
				Wedge( mesh, half );
				break;

			case Kind.Stairs:
				for ( var i = 0; i < segments; i++ )
				{
					var f0 = i / (float)segments;
					var f1 = ( i + 1 ) / (float)segments;
					// Each step is its own block, front at the low end, each one
					// higher than the last and reaching to the back.
					var z0 = -half.z + f0 * size.z;
					Block( mesh, new Vector3( -half.x, 0, z0 ), new Vector3( half.x, f1 * size.y, half.z ) );
				}
				break;

			case Kind.Prism:
				Prism( mesh, segments, half.x, 0.0f, size.y );
				break;

			case Kind.Ring:
				Prism( mesh, segments, half.x, half.x * 0.6f, size.y );
				break;

			case Kind.Box:
				Block( mesh, new Vector3( -half.x, 0, -half.z ), new Vector3( half.x, size.y, half.z ) );
				break;
		}

		if ( material is not null )
		{
			foreach ( var face in mesh.FaceHandles ) mesh.SetFaceMaterial( face, material );
		}

		return mesh;
	}

	/// <summary>
	/// A face wound the way the mesh wants its front: the corners are listed
	/// counter-clockwise seen from outside, and the mesh takes them clockwise.
	/// </summary>
	static void Face( PolygonMesh mesh, params VertexHandle[] corners )
	{
		System.Array.Reverse( corners );
		mesh.AddFace( corners );
	}

	/// <summary>Six faces between two corners.</summary>
	static void Block( PolygonMesh mesh, Vector3 min, Vector3 max )
	{
		var v = mesh.AddVertices(
			new Vector3( min.x, min.y, min.z ), new Vector3( max.x, min.y, min.z ), new Vector3( max.x, min.y, max.z ), new Vector3( min.x, min.y, max.z ),
			new Vector3( min.x, max.y, min.z ), new Vector3( max.x, max.y, min.z ), new Vector3( max.x, max.y, max.z ), new Vector3( min.x, max.y, max.z ) );
		Face( mesh, v[0], v[3], v[2], v[1] ); // bottom
		Face( mesh, v[4], v[5], v[6], v[7] ); // top
		Face( mesh, v[0], v[1], v[5], v[4] ); // front (-z)
		Face( mesh, v[2], v[3], v[7], v[6] ); // back (+z)
		Face( mesh, v[3], v[0], v[4], v[7] ); // left
		Face( mesh, v[1], v[2], v[6], v[5] ); // right
	}

	static void Wedge( PolygonMesh mesh, Vector3 half )
	{
		var v = mesh.AddVertices(
			new Vector3( -half.x, 0, -half.z ), new Vector3( half.x, 0, -half.z ),
			new Vector3( half.x, 0, half.z ), new Vector3( -half.x, 0, half.z ),
			new Vector3( half.x, half.y * 2, half.z ), new Vector3( -half.x, half.y * 2, half.z ) );

		Face( mesh, v[0], v[3], v[2], v[1] ); // bottom
		Face( mesh, v[0], v[1], v[4], v[5] ); // slope
		Face( mesh, v[2], v[3], v[5], v[4] ); // back
		Face( mesh, v[3], v[0], v[5] );       // left
		Face( mesh, v[1], v[2], v[4] );       // right
	}

	/// <summary>An upright n-gon; an inner radius above nought makes it a ring.</summary>
	/// <remarks>
	/// A half-edge mesh takes a face only if every edge it shares with a face
	/// already there is walked the other way round - so the sides, the caps
	/// and the inner wall are all written to the same rule as <see cref="Block"/>:
	/// a side is bottom-left, bottom-right, top-right, top-left with the bottom
	/// edge going the way the cap above it goes.
	/// </remarks>
	static void Prism( PolygonMesh mesh, int sides, float radius, float inner, float height )
	{
		var outerBottom = new VertexHandle[sides];
		var outerTop = new VertexHandle[sides];
		var innerBottom = new VertexHandle[sides];
		var innerTop = new VertexHandle[sides];

		for ( var i = 0; i < sides; i++ )
		{
			var angle = i / (float)sides * 3.14159265f * 2.0f;
			var dir = new Vector3( float.Cos( angle ), 0, float.Sin( angle ) );

			outerBottom[i] = mesh.AddVertex( dir * radius );
			outerTop[i] = mesh.AddVertex( dir * radius + Vector3.Up * height );

			if ( inner > 0 )
			{
				innerBottom[i] = mesh.AddVertex( dir * inner );
				innerTop[i] = mesh.AddVertex( dir * inner + Vector3.Up * height );
			}
		}

		for ( var i = 0; i < sides; i++ )
		{
			var j = ( i + 1 ) % sides;
			Face( mesh, outerBottom[i], outerBottom[j], outerTop[j], outerTop[i] );

			if ( inner > 0 )
			{
				Face( mesh, innerBottom[j], innerBottom[i], innerTop[i], innerTop[j] );
				Face( mesh, outerTop[j], innerTop[j], innerTop[i], outerTop[i] );
				Face( mesh, outerBottom[i], innerBottom[i], innerBottom[j], outerBottom[j] );
			}
		}

		if ( inner <= 0 )
		{
			var top = new VertexHandle[sides];
			var bottom = new VertexHandle[sides];
			for ( var i = 0; i < sides; i++ )
			{
				top[i] = outerTop[i];
				bottom[i] = outerBottom[sides - 1 - i];
			}
			Face( mesh, top );
			Face( mesh, bottom );
		}
	}
}
