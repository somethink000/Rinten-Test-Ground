namespace TestGround;

/// <summary>
/// A case or a round thrown out of a pistol: a small body that bounces, rings
/// when it lands, and goes after a while - the oldest first once there are too many.
/// </summary>
[Title( "VR Shell" )]
[Category( "Test Ground" )]
[Icon( "hdr_strong" )]
public sealed class VrShell : Component, Component.ICollisionListener
{
	[Property] public SoundEvent Land { get; set; }

	/// <summary>How long it lies about, in seconds.</summary>
	[Property] public float Life { get; set; } = 30.0f;

	/// <summary>How many rings it makes, the hardest landings only.</summary>
	[Property] public int Rings { get; set; } = 3;

	public const int Limit = 60;

	private static readonly Queue<GameObject> shells = new();

	private TimeSince born;
	private TimeSince lastRing;
	private int rung;

	protected override void OnStart()
	{
		Land ??= ResourceLibrary.Get<SoundEvent>( "sounds/weapons/pistol/shell.sound" );
		born = 0;
		lastRing = 1;

		shells.Enqueue( GameObject );
		while ( shells.Count > Limit )
		{
			var old = shells.Dequeue();
			if ( old.IsValid() ) old.Destroy();
		}
	}

	protected override void OnUpdate()
	{
		if ( born > Life ) GameObject.Destroy();
	}

	public void OnCollisionStart( Collision collision )
	{
		if ( rung >= Rings || lastRing < 0.08f || Land is null ) return;
		if ( System.MathF.Abs( collision.Contact.NormalSpeed ) < 0.4f ) return;

		rung++;
		lastRing = 0;
		Sound.Play( Land, collision.Contact.Point );
	}
}
