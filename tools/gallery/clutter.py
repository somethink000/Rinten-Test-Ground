#!/usr/bin/env python3
"""Writes the clutter gallery: the .clutter definitions under clutter/ and
scenes/rendering/clutter.scene - a volume a station, each with a ClutterProbe that fills
it and says what it got."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from common import Scene, ROOT, RENDER, v, yaw, pitch_yaw, register_in_menu

S = Scene("clutter", "Clutter",
          "Clutter volumes: density, scale, weights, ground placement, height offset, slope alignment, seeds, shadows, physics, tile sizes, churn, a big one, and the infinite mode.")

DEF_DIR = os.path.join(ROOT, "clutter")
os.makedirs(DEF_DIR, exist_ok=True)

# ---------------------------------------------------------------- definitions

def entry(model=None, prefab=None, weight=1.0, scale=1.0, shadows=True, physics=True):
    return {"Prefab": prefab, "Model": model, "Weight": weight, "LocalScale": scale, "CastShadows": shadows, "EnablePhysics": physics}

def definition(name, entries, density=1.0, scale=(0.8, 1.2), ground=True, offset=0.0, align=False, tile="Size512", radius=4):
    d = {"Entries": entries, "IsEmpty": len(entries) == 0, "TileSizeEnum": tile, "TileRadius": radius,
         "Scatterer": {"Type": "SimpleScatterer", "Scale": f"{scale[0]} {scale[1]}", "Density": density,
                       "PlaceOnGround": ground, "HeightOffset": offset, "AlignToNormal": align},
         "__references": [], "__version": 0}
    with open(os.path.join(DEF_DIR, name + ".clutter"), "w") as f:
        json.dump(d, f, indent=2)
        f.write("\n")
    return f"clutter/{name}.clutter"

BOX = "models/dev/box.mdl"
SPHERE = "models/dev/sphere.mdl"
URN = "models/props/urn_broken.mdl"

DEFS = {
    "cubes": definition("cubes", [entry(BOX, scale=0.4)], density=1.5),
    "spheres": definition("spheres", [entry(SPHERE, scale=0.4)], density=1.5),
    "mixed": definition("mixed", [entry(BOX, weight=1.0, scale=0.4), entry(SPHERE, weight=0.3, scale=0.4), entry(URN, weight=0.1, scale=0.25)], density=2.0),
    "sparse": definition("sparse", [entry(BOX, scale=0.4)], density=0.2),
    "dense": definition("dense", [entry(BOX, scale=0.25)], density=2.0),
    "tiny": definition("tiny", [entry(BOX, scale=0.4)], density=1.5, scale=(0.2, 0.3)),
    "huge": definition("huge", [entry(BOX, scale=0.4)], density=1.0, scale=(2.0, 3.0)),
    "spread": definition("spread", [entry(BOX, scale=0.4)], density=1.5, scale=(0.2, 2.5)),
    "floating": definition("floating", [entry(SPHERE, scale=0.4)], density=1.5, ground=False),
    "offset": definition("offset", [entry(SPHERE, scale=0.4)], density=1.5, offset=1.0),
    "aligned": definition("aligned", [entry(BOX, scale=0.4)], density=1.5, align=True),
    "unaligned": definition("unaligned", [entry(BOX, scale=0.4)], density=1.5, align=False),
    "noshadow": definition("noshadow", [entry(BOX, scale=0.4, shadows=False)], density=1.5),
    "nophysics": definition("nophysics", [entry(BOX, scale=0.5, physics=False)], density=1.5),
    "physics": definition("physics", [entry(BOX, scale=0.5, physics=True)], density=1.5),
    "tile256": definition("tile256", [entry(BOX, scale=0.4)], density=1.5, tile="Size256"),
    "tile4096": definition("tile4096", [entry(BOX, scale=0.4)], density=1.5, tile="Size4096"),
    "prefab": definition("prefab", [entry(prefab="prefabs/cube.prefab")], density=1.5),
    "empty": definition("empty", [], density=1.5),
    "missing": definition("missing", [entry("models/does_not_exist.mdl", scale=0.4)], density=1.5),
    "infinite": definition("infinite", [entry(SPHERE, scale=0.15)], density=0.02, tile="Size256", radius=2),
}
print("wrote", len(DEFS), "definitions")

# ---------------------------------------------------------------- stations

PEDESTAL = "0.2,0.22,0.26,1"
FLOOR = "0.3,0.32,0.36,1"

def volume(name, definition, size=(10, 4, 10), seed=1, churn=0.0, note="", mode="Volume"):
    hx, hy, hz = size[0] / 2, size[1] / 2, size[2] / 2
    return S.go(f"Volume: {name}", (0, hy, 0), components=[
        S.comp("Rinten.ClutterComponent", "clutter/" + name, Clutter=definition, Seed=seed, Mode=mode,
               Bounds={"Mins": v(-hx, -hy, -hz), "Maxs": v(hx, hy, hz)}),
        S.comp("TestGround.ClutterProbe", "probe/" + name, Churn=churn, Note=note)])

def station(name, note, definition, pos, size=(10, 4, 10), seed=1, churn=0.0, floor=True, extra=(), mode="Volume"):
    kids = []
    if floor: kids.append(S.block(f"Floor: {name}", (0, 0.05, 0), (size[0], 0.1, size[2]), FLOOR))
    kids.append(volume(name, definition, size, seed, churn, note, mode))
    kids.extend(extra)
    return S.go(f"Station: {name}", pos, children=kids)

def slope(name, pitch=25.0):
    return S.block(f"Slope: {name}", (0, 1.0, 0), (9, 0.3, 9), FLOOR, rot=pitch_yaw(pitch, 0))

def row(items, spacing, z):
    n = len(items)
    out = []
    for i, (name, note, d, kw) in enumerate(items):
        x = (i - (n - 1) / 2) * spacing
        out.append(station(name, note, d, (x, 0, z), **kw))
    return out, n * spacing + 8

ROW_DEPTH = 22
areas = []
z = -12

# what and how many
ROW1 = [
    ("Cubes", "cubes, density 1.5\n10 x 10 m", DEFS["cubes"], {}),
    ("Spheres", "spheres, density 1.5", DEFS["spheres"], {}),
    ("Mixed", "box 1.0, sphere 0.3, urn 0.1 by weight\ndensity 2", DEFS["mixed"], {}),
    ("Sparse", "density 0.2\ntwo or so", DEFS["sparse"], {}),
    ("Dense", "density 2, the most it allows", DEFS["dense"], {}),
    ("Seed 1", "the cubes with Seed 1", DEFS["cubes"], dict(seed=1)),
    ("Seed 2", "the same with Seed 2\nshould differ from Seed 1", DEFS["cubes"], dict(seed=2)),
    ("Seed 1 again", "Seed 1 again\nshould match the first", DEFS["cubes"], dict(seed=1)),
]
kids, width = row(ROW1, 13.0, z)
areas.append(S.area("What and How Many", "models, weights, density and seeds", z, width, depth=16, wall=False, slab_material=None, children=kids))
z -= ROW_DEPTH

# scale and placement
ROW2 = [
    ("Tiny", "Scale 0.2 .. 0.3", DEFS["tiny"], {}),
    ("Huge", "Scale 2 .. 3", DEFS["huge"], {}),
    ("Spread", "Scale 0.2 .. 2.5", DEFS["spread"], {}),
    ("Floating", "PlaceOnGround off\nspread through the volume's height", DEFS["floating"], {}),
    ("Offset", "HeightOffset 1\na metre above the floor", DEFS["offset"], {}),
    ("Aligned", "AlignToNormal on a 25 degree slope\ncubes should lean with it", DEFS["aligned"], dict(floor=False, extra=[slope("Aligned")])),
    ("Unaligned", "the slope again, AlignToNormal off\ncubes should stand upright", DEFS["unaligned"], dict(floor=False, extra=[slope("Unaligned")])),
    ("Steps", "a floor at two heights\nboth should be found", DEFS["cubes"], dict(floor=False, extra=[
        S.block("Steps low", (-2.5, 0.05, 0), (5, 0.1, 10), FLOOR), S.block("Steps high", (2.5, 1.0, 0), (5, 2.0, 10), FLOOR)])),
]
kids, width = row(ROW2, 13.0, z)
areas.append(S.area("Scale and Placement", "scale ranges, floating, height offset, slopes, steps", z, width, depth=16, wall=False, slab_material=None, children=kids))
z -= ROW_DEPTH

# shadows, physics, tiles, edges
ROW3 = [
    ("Shadows", "CastShadows on", DEFS["cubes"], {}),
    ("No shadows", "CastShadows off\nthe cubes, no shadows under them", DEFS["noshadow"], {}),
    ("Physics", "EnablePhysics on\nwalk into it", DEFS["physics"], {}),
    ("No physics", "EnablePhysics off\nwalk through it", DEFS["nophysics"], {}),
    ("Tile 256", "TileSize 256 - one tile", DEFS["tile256"], {}),
    ("Tile 4096", "TileSize 4096", DEFS["tile4096"], {}),
    ("Prefab", "a prefab entry, not a model\nvolumes store models only", DEFS["prefab"], {}),
    ("Empty", "a definition with no entries", DEFS["empty"], {}),
    ("Missing model", "a model that does not exist", DEFS["missing"], {}),
]
kids, width = row(ROW3, 13.0, z)
areas.append(S.area("Shadows, Physics, Tiles, Edges", "what an entry can turn off, tile sizes, and definitions with nothing to place", z, width, depth=16, wall=False, slab_material=None, children=kids))
z -= ROW_DEPTH

# churn and a big one
ROW4 = [
    ("Churn", "regenerated every 2 s with a new seed\nnothing should be left behind", DEFS["cubes"], dict(churn=2.0)),
    ("Fast churn", "every 0.3 s", DEFS["mixed"], dict(churn=0.3)),
    ("Tall", "a 10 x 20 x 10 volume\nground is still the floor", DEFS["cubes"], dict(size=(10, 20, 10))),
    ("Flat", "a 10 x 0.5 x 10 volume\nthe floor is inside it", DEFS["cubes"], dict(size=(10, 0.5, 10))),
    ("Across tiles", "a 24 m volume on 256 m tiles\nplaced across a tile edge if it lands on one", DEFS["tile256"], dict(size=(24, 4, 24))),
    ("Big", "40 x 40 m, density 2\nsome hundreds", DEFS["dense"], dict(size=(40, 4, 40))),
]

def sized_row(items, gap, z):
    """Stations laid by their own widths with a gap between, centred on x."""
    widths = [kw.get("size", (10, 4, 10))[0] for _, _, _, kw in items]
    total = sum(widths) + gap * (len(items) - 1)
    out, x = [], -total / 2
    for (name, note, d, kw), w in zip(items, widths):
        out.append(station(name, note, d, (x + w / 2, 0, z), **kw))
        x += w + gap
    return out, total + 8

kids, width = sized_row(ROW4, 4.0, z - 12)
areas.append(S.area("Churn and Size", "volumes made again and again, and big ones", z - 12, width, depth=48, wall=False, slab_material=None, children=kids))
z -= ROW_DEPTH + 48

# infinite: streams round the camera, everywhere
infinite = S.go("Infinite", (0, 2, 0), components=[
    S.comp("Rinten.ClutterComponent", "clutter/infinite", Clutter=DEFS["infinite"], Seed=7, Mode="Infinite",
           Bounds={"Mins": "-512,-512,-512", "Maxs": "512,512,512"})])
infinite_sign = S.label("Infinite", (0, 4.0, -4), "Infinite mode: small spheres streamed round the camera, everywhere, on 256 m tiles two deep\nwalk and they should keep coming; look back and the old ones should have gone", scale=0.5, size=44)

# ---------------------------------------------------------------- the scene

S.objects = [
    S.environment(sun_brightness=1.4),
    S.block("Ground", (0, -0.7, -70), (240, 0.5, 220), "0.2,0.21,0.24,1"),
    S.go("Areas", children=areas),
    infinite, infinite_sign,
    S.player((0, 3.0, 8)),
    S.hud("Four rows of clutter volumes, a probe over each saying what was asked and what was placed; small spheres everywhere are the infinite mode. Q returns."),
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

S.write("rendering/clutter.scene")
register_in_menu("rendering/clutter.scene", "Clutter", "Rendering",
                 "Clutter volumes: density, scale, weights, placement, slopes, seeds, shadows, physics, tiles, churn, a big one, and the infinite mode")
