#!/usr/bin/env python3
"""scenes/rendering/jungle.scene - the jungle, laid out on the ground that
grow.py cut: a stream down the middle, a path beside it, and everything from
the catalogue placed as an object of its own - no clutter volumes. Every
thing stands on the ground at the ground's height, tilted to its slope
where it should be, sunk into it where it should be; a vine hangs from a
limb the tree really has, an arch runs from one trunk's bark to another's,
a log lies along the slope it fell on.

Positions here are in Blender's frame, the one grow.py thinks in (x, y along
the ground, z up), and turned into the engine's (x, up, -y) on the way out.
tools/jungle/ground.json is the ground's height grid and the lines of the
stream and the path; tools/jungle/sockets.json is what grow.py wrote about
each model - its box, and for a tree the frames of its trunk and limbs.

    python3 tools/jungle/scene.py
"""
import json, math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery"))
from common import Scene, ROOT, v, yaw, pitch_yaw, register_in_menu

HERE = os.path.dirname(os.path.abspath(__file__))
GROUND = json.load(open(os.path.join(HERE, "ground.json")))
SOCKETS = json.load(open(os.path.join(HERE, "sockets.json")))
MODELS = os.path.join(ROOT, "models", "jungle")

S = Scene("jungle", "Jungle",
          "A rainforest: a stream, a path, giants with buttresses and roots, stranglers, banyans, palms, bamboo, "
          "ferns and litter everywhere, dead wood, moss, and the fog that hides the rest.")


# ---------------------------------------------------------------------------
# The ground: heights, slopes and the two lines through it
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


def normal(x, y, d=0.4):
    """The ground's normal at (x, y), Blender frame, unit length."""
    dx = (height(x + d, y) - height(x - d, y)) / (2 * d)
    dy = (height(x, y + d) - height(x, y - d)) / (2 * d)
    L = math.sqrt(dx * dx + dy * dy + 1.0)
    return (-dx / L, -dy / L, 1.0 / L)


def slope(x, y):
    """Degrees off level."""
    return math.degrees(math.acos(max(-1.0, min(1.0, normal(x, y)[2]))))


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


def on_path(x, y, margin=0.0):
    return abs(x - px(y)) < 1.6 + margin


def in_stream(x, y, margin=0.0):
    return abs(x - sx(y)) < 1.8 + margin


SCENE = 60        # the square the walk is laid out on; the apron beyond it rises into the valley's sides
APRON = GROUND["size"]


def inside(x, y, edge=0.5):
    half = SCENE / 2 - edge
    return -half < x < half and -half < y < half


# ---------------------------------------------------------------------------
# Rotations: yaw about up, then the tilt that lays a thing on a slope
# ---------------------------------------------------------------------------

def q_mul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
            aw * bw - ax * bx - ay * by - az * bz)


def q_yaw(deg):
    h = math.radians(deg) / 2
    return (0.0, math.sin(h), 0.0, math.cos(h))


def q_tilt_to(n_engine):
    """The rotation that takes the engine's up onto a normal."""
    nx, ny, nz = n_engine
    c = max(-1.0, min(1.0, ny))
    if c > 0.99999:
        return (0.0, 0.0, 0.0, 1.0)
    # axis = up x n = (0,1,0) x (nx,ny,nz) = (nz, 0, -nx)
    ax, ay, az = nz, 0.0, -nx
    L = math.sqrt(ax * ax + az * az) or 1.0
    ang = math.acos(c)
    s = math.sin(ang / 2)
    return (ax / L * s, 0.0, az / L * s, math.cos(ang / 2))


def rotation(turn, x=None, y=None, align=0.0):
    """A quaternion string: yaw, and `align` (0..1) of the ground's tilt."""
    q = q_yaw(turn)
    if align > 0.0 and x is not None:
        nb = normal(x, y)
        ne = (nb[0] * align, nb[2], -nb[1] * align)
        L = math.sqrt(sum(c * c for c in ne))
        q = q_mul(q_tilt_to((ne[0] / L, ne[1] / L, ne[2] / L)), q)
    return v(*(round(c, 7) for c in q))


# ---------------------------------------------------------------------------
# Placing a model
# ---------------------------------------------------------------------------

placed = []   # (x, y, radius) of everything that takes room, so the scatter keeps clear
names = set()


def bounds_of(model):
    return SOCKETS.get(model, {}).get("bounds", [-0.5, -0.5, 0, 0.5, 0.5, 1])


def put(model, x, y, turn=0.0, scale=1.0, lift=0.0, sink=0.0, align=0.0, on_ground=True, collide=False, clear=0.0, name=None):
    """A model at Blender (x, y). It stands at the ground's height there, less
    `sink` (a fraction of its own height buried) plus `lift` metres; `align`
    tilts it to the slope, one being flat against it. `collide` adds a
    ModelCollider - the model's .mdl must carry a hull for that to do
    anything. `clear` reserves a footprint the scatter keeps out of."""
    bb = bounds_of(model)
    tall = (bb[5] - bb[2]) * scale
    z = (height(x, y) if on_ground else 0.0) + lift - sink * tall
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
    return S.go(name, (x, z, -y), rot=rotation(turn, x, y, align), scale=(scale, scale, scale), tags="world", components=comps)


def free(x, y, radius, path_margin=0.0, stream_margin=0.0):
    """Clear of the path, the stream and everything placed."""
    if not inside(x, y, radius):
        return False
    if on_path(x, y, path_margin + radius * 0.5) or in_stream(x, y, stream_margin + radius * 0.5):
        return False
    return all(math.hypot(x - qx, y - qy) > r + radius for qx, qy, r in placed)


def nearest_tree(x, y):
    """How far the nearest big trunk is - the shade a plant stands in."""
    return min((math.hypot(x - tx, y - ty) for tx, ty in tree_pos.values()), default=99.0)


def scatter(rng, models, count, radius, tries=60, scale=(0.85, 1.15), collide=False, clear=None, sink=0.0, align=0.0,
            path_margin=0.0, stream_margin=0.0, prefer=None, weights=None, max_slope=45.0, allow_path=False, allow_stream=False):
    """`count` models dropped where `free` says, `prefer(x, y)` (0..1) thinning
    the ones the dice put where they do not belong."""
    out = []
    for _ in range(count):
        for _ in range(tries):
            x, y = rng.uniform(-29.5, 29.5), rng.uniform(-29.5, 29.5)
            if not inside(x, y, radius):
                continue
            if not allow_path and on_path(x, y, path_margin + radius * 0.5):
                continue
            if not allow_stream and in_stream(x, y, stream_margin + radius * 0.5):
                continue
            if not all(math.hypot(x - qx, y - qy) > r + radius for qx, qy, r in placed):
                continue
            if slope(x, y) > max_slope:
                continue
            if prefer is not None and rng.random() > prefer(x, y):
                continue
            m = rng.choices(models, weights=weights)[0] if weights else rng.choice(models)
            out.append(put(m, x, y, rng.uniform(0, 360), rng.uniform(*scale), sink=sink, align=align, collide=collide, clear=clear or radius))
            break
    return out


# ---------------------------------------------------------------------------
# Sockets: where on a placed tree a thing can hang
# ---------------------------------------------------------------------------

def to_world(tree, p):
    """A point in a placed tree's own (Blender) frame into the scene's Blender frame."""
    x, y, turn, scale = tree_place[tree]
    c, s = math.cos(math.radians(turn)), math.sin(math.radians(turn))
    lx, ly, lz = p[0] * scale, p[1] * scale, p[2] * scale
    return (x + lx * c - ly * s, y + lx * s + ly * c, height(x, y) + lz)


def limb_points(tree, min_z=4.0, min_r=0.0):
    """Points on a placed tree's limbs, high enough and thick enough, with the
    world point on the limb's underside and the limb's radius."""
    model = tree_model[tree]
    out = []
    for limb in SOCKETS.get(model, {}).get("limbs", []):
        for fr in limb[1:-1]:
            px_, py_, pz_, tx, ty, tz, r, u = fr
            if pz_ < min_z or r < min_r:
                continue
            wx, wy, wz = to_world(tree, (px_, py_, pz_))
            out.append(((wx, wy, wz - r * tree_place[tree][3]), r))
    return out


def trunk_point(tree, z):
    """The trunk's centre and radius at about height z (the tree's own frame), in the world."""
    model = tree_model[tree]
    frames = SOCKETS.get(model, {}).get("trunk", [])
    if not frames:
        x, y, turn, scale = tree_place[tree]
        return (x, y, height(x, y) + z), 0.5
    best = min(frames, key=lambda fr: abs(fr[2] - z))
    wx, wy, wz = to_world(tree, best[:3])
    return (wx, wy, wz), best[6] * tree_place[tree][3]


# ---------------------------------------------------------------------------
# Collision in the .mdl files: a triangle mesh for what is walked on, a
# capsule up the trunk of a tree
# ---------------------------------------------------------------------------

HULL = {"__type": "RenderMesh", "Name": "", "Enabled": True, "Bone": "", "Surface": "", "Tags": "", "Folder": ""}

MESH_COLLIDERS = ["ground", "ground_apron", "log_a", "log_b", "logmossy_a", "logmossy_b", "logmossy_c", "uprooted_a", "uprooted_b",
                  "rootmat_a", "rootmat_b", "stump_a", "stump_b", "stump_c", "broken_a", "broken_b",
                  "rock_a", "rock_b", "rock_c", "rockflat_a", "rockflat_b", "rockflat_c", "rockflat_d", "rockslab_a",
                  "boulder_a", "boulder_b", "rockmid_a", "rockmid_b", "rockmid_c", "rockbig_a", "rockbig_b", "rockbig_c",
                  "cliff_a", "cliff_b", "streamstone_a", "streamstone_b", "streamstone_c", "rockstack_a", "rockstack_b"]

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
# The layout
# ---------------------------------------------------------------------------

rng = random.Random(7)
objects = [put("ground", 0, 0, on_ground=False, collide=True, name="Ground"),
           put("ground_apron", 0, 0, on_ground=False, collide=True, name="Ground apron"),
           put("water", 0, 0, on_ground=False, name="Stream")]

tree_place = {}   # name -> (x, y, turn, scale)
tree_model = {}   # name -> model


def tree(model, x, y, turn, clear, scale=1.0, name=None):
    name = name or model
    o = put(model, x, y, turn=turn, scale=scale, collide=True, clear=clear, name=name)
    tree_place[name] = (x, y, turn, scale)
    tree_model[name] = model
    return o


# -- the big trees, by hand: the composition the references have ------------
objects += [
    tree("tree_lean_a", px(-8) - 3.5, -8, 15, 2.5),           # the trunk over the path
    tree("tree_giant_b", px(-2) + 9, -2, 40, 4),
    tree("mossy_giant", px(8) - 12, 8, 200, 4),
    tree("tree_giant_a", sx(16) - 9, 16, 110, 4),
    tree("tree_giant_c", px(-27) + 9, -27, 300, 3.5),
    tree("banyan_a", px(20) + 13, 20, 70, 6),
    tree("banyan_b", px(-24) + 12, -24, 250, 5),
    tree("strangler_a", px(-16) - 8, -16, 0, 2.5),
    tree("strangler_b", sx(4) - 14, 4, 130, 2.5),
    tree("tree_winding_a", px(2) + 5, 2, 170, 2.5),
    tree("tree_winding_b", sx(-12) - 6, -12, 20, 2.5),
    tree("tree_winding_c", px(26) - 6, 26, 95, 2.5),
    tree("tree_lean_b", sx(24) - 5, 24, 60, 2.5),
    tree("tree_forked_a", px(14) + 6, 14, 210, 2),
    tree("tree_forked_b", sx(-22) - 9, -22, 340, 2),
    tree("climbed_a", px(-12) + 7, -12, 0, 2),
    tree("climbed_b", sx(12) - 4, 12, 45, 2),
]
tree_pos = {n: (p[0], p[1]) for n, p in tree_place.items()}

# -- the picket behind: tall trunks that go into the fog --------------------
for i in range(34):
    for _ in range(80):
        x, y = rng.uniform(-29, 29), rng.uniform(-29, 29)
        if free(x, y, 2.2, path_margin=1.5, stream_margin=1.0) and slope(x, y) < 30:
            m = rng.choice(["tree_tall_a", "tree_tall_b", "tree_tall_c", "tree_tall_d"])
            objects.append(tree(m, x, y, rng.uniform(0, 360), 2.2, scale=rng.uniform(0.85, 1.15), name=f"{m} #{i}"))
            break
tree_pos = {n: (p[0], p[1]) for n, p in tree_place.items()}

# -- the wall of forest on the valley's sides, beyond the walk: what the fog
# shows as silhouettes and what fills the horizon --------------------------
wall = []
big = ["tree_giant_a", "tree_giant_b", "tree_giant_c", "banyan_a", "strangler_a", "mossy_giant"]
for i in range(150):
    for _ in range(60):
        x, y = rng.uniform(-APRON / 2 + 6, APRON / 2 - 6), rng.uniform(-APRON / 2 + 6, APRON / 2 - 6)
        d = max(abs(x), abs(y))
        if d < SCENE / 2 + 1.5 or (x < 0 and y > 0 and rng.random() < 0.5):
            continue
        r = 3.0 if d < 42 else 5.0
        if not all(math.hypot(x - qx, y - qy) > r for qx, qy, _ in wall):
            continue
        if d < 45 and rng.random() < 0.3:
            m = rng.choice(big)
        else:
            m = rng.choice(["tree_tall_a", "tree_tall_b", "tree_tall_c", "tree_tall_d", "tree_tall_b", "palm_c", "tree_arch_a"])
        wall.append((x, y, r))
        objects.append(put(m, x, y, rng.uniform(0, 360), rng.uniform(0.9, 1.3), name=f"wall {m} #{i}"))
        break
for i in range(90):
    for _ in range(40):
        x, y = rng.uniform(-APRON / 2 + 4, APRON / 2 - 4), rng.uniform(-APRON / 2 + 4, APRON / 2 - 4)
        if max(abs(x), abs(y)) < SCENE / 2 + 1.0:
            continue
        m = rng.choice(["bush_a", "bush_b", "fern_a", "fern_c", "broadleaf_a", "palm_fan_a", "treefern_a", "banana_b", "elephant_a"])
        objects.append(put(m, x, y, rng.uniform(0, 360), rng.uniform(1.2, 2.2), sink=0.03, align=0.5, name=f"wall {m} #{i}"))
        break

# -- palms, tree ferns, bamboo, the odd ones, by hand near the walk ----------
objects += [
    tree("palm_a", px(-12) + 4, -12, 30, 1.5),
    tree("palm_c", sx(-5) - 5, -5, 200, 1.5),
    tree("palm_b", px(12) + 4, 12, 110, 1.5),
    tree("palm_fan_a", px(4) - 5, 4, 0, 1.5),
    tree("palm_fan_b", sx(-14) + 4, -14, 80, 1.2),
    tree("treefern_a", sx(-8) + 3.5, -8, 0, 1.2),
    tree("treefern_b", sx(6) + 3.5, 6, 140, 1.2),
    put("bambooclump_a", px(-18) + 4, -18, turn=0, clear=1.5, sink=0.01),
    put("bambooclump_b", px(-26) - 4, -26, turn=60, clear=1.8, sink=0.01),
    put("bambooclump_a", px(-20) - 4.5, -20, turn=200, scale=0.9, clear=1.5, sink=0.01),
    put("bamboo_b", px(-15) - 3.5, -15, turn=0, clear=0.5, sink=0.01),
    put("bamboo_c", px(-22) + 3.5, -22, turn=90, clear=0.5, sink=0.01),
    put("stilt_a", sx(10) + 4, 10, turn=0, clear=1.5, sink=0.02),
    put("stilt_b", sx(-20) - 4, -20, turn=120, clear=1.5, sink=0.02),
    put("stilt_c", px(28) + 6, 28, turn=0, clear=1.5, sink=0.02),
    put("cycad_a", px(0) - 4, 0, turn=40, clear=1, sink=0.03, align=0.5),
    put("cycad_b", px(24) + 5, 24, turn=0, clear=1.2, sink=0.03, align=0.5),
    put("banana_a", px(14) - 5, 14, turn=0, clear=1.5, sink=0.02),
    put("banana_b", sx(22) + 5, 22, turn=180, clear=1.8, sink=0.02),
    put("reeds_a", sx(-16) + 2.6, -16, clear=0.5, sink=0.03, align=0.6),
    put("reeds_b", sx(2) - 2.6, 2, turn=50, clear=0.5, sink=0.03, align=0.6),
    put("reeds_a", sx(20) + 2.6, 20, turn=120, clear=0.5, sink=0.03, align=0.6),
]
# more palms and tree ferns, scattered where the walk can see them
objects += scatter(rng, ["palm_a", "palm_b", "palm_fan_a", "palm_fan_b", "treefern_a", "treefern_b", "cycad_b", "banana_a"], 14, 1.5,
                   collide=True, sink=0.02, path_margin=1.0, stream_margin=0.5, max_slope=30)
objects += scatter(rng, ["tree_thin_a", "tree_thin_b", "tree_arch_a", "tree_arch_b"], 26, 1.0, sink=0.02, path_margin=1.0,
                   stream_margin=0.5, max_slope=35)

# -- dead wood: logs lie along the slope, sunk a little; stumps and snags stand
objects += [
    put("logmossy_a", px(6) + 2, 6, turn=70, collide=True, clear=1.5, sink=0.12, align=1.0),
    put("logmossy_b", sx(-2) + 6, -2, turn=20, collide=True, clear=2, sink=0.12, align=1.0),
    put("log_a", px(-28) + 6, -28, turn=150, collide=True, clear=1.5, sink=0.12, align=1.0),
    put("log_b", sx(28) - 7, 28, turn=100, collide=True, clear=2, sink=0.12, align=1.0),
    put("logmossy_c", px(18) - 4, 18, turn=10, collide=True, clear=1, sink=0.15, align=1.0),
    put("uprooted_a", sx(28) - 4, 28, turn=30, collide=True, clear=3, sink=0.05, align=0.6),
    put("uprooted_b", px(-30) + 10, -29, turn=200, collide=True, clear=2.5, sink=0.05, align=0.6),
    tree("snag_a", px(18) - 7, 18, 0, 1.2),
    tree("snag_b", sx(-10) - 8, -10, 90, 1.5),
    tree("snag_c", px(-4) + 7, -4, 200, 1),
    put("stump_a", px(10) - 3.5, 10, turn=0, collide=True, clear=1, sink=0.06, align=0.7),
    put("stump_b", sx(-24) + 5, -24, turn=90, collide=True, clear=1.2, sink=0.06, align=0.7),
    put("stump_c", px(-8) + 4, -8, turn=180, collide=True, clear=0.8, sink=0.06, align=0.7),
    put("broken_a", px(26) - 9, 26, turn=250, collide=True, clear=2, sink=0.03),
    put("broken_b", sx(-28) - 6, -28, turn=30, collide=True, clear=2, sink=0.03),
    put("rootmat_a", *tree_pos["mossy_giant"], turn=20, collide=True, sink=0.15, align=1.0),
    put("rootmat_b", *tree_pos["tree_giant_a"], turn=70, collide=True, sink=0.15, align=1.0),
    put("vinetangle_b", px(10) - 4.5, 10.8, sink=0.05, align=1.0),
]
objects += scatter(rng, ["debris_a", "debris_b", "debris_c"], 30, 0.8, sink=0.25, align=1.0, path_margin=0.5, allow_path=False)
objects += scatter(rng, ["fallenfrond_a", "fallenfrond_b"], 14, 0.6, sink=0.0, align=1.0, path_margin=0.0, allow_path=True)

# -- the stream: stones in the bed, sunk and tilted with it; boulders on the banks
bed = ["streamstone_a", "streamstone_b", "streamstone_c", "rockflat_a", "rockflat_b", "rockflat_d", "rock_b", "streamstone_b"]
bank = ["boulder_a", "boulder_b", "rockbig_a", "rockmid_a", "rockmid_b", "rockmid_c", "rockstack_a", "rockflat_c", "rockslab_a"]
y = -29.0
i = 0
while y < 29:
    x = sx(y) + rng.uniform(-1.3, 1.3)
    objects.append(put(bed[i % len(bed)], x, y, turn=rng.uniform(0, 360), scale=rng.uniform(0.7, 1.2), sink=0.3, align=1.0, collide=True, clear=0.8))
    if i % 3 != 2:
        x2 = sx(y) + rng.uniform(-1.5, 1.5)
        objects.append(put("streamstone_a", x2, y + 1.2, turn=rng.uniform(0, 360), scale=rng.uniform(0.5, 0.9), sink=0.35, align=1.0, clear=0.4))
    if i % 2 == 0:
        side = 1 if i % 4 == 0 else -1
        bx, by = sx(y) + side * rng.uniform(2.6, 4.0), y + rng.uniform(-1, 1)
        objects.append(put(bank[(i // 2) % len(bank)], bx, by, turn=rng.uniform(0, 360), sink=0.25, align=0.9, collide=True, clear=1.5))
    y += rng.uniform(2.0, 3.2)
    i += 1
objects += [
    put("cliff_a", -26, 10, turn=20, collide=True, clear=5, sink=0.2, align=0.5),
    put("cliff_b", 27, -14, turn=110, collide=True, clear=6, sink=0.2, align=0.5),
    put("rockbig_b", -22, -6, turn=60, collide=True, clear=3, sink=0.25, align=0.8),
    put("rockbig_c", 24, 6, turn=300, collide=True, clear=3.5, sink=0.25, align=0.8),
    put("rockstack_b", px(-6) + 10, -6, turn=0, collide=True, clear=1.5, sink=0.1, align=0.8),
]
objects += scatter(rng, ["rock_a", "rock_b", "rockmid_a", "rockflat_a"], 24, 0.8, sink=0.3, align=1.0, collide=True, path_margin=0.3,
                   stream_margin=0.0, weights=[3, 2, 1, 1])
objects += scatter(rng, ["pebbles_a", "pebbles_b"], 20, 0.8, sink=0.35, align=1.0, allow_path=True, allow_stream=True,
                   prefer=lambda x, y: 1.0 if in_stream(x, y, 3.0) else 0.25)


# -- vines: hung from limbs the trees have, strung from bark to bark --------
def hang(model, tree, choose, turn=None, scale=1.0, lift=0.0, name=None):
    """A model whose origin is its top, at a limb's underside."""
    points = limb_points(tree, min_z=4.5, min_r=0.12)
    if not points:
        return None
    (wx, wy, wz), r = choose(points)
    return put(model, wx, wy, turn=turn if turn is not None else rng.uniform(0, 360), scale=scale, lift=wz - height(wx, wy) + lift, name=name)


def strung(model, span, a, b, z):
    """An arch from tree a's bark to tree b's, at about height z."""
    (ax, ay, az), ra = trunk_point(a, z)
    (bx, by, bz), rb = trunk_point(b, z)
    d = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / d, (by - ay) / d
    ax, ay = ax + ux * ra, ay + uy * ra
    bx, by = bx - ux * rb, by - uy * rb
    dist = math.hypot(bx - ax, by - ay)
    turn = math.degrees(math.atan2(by - ay, bx - ax))
    return put(model, ax, ay, turn=turn, scale=dist / span, lift=az - height(ax, ay), name=f"{model} {a}-{b}")


def highest(points):
    return max(points, key=lambda p: p[0][2])


def pick(rng, k=0):
    return lambda points: sorted(points, key=lambda p: -p[0][2])[min(k, len(points) - 1)]


def outermost(tree):
    x0, y0 = tree_pos[tree]
    return lambda points: max(points, key=lambda p: math.hypot(p[0][0] - x0, p[0][1] - y0))


vines = [
    hang("vinehang_b", "tree_giant_b", outermost("tree_giant_b")),
    hang("vinehang_a", "tree_giant_b", pick(rng, 3)),
    hang("mossdrape_b", "tree_giant_b", pick(rng, 6)),
    hang("vinehang_a", "mossy_giant", outermost("mossy_giant")),
    hang("mossdrape_b", "mossy_giant", pick(rng, 4)),
    hang("vinehang_c", "tree_lean_a", outermost("tree_lean_a")),
    hang("mossdrape_a", "tree_lean_a", pick(rng, 2)),
    hang("vinehang_b", "banyan_a", outermost("banyan_a"), scale=0.8),
    hang("vinerope_a", "banyan_a", pick(rng, 2)),
    hang("aerialroots_a", "banyan_b", outermost("banyan_b")),
    hang("vinerope_b", "tree_giant_a", outermost("tree_giant_a")),
    hang("mossdrape_a", "tree_giant_a", pick(rng, 3)),
    hang("aerialroots_b", "strangler_a", pick(rng, 1)),
    hang("mossdrape_a", "tree_winding_c", pick(rng, 1)),
    hang("vinehang_c", "tree_winding_a", pick(rng, 1)),
    hang("mossdrape_b", "tree_giant_c", pick(rng, 2)),
    hang("vinehang_a", "climbed_b", pick(rng, 1)),
    strung("vinearch_a", 8, "tree_lean_a", "tree_giant_b", 7.0),
    strung("vinearch_b", 12, "mossy_giant", "strangler_b", 8.0),
    strung("vinearch_a", 8, "tree_winding_a", "tree_forked_a", 6.5),
    strung("vinearch_b", 12, "tree_giant_a", "climbed_b", 7.5),
]
objects += [o for o in vines if o is not None]
# and a curtain from a few of the tall picket trees
tall = [n for n in tree_place if n.startswith("tree_tall")]
for n in rng.sample(tall, 8):
    o = hang(rng.choice(["vinehang_a", "vinehang_c", "mossdrape_a"]), n, pick(rng, 0), scale=rng.uniform(0.7, 1.0), name=f"vines on {n}")
    if o:
        objects.append(o)
# lianas coiled on the ground, where it is nearly level
objects += scatter(rng, ["liana_a", "liana_b", "liana_c"], 6, 2.5, sink=0.02, align=1.0, max_slope=8, path_margin=1.0)
objects += scatter(rng, ["vinetangle_a", "vinetangle_b"], 8, 1.2, sink=0.05, align=1.0, max_slope=15, path_margin=0.5)

# -- shelf fungi on the dead wood, facing out of the bark --------------------
for snag_name, z in (("snag_a", 1.6), ("snag_b", 1.2), ("snag_c", 0.9), ("snag_b", 3.0)):
    (cx, cy, cz), r = trunk_point(snag_name, z)
    a = rng.uniform(0, 360)
    fx, fy = cx + math.cos(math.radians(a)) * r * 0.95, cy + math.sin(math.radians(a)) * r * 0.95
    objects.append(put(rng.choice(["brackets_a", "brackets_b"]), fx, fy, turn=a, lift=cz - height(fx, fy), name=f"brackets on {snag_name} {z}"))

# -- the understory, by rule rather than by volume ---------------------------
def shade(x, y):
    d = nearest_tree(x, y)
    return 1.0 if d < 5 else 0.75 if d < 9 else 0.45


def damp(x, y):
    d = abs(x - sx(y))
    return 1.0 if d < 6 else 0.5 if d < 10 else 0.2


ferns = ["fern_a", "fern_b", "fern_c", "fern_d"]
objects += scatter(rng, ferns, 520, 0.55, sink=0.04, align=0.8, prefer=shade, weights=[3, 2, 3, 1], path_margin=0.4, max_slope=40)
objects += scatter(rng, ["broadleaf_a", "broadleaf_b", "elephant_a", "elephant_b"], 90, 0.7, sink=0.03, align=0.5, prefer=damp,
                   weights=[3, 3, 1, 1], path_margin=0.6)
objects += scatter(rng, ["lily_a", "lily_b", "fanplant_a", "fanplant_b"], 70, 0.6, sink=0.03, align=0.6, path_margin=0.4)
objects += scatter(rng, ["bush_a", "bush_b"], 40, 1.0, sink=0.03, align=0.4, prefer=shade, path_margin=0.8)
objects += scatter(rng, ["sapling_a", "sapling_b"], 60, 0.4, sink=0.03, align=0.3, path_margin=0.5)
objects += scatter(rng, ["grass_a", "grass_b"], 260, 0.45, sink=0.04, align=0.9, allow_path=False, allow_stream=False, scale=(0.6, 0.95),
                   path_margin=0.2, prefer=lambda x, y: 0.9 if on_path(x, y, 2.5) or in_stream(x, y, 3.5) else 0.3)
objects += scatter(rng, ["mosscushion_a", "mosscushion_b", "mosscushion_c", "mosscarpet_a"], 120, 0.5, sink=0.12, align=1.0,
                   prefer=lambda x, y: min(1.0, 0.5 * shade(x, y) + 0.5 * damp(x, y)), path_margin=0.3)
objects += scatter(rng, ["litter_a", "litter_b"], 200, 0.4, sink=0.02, align=1.0, allow_path=True, prefer=shade, clear=0.0, scale=(0.5, 0.85))

# -- light, fog, the player, the HUD ----------------------------------------
# The sun low, from behind and to the left of the walk, so trunks are lit on
# their edges and the fog glows between them.
# An overcast sky - materials/skybox/overcast.mat, the engine's sky shader with
# its cloud cover nearly full - and the distance fog takes its colour from that
# sky, so what is far away sinks into the same white the sky is.
objects += [
    S.environment(sun_brightness=0.7, sun_rot=pitch_yaw(-34, 155), sun_color="1,0.96,0.9,1", ambient="0.16,0.22,0.18,1",
                  sky_tint="0.9,0.93,0.92,1", shadow_detail=96, sky_material="materials/skybox/overcast.mat"),
    S.go("Distance Fog", components=[S.comp("Rinten.CubemapFog", "fog/distance", Tint="0.86,0.88,0.84,0.85", StartDistance=6, EndDistance=60,
                                            FalloffExponent=1.25, HeightStart=-6, HeightWidth=26, HeightExponent=1.1)]),
    S.go("Volume Fog", (0, 4, 0), components=[S.comp("Rinten.VolumetricFogVolume", "fog/volume", Bounds={"Mins": "-32,-6,-32", "Maxs": "32,10,32"},
                                                     Strength=0.08, FalloffExponent=0.8, Color="0.68,0.78,0.74,1")]),
]

# The camera keeps a picture of the depth for the water to read the bed
# through - see DepthPicture - and darkens the corners with occlusion.
# The grade: a little less saturated and a touch more contrast than the raw
# render - the look of the references, which are overcast and damp. The cool
# of them is the sky's own, not a grade.
pl = S.player((px(-23), height(px(-23), -23) + 1.15, 23), speed=4.5, camera_extra=[
    S.comp("Rinten.DepthPicture", "depthpicture", __version=1),
    S.comp("Rinten.AmbientOcclusion", "ssao", __version=1, Intensity=0.8),
    S.comp("Rinten.ColorAdjustments", "adjust", __version=1, Blend=1.0, Saturation=0.9, HueRotate=0.0, Brightness=1.0, Contrast=1.03),
])
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
