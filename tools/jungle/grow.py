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
MATERIALS = ["Bark", "Leaf", "Bamboo", "Rock", "Ground", "Vine"]

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
        me.polygons.foreach_set("use_smooth", [True] * len(me.polygons))
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
    tips = [(frames[-1][0], frames[-1][1])]
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


def surface_roots(mesh, rng, base_r, count, length, seed):
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
            p.z = max(0.0, 0.55 * (1 - t) ** 1.5 * base_r) + abs(fbm(Vector((t * 4, i * 3.1, seed)))) * 0.25 * (1 - t) + 0.05
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
         taper=1.0, lumps=0.06, first_limb=0.5, steps=None):
    """A tree of some habit. The trunk winds by `wind` and leans by `lean`;
    limbs follow `spec` (see DEFAULT_SPEC); the base can have buttress flutes,
    surface roots, vines wound about it, strands hanging from the limbs, and
    epiphyte rosettes sitting on its upper side. `fork` splits the trunk into
    that many stems partway up instead of one crown."""
    rng = random.Random(seed)
    mesh = Mesh()
    spec = dict(DEFAULT_SPEC, **(spec or {}))
    spec = dict(spec, where=(first_limb, spec["where"][1]))
    sides = sides or (20 if flutes else 12)
    steps = steps or max(12, int(height * 2))
    path = winding_path(rng, Vector((0, 0, 0)), height, wind, lean, steps)
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
    if roots:
        surface_roots(mesh, rng, r0, roots, root_len, seed)
    if vines:
        helix_vines(mesh, rng, frames, vines, seed)
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
    """A culm with a collar at every node, and twigs with leaf tufts along
    the upper half."""
    rng = random.Random(seed)
    mesh = Mesh()
    yaw = rng.uniform(0, TAU)
    lean_dir = Vector((math.cos(yaw), math.sin(yaw), 0))
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
        return Vector((0, 0, z)) + lean_dir * (lean * z + 0.25 * t * t * height * lean * 6)

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
    return mesh


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

def rock(seed, size, stretch=(1.0, 1.0, 0.65), flat_top=0.0, subdiv=3, rough=0.35, warp=0.3):
    """An icosphere pushed about by noise, squashed, cut flat underneath, and
    with `flat_top` the top sliced off too - a slab, a stepping stone. `warp`
    is a slow noise that pulls the whole shape out of round; `rough` the fast
    one that breaks the surface."""
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    for v in bm.verts:
        p = v.co * 1.4 + Vector((seed * 3.1, seed * 1.7, 0))
        v.co += v.normal * (fbm(p * 0.5, octaves=2) * warp + fbm(p, octaves=4) * rough + fbm(p * 3.5, octaves=2) * 0.06)
    hz = size * 0.5 * stretch[2]
    for v in bm.verts:
        v.co = Vector((v.co.x * stretch[0], v.co.y * stretch[1], v.co.z * stretch[2])) * size * 0.5
        v.co.z = max(v.co.z, -hz * 0.55)
        if flat_top:
            v.co.z = min(v.co.z, hz * (1 - flat_top) + fbm(v.co * 2) * hz * 0.08)
        v.co.z += hz * 0.45
    me = bpy.data.meshes.new("rock")
    bm.to_mesh(me)
    bm.free()
    for m in MATERIALS:
        me.materials.append(bpy.data.materials.get(m) or bpy.data.materials.new(m))
    me.polygons.foreach_set("material_index", [MATERIALS.index("Rock")] * len(me.polygons))
    me.polygons.foreach_set("use_smooth", [flat_top == 0] * len(me.polygons))
    me.update()
    ob = bpy.data.objects.new("rock", me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def log(seed, length, r, stubs=3):
    """A fallen trunk lying along X, a little bowed, with broken limb stubs."""
    rng = random.Random(seed)
    mesh = Mesh()
    pts = bent_path(Vector((-length / 2, 0, r * 0.8)), Vector((1, 0, 0)), length, 0.03, Z, 0.02, seed, max(8, int(length * 2)))
    frames = sweep(mesh, pts, lambda u: r * (1.15 - u * 0.3), 12, "Bark", seed, lumps=0.1, grooves=0.05, knots=0.15)
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
    "rock_c": lambda: rock(173, 1.9, stretch=(1.0, 0.9, 0.7)),
    "rockflat_a": lambda: rock(174, 1.4, stretch=(1.4, 1.0, 0.45), flat_top=0.25, subdiv=2, rough=0.35, warp=0.45),
    "rockflat_b": lambda: rock(175, 2.4, stretch=(1.5, 1.1, 0.4), flat_top=0.3, subdiv=2, rough=0.4, warp=0.5),
    "rockflat_c": lambda: rock(176, 3.2, stretch=(1.7, 1.0, 0.38), flat_top=0.25, subdiv=2, rough=0.35, warp=0.5),
    "rockflat_d": lambda: rock(179, 2.0, stretch=(1.2, 1.3, 0.5), flat_top=0.2, subdiv=2, rough=0.45, warp=0.4),
    "rockslab_a": lambda: rock(177, 1.8, stretch=(1.0, 1.6, 0.25), flat_top=0.35, subdiv=2, rough=0.3, warp=0.4),
    "boulder_a": lambda: rock(178, 3.0, stretch=(1.2, 1.0, 0.8), rough=0.4, warp=0.5),
    "boulder_b": lambda: rock(180, 2.2, stretch=(1.0, 1.1, 0.9), rough=0.45, warp=0.6, subdiv=2),
    "log_a": lambda: log(181, 7, 0.35),
    "log_b": lambda: log(182, 10, 0.5, stubs=5),
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
