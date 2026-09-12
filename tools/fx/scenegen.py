#!/usr/bin/env python3
"""Writes scenes/FX.scene for the test ground: a row of stations, one effect each."""
import json, uuid, os

ROOT = "/home/sampesss/Documents/Rinten Projects/Rinten-Test-Ground/Assets"

def guid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "rinten-fx-scene/" + name))

EVENTS = {"OnComponentDestroy": None, "OnComponentDisabled": None, "OnComponentEnabled": None,
          "OnComponentFixedUpdate": None, "OnComponentStart": None, "OnComponentUpdate": None}

def v(*a): return ",".join(str(x) for x in a)

def go(name, pos=(0, 0, 0), rot="0,0,0,1", scale=(1, 1, 1), tags="", components=(), children=()):
    return {"__guid": guid("go/" + name), "__version": 2, "Flags": 0, "Name": name,
            "Position": v(*pos), "Rotation": rot, "Scale": v(*scale), "Tags": tags, "Enabled": True,
            "NetworkMode": 2, "NetworkFlags": 0, "NetworkOrphaned": 0, "NetworkTransmit": True, "OwnerTransfer": 1,
            "Components": list(components), "Children": list(children)}

def comp(type_, name, **props):
    d = {"__type": type_, "__guid": guid("comp/" + name), "__enabled": True, "Flags": 0}
    d.update(props)
    d.update(EVENTS)
    return d

RENDER = {"GameLayer": True, "OverlayLayer": False, "BloomLayer": False, "AfterUILayer": False}

def model(name, tint, material=None, model="models/dev/box.mdl"):
    return comp("Rinten.ModelRenderer", "model/" + name, BodyGroups=18446744073709551615, CreateAttachments=False, MaterialGroup=None,
                MaterialOverride=material, Materials=None, Model=model, RenderOptions=RENDER, RenderType="On", Tint=tint)

def box_collider(name):
    return comp("Rinten.BoxCollider", "collider/" + name, Center="0,0,0", ColliderFlags=0, Elasticity=None, Friction=None, IsTrigger=False,
                OnObjectTriggerEnter=None, OnObjectTriggerExit=None, OnTriggerEnter=None, OnTriggerExit=None,
                RollingResistance=None, Scale="1,1,1", Static=True, Surface=None, SurfaceVelocity="0,0,0")

def block(name, pos, scale, tint, material=None):
    return go(name, pos, scale=scale, tags="world", components=[model(name, tint, material), box_collider(name)])

def label(name, pos, text, scale=0.26):
    return go(f"Label: {name}", pos, components=[comp("Rinten.TextRenderer", "label/" + name, __version=2,
        Billboard="YOnly", BlendMode="Normal", FogStrength=1, HorizontalAlignment="Center", RenderOptions=RENDER, Scale=scale,
        TextScope={"Text": text, "TextColor": "0.9,0.94,1,1", "FontName": "Poppins", "FontSize": 50, "FontWeight": 700,
                   "FontItalic": False, "FontVariantNumeric": "Normal", "LineHeight": 1.1, "LetterSpacing": 0, "WordSpacing": 0,
                   "FilterMode": "Bilinear", "FontSmooth": "Auto",
                   "Outline": {"Enabled": False, "Size": 4, "Color": "0,0,1,1"},
                   "Shadow": {"Enabled": True, "Size": 6, "Color": "0,0,0,0.8", "Offset": "3,3"},
                   "OutlineUnder": {"Enabled": False, "Size": 4, "Color": "0,1,0,1"},
                   "ShadowUnder": {"Enabled": False, "Size": 4, "Color": "0,0,0,1", "Offset": "4,4"}},
        VerticalAlignment="Center")])

def player(name, fx, pos, rot="0,0,0,1"):
    return go(name, pos, rot, components=[comp("Rinten.ParticlePlayer", "fx/" + name, Definition=f"fx/{fx}.fx",
        DestroyOnEnd=False, FloatOverrides={}, VectorOverrides={}, ColorOverrides={})])

# ---------------------------------------------------------------- the row

Z = 0
PEDESTAL = "0.2,0.22,0.26,1"
stations = []

# Every station is registered by name and placed later, area by area - see
# AREAS at the bottom. The x handed in is ignored; it is the row's old order.
registry = {}

# What each sign says: a title, one line of what it shows, one line of its
# parameters. Short, because the text renderer clips long lines and nobody
# reads a paragraph over a fountain.
SIGNS = {
    "Campfire":       ("Campfire",        "flames, embers, smoke",                       "Intensity, Wind, Flame"),
    "Chimney":        ("Chimney",         "lit smoke on the wind",                       "Volume, Wind"),
    "Explosion":      ("Explosion",       "flash, shockwave, 3D chunks, smoke",          "Power, Sparks, Debris"),
    "Gunshot":        ("Gunshot",         "muzzle flash, tracer, brass casing",          "Spread, Tracer"),
    "Fountain":       ("Fountain",        "a jet, drops that land",                      "Jet, Water"),
    "Confetti":       ("Confetti",        "tumbling paper, collisions",                  "Amount, Paper"),
    "Fireflies":      ("Fireflies",       "motes on curl noise, a light each",           "Count, Glow"),
    "Sparkler":       ("Sparkler",        "sparks with ribbons, bouncing",               "Rate, Force, Color"),
    "Snowfall":       ("Snowfall",        "a 7 m box of drifting flakes",                "Density, Wind"),
    "Rain":           ("Rain",            "drops from 7 m, splashes where they land",    "Density, Speed, Wind"),
    "Tornado":        ("Dust Devil",      "a shell of dust spun by Orbit",               "Spin, Density"),
    "Magic Orb":      ("Magic Orb",       "a shell pulled in and spun",                  "Spin, Pull, Aura"),
    "Portal":         ("Portal",          "a ring, orbiting motes",                      "Spin, Glow"),
    "Beam":           ("Energy Beam",     "a beam with rings and sparks",                "Power, Length"),
    "Singularity":    ("Singularity",     "a core, a disc, infalling streaks",           "Spin, Pull, Density"),
    "Firework":       ("Firework",        "rocket, burst, crackle - timed",              "Height, Burst"),
    "Slash":          ("Slash",           "two crescents riding Circle shapes",          "Width, Sparks"),
    "Formation":      ("Formation",       "Grid -> Ring -> Helix, By Index",             "Ring, Helix, Spin"),
    "Snake":          ("Snake",           "a Spline by time; sparks remember home",      "Speed, Sparks, Pull"),
    "DNA":            ("DNA",             "two Helix shapes, chained Follow weights",    "Spin, Size, Fizz"),
    "Jelly":          ("Jelly",           "400 motes held by a slot each",               "Stiffness, Shake"),
    "Orrery":         ("Orrery",          "mesh planets on Circle shapes, by the clock", "Spin, Glow, colours"),
    "Buff Aura":      ("Buff Aura",       "runes By Index, helix streamers, cone rim",   "Spin, Rise, Intensity"),
    "Mesh Fire":      ("Stylised Fire",   "one mesh, blend shapes, dissolve shader",     "Intensity, Sway, Burn"),
    "Shield":         ("Shield",          "a mesh that breathes, rim-lit, holed",        "Breathe, Spikes, Holes"),
    "Shards":         ("Shards",          "3D chunks that land still and burn away",     "Count, Force, Burn"),
    "Assemble":       ("Assemble",        "48 shards Goal onto a Grid, then burn",       "Gather, Glow"),
    "Shatter":        ("Shatter",         "an urn in 16 pieces, back together by Goal",  "Assemble, Force"),
    "Meteor":         ("Meteor",          "a rock with a fire ribbon, an impact",        "Speed, Trail, Impact"),
    "Homing":         ("Homing",          "missiles pulled onto a moving anchor",        "Rate, Pull"),
    "Tesla":          ("Tesla",           "bolts between two moving anchors",            "Arcs"),
    "Chain Reaction": ("Chain Reaction",  "events hand colour and direction down",       "Rate, Fuse"),
}

def sign(name, title, note):
    if name in SIGNS:
        t, what, params = SIGNS[name]
        return f"{t}\n{what}\nparams: {params}"
    return f"{title}\n{note}"

def station(x, name, fx, title, note, y=0.3, rot="0,0,0,1", pedestal=True, label_y=4.6):
    def build(px, pz):
        kids = []
        if pedestal:
            kids.append(block(f"Pedestal: {name}", (0, 0.1, 0), (1.4, 0.2, 1.4), PEDESTAL))
        kids.append(player(name, fx, (0, y, 0), rot))
        kids.append(label(name, (0, label_y, 0), sign(name, title, note)))
        return go(f"Station: {name}", (px, 0, pz), children=kids)
    registry[name] = build

def bound_player(name, fx, pos, bindings):
    """A player whose anchors are bound to objects of the station."""
    return go(name, pos, components=[comp("Rinten.ParticlePlayer", "fx/" + name, Definition=f"fx/{fx}.fx",
        DestroyOnEnd=False, FloatOverrides={}, VectorOverrides={}, ColorOverrides={},
        AnchorBindings=[{"Name": a, "Target": guid("go/" + target), "Bone": None, "Offset": "0,0,0"} for a, target in bindings])])

def swing(name, axis, amplitude, period, hold=0.0, phase=0.0):
    return comp("TestGround.Swing", "swing/" + name, Axis=",".join(map(str, axis)), Amplitude=amplitude, Period=period, Hold=hold, Phase=phase)

def tesla_station(x, name, title, note):
    # Two arms swinging out of step, a ball on each; the effect's A and B
    # anchors are bound to the balls, and the arcs follow wherever they go.
    def arm(tag, x_, phase):
        ball = go(f"Tesla Ball {tag}", (0, 0, -1.2), scale=(0.2, 0.2, 0.2), components=[model(f"Tesla Ball {tag}", "0.7,0.8,1,1", model="models/dev/sphere.mdl")])
        return go(f"Tesla Arm {tag}", (x_, 1.5, 0), components=[swing(f"Tesla Arm {tag}", (0, 1, 0), 55, 2.6, phase=phase)], children=[ball])
    def build(px, pz):
        kids = [block(f"Pedestal: {name}", (0, 0.1, 0), (1.4, 0.2, 1.4), PEDESTAL), arm("A", -1.4, 0.0), arm("B", 1.4, 0.5),
                bound_player(name, "tesla", (0, 0, 0), [("A", "Tesla Ball A"), ("B", "Tesla Ball B")]),
                label(name, (0, 4.6, 0), sign(name, title, note))]
        return go(f"Station: {name}", (px, 0, pz), children=kids)
    registry[name] = build

def homing_station(x, name, title, note):
    ball = go("Homing Target", (0, 0, -2.2), scale=(0.25, 0.25, 0.25), components=[model("Homing Target", "1,0.4,0.3,1", model="models/dev/sphere.mdl")])
    arm = go("Homing Arm", (0, 1.6, 0), components=[swing("Homing Arm", (0, 1, 0), 70, 3.2)], children=[ball])
    def build(px, pz):
        kids = [block(f"Pedestal: {name}", (0, 0.1, 0), (1.4, 0.2, 1.4), PEDESTAL), arm,
                bound_player(name, "homing", (0, 0, 0), [("Target", "Homing Target")]),
                label(name, (0, 4.6, 0), sign(name, title, note))]
        return go(f"Station: {name}", (px, 0, pz), children=kids)
    registry[name] = build

# Fourteen metres apart, big ones at the ends. Nineteen effects in a row, the
# spawn in the middle of it.
X = iter(range(-224, 225, 14))

station(next(X), "Mesh Fire", "mesh_fire", "Stylised Fire (mesh)",
        "one flame mesh: three blend shapes on curves, a dissolve shader driven per particle\nIntensity, Flicker, Sway, Burn, Speed and Tint are parameters", y=0.3)
station(next(X), "Shield", "mesh_shield", "Shield (mesh)",
        "a sphere that breathes and spikes by morph, rim-lit and holed by the same shader\nBreathe, Spikes, Holes, Rim and Tint are parameters", y=1.6)
station(next(X), "Shards", "mesh_shards", "Dissolving Shards (mesh)",
        "3D chunks that bounce and burn away - Dissolve and Emission on curves over each life\nCount, Force, Burn and Intensity are parameters", y=0.3)
station(next(X), "Formation", "formation", "Formation (shapes)",
        "96 beads parked on a Grid shape By Index, blended to a Ring and a Helix by Follow Shape -\ncolour and size read By Index. Ring, Helix, Spin and Size are parameters", y=0.3)
station(next(X), "Snake", "snake", "Snake (spline + slots)",
        "a head riding a closed Spline shape by time with a ribbon body, scales on the same path,\nsparks that Remember their birth point in a slot and are pulled back to it. Speed, Sparks and Pull are parameters", y=0.3)
station(next(X), "Buff Aura", "buff_aura", "Buff Aura (real case)",
        "what a heal or level-up needs: runes on a ring By Index turned by the clock, streamers riding a helix\nwith ribbons, motes off a cone's rim - every shape offset from the feet. Spin, Rise, Intensity, Size are parameters", y=0.3)
station(next(X), "DNA", "dna", "DNA (two shapes, chained weights)",
        "two helix shapes, one turned half a circle; beads parked By Index on each and turned by Speed;\nrungs are Follow A then Follow B at weight 0.5 - the midpoint. Spin, Size and Fizz are parameters", y=0.3)
station(next(X), "Jelly", "jelly", "Jelly (slots)",
        "400 motes fill a box, each Remembers its birth point in slot Home, and one attractor reading\nthat slot springs every mote back - noise shakes it, it wobbles. Stiffness, Shake, Damping are parameters", y=0.3)
station(next(X), "Slash", "slash", "Slash (shapes + drivers)",
        "the cut, not the sword: two crescents in an X, each one particle riding an arc of a Circle shape with a\ntapering ribbon and a white core, sparks on the arc, a ring pushed out by Transform Over Life. Width, Sparks", y=1.3)
station(next(X), "Assemble", "assemble", "Assemble (Goal + mesh + shader)",
        "48 dissolve-shader shards scattered in a sphere, pulled by a Goal onto a grid wall By Index - position and\nrotation on one curve - lock, hold, burn away with a crackle each. Gather, Glow, Size are parameters", y=0.3)
station(next(X), "Shatter", "shatter", "Shatter / Assemble (model parts)",
        "a real urn broken into 16 pieces in Blender: each particle is born on the Model shape By Parts and draws\nonly its piece; a Goal back to the same shape is the urn whole. Assemble, Force, Glow are parameters", y=0.3)
station(next(X), "Chain Reaction", "chain_rocket", "Chain Reaction (events + context)",
        "a rocket born a random colour kills itself On Time and spawns a burst told its Color and Velocity;\neach spark that lands spawns a pop told the colour again. Rate and Fuse are parameters", y=0.3)
tesla_station(next(X), "Tesla", "Tesla (anchors + Goal)",
        "arcs between two anchors on two swinging arms: each bolt is a particle whose Goal runs it along the Line\nbetween them at weight 0.8 - the rest is its own noised motion, the zigzag. Arcs is a parameter")
homing_station(next(X), "Homing", "Homing (Goal + Transform Over Life)",
        "missiles thrown anywhere, pulled onto a moving anchor by a Goal weight curve; launch puffs rise and grow\nby Transform Over Life; the glow rides the target. Rate and Pull are parameters")
station(next(X), "Meteor", "meteor", "Meteor",
        "a 3D sphere falling with a fire ribbon; where it lands it plays impact.fx -\n3D rubble that bounces, a shockwave, dust. Speed, Trail and Impact are parameters", y=0.3, label_y=5.2)
station(next(X), "Singularity", "singularity", "Singularity",
        "a 3D core, an accretion disc and infalling streaks with ribbons\nSpin, Pull, Density and three gradients are parameters", y=2.4)

station(next(X), "Snowfall", "snow", "Snowfall",
        "a seven metre box of flakes drifting on curl noise, lit\nDensity and Wind are parameters", y=5.2, pedestal=False, label_y=7.4)
station(next(X), "Rain", "rain", "Rain",
        "stretched drops born seven metres up, splashes and rings where they land\nDensity, Speed, Splash, Wind and the Water colour are parameters", y=0.05, pedestal=False, label_y=8.6)
station(next(X), "Tornado", "tornado", "Dust Devil",
        "a shell of dust spun up by a vortex and pushed out as it climbs\nSpin and Density are parameters", y=0.1)
station(next(X), "Chimney", "chimney", "Chimney",
        "slow lit smoke carried off by the wind, with faster wisps inside it\nVolume and Wind are parameters", y=0.3)
station(next(X), "Campfire", "fire", "Campfire",
        "flames, embers and smoke\nIntensity, Wind and the Flame gradient are parameters")
station(next(X), "Explosion", "explosion", "Explosion",
        "flash, shockwave, fireball, sparks that bounce, 3D stone chunks that land and lie still, smoke\nPower, Sparks and Debris scale it - bursts every 3.5 s")
next(X)
registry["Gunshot"] = lambda px, pz: go("Station: Gunshot", (px, 0, pz), children=[
    block("Post: Gunshot", (0, 0.6, 0), (0.18, 1.2, 0.18), PEDESTAL),
    player("Gunshot", "gunshot", (0, 1.25, 0), "0,-0.5,0,0.8660254"),
    label("Gunshot", (0, 4.6, 0), sign("Gunshot", "Gunshot", "")),
])
station(next(X), "Magic Orb", "magic_orb", "Magic Orb",
        "a sphere shell pulled inward and spun by a vortex, motion-blurred\nSpin, Pull and the Aura gradient are parameters", y=1.7)
station(next(X), "Portal", "portal", "Portal",
        "two counter-flowing rings on a vertical circle, lit from the sheet\nSpeed and the Glow gradient are parameters",
        y=2.0, rot="-0.7071068,0,0,0.7071068")
# Turned to run along the row, so the beam is seen side-on rather than end-on.
station(next(X), "Beam", "beam", "Energy Beam",
        "particles born along a line, an impact at the far end\nthe Beam gradient is a parameter", y=1.4, rot="0,-0.7071068,0,0.7071068")
station(next(X), "Fountain", "fountain", "Fountain",
        "a jet under gravity, droplets that collide with the ground and die\nJet velocity and Water colour are parameters", y=0.25)
station(next(X), "Firework", "firework", "Firework (timed)",
        "a rocket, its trail, and a burst timed to where it should be by then\nStars, Size and the Stars gradient are parameters", y=0.3, label_y=3.2)
station(next(X), "Firework Chain", "firework_chain", "Firework (chained)",
        "the rocket plays firework_burst.fx where it actually dies, and every star\nplays crackle.fx where it goes out - three files, Effect On Death between them", y=0.3, label_y=3.2)
station(next(X), "Sparkler", "sparkler", "Sparkler",
        "sparks with ribbons behind them, bouncing off the ground\nRate, Force and the Color gradient are parameters", y=1.6)
station(next(X), "Orrery", "swarm", "Orrery",
        "a sun mesh in the ember shader, three mesh planets parked on tilted Circle shapes and turned by the clock,\neach with a ribbon and a light; orbits are dots parked By Index. Spin, Glow and the planet colours are parameters", y=2.4)
station(next(X), "Confetti", "confetti", "Confetti",
        "tumbling paper on its own rotation, colliding with the ground\nAmount and the Paper colours are parameters", y=0.4)
station(next(X), "Fireflies", "fireflies", "Fireflies",
        "slow motes on curl noise, each one a flicker and a light\nCount and the Glow gradient are parameters", y=1.8, pedestal=False)

# ---------------------------------------------------------------- the areas
#
# Rows of stations by what they show, each on its own slab with a wall
# behind it and a title in front, front row nearest the spawn.
AREAS = [
    ("Basics", "sprites, forces, collisions",
     ["Campfire", "Chimney", "Explosion", "Gunshot", "Fountain", "Confetti", "Fireflies", "Sparkler"]),
    ("Weather", "volumes, wind, noise",
     ["Snowfall", "Rain", "Tornado"]),
    ("Magic and Energy", "additive layers, orbits, timing",
     ["Magic Orb", "Portal", "Beam", "Singularity", "Firework", "Slash"]),
    ("Shapes and Slots", "geometry by index and time, memory",
     ["Formation", "Snake", "DNA", "Jelly", "Orrery", "Buff Aura"]),
    ("Meshes and Models", "blend shapes, shader rows, pieces",
     ["Mesh Fire", "Shield", "Shards", "Assemble", "Shatter", "Meteor"]),
    ("Anchors and Events", "bound poses, goals, chained effects",
     ["Homing", "Tesla", "Chain Reaction"]),
]

SPACING = 14
ROW_DEPTH = 30
SLAB = "0.34,0.36,0.4,1"
WALL = "0.11,0.12,0.15,1"

area_objects = []
missing = []
for k, (title, note, names) in enumerate(AREAS):
    z = -8 - k * ROW_DEPTH
    n = len(names)
    width = n * SPACING + 8
    kids = [
        block(f"Slab: {title}", (0, -0.2, z), (width, 0.4, 20), SLAB, "materials/dev/grid.mat"),
        block(f"Wall: {title}", (0, 5, z - 10), (width, 10, 0.5), WALL),
        label(f"Area: {title}", (0, 12.2, z - 6), f"{title}\n{note}", scale=1.3),
    ]
    for i, name in enumerate(names):
        x = (i - (n - 1) / 2) * SPACING
        if name not in registry:
            missing.append(name); continue
        kids.append(registry[name](x, z))
    area_objects.append(go(f"Area: {title}", children=kids))
if missing:
    raise SystemExit(f"stations not registered: {missing}")
placed = {name for _, _, names in AREAS for name in names}
unplaced = [name for name in registry if name not in placed]
if unplaced:
    print("not placed (left out on purpose?):", unplaced)

# ---------------------------------------------------------------- the scene

objects = [
    go("Environment", children=[
        go("Sun", rot="-0.4508033,0.1919843,0.0999407,0.8659851", tags="light_directional,light", components=[
            comp("Rinten.DirectionalLight", "sun", __version=1, Attenuation=1, Brightness=1.2, Contribution="Diffuse, Specular, Transmissive",
                 FogMode="Enabled", FogStrength=1, LightColor="1,0.95,0.88,1", ShadowAngle=0.6, ShadowDetail=64, Shadows=True,
                 SkyColor="0,0,0,0", SourceRadius=0.05)]),
        go("Ambient", components=[comp("Rinten.AmbientLight", "ambient", Color="0.2,0.22,0.3,1")]),
        go("2D Skybox", tags="skybox", components=[comp("Rinten.SkyBox2D", "sky", SkyIndirectLighting=True,
            SkyMaterial="materials/skybox/procedural.mat", Tint="0.75,0.8,0.9,1")]),
    ]),
    block("Ground", (0, -0.6, -80), (160, 0.5, 220), "0.2,0.21,0.24,1"),
    go("Areas", children=area_objects),
    go("Player", (0, 2.6, 14), components=[comp("Template.Player", "player",
        Camera={"_type": "component", "component_id": guid("comp/camera"), "go": guid("go/Camera"), "component_type": "CameraComponent"},
        PitchClamp=89, RunScale=3, Speed=7)], children=[
        go("Camera", rot="-0.0697565,0,0,0.9975641", tags="maincamera", components=[
            comp("Rinten.CameraComponent", "camera", BackgroundColor="0.05,0.06,0.08,1", ClearFlags="All", EnablePostProcessing=True,
                 FieldOfView=75, FovAxis="Horizontal", IsMainCamera=True, Orthographic=False, OrthographicHeight=10,
                 PostProcessAnchor=None, Priority=1, RenderExcludeTags="", RenderTags="", RenderTexture=None, TargetEye="None",
                 Viewport="0,0,1,1", ZFar=400, ZNear=0.05),
            comp("Rinten.Bloom", "bloom", __version=1, Mode="Additive", Spread=0.6, Strength=0.8, Threshold=1, Tint="1,1,1,1"),
        ])]),
    go("HUD", components=[
        comp("Rinten.ScreenPanel", "hud/panel", AutoScreenScale=True, Opacity=1, Scale=1, ScaleStrategy="ConsistentHeight", TargetCamera=None, ZIndex=100),
        comp("TestGround.SceneHud", "hud/scene", Note="Six rows of effects from the particle editor. Walk back through them; Q returns.", Title="Particles"),
        comp("TestGround.ReturnToMenu", "hud/return", Key="Q", MenuScene=None),
    ]),
]

scene = {
    "__guid": "b8267682-fc9d-4a10-a42e-ead098314174",
    "SceneProperties": {
        "NetworkInterpolation": True, "TimeScale": 1, "WantsSystemScene": True, "Metadata": {},
        "NavMesh": {"Enabled": False, "IncludeStaticBodies": True, "IncludeKeyframedBodies": True, "EditorAutoUpdate": False,
                    "AgentHeight": 1.6, "AgentRadius": 0.4, "AgentStepSize": 0.45, "AgentMaxSlope": 40,
                    "ExcludedBodies": "", "IncludedBodies": "", "DeferGeneration": False, "CustomBounds": False},
        "GameObjectSystems": {"Rinten.SelectionSetsSystem": {"Data": {"SelectionSets": []}}},
    },
    "GameObjects": objects,
    "ResourceVersion": 4, "Title": "Particles", "Description": "Fire, explosion, gunshot, magic, water, snow and a portal - the particle editor's effects with their parameters.",
    "__references": [], "__version": 4,
}

path = os.path.join(ROOT, "scenes/FX.scene")
with open(path, "w") as f:
    json.dump(scene, f, indent=2)
print("wrote", path)
