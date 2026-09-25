#!/usr/bin/env python3
"""Writes the hand-laid test scenes: prefabs, traces, the debug overlay, lights,
fog, sound and world UI - each under its category folder in scenes/. The
galleries come from tools/gallery, the particle scenes from tools/fx."""
import json, uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent / "Assets" / "scenes"
NS = uuid.UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")

def uid(*parts):
    return str(uuid.uuid5(NS, "/".join(parts)))

IDENT = "0,0,0,1"
LOOK_DOWN = "-0.7071068,0,0,0.7071068"

def vec(x, y, z):
    return f"{x},{y},{z}"

def go(name, pos="0,0,0", rot=IDENT, scale="1,1,1", tags="", components=None, children=None):
    return {
        "__guid": uid("go", name, str(pos)),
        "__version": 2,
        "Flags": 0,
        "Name": name,
        "Position": pos,
        "Rotation": rot,
        "Scale": scale,
        "Tags": tags,
        "Enabled": True,
        "NetworkMode": 2,
        "NetworkFlags": 0,
        "NetworkOrphaned": 0,
        "NetworkTransmit": True,
        "OwnerTransfer": 1,
        "Components": components or [],
        "Children": children or [],
    }

def comp(type_name, name, **props):
    d = {
        "__type": type_name,
        "__guid": uid("comp", type_name, name),
        "__enabled": True,
        "Flags": 0,
    }
    d.update(props)
    return d

def renderer(name, model, tint="1,1,1,1", material=None):
    return comp(
        "Rinten.ModelRenderer", name,
        BodyGroups=18446744073709551615,
        CreateAttachments=False,
        MaterialGroup=None,
        MaterialOverride=material,
        Materials=None,
        Model=model,
        RenderOptions={"GameLayer": True, "OverlayLayer": False, "BloomLayer": False, "AfterUILayer": False},
        RenderType="On",
        Tint=tint,
    )

def box_collider(name, static=True, trigger=False, scale="1,1,1"):
    return comp(
        "Rinten.BoxCollider", name,
        Center="0,0,0",
        Scale=scale,
        ColliderFlags=0,
        Elasticity=None,
        Friction=None,
        IsTrigger=trigger,
        RollingResistance=None,
        Static=static,
        Surface=None,
        SurfaceVelocity="0,0,0",
    )

def sphere_collider(name, static=True, radius=0.5):
    return comp(
        "Rinten.SphereCollider", name,
        Center="0,0,0",
        Radius=radius,
        ColliderFlags=0,
        Elasticity=None,
        Friction=None,
        IsTrigger=False,
        RollingResistance=None,
        Static=static,
        Surface=None,
        SurfaceVelocity="0,0,0",
    )

def rigidbody(name):
    return comp(
        "Rinten.Rigidbody", name,
        AngularDamping=0.05,
        EnableImpactDamage=False,
        EnhancedCcd=False,
        Gravity=True,
        GravityScale=1,
        ImpactDamage=0,
        LinearDamping=0,
        Locking={"X": False, "Y": False, "Z": False, "Pitch": False, "Yaw": False, "Roll": False},
        MassCenterOverride="0,0,0",
        MassOverride=0,
        MinImpactDamageSpeed=500,
        MotionEnabled=True,
        OverrideMassCenter=False,
        RigidbodyFlags=0,
        SleepThreshold=2,
        StartAsleep=False,
    )

def reset_on_fall(name):
    return comp("TestGround.ResetOnFall", name, Height=-10, SpawnPoint=None)

def label(name, pos, text):
    return go(name, pos=pos, components=[
        comp(
            "Rinten.TextRenderer", name,
            __version=2,
            Billboard="YOnly",
            BlendMode="Normal",
            FogStrength=1,
            HorizontalAlignment="Center",
            RenderOptions={"GameLayer": True, "OverlayLayer": False, "BloomLayer": False, "AfterUILayer": False},
            Scale=0.18,
            TextScope={
                "Text": text,
                "TextColor": "0.9,0.94,1,1",
                "FontName": "Poppins",
                "FontSize": 44,
                "FontWeight": 700,
                "FontItalic": False,
                "FontVariantNumeric": "Normal",
                "LineHeight": 1.1,
                "LetterSpacing": 0,
                "WordSpacing": 0,
                "FilterMode": "Bilinear",
                "FontSmooth": "Auto",
                "Outline": {"Enabled": False, "Size": 4, "Color": "0,0,1,1"},
                "Shadow": {"Enabled": True, "Size": 6, "Color": "0,0,0,0.8", "Offset": "3,3"},
                "OutlineUnder": {"Enabled": False, "Size": 4, "Color": "0,1,0,1"},
                "ShadowUnder": {"Enabled": False, "Size": 4, "Color": "0,0,0,1", "Offset": "4,4"},
            },
            VerticalAlignment="Center",
        )
    ])

def primitive(name, pos, scale, model, tint, collider, extra=None):
    comps = [renderer(name, model, tint), collider]
    if extra:
        comps.extend(extra)
    return go(name, pos=pos, scale=scale, components=comps)

def environment(sun_brightness=1.6, ambient="0.18,0.21,0.27,1"):
    return go("Environment", children=[
        go("Sun", tags="light_directional,light", rot="-0.372788548,-0.776215434,-0.149966598,0.485827178", components=[
            comp(
                "Rinten.DirectionalLight", "sun",
                __version=1,
                Attenuation=1,
                Brightness=sun_brightness,
                Contribution="Diffuse, Specular, Transmissive",
                FogMode="Enabled",
                FogStrength=1,
                LightColor="1,0.97,0.92,1",
                ShadowAngle=0.6,
                ShadowDetail=64,
                Shadows=True,
                SkyColor="0,0,0,0",
                SourceRadius=0.05,
            )
        ]),
        go("Ambient", components=[comp("Rinten.AmbientLight", "ambient", Color=ambient)]),
        go("2D Skybox", tags="skybox", components=[
            comp("Rinten.SkyBox2D", "sky", SkyIndirectLighting=True, SkyMaterial="materials/skybox/procedural.mat", Tint="1,1,1,1")
        ]),
    ])

def ground(size=40):
    return go(
        "Ground",
        pos=vec(0, -0.25, 0),
        scale=vec(size, 0.5, size),
        tags="world",
        components=[
            renderer("ground", "models/dev/box.mdl", "0.55,0.58,0.62,1", "materials/dev/grid.mat"),
            box_collider("ground"),
        ],
    )

def player(name="Player", pos="0,2.5,12", extra=None, camera_extra=None, speed=6.0):
    cam_id = uid("comp", "Rinten.CameraComponent", name + "-cam")
    cam_go = uid("go", name + "/Camera", "0,0,0")
    cam_comps = [
        {
            "__type": "Rinten.CameraComponent",
            "__guid": cam_id,
            "__enabled": True,
            "Flags": 0,
            "BackgroundColor": "0.05,0.06,0.08,1",
            "ClearFlags": "All",
            "EnablePostProcessing": True,
            "FieldOfView": 70,
            "FovAxis": "Horizontal",
            "IsMainCamera": True,
            "Orthographic": False,
            "OrthographicHeight": 10,
            "PostProcessAnchor": None,
            "Priority": 1,
            "RenderExcludeTags": "",
            "RenderTags": "",
            "RenderTexture": None,
            "TargetEye": "None",
            "Viewport": "0,0,1,1",
            "ZFar": 400,
            "ZNear": 0.05,
        },
        comp("Rinten.Bloom", name + "-bloom", __version=1, Mode="Additive", Strength=0.6, Threshold=1, Tint="1,1,1,1"),
    ]
    if camera_extra:
        cam_comps.extend(camera_extra)
    comps = [
        {
            "__type": "Template.Player",
            "__guid": uid("comp", "Template.Player", name),
            "__enabled": True,
            "Flags": 0,
            "Camera": {
                "_type": "component",
                "component_id": cam_id,
                "go": cam_go,
                "component_type": "CameraComponent",
            },
            "PitchClamp": 89,
            "RunScale": 3,
            "Speed": speed,
        }
    ]
    if extra:
        comps.extend(extra)
    p = go(name, pos=pos, components=comps, children=[
        {
            "__guid": cam_go,
            "__version": 2,
            "Flags": 0,
            "Name": "Camera",
            "Position": "0,0,0",
            "Rotation": IDENT,
            "Scale": "1,1,1",
            "Tags": "maincamera",
            "Enabled": True,
            "NetworkMode": 2,
            "NetworkFlags": 0,
            "NetworkOrphaned": 0,
            "NetworkTransmit": True,
            "OwnerTransfer": 1,
            "Components": cam_comps,
            "Children": [],
        }
    ])
    return p

def hud(title, note):
    return go("HUD", components=[
        comp("Rinten.ScreenPanel", "hud-panel", AutoScreenScale=True, Opacity=1, Scale=1, ScaleStrategy="ConsistentHeight", TargetCamera=None, ZIndex=100),
        comp("TestGround.SceneHud", "hud", Title=title, Note=note),
        comp("TestGround.ReturnToMenu", "return", Key="Q", MenuScene=None),
    ])

def scene(objects, guid_name):
    return {
        "__guid": uid("scene", guid_name),
        "GameObjects": objects,
        "SceneProperties": {
            "NetworkInterpolation": True,
            "TimeScale": 1,
            "WantsSystemScene": True,
            "Metadata": {},
            "NavMesh": {
                "Enabled": False,
                "IncludeStaticBodies": True,
                "IncludeKeyframedBodies": True,
                "EditorAutoUpdate": False,
                "AgentHeight": 1.6,
                "AgentRadius": 0.4,
                "AgentStepSize": 0.45,
                "AgentMaxSlope": 40,
                "ExcludedBodies": "",
                "IncludedBodies": "",
                "DeferGeneration": False,
                "CustomBounds": False,
            },
            "GameObjectSystems": {},
        },
        "ResourceVersion": 4,
        "Title": None,
        "Description": None,
        "__references": [],
        "__version": 4,
    }

def write(name, data):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")
    print("wrote", path)

# --- Prefabs scene ---
loose = []
for i, (x, z, tint) in enumerate((
    (-2.2, -1.5, "0.25,0.55,0.95,1"),
    (-1.4, -1.1, "0.95,0.45,0.2,1"),
    (-1.8, -0.4, "0.3,0.8,0.45,1"),
    (2.4, -1.2, "0.95,0.8,0.25,1"),
    (1.6, -0.6, "0.7,0.4,0.95,1"),
)):
    loose.append(primitive(
        f"Loose Cube {i+1}",
        pos=vec(x, 0.4, z),
        scale="0.45,0.45,0.45",
        model="models/dev/box.mdl",
        tint=tint,
        collider=box_collider(f"loose-{i}", static=False),
        extra=[rigidbody(f"loose-rb-{i}"), reset_on_fall(f"loose-reset-{i}")],
    ))

prefabs = scene([
    environment(),
    ground(36),
    label("Label: Spawn", vec(-4.5, 2.4, -3.5), "Spawner\nclones cube.prefab every second"),
    label("Label: Throw", vec(0, 2.8, 4), "Click to throw  ·  RMB grab  ·  E open the door"),
    label("Label: Door", vec(4.2, 2.6, -1.8), "Door\nIPressable, Use to swing"),
    label("Label: Platform", vec(0, 2.2, -6.5), "Oscillator\nkeyframed collider"),
    go("Spawner", pos=vec(-4.5, 3.2, -3.5), components=[
        comp("TestGround.Spawner", "spawner", Prefab="prefabs/cube.prefab", Interval=1.0, Lifetime=0.0),
        renderer("spawner-mark", "models/dev/sphere.mdl", "0.25,0.55,0.95,0.35"),
    ]),
    go("Door", pos=vec(4.2, 1.0, -1.8), scale="0.2,2,1.2", components=[
        renderer("door", "models/dev/box.mdl", "0.72,0.55,0.32,1"),
        box_collider("door", static=False),
        comp("TestGround.Door", "door-comp", Angle=90, Speed=6),
    ]),
    go("Platform", pos=vec(0, 0.15, -6.5), scale="2.4,0.2,1.2", components=[
        renderer("platform", "models/dev/box.mdl", "0.85,0.55,0.2,1"),
        box_collider("platform", static=False),
        comp("TestGround.Oscillator", "osc", Axis="0,1,0", Amplitude=0.8, Speed=0.45, Phase=0),
    ]),
    go("Loose Cubes", children=loose),
    player(extra=[
        comp("TestGround.Launcher", "launcher", Prefab="prefabs/cube.prefab", Action="Attack1", Offset=1.2, Speed=12, Lifetime=0),
        comp("TestGround.Grabber", "grabber", Action="Attack2", Reach=8, Smoothness=4),
        comp("TestGround.PlayerUse", "use", Action="Use", Reach=3),
    ]),
    hud("Prefabs", "Click throws cube.prefab. Right mouse grabs a body. E opens the door. Copies die after six seconds."),
], "prefabs")
write("general/prefabs.scene", prefabs)

# --- Trace scene ---
trace_wall = primitive(
    "Wall",
    pos=vec(0, 1.5, -4),
    scale="8,3,0.3",
    model="models/dev/box.mdl",
    tint="0.62,0.66,0.72,1",
    collider=box_collider("wall"),
)
trace_blocks = [
    primitive("Block A", vec(-2.2, 0.5, -1.5), "1,1,1", "models/dev/box.mdl", "0.2,0.45,0.9,1", box_collider("ba")),
    primitive("Block B", vec(0, 0.4, -0.5), "0.8,0.8,0.8", "models/dev/sphere.mdl", "0.95,0.45,0.2,1", sphere_collider("bb")),
    primitive("Block C", vec(2.2, 0.7, -1.8), "1.2,1.4,0.8", "models/dev/box.mdl", "0.3,0.8,0.45,1", box_collider("bc")),
]
trace = scene([
    environment(),
    ground(30),
    label("Label: Traces", vec(0, 3.4, -4), "Traces\nray, box and sphere from the camera"),
    trace_wall,
    go("Blocks", children=trace_blocks),
    go("Ray Probe", pos=vec(-3.5, 1.2, 2.5), components=[
        renderer("ray-mark", "models/dev/sphere.mdl", "0.35,0.75,0.95,1"),
        comp("TestGround.TraceProbe", "ray", Type="Ray", Length=8, BoxSize="0.15,0.15,0.15", Radius=0.15, DrawMiss=True),
    ]),
    go("Box Probe", pos=vec(0, 1.2, 3.2), components=[
        renderer("box-mark", "models/dev/box.mdl", "0.95,0.45,0.2,1"),
        comp("TestGround.TraceProbe", "box", Type="Box", Length=8, BoxSize="0.2,0.2,0.2", Radius=0.15, DrawMiss=True),
    ]),
    go("Sphere Probe", pos=vec(3.5, 1.2, 2.5), components=[
        renderer("sph-mark", "models/dev/sphere.mdl", "0.3,0.8,0.45,1"),
        comp("TestGround.TraceProbe", "sph", Type="Sphere", Length=8, BoxSize="0.15,0.15,0.15", Radius=0.22, DrawMiss=True),
    ]),
    player(camera_extra=[
        comp("TestGround.TraceProbe", "cam-trace", Type="Ray", Length=16, BoxSize="0.12,0.12,0.12", Radius=0.12, DrawMiss=True),
    ]),
    hud("Traces", "A ray follows the camera. Three probes on the floor sweep a ray, a box and a sphere at the wall."),
], "trace")
write("physics/trace.scene", trace)

# --- Overlay scene ---
overlay = scene([
    environment(),
    ground(28),
    label("Label: Overlay", vec(0, 2.6, 0), "Debug Overlay\nline, text, sphere, box"),
    go("Gallery", pos=vec(-4.8, 0, 0), components=[
        comp("TestGround.OverlayGallery", "gallery", Spacing=1.6),
    ]),
    player(pos="0,2.2,8"),
    hud("Overlay", "One of each debug overlay primitive, drawn every frame. A missing shape means that draw path is broken."),
], "overlay")
write("general/overlay.scene", overlay)

# --- Lights scene ---
light_cubes = []
for i, x in enumerate((-3.5, -1.2, 1.2, 3.5)):
    light_cubes.append(primitive(
        f"Cube {i+1}",
        pos=vec(x, 0.5, -1.5),
        scale="1,1,1",
        model="models/dev/box.mdl",
        tint="0.85,0.86,0.88,1",
        collider=box_collider(f"lc{i}"),
    ))

def point_light(name, pos, color, brightness, radius):
    return go(name, pos=pos, tags="light_point,light", components=[
        comp(
            "Rinten.PointLight", name,
            Attenuation=0.15,
            Brightness=brightness,
            FogMode="Enabled",
            FogStrength=1,
            LightColor=color,
            Radius=radius,
            Shadows=True,
            SourceRadius=0.05,
            Contribution="Diffuse, Specular, Transmissive",
        )
    ])

lights = scene([
    environment(sun_brightness=0.12, ambient="0.03,0.035,0.05,1"),
    ground(32),
    label("Label: Lights", vec(0, 3.2, -3), "Lights\npoint, spot, coloured pools"),
    go("Cubes", children=light_cubes),
    primitive("Pillar", vec(0, 1.5, 2.5), "0.4,3,0.4", "models/dev/box.mdl", "0.7,0.72,0.76,1", box_collider("pillar")),
    point_light("Red Point", vec(-3.5, 1.8, 0.4), "1,0.25,0.18,1", 28, 8),
    point_light("Green Point", vec(0, 1.8, 0.4), "0.25,1,0.4,1", 22, 8),
    point_light("Blue Point", vec(3.5, 1.8, 0.4), "0.3,0.45,1,1", 28, 8),
    go("Spot", pos=vec(0, 4.2, 2.5), rot=LOOK_DOWN, tags="light_spot,light", components=[
        comp(
            "Rinten.SpotLight", "spot",
            Attenuation=0.15,
            Brightness=40,
            ConeInner=18,
            ConeOuter=38,
            FogMode="Enabled",
            FogStrength=1,
            LightColor="1,0.95,0.8,1",
            Radius=12,
            Shadows=True,
            SourceRadius=0.08,
            Contribution="Diffuse, Specular, Transmissive",
        )
    ]),
    player(pos="0,2.4,10"),
    hud("Lights", "The sun is almost out. Three coloured point lights and a spot from above. Walk the cubes and watch the shadows."),
], "lights")
write("rendering/lights.scene", lights)

# --- Fog scene ---
fog_row = []
for i in range(8):
    z = -2 - i * 3.2
    fog_row.append(primitive(
        f"Post {i+1}",
        pos=vec((-1.6 if i % 2 == 0 else 1.6), 1.0, z),
        scale="0.5,2,0.5",
        model="models/dev/box.mdl",
        tint="0.75,0.78,0.82,1",
        collider=box_collider(f"post{i}"),
    ))

fog = scene([
    environment(sun_brightness=0.9, ambient="0.22,0.24,0.28,1"),
    ground(48),
    label("Label: Fog", vec(0, 3.0, 2), "Fog\ngradient in the distance, volume in the hollow"),
    go("Posts", children=fog_row),
    go("Gradient Fog", pos=vec(0, 0, 0), components=[
        comp(
            "Rinten.GradientFog", "grad",
            Color="0.55,0.62,0.72,0.85",
            Height=6,
            VerticalFalloffExponent=1.4,
            StartDistance=6,
            EndDistance=28,
            FalloffExponent=1.2,
        )
    ]),
    go("Volume Fog", pos=vec(0, 1.2, -12), components=[
        comp(
            "Rinten.VolumetricFogVolume", "vol",
            Bounds={"Mins": "-6,-1.5,-8", "Maxs": "6,4,8"},
            Strength=0.7,
            FalloffExponent=0.6,
            Color="0.7,0.78,0.88,1",
        )
    ]),
    player(pos="0,2.4,8"),
    hud("Fog", "Gradient fog eats the row of posts with distance. A volumetric volume sits in the hollow halfway down."),
], "fog")
write("rendering/fog.scene", fog)

# --- Sound scene ---
def sound_point(name, pos, event, repeat=True, distance=14, volume=1.0, pitch=1.0):
    return go(name, pos=pos, components=[
        renderer(name + "-mark", "models/dev/sphere.mdl", "0.4,0.85,0.55,0.45"),
        comp(
            "Rinten.SoundPointComponent", name,
            Distance=distance,
            DistanceAttenuation=True,
            DistanceAttenuationOverride=True,
            Falloff=[
                {"x": 0, "y": 1, "in": 3.1415927, "out": -3.1415927, "mode": "Mirrored"},
                {"x": 1, "y": 0, "in": 0, "out": 0, "mode": "Mirrored"},
            ],
            Force2d=False,
            MaxRepeatTime=1,
            MinRepeatTime=1,
            Occlusion=False,
            OcclusionOverride=False,
            OcclusionRadius=0.8,
            Pitch=pitch,
            PlayOnStart=True,
            ReflectionOverride=False,
            Reflections=False,
            Repeat=repeat,
            SoundEvent=event,
            SoundOverride=True,
            StopOnNew=False,
            TargetMixer={"Name": "unknown", "Id": "00000000-0000-0000-0000-000000000000"},
            Volume=volume,
        ),
    ])

sound = scene([
    environment(),
    ground(28),
    label("Label: Near", vec(-4, 2.2, -2), "Fire loop\nclose, loud"),
    label("Label: Mid", vec(0, 2.2, -6), "Metal impacts\nevery second"),
    label("Label: Far", vec(5, 2.2, -10), "Crow\nfar, quiet"),
    sound_point("Fire", vec(-4, 0.6, -2), "sounds/effects/fire/fire_burn_loop01.sound", True, 10, 0.9, 1.0),
    sound_point("Metal", vec(0, 0.6, -6), "sounds/impacts/melee/impact-melee-metal.sound", True, 12, 0.8, 1.0),
    sound_point("Crow", vec(5, 1.4, -10), "sounds/ambience/stings/sting-crow.sound", True, 18, 0.7, 1.0),
    go("Sound Box", pos=vec(3.5, 1.0, -2), components=[
        renderer("box-mark", "models/dev/box.mdl", "0.4,0.7,0.95,0.25"),
        box_collider("sbox", trigger=True, static=True),
        comp(
            "Rinten.SoundBoxComponent", "sbox",
            Scale="4,3,4",
            Distance=10,
            DistanceAttenuation=True,
            DistanceAttenuationOverride=True,
            Falloff=[
                {"x": 0, "y": 1, "in": 3.1415927, "out": -3.1415927, "mode": "Mirrored"},
                {"x": 1, "y": 0, "in": 0, "out": 0, "mode": "Mirrored"},
            ],
            Force2d=False,
            MaxRepeatTime=2.5,
            MinRepeatTime=1.5,
            Occlusion=False,
            OcclusionOverride=False,
            OcclusionRadius=0.8,
            Pitch=1,
            PlayOnStart=True,
            ReflectionOverride=False,
            Reflections=False,
            Repeat=True,
            SoundEvent="sounds/kenney/ui/ui.button.press.sound",
            SoundOverride=True,
            StopOnNew=False,
            TargetMixer={"Name": "unknown", "Id": "00000000-0000-0000-0000-000000000000"},
            Volume=0.6,
        ),
    ]),
    player(pos="0,2.2,6", extra=[
        comp("Rinten.AudioListener", "listener", UseCameraDirection=True),
    ]),
    hud("Sound", "Walk between the points. Fire is close, metal sits mid-field, the crow is far. A sound box ticks on the right."),
], "sound")
write("general/sound.scene", sound)

# --- World UI scene ---
def tagged(name, pos, tint, title, note):
    return go(name, pos=pos, scale="0.8,0.8,0.8", components=[
        renderer(name, "models/dev/box.mdl", tint),
        box_collider(name),
        comp(
            "Rinten.WorldPanel", name + "-panel",
            HorizontalAlign="Center",
            InteractionRange=6,
            LookAtCamera=True,
            PanelSize="420,180",
            RenderOptions={"GameLayer": True, "OverlayLayer": False, "BloomLayer": False, "AfterUILayer": False},
            RenderScale=1,
            VerticalAlign="Center",
        ),
        comp("TestGround.WorldLabel", name + "-label", Title=title, Note=note),
    ])

worldui = scene([
    environment(),
    ground(24),
    label("Label: World UI", vec(0, 3.0, -2), "World Panels\nUI sitting on objects, facing the camera"),
    tagged("Alpha", vec(-2.4, 0.4, -1.5), "0.25,0.55,0.95,1", "Alpha", "A panel on a cube"),
    tagged("Beta", vec(0, 0.4, -2.2), "0.95,0.5,0.2,1", "Beta", "LookAtCamera is on"),
    tagged("Gamma", vec(2.4, 0.4, -1.5), "0.3,0.8,0.45,1", "Gamma", "Click through World Input"),
    player(pos="0,2.2,6", camera_extra=[
        comp("Rinten.WorldInput", "winput", LeftMouseAction="Attack1", RightMouseAction="Attack2", VRHandSource="Left"),
    ]),
    hud("World UI", "Three world panels sit on cubes and turn to face you. Screen UI is the other showcase; this is UI in the scene."),
], "worldui")
write("ui/world.scene", worldui)

print("done")
