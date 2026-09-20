#!/usr/bin/env python3
"""scenes/rendering/jungle.scene - the jungle, laid out on the ground that
grow.py cut: a stream down the middle, a path beside it, and everything from
the catalogue placed by hand where the references put it, with the
undergrowth and the litter scattered by clutter.

Positions here are in Blender's frame, the one grow.py thinks in (x, y along
the ground, z up), and turned into the engine's (x, up, -y) on the way out.
tools/jungle/ground.json is the ground's height grid and the lines of the
stream and the path, sampled from the same noise grow.py's ground uses.

    python3 tools/jungle/scene.py
"""
import json, math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery"))
from common import Scene, ROOT, v, yaw, pitch_yaw, register_in_menu

HERE = os.path.dirname(os.path.abspath(__file__))
GROUND = json.load(open(os.path.join(HERE, "ground.json")))
MODELS = os.path.join(ROOT, "models", "jungle")

S = Scene("jungle", "Jungle",
          "A rainforest: a stream, a path, giants with buttresses and roots, stranglers, banyans, palms, bamboo, "
          "ferns and litter everywhere, dead wood, moss, and the fog that hides the rest.")


# ---------------------------------------------------------------------------
# The ground: heights and the two lines through it
# ---------------------------------------------------------------------------

def height(x, y):
    """Bilinear height of the ground at Blender (x, y)."""
    n, step, size = GROUND["n"], GROUND["step"], GROUND["size"]
    fx = (x + size / 2) / step
    fy = (y + size / 2) / step
    ix = max(0, min(n - 2, int(math.floor(fx))))
    iy = max(0, min(n - 2, int(math.floor(fy))))
    tx, ty = max(0.0, min(1.0, fx - ix)), max(0.0, min(1.0, fy - iy))
    h = GROUND["heights"]
    a = h[iy][ix] * (1 - tx) + h[iy][ix + 1] * tx
    b = h[iy + 1][ix] * (1 - tx) + h[iy + 1][ix + 1] * tx
    return a * (1 - ty) + b * ty


def line_at(key, y):
    n, step, size = GROUND["n"], GROUND["step"], GROUND["size"]
    fy = (y + size / 2) / step
    iy = max(0, min(n - 2, int(math.floor(fy))))
    t = max(0.0, min(1.0, fy - iy))
    xs = GROUND[key]
    return xs[iy] * (1 - t) + xs[iy + 1] * t


def sx(y):
    return line_at("stream_x", y)


def px(y):
    return line_at("path_x", y)


# ---------------------------------------------------------------------------
# Placing a model
# ---------------------------------------------------------------------------

placed = []   # (x, y, radius) of everything big, so the scatter keeps clear
names = set()


def put(model, x, y, turn=0.0, scale=1.0, lift=0.0, on_ground=True, collide=False, clear=0.0, name=None):
    """A model at Blender (x, y), standing on the ground (or `lift` above it),
    turned `turn` degrees about up. `collide` adds a ModelCollider - the
    model's .mdl must carry a hull for that to do anything."""
    z = (height(x, y) if on_ground else 0.0) + lift
    name = name or f"{model} @ {x:.1f},{y:.1f}"
    while name in names:
        name += "'"
    names.add(name)
    path = f"models/jungle/{model}.mdl"
    comps = [S.model(name, model=path)]
    if collide:
        comps.append(S.comp("Rinten.ModelCollider", "collider/" + name, Model=path, Static=True, IsTrigger=False,
                            Friction=None, Elasticity=None, RollingResistance=None, Surface=None, SurfaceVelocity="0,0,0",
                            OnTriggerEnter=None, OnTriggerExit=None, OnObjectTriggerEnter=None, OnObjectTriggerExit=None))
    if clear:
        placed.append((x, y, clear))
    return S.go(name, (x, z, -y), rot=yaw(turn), scale=(scale, scale, scale), tags="world", components=comps)


def free(x, y, radius):
    """Whether a spot is clear of the stream, the path and what is placed."""
    if abs(x - px(y)) < 1.6 + radius * 0.35 or abs(x - sx(y)) < 1.8 + radius * 0.35:
        return False
    return all(math.hypot(x - qx, y - qy) > r + radius for qx, qy, r in placed)


def scatter(rng, models, count, radius, tries=400, scale=(0.85, 1.15), collide=False):
    out = []
    for _ in range(count):
        for _ in range(tries):
            x, y = rng.uniform(-29, 29), rng.uniform(-29, 29)
            if free(x, y, radius):
                out.append(put(rng.choice(models), x, y, rng.uniform(0, 360), rng.uniform(*scale), collide=collide, clear=radius))
                break
    return out


# ---------------------------------------------------------------------------
# Collision in the .mdl files: a triangle mesh for what is walked on, a
# capsule up the trunk of a tree
# ---------------------------------------------------------------------------

HULL = {"__type": "RenderMesh", "Name": "", "Enabled": True, "Bone": "", "Surface": "", "Tags": "", "Folder": ""}

MESH_COLLIDERS = ["ground", "log_a", "log_b", "logmossy_a", "logmossy_b", "logmossy_c", "uprooted_a", "uprooted_b",
                  "rootmat_a", "rootmat_b", "stump_a", "stump_b", "stump_c", "broken_a", "broken_b",
                  "rock_a", "rock_b", "rock_c", "rockflat_a", "rockflat_b", "rockflat_c", "rockflat_d", "rockslab_a",
                  "boulder_a", "boulder_b", "rockmid_a", "rockmid_b", "rockmid_c", "rockbig_a", "rockbig_b", "rockbig_c",
                  "cliff_a", "cliff_b", "streamstone_a", "streamstone_b", "streamstone_c", "rockstack_a", "rockstack_b"]

# (trunk radius at the base, how high the capsule goes), in metres, from the
# catalogue's numbers. The capsule stands straight up the model's Y, which is
# close enough for a leaning trunk to stop a player walking through its foot.
TRUNK_CAPSULES = {
    "tree_giant_a": (1.5, 10), "tree_giant_b": (1.8, 9), "tree_giant_c": (1.3, 9), "mossy_giant": (1.4, 9),
    "tree_winding_a": (0.8, 6), "tree_winding_b": (0.7, 5), "tree_winding_c": (0.9, 6),
    "tree_lean_a": (1.1, 3), "tree_lean_b": (0.9, 3), "tree_forked_a": (0.7, 3), "tree_forked_b": (0.8, 3),
    "tree_tall_a": (0.35, 12), "tree_tall_b": (0.3, 12), "tree_tall_c": (0.4, 10), "tree_tall_d": (0.32, 14),
    "strangler_a": (1.0, 12), "strangler_b": (0.9, 10), "banyan_a": (1.4, 8), "banyan_b": (1.1, 7),
    "climbed_a": (0.5, 9), "climbed_b": (0.7, 7), "palm_a": (0.2, 7), "palm_b": (0.18, 5), "palm_c": (0.22, 10),
    "palm_fan_a": (0.16, 4), "palm_fan_b": (0.14, 2.5), "snag_a": (0.5, 8), "snag_b": (0.7, 12), "snag_c": (0.4, 5),
    "treefern_a": (0.16, 2.3), "treefern_b": (0.16, 3.2), "cycad_a": (0.3, 0.8), "cycad_b": (0.3, 1.5),
}


def ensure_hulls():
    """Writes the collision each model wants into its .mdl, once."""
    changed = 0
    for name in MESH_COLLIDERS:
        changed += set_hulls(name, [dict(HULL)])
    for name, (r, h) in TRUNK_CAPSULES.items():
        changed += set_hulls(name, [dict(HULL, __type="CapsuleHull", PointA=v(0, 0, 0), PointB=v(0, h, 0), Radius=r)])
    print("hulls written into", changed, "models")


def set_hulls(name, hulls):
    path = os.path.join(MODELS, name + ".mdl")
    with open(path) as f:
        d = json.load(f)
    if d.get("Hulls") == hulls:
        return 0
    d["Hulls"] = hulls
    with open(path, "w") as f:
        json.dump(d, f, indent=2)
    return 1


# ---------------------------------------------------------------------------
# Clutter: the undergrowth, the litter, the saplings
# ---------------------------------------------------------------------------

DEF_DIR = os.path.join(ROOT, "clutter")


def entry(model, weight=1.0, scale=1.0, shadows=True):
    return {"Prefab": None, "Model": f"models/jungle/{model}.mdl", "Weight": weight, "LocalScale": scale, "CastShadows": shadows, "EnablePhysics": False}


def definition(name, entries, density, scale=(0.75, 1.3), align=False):
    d = {"Entries": entries, "IsEmpty": False, "TileSizeEnum": "Size256", "TileRadius": 4,
         "Scatterer": {"Type": "SimpleScatterer", "Scale": f"{scale[0]} {scale[1]}", "Density": density,
                       "PlaceOnGround": True, "HeightOffset": -0.02, "AlignToNormal": align},
         "__references": [], "__version": 0}
    with open(os.path.join(DEF_DIR, name + ".clutter"), "w") as f:
        json.dump(d, f, indent=2)
        f.write("\n")
    return f"clutter/{name}.clutter"


UNDERSTORY = [entry("fern_a", 3), entry("fern_b", 2), entry("fern_c", 2.5), entry("fern_d", 1), entry("broadleaf_a", 1),
              entry("broadleaf_b", 1.2), entry("elephant_a", 0.4), entry("elephant_b", 0.2), entry("lily_a", 1), entry("lily_b", 0.5),
              entry("fanplant_a", 0.7), entry("fanplant_b", 0.4), entry("sapling_a", 1), entry("sapling_b", 0.6), entry("bush_a", 0.8),
              entry("bush_b", 0.4), entry("grass_a", 2), entry("grass_b", 1.5), entry("cycad_a", 0.15), entry("banana_a", 0.1)]
FLOOR = [entry("litter_a", 2), entry("litter_b", 1), entry("pebbles_a", 0.6), entry("mosscushion_a", 1), entry("mosscushion_b", 0.5),
         entry("mosscushion_c", 0.5), entry("debris_a", 0.7), entry("debris_b", 0.3), entry("debris_c", 0.8), entry("fallenfrond_a", 0.4),
         entry("fallenfrond_b", 0.2), entry("rock_a", 0.5), entry("streamstone_a", 0.3), entry("vinetangle_a", 0.15), entry("mosscarpet_a", 0.3)]
SAPLINGS = [entry("tree_thin_a", 1), entry("tree_thin_b", 1), entry("tree_arch_a", 0.6), entry("tree_arch_b", 0.6), entry("treefern_a", 0.5),
            entry("bamboo_a", 0.5), entry("bamboo_b", 0.4), entry("bamboo_c", 0.6), entry("sapling_b", 0.8)]

# Density is points per m², then the scatterer divides by 10 - 0.5 is grass-dense
# in the clutter test scene, 6 is a fern thicket.
DEFS = {
    "understory": definition("jungle_understory", UNDERSTORY, density=6.0),
    "understory_thin": definition("jungle_understory_thin", UNDERSTORY, density=2.4),
    "floor": definition("jungle_floor", FLOOR, density=4.0, scale=(0.8, 1.2), align=True),
    "floor_thin": definition("jungle_floor_thin", FLOOR, density=1.8, scale=(0.8, 1.2), align=True),
    "saplings": definition("jungle_saplings", SAPLINGS, density=0.4, scale=(0.8, 1.2)),
}


def clutter_volume(name, definition, x0, x1, y0, y1, seed):
    """A clutter volume over a rectangle of ground (Blender x and y).

    ClutterProbe is what actually fills the volume - a ClutterComponent written
    into a scene file has empty Storage until Generate runs, and the probe does
    that on the first frames once the ground is in the physics world.
    """
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hx, hy = (x1 - x0) / 2, (y1 - y0) / 2
    return S.go(f"Clutter: {name}", (cx, 1.0, -cy), components=[
        S.comp("Rinten.ClutterComponent", "clutter/" + name, Clutter=definition, Seed=seed, Mode="Volume",
               Bounds={"Mins": v(-hx, -5, -hy), "Maxs": v(hx, 8, hy)}),
        S.comp("TestGround.ClutterProbe", "probe/" + name, Churn=0.0, Note=name, Overlay=False)])


def clutter_strips(name, definition, x0f, x1f, seed, step=10.0):
    """Clutter volumes that follow a meandering x-range along y, so the path
    and the stream stay clear while the forest comes up to their banks."""
    out, y, i = [], -30.0, 0
    while y < 30:
        y1 = min(y + step, 30.0)
        ym = (y + y1) / 2
        a, b = x0f(ym), x1f(ym)
        if b > a + 0.9:
            out.append(clutter_volume(f"{name} {i}", definition, a, b, y, y1, seed + i))
            i += 1
        y = y1
    return out


# ---------------------------------------------------------------------------
# The layout
# ---------------------------------------------------------------------------

rng = random.Random(7)
objects = [put("ground", 0, 0, on_ground=False, collide=True, name="Ground")]

# -- the big trees, by hand ------------------------------------------------
hero = [
    put("tree_lean_a", px(-15) - 3.2, -15, turn=15, collide=True, clear=2.5),
    put("tree_giant_b", px(-2) + 9, -2, turn=40, collide=True, clear=4),
    put("mossy_giant", px(8) - 12, 8, turn=200, collide=True, clear=4),
    put("tree_giant_a", sx(16) - 9, 16, turn=110, collide=True, clear=4),
    put("tree_giant_c", px(-27) + 9, -27, turn=300, collide=True, clear=3.5),
    put("banyan_a", px(20) + 13, 20, turn=70, collide=True, clear=6),
    put("banyan_b", px(-24) + 12, -24, turn=250, collide=True, clear=5),
    put("strangler_a", px(-16) - 8, -16, turn=0, collide=True, clear=2.5),
    put("strangler_b", sx(4) - 14, 4, turn=130, collide=True, clear=2.5),
    put("tree_winding_a", px(2) + 5, 2, turn=170, collide=True, clear=2.5),
    put("tree_winding_b", sx(-12) - 6, -12, turn=20, collide=True, clear=2.5),
    put("tree_winding_c", px(26) - 6, 26, turn=95, collide=True, clear=2.5),
    put("tree_lean_b", sx(24) - 5, 24, turn=60, collide=True, clear=2.5),
    put("tree_forked_a", px(14) + 6, 14, turn=210, collide=True, clear=2),
    put("tree_forked_b", sx(-22) - 9, -22, turn=340, collide=True, clear=2),
    put("climbed_a", px(-12) + 7, -12, turn=0, collide=True, clear=2),
    put("climbed_b", sx(12) - 4, 12, turn=45, collide=True, clear=2),
]
objects += hero
tree_pos = {}
for o in hero:
    x, hh, z = (float(c) for c in o["Position"].split(","))
    tree_pos[o["Name"].split(" @ ")[0]] = (x, -z)

# -- palms, tree ferns, bamboo, the odd ones -------------------------------
objects += [
    put("palm_a", px(-12) + 4, -12, turn=30, collide=True, clear=1.5),
    put("palm_c", sx(-5) - 5, -5, turn=200, collide=True, clear=1.5),
    put("palm_b", px(12) + 4, 12, turn=110, collide=True, clear=1.5),
    put("palm_fan_a", px(4) - 5, 4, turn=0, collide=True, clear=1.5),
    put("palm_fan_b", sx(-14) + 4, -14, turn=80, collide=True, clear=1.2),
    put("treefern_a", sx(-8) + 3.5, -8, turn=0, collide=True, clear=1.2),
    put("treefern_b", sx(6) + 3.5, 6, turn=140, collide=True, clear=1.2),
    put("bambooclump_a", px(-23) - 3.1, -22.2, turn=15, clear=1.5),
    put("bambooclump_b", px(-23) + 3.4, -21.5, turn=200, clear=1.8),
    put("bamboo_a", px(-23) - 2.2, -23.4, turn=8, clear=0.4),
    put("bamboo_c", px(-23) + 2.4, -22.6, turn=95, clear=0.4),
    put("bambooclump_a", px(-18) + 4, -18, turn=0, scale=0.9, clear=1.5),
    put("bambooclump_b", px(-26) - 4, -26, turn=60, clear=1.8),
    put("bambooclump_a", px(-20) - 4.5, -20, turn=200, scale=0.9, clear=1.5),
    put("bamboo_b", px(-15) - 3.5, -15, turn=0, clear=0.5),
    put("bamboo_c", px(-22) + 3.5, -22, turn=90, clear=0.5),
    put("fern_a", px(-23) - 1.5, -22.8),
    put("fern_c", px(-23) + 1.3, -22.4),
    put("fern_b", px(-23) - 1.1, -21.6),
    put("fern_d", px(-23) + 1.7, -23.2),
    put("broadleaf_a", px(-23) - 2.6, -21.0, turn=40),
    put("boulder_a", sx(-21) + 1.4, -21, turn=50, lift=-0.12, collide=True, clear=1.2),
    put("rockflat_c", sx(-23) - 0.3, -22.5, turn=20, lift=-0.18, collide=True),
    put("streamstone_b", sx(-22), -22, turn=80, lift=-0.1, collide=True),
    put("rockmid_a", sx(-20) - 2.4, -20.5, turn=110, lift=-0.15, collide=True, clear=1.2),
    put("stilt_a", sx(10) + 4, 10, turn=0, clear=1.5),
    put("stilt_b", sx(-20) - 4, -20, turn=120, clear=1.5),
    put("stilt_c", px(28) + 6, 28, turn=0, clear=1.5),
    put("cycad_a", px(0) - 4, 0, turn=40, clear=1),
    put("cycad_b", px(24) + 5, 24, turn=0, clear=1.2),
    put("banana_a", px(14) - 5, 14, turn=0, clear=1.5),
    put("banana_b", sx(22) + 5, 22, turn=180, clear=1.8),
    put("reeds_a", sx(-16) + 2.6, -16, clear=0.5),
    put("reeds_b", sx(2) - 2.6, 2, turn=50, clear=0.5),
    put("reeds_a", sx(20) + 2.6, 20, turn=120, clear=0.5),
]

# -- dead wood -------------------------------------------------------------
objects += [
    put("logmossy_a", px(6) + 2, 6, turn=70, collide=True, clear=1.5),
    put("logmossy_b", sx(-2) + 6, -2, turn=20, collide=True, clear=2),
    put("log_a", px(-28) + 6, -28, turn=150, collide=True, clear=1.5),
    put("log_b", sx(28) - 7, 28, turn=100, collide=True, clear=2),
    put("logmossy_c", px(18) - 4, 18, turn=10, collide=True, clear=1),
    put("uprooted_a", sx(28) - 4, 30, turn=30, collide=True, clear=3),
    put("uprooted_b", px(-30) + 10, -30, turn=200, collide=True, clear=2.5),
    put("snag_a", px(18) - 7, 18, turn=0, collide=True, clear=1.2),
    put("snag_b", sx(-10) - 8, -10, turn=90, collide=True, clear=1.5),
    put("snag_c", px(-4) + 7, -4, turn=200, collide=True, clear=1),
    put("stump_a", px(10) - 3.5, 10, turn=0, collide=True, clear=1),
    put("stump_b", sx(-24) + 5, -24, turn=90, collide=True, clear=1.2),
    put("stump_c", px(-8) + 4, -8, turn=180, collide=True, clear=0.8),
    put("broken_a", px(26) - 9, 26, turn=250, collide=True, clear=2),
    put("broken_b", sx(-28) - 6, -28, turn=30, collide=True, clear=2),
    put("rootmat_a", px(8) - 12, 8, turn=20, collide=True),
    put("rootmat_b", sx(16) - 9, 16, turn=70, collide=True),
    put("vinetangle_b", px(10) - 4.5, 10.8),
]

# -- the stream: stones in the bed, boulders on the banks ------------------
bed = ["streamstone_a", "streamstone_b", "streamstone_c", "rockflat_a", "rockflat_b", "rockflat_d", "rock_b", "streamstone_b"]
bank = ["boulder_a", "boulder_b", "rockbig_a", "rockmid_a", "rockmid_b", "rockmid_c", "rockstack_a", "rockflat_c", "rockslab_a"]
y = -29.0
i = 0
while y < 29:
    objects.append(put(bed[i % len(bed)], sx(y) + rng.uniform(-1.4, 1.4), y, turn=rng.uniform(0, 360), scale=rng.uniform(0.7, 1.2), lift=-0.15, collide=True))
    if i % 2 == 0:
        side = 1 if i % 4 == 0 else -1
        objects.append(put(bank[(i // 2) % len(bank)], sx(y) + side * rng.uniform(2.8, 4.2), y + rng.uniform(-1, 1),
                           turn=rng.uniform(0, 360), lift=-0.2, collide=True, clear=1.5))
    y += rng.uniform(2.0, 3.2)
    i += 1
objects += [
    put("cliff_a", -26, 10, turn=20, collide=True, clear=5),
    put("cliff_b", 27, -14, turn=110, collide=True, clear=6),
    put("rockbig_b", -22, -6, turn=60, collide=True, clear=3),
    put("rockbig_c", 24, 6, turn=300, collide=True, clear=3.5),
    put("rockstack_b", px(-6) + 10, -6, turn=0, collide=True, clear=1.5),
]

# -- the picket behind: tall trunks that go into the fog --------------------
objects += scatter(rng, ["tree_tall_a", "tree_tall_b", "tree_tall_c", "tree_tall_d"], 34, 2.2, collide=True)
objects += scatter(rng, ["tree_thin_a", "tree_thin_b", "tree_arch_a", "tree_arch_b"], 22, 1.0)
objects += scatter(rng, ["palm_a", "palm_b", "palm_fan_a", "treefern_b", "cycad_b", "banana_a"], 12, 1.5, collide=True)


# -- vines: hung from limbs, strung between trunks, coiled on the ground ---
def hang(model, tree, dx, dy, h, turn=0, scale=1.0):
    x, y = tree_pos[tree]
    return put(model, x + dx, y + dy, turn=turn, scale=scale, lift=h)


def strung(model, span, a, b, h):
    (ax, ay), (bx, by) = tree_pos[a], tree_pos[b]
    dist = math.hypot(bx - ax, by - ay)
    return put(model, ax, ay, turn=math.degrees(math.atan2(by - ay, bx - ax)), scale=dist / span, lift=h)


objects += [
    hang("vinehang_b", "tree_giant_b", 3.0, 0.5, 9.0),
    hang("vinehang_a", "mossy_giant", -3.0, 2.0, 8.0, turn=40),
    hang("vinehang_c", "tree_lean_a", 4.5, 1.2, 5.5),
    hang("vinehang_b", "banyan_a", -4.0, 3.0, 8.5, turn=90, scale=0.8),
    hang("vinerope_a", "banyan_a", 5.0, -2.0, 9.0),
    hang("vinerope_b", "tree_giant_a", 3.5, 3.0, 10.0),
    hang("mossdrape_b", "tree_giant_b", -3.5, 2.5, 8.0),
    hang("mossdrape_a", "tree_winding_c", 2.0, 1.0, 6.0),
    hang("mossdrape_b", "mossy_giant", 4.0, -2.5, 9.0, turn=30),
    hang("aerialroots_b", "strangler_a", 1.5, 0.0, 6.0),
    hang("aerialroots_a", "banyan_b", -3.0, 2.0, 5.5),
    strung("vinearch_a", 8, "tree_lean_a", "tree_giant_b", 7.0),
    strung("vinearch_b", 12, "mossy_giant", "strangler_b", 8.0),
    strung("vinearch_a", 8, "tree_winding_a", "tree_forked_a", 6.5),
    put("liana_a", px(-13) + 6, -13, turn=200),
    put("liana_b", sx(-6) - 7, -6, turn=30),
    put("liana_c", px(16) - 6, 16, turn=300),
    put("brackets_b", tree_pos["tree_giant_b"][0] - 1.7, tree_pos["tree_giant_b"][1], turn=180, lift=1.2),
    put("brackets_a", px(18) - 7 + 0.5, 18, turn=0, lift=1.6),
]

# -- the scatter: dense forest up to the banks, a narrow path, a stream bed --
# The path and stream meander, so these are short strips rather than one 20 m
# clearing down the middle - that left the first view looking like a field.
objects += clutter_strips("understory west", DEFS["understory"],
                          lambda y: -30.0, lambda y: sx(y) - 1.6, 110)
objects += clutter_strips("understory between", DEFS["understory"],
                          lambda y: sx(y) + 1.7, lambda y: px(y) - 1.5, 130)
objects += clutter_strips("understory east", DEFS["understory"],
                          lambda y: px(y) + 1.5, lambda y: 30.0, 150)
objects += clutter_strips("floor west", DEFS["floor"],
                          lambda y: -30.0, lambda y: sx(y) - 1.4, 210)
objects += clutter_strips("floor stream", DEFS["floor"],
                          lambda y: sx(y) - 1.4, lambda y: sx(y) + 1.7, 230)
objects += clutter_strips("floor between", DEFS["floor"],
                          lambda y: sx(y) + 1.7, lambda y: px(y) - 1.3, 250)
objects += clutter_strips("floor path", DEFS["floor_thin"],
                          lambda y: px(y) - 1.3, lambda y: px(y) + 1.3, 270)
objects += clutter_strips("floor east", DEFS["floor"],
                          lambda y: px(y) + 1.3, lambda y: 30.0, 290)
objects += [clutter_volume("saplings", DEFS["saplings"], -30, 30, -30, 30, 31)]

# -- light, fog, the player, the HUD ----------------------------------------
# The sun low, from behind and to the left of the walk, so trunks are lit on
# their edges and the fog glows between them.
objects += [
    S.environment(sun_brightness=1.0, sun_rot=pitch_yaw(-28, 155), sun_color="1,0.93,0.8,1", ambient="0.16,0.22,0.18,1",
                  sky_tint="0.6,0.7,0.68,1", shadow_detail=96),
    S.go("Gradient Fog", components=[S.comp("Rinten.GradientFog", "fog/gradient", Color="0.55,0.66,0.62,0.92", Height=16,
                                            VerticalFalloffExponent=1.1, StartDistance=4, EndDistance=36, FalloffExponent=1.15)]),
    S.go("Volume Fog", (0, 4, 0), components=[S.comp("Rinten.VolumetricFogVolume", "fog/volume", Bounds={"Mins": "-32,-6,-32", "Maxs": "32,10,32"},
                                                     Strength=0.48, FalloffExponent=0.8, Color="0.68,0.78,0.74,1")]),
]

pl = S.player((px(-23), height(px(-23), -23) + 1.15, 23), speed=4.5)
pl["Rotation"] = yaw(22)
objects += [pl, S.hud("The jungle. Walk the path north along the stream. Q returns.")]

S.objects = objects


def check_unique(objs):
    seen = {}

    def walk(o):
        for key, what in ((o["__guid"], o["Name"]), *((c["__guid"], c["__type"]) for c in o["Components"])):
            if key in seen:
                raise SystemExit(f"guid clash: {what} and {seen[key]}")
            seen[key] = what
        for c in o["Children"]:
            walk(c)

    for o in objs:
        walk(o)


if __name__ == "__main__":
    ensure_hulls()
    check_unique(S.objects)
    S.write("rendering/jungle.scene")
    register_in_menu("rendering/jungle.scene", "Jungle", "Rendering",
                     "A rainforest: stream, path, giants, stranglers, banyans, palms, bamboo, ferns, dead wood, moss and fog")
    print(len(objects), "objects")
