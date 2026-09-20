#!/usr/bin/env python3
"""Writes scenes/rendering/renderers.scene: one row of stations per renderer component -
lines, trails, sprites, text, the model renderer's options, reflection probes
and meshes built by hand - each station one setting, labelled."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import Scene, RENDER, v, yaw, pitch_yaw, register_in_menu

S = Scene("renderers", "Renderers",
          "Line and trail renderers, sprites, text, the model renderer's options, reflection probes and hand-built meshes - one station a setting.")

PEDESTAL = "0.2,0.22,0.26,1"
OVERLAY = {"GameLayer": True, "OverlayLayer": True, "BloomLayer": False, "AfterUILayer": False}
BLOOM_ONLY = {"GameLayer": False, "OverlayLayer": False, "BloomLayer": True, "AfterUILayer": False}
AFTER_UI = {"GameLayer": True, "OverlayLayer": False, "BloomLayer": False, "AfterUILayer": True}

def pedestal(name, size=1.2):
    return S.block(f"Pedestal: {name}", (0, 0.1, 0), (size, 0.2, size), PEDESTAL)

def sign(name, text, y=3.0, scale=0.38):
    return S.label(name, (0, y, 0), text, scale=scale, size=44)

def station(name, text, children, pos, sign_y=3.4):
    return S.go(f"Station: {name}", pos, children=[pedestal(name), sign(name, text, sign_y), *children])

def gradient(*stops, alpha=()):
    return {"blend": "Linear", "color": [{"t": t, "c": c} for t, c in stops], "alpha": [{"t": t, "a": a} for t, a in alpha]}

def curve(*frames):
    return [{"x": x, "y": y, "in": 0, "out": 0, "mode": "Mirrored"} for x, y in frames]

TEXTURING = {"Texture": None, "Material": None, "WorldSpace": True, "UnitsPerTexture": 1, "Scale": 1, "Offset": 0, "Scroll": 0,
             "FilterMode": "Anisotropic", "TextureAddressMode": "Wrap", "Clamp": False}

# ---------------------------------------------------------------- lines

def line(name, color=None, width=None, points=None, vector_points=None, **more):
    props = dict(Additive=False, AutoCalculateNormals=True, CastShadows=False, Color=color or gradient((0.5, "1,1,1,1")),
                 CylinderSegments=12, DepthFeather=0, EndCap="None", Face="Camera", FogStrength=1, Lighting=False, Opaque=True,
                 Points=points, RenderOptions=RENDER, SplineBias=0, SplineContinuity=0, SplineInterpolation=0, SplineTension=0,
                 StartCap="None", Texturing=dict(TEXTURING), UseVectorPoints=vector_points is not None,
                 VectorPoints=[v(*p) for p in vector_points] if vector_points else None,
                 Width=width or curve((0.5, 0.06)), Wireframe=False)
    props.update(more)
    return S.comp("Rinten.LineRenderer", "line/" + name, **props)

def point_objects(name, positions):
    return [S.go(f"{name} P{i}", p, scale=(0.08, 0.08, 0.08), components=[S.model(f"{name} P{i}", "1,0.5,0.2,1", model="models/dev/sphere.mdl")])
            for i, p in enumerate(positions)]

ZIG = [(-1.2, 0.4, 0), (-0.4, 2.2, 0), (0.4, 0.6, 0), (1.2, 2.4, 0)]
HELIX = [(1.0 * __import__("math").cos(i * 0.9), 0.4 + i * 0.18, 1.0 * __import__("math").sin(i * 0.9)) for i in range(14)]

def offset(points, pos):
    """Vector points are in the world, not the object - so a station's are
    written where the station stands."""
    return [(x + pos[0], y + pos[1], z + pos[2]) for x, y, z in points]

def line_station(name, text, pos, **kw):
    kids = []
    comps = []
    if "points" in kw:
        pts = kw.pop("points")
        kids += point_objects(name, pts)
        comps.append(line(name, points=[S.ref_go(f"{name} P{i}") for i in range(len(pts))], **kw))
    else:
        kw["vector_points"] = offset(kw["vector_points"], pos)
        comps.append(line(name, **kw))
    kids.append(S.go(f"Line: {name}", components=comps))
    return station(name, text, kids, pos)

LINES = [
    ("Points", "four objects as points\nwidth 0.06", dict(points=ZIG)),
    ("Spline", "vector points, interpolation 8\ntension 0", dict(vector_points=ZIG, SplineInterpolation=8)),
    ("Spline tight", "the same, tension -0.8\ncontinuity 0.5", dict(vector_points=ZIG, SplineInterpolation=8, SplineTension=-0.8, SplineContinuity=0.5)),
    ("Width curve", "0 -> 0.3 -> 0 along the line", dict(vector_points=ZIG, SplineInterpolation=8, Width=curve((0, 0.0), (0.5, 0.3), (1, 0.0)))),
    ("Gradient", "red -> green -> blue\nalpha 1 -> 0", dict(vector_points=ZIG, SplineInterpolation=8, Width=curve((0.5, 0.12)),
        Color=gradient((0, "1,0.2,0.2,1"), (0.5, "0.2,1,0.2,1"), (1, "0.3,0.4,1,1"), alpha=((0, 1), (1, 0))), Opaque=False)),
    ("Face Normal", "a helix facing its normals\nnot the camera", dict(vector_points=HELIX, SplineInterpolation=4, Face="Normal", Width=curve((0.5, 0.1)))),
    ("Cylinder", "Face: Cylinder, 12 segments\nLighting on", dict(vector_points=HELIX, SplineInterpolation=4, Face="Cylinder", CylinderSegments=12, Lighting=True, Width=curve((0.5, 0.08)))),
    ("Cylinder 3", "Face: Cylinder, 3 segments", dict(vector_points=HELIX, SplineInterpolation=4, Face="Cylinder", CylinderSegments=3, Lighting=True, Width=curve((0.5, 0.08)))),
    ("Caps", "start Arrow, end Rounded\nwidth 0.25", dict(vector_points=[(-1.2, 1.2, 0), (1.2, 1.4, 0)], StartCap="Arrow", EndCap="Rounded", Width=curve((0.5, 0.25)))),
    ("Caps Triangle", "both Triangle", dict(vector_points=[(-1.2, 1.2, 0), (1.2, 1.4, 0)], StartCap="Triangle", EndCap="Triangle", Width=curve((0.5, 0.25)))),
    ("Additive", "Additive, not opaque\ncyan at 0.6", dict(vector_points=ZIG, SplineInterpolation=8, Additive=True, Opaque=False, Width=curve((0.5, 0.3)), Color=gradient((0.5, "0.2,0.9,1,0.6")))),
    ("Translucent", "Opaque off, white at 0.3", dict(vector_points=ZIG, SplineInterpolation=8, Opaque=False, Width=curve((0.5, 0.3)), Color=gradient((0.5, "1,1,1,0.3")))),
    ("Wireframe", "Wireframe on", dict(vector_points=ZIG, SplineInterpolation=8, Wireframe=True, Width=curve((0.5, 0.3)))),
    ("Textured", "ring.png every 0.5 m\nscrolling", dict(vector_points=ZIG, SplineInterpolation=8, Width=curve((0.5, 0.3)),
        Texturing={**TEXTURING, "Texture": "textures/fx/ring.png", "UnitsPerTexture": 0.5, "Scroll": 0.5})),
    ("Depth feather", "DepthFeather 0.5\nthrough the pedestal", dict(vector_points=[(-1, -0.3, 0), (1, 0.8, 0)], DepthFeather=0.5, Opaque=False, Width=curve((0.5, 0.35)), Color=gradient((0.5, "1,0.8,0.2,0.8")))),
    ("Fog off", "FogStrength 0", dict(vector_points=ZIG, SplineInterpolation=8, FogStrength=0, Width=curve((0.5, 0.12)))),
    ("Shadow", "CastShadows on\nlook under it", dict(vector_points=[(-1.2, 1.5, 0), (1.2, 1.5, 0)], CastShadows=True, Width=curve((0.5, 0.3)), Lighting=True)),
]

def moving_line_station(pos):
    name = "Moving point"
    pts = ZIG
    kids = point_objects(name, pts)
    kids[2]["Components"].append(S.comp("TestGround.Oscillator", "osc/" + name, Axis="0,1,0", Amplitude=0.8, Speed=0.5, Phase=0))
    kids.append(S.go(f"Line: {name}", components=[line(name, points=[S.ref_go(f"{name} P{i}") for i in range(len(pts))],
        SplineInterpolation=8, Width=curve((0.5, 0.08)))]))
    return station(name, "the third point oscillates\nthe line follows", kids, pos)

def overlay_line_station(pos):
    name = "Overlay layer"
    kids = [S.block(f"Wall: {name}", (0, 1.2, 0.6), (2.6, 2.2, 0.2), "0.5,0.2,0.2,1"),
            S.go(f"Line: {name}", components=[line(name, vector_points=offset(ZIG, pos), SplineInterpolation=8, Width=curve((0.5, 0.12)),
                RenderOptions=OVERLAY, Color=gradient((0.5, "0.2,1,0.4,1")))])]
    return station(name, "RenderOptions.OverlayLayer\nseen through the wall", kids, pos)

# ---------------------------------------------------------------- trails

def trail(name, **more):
    props = dict(BlendMode="Normal", CastShadows=False, Color=gradient((0.5, "0.3,0.9,1,1")), Emitting=True, Face="Camera", LifeTime=2,
                 MaxPoints=64, Opaque=True, PointDistance=0.1, RenderOptions=RENDER, Texturing=dict(TEXTURING),
                 Width=curve((0.5, 0.08)), Wireframe=False)
    props.update(more)
    return S.comp("Rinten.TrailRenderer", "trail/" + name, **props)

def orbit(name, radius=1.1, period=3.0, tilt=35.0, phase=0.0):
    return S.comp("TestGround.Orbit", "orbit/" + name, Centre=S.ref_go(f"Centre: {name}"), Radius=radius, Period=period, Tilt=tilt, Phase=phase)

def trail_station(name, text, pos, extra=(), orbit_kw=None, **kw):
    centre = S.go(f"Centre: {name}", (0, 1.5, 0))
    mover = S.go(f"Mover: {name}", (1.1, 1.5, 0), scale=(0.15, 0.15, 0.15), components=[
        S.model(f"Mover: {name}", "1,0.6,0.2,1", model="models/dev/sphere.mdl"), orbit(name, **(orbit_kw or {})), trail(name, **kw), *extra])
    return station(name, text, [centre, mover], pos)

TRAILS = [
    ("Trail", "LifeTime 2, PointDistance 0.1\n64 points", {}),
    ("Long", "LifeTime 8, 256 points\nthe whole orbit and more", dict(LifeTime=8, MaxPoints=256)),
    ("Few points", "PointDistance 0.6\na polygon of an orbit", dict(PointDistance=0.6)),
    ("Taper", "width 0.2 -> 0\ngradient to transparent", dict(Width=curve((0, 0.2), (1, 0.0)), Opaque=False,
        Color=gradient((0, "1,0.9,0.3,1"), (1, "1,0.3,0.1,1"), alpha=((0, 1), (1, 0))))),
    ("Lighten", "BlendMode Lighten, not opaque", dict(BlendMode="Lighten", Opaque=False, Width=curve((0.5, 0.25)), Color=gradient((0.5, "0.3,0.6,1,0.7")))),
    ("Multiply", "BlendMode Multiply", dict(BlendMode="Multiply", Opaque=False, Width=curve((0.5, 0.25)), Color=gradient((0.5, "0.6,0.2,0.2,1")))),
    ("Premultiplied", "BlendMode PremultipliedAlpha", dict(BlendMode="PremultipliedAlpha", Opaque=False, Width=curve((0.5, 0.25)), Color=gradient((0.5, "0.9,0.9,0.3,0.5")))),
    ("Face Normal", "Face: Normal", dict(Face="Normal", Width=curve((0.5, 0.15)))),
    ("Wireframe", "Wireframe on", dict(Wireframe=True, Width=curve((0.5, 0.2)))),
    ("Textured", "ring.png, scrolling", dict(Width=curve((0.5, 0.25)), Texturing={**TEXTURING, "Texture": "textures/fx/ring.png", "UnitsPerTexture": 0.4, "Scroll": 1})),
    ("Shadow", "CastShadows on", dict(CastShadows=True, Width=curve((0.5, 0.2)))),
]

# ---------------------------------------------------------------- sprites

def sprite(name, sprite="sprites/glow.sprite", size=0.6, **more):
    props = dict(__version=2, Additive=False, AlphaCutoff=0.5, Billboard="Always", Color="1,1,1,1", DepthFeather=0, FlipHorizontal=False,
                 FlipVertical=False, FogStrength=1, IsSorted=False, Lighting=False, OnAnimationEnd=None, OnAnimationStart=None,
                 OnBroadcastMessage=None, Opaque=False, OverlayColor="1,1,1,0", PlaybackSpeed=1, RenderOptions=RENDER, Shadows=False,
                 Size=v(size, size), Sprite=sprite, StartingAnimationName="Default", TextureFilter="Bilinear")
    props.update(more)
    return S.comp("Rinten.SpriteRenderer", "sprite/" + name, **props)

def sprite_station(name, text, pos, y=1.5, rot="0,0,0,1", **kw):
    return station(name, text, [S.go(f"Sprite: {name}", (0, y, 0), rot=rot, components=[sprite(name, **kw)])], pos)

SPRITES = [
    ("Glow", "glow.sprite, 0.6 m\nBillboard Always", dict()),
    ("Ring", "ring.sprite, 1.2 m", dict(sprite="sprites/ring.sprite", size=1.2)),
    ("Flame", "flame.sprite, 12 fps\nanimated", dict(sprite="sprites/flame.sprite", size=1.0)),
    ("Flame x3", "PlaybackSpeed 3", dict(sprite="sprites/flame.sprite", size=1.0, PlaybackSpeed=3)),
    ("Y only", "Billboard YOnly\nwalk around it", dict(sprite="sprites/ring.sprite", size=1.0, Billboard="YOnly")),
    ("Fixed", "Billboard None\nfacing +Z", dict(sprite="sprites/ring.sprite", size=1.0, Billboard="None")),
    ("Particle", "Billboard Particle", dict(sprite="sprites/ring.sprite", size=1.0, Billboard="Particle")),
    ("Additive", "Additive on", dict(size=1.2, Additive=True)),
    ("Cutout", "Opaque, AlphaCutoff 0.5", dict(sprite="sprites/ring.sprite", size=1.0, Opaque=True, AlphaCutoff=0.5)),
    ("Cutout 0.9", "Opaque, AlphaCutoff 0.9", dict(sprite="sprites/ring.sprite", size=1.0, Opaque=True, AlphaCutoff=0.9)),
    ("Lit", "Lighting on", dict(sprite="sprites/paper.sprite", size=1.0, Lighting=True)),
    ("Flipped", "FlipHorizontal + FlipVertical", dict(sprite="sprites/flame.sprite", size=1.0, FlipHorizontal=True, FlipVertical=True)),
    ("Tint", "Color orange at 0.5", dict(size=1.2, Color="1,0.5,0.1,0.5")),
    ("Overlay colour", "OverlayColor red 0.7", dict(sprite="sprites/ring.sprite", size=1.0, OverlayColor="1,0,0,0.7")),
    ("Shadow", "Shadows on\nlook under it", dict(sprite="sprites/ring.sprite", size=1.4, Shadows=True)),
    ("Point filter", "TextureFilter Point\ndot.sprite at 1.4 m", dict(sprite="sprites/dot.sprite", size=1.4, TextureFilter="Point")),
    ("Feather", "DepthFeather 0.5\nhalf in the pedestal", dict(size=1.4, DepthFeather=0.5, y=0.2)),
    ("No fog", "FogStrength 0", dict(size=1.0, FogStrength=0)),
]

def sorted_station(pos):
    name = "Sorted"
    kids = []
    for i, (c, z) in enumerate([("1,0.2,0.2,0.8", 0.3), ("0.2,1,0.2,0.8", 0.0), ("0.2,0.4,1,0.8", -0.3)]):
        kids.append(S.go(f"Sprite: {name} {i}", (i * 0.25 - 0.25, 1.5, z), components=[sprite(f"{name} {i}", size=1.0, Color=c, IsSorted=True)]))
    return station(name, "three overlapping, IsSorted\nback to front", kids, pos)

# ---------------------------------------------------------------- text

def text_go(name, text, pos=(0, 1.6, 0), rot="0,0,0,1", scale=0.4, color="0.95,0.95,1,1", font="Poppins", size=48, weight=600, italic=False,
            billboard="YOnly", blend="Normal", fog=1, halign="Center", valign="Center", options=None, line_height=1.1, letter_spacing=0,
            outline=None, shadow=True, extra=()):
    scope = S.text_scope(text, color=color, font=font, size=size, weight=weight, italic=italic, line_height=line_height,
                         letter_spacing=letter_spacing, outline=outline, shadow=shadow)
    return S.go(f"Text: {name}", pos, rot=rot, components=[S.text(name, scope, scale=scale, billboard=billboard, blend=blend, fog=fog,
                                                                    halign=halign, valign=valign, options=options), *extra])

def text_station(name, text, pos, texts):
    return station(name, text, texts, pos)

TEXTS = [
    ("Fonts", "Poppins, Roboto, Roboto Mono", [
        text_go("Fonts A", "Poppins", (0, 2.2, 0), font="Poppins"),
        text_go("Fonts B", "Roboto", (0, 1.6, 0), font="Roboto"),
        text_go("Fonts C", "Roboto Mono", (0, 1.0, 0), font="Roboto Mono")]),
    ("Weights", "300, 500, 800, italic", [
        text_go("Weights A", "light 300", (0, 2.4, 0), weight=300),
        text_go("Weights B", "medium 500", (0, 1.8, 0), weight=500),
        text_go("Weights C", "bold 800", (0, 1.2, 0), weight=800),
        text_go("Weights D", "italic", (0, 0.6, 0), weight=500, italic=True)]),
    ("Sizes", "FontSize 16 and 96 at one scale\nScale 0.15 and 0.8 at one size", [
        text_go("Sizes A", "16px", (-0.8, 2.2, 0), size=16),
        text_go("Sizes B", "96px", (0.8, 2.2, 0), size=96),
        text_go("Sizes C", "0.15", (-0.8, 1.0, 0), scale=0.15),
        text_go("Sizes D", "0.8", (0.8, 1.0, 0), scale=0.8)]),
    ("Colours", "colour, outline, shadow off", [
        text_go("Colours A", "orange", (0, 2.3, 0), color="1,0.6,0.1,1"),
        text_go("Colours B", "outline", (0, 1.7, 0), outline={"Enabled": True, "Size": 4, "Color": "0,0,0,1"}, color="1,1,0.3,1"),
        text_go("Colours C", "no shadow", (0, 1.1, 0), shadow=False),
        text_go("Colours D", "alpha 0.4", (0, 0.5, 0), color="1,1,1,0.4")]),
    ("Billboard", "None, YOnly, Always\nfrom the side they differ", [
        text_go("Billboard A", "None", (0, 2.3, 0), billboard="None"),
        text_go("Billboard B", "YOnly", (0, 1.7, 0), billboard="YOnly"),
        text_go("Billboard C", "Always", (0, 1.1, 0), billboard="Always")]),
    ("Alignment", "hung off the red pin\nleft / right, top / bottom", [
        S.go("Pin: Alignment", (0, 1.6, 0), scale=(0.06, 0.06, 0.06), components=[S.model("Pin: Alignment", "1,0.2,0.2,1", model="models/dev/sphere.mdl")]),
        text_go("Alignment A", "Left", (0, 1.6, 0), halign="Left", billboard="None", scale=0.25),
        text_go("Alignment B", "Right", (0, 1.6, 0), halign="Right", billboard="None", scale=0.25),
        text_go("Alignment C", "Top", (0, 1.6, 0), valign="Top", billboard="None", scale=0.25),
        text_go("Alignment D", "Bottom", (0, 1.6, 0), valign="Bottom", billboard="None", scale=0.25)]),
    ("Layout", "LineHeight 0.8 and 1.6\nLetterSpacing 6", [
        text_go("Layout A", "tight\nlines", (-0.9, 1.8, 0), line_height=0.8),
        text_go("Layout B", "loose\nlines", (0.9, 1.8, 0), line_height=1.6),
        text_go("Layout C", "s p a c e d", (0, 0.7, 0), letter_spacing=6)]),
    ("Blend", "BlendMode Lighten and Multiply\nFogStrength 0", [
        text_go("Blend A", "Lighten", (0, 2.3, 0), blend="Lighten", color="0.3,0.8,1,1"),
        text_go("Blend B", "Multiply", (0, 1.7, 0), blend="Multiply", color="0.5,0.2,0.2,1"),
        text_go("Blend C", "no fog", (0, 1.1, 0), fog=0)]),
    ("Overlay", "RenderOptions.OverlayLayer\nseen through the wall", [
        S.block("Wall: Text Overlay", (0, 1.2, 0.6), (2.6, 2.2, 0.2), "0.5,0.2,0.2,1"),
        text_go("Overlay A", "through", (0, 1.6, 0), options=OVERLAY, color="0.3,1,0.5,1")]),
    ("Spinning", "Billboard None on a Spinner", [
        text_go("Spinning A", "spin", (0, 1.6, 0), billboard="None", scale=0.6,
                extra=[S.comp("TestGround.Spinner", "spin/text", Axis="0,1,0", Speed=45, Local=True)])]),
    ("Unicode", "Cyrillic, symbols, emoji", [
        text_go("Unicode A", "Привет мир", (0, 2.2, 0)),
        text_go("Unicode B", "✓ ★ ∞ → €", (0, 1.6, 0)),
        text_go("Unicode C", "❤ 🔥 🎮", (0, 1.0, 0))]),
    ("Long", "a long single line\nand a paragraph", [
        text_go("Long A", "the quick brown fox jumps over the lazy dog and keeps going", (0, 2.2, 0), scale=0.2),
        text_go("Long B", "one\ntwo\nthree\nfour\nfive\nsix", (0, 1.1, 0), scale=0.25)]),
]

# ---------------------------------------------------------------- model renderer

def cube(name, pos, tint="1,1,1,1", material=None, model="models/dev/box.mdl", scale=(0.6, 0.6, 0.6), render="On", options=None, rot="0,0,0,1", collide=False):
    return S.block(name, pos, scale, tint, material, model, render=render, collide=collide, rot=rot) if collide else \
        S.go(name, pos, rot=rot, scale=scale, components=[S.model(name, tint, material, model, render, options)])

def model_station(name, text, pos, kids):
    return station(name, text, kids, pos)

PROJECT_MODELS = ["models/props/urn_broken.mdl", "models/fx/shield.mdl", "models/fx/flame.mdl", "models/space/rover.mdl", "models/space/iss.mdl",
                  "models/space/satellite.mdl", "models/space/voyager.mdl", "models/space/hubble.mdl"]

def instancing_station(pos):
    name = "Instancing"
    kids = []
    for i in range(10):
        for j in range(10):
            kids.append(cube(f"{name} {i}-{j}", (i * 0.3 - 1.35, 0.35 + j * 0.3, 0), tint=f"{0.3 + i * 0.07:.2f},{0.3 + j * 0.07:.2f},0.8,1", scale=(0.2, 0.2, 0.2)))
    return station(name, "100 renderers, one model", kids, pos)

MODELS = [
    ("Tint", "Tint red, green, blue, half alpha", [
        cube("Tint R", (-0.9, 0.5, 0), "1,0.2,0.2,1"), cube("Tint G", (0, 0.5, 0), "0.2,1,0.2,1"), cube("Tint B", (0.9, 0.5, 0), "0.3,0.4,1,1"),
        cube("Tint A", (0, 1.3, 0), "1,1,1,0.5")]),
    ("Render type", "On, Off, ShadowsOnly\nthe shadow of a cube that is not there", [
        cube("Render On", (-0.9, 0.9, 0), render="On"), cube("Render Off", (0, 0.9, 0), render="Off"), cube("Render Shadows", (0.9, 0.9, 0), render="ShadowsOnly")]),
    ("Material override", "grid, metal, glass on a sphere", [
        cube("Override grid", (-0.9, 0.7, 0), material="materials/dev/grid.mat", model="models/dev/sphere.mdl"),
        cube("Override metal", (0, 0.7, 0), material="materials/dev/metal.mat", model="models/dev/sphere.mdl"),
        cube("Override glass", (0.9, 0.7, 0), material="materials/common/glass.mat", model="models/dev/sphere.mdl")]),
    ("Overlay layer", "OverlayLayer behind a wall", [
        S.block("Wall: Model Overlay", (0, 1.2, 0.6), (2.6, 2.2, 0.2), "0.5,0.2,0.2,1"),
        cube("Overlay cube", (0, 0.8, -0.3), "0.3,1,0.5,1", options=OVERLAY)]),
    ("Bloom layer", "BloomLayer only", [cube("Bloom cube", (0, 0.8, 0), "1,0.9,0.3,1", options=BLOOM_ONLY)]),
    ("After UI", "AfterUILayer\ndraws over the HUD?", [cube("After UI cube", (0, 0.8, 0), "0.9,0.3,1,1", options=AFTER_UI)]),
    ("Disabled", "object disabled, component disabled\nneither should show", [
        S.go("Disabled object", (-0.6, 0.8, 0), scale=(0.6, 0.6, 0.6), enabled=False, components=[S.model("Disabled object", "1,0,0,1")]),
        S.go("Disabled component", (0.6, 0.8, 0), scale=(0.6, 0.6, 0.6), components=[{**S.model("Disabled component", "1,0,0,1"), "__enabled": False}])]),
    ("Mirrored", "scale -1 on X, then Y\nthe grid should read backwards", [
        cube("Mirror X", (-0.9, 0.7, 0), material="materials/dev/grid.mat", scale=(-0.6, 0.6, 0.6)),
        cube("Mirror Y", (0, 0.7, 0), material="materials/dev/grid.mat", scale=(0.6, -0.6, 0.6)),
        cube("Mirror none", (0.9, 0.7, 0), material="materials/dev/grid.mat")]),
    ("Nested", "parent turned 45, child offset\nand scaled", [
        S.go("Nested parent", (0, 0.8, 0), rot=yaw(45), scale=(0.6, 0.6, 0.6), components=[S.model("Nested parent", "0.9,0.9,0.9,1")],
             children=[S.go("Nested child", (1.0, 0.5, 0), scale=(0.5, 0.5, 0.5), components=[S.model("Nested child", "1,0.6,0.2,1")])])]),
    ("Spinning", "a Spinner on the object", [cube("Spin cube", (0, 0.8, 0), "0.6,0.8,1,1"),]),
]

def project_models_station(pos):
    kids = []
    n = len(PROJECT_MODELS)
    for i, m in enumerate(PROJECT_MODELS):
        x = (i - (n - 1) / 2) * 1.1
        kids.append(S.go(f"Model: {os.path.basename(m)}", (x, 0.2, 0), scale=(0.35, 0.35, 0.35), components=[S.model(f"project/{m}", "1,1,1,1", model=m)]))
    return station("Project models", "the project's own models\nurn, shield, flame, five spacecraft", kids, pos)

# ---------------------------------------------------------------- reflections

CHROME = "materials/gallery/surface/chrome.mat"
BRUSHED = "materials/gallery/surface/brushed.mat"

def probe(name, mode="Baked", projection="Sphere", bounds=(6, 6, 6), tint="1,1,1,1", feather=0.2, priority=0, update="OnEnabled", interval=5, max_distance=6):
    hx, hy, hz = bounds[0] / 2, bounds[1] / 2, bounds[2] / 2
    return S.comp("Rinten.EnvmapProbe", "probe/" + name, __version=1, BakedTexture=None, Bounds={"Mins": v(-hx, -hy, -hz), "Maxs": v(hx, hy, hz)},
                  DelayBetweenUpdates=0.1, Feathering=feather, FrameInterval=interval, MaxDistance=max_distance, Mode=mode, MultiBounce=False,
                  Priority=priority, Projection=projection, RenderExcludeTags="", Resolution="Small", Texture=None, TintColor=tint,
                  UpdateStrategy=update, ZFar=104, ZNear=0.4)

def chrome_ball(name, pos=(0, 1.1, 0), material=CHROME, r=0.9):
    return S.go(f"Ball: {name}", pos, scale=(r, r, r), components=[S.model(f"ball/{name}", "1,1,1,1", material, "models/dev/sphere.mdl")])

def coloured_room(name, size=4.0, h=3.0):
    """Four coloured walls round a station, so a reflection has something to show."""
    s = size / 2
    return [S.block(f"Room {name} N", (0, h / 2, -s), (size, h, 0.1), "0.9,0.2,0.2,1"),
            S.block(f"Room {name} W", (-s, h / 2, 0), (0.1, h, size), "0.2,0.9,0.2,1"),
            S.block(f"Room {name} E", (s, h / 2, 0), (0.1, h, size), "0.2,0.3,1,1")]

def probe_station(name, text, pos, room=True, ball=CHROME, probe_here=True, **kw):
    kids = []
    if room: kids += coloured_room(name)
    kids.append(chrome_ball(name, material=ball))
    if probe_here:
        kids.append(S.go(f"Probe: {name}", (0, 1.5, 0), components=[probe(name, **kw)]))
    return station(name, text, kids, pos, sign_y=3.8)

REFLECTIONS = [
    ("No probe", "chrome with no probe\nsky only", dict(probe_here=False)),
    ("Sphere probe", "Baked, Sphere projection\nthe room in the ball", dict(projection="Sphere")),
    ("Box probe", "Baked, Box projection\nbounds 4 x 3 x 4", dict(projection="Box", bounds=(4, 3, 4))),
    ("Tinted", "TintColor orange", dict(tint="1,0.6,0.2,1")),
    ("Realtime", "Realtime, every frame\nthe spinner should move in it", dict(mode="Realtime", update="EveryFrame")),
    ("Interval", "Realtime, every 30 frames", dict(mode="Realtime", update="FrameInterval", interval=30)),
    ("Feathered", "Feathering 1.0, MaxDistance 3", dict(feather=1.0, max_distance=3)),
    ("Brushed", "roughness 0.4 metal under a probe", dict(ball=BRUSHED)),
]

def priority_station(pos):
    name = "Priority"
    kids = coloured_room(name) + [chrome_ball(name),
        S.go(f"Probe: {name} low", (0, 1.5, 0), components=[probe(name + " low", tint="1,0.2,0.2,1", priority=0, bounds=(8, 8, 8))]),
        S.go(f"Probe: {name} high", (0, 1.5, 0), components=[probe(name + " high", tint="0.2,0.4,1,1", priority=10, bounds=(3, 3, 3))])]
    return station(name, "two probes, red 0 and blue 10\nblue should win", kids, pos, sign_y=3.8)

def mirror_station(pos):
    name = "Mirror"
    kids = coloured_room(name) + [
        S.go("Mirror plane", (0, 1.2, 0.5), scale=(3, 2.2, 0.05), components=[S.model("mirror", "1,1,1,1", CHROME)]),
        S.go(f"Probe: {name}", (0, 1.5, 0), components=[probe(name, projection="Box", bounds=(4, 3, 4))])]
    return station(name, "a chrome slab under a box probe", kids, pos, sign_y=3.8)

# ---------------------------------------------------------------- procedural meshes

def procedural(name, text, pos, shape, size=(2.0, 1.0, 2.0), segments=6, material="materials/dev/grid.mat", smoothing=0.0):
    kids = [S.go(f"Mesh: {name}", (0, 0.2, 0), components=[
        S.comp("TestGround.ProceduralMesh", "proc/" + name, Shape=shape, Size=v(*size), Segments=segments, Material=material, SmoothingAngle=smoothing)])]
    return station(name, text, kids, pos)

PROCEDURAL = [
    ("Ramp", "a wedge, 2 x 1 x 2", dict(shape="Ramp")),
    ("Stairs", "8 steps", dict(shape="Stairs", segments=8)),
    ("Stairs 3", "3 steps, metal", dict(shape="Stairs", segments=3, material="materials/dev/metal.mat")),
    ("Prism", "6 sides, flat shaded", dict(shape="Prism", segments=6, size=(1.6, 1.4, 1.6))),
    ("Cylinder", "24 sides, SmoothingAngle 60", dict(shape="Prism", segments=24, size=(1.6, 1.4, 1.6), smoothing=60)),
    ("Ring", "12 sides, hollow", dict(shape="Ring", segments=12, size=(2.0, 0.5, 2.0))),
    ("Box", "a built box beside the model box", dict(shape="Box", size=(1.0, 1.0, 1.0))),
    ("Glass", "glass material, backfaces", dict(shape="Prism", segments=8, size=(1.4, 1.4, 1.4), material="materials/common/glass.mat", smoothing=60)),
]

# ---------------------------------------------------------------- areas

def row(tag, items, make, spacing, z):
    """Stations along x, each named under the row's tag so two rows may both
    have a 'Shadow' and keep their own ids."""
    n = len(items)
    out = []
    for i, item in enumerate(items):
        x = (i - (n - 1) / 2) * spacing
        out.append(make((f"{tag} {item[0]}", *item[1:]), (x, 0, z)))
    return out, n * spacing + 8

ROW_DEPTH = 18
areas = []
z = -8

# Lines
kids, width = row("Line",LINES, lambda it, p: line_station(it[0], it[1], p, **it[2]), 4.5, z)
extra_z = z
kids.append(moving_line_station((-(len(LINES) / 2) * 4.5 - 4.5, 0, z)))
kids.append(overlay_line_station(((len(LINES) / 2) * 4.5 + 4.5, 0, z)))
S.stagger_signs(kids)
areas.append(S.area("Line Renderer", "points, splines, widths, faces, caps, blending, texture", z, width + 9, children=kids))
z -= ROW_DEPTH

# Trails
kids, width = row("Trail",TRAILS, lambda it, p: trail_station(it[0], it[1], p, **it[2]), 5.0, z)
kids.append(trail_station("Pulse", "TrailPulse: 1 s on, 0.5 s off", ((len(TRAILS) / 2) * 5.0 + 5.0, 0, z), extra=[S.comp("TestGround.TrailPulse", "pulse/trail", On=1.0, Off=0.5)]))
kids.append(trail_station("Fast", "Period 0.7 s\nfew points a turn", (-(len(TRAILS) / 2) * 5.0 - 5.0, 0, z), orbit_kw=dict(period=0.7)))
S.stagger_signs(kids)
areas.append(S.area("Trail Renderer", "orbiting emitters: lifetime, spacing, width, blend, faces", z, width + 10, children=kids))
z -= ROW_DEPTH

# Sprites
kids, width = row("Sprite",SPRITES, lambda it, p: sprite_station(it[0], it[1], p, **it[2]), 4.0, z)
kids.append(sorted_station(((len(SPRITES) / 2) * 4.0 + 4.0, 0, z)))
S.stagger_signs(kids)
areas.append(S.area("Sprite Renderer", "sprites, animation, billboards, blending, cutout, lighting, sorting", z, width + 8, children=kids))
z -= ROW_DEPTH

# Text
kids, width = row("Text",TEXTS, lambda it, p: text_station(it[0], it[1], p, it[2]), 5.0, z)
S.stagger_signs(kids)
areas.append(S.area("Text Renderer", "fonts, weights, sizes, colours, billboards, alignment, layout, blending", z, width, children=kids))
z -= ROW_DEPTH

# Model renderer
kids, width = row("Model",MODELS, lambda it, p: model_station(it[0], it[1], p, it[2]), 5.0, z)
# the spinner on its cube
for k in kids:
    if k["Name"] == "Station: Model Spinning":
        for c in k["Children"]:
            if c["Name"] == "Spin cube":
                c["Components"].append(S.comp("TestGround.Spinner", "spin/cube", Axis="0,1,0", Speed=60, Local=True))
kids.append(instancing_station(((len(MODELS) / 2) * 5.0 + 5.0, 0, z)))
kids.append(project_models_station((-(len(MODELS) / 2) * 5.0 - 8.0, 0, z)))
S.stagger_signs(kids)
areas.append(S.area("Model Renderer", "tint, render type, overrides, layers, disabled, mirrored, nested, instancing, project models", z, width + 22, children=kids))
z -= ROW_DEPTH

# Reflections
kids, width = row("Probe",REFLECTIONS, lambda it, p: probe_station(it[0], it[1], p, **it[2]), 6.0, z)
# a spinner beside the realtime probe
for k in kids:
    if k["Name"] == "Station: Probe Realtime":
        k["Children"].append(S.go("Spinner: Realtime", (1.3, 1.2, 0.8), scale=(0.4, 0.4, 0.4), components=[
            S.model("spinner/realtime", "1,0.8,0.2,1"), S.comp("TestGround.Spinner", "spin/realtime", Axis="0,1,0", Speed=90, Local=True)]))
kids.append(priority_station(((len(REFLECTIONS) / 2) * 6.0 + 6.0, 0, z)))
kids.append(mirror_station((-(len(REFLECTIONS) / 2) * 6.0 - 6.0, 0, z)))
S.stagger_signs(kids)
areas.append(S.area("Reflection Probes", "chrome balls in coloured rooms: sphere and box projection, tint, realtime, priority", z, width + 12, children=kids))
z -= ROW_DEPTH

# Procedural
kids, width = row("Mesh",PROCEDURAL, lambda it, p: procedural(it[0], it[1], p, **it[2]), 5.0, z)
for k in kids:
    if k["Name"] == "Station: Mesh Box":
        k["Children"].append(S.go("Model box", (1.4, 0.7, 0), scale=(1, 1, 1), components=[S.model("model box", "1,1,1,1", "materials/dev/grid.mat")]))
S.stagger_signs(kids)
areas.append(S.area("Polygon Meshes", "geometry built in code: ramp, stairs, prisms, a ring, smoothing", z, width, children=kids))

# ---------------------------------------------------------------- the scene

S.objects = [
    S.environment(),
    S.block("Ground", (0, -0.7, -60), (200, 0.5, 180), "0.2,0.21,0.24,1"),
    S.go("Areas", children=areas),
    S.player((0, 2.6, 14)),
    S.hud("Seven rows, one renderer each. Every station is one setting; a missing thing is a broken path. Q returns."),
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

S.write("rendering/renderers.scene")
register_in_menu("rendering/renderers.scene", "Renderers", "Rendering",
                 "Lines, trails, sprites, text, model renderer options, reflection probes and hand-built meshes - a station a setting")
