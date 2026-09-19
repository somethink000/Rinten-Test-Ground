#!/usr/bin/env python3
"""Writes scenes/Shadows.scene: the sun over a long field for its cascades and
detail, every kind of caster, source radii, point and spot lights with their
own shadows, lights and casters that move, and the surfaces shadows land on.
The sun's own settings are on the number keys - see ShadowRack."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from common import Scene, RENDER, v, yaw, pitch_yaw, register_in_menu

S = Scene("shadows", "Shadows",
          "The sun's cascades and detail over a long field, every kind of caster, source radii, point and spot shadows, moving lights and casters, and the surfaces they land on.")

PEDESTAL = "0.2,0.22,0.26,1"
FLOOR = "0.62,0.6,0.56,1"

def sign(name, text, pos, scale=0.38):
    return S.label(name, pos, text, scale=scale, size=44)

def station(name, text, children, pos, sign_y=3.0, pedestal=True):
    kids = []
    if pedestal: kids.append(S.block(f"Pedestal: {name}", (0, 0.1, 0), (1.6, 0.2, 1.6), PEDESTAL))
    kids.append(sign(name, text, (0, sign_y, 0)))
    return S.go(f"Station: {name}", pos, children=kids + list(children))

def cube(name, pos, size=(0.8, 0.8, 0.8), tint="0.85,0.8,0.7,1", material=None, render="On", rot="0,0,0,1", model="models/dev/box.mdl", extra=()):
    return S.go(name, pos, rot=rot, scale=size, components=[S.model(name, tint, material, model, render), *extra])

# Brightness is what the Lights scene uses for a pool that reads: tens, with
# the attenuation low, not the sun's ones.
def point_light(name, pos, color="1,1,1,1", brightness=6.0, radius=8.0, shadows=True, source=0.05, extra=()):
    return S.go(f"Light: {name}", pos, tags="light_point,light", components=[S.comp("Rinten.PointLight", "light/" + name, __version=1,
        Attenuation=0.15, Brightness=brightness, Contribution="Diffuse, Specular, Transmissive", FogMode="Enabled", FogStrength=1,
        LightColor=color, Radius=radius, Shadows=shadows, SourceRadius=source), *extra])

def spot_light(name, pos, rot, color="1,1,1,1", brightness=12.0, radius=12.0, outer=35.0, inner=25.0, shadows=True, cookie=None, source=0.05, extra=()):
    return S.go(f"Light: {name}", pos, rot=rot, tags="light_spot,light", components=[S.comp("Rinten.SpotLight", "light/" + name, __version=1,
        Attenuation=0.15, Brightness=brightness, ConeInner=inner, ConeOuter=outer, Contribution="Diffuse, Specular, Transmissive", Cookie=cookie,
        FogMode="Enabled", FogStrength=1, LightColor=color, Radius=radius, Shadows=shadows, SourceRadius=source), *extra])

def spinner(name, axis=(0, 1, 0), speed=45.0):
    return S.comp("TestGround.Spinner", "spin/" + name, Axis=v(*axis), Speed=speed, Local=True)

def oscillator(name, axis=(0, 1, 0), amplitude=1.0, speed=0.5, phase=0.0):
    return S.comp("TestGround.Oscillator", "osc/" + name, Axis=v(*axis), Amplitude=amplitude, Speed=speed, Phase=phase)

def orbit(name, centre, radius=2.0, period=6.0, tilt=0.0):
    return S.comp("TestGround.Orbit", "orbit/" + name, Centre=S.ref_go(centre), Radius=radius, Period=period, Tilt=tilt)

def row(tag, items, make, spacing, z):
    n = len(items)
    out = []
    for i, item in enumerate(items):
        x = (i - (n - 1) / 2) * spacing
        out.append(make((f"{tag} {item[0]}", *item[1:]), (x, 0, z)))
    return out, n * spacing + 8

ROW_DEPTH = 20
areas = []
z = -8

# -- the field: posts every six metres out to the horizon ----------------------
# A pale floor so the shadows read, posts and beams going away for the
# cascades to hand over on, a tall gate at the far end. The keys change the
# sun over all of it.
kids = [S.block("Field floor", (0, -0.15, -60), (60, 0.3, 140), FLOOR)]
for i in range(20):
    zz = -6 - i * 6
    kids.append(cube(f"Post {i}", (-6, 1.5, zz), (0.4, 3.0, 0.4)))
    kids.append(cube(f"Post R {i}", (6, 1.5, zz), (0.4, 3.0, 0.4)))
    if i % 4 == 0:
        kids.append(cube(f"Beam {i}", (0, 3.2, zz), (12.4, 0.4, 0.4)))
        kids.append(S.label(f"Distance {i}", (0, 4.2, zz), f"{-zz} m", scale=0.6, size=44))
kids.append(cube("Gate L", (-12, 6, -126), (1, 12, 1)))
kids.append(cube("Gate R", (12, 6, -126), (1, 12, 1)))
kids.append(cube("Gate top", (0, 12.5, -126), (25, 1, 1)))
kids.append(sign("Field", "the field\nposts every 6 m, beams every 24 m, a gate at 120 m\nkeys 1-5 change the sun", (0, 5.6, -6), scale=0.6))
field = S.go("Field", (0, 0, 0), children=kids)

# -- casters ---------------------------------------------------------------------
CUT_LEAF = "materials/gallery/blend_leaf.mat"
CUT_RING = "materials/gallery/blend_cut_05.mat"
TRANS = "materials/gallery/blend_trans_05.mat"
GLASS = "materials/glass.mat"
ONE_SIDED = "materials/gallery/sides_one.mat"
TWO_SIDED = "materials/gallery/sides_two.mat"
UPRIGHT = "0.7071068,0,0,0.7071068"

CASTERS = [
    ("Cube", "RenderType On\nthe plain case", [cube("Caster cube", (0, 1.0, 0))]),
    ("Shadows only", "RenderType ShadowsOnly\na shadow with nothing over it", [cube("Caster shadows only", (0, 1.0, 0), render="ShadowsOnly")]),
    ("No shadow", "RenderType Off\na cube that casts nothing", [cube("Caster off", (0, 1.0, 0), render="Off")]),
    ("Sphere", "self-shadowing\nthe terminator", [cube("Caster sphere", (0, 1.0, 0), (1.0, 1.0, 1.0), model="models/dev/sphere.mdl")]),
    ("Leaf cutout", "a masked leaf slab\nthe shadow should be leaf-shaped", [cube("Caster leaf", (0, 1.2, 0), (1.4, 1.4, 0.02), material=CUT_LEAF)]),
    ("Ring cutout", "a masked ring, cutoff 0.5", [cube("Caster ring", (0, 1.2, 0), (1.4, 1.4, 0.02), material=CUT_RING)]),
    ("Translucent", "Translucent at alpha 0.5\ndoes it cast, and how dark", [cube("Caster trans", (0, 1.2, 0), (1.4, 1.4, 0.02), material=TRANS)]),
    ("Glass", "the project's glass", [cube("Caster glass", (0, 1.2, 0), (1.4, 1.4, 0.02), material=GLASS)]),
    ("One-sided away", "a plane facing away from the sun\ndoes its back cast", [cube("Caster plane away", (0, 1.2, 0), (1.4, 1.4, 1.0), rot=UPRIGHT, material=ONE_SIDED, model="models/dev/plane.mdl")]),
    ("Two-sided", "the same plane, two-sided", [cube("Caster plane two", (0, 1.2, 0), (1.4, 1.4, 1.0), rot=UPRIGHT, material=TWO_SIDED, model="models/dev/plane.mdl")]),
    ("Grazing", "a slab tilted 80 degrees to the sun\nacne or peter-panning shows here", [cube("Caster grazing", (0, 0.5, 0), (1.6, 0.05, 1.6), rot=pitch_yaw(-20, 0))]),
    ("Contact", "a small cube on a big one\nthe join should be dark", [cube("Caster big", (0, 0.6, 0), (1.2, 0.8, 1.2)), cube("Caster small", (0, 1.15, 0), (0.3, 0.3, 0.3))]),
    ("High", "a cube 6 m up\nits shadow is far from it", [cube("Caster high", (0, 6.0, 0), (0.8, 0.8, 0.8))]),
    ("Thin", "a 2 cm rod\nit should keep a shadow at distance", [cube("Caster rod", (0, 1.5, 0), (0.02, 3.0, 0.02))]),
    ("Sprite", "a sprite with Shadows on", [S.go("Caster sprite", (0, 1.3, 0), components=[S.comp("Rinten.SpriteRenderer", "sprite/caster", __version=2,
        Additive=False, AlphaCutoff=0.5, Billboard="Always", Color="1,1,1,1", DepthFeather=0, FlipHorizontal=False, FlipVertical=False, FogStrength=1,
        IsSorted=False, Lighting=False, OnAnimationEnd=None, OnAnimationStart=None, OnBroadcastMessage=None, Opaque=False, OverlayColor="1,1,1,0",
        PlaybackSpeed=1, RenderOptions=RENDER, Shadows=True, Size="1.4,1.4", Sprite="sprites/ring.sprite", StartingAnimationName="Default", TextureFilter="Bilinear")])]),
    ("Line", "a LineRenderer with CastShadows", [S.go("Caster line", components=[S.comp("Rinten.LineRenderer", "line/caster",
        Additive=False, AutoCalculateNormals=True, CastShadows=True, Color={"blend": "Linear", "color": [{"t": 0.5, "c": "1,1,1,1"}], "alpha": []},
        CylinderSegments=12, DepthFeather=0, EndCap="None", Face="Camera", FogStrength=1, Lighting=True, Opaque=True, Points=None, RenderOptions=RENDER,
        SplineBias=0, SplineContinuity=0, SplineInterpolation=0, SplineTension=0, StartCap="None",
        Texturing={"Texture": None, "Material": None, "WorldSpace": True, "UnitsPerTexture": 1, "Scale": 1, "Offset": 0, "Scroll": 0, "FilterMode": "Anisotropic", "TextureAddressMode": "Wrap", "Clamp": False},
        UseVectorPoints=True, VectorPoints=None, Width=[{"x": 0.5, "y": 0.25, "in": 0, "out": 0, "mode": "Mirrored"}], Wireframe=False)])]),
    ("Model", "the urn, a real model", [cube("Caster urn", (0, 0.2, 0), (0.5, 0.5, 0.5), model="models/urn_broken.mdl")]),
]

def caster_station(item, pos):
    name, text, kids = item
    for k in kids:
        for c in k["Components"]:
            if c["__type"] == "Rinten.LineRenderer":
                c["VectorPoints"] = [v(pos[0] - 0.8, 1.6, pos[2]), v(pos[0] + 0.8, 1.6, pos[2])]
    return station(name, text, kids, pos)

kids, width = row("Caster", CASTERS, caster_station, 3.4, z - 130)
S.stagger_signs(kids)
areas.append(S.area("Casters", "every kind of thing that can cast a shadow, and two that should not", z - 130, width, slab_material=None, children=kids))
z -= 130 + ROW_DEPTH

# -- source radius: coloured point lights with their own penumbrae --------------
RADII = [("0", 0.0, "1,0.9,0.8,1"), ("0.05", 0.05, "1,0.9,0.8,1"), ("0.3", 0.3, "1,0.9,0.8,1"), ("1", 1.0, "1,0.9,0.8,1"), ("3", 3.0, "1,0.9,0.8,1")]
def radius_station(item, pos):
    name, r, color = item
    kids = [cube(f"{name} pillar", (0, 1.2, 0), (0.3, 2.4, 0.3)), cube(f"{name} backdrop", (0, 1.5, -2.4), (5, 3, 0.2), tint="0.6,0.6,0.6,1"),
            point_light(name, (0, 2.5, 2.5), color=color, brightness=8, radius=9, source=r)]
    return station(name, f"point light, SourceRadius {r}\nthe edge of the shadow on the backdrop", kids, pos, sign_y=3.8)
DARK = "0.12,0.12,0.14,1"

def roof(name, z, width):
    """A slab over a row, so the sun stays out and the row's own lights are what shows; the row's own slab is dark."""
    return S.block(f"Roof: {name}", (0, 7.0, z), (width, 0.3, 16), "0.25,0.26,0.3,1")

kids, width = row("Radius", RADII, radius_station, 6.0, z)
kids.append(roof("radius", z, width))
S.stagger_signs(kids)
areas.append(S.area("Source Radius", "five point lights under a roof, the same but for the size of the source: the penumbra widens", z, width, wall=False, slab_material=None, slab_tint=DARK, children=kids))
z -= ROW_DEPTH

# -- point and spot lights -----------------------------------------------------------
def cage(name):
    kids = []
    for i in range(8):
        a = i / 8 * math.tau
        kids.append(cube(f"{name} bar {i}", (math.cos(a) * 1.6, 1.2, math.sin(a) * 1.6), (0.15, 2.4, 0.15)))
    return kids

LIGHTS = [
    ("Point in a cage", "a point light in eight bars\nshadows every way", cage("Cage") + [point_light("Cage", (0, 1.2, 0), brightness=6, radius=7)]),
    ("Point no shadow", "the same, Shadows off", cage("Cage off") + [point_light("Cage off", (0, 1.2, 0), brightness=6, radius=7, shadows=False)]),
    ("Point radius 2", "Radius 2, cut off short", cage("Cage short") + [point_light("Cage short", (0, 1.2, 0), brightness=8, radius=2)]),
    ("Four colours", "red, green, blue, yellow round one pillar\nfour coloured shadows", [cube("Four pillar", (0, 1.2, 0), (0.3, 2.4, 0.3)),
        point_light("Four R", (2, 1.5, 0), "1,0.2,0.2,1", 6, 7), point_light("Four G", (-2, 1.5, 0), "0.2,1,0.2,1", 6, 7),
        point_light("Four B", (0, 1.5, 2), "0.3,0.4,1,1", 6, 7), point_light("Four Y", (0, 1.5, -2), "1,0.9,0.2,1", 6, 7)]),
    ("Spot down", "a spot straight down, 35 degrees", [cube("Spot pillar", (0, 0.8, 0), (0.4, 1.6, 0.4)), spot_light("Spot down", (0, 4.5, 0), pitch_yaw(-90, 0), brightness=12)]),
    ("Spot narrow", "ConeOuter 12, ConeInner 4", [cube("Spot narrow pillar", (0, 0.8, 0), (0.4, 1.6, 0.4)), spot_light("Spot narrow", (0, 4.5, 0), pitch_yaw(-90, 0), brightness=12, outer=12, inner=4)]),
    ("Spot wide", "ConeOuter 70, ConeInner 60", [cube("Spot wide pillar", (0, 0.8, 0), (0.4, 1.6, 0.4)), spot_light("Spot wide", (0, 4.5, 0), pitch_yaw(-90, 0), brightness=12, outer=70, inner=60)]),
    ("Spot cookie", "a ring cookie on the spot", [cube("Spot cookie pillar", (0, 0.8, 0), (0.4, 1.6, 0.4)), spot_light("Spot cookie", (0, 4.5, 0), pitch_yaw(-90, 0), brightness=12, cookie="textures/fx/ring.png")]),
    ("Spot sideways", "a spot along the floor onto a wall", [cube("Spot wall", (0, 1.5, -2.5), (4, 3, 0.2), tint="0.6,0.6,0.6,1"), cube("Spot side pillar", (0, 0.8, -0.5), (0.3, 1.6, 0.3)),
        spot_light("Spot side", (0, 1.2, 2.5), "0,0,0,1", brightness=12, outer=40, inner=30)]),
    ("Spot no shadow", "the same, Shadows off", [cube("Spot off wall", (0, 1.5, -2.5), (4, 3, 0.2), tint="0.6,0.6,0.6,1"), cube("Spot off pillar", (0, 0.8, -0.5), (0.3, 1.6, 0.3)),
        spot_light("Spot off", (0, 1.2, 2.5), "0,0,0,1", brightness=12, outer=40, inner=30, shadows=False)]),
]
kids, width = row("Light", LIGHTS, lambda it, p: station(it[0], it[1], it[2], p, sign_y=3.8), 6.0, z)
kids.append(roof("lights", z, width))
S.stagger_signs(kids)
areas.append(S.area("Point and Spot", "lights with their own shadow maps: cages, colours, cones, a cookie, and the same without shadows", z, width, wall=False, slab_material=None, slab_tint=DARK, children=kids))
z -= ROW_DEPTH

# -- moving --------------------------------------------------------------------------
MOVING = [
    ("Propeller", "a cross on a Spinner\nthe shadow turns with it", [S.go("Propeller", (0, 1.8, 0), components=[spinner("propeller", (0, 0, 1), 60)], children=[
        cube("Blade A", (0, 0, 0), (2.4, 0.2, 0.1)), cube("Blade B", (0, 0, 0), (0.2, 2.4, 0.1))])]),
    ("Bobbing", "a cube on an Oscillator\nup and down 1.5 m", [cube("Bob", (0, 1.5, 0), extra=[oscillator("bob", (0, 1, 0), 1.5, 0.4)])]),
    ("Sliding", "a cube sliding sideways", [cube("Slide", (0, 0.6, 0), extra=[oscillator("slide", (1, 0, 0), 1.5, 0.3)])]),
    ("Turning spot", "a spot light on a Spinner", [cube("Turn pillar A", (1.5, 0.8, 0), (0.3, 1.6, 0.3)), cube("Turn pillar B", (-1.5, 0.8, 0), (0.3, 1.6, 0.3)),
        cube("Turn pillar C", (0, 0.8, 1.5), (0.3, 1.6, 0.3)), cube("Turn pillar D", (0, 0.8, -1.5), (0.3, 1.6, 0.3)),
        S.go("Spot turner", (0, 3.0, 0), components=[spinner("spot turner", (0, 1, 0), 30)], children=[spot_light("Turning", (0, 0, 0), pitch_yaw(-45, 0), brightness=12, outer=30, inner=20)])]),
    ("Orbiting point", "a point light on an Orbit round a pillar", [cube("Orbit pillar", (0, 1.2, 0), (0.3, 2.4, 0.3)),
        S.go("Orbit centre", (0, 1.5, 0)), point_light("Orbiting", (2, 1.5, 0), "1,0.8,0.5,1", 6, 7, extra=[orbit("orbiting light", "Orbit centre", 2.0, 5.0)])]),
    ("Walking caster", "a cube orbiting in a point light", [point_light("Walk light", (0, 3.0, 0), "1,1,1,1", 6, 8),
        S.go("Walk centre", (0, 0.6, 0)), cube("Walker", (2, 0.6, 0), (0.6, 0.6, 0.6), extra=[orbit("walker", "Walk centre", 2.0, 6.0)])]),
]
kids, width = row("Moving", MOVING, lambda it, p: station(it[0], it[1], it[2], p, sign_y=3.8), 6.0, z)
kids.append(roof("moving", z, width))
S.stagger_signs(kids)
areas.append(S.area("Moving", "casters that turn, bob and slide; a spot that turns; a point that orbits; a caster that orbits a light", z, width, wall=False, slab_material=None, slab_tint=DARK, children=kids))
z -= ROW_DEPTH

# -- receivers -----------------------------------------------------------------------
RECEIVERS = [
    ("Rough", "the shadow on a rough pale slab", "materials/gallery/grid_r4_m0.mat"),
    ("Chrome", "on chrome\na shadow on a mirror", "materials/gallery/chrome.mat"),
    ("Metal", "on brushed metal", "materials/gallery/brushed.mat"),
    ("Normal map", "on the bumps normal map", "materials/gallery/map_normal.mat"),
    ("Emissive", "on an emissive slab\nemission should not darken", "materials/gallery/emission_2.mat"),
    ("Translucent", "on a translucent slab", "materials/gallery/blend_trans_05.mat"),
    ("Unlit", "on an unlit slab\nno shadow can land", "materials/gallery/shader_unlit.mat"),
    ("Dark", "on a nearly black slab", "materials/gallery/tint_dark.mat"),
]
def receiver_station(item, pos):
    name, text, m = item
    kids = [cube(f"{name} slab", (0, 0.25, 0), (2.4, 0.1, 2.4), material=m, tint="1,1,1,1"), cube(f"{name} caster", (0, 1.3, 0), (0.6, 0.6, 0.6))]
    return station(name, text, kids, pos, pedestal=False)
kids, width = row("Receiver", RECEIVERS, receiver_station, 4.0, z)
S.stagger_signs(kids)
areas.append(S.area("Receivers", "the same cube's shadow on eight surfaces", z, width, wall=False, children=kids))
z -= ROW_DEPTH

# -- a room with a window ---------------------------------------------------------------
room = []
room.append(cube("Room floor", (0, 0.1, 0), (8, 0.2, 8), tint=FLOOR))
room.append(cube("Room roof", (0, 3.9, 0), (8, 0.2, 8)))
room.append(cube("Room back", (0, 2, -4), (8, 4, 0.2)))
room.append(cube("Room right", (4, 2, 0), (0.2, 4, 8)))
# the left wall faces the sun and has a lattice window: a frame of bars with gaps
room.append(cube("Room left low", (-4, 0.6, 0), (0.2, 1.2, 8)))
room.append(cube("Room left high", (-4, 3.5, 0), (0.2, 1.0, 8)))
for i in range(5):
    room.append(cube(f"Room bar {i}", (-4, 2.0, -3.2 + i * 1.6), (0.2, 1.8, 0.3)))
room.append(cube("Room sill", (-4, 2.0, 0), (0.2, 0.15, 8)))
room.append(cube("Room table", (0, 0.6, 0), (1.5, 0.1, 1.0)))
room.append(cube("Room vase", (0, 1.0, 0), (0.3, 0.3, 0.3), model="models/urn_broken.mdl"))
room.append(sign("Room", "a room open on the front\nthe sun comes through the lattice on the left\ninside is what the ambient light gives", (0, 5.2, 0), scale=0.5))
areas.append(S.go("Room", (0, 0, z), children=room))

# ---------------------------------------------------------------- the scene

S.objects = [
    # A sun from behind the spawn, high enough that shadows land on the slabs in front of the walls.
    S.environment(sun_brightness=1.6, sun_rot=pitch_yaw(-40, 210), ambient="0.12,0.13,0.17,1", shadow_detail=64, source_radius=0.05),
    S.block("Ground", (0, -0.7, -110), (240, 0.5, 320), FLOOR),
    field,
    S.go("Areas", children=areas),
    S.player((0, 2.6, 6)),
    S.hud("The sun's field first; walk past the gate to the casters, radii, lights, movers, receivers and the room. Keys 1-5 change the sun. Q returns.",
          extra=[S.comp("TestGround.ShadowRack", "hud/rack", Sun=None, DaySpeed=6.0)]),
]

def check_unique(objects):
    seen = {}
    def walk(o):
        for key, what in ((o["__guid"], o["Name"]), *((c["__guid"], c["__type"]) for c in o["Components"])):
            if key in seen: raise SystemExit(f"guid clash: {what} and {seen[key]}")
            seen[key] = what
        for c in o["Children"]: walk(c)
    for o in objects: walk(o)
check_unique(S.objects)

S.write("Shadows.scene")
register_in_menu("shadows.scene", "Shadows", "Rendering",
                 "The sun over a long field, every kind of caster, source radii, point and spot shadows, moving lights, receivers and a room; keys change the sun")
