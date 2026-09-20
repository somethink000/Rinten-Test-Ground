#!/usr/bin/env python3
"""Jungle geometry, grown from seeds inside Blender and written out as FBX with
a .mdl beside each - no materials, no textures, just the shapes.

Everything comes from a handful of primitives: a `sweep` (a tube along any
path, its radius a function of how far along), a `strip` (a leaf or frond: a
row of verts carried along an arch, its width a function of how far along),
and `catmull` (a smooth path through a few control points). On those stand
the generators - trees of several habits, palms, ferns, vines, rocks, the
ground - and the CATALOGUE at the bottom says which seeds become which files.
Adding a model is one line there.

Run inside Blender - the MCP bridge or `blender -b -P tools/jungle/grow.py`:

    JUNGLE_ROOT = "/path/to/project"   # optional, the checkout to write into
    exec(open("tools/jungle/grow.py").read()); build_all()

Blender is Z-up here; the FBX export turns that into the engine's Y-up, and
ufbx brings the units to metres, so every number below is in metres.
"""
import bpy, bmesh, math, random, os, json
from mathutils import Vector, Matrix, noise

ROOT = globals().get("JUNGLE_ROOT", "/home/sampesss/Documents/Rinten Projects/Rinten-Test-Ground")
OUT = "models/jungle"

# Every face is tagged with one of these, and they become material slots of
# the same name in the FBX - so a material can be pinned to "Leaf" later by a
# remap, without touching the geometry again.
MATERIALS = ["Bark", "Leaf", "Bamboo", "Rock", "Ground", "Vine", "Moss", "Fungus", "Litter"]

TAU = math.tau
Z = Vector((0, 0, 1))


def lerp(a, b, t):
    return a + (b - a) * t


def smoothstep(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def fbm(p, octaves=4, lac=2.0, gain=0.5):
    """Layered Perlin in -1..1, the general purpose lumpiness."""
    amp, freq, total, norm = 1.0, 1.0, 0.0, 0.0
    for _ in range(octaves):
        total += amp * noise.noise(p * freq)
        norm += amp
        amp *= gain
        freq *= lac
    return total / norm


def catmull(pts, n):
    """n+1 points along a Catmull-Rom spline through pts."""
    P = [pts[0]] + list(pts) + [pts[-1]]
    segs = len(pts) - 1
    out = []
    for i in range(n + 1):
        u = i / n * segs
        k = min(int(u), segs - 1)
        s = u - k
        p0, p1, p2, p3 = P[k], P[k + 1], P[k + 2], P[k + 3]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * s + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s * s
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * s * s * s))
    return out


def perp(d):
    """Some unit vector at right angles to d."""
    ref = Vector((1, 0, 0)) if abs(d.x) < 0.9 else Vector((0, 1, 0))
    return (ref - d * ref.dot(d)).normalized()


def around(d, rng, spread):
    """A random direction within `spread` radians of d."""
    a = perp(d)
    b = d.cross(a)
    ang = rng.uniform(0, TAU)
    tilt = rng.uniform(0, spread)
    return (d * math.cos(tilt) + (a * math.cos(ang) + b * math.sin(ang)) * math.sin(tilt)).normalized()


class Mesh:
    """Positions and faces collected by the generators, turned into one Blender
    object at the end. Faces carry the index of their material slot."""

    def __init__(self):
        self.verts = []
        self.faces = []
        # What a tree generator leaves behind for the things that grow on it:
        # the trunk's frames, each first-order limb's frames, the tip of every
        # twig. Empty for anything that is not a tree.
        self.trunk = []
        self.limbs = []
        self.tips = []
        self.smooth = True

    def vert(self, p):
        self.verts.append(Vector(p))
        return len(self.verts) - 1

    def face(self, idx, mat):
        self.faces.append((tuple(idx), MATERIALS.index(mat)))

    def quad_strip(self, ring_a, ring_b, mat, closed=True):
        n = len(ring_a)
        last = n if closed else n - 1
        for i in range(last):
            j = (i + 1) % n
            self.face((ring_a[i], ring_a[j], ring_b[j], ring_b[i]), mat)

    def tube(self, rings, mat, cap=True):
        for a, b in zip(rings, rings[1:]):
            self.quad_strip(a, b, mat)
        if cap:
            self.face(list(reversed(rings[-1])), mat)

    def to_object(self, name):
        me = bpy.data.meshes.new(name)
        me.from_pydata([tuple(v) for v in self.verts], [], [f for f, _ in self.faces])
        for m in MATERIALS:
            me.materials.append(bpy.data.materials.get(m) or bpy.data.materials.new(m))
        me.polygons.foreach_set("material_index", [m for _, m in self.faces])
        me.polygons.foreach_set("use_smooth", [self.smooth] * len(me.polygons))
        me.validate()
        me.update()
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(me)
        bm.free()
        me.update()
        return ob


# ---------------------------------------------------------------------------
# Primitives: the tube and the leaf
# ---------------------------------------------------------------------------

def sweep(mesh, path, radius_at, sides, mat, seed=0, lumps=0.05, grooves=0.0, knots=0.0,
          scars=0.0, flutes=0, flare=0.0, flute_height=0.25, cap=True):
    """A tube along `path`, `radius_at(u)` wide at fraction u of its length.

    The frame is carried along by parallel transport, so a winding trunk does
    not twist. The relief: `lumps` is noise on the radius, `grooves` nine bark
    ridges around, `knots` occasional burls, `scars` the ring marks of a palm,
    and `flutes`/`flare` widen the first `flute_height` of the tube into that
    many buttress ridges. Returns one frame per ring: (point, tangent, normal,
    binormal, radius, u)."""
    n = len(path)
    tangents = [(path[min(i + 1, n - 1)] - path[max(i - 1, 0)]).normalized() for i in range(n)]
    nrm = perp(tangents[0])
    total = sum((path[i + 1] - path[i]).length for i in range(n - 1)) or 1.0
    arc = 0.0
    rings, frames = [], []
    for i in range(n):
        t = tangents[i]
        if i:
            arc += (path[i] - path[i - 1]).length
            nrm = nrm - t * nrm.dot(t)
            nrm = nrm.normalized() if nrm.length > 1e-6 else perp(t)
        bn = t.cross(nrm).normalized()
        u = arc / total
        r = radius_at(u)
        ring = []
        for k in range(sides):
            ang = k / sides * TAU
            c, s = math.cos(ang), math.sin(ang)
            rad = r * (1.0 + lumps * fbm(Vector((c * 2 + seed, s * 2, arc * 1.5))))
            if grooves:
                rad *= 1.0 + grooves * math.cos(9 * ang + seed + arc * 0.4) * (1.0 - u * 0.5)
            if knots:
                rad *= 1.0 + knots * max(0.0, fbm(Vector((c + seed * 3, s, arc * 0.8)), 2) - 0.2) * 3
            if scars:
                rad *= 1.0 + scars * max(0.0, math.cos(arc * TAU / 0.28)) ** 6
            if flutes and u < flute_height:
                ridge = max(0.0, math.cos(flutes * ang + seed)) ** 6
                rad += flare * radius_at(0) * ridge * (1.0 - u / flute_height) ** 1.3
            ring.append(mesh.vert(path[i] + nrm * (c * rad) + bn * (s * rad)))
        rings.append(ring)
        frames.append((path[i], t, nrm, bn, r, u))
    mesh.tube(rings, mat, cap)
    return frames


def bent_path(start, d, length, bend, bend_dir, wiggle, seed, steps):
    """A path from `start` along `d`, curving toward `bend_dir` and wandering
    by `wiggle` - a limb, a stalk, a strand."""
    d = d.normalized()
    a = perp(d)
    b = d.cross(a)
    pts = []
    for i in range(steps + 1):
        t = i / steps
        p = start + d * (t * length) + bend_dir * (bend * length * t * t)
        w = (a * fbm(Vector((t * 2.5, seed * 0.37, 1.3))) + b * fbm(Vector((7.1, t * 2.5, seed * 0.37)))) * wiggle * length * t
        pts.append(p + w)
    return pts


def winding_path(rng, start, height, amp, lean, steps, knots_n=5):
    """A trunk that wanders: a random walk of a few control points, leaning
    one way, smoothed. `amp` is how far it strays per step as a fraction of
    height; 0.05 is a straight-ish tree, 0.4 an arch across the path."""
    yaw = rng.uniform(0, TAU)
    lean_dir = Vector((math.cos(yaw), math.sin(yaw), 0))
    # The first bit stands straight, so the base sits in the ground however
    # hard the rest of it leans.
    pts = [Vector(start), Vector(start) + Z * height * 0.04]
    off = Vector((0, 0, 0))
    for i in range(1, knots_n + 1):
        z = i / knots_n * height
        ease = 1.7 * (1.0 - (i - 1) / knots_n)
        off += lean_dir * (lean * ease * height / knots_n) + Vector((rng.gauss(0, 1), rng.gauss(0, 1), 0)) * amp * height / knots_n
        pts.append(Vector(start) + Vector((off.x, off.y, z)))
    path = catmull(pts, steps)
    # The spline overshoots backwards where the lean begins; the bottom of
    # the trunk is pinned straight up over its base.
    for q in path:
        if q.z < height * 0.05:
            q.x, q.y = start[0], start[1]
    return path


def strip(mesh, rng, base, d, up, length, width, profile, droop, segs=12, cross=3,
          crease=0.25, cup=0.0, twist=0.0, mat="Leaf"):
    """A leaf or frond: `cross` verts across, swept along an arch that rises
    with `up` and falls with `droop`, its width `width * profile(s)`. The
    middle vert is raised by `crease` so a flat strip still has a rib."""
    d = d.normalized()
    side = d.cross(Z)
    side = side.normalized() if side.length > 1e-4 else Vector((1, 0, 0))
    rows = []
    for i in range(segs + 1):
        s = i / segs
        p = base + d * (s * length) + Z * (length * (up * s - droop * s * s))
        w = width * profile(s)
        tw = twist * s
        row = []
        for c in range(cross):
            u = -1 + 2 * c / (cross - 1) if cross > 1 else 0.0
            lift = -w * crease * abs(u) + w * cup * u * u
            q = p + side * (u * w * math.cos(tw)) + Z * (lift + u * w * math.sin(tw))
            row.append(mesh.vert(q))
        rows.append(row)
    for a, b in zip(rows, rows[1:]):
        mesh.quad_strip(a, b, mat, closed=False)


OVAL = lambda s: math.sin(math.pi * s ** 0.6) ** 0.8
HEART = lambda s: math.sin(math.pi * s ** 0.45) ** 0.6
STRAP = lambda s: math.sin(math.pi * s ** 0.85) ** 0.5
BLADE = lambda s: 1.0 - s * 0.9


def pinnate(p, amp=0.45):
    """A serrated outline: the leaflets of a fern or a palm frond."""
    return lambda s: math.sin(math.pi * s ** 0.65) ** 0.9 * (1 - amp + amp * abs(math.sin(s * p * math.pi)))


def leaves(mesh, rng, center, d, count, length, width, spread=1.2, up=(0.0, 0.3), droop=(0.2, 0.7)):
    """A cluster of oval leaves fanned about `d` - the end of a twig, a bush."""
    for _ in range(count):
        dd = around(d, rng, spread)
        L = length * rng.uniform(0.7, 1.3)
        strip(mesh, rng, center + dd * rng.uniform(0, 0.1), dd, rng.uniform(*up), L, L * width, OVAL,
              rng.uniform(*droop), segs=3, cross=3, crease=0.15, twist=rng.uniform(-0.4, 0.4))


def fan(mesh, rng, base, d, radius, blades=14, spread=2.4, pleat=0.45):
    """A fan palm leaf: pleated blades in an arc about d, drooping at the rim."""
    d = d.normalized()
    axis = Z if abs(d.z) < 0.9 else Vector((1, 0, 0))
    for i in range(blades):
        a = -spread / 2 + spread * i / (blades - 1)
        bd = Matrix.Rotation(a, 3, axis) @ d
        strip(mesh, rng, base, bd, 0.2 + 0.4 * math.cos(a), radius * (0.8 + 0.2 * math.cos(a)), radius * 0.11, BLADE,
              0.5 + rng.uniform(0, 0.3), segs=5, cross=3, crease=pleat)


# ---------------------------------------------------------------------------
# Trees
# ---------------------------------------------------------------------------

def branch(mesh, rng, start, d, length, r0, r1, depth, spec, seed):
    """A limb and everything that grows from it: children at the next depth,
    and leaf clusters once there are no more children."""
    kids = spec["kids"]
    steps = max(4, int(length * 2))
    # Limbs curve every which way - up as often as not, but sideways too,
    # which is the difference between a broom and a crown.
    bend_dir = around(Z, rng, 1.3)
    path = bent_path(start, d, length, rng.uniform(*spec["bend"]), bend_dir, spec["wiggle"], seed, steps)
    sides = max(5, spec["sides"] - depth * 4)
    frames = sweep(mesh, path, lambda u: lerp(r0, r1, u ** spec["taper"]), sides, "Bark", seed,
                   lumps=spec["lumps"] * (1 if depth == 0 else 0.5), knots=spec.get("knots", 0.0) * (1 if depth == 0 else 0.5))
    if depth <= 1:
        mesh.limbs.append(frames)
    tips = [(frames[-1][0], frames[-1][1])]
    mesh.tips.append(tips[0])
    if depth < len(kids):
        n = rng.randint(max(1, kids[depth] - 1), kids[depth] + 1)
        for i in range(n):
            u = rng.uniform(*spec["where"])
            k = min(int(u * (len(frames) - 1)), len(frames) - 2)
            p, t, nrm, bn, r, _ = frames[k]
            ang = i / n * TAU + rng.uniform(-0.6, 0.6)
            out = (nrm * math.cos(ang) + bn * math.sin(ang)).normalized()
            up = rng.uniform(*spec["up"])
            cd = (t * 0.7 + out * 0.6 * (1 - up) + Z * up * 0.6).normalized()
            cl = length * rng.uniform(*spec["ratio"]) * (1.3 - u * 0.5)
            cr = r * rng.uniform(*spec["kid_r"])
            tips += branch(mesh, rng, p + out * r * 0.6, cd, cl, cr, cr * 0.3, depth + 1, spec, seed * 7 + i + depth * 131)
        for u in (0.6, 0.85):
            k = int(u * (len(frames) - 1))
            leaves(mesh, rng, frames[k][0], frames[k][1], spec["leaves"] // 3, spec["leaf"], 0.45, spread=1.8)
    else:
        leaves(mesh, rng, frames[-1][0], frames[-1][1], spec["leaves"], spec["leaf"], 0.45, spread=1.4)
        for u in (0.35, 0.5, 0.65, 0.8):
            k = int(u * (len(frames) - 1))
            leaves(mesh, rng, frames[k][0], frames[k][1], spec["leaves"] // 2, spec["leaf"], 0.45, spread=1.7)
    return tips


DEFAULT_SPEC = dict(kids=(4, 2), where=(0.5, 0.92), up=(0.3, 0.7), ratio=(0.3, 0.5), kid_r=(0.35, 0.5),
                    bend=(0.1, 0.3), wiggle=0.08, taper=1.1, sides=12, lumps=0.05, knots=0.0, leaves=28, leaf=0.32)


def surface_roots(mesh, rng, base_r, count, length, seed, lift=0.55):
    """Roots that leave the base above ground and snake away along it - the
    tangle at the foot of a giant."""
    for i in range(count):
        ang = i / count * TAU + rng.uniform(-0.3, 0.3)
        out = Vector((math.cos(ang), math.sin(ang), 0))
        side = Vector((-out.y, out.x, 0))
        L = length * rng.uniform(0.6, 1.3)
        steps = max(6, int(L * 2))
        pts = []
        for k in range(steps + 1):
            t = k / steps
            p = out * (base_r * 0.7 + t * L) + side * fbm(Vector((t * 2.2 + seed, i, 0.5))) * L * 0.25
            p.z = max(0.0, lift * (1 - t) ** 1.5 * base_r) + abs(fbm(Vector((t * 4, i * 3.1, seed)))) * 0.25 * (1 - t) + 0.05
            pts.append(p)
        sweep(mesh, pts, lambda u: lerp(base_r * 0.36, 0.04, u ** 0.7), 8, "Bark", seed + i, lumps=0.14)
        for j in range(rng.randint(0, 2)):
            k = int(rng.uniform(0.15, 0.5) * steps)
            sd = side * rng.choice((-1, 1))
            spts = bent_path(pts[k], (out * 0.5 + sd).normalized(), L * 0.4, 0.05, Vector((0, 0, -0.5)), 0.15, seed + j, 5)
            for q in spts:
                q.z = max(q.z, 0.04)
            sweep(mesh, spts, lambda u: lerp(base_r * 0.1, 0.02, u), 5, "Bark", seed + j)


def helix_vines(mesh, rng, frames, count, seed):
    """Vines wound about a trunk."""
    for i in range(count):
        a0 = rng.uniform(0, TAU)
        turns = rng.uniform(1.0, 2.5)
        u0, u1 = rng.uniform(0.0, 0.2), rng.uniform(0.6, 1.0)
        pts = []
        for p, t, nrm, bn, r, u in frames:
            if u < u0 or u > u1:
                continue
            ang = a0 + (u - u0) / (u1 - u0) * turns * TAU
            pts.append(p + (nrm * math.cos(ang) + bn * math.sin(ang)) * (r + 0.03))
        if len(pts) > 2:
            sweep(mesh, pts, lambda u: 0.035, 5, "Vine", seed + i, lumps=0.1)


def strands(mesh, rng, top, count, length, spread, seed, leaf_every=0, mat="Vine", r=0.012):
    """Thin things hanging from a point: aerial roots, a curtain of vine."""
    for i in range(count):
        L = length * rng.uniform(0.5, 1.3)
        start = top + Vector((rng.gauss(0, spread), rng.gauss(0, spread), 0))
        steps = max(4, int(L * 2))
        pts = []
        for k in range(steps + 1):
            t = k / steps
            sway = Vector((fbm(Vector((t * 2 + i, seed, 0))), fbm(Vector((seed, t * 2 + i, 3))), 0)) * L * 0.15 * t
            pts.append(start + sway - Z * (t * L))
        sweep(mesh, pts, lambda u: r * (1.2 - u * 0.6), 4, mat, seed + i, lumps=0)
        if leaf_every:
            for k in range(1, steps, leaf_every):
                leaves(mesh, rng, pts[k], around(-Z, rng, 1.5), 2, 0.12, 0.5, spread=1.0)


def rosette(mesh, rng, base, up_dir, count, length, width=0.1, mat="Leaf"):
    """Strap leaves radiating from a point: a bromeliad on a trunk, a lily on
    the ground. `up_dir` is the way it grows out of what it sits on."""
    a = perp(up_dir)
    b = up_dir.cross(a)
    for i in range(count):
        ang = i / count * TAU + rng.uniform(-0.3, 0.3)
        d = ((a * math.cos(ang) + b * math.sin(ang)) + up_dir * rng.uniform(0.6, 1.4)).normalized()
        flat = Vector((d.x, d.y, 0))
        flat = flat.normalized() if flat.length > 0.05 else a
        L = length * rng.uniform(0.7, 1.2)
        strip(mesh, rng, base, flat, max(d.z, 0.1) * 1.6, L, width * L / length, STRAP, rng.uniform(0.8, 1.4),
              segs=6, cross=3, crease=0.35, mat=mat)


def tree(seed, height, r0, r1, spec=None, wind=0.0, lean=0.0, flutes=0, flare=0.0, flute_height=0.25,
         grooves=0.0, knots=0.0, roots=0, root_len=3.0, vines=0, hang=0, epiphytes=0, fork=0, sides=None,
         taper=1.0, lumps=0.06, first_limb=0.5, steps=None, start_z=0.0, moss=0, climber=0, mesh=None):
    """A tree of some habit. The trunk winds by `wind` and leans by `lean`;
    limbs follow `spec` (see DEFAULT_SPEC); the base can have buttress flutes,
    surface roots, vines wound about it, strands hanging from the limbs, and
    epiphyte rosettes sitting on its upper side. `fork` splits the trunk into
    that many stems partway up instead of one crown."""
    rng = random.Random(seed)
    mesh = mesh or Mesh()
    spec = dict(DEFAULT_SPEC, **(spec or {}))
    spec = dict(spec, where=(first_limb, spec["where"][1]))
    sides = sides or (20 if flutes else 12)
    steps = steps or max(12, int(height * 2))
    path = winding_path(rng, Vector((0, 0, start_z)), height, wind, lean, steps)
    kids = spec["kids"]
    if fork:
        # The trunk stops at the fork; the stems carry on from there.
        u = rng.uniform(0.2, 0.4)
        cut = int(u * (len(path) - 1))
        frames = sweep(mesh, path[:cut + 1], lambda v: lerp(r0, r1, v * u), sides, "Bark", seed, lumps=lumps,
                       grooves=grooves, knots=knots, flutes=flutes, flare=flare, flute_height=flute_height / u)
        stems = rng.randint(max(2, fork - 1), fork + 1)
        p, t, nrm, bn, r, _ = frames[-1]
        for i in range(stems):
            ang = i / stems * TAU + rng.uniform(-0.4, 0.4)
            out = nrm * math.cos(ang) + bn * math.sin(ang)
            d = (t + out * rng.uniform(0.3, 0.6)).normalized()
            branch(mesh, rng, p + out * r * 0.3 - t * r * 0.3, d, height * (1 - u) * rng.uniform(0.7, 1.0), r * 0.65, r1 * 0.5, 0,
                   dict(spec, kids=kids[1:] or (2,)), seed + i * 17)
    else:
        frames = sweep(mesh, path, lambda u: lerp(r0, r1, u ** taper), sides, "Bark", seed, lumps=lumps,
                       grooves=grooves, knots=knots, flutes=flutes, flare=flare, flute_height=flute_height)
        n = rng.randint(max(1, kids[0] - 1), kids[0] + 1)
        for i in range(n):
            u = rng.uniform(*spec["where"])
            k = min(int(u * (len(frames) - 1)), len(frames) - 2)
            p, t, nrm, bn, r, _ = frames[k]
            ang = i / n * TAU + rng.uniform(-0.6, 0.6)
            out = (nrm * math.cos(ang) + bn * math.sin(ang)).normalized()
            up = rng.uniform(*spec["up"])
            d = (out * (1 - up) + Z * up).normalized()
            L = height * rng.uniform(*spec["ratio"]) * (1.3 - u * 0.5)
            rr = r * rng.uniform(*spec["kid_r"])
            branch(mesh, rng, p + out * r * 0.6, d, L, rr, rr * 0.3, 1, spec, seed * 7 + i)
        # The top of the trunk goes on as two or three stems rather than
        # stopping in a stub.
        p, t, nrm, bn, r, _ = frames[-1]
        for i in range(rng.randint(2, 3)):
            ang = i / 3 * TAU + rng.uniform(-0.5, 0.5)
            out = nrm * math.cos(ang) + bn * math.sin(ang)
            d = (t + out * rng.uniform(0.4, 0.9)).normalized()
            branch(mesh, rng, p - t * r * 0.5, d, height * rng.uniform(0.2, 0.35), r * 0.7, r * 0.15, 1, spec, seed * 13 + i)
    mesh.trunk = frames
    if roots:
        surface_roots(mesh, rng, r0, roots, root_len, seed)
    if vines:
        helix_vines(mesh, rng, frames, vines, seed)
    if climber:
        climbers(mesh, rng, frames, climber, seed)
    if moss:
        moss_on(mesh, rng, frames, moss, seed)
        for limb in mesh.limbs[:4]:
            moss_on(mesh, rng, limb, max(1, moss // 3), seed + 1)
    for i in range(hang):
        u = rng.uniform(0.45, 0.9)
        p, t, nrm, bn, r, _ = frames[int(u * (len(frames) - 1))]
        strands(mesh, rng, p + around(Z, rng, 1.2) * r, rng.randint(3, 7), height * 0.35, r * 0.6, seed + i, leaf_every=3)
    placed = 0
    for _ in range(epiphytes * 8):
        if placed >= epiphytes:
            break
        p, t, nrm, bn, r, u = frames[rng.randint(2, len(frames) - 2)]
        ang = rng.uniform(0, TAU)
        n = (nrm * math.cos(ang) + bn * math.sin(ang)).normalized()
        if n.z < 0.35 or u < 0.15:
            continue
        rosette(mesh, rng, p + n * r * 0.95, n, rng.randint(7, 11), rng.uniform(0.35, 0.6))
        placed += 1
    return mesh


def palm(seed, height, r, fronds=12, frond_len=3.0, wind=0.08, lean=0.15, fan_leaf=False, dead=3):
    """A palm: a slender ringed trunk that leans, a crown of fronds - pinnate
    or fan - and a few dead ones hanging under it."""
    rng = random.Random(seed)
    mesh = Mesh()
    path = winding_path(rng, Vector((0, 0, 0)), height, wind, lean, max(10, int(height * 2)), knots_n=4)
    frames = sweep(mesh, path, lambda u: lerp(r, r * 0.8, u), 10, "Bark", seed, lumps=0.03, scars=0.12)
    top = frames[-1][0]
    for i in range(fronds):
        ang = i / fronds * TAU + rng.uniform(-0.3, 0.3)
        d = Vector((math.cos(ang), math.sin(ang), 0))
        L = frond_len * rng.uniform(0.8, 1.15)
        if fan_leaf:
            stalk = bent_path(top, (d + Z * rng.uniform(0.4, 1.2)).normalized(), L * 0.5, 0.1, Z, 0.0, seed + i, 4)
            sweep(mesh, stalk, lambda u: 0.03, 5, "Leaf", seed + i, lumps=0, cap=False)
            fan(mesh, rng, stalk[-1], (stalk[-1] - stalk[-2]).normalized(), L * 0.55, blades=13)
        else:
            strip(mesh, rng, top, d, rng.uniform(0.5, 1.3), L, L * 0.15, pinnate(30, 0.65), rng.uniform(0.9, 1.5),
                  segs=40, cross=3, crease=0.35)
    for i in range(dead):
        ang = rng.uniform(0, TAU)
        d = Vector((math.cos(ang), math.sin(ang), 0))
        strip(mesh, rng, top - Z * 0.2, d, 0.0, frond_len * 0.7, frond_len * 0.1, pinnate(16, 0.5), 2.2, segs=16, cross=3, crease=0.4)
    return mesh


def tree_fern(seed, height, fronds=12, frond_len=1.8):
    """A fibrous stem with a fern crown on top."""
    rng = random.Random(seed)
    mesh = Mesh()
    path = winding_path(rng, Vector((0, 0, 0)), height, 0.06, 0.05, 10, knots_n=3)
    frames = sweep(mesh, path, lambda u: lerp(0.16, 0.13, u), 9, "Bark", seed, lumps=0.15)
    top = frames[-1][0]
    for i in range(fronds):
        ang = i / fronds * TAU + rng.uniform(-0.3, 0.3)
        d = Vector((math.cos(ang), math.sin(ang), 0))
        L = frond_len * rng.uniform(0.8, 1.2)
        strip(mesh, rng, top, d, rng.uniform(0.7, 1.4), L, L * 0.14, pinnate(14), rng.uniform(0.8, 1.3), segs=26, cross=3, crease=0.3)
    return mesh


def bamboo(seed, height, radius, lean=0.03):
    rng = random.Random(seed)
    mesh = Mesh()
    yaw = rng.uniform(0, TAU)
    culm(mesh, rng, Vector((0, 0, 0)), height, radius, Vector((math.cos(yaw), math.sin(yaw), 0)), lean, seed)
    return mesh


def bamboo_clump(seed, count, height, radius):
    """Several culms from one root, leaning away from each other."""
    rng = random.Random(seed)
    mesh = Mesh()
    for i in range(count):
        ang = i / count * TAU + rng.uniform(-0.4, 0.4)
        out = Vector((math.cos(ang), math.sin(ang), 0))
        base = out * rng.uniform(0.1, 0.45)
        culm(mesh, rng, base, height * rng.uniform(0.6, 1.1), radius * rng.uniform(0.7, 1.1), out, rng.uniform(0.04, 0.14), seed + i)
    return mesh


def culm(mesh, rng, base, height, radius, lean_dir, lean, seed):
    """A bamboo culm with a collar at every node, and twigs with leaf tufts
    along the upper half."""
    z = 0.0
    nodes = []
    while z < height:
        nodes.append(z)
        z += rng.uniform(0.5, 0.8)
    zs = [0.0]
    for nz in nodes[1:]:
        zs += [nz - 0.06, nz - 0.02, nz, nz + 0.02, nz + 0.06, (nz + zs[-1]) * 0.5]
    zs = sorted(set(round(v, 4) for v in zs if v < height)) + [height]

    def at(z):
        t = z / height
        return base + Vector((0, 0, z)) + lean_dir * (lean * z + 0.25 * t * t * height * lean * 6)

    rings = []
    sides = 10
    for z in zs:
        r = radius * lerp(1.0, 0.7, z / height)
        for nz in nodes:
            r *= 1.0 + 0.14 * math.exp(-((z - nz) / 0.035) ** 2)
        rings.append([mesh.vert(at(z) + Vector((math.cos(k / sides * TAU) * r, math.sin(k / sides * TAU) * r, 0))) for k in range(sides)])
    mesh.tube(rings, "Bamboo")
    for nz in [n for n in nodes if n > height * 0.45]:
        for _ in range(rng.randint(2, 4)):
            ang = rng.uniform(0, TAU)
            d = Vector((math.cos(ang), math.sin(ang), rng.uniform(0.1, 0.6))).normalized()
            twig = bent_path(at(nz), d, rng.uniform(0.5, 1.1), 0.35, -Z, 0.0, seed + int(nz * 10), 4)
            sweep(mesh, twig, lambda u: lerp(radius * 0.18, radius * 0.08, u), 4, "Bamboo", seed, lumps=0)
            tdir = (twig[-1] - twig[-2]).normalized()
            for anchor in (twig[-1], twig[-2]):
                for _ in range(rng.randint(4, 7)):
                    dd = (tdir + Vector((rng.gauss(0, 0.6), rng.gauss(0, 0.6), rng.gauss(-0.2, 0.3)))).normalized()
                    strip(mesh, rng, anchor, dd, rng.uniform(0.0, 0.25), rng.uniform(0.28, 0.42), 0.035,
                          lambda s: math.sin(math.pi * s ** 0.8) ** 0.7, rng.uniform(0.4, 0.8), segs=5, cross=2, crease=0)


# ---------------------------------------------------------------------------
# Undergrowth
# ---------------------------------------------------------------------------

def fern(seed, fronds, length, up=(0.9, 1.7)):
    """Fronds fanned from one point, each a serrated strip that arches over."""
    rng = random.Random(seed)
    mesh = Mesh()
    for i in range(fronds):
        ang = i / fronds * TAU + rng.uniform(-0.25, 0.25)
        d = Vector((math.cos(ang), math.sin(ang), 0))
        L = length * rng.uniform(0.7, 1.15)
        rise = rng.uniform(*up)
        strip(mesh, rng, Vector((0, 0, 0.02)), d, rise, L, L * 0.1, pinnate(rng.randint(15, 22), 0.6),
              rise * 0.75 + rng.uniform(0.1, 0.3), segs=44, cross=3, crease=0.35, twist=rng.uniform(-0.3, 0.3))
    return mesh


def broadleaf(seed, count, length, profile=OVAL, width=0.28, cup=0.22, stalk_up=(0.6, 1.4)):
    """Big leaves on stalks: the wide glossy ones, or with HEART and a wider
    blade, elephant ears."""
    rng = random.Random(seed)
    mesh = Mesh()
    for i in range(count):
        ang = i / count * TAU + rng.uniform(-0.4, 0.4)
        d = Vector((math.cos(ang), math.sin(ang), 0))
        L = length * rng.uniform(0.75, 1.15)
        up = rng.uniform(*stalk_up)
        stalk = L * rng.uniform(0.3, 0.5)
        pts = bent_path(Vector((0, 0, 0)), (d + Z * up).normalized(), stalk, 0.05, -Z, 0.0, seed + i, 4)
        sweep(mesh, pts, lambda u: lerp(0.014, 0.008, u), 5, "Leaf", seed + i, lumps=0, cap=False)
        tdir = (pts[-1] - pts[-2]).normalized()
        blade = L - stalk
        strip(mesh, rng, pts[-1], Vector((tdir.x, tdir.y, 0)), max(tdir.z, 0.05) * 0.9, blade, blade * width,
              profile, rng.uniform(0.5, 0.9), segs=10, cross=5, crease=0.12, cup=cup)
    return mesh


def grass(seed, blades, length):
    rng = random.Random(seed)
    mesh = Mesh()
    for i in range(blades):
        ang = rng.uniform(0, TAU)
        d = Vector((math.cos(ang), math.sin(ang), 0))
        L = length * rng.uniform(0.6, 1.3)
        base = Vector((rng.gauss(0, 0.08), rng.gauss(0, 0.08), 0))
        strip(mesh, rng, base, d, rng.uniform(1.4, 2.6), L, L * 0.035, BLADE, rng.uniform(1.0, 2.0), segs=4, cross=2, crease=0)
    return mesh


def sapling(seed, height, leaf_count=9):
    rng = random.Random(seed)
    mesh = Mesh()
    path = winding_path(rng, Vector((0, 0, 0)), height, 0.08, 0.1, 8, knots_n=3)
    frames = sweep(mesh, path, lambda u: lerp(0.02, 0.008, u), 5, "Bark", seed, lumps=0, cap=False)
    for i in range(leaf_count):
        p, t, nrm, bn, r, u = frames[rng.randint(2, len(frames) - 1)]
        ang = rng.uniform(0, TAU)
        d = (nrm * math.cos(ang) + bn * math.sin(ang) + Z * 0.2).normalized()
        L = rng.uniform(0.2, 0.32)
        strip(mesh, rng, p, d, 0.3, L, L * 0.4, OVAL, 0.6, segs=5, cross=3, crease=0.15)
    leaves(mesh, rng, frames[-1][0], Z, 5, 0.25, 0.4, spread=1.2)
    return mesh


def bush(seed, radius, clusters):
    """Leaf clusters on short twigs from one root - a green mass."""
    rng = random.Random(seed)
    mesh = Mesh()
    for i in range(clusters):
        d = around(Z, rng, 1.3)
        L = radius * rng.uniform(0.5, 1.0)
        pts = bent_path(Vector((0, 0, 0)), d, L, 0.15, Z, 0.05, seed + i, 4)
        sweep(mesh, pts, lambda u: lerp(0.02, 0.008, u), 5, "Bark", seed + i, lumps=0, cap=False)
        leaves(mesh, rng, pts[-1], d, 10, radius * 0.28, 0.5, spread=1.4)
        leaves(mesh, rng, pts[2], d, 5, radius * 0.25, 0.5, spread=1.6)
    return mesh


def lily(seed, count, length):
    rng = random.Random(seed)
    mesh = Mesh()
    rosette(mesh, rng, Vector((0, 0, 0)), Z, count, length, width=0.12)
    return mesh


# ---------------------------------------------------------------------------
# Vines
# ---------------------------------------------------------------------------

def vine_hang(seed, height, count, spread=0.6):
    """A curtain of thin vines from one point up high - origin at the top,
    to hang from a limb."""
    rng = random.Random(seed)
    mesh = Mesh()
    strands(mesh, rng, Vector((0, 0, 0)), count, height, spread, seed, leaf_every=2, r=0.015)
    return mesh


def aerial_roots(seed, count, length):
    rng = random.Random(seed)
    mesh = Mesh()
    strands(mesh, rng, Vector((0, 0, 0)), count, length, 0.25, seed, mat="Bark", r=0.02)
    return mesh


def liana(seed, height, span, loops=1, r=0.07):
    """A woody liana: from the ground up into a loop or two and away - the
    thick curling ropes between the palms of the fourth reference."""
    rng = random.Random(seed)
    mesh = Mesh()
    pts = [Vector((0, 0, 0))]
    n = 6 + loops * 4
    for i in range(1, n + 1):
        t = i / n
        z = height * math.sin(math.pi * t) + fbm(Vector((t * 3, seed, 0))) * height * 0.2
        ang = t * loops * TAU + fbm(Vector((seed, t * 2, 0))) * 1.5
        pts.append(Vector((t * span + math.cos(ang) * span * 0.18, math.sin(ang) * span * 0.25, max(z, 0.05))))
    path = catmull(pts, n * 4)
    sweep(mesh, path, lambda u: r * (1.1 - u * 0.4), 7, "Vine", seed, lumps=0.15, knots=0.2, cap=False)
    # A thinner one twisted about it.
    twist = []
    nrm = perp((path[1] - path[0]).normalized())
    for i, q in enumerate(path):
        t = (path[min(i + 1, len(path) - 1)] - path[max(i - 1, 0)]).normalized()
        nrm = (nrm - t * nrm.dot(t)).normalized()
        a = i / len(path) * TAU * 3
        twist.append(q + (nrm * math.cos(a) + t.cross(nrm) * math.sin(a)) * r * 1.3)
    sweep(mesh, twist, lambda u: r * 0.35, 5, "Vine", seed + 1, lumps=0.1, cap=False)
    return mesh


def vine_arch(seed, span, height, r=0.05):
    """A vine strung between two trunks `span` apart, sagging in the middle
    and dropping strands. Ends at (0,0,height) and (span,0,height)."""
    rng = random.Random(seed)
    mesh = Mesh()
    pts = []
    for i in range(7):
        t = i / 6
        pts.append(Vector((t * span, fbm(Vector((t * 2, seed, 1))) * span * 0.12, height - math.sin(math.pi * t) * height * 0.35)))
    path = catmull(pts, 30)
    sweep(mesh, path, lambda u: r, 6, "Vine", seed, lumps=0.12, cap=False)
    for i in range(rng.randint(3, 6)):
        k = rng.randint(4, 26)
        strands(mesh, rng, path[k], rng.randint(1, 3), height * 0.5, 0.05, seed + i, leaf_every=2)
    for k in range(2, 30, 3):
        leaves(mesh, rng, path[k], around(Z, rng, 1.2), 3, 0.15, 0.5, spread=1.2)
    return mesh


# ---------------------------------------------------------------------------
# Rocks, logs and the ground
# ---------------------------------------------------------------------------

def rock_geom(mesh, rng, center, size, seed, stretch=(1.0, 1.0, 0.65), flat_top=0.0, subdiv=3, rough=0.35,
              warp=0.3, yaw=0.0, moss=0, mat="Rock"):
    """An icosphere pushed about by noise, squashed, cut flat underneath, and
    with `flat_top` the top sliced off too - a slab, a stepping stone. `warp`
    is a slow noise that pulls the whole shape out of round; `rough` the fast
    one that breaks the surface. `moss` cushions sit on its upper faces."""
    bm = bmesh.new()
    # A mossy rock is cut finer, so the edge of the moss can follow the
    # noise rather than the triangles.
    bmesh.ops.create_icosphere(bm, subdivisions=min(subdiv + 1, 4) if moss else subdiv, radius=1.0)
    for v in bm.verts:
        p = v.co * 1.4 + Vector((seed * 3.1, seed * 1.7, 0))
        v.co += v.normal * (fbm(p * 0.5, octaves=2) * warp + fbm(p, octaves=4) * rough + fbm(p * 3.5, octaves=2) * 0.06)
    hz = size * 0.5 * stretch[2]
    rot = Matrix.Rotation(yaw, 3, Z)
    tops = []
    for v in bm.verts:
        v.co = Vector((v.co.x * stretch[0], v.co.y * stretch[1], v.co.z * stretch[2])) * size * 0.5
        v.co.z = max(v.co.z, -hz * 0.55)
        if flat_top:
            v.co.z = min(v.co.z, hz * (1 - flat_top) + fbm(v.co * 2) * hz * 0.08)
        v.co.z += hz * 0.45
        v.co = rot @ v.co + center
    bm.verts.ensure_lookup_table()
    bm.normal_update()
    base = len(mesh.verts)
    for v in bm.verts:
        mesh.vert(v.co)
    for f in bm.faces:
        mesh.face([base + v.index for v in f.verts], mat)
    if moss:
        # Where moss grows: faces that look up, thinned by noise so it lies
        # in patches. Each vertex gets a weight, the shell is those faces
        # pushed out by it, and where the weight reaches zero the shell
        # touches the rock - no edge floating free.
        cover = min(1.0, moss / 20.0)
        lo, hi = 1.0 - 0.55 * cover, 1.3 - 0.55 * cover
        weight = {}
        for v in bm.verts:
            w = smoothstep(lo, hi, v.normal.z + 0.7 * fbm((v.co - center) * (4.5 / size) + Vector((seed, 0, 0)), 3))
            weight[v.index] = w
        shell = {}
        for f in bm.faces:
            if max(weight[v.index] for v in f.verts) < 0.04:
                continue
            for v in f.verts:
                if v.index not in shell:
                    w = weight[v.index]
                    lump = 1.0 + 0.5 * fbm((v.co - center) * (6.0 / size) + Vector((0, seed, 0)), 2)
                    shell[v.index] = mesh.vert(v.co + v.normal * (size * 0.035 * w * lump))
            mesh.face([shell[v.index] for v in f.verts], "Moss")
    bm.free()


def rock(seed, size, stretch=(1.0, 1.0, 0.65), flat_top=0.0, subdiv=3, rough=0.35, warp=0.3, moss=0):
    rng = random.Random(seed)
    mesh = Mesh()
    mesh.smooth = flat_top == 0
    rock_geom(mesh, rng, Vector((0, 0, 0)), size, seed, stretch, flat_top, subdiv, rough, warp, moss=moss)
    return mesh


def log(seed, length, r, stubs=3):
    """A fallen trunk lying along X, a little bowed, with broken limb stubs."""
    rng = random.Random(seed)
    mesh = Mesh()
    pts = bent_path(Vector((-length / 2, 0, r * 0.8)), Vector((1, 0, 0)), length, 0.03, Z, 0.02, seed, max(8, int(length * 2)))
    frames = sweep(mesh, pts, lambda u: r * (1.15 - u * 0.3), 12, "Bark", seed, lumps=0.1, grooves=0.05, knots=0.15)
    mesh.limbs.append(frames)
    for i in range(stubs):
        p, t, nrm, bn, rr, u = frames[rng.randint(2, len(frames) - 3)]
        ang = rng.uniform(-2.2, 2.2)
        d = (nrm * math.cos(ang) + bn * math.sin(ang)).normalized()
        if d.z < -0.2:
            d.z = 0.3
        stub = bent_path(p + d * rr * 0.8, d, rr * rng.uniform(1.5, 4), 0.1, Z, 0.1, seed + i, 4)
        sweep(mesh, stub, lambda u, rr=rr: rr * lerp(0.35, 0.2, u), 6, "Bark", seed + i, lumps=0.1)
    return mesh


def ground(seed, size, step=0.75):
    """A square of ground that rolls gently, a stream bed wandering along its
    length and a path worn beside it."""
    mesh = Mesh()
    n = int(size / step)
    grid = []
    for iy in range(n + 1):
        row = []
        for ix in range(n + 1):
            x = -size / 2 + ix * step
            y = -size / 2 + iy * step
            h = fbm(Vector((x * 0.06, y * 0.06, seed))) * 1.4 + fbm(Vector((x * 0.25, y * 0.25, seed + 5))) * 0.25
            cx = math.sin(y * 0.09) * 4.0 + fbm(Vector((y * 0.05, seed + 9, 0))) * 3.0
            bed = 1.0 - smoothstep(0.4, 1.6, abs(x - cx))
            h -= bed * 0.8
            px = cx + 8.0 + fbm(Vector((y * 0.07, seed + 13, 0))) * 2.0
            path = 1.0 - smoothstep(0.5, 1.5, abs(x - px))
            h = lerp(h, h * 0.4 - 0.1, path)
            row.append(mesh.vert((x, y, h)))
        grid.append(row)
    for a, b in zip(grid, grid[1:]):
        mesh.quad_strip(a, b, "Ground", closed=False)
    return mesh


# ---------------------------------------------------------------------------
# Moss, fungus and the things that grow on other things
# ---------------------------------------------------------------------------

def blob(mesh, center, radius, seed, flat=0.5, up=Z, mat="Moss", rings=5, segs=10, rough=0.3):
    """A noisy dome sitting on a surface whose normal is `up`: a moss cushion,
    a clod of earth."""
    a = perp(up)
    b = up.cross(a)
    rows = []
    for i in range(rings + 1):
        phi = i / rings * (math.pi / 2)
        row = []
        for k in range(segs):
            th = k / segs * TAU
            r = radius * (1 + rough * fbm(Vector((math.cos(th) * 2 + seed * 0.1, math.sin(th) * 2, phi * 3))))
            p = center + (a * math.cos(th) + b * math.sin(th)) * (r * math.sin(phi)) + up * (r * flat * math.cos(phi)) - up * radius * 0.08
            row.append(mesh.vert(p))
        rows.append(row)
    for r0, r1 in zip(rows, rows[1:]):
        mesh.quad_strip(r0, r1, mat)


def densify(frames, step):
    """The same frames with extra ones interpolated between, so a skin laid
    over them can have a finer edge than the tube underneath."""
    out = []
    for a, b in zip(frames, frames[1:]):
        n = max(1, int((b[0] - a[0]).length / step))
        for i in range(n):
            f = i / n
            p = a[0].lerp(b[0], f)
            nrm = a[2].lerp(b[2], f).normalized()
            t = a[1].lerp(b[1], f).normalized()
            nrm = (nrm - t * nrm.dot(t)).normalized()
            out.append((p, t, nrm, t.cross(nrm).normalized(), lerp(a[4], b[4], f), lerp(a[5], b[5], f)))
    out.append(frames[-1])
    return out


def moss_sleeve(mesh, frames, u0, u1, angle, width, thick, seed, segs=11, mat="Moss"):
    """Moss lying on a swept tube: a sector of a second skin over the same
    frames, so it follows every bend. Its thickness falls to nothing at the
    sides and at both ends, so the edge meets the bark, and noise tears that
    edge and lumps the surface. `angle` is which side, measured from the
    frame's normal; when the tube is not vertical the sector is centred on
    whichever side faces up."""
    rows = []
    span = max(u1 - u0, 1e-3)
    for p, t, nrm, bn, r, u in densify(frames, 0.15):
        if u < u0 or u > u1:
            continue
        up = Z - t * Z.dot(t)
        a0 = math.atan2(up.dot(bn), up.dot(nrm)) if up.length > 0.35 else angle
        row = []
        for k in range(segs):
            f = k / (segs - 1)
            # The end of the patch comes at a different place on every
            # strand across it, and its sides wander: a torn edge, not a cut.
            tear = fbm(Vector((f * 4 + seed, u * 3, 0.5)), 2) * 0.25
            along = smoothstep(0, 0.35, (u - u0) / span + tear) * smoothstep(0, 0.35, (u1 - u) / span - tear)
            wander = fbm(Vector((u * 6 + seed, k * 0.7, 1.5)), 2) * 0.35
            ang = a0 - width / 2 + width * f + wander * width * (0.5 + 0.5 * abs(2 * f - 1))
            across = max(0.0, math.sin(math.pi * f)) ** 0.5
            n = nrm * math.cos(ang) + bn * math.sin(ang)
            lump = 0.5 + 0.5 * abs(fbm(Vector((u * 14 + seed, f * 6, 2.0)), 3))
            h = thick * max(0.0, along) * across * lump
            row.append(mesh.vert(p + n * (r * 1.003 + h)))
        rows.append(row)
    for a, b in zip(rows, rows[1:]):
        mesh.quad_strip(a, b, mat, closed=False)


def moss_on(mesh, rng, frames, count, seed, size=None):
    """`count` patches of moss along a tube: mostly on the side that faces
    up, a few round the shady side of a vertical trunk."""
    if len(frames) < 4:
        return
    for i in range(count):
        length = rng.uniform(0.1, 0.35)
        u0 = rng.uniform(0.0, 1.0 - length)
        r = frames[min(int((u0 + length / 2) * (len(frames) - 1)), len(frames) - 1)][4]
        moss_sleeve(mesh, frames, u0, u0 + length, rng.uniform(0, TAU), rng.uniform(1.4, 3.2),
                    (size or r) * rng.uniform(0.12, 0.28) + 0.02, seed + i * 3)


def climbers(mesh, rng, frames, count, seed):
    """A climbing plant up the trunk: a vine wound round it with big lobed
    leaves standing out from it every so often."""
    for i in range(count):
        a0 = rng.uniform(0, TAU)
        turns = rng.uniform(0.6, 1.5)
        u0, u1 = rng.uniform(0.0, 0.1), rng.uniform(0.5, 0.9)
        pts, normals = [], []
        for p, t, nrm, bn, r, u in frames:
            if u < u0 or u > u1:
                continue
            ang = a0 + (u - u0) / (u1 - u0) * turns * TAU
            n = nrm * math.cos(ang) + bn * math.sin(ang)
            pts.append(p + n * (r + 0.04))
            normals.append(n)
        if len(pts) < 3:
            continue
        sweep(mesh, pts, lambda u: 0.03, 5, "Vine", seed + i, lumps=0.1)
        for k in range(1, len(pts) - 1, 2):
            d = (normals[k] + Z * 0.3 + around(normals[k], rng, 0.6) * 0.5).normalized()
            L = rng.uniform(0.35, 0.55)
            strip(mesh, rng, pts[k], Vector((d.x, d.y, 0)).normalized(), 0.5, L, L * 0.45, HEART, 0.9, segs=6, cross=5, crease=0.1, cup=0.15)


def moss_cushion(seed, size, count=1):
    """Low, ragged mounds on the ground, their rims tucked under."""
    rng = random.Random(seed)
    mesh = Mesh()
    for i in range(count):
        c = Vector((rng.gauss(0, size * 0.5), rng.gauss(0, size * 0.5), 0)) if count > 1 else Vector((0, 0, 0))
        blob(mesh, c, size * rng.uniform(0.6, 1.2), seed + i, flat=rng.uniform(0.2, 0.35), rings=6, segs=16, rough=0.5)
    return mesh


def moss_carpet(seed, size):
    """A flat, ragged patch to lie on a rock or a log."""
    rng = random.Random(seed)
    mesh = Mesh()
    blob(mesh, Vector((0, 0, 0)), size, seed, flat=0.12, rings=6, segs=18)
    for i in range(3):
        blob(mesh, Vector((rng.gauss(0, size * 0.5), rng.gauss(0, size * 0.5), 0)), size * 0.5, seed + i, flat=0.15, rings=4, segs=10)
    return mesh


def moss_drape(seed, count, length, spread):
    """Beard moss hanging from a limb: origin at the top."""
    rng = random.Random(seed)
    mesh = Mesh()
    strands(mesh, rng, Vector((0, 0, 0)), count, length, spread, seed, mat="Moss", r=0.008)
    return mesh


def fungus_at(mesh, rng, base, out, count, radius, seed):
    """Shelf fungi stacked on a surface at `base` whose normal is `out`: a
    half-disc each, drooping at the rim, with an underside so it has an
    edge."""
    side = out.cross(Z).normalized() if abs(out.z) < 0.95 else Vector((1, 0, 0))
    for i in range(count):
        R = radius * rng.uniform(0.5, 1.2)
        b = base + Z * (i * radius * 0.5) + side * rng.gauss(0, radius * 0.3)
        rows = []
        for ring in range(4):
            rr = R * ring / 3
            row = []
            for k in range(9):
                a = -math.pi / 2 + math.pi * k / 8
                q = b + (Matrix.Rotation(a, 3, Z) @ out) * rr * (1 + 0.1 * fbm(Vector((k, ring, seed + i))))
                q.z += -rr * 0.25 * (ring / 3) ** 2
                row.append(mesh.vert(q))
            rows.append(row)
        under = [[mesh.vert(mesh.verts[v] - Z * 0.02) for v in row] for row in rows]
        for r0, r1 in zip(rows, rows[1:]):
            mesh.quad_strip(r0, r1, "Fungus", closed=False)
        for r0, r1 in zip(under, under[1:]):
            mesh.quad_strip(list(reversed(r0)), list(reversed(r1)), "Fungus", closed=False)
        mesh.quad_strip(rows[-1], under[-1], "Fungus", closed=False)


def brackets(seed, count, radius):
    """A stack of shelf fungi at the origin, growing out along +X from a
    vertical surface at x=0."""
    rng = random.Random(seed)
    mesh = Mesh()
    fungus_at(mesh, rng, Vector((0, 0, 0)), Vector((1, 0, 0)), count, radius, seed)
    return mesh


# ---------------------------------------------------------------------------
# Dead wood
# ---------------------------------------------------------------------------

def splinters(mesh, rng, frame, count, height, seed):
    """Jagged spikes up from the rim of a broken trunk."""
    p, t, nrm, bn, r, u = frame
    for i in range(count):
        ang = i / count * TAU + rng.uniform(-0.3, 0.3)
        n = nrm * math.cos(ang) + bn * math.sin(ang)
        base = p + n * r * rng.uniform(0.5, 0.9) - t * r * 0.3
        d = (t + n * rng.uniform(-0.1, 0.3)).normalized()
        L = height * rng.uniform(0.25, 1.0)
        pts = bent_path(base, d, L, rng.uniform(0.05, 0.3), n, 0.08, seed + i, 4)
        sweep(mesh, pts, lambda u, r=r: r * lerp(rng.uniform(0.25, 0.45), 0.02, u), 5, "Bark", seed + i, lumps=0.15)


def snag(seed, height, r0, r1, limbs=3, moss=3, fungi=2):
    """A dead tree: bare, broken off at the top, a few limb stubs, moss and
    shelf fungi on it."""
    rng = random.Random(seed)
    mesh = Mesh()
    path = winding_path(rng, Vector((0, 0, 0)), height, 0.08, rng.uniform(0.0, 0.15), max(10, int(height * 2)), knots_n=4)
    frames = sweep(mesh, path, lambda u: lerp(r0, r1, u), 14, "Bark", seed, lumps=0.15, grooves=0.12, knots=0.3, flutes=4, flare=0.6)
    splinters(mesh, rng, frames[-1], rng.randint(5, 9), r0 * 4.5, seed)
    for i in range(limbs):
        p, t, nrm, bn, r, u = frames[rng.randint(len(frames) // 2, len(frames) - 3)]
        ang = rng.uniform(0, TAU)
        d = (nrm * math.cos(ang) + bn * math.sin(ang) + Z * rng.uniform(-0.2, 0.6)).normalized()
        pts = bent_path(p + d * r * 0.5, d, r * rng.uniform(3, 9), 0.15, Z * rng.choice((-1, 1)), 0.1, seed + i, 5)
        sweep(mesh, pts, lambda u, r=r: r * lerp(0.4, 0.06, u), 6, "Bark", seed + i, lumps=0.1)
    moss_on(mesh, rng, frames, moss, seed)
    for i in range(fungi):
        p, t, nrm, bn, r, u = frames[rng.randint(2, len(frames) // 2)]
        ang = rng.uniform(0, TAU)
        n = nrm * math.cos(ang) + bn * math.sin(ang)
        fungus_at(mesh, rng, p + n * r * 0.95, n, rng.randint(2, 4), r * 0.4, seed + i)
    return mesh


def stump(seed, height, r, moss=4, fungi=1):
    rng = random.Random(seed)
    mesh = Mesh()
    path = [Vector((0, 0, height * i / 8)) for i in range(9)]
    frames = sweep(mesh, path, lambda u: lerp(r, r * 0.85, u), 16, "Bark", seed, lumps=0.12, grooves=0.1, knots=0.15, flutes=5, flare=0.9, flute_height=0.6)
    splinters(mesh, rng, frames[-1], rng.randint(3, 6), height * 0.8, seed)
    surface_roots(mesh, rng, r, rng.randint(3, 5), r * 4, seed, lift=0.2)
    moss_on(mesh, rng, frames, moss, seed)
    for i in range(fungi):
        ang = rng.uniform(0, TAU)
        n = Vector((math.cos(ang), math.sin(ang), 0))
        fungus_at(mesh, rng, n * r * 0.95 + Z * height * 0.4, n, 3, r * 0.5, seed + i)
    return mesh


def broken_tree(seed, height, r0, break_at=0.4, moss=4):
    """A trunk snapped part way up, the top hanging down from the break with
    its end on the ground - what a storm leaves."""
    rng = random.Random(seed)
    mesh = Mesh()
    hb = height * break_at
    path = winding_path(rng, Vector((0, 0, 0)), hb, 0.05, 0.05, 10, knots_n=3)
    frames = sweep(mesh, path, lambda u: lerp(r0, r0 * (1 - 0.6 * break_at), u), 12, "Bark", seed, lumps=0.08, grooves=0.05, flutes=4, flare=0.5, flute_height=0.4)
    splinters(mesh, rng, frames[-1], 6, r0 * 2.5, seed)
    top, t, nrm, bn, r, _ = frames[-1]
    ang = rng.uniform(0, TAU)
    out = Vector((math.cos(ang), math.sin(ang), 0))
    L = height * (1 - break_at)
    # The fallen part: hinged at the break, its far end resting on the ground.
    ground = top + out * L * 0.85 - Z * (hb - r * 0.8)
    pts = catmull([top + out * r * 0.5 - Z * r * 0.3, (top + ground) / 2 + Z * 0.5 + out.cross(Z) * fbm(Vector((seed, 1, 2))) * 1.5, ground], max(8, int(L * 2)))
    fr = sweep(mesh, pts, lambda u, r=r: lerp(r * 0.9, r * 0.25, u), 10, "Bark", seed + 1, lumps=0.08, grooves=0.05)
    mesh.limbs.append(fr)
    for i in range(4):
        p, t2, n2, b2, rr, u = fr[rng.randint(len(fr) // 3, len(fr) - 2)]
        a = rng.uniform(0, TAU)
        d = (n2 * math.cos(a) + b2 * math.sin(a) + t2 * 0.3).normalized()
        branch(mesh, rng, p + d * rr * 0.5, d, L * rng.uniform(0.2, 0.35), rr * 0.5, rr * 0.1, 2,
               dict(DEFAULT_SPEC, kids=(2, 1), leaves=14, leaf=0.3), seed + i)
    moss_on(mesh, rng, frames, moss, seed)
    return mesh


def uprooted(seed, length, r, plate=2.0, moss=5):
    """A tree on its side, torn out with the disc of roots and earth standing
    on end at the base. Lies along +X from the plate."""
    rng = random.Random(seed)
    mesh = Mesh()
    hub = Vector((plate * 0.3, 0, plate * 0.8))
    pts = catmull([hub, hub + Vector((length * 0.4, 0, -(plate * 0.8 - r * 0.9))), hub + Vector((length, fbm(Vector((seed, 2, 3))) * 1.5, -(plate * 0.8 - r * 0.8)))],
                  max(10, int(length * 2)))
    frames = sweep(mesh, pts, lambda u: lerp(r, r * 0.3, u ** 0.9), 12, "Bark", seed, lumps=0.1, grooves=0.05, knots=0.15)
    # The root plate: a ragged clod standing on end, roots all through it and
    # poking out of it every way, the longest of them still in the air.
    blob(mesh, hub - Vector((plate * 0.05, 0, 0)), plate * 0.9, seed, flat=0.3, up=Vector((-1, 0, 0)), mat="Ground", rings=6, segs=18, rough=0.6)
    blob(mesh, hub + Vector((plate * 0.05, 0, 0)), plate * 0.8, seed + 3, flat=0.2, up=Vector((1, 0, 0)), mat="Ground", rings=5, segs=16, rough=0.6)
    for i in range(rng.randint(14, 22)):
        a = rng.uniform(0, TAU)
        out = Vector((rng.uniform(-0.5, 0.2), math.cos(a), math.sin(a))).normalized()
        base = hub + out * plate * rng.uniform(0.3, 0.8)
        rp = bent_path(base, out, plate * rng.uniform(0.3, 1.0), rng.uniform(0.05, 0.25), around(out, rng, 1.5), 0.15, seed + i, 5)
        sweep(mesh, rp, lambda u, w=rng.uniform(0.2, 0.4): lerp(r * w, 0.02, u), 5, "Bark", seed + i, lumps=0.15)
    for i in range(5):
        p, t, nrm, bn, rr, u = frames[rng.randint(len(frames) // 3, len(frames) - 2)]
        a = rng.uniform(0, TAU)
        d = (nrm * math.cos(a) + bn * math.sin(a) + t * 0.3).normalized()
        if d.z < -0.3:
            d.z = 0.3
        branch(mesh, rng, p + d * rr * 0.5, d, length * rng.uniform(0.15, 0.3), rr * 0.5, rr * 0.1, 2,
               dict(DEFAULT_SPEC, kids=(2, 1), leaves=12, leaf=0.28), seed + i)
    moss_on(mesh, rng, frames, moss, seed)
    return mesh


def log_mossy(seed, length, r, stubs=3, moss=6, fungi=2):
    mesh = log(seed, length, r, stubs)
    rng = random.Random(seed + 99)
    frames = mesh.limbs[0] if mesh.limbs else []
    moss_on(mesh, rng, frames, moss, seed)
    for i in range(fungi):
        p, t, nrm, bn, rr, u = frames[rng.randint(2, len(frames) - 3)]
        a = rng.uniform(0.6, 2.5) * rng.choice((-1, 1))
        n = nrm * math.cos(a) + bn * math.sin(a)
        if n.z > 0.6:
            n = (n - Z * 0.5).normalized()
        fungus_at(mesh, rng, p + n * rr * 0.95, n, rng.randint(2, 4), rr * 0.5, seed + i)
    return mesh


def branch_debris(seed, length, r):
    """A fallen limb lying on the ground with its twigs."""
    rng = random.Random(seed)
    mesh = Mesh()
    pts = bent_path(Vector((-length / 2, 0, r)), Vector((1, 0, 0)), length, 0.05, Z * rng.choice((-1, 1)), 0.1, seed, 8)
    for q in pts:
        q.z = max(q.z, r * 0.6)
    frames = sweep(mesh, pts, lambda u: lerp(r, r * 0.3, u), 7, "Bark", seed, lumps=0.1)
    for i in range(rng.randint(3, 6)):
        p, t, nrm, bn, rr, u = frames[rng.randint(1, len(frames) - 2)]
        a = rng.uniform(0, TAU)
        d = (nrm * math.cos(a) + bn * math.sin(a) + t * 0.5).normalized()
        if d.z < 0:
            d.z *= -0.3
        tp = bent_path(p, d, length * rng.uniform(0.15, 0.35), 0.1, Z, 0.15, seed + i, 4)
        sweep(mesh, tp, lambda u, rr=rr: lerp(rr * 0.4, 0.01, u), 4, "Bark", seed + i, lumps=0)
    return mesh


# ---------------------------------------------------------------------------
# Unusual trees
# ---------------------------------------------------------------------------

def strangler(seed, height, r, roots=10, moss=4):
    """A strangler fig: a tall host trunk wrapped in a lattice of descending
    roots that merge and fuse, with the fig's own crown on top."""
    rng = random.Random(seed)
    mesh = tree(seed, height, r, r * 0.4, TALL, wind=0.04, lean=0.04, first_limb=0.75, moss=moss)
    frames = mesh.trunk
    n = len(frames)
    starts = []
    for j in range(roots):
        a0 = j / roots * TAU + rng.uniform(-0.3, 0.3)
        u0 = rng.uniform(0.55, 0.85)
        rate = rng.choice((-1, 1)) * rng.uniform(0.5, 1.4)
        pts = []
        for p, t, nrm, bn, rr, u in reversed(frames):
            if u > u0:
                continue
            ang = a0 + (u0 - u) * rate * TAU + fbm(Vector((u * 4, j, seed))) * 0.7
            flare = 1.0 + max(0.0, 0.2 - u) * 12
            off = rr * 1.05 + 0.12 * flare + abs(fbm(Vector((u * 3, j * 2, seed)))) * 0.25
            pts.append(p + (nrm * math.cos(ang) + bn * math.sin(ang)) * off)
        if len(pts) > 2:
            sweep(mesh, pts, lambda u: lerp(0.09, 0.3, u ** 1.5), 7, "Bark", seed + j, lumps=0.2, knots=0.2)
            starts.append((a0, u0, rate))
    # Cross-links between neighbouring roots, the lattice.
    for j in range(len(starts)):
        a0, u0, rate = starts[j]
        a1, u1, rate1 = starts[(j + 1) % len(starts)]
        for _ in range(rng.randint(3, 6)):
            u = rng.uniform(0.05, min(u0, u1) * 0.9)
            k = min(int(u * (n - 1)), n - 1)
            p, t, nrm, bn, rr, uu = frames[k]
            aa = a0 + (u0 - u) * rate * TAU
            ab = a1 + (u1 - u) * rate1 * TAU
            while ab < aa:
                ab += TAU
            if ab - aa > math.pi:
                continue
            arc = []
            for i in range(5):
                a = lerp(aa, ab, i / 4)
                arc.append(p + (nrm * math.cos(a) + bn * math.sin(a)) * (rr * 1.05 + 0.14) + t * fbm(Vector((i, j, u * 5))) * 0.3)
            sweep(mesh, arc, lambda v: 0.08 + 0.04 * math.sin(math.pi * v), 6, "Bark", seed + j + 50, lumps=0.2)
    return mesh


def banyan(seed, height, r0, r1, pillars=6, moss=4):
    """A spreading tree whose limbs drop prop roots to the ground - pillars
    that hold the crown up as it walks outward."""
    rng = random.Random(seed)
    mesh = tree(seed, height, r0, r1, dict(SPREADING, kids=(6, 3, 2), up=(0.0, 0.25), ratio=(0.5, 0.75), kid_r=(0.55, 0.7)),
                wind=0.08, lean=0.05, flutes=5, flare=0.8, roots=6, root_len=4, epiphytes=4, moss=moss, sides=24, first_limb=0.35)
    limbs = [f for f in mesh.limbs if len(f) > 4]
    for i in range(pillars):
        if not limbs:
            break
        fr = rng.choice(limbs)
        p, t, nrm, bn, rr, u = fr[rng.randint(len(fr) // 4, len(fr) - 2)]
        if p.z < 2.5:
            continue
        foot = Vector((p.x + rng.gauss(0, 0.4), p.y + rng.gauss(0, 0.4), 0))
        pts = catmull([p - Z * rr * 0.3, (p + foot) / 2 + Vector((rng.gauss(0, 0.3), rng.gauss(0, 0.3), 0)), foot], max(6, int(p.z * 2)))
        fused = rng.random() < 0.4
        pr = rr * rng.uniform(0.55, 0.85)
        sweep(mesh, pts, lambda v, pr=pr: lerp(pr, pr * 1.7, v ** 3), 8, "Bark", seed + i, lumps=0.12, knots=0.1)
        if fused:
            sweep(mesh, [q + Vector((0.12, 0.08, 0)) for q in pts], lambda v, pr=pr: pr * 0.5, 6, "Bark", seed + i + 7, lumps=0.12)
    return mesh


def stilt_tree(seed, height, r, stilts=10, stilt_h=2.0, pandan=True):
    """A trunk that starts a couple of metres up, standing on a cone of stilt
    roots - a walking palm or a pandanus, whose tips carry strap rosettes."""
    rng = random.Random(seed)
    mesh = Mesh()
    spec = dict(THIN, kids=(3, 2), up=(0.3, 0.7), ratio=(0.3, 0.45), leaves=0 if pandan else 20)
    tree(seed, height, r, r * 0.6, spec, wind=0.1, lean=0.1, start_z=stilt_h, mesh=mesh, first_limb=0.4, taper=0.6)
    for i in range(stilts):
        a = i / stilts * TAU + rng.uniform(-0.25, 0.25)
        out = Vector((math.cos(a), math.sin(a), 0))
        top = Vector((0, 0, stilt_h + rng.uniform(-0.3, 0.3))) + out * r * 0.5
        foot = out * stilt_h * rng.uniform(0.5, 0.9)
        pts = catmull([top, (top + foot) / 2 + out * 0.2, foot], 8)
        sweep(mesh, pts, lambda u: lerp(r * 0.45, r * 0.25, u), 6, "Bark", seed + i, lumps=0.08)
    if pandan:
        for p, d in mesh.tips:
            rosette(mesh, rng, p, (d + Z * 0.5).normalized(), rng.randint(12, 18), rng.uniform(1.0, 1.6), width=0.06)
    return mesh


def cycad(seed, height, fronds):
    """A short scaly trunk with a crown of stiff pinnate fronds."""
    rng = random.Random(seed)
    mesh = Mesh()
    path = [Vector((0, 0, z)) for z in (0, height * 0.5, height)]
    frames = sweep(mesh, path, lambda u: lerp(0.3, 0.25, u), 12, "Bark", seed, lumps=0.15, scars=0.35)
    top = frames[-1][0]
    for i in range(fronds):
        a = i / fronds * TAU + rng.uniform(-0.2, 0.2)
        d = Vector((math.cos(a), math.sin(a), 0))
        L = rng.uniform(1.4, 2.2)
        strip(mesh, rng, top, d, rng.uniform(0.7, 1.3), L, L * 0.12, pinnate(26, 0.7), rng.uniform(0.5, 0.8), segs=36, cross=3, crease=0.4)
    return mesh


def banana(seed, stalks, height):
    """A banana or heliconia clump: leaning stalks, each with a few huge
    paddle leaves torn along the edges."""
    rng = random.Random(seed)
    mesh = Mesh()

    def torn(s):
        return OVAL(s) * (1 - 0.3 * (fbm(Vector((s * 9, seed, 0)), 2) > 0.2))

    for i in range(stalks):
        a = i / stalks * TAU + rng.uniform(-0.5, 0.5)
        out = Vector((math.cos(a), math.sin(a), 0))
        H = height * rng.uniform(0.6, 1.1)
        pts = bent_path(out * rng.uniform(0, 0.3), (Z + out * 0.25).normalized(), H, 0.1, out, 0.03, seed + i, 6)
        frames = sweep(mesh, pts, lambda u: lerp(0.09, 0.04, u), 8, "Bamboo", seed + i, lumps=0.02)
        for j in range(rng.randint(3, 5)):
            b = rng.uniform(0, TAU)
            d = Vector((math.cos(b), math.sin(b), 0))
            L = H * rng.uniform(0.6, 0.9)
            base = frames[max(len(frames) - 1 - j * 2, 1)][0]
            strip(mesh, rng, base, d, rng.uniform(0.8, 1.5), L, L * 0.22, torn, rng.uniform(0.9, 1.4), segs=14, cross=5, crease=0.25, cup=0.05,
                  twist=rng.uniform(-0.3, 0.3))
    return mesh


def reeds(seed, stalks, height):
    """Tall stems by the water, a few narrow leaves each."""
    rng = random.Random(seed)
    mesh = Mesh()
    for i in range(stalks):
        base = Vector((rng.gauss(0, 0.35), rng.gauss(0, 0.35), 0))
        d = (Z + Vector((rng.gauss(0, 0.15), rng.gauss(0, 0.15), 0))).normalized()
        H = height * rng.uniform(0.6, 1.2)
        pts = bent_path(base, d, H, 0.15, around(Z, rng, 1.5), 0.05, seed + i, 5)
        frames = sweep(mesh, pts, lambda u: lerp(0.012, 0.004, u), 4, "Bamboo", seed + i, lumps=0, cap=False)
        for k in range(1, len(frames) - 1):
            p, t, nrm, bn, r, u = frames[k]
            a = rng.uniform(0, TAU)
            ld = (nrm * math.cos(a) + bn * math.sin(a) + t * 0.6).normalized()
            L = rng.uniform(0.3, 0.6)
            strip(mesh, rng, p, Vector((ld.x, ld.y, 0)).normalized(), max(ld.z, 0.1) * 1.4, L, L * 0.05, BLADE, rng.uniform(0.6, 1.4), segs=4, cross=2, crease=0)
    return mesh


# ---------------------------------------------------------------------------
# The floor
# ---------------------------------------------------------------------------

def litter(seed, radius, count, twigs=6):
    """Fallen leaves lying about, a few twigs among them."""
    rng = random.Random(seed)
    mesh = Mesh()
    for i in range(count):
        base = Vector((rng.gauss(0, radius * 0.5), rng.gauss(0, radius * 0.5), rng.uniform(0.0, 0.04)))
        a = rng.uniform(0, TAU)
        d = Vector((math.cos(a), math.sin(a), 0))
        L = rng.uniform(0.15, 0.4)
        strip(mesh, rng, base, d, rng.uniform(0.05, 0.35), L, L * rng.uniform(0.35, 0.55), OVAL, rng.uniform(0.1, 0.5),
              segs=4, cross=3, crease=-0.15, cup=0.35, twist=rng.uniform(-0.5, 0.5), mat="Litter")
    for i in range(twigs):
        base = Vector((rng.gauss(0, radius * 0.5), rng.gauss(0, radius * 0.5), 0.015))
        a = rng.uniform(0, TAU)
        pts = bent_path(base, Vector((math.cos(a), math.sin(a), 0)), rng.uniform(0.3, 0.9), 0.05, Z, 0.15, seed + i, 4)
        for q in pts:
            q.z = max(q.z, 0.012)
        sweep(mesh, pts, lambda u: lerp(0.015, 0.006, u), 4, "Bark", seed + i, lumps=0)
    return mesh


def root_mat(seed, size, roots):
    """Surface roots criss-crossing a patch of ground - what the foot of a
    giant looks like a few metres out."""
    rng = random.Random(seed)
    mesh = Mesh()
    for i in range(roots):
        a = rng.uniform(0, TAU)
        A = Vector((math.cos(a), math.sin(a), 0)) * size * 0.5
        b = a + math.pi + rng.uniform(-1.2, 1.2)
        B = Vector((math.cos(b), math.sin(b), 0)) * size * 0.5
        mid1 = lerp(A, B, 0.33) + Vector((rng.gauss(0, size * 0.12), rng.gauss(0, size * 0.12), 0))
        mid2 = lerp(A, B, 0.66) + Vector((rng.gauss(0, size * 0.12), rng.gauss(0, size * 0.12), 0))
        pts = catmull([A, mid1, mid2, B], int(size * 3))
        R = rng.uniform(0.05, 0.16)
        for k, q in enumerate(pts):
            s = k / (len(pts) - 1)
            q.z = R * 0.6 + abs(fbm(Vector((s * 5, i, seed)))) * R * 2.5 * math.sin(math.pi * s) - R * 1.4 * (1 - math.sin(math.pi * s)) ** 4
        sweep(mesh, pts, lambda u, R=R: R * (0.6 + 0.4 * math.sin(math.pi * u)), 6, "Bark", seed + i, lumps=0.15, knots=0.1)
        for j in range(rng.randint(1, 3)):
            k = rng.randint(2, len(pts) - 3)
            sd = (pts[k + 1] - pts[k - 1]).cross(Z).normalized() * rng.choice((-1, 1))
            sp = bent_path(pts[k], sd, size * rng.uniform(0.1, 0.25), 0.05, Z * -0.3, 0.2, seed + j, 4)
            for q in sp:
                q.z = max(q.z, 0.03)
            sweep(mesh, sp, lambda u, R=R: lerp(R * 0.4, 0.02, u), 4, "Bark", seed + j)
    return mesh


def fallen_frond(seed, length):
    rng = random.Random(seed)
    mesh = Mesh()
    strip(mesh, rng, Vector((-length / 2, 0, 0.03)), Vector((1, 0, 0)), 0.12, length, length * 0.14, pinnate(20, 0.6), 0.12,
          segs=30, cross=3, crease=0.3, twist=rng.uniform(-0.4, 0.4), mat="Litter")
    return mesh


def pebbles(seed, radius, count):
    rng = random.Random(seed)
    mesh = Mesh()
    for i in range(count):
        c = Vector((rng.gauss(0, radius * 0.45), rng.gauss(0, radius * 0.45), 0))
        rock_geom(mesh, rng, c, rng.uniform(0.08, 0.3), seed + i, stretch=(1.0, rng.uniform(0.7, 1.0), rng.uniform(0.4, 0.7)),
                  subdiv=1, rough=0.3, warp=0.3, yaw=rng.uniform(0, TAU))
    return mesh


def rock_stack(seed, sizes):
    rng = random.Random(seed)
    mesh = Mesh()
    mesh.smooth = False
    z = 0.0
    for i, s in enumerate(sizes):
        rock_geom(mesh, rng, Vector((rng.gauss(0, 0.1), rng.gauss(0, 0.1), z)), s, seed + i, stretch=(1.2, 1.0, 0.45),
                  flat_top=0.3, subdiv=2, rough=0.35, warp=0.4, yaw=rng.uniform(0, TAU), moss=1 if i else 2)
        z += s * 0.45 * 0.9
    return mesh


def vine_tangle(seed, radius, count):
    """A knot of vine on the ground or round a stump."""
    rng = random.Random(seed)
    mesh = Mesh()
    for i in range(count):
        pts = [Vector((rng.gauss(0, radius * 0.5), rng.gauss(0, radius * 0.5), rng.uniform(0.05, radius))) for _ in range(6)]
        path = catmull(pts, 24)
        for q in path:
            q.z = max(q.z, 0.04)
        rr = rng.uniform(0.02, 0.045)
        sweep(mesh, path, lambda u, rr=rr: rr, 5, "Vine", seed + i, lumps=0.15, cap=False)
        for k in range(3, 24, 6):
            leaves(mesh, rng, path[k], around(Z, rng, 1.3), 2, 0.14, 0.5, spread=1.2)
    return mesh


def vine_rope(seed, length, r):
    """Two thick vines twisted about each other, hanging from the origin."""
    rng = random.Random(seed)
    mesh = Mesh()
    axis = [Vector((fbm(Vector((t * 2, seed, 0))) * 0.4, fbm(Vector((seed, t * 2, 1))) * 0.4, -t * length)) for t in [i / 20 for i in range(21)]]
    for j in range(2):
        pts = []
        for i, q in enumerate(axis):
            a = i / 20 * TAU * 2.5 + j * math.pi
            pts.append(q + Vector((math.cos(a), math.sin(a), 0)) * r * 1.2)
        sweep(mesh, pts, lambda u, r=r: r * (1.0 - 0.3 * u), 6, "Vine", seed + j, lumps=0.15, knots=0.15, cap=False)
    for k in range(2, 20, 4):
        leaves(mesh, rng, axis[k], around(-Z, rng, 1.4), 3, 0.16, 0.5, spread=1.3)
    return mesh


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def export(ob, name):
    """One FBX for the object, at the origin, and a .mdl beside it that names
    the FBX and leaves the material to the default until one is chosen. An
    existing .mdl is kept - the editor fills it out on compile."""
    out_dir = os.path.join(ROOT, "Assets", OUT)
    os.makedirs(out_dir, exist_ok=True)
    ob.name = name
    ob.data.name = name
    ob.location = (0, 0, 0)
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    fbx = os.path.join(out_dir, name + ".fbx")
    bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, object_types={"MESH"},
                             apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y",
                             mesh_smooth_type="FACE", use_mesh_modifiers=True, add_leaf_bones=False,
                             bake_anim=False, path_mode="AUTO")
    mdl_path = os.path.join(out_dir, name + ".mdl")
    if not os.path.exists(mdl_path):
        mdl = {
            "Meshes": [{"Name": "", "File": f"{OUT}/{name}.fbx", "Scale": 1.0, "Include": [],
                        "Enabled": True, "Position": "0,0,0", "Rotation": "0,0,0", "Parent": ""}],
            "Scale": 1.0, "Material": "", "Materials": [], "MaterialRemaps": [],
        }
        with open(mdl_path, "w") as f:
            json.dump(mdl, f, indent=2)
    return fbx


# ---------------------------------------------------------------------------
# The catalogue: name -> how it is grown. Grouped as the rows they are laid
# out in for review.
# ---------------------------------------------------------------------------

GIANT = dict(kids=(6, 4, 3), where=(0.5, 0.9), up=(0.05, 0.35), ratio=(0.4, 0.6), kid_r=(0.55, 0.7),
             bend=(0.15, 0.4), wiggle=0.1, sides=16, lumps=0.08, knots=0.15, leaves=50, leaf=0.5)
TALL = dict(kids=(4, 3), where=(0.7, 0.95), up=(0.3, 0.6), ratio=(0.22, 0.38), kid_r=(0.4, 0.55), leaves=40, leaf=0.38)
SPREADING = dict(kids=(5, 4, 3), where=(0.4, 0.85), up=(0.1, 0.4), ratio=(0.4, 0.6), kid_r=(0.5, 0.65),
                 bend=(0.15, 0.4), wiggle=0.1, sides=14, lumps=0.07, knots=0.1, leaves=44, leaf=0.45)
THIN = dict(kids=(3, 2), where=(0.6, 0.95), up=(0.4, 0.8), ratio=(0.25, 0.4), kid_r=(0.35, 0.5), sides=8, leaves=24, leaf=0.3)

CATALOGUE = {
    # -- giants: fluted, rooted, mossy, the ones the camera looks up at ------
    "tree_giant_a": lambda: tree(1, 17, 1.5, 0.5, GIANT, wind=0.06, lean=0.05, flutes=6, flare=1.4, flute_height=0.3,
                                 grooves=0.05, knots=0.15, roots=7, root_len=5, vines=2, hang=2, epiphytes=4, sides=36),
    "tree_giant_b": lambda: tree(2, 15, 1.8, 0.6, GIANT, wind=0.1, lean=0.12, flutes=5, flare=1.5, flute_height=0.32,
                                 grooves=0.06, knots=0.2, roots=9, root_len=6, vines=3, hang=3, epiphytes=5, sides=36),
    "tree_giant_c": lambda: tree(3, 14, 1.3, 0.45, dict(GIANT, kids=(4, 3, 2)), wind=0.08, lean=0.0, flutes=7, flare=1.2,
                                 flute_height=0.26, grooves=0.05, knots=0.1, roots=6, root_len=4, vines=1, hang=1, epiphytes=3, sides=36),
    # -- winding: the leaning, arching trunks over the path ------------------
    "tree_winding_a": lambda: tree(11, 13, 0.8, 0.3, SPREADING, wind=0.35, lean=0.3, knots=0.25, lumps=0.1, roots=4,
                                   root_len=3, vines=2, hang=3, epiphytes=6, first_limb=0.35),
    "tree_winding_b": lambda: tree(12, 11, 0.7, 0.25, SPREADING, wind=0.45, lean=0.3, knots=0.3, lumps=0.12, roots=3,
                                   root_len=2.5, vines=1, hang=2, epiphytes=5, first_limb=0.4),
    "tree_winding_c": lambda: tree(13, 15, 0.9, 0.3, SPREADING, wind=0.25, lean=0.4, knots=0.2, lumps=0.1, roots=5,
                                   root_len=3.5, vines=2, hang=4, epiphytes=8, first_limb=0.3),
    # -- leaning: the thick trunk over the path in the first reference, that
    #    goes up at forty-five degrees and curves back toward the sky --------
    "tree_lean_a": lambda: tree(15, 12, 1.1, 0.35, SPREADING, wind=0.2, lean=0.45, knots=0.3, lumps=0.12, grooves=0.04,
                                roots=6, root_len=4, vines=2, hang=4, epiphytes=10, first_limb=0.45, sides=18),
    "tree_lean_b": lambda: tree(16, 14, 0.9, 0.3, SPREADING, wind=0.3, lean=0.35, knots=0.25, lumps=0.1, grooves=0.04,
                                roots=5, root_len=3.5, vines=1, hang=3, epiphytes=8, first_limb=0.4, sides=18),
    # -- forked: two or three stems from one base ----------------------------
    "tree_forked_a": lambda: tree(21, 12, 0.7, 0.2, SPREADING, wind=0.1, fork=2, knots=0.15, roots=3, root_len=2.5, epiphytes=2),
    "tree_forked_b": lambda: tree(22, 10, 0.8, 0.2, SPREADING, wind=0.15, fork=3, knots=0.2, roots=4, root_len=2, vines=1, epiphytes=3),
    # -- tall and straight: the picket that fades into the fog ---------------
    "tree_tall_a": lambda: tree(31, 16, 0.35, 0.12, TALL, wind=0.03, lean=0.03, flutes=4, flare=0.5, grooves=0.04, vines=1),
    "tree_tall_b": lambda: tree(32, 18, 0.3, 0.1, TALL, wind=0.04, lean=0.06, flutes=4, flare=0.4, hang=1),
    "tree_tall_c": lambda: tree(33, 14, 0.4, 0.14, TALL, wind=0.05, lean=0.02, flutes=5, flare=0.6, grooves=0.05, vines=2, epiphytes=2),
    "tree_tall_d": lambda: tree(34, 20, 0.32, 0.1, TALL, wind=0.02, lean=0.08, flutes=3, flare=0.4),
    # -- thin: saplings and the arched poles of the middle ground ------------
    "tree_thin_a": lambda: tree(41, 8, 0.12, 0.05, THIN, wind=0.1, lean=0.1),
    "tree_thin_b": lambda: tree(42, 7, 0.1, 0.04, THIN, wind=0.15, lean=0.2),
    "tree_arch_a": lambda: tree(43, 9, 0.14, 0.05, dict(THIN, kids=(2,)), wind=0.2, lean=0.4),
    "tree_arch_b": lambda: tree(44, 7, 0.11, 0.04, dict(THIN, kids=(1,)), wind=0.25, lean=0.55),
    # -- palms and tree ferns ------------------------------------------------
    "palm_a": lambda: palm(51, 8, 0.2, fronds=16, frond_len=3.2, lean=0.25),
    "palm_b": lambda: palm(52, 6, 0.18, fronds=14, frond_len=2.8, lean=0.4, wind=0.12),
    "palm_c": lambda: palm(53, 11, 0.22, fronds=18, frond_len=3.6, lean=0.1),
    "palm_fan_a": lambda: palm(54, 5, 0.16, fronds=9, frond_len=2.6, lean=0.2, fan_leaf=True, dead=2),
    "palm_fan_b": lambda: palm(55, 3, 0.14, fronds=8, frond_len=2.2, lean=0.3, fan_leaf=True, dead=1),
    "treefern_a": lambda: tree_fern(61, 2.5),
    "treefern_b": lambda: tree_fern(62, 3.5, fronds=14, frond_len=2.2),
    # -- bamboo --------------------------------------------------------------
    "bamboo_a": lambda: bamboo(71, 7.0, 0.06),
    "bamboo_b": lambda: bamboo(72, 8.5, 0.07, lean=0.05),
    "bamboo_c": lambda: bamboo(73, 5.5, 0.05, lean=0.02),
    # -- undergrowth ---------------------------------------------------------
    "fern_a": lambda: fern(81, 9, 0.9),
    "fern_b": lambda: fern(82, 12, 1.1),
    "fern_c": lambda: fern(83, 7, 0.65),
    "fern_d": lambda: fern(84, 14, 1.4, up=(1.2, 2.0)),
    "broadleaf_a": lambda: broadleaf(91, 6, 1.2),
    "broadleaf_b": lambda: broadleaf(92, 5, 0.9),
    "elephant_a": lambda: broadleaf(93, 4, 1.8, profile=HEART, width=0.42, cup=0.3, stalk_up=(1.2, 2.2)),
    "elephant_b": lambda: broadleaf(94, 3, 2.3, profile=HEART, width=0.45, cup=0.3, stalk_up=(1.4, 2.4)),
    "fanplant_a": lambda: palm(95, 0.6, 0.06, fronds=6, frond_len=1.6, lean=0.1, fan_leaf=True, dead=0),
    "fanplant_b": lambda: palm(96, 1.2, 0.08, fronds=8, frond_len=2.0, lean=0.2, fan_leaf=True, dead=1),
    "grass_a": lambda: grass(101, 40, 0.6),
    "grass_b": lambda: grass(102, 60, 0.9),
    "sapling_a": lambda: sapling(111, 1.6),
    "sapling_b": lambda: sapling(112, 2.4, leaf_count=12),
    "bush_a": lambda: bush(121, 1.0, 14),
    "bush_b": lambda: bush(122, 1.5, 20),
    "lily_a": lambda: lily(131, 9, 0.6),
    "lily_b": lambda: lily(132, 12, 0.9),
    # -- vines ---------------------------------------------------------------
    "vinehang_a": lambda: vine_hang(141, 6, 5),
    "vinehang_b": lambda: vine_hang(142, 9, 8, spread=1.0),
    "vinehang_c": lambda: vine_hang(143, 4, 3, spread=0.3),
    "aerialroots_a": lambda: aerial_roots(144, 12, 1.8),
    "aerialroots_b": lambda: aerial_roots(145, 20, 2.8),
    "liana_a": lambda: liana(151, 5, 7, loops=1),
    "liana_b": lambda: liana(152, 7, 9, loops=2, r=0.09),
    "liana_c": lambda: liana(153, 3.5, 5, loops=1, r=0.05),
    "vinearch_a": lambda: vine_arch(161, 8, 6),
    "vinearch_b": lambda: vine_arch(162, 12, 8, r=0.07),
    # -- rocks and logs ------------------------------------------------------
    "rock_a": lambda: rock(171, 0.6),
    "rock_b": lambda: rock(172, 1.1),
    "rock_c": lambda: rock(173, 1.9, stretch=(1.0, 0.9, 0.7), moss=3),
    "rockflat_a": lambda: rock(174, 1.4, stretch=(1.4, 1.0, 0.45), flat_top=0.25, subdiv=2, rough=0.35, warp=0.45),
    "rockflat_b": lambda: rock(175, 2.4, stretch=(1.5, 1.1, 0.4), flat_top=0.3, subdiv=2, rough=0.4, warp=0.5),
    "rockflat_c": lambda: rock(176, 3.2, stretch=(1.7, 1.0, 0.38), flat_top=0.25, subdiv=2, rough=0.35, warp=0.5),
    "rockflat_d": lambda: rock(179, 2.0, stretch=(1.2, 1.3, 0.5), flat_top=0.2, subdiv=2, rough=0.45, warp=0.4),
    "rockslab_a": lambda: rock(177, 1.8, stretch=(1.0, 1.6, 0.25), flat_top=0.35, subdiv=2, rough=0.3, warp=0.4),
    "boulder_a": lambda: rock(178, 3.0, stretch=(1.2, 1.0, 0.8), rough=0.4, warp=0.5, moss=4),
    "boulder_b": lambda: rock(180, 2.2, stretch=(1.0, 1.1, 0.9), rough=0.45, warp=0.6, subdiv=2),
    "log_a": lambda: log(181, 7, 0.35),
    "log_b": lambda: log(182, 10, 0.5, stubs=5),
    # -- unusual trees -------------------------------------------------------
    "strangler_a": lambda: strangler(201, 16, 0.8, roots=10),
    "strangler_b": lambda: strangler(202, 13, 0.7, roots=14, moss=6),
    "banyan_a": lambda: banyan(211, 13, 1.4, 0.4, pillars=7),
    "banyan_b": lambda: banyan(212, 11, 1.1, 0.35, pillars=5, moss=6),
    "stilt_a": lambda: stilt_tree(221, 6, 0.22, stilts=10, stilt_h=2.0),
    "stilt_b": lambda: stilt_tree(222, 5, 0.2, stilts=14, stilt_h=1.6),
    "stilt_c": lambda: stilt_tree(223, 8, 0.25, stilts=8, stilt_h=2.5, pandan=False),
    "climbed_a": lambda: tree(231, 12, 0.5, 0.15, TALL, wind=0.05, lean=0.05, flutes=4, flare=0.5, climber=2, moss=5),
    "climbed_b": lambda: tree(232, 10, 0.7, 0.25, SPREADING, wind=0.15, lean=0.2, knots=0.2, climber=3, moss=8, roots=4, epiphytes=3),
    "mossy_giant": lambda: tree(233, 15, 1.4, 0.5, GIANT, wind=0.08, lean=0.1, flutes=6, flare=1.3, flute_height=0.3,
                                grooves=0.05, knots=0.2, roots=8, root_len=5, vines=1, hang=3, epiphytes=6, sides=36, moss=14),
    "cycad_a": lambda: cycad(241, 0.8, 16),
    "cycad_b": lambda: cycad(242, 1.5, 20),
    "banana_a": lambda: banana(251, 4, 2.8),
    "banana_b": lambda: banana(252, 6, 3.5),
    "reeds_a": lambda: reeds(261, 30, 1.8),
    "reeds_b": lambda: reeds(262, 45, 2.4),
    "bambooclump_a": lambda: bamboo_clump(271, 7, 7.0, 0.06),
    "bambooclump_b": lambda: bamboo_clump(272, 11, 8.5, 0.07),
    # -- dead wood -----------------------------------------------------------
    "snag_a": lambda: snag(301, 9, 0.5, 0.3),
    "snag_b": lambda: snag(302, 14, 0.7, 0.35, limbs=4, moss=5, fungi=3),
    "snag_c": lambda: snag(303, 6, 0.4, 0.3, limbs=2, moss=2, fungi=1),
    "stump_a": lambda: stump(311, 0.8, 0.6),
    "stump_b": lambda: stump(312, 1.4, 0.8, moss=6, fungi=2),
    "stump_c": lambda: stump(313, 0.5, 0.45, moss=3, fungi=0),
    "broken_a": lambda: broken_tree(321, 14, 0.6),
    "broken_b": lambda: broken_tree(322, 11, 0.45, break_at=0.55, moss=6),
    "uprooted_a": lambda: uprooted(331, 12, 0.55),
    "uprooted_b": lambda: uprooted(332, 9, 0.4, plate=1.5, moss=7),
    "logmossy_a": lambda: log_mossy(341, 8, 0.4),
    "logmossy_b": lambda: log_mossy(342, 12, 0.6, stubs=5, moss=10, fungi=4),
    "logmossy_c": lambda: log_mossy(343, 5, 0.3, stubs=2, moss=4, fungi=1),
    "debris_a": lambda: branch_debris(351, 2.5, 0.06),
    "debris_b": lambda: branch_debris(352, 4.0, 0.1),
    "debris_c": lambda: branch_debris(353, 1.5, 0.04),
    # -- moss and fungus -----------------------------------------------------
    "mosscushion_a": lambda: moss_cushion(401, 0.4),
    "mosscushion_b": lambda: moss_cushion(402, 0.7),
    "mosscushion_c": lambda: moss_cushion(403, 0.5, count=5),
    "mosscarpet_a": lambda: moss_carpet(411, 0.8),
    "mosscarpet_b": lambda: moss_carpet(412, 1.5),
    "mossdrape_a": lambda: moss_drape(421, 30, 0.6, 0.3),
    "mossdrape_b": lambda: moss_drape(422, 60, 1.2, 0.6),
    "brackets_a": lambda: brackets(431, 4, 0.2),
    "brackets_b": lambda: brackets(432, 7, 0.35),
    # -- the floor -----------------------------------------------------------
    "litter_a": lambda: litter(501, 1.2, 50),
    "litter_b": lambda: litter(502, 2.0, 110, twigs=10),
    "rootmat_a": lambda: root_mat(511, 5, 10),
    "rootmat_b": lambda: root_mat(512, 8, 16),
    "fallenfrond_a": lambda: fallen_frond(521, 2.2),
    "fallenfrond_b": lambda: fallen_frond(522, 3.0),
    "vinetangle_a": lambda: vine_tangle(531, 1.2, 7),
    "vinetangle_b": lambda: vine_tangle(532, 2.0, 10),
    "vinerope_a": lambda: vine_rope(541, 7, 0.06),
    "vinerope_b": lambda: vine_rope(542, 11, 0.09),
    # -- more rocks: pebbles to a cliff, mossy ones, stacks ------------------
    "pebbles_a": lambda: pebbles(601, 1.0, 25),
    "pebbles_b": lambda: pebbles(602, 1.8, 45),
    "rockmid_a": lambda: rock(611, 0.9, warp=0.5, moss=2),
    "rockmid_b": lambda: rock(612, 1.3, stretch=(1.3, 0.9, 0.6), warp=0.5, moss=3),
    "rockmid_c": lambda: rock(613, 1.6, stretch=(0.9, 1.2, 0.75), warp=0.6, moss=2),
    "rockbig_a": lambda: rock(621, 3.5, stretch=(1.1, 1.0, 0.85), warp=0.6, rough=0.4, moss=5),
    "rockbig_b": lambda: rock(622, 4.5, stretch=(1.4, 1.0, 0.7), warp=0.6, rough=0.4, moss=7),
    "rockbig_c": lambda: rock(623, 5.5, stretch=(1.0, 1.3, 0.9), warp=0.7, rough=0.45, moss=8),
    "cliff_a": lambda: rock(631, 8.0, stretch=(1.4, 0.9, 0.6), flat_top=0.12, warp=0.6, rough=0.35, moss=10),
    "cliff_b": lambda: rock(632, 11.0, stretch=(1.6, 0.8, 0.55), flat_top=0.15, warp=0.7, rough=0.35, moss=14),
    "streamstone_a": lambda: rock(641, 0.7, stretch=(1.2, 0.9, 0.5), warp=0.3, rough=0.15),
    "streamstone_b": lambda: rock(642, 1.2, stretch=(1.3, 1.0, 0.45), warp=0.35, rough=0.15, moss=2),
    "streamstone_c": lambda: rock(643, 2.0, stretch=(1.4, 1.1, 0.5), warp=0.35, rough=0.18, moss=3),
    "rockstack_a": lambda: rock_stack(651, [1.6, 1.1, 0.7]),
    "rockstack_b": lambda: rock_stack(652, [2.4, 1.5]),
    # -- the ground, 60 m square ---------------------------------------------
    "ground": lambda: ground(191, 60),
}

# Which row of the review layout each model stands in: the word before the
# first underscore, except trees, which go by their habit.
def row_of(name):
    parts = name.split("_")
    return parts[1] if parts[0] == "tree" else parts[0]


def to_ob(thing, name):
    return thing if isinstance(thing, bpy.types.Object) else thing.to_object(name)


def build_all(names=None, keep=True, export_files=True):
    """Grow every model in the catalogue (or the named ones), export each, and
    lay them out in rows by group so the viewport shows the set."""
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    names = names or list(CATALOGUE)
    rows = {}
    for n in names:
        rows.setdefault(row_of(n), []).append(n)
    written = []
    y = 0.0
    for key, group in rows.items():
        x = 0.0
        deepest = 0.0
        for name in group:
            old = bpy.data.objects.get(name)
            if old:
                bpy.data.objects.remove(old, do_unlink=True)
            ob = to_ob(CATALOGUE[name](), name)
            ob.name = name
            if export_files:
                written.append(export(ob, name))
            if keep:
                w = max(ob.dimensions.x, ob.dimensions.y, 1.0)
                x += w * 0.5 + 2.0
                ob.location = (x, y, 0)
                x += w * 0.5
                deepest = max(deepest, w, ob.dimensions.z)
            else:
                bpy.data.objects.remove(ob, do_unlink=True)
        y -= deepest + 12.0
    return written


if __name__ == "__main__":
    build_all()
