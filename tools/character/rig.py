#!/usr/bin/env python3
"""The test ground's rigged character, built inside Blender and written out as
one FBX with every take in it, plus the .mdl that names the clips, the jiggle
bones, the ragdoll and the attachments.

There is no hand-made art here on purpose: a test scene has to be regenerable,
and a character nobody can rebuild is a character nobody can change. The body
is a wooden artist's mannequin grown from spheres and tapered tubes, one piece
per bone, skinned by distance to the bone it sits on.

Run it headless:

    blender -b -P tools/character/rig.py

or from inside Blender, with the checkout to write into set first:

    CHARACTER_ROOT = "/path/to/Rinten-Test-Ground"
    exec(open("tools/character/rig.py").read()); build()

Conventions this file keeps to, and why:

- Blender is Z-up with the character facing **+Y**. The FBX export turns that
  into the engine's Y-up (x, y, z) -> (x, z, -y), so +Y lands on -Z, which is
  `Vector3.Forward`. A character modelled facing -Y arrives back to front.
- Everything is in metres. The mannequin is 1.74 m to the top of the head.
- Bone local space: a bone runs along its own local **+Y**, in the engine as
  much as in Blender - the export turns the armature and leaves the bone frames
  where they were. That is why every ragdoll capsule and every attachment below
  is an offset along +Y: bone space is the space `ModelCollision` reads a hull
  in, and `tools/character/probe.py` is what says so - it reads the fbx back
  through the same ufbx the engine uses and prints each bone's local axes.
  Guessing this gave `(0, 0, -length)`, which is a ragdoll of capsules lying
  across their own limbs.
- Ragdoll joint anchors are written with `ModelSpace: true`, so they are the
  child bone's head in the model's own space - no bone frame to get wrong.
"""

import bpy
import json
import math
import os
from mathutils import Vector, Quaternion, Matrix

ROOT = globals().get("CHARACTER_ROOT", "/home/skipin/Documents/GitHub/Rinten-Test-Ground")
OUT = "models/character"
NAME = "mannequin"

TAU = math.tau
D = math.radians

# The arms rest in a T-pose, pointing along the character's own x. Turning the
# left one about the armature's +Y by this much sends +X to -Z, which is an arm
# hanging by its side; the right arm is the same number negated. The sign the
# other way round is a character holding both arms straight up, which is what
# every take here looked like the first time round.
ARM_DOWN = 72.0


# ---------------------------------------------------------------------------
# The skeleton
# ---------------------------------------------------------------------------
#
# name, head, tail, parent, connected. Heads and tails are in metres, Blender
# space, and the bones are listed parents first because the builder relies on
# that to hook each one up.

def mirrored(rows):
    """Every row again with x negated and .L swapped for .R."""
    out = []
    for name, head, tail, parent, conn in rows:
        out.append((name + ".L", head, tail, parent + ".L" if parent.endswith(("Arm", "Leg", "Shoulder", "Hand", "Foot")) else parent, conn))
    for name, head, tail, parent, conn in rows:
        flip = lambda p: (-p[0], p[1], p[2])
        out.append((name + ".R", flip(head), flip(tail), parent + ".R" if parent.endswith(("Arm", "Leg", "Shoulder", "Hand", "Foot")) else parent, conn))
    return out


SPINE = [
    ("Hips",  (0, 0, 0.98), (0, 0, 1.12), "",      False),
    ("Spine", (0, 0, 1.12), (0, 0, 1.29), "Hips",  True),
    ("Chest", (0, 0, 1.29), (0, 0, 1.47), "Spine", True),
    ("Neck",  (0, 0, 1.47), (0, 0, 1.57), "Chest", True),
    ("Head",  (0, 0, 1.57), (0, 0, 1.74), "Neck",  True),
]

LIMBS = mirrored([
    ("Shoulder", (0.035, 0, 1.425), (0.155, 0, 1.445), "Chest",    False),
    ("UpperArm", (0.155, 0, 1.445), (0.405, 0, 1.445), "Shoulder", True),
    ("LowerArm", (0.405, 0, 1.445), (0.640, 0, 1.445), "UpperArm", True),
    ("Hand",     (0.640, 0, 1.445), (0.760, 0, 1.445), "LowerArm", True),
    ("UpperLeg", (0.100, 0, 0.955), (0.100, 0, 0.530), "Hips",     False),
    ("LowerLeg", (0.100, 0, 0.530), (0.100, 0, 0.100), "UpperLeg", True),
    ("Foot",     (0.100, 0, 0.100), (0.100, 0.130, 0.048), "LowerLeg", True),
    ("Toe",      (0.100, 0.130, 0.048), (0.100, 0.205, 0.048), "Foot", True),
])

# The ponytail is the jiggle chain: nothing animates it, it only ever swings
# because the body it hangs off moved.
PONYTAIL = [
    ("Ponytail1", (0, -0.090, 1.690), (0, -0.150, 1.600), "Head",      False),
    ("Ponytail2", (0, -0.150, 1.600), (0, -0.195, 1.500), "Ponytail1", True),
    ("Ponytail3", (0, -0.195, 1.500), (0, -0.225, 1.395), "Ponytail2", True),
    ("Ponytail4", (0, -0.225, 1.395), (0, -0.240, 1.285), "Ponytail3", True),
]

# And a belt tassel, so there is a second chain hanging off a bone that the
# walk cycle itself throws about.
TASSEL = [
    ("Tassel1", (0.000, -0.135, 1.040), (0.000, -0.170, 0.945), "Hips",    False),
    ("Tassel2", (0.000, -0.170, 0.945), (0.000, -0.190, 0.845), "Tassel1", True),
    ("Tassel3", (0.000, -0.190, 0.845), (0.000, -0.200, 0.750), "Tassel2", True),
]

BONES = SPINE + LIMBS + PONYTAIL + TASSEL

BY_NAME = {b[0]: b for b in BONES}


def head_of(name):
    return Vector(BY_NAME[name][1])


def tail_of(name):
    return Vector(BY_NAME[name][2])


def length_of(name):
    return (tail_of(name) - head_of(name)).length


# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------
#
# A piece is a list of vertices and faces in model space, tagged with the
# material slot it wears. Built here rather than by a modifier stack so that
# the same numbers can be read back for the ragdoll below.

class Mesh:
    def __init__(self):
        self.verts = []
        self.faces = []
        self.slots = []          # one material slot index per face

    def add(self, verts, faces, slot):
        base = len(self.verts)
        self.verts.extend(verts)
        for f in faces:
            self.faces.append(tuple(base + i for i in f))
            self.slots.append(slot)


SLOTS = ["Body", "Joint"]
BODY, JOINT = 0, 1


def frame(direction):
    """A right-handed frame with its third axis along `direction`."""
    z = Vector(direction).normalized()
    up = Vector((0, 0, 1)) if abs(z.z) < 0.9 else Vector((1, 0, 0))
    x = up.cross(z).normalized()
    y = z.cross(x)
    return x, y, z


def tube(mesh, a, b, ra, rb, sides=12, slot=BODY, squash=1.0):
    """A tapered tube from a to b. `squash` flattens it across its own x."""
    a, b = Vector(a), Vector(b)
    x, y, z = frame(b - a)
    verts, faces = [], []
    for ring, (centre, r) in enumerate(((a, ra), (b, rb))):
        for i in range(sides):
            t = i / sides * TAU
            verts.append(centre + x * (math.cos(t) * r * squash) + y * (math.sin(t) * r))
    for i in range(sides):
        j = (i + 1) % sides
        faces.append((i, j, sides + j, sides + i))
    # Caps, as fans round a centre vertex, so the shape is closed and the
    # convex hull the collision is built from has nothing to leak through.
    for ring, centre in ((0, a), (1, b)):
        c = len(verts)
        verts.append(centre)
        for i in range(sides):
            j = (i + 1) % sides
            o = ring * sides
            faces.append((c, o + j, o + i) if ring == 0 else (c, o + i, o + j))
    mesh.add(verts, faces, slot)


def ball(mesh, centre, r, seg=12, rings=8, slot=JOINT, scale=(1, 1, 1)):
    centre = Vector(centre)
    verts, faces = [], []
    for ring in range(rings + 1):
        v = ring / rings * math.pi
        for i in range(seg):
            u = i / seg * TAU
            p = Vector((math.sin(v) * math.cos(u), math.sin(v) * math.sin(u), math.cos(v)))
            verts.append(centre + Vector((p.x * r * scale[0], p.y * r * scale[1], p.z * r * scale[2])))
    for ring in range(rings):
        for i in range(seg):
            j = (i + 1) % seg
            a = ring * seg
            b = (ring + 1) * seg
            faces.append((a + i, a + j, b + j, b + i))
    mesh.add(verts, faces, slot)


def box(mesh, centre, extents, slot=BODY):
    c, e = Vector(centre), Vector(extents)
    verts = [c + Vector((sx * e.x, sy * e.y, sz * e.z))
             for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1),
             (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    mesh.add(verts, faces, slot)


def along(name, t):
    """A point a fraction of the way down a bone."""
    return head_of(name).lerp(tail_of(name), t)


def limb(mesh, name, ra, rb, joint=None, sides=10, squash=1.0):
    """The usual thing: a tapered tube on a bone with a ball at its head."""
    tube(mesh, head_of(name), tail_of(name), ra, rb, sides, BODY, squash)
    if joint:
        ball(mesh, head_of(name), joint, slot=JOINT)


def build_body():
    """The mannequin, in its rest pose, one piece per bone."""
    m = Mesh()

    # Torso: a pelvis block, a waist ball and a chest that widens to the
    # shoulders - the shape that makes a mannequin read as a mannequin.
    tube(m, head_of("Hips"), tail_of("Hips"), 0.115, 0.098, 14, BODY, 1.35)
    ball(m, tail_of("Hips"), 0.062, slot=JOINT)
    tube(m, head_of("Spine"), tail_of("Spine"), 0.098, 0.115, 14, BODY, 1.25)
    ball(m, tail_of("Spine"), 0.066, slot=JOINT)
    tube(m, head_of("Chest"), tail_of("Chest"), 0.120, 0.105, 14, BODY, 1.5)

    tube(m, head_of("Neck"), tail_of("Neck"), 0.042, 0.040, 8, BODY)
    # The head is an egg with a flat face, so which way it looks is never in
    # doubt in a screenshot.
    ball(m, head_of("Head") + Vector((0, 0.005, 0.082)), 0.092, 14, 10, BODY, (0.92, 1.0, 1.05))
    box(m, head_of("Head") + Vector((0, 0.088, 0.082)), (0.052, 0.008, 0.040), JOINT)

    for side, s in (("L", 1.0), ("R", -1.0)):
        ball(m, head_of("UpperArm." + side), 0.055, slot=JOINT)
        limb(m, "UpperArm." + side, 0.048, 0.040, sides=10)
        ball(m, head_of("LowerArm." + side), 0.043, slot=JOINT)
        limb(m, "LowerArm." + side, 0.038, 0.030, sides=10)
        ball(m, head_of("Hand." + side), 0.032, slot=JOINT)
        tube(m, head_of("Hand." + side), tail_of("Hand." + side), 0.036, 0.030, 8, BODY, 0.55)

        ball(m, head_of("UpperLeg." + side), 0.072, slot=JOINT)
        limb(m, "UpperLeg." + side, 0.068, 0.054, sides=12)
        ball(m, head_of("LowerLeg." + side), 0.056, slot=JOINT)
        limb(m, "LowerLeg." + side, 0.050, 0.038, sides=10)
        ball(m, head_of("Foot." + side), 0.040, slot=JOINT)
        tube(m, head_of("Foot." + side), tail_of("Foot." + side), 0.046, 0.044, 8, BODY, 0.75)
        tube(m, head_of("Toe." + side), tail_of("Toe." + side), 0.044, 0.030, 8, BODY, 0.75)
        box(m, (s * 0.100, 0.095, 0.030), (0.042, 0.105, 0.026), BODY)

    for chain, r0, r1 in ((PONYTAIL, 0.058, 0.022), (TASSEL, 0.040, 0.016)):
        n = len(chain)
        for i, (name, _, _, _, _) in enumerate(chain):
            a = r0 + (r1 - r0) * (i / n)
            b = r0 + (r1 - r0) * ((i + 1) / n)
            tube(m, head_of(name), tail_of(name), a, b, 8, JOINT)

    return m


# ---------------------------------------------------------------------------
# Skinning
# ---------------------------------------------------------------------------
#
# Weights by distance to the bone segment, with a per-bone reach so nothing
# bleeds across the body, then two passes of smoothing over the mesh edges.
# It is not a weight paint, but for a body made of one piece per bone it lands
# where a weight paint would and it is reproducible.

REACH = {
    "Hips": 0.32, "Spine": 0.30, "Chest": 0.34, "Neck": 0.16, "Head": 0.22,
    "Shoulder": 0.16, "UpperArm": 0.16, "LowerArm": 0.13, "Hand": 0.12,
    "UpperLeg": 0.22, "LowerLeg": 0.18, "Foot": 0.14, "Toe": 0.12,
    "Ponytail1": 0.10, "Ponytail2": 0.09, "Ponytail3": 0.08, "Ponytail4": 0.08,
    "Tassel1": 0.08, "Tassel2": 0.07, "Tassel3": 0.07,
}


def reach_of(name):
    return REACH.get(name.split(".")[0], 0.15)


def side_of(name):
    return name[-2:] if name[-2:] in (".L", ".R") else ""


def chain_of(name):
    stem = name.split(".")[0]
    if stem.startswith("Ponytail"):
        return "ponytail"
    if stem.startswith("Tassel"):
        return "tassel"
    return ""


def distance_to_segment(p, a, b):
    ab = b - a
    denom = ab.dot(ab)
    t = 0.0 if denom == 0.0 else max(0.0, min(1.0, (p - a).dot(ab) / denom))
    return (p - (a + ab * t)).length


def skin(verts, edges):
    """Four weights a vertex, as {bone name: weight} per vertex."""
    segments = [(n, head_of(n), tail_of(n), reach_of(n), side_of(n), chain_of(n)) for n, *_ in BONES]

    raw = []
    for p in verts:
        scores = {}
        for name, a, b, reach, side, chain in segments:
            d = distance_to_segment(p, a, b)
            if d > reach:
                continue
            # A hair chain only ever holds its own hair, and a hand never
            # holds the other arm: without these two the ponytail drags the
            # skull about and the arms weld to the hips when they hang.
            if chain and d > reach * 0.55:
                continue
            scores[name] = ((reach - d) / reach) ** 3 + 1e-6
        if not scores:
            name = min(segments, key=lambda s: distance_to_segment(p, s[1], s[2]))[0]
            scores = {name: 1.0}
        raw.append(scores)

    # Smoothing over the edges takes the seam out of the joints, where a
    # distance rule steps from one bone to the next in a single ring.
    for _ in range(3):
        blended = [dict(w) for w in raw]
        for i, j in edges:
            for a, b in ((i, j), (j, i)):
                for name, weight in raw[b].items():
                    blended[a][name] = blended[a].get(name, 0.0) + weight * 0.5
        raw = blended

    out = []
    for scores in raw:
        best = sorted(scores.items(), key=lambda kv: -kv[1])[:4]
        total = sum(w for _, w in best)
        out.append({n: w / total for n, w in best})
    return out


# ---------------------------------------------------------------------------
# Building it in Blender
# ---------------------------------------------------------------------------

def wipe():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.armatures, bpy.data.actions, bpy.data.materials):
        for item in list(block):
            block.remove(item)


def make_armature():
    arm = bpy.data.armatures.new("Armature")
    ob = bpy.data.objects.new("Armature", arm)
    bpy.context.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode="EDIT")

    for name, head, tail, parent, conn in BONES:
        bone = arm.edit_bones.new(name)
        bone.head = Vector(head)
        bone.tail = Vector(tail)
        bone.roll = 0.0
        if parent:
            bone.parent = arm.edit_bones[parent]
            bone.use_connect = conn

    bpy.ops.object.mode_set(mode="OBJECT")
    return ob


def make_body(armature):
    m = build_body()

    mesh = bpy.data.meshes.new(NAME)
    mesh.from_pydata([tuple(v) for v in m.verts], [], m.faces)
    mesh.validate()
    mesh.update()

    for slot in SLOTS:
        material = bpy.data.materials.get(slot) or bpy.data.materials.new(slot)
        mesh.materials.append(material)
    for face, slot in zip(mesh.polygons, m.slots):
        face.material_index = slot
        face.use_smooth = True

    # A planar unwrap is enough: the character wears flat colours, and a
    # model with no UVs at all is a model no textured material can ever be
    # tried on.
    uv = mesh.uv_layers.new(name="UVMap")
    for loop in mesh.loops:
        p = mesh.vertices[loop.vertex_index].co
        uv.data[loop.index].uv = (p.x * 0.5 + 0.5, p.z * 0.5)

    ob = bpy.data.objects.new(NAME, mesh)
    bpy.context.collection.objects.link(ob)

    edges = [(e.vertices[0], e.vertices[1]) for e in mesh.edges]
    weights = skin([Vector(v) for v in m.verts], edges)

    groups = {name: ob.vertex_groups.new(name=name) for name, *_ in BONES}
    for index, scores in enumerate(weights):
        for name, weight in scores.items():
            groups[name].add([index], weight, "REPLACE")

    ob.parent = armature
    modifier = ob.modifiers.new("Armature", "ARMATURE")
    modifier.object = armature
    modifier.use_vertex_groups = True
    return ob


# ---------------------------------------------------------------------------
# The takes
# ---------------------------------------------------------------------------
#
# Poses are written as turns about the armature's own axes, converted into the
# bone's rest frame - which is how an animator thinks about a leg swinging
# forwards, and keeps the numbers below readable.

def local_turn(armature, name, rx, ry, rz):
    bone = armature.data.bones[name]
    basis = bone.matrix_local.to_3x3().inverted()
    q = Quaternion()
    for axis, angle in ((Vector((1, 0, 0)), rx), (Vector((0, 1, 0)), ry), (Vector((0, 0, 1)), rz)):
        if angle:
            q = q @ Quaternion(basis @ axis, D(angle))
    return q


def key(armature, action, frame, name, rx=0.0, ry=0.0, rz=0.0, move=None):
    pose = armature.pose.bones[name]
    pose.rotation_mode = "QUATERNION"
    pose.rotation_quaternion = local_turn(armature, name, rx, ry, rz)
    if move is not None:
        bone = armature.data.bones[name]
        pose.location = bone.matrix_local.to_3x3().inverted() @ Vector(move)
    armature.keyframe_insert(f'pose.bones["{name}"].rotation_quaternion', frame=frame)
    if move is not None:
        armature.keyframe_insert(f'pose.bones["{name}"].location', frame=frame)


def new_action(armature, name):
    action = bpy.data.actions.new(name)
    action.use_fake_user = True
    armature.animation_data.action = action
    return action


def cycle(armature, action, frames, poser):
    """poser(frame, phase) for every frame, phase running 0..1 over the loop."""
    for i in range(frames + 1):
        poser(i + 1, (i % frames) / frames)


def build_actions(armature):
    armature.animation_data_create()
    actions = {}

    # --- idle: breathing, a slow weight shift, arms hanging.
    action = new_action(armature, "idle")
    def idle(frame, t):
        s = math.sin(t * TAU)
        key(armature, action, frame, "Hips", rz=2.0 * s, move=(0, 0, 0.008 * s))
        key(armature, action, frame, "Spine", rx=1.6 * s)
        key(armature, action, frame, "Chest", rx=-2.4 * s)
        key(armature, action, frame, "Neck", rx=1.0 * s)
        key(armature, action, frame, "Head", rz=-2.5 * s, rx=-1.0 * s)
        for side, sign in (("L", 1), ("R", -1)):
            key(armature, action, frame, "Shoulder." + side, ry=3.0 * sign)
            key(armature, action, frame, "UpperArm." + side, ry=ARM_DOWN * sign, rz=4.0 * s * sign)
            key(armature, action, frame, "LowerArm." + side, ry=8.0 * sign, rz=9.0 * sign)
            key(armature, action, frame, "Hand." + side, ry=4.0 * sign)
    cycle(armature, action, 72, idle)
    actions["idle"] = (action, 72)

    # --- walk: a 24 frame cycle, travelling forwards so the clip has root
    # motion to take off. The .mdl lifts it with MotionBone.
    action = new_action(armature, "walk")
    def walk(frame, t):
        s = math.sin(t * TAU)
        c = math.cos(t * TAU)
        stride = 0.72 / 24.0 * 24.0      # metres a cycle
        key(armature, action, frame, "Hips", rz=5.0 * c, rx=2.0,
            move=(0.018 * c, stride * t, -0.022 + 0.022 * math.cos(t * 2 * TAU)))
        key(armature, action, frame, "Spine", rz=-3.0 * c)
        key(armature, action, frame, "Chest", rz=-4.0 * c, rx=-2.0)
        key(armature, action, frame, "Head", rz=3.0 * c)
        for side, phase, sign in (("L", 0.0, 1), ("R", 0.5, -1)):
            p = (t + phase) % 1.0
            swing = math.sin(p * TAU)
            lift = max(0.0, math.sin(p * TAU + 0.6))
            key(armature, action, frame, "UpperLeg." + side, rx=30.0 * swing)
            key(armature, action, frame, "LowerLeg." + side, rx=-46.0 * lift * lift)
            key(armature, action, frame, "Foot." + side, rx=18.0 * lift - 12.0 * min(0.0, swing))
            key(armature, action, frame, "Toe." + side, rx=-10.0 * max(0.0, -swing))
            key(armature, action, frame, "Shoulder." + side, ry=3.0 * sign)
            key(armature, action, frame, "UpperArm." + side,
                ry=ARM_DOWN * sign, rz=(-32.0 * swing) * sign, rx=6.0 * sign)
            key(armature, action, frame, "LowerArm." + side,
                ry=10.0 * sign, rz=(22.0 + 14.0 * max(0.0, swing)) * sign)
    cycle(armature, action, 24, walk)
    actions["walk"] = (action, 24)

    # --- run: the same shape, harder, leaning in, off the ground in the middle.
    action = new_action(armature, "run")
    def run(frame, t):
        c = math.cos(t * TAU)
        key(armature, action, frame, "Hips", rz=7.0 * c, rx=9.0,
            move=(0.02 * c, 1.9 * t, -0.03 + 0.055 * math.cos(t * 2 * TAU)))
        key(armature, action, frame, "Spine", rz=-5.0 * c, rx=4.0)
        key(armature, action, frame, "Chest", rz=-6.0 * c, rx=2.0)
        key(armature, action, frame, "Neck", rx=-9.0)
        key(armature, action, frame, "Head", rz=4.0 * c, rx=-6.0)
        for side, phase, sign in (("L", 0.0, 1), ("R", 0.5, -1)):
            p = (t + phase) % 1.0
            swing = math.sin(p * TAU)
            lift = max(0.0, math.sin(p * TAU + 0.5))
            key(armature, action, frame, "UpperLeg." + side, rx=52.0 * swing - 6.0)
            key(armature, action, frame, "LowerLeg." + side, rx=-95.0 * lift * lift - 15.0)
            key(armature, action, frame, "Foot." + side, rx=26.0 * lift)
            key(armature, action, frame, "Toe." + side, rx=-14.0 * max(0.0, -swing))
            key(armature, action, frame, "Shoulder." + side, ry=5.0 * sign)
            key(armature, action, frame, "UpperArm." + side,
                ry=(ARM_DOWN - 14.0) * sign, rz=(-52.0 * swing) * sign, rx=12.0 * sign)
            key(armature, action, frame, "LowerArm." + side,
                ry=12.0 * sign, rz=(72.0 + 20.0 * max(0.0, swing)) * sign)
    cycle(armature, action, 18, run)
    actions["run"] = (action, 18)

    # --- wave: a one-shot the whole body plays, arm up and swinging.
    action = new_action(armature, "wave")
    frames = 48
    for i in range(frames + 1):
        frame = i + 1
        t = i / frames
        ease = min(1.0, t * 4.0) * min(1.0, (1.0 - t) * 4.0)
        s = math.sin(t * TAU * 3.0) * ease
        key(armature, action, frame, "Hips", rz=3.0 * ease)
        key(armature, action, frame, "Spine", rz=-3.0 * ease)
        key(armature, action, frame, "Chest", rz=-4.0 * ease, rx=-3.0 * ease)
        key(armature, action, frame, "Head", rz=6.0 * ease)
        key(armature, action, frame, "Shoulder.L", ry=3.0, rz=14.0 * ease)
        key(armature, action, frame, "UpperArm.L", ry=ARM_DOWN - 142.0 * ease, rz=16.0 * ease, rx=-7.0 * ease)
        key(armature, action, frame, "LowerArm.L", ry=8.0, rz=9.0 + 52.0 * ease + 20.0 * s)
        key(armature, action, frame, "Hand.L", ry=4.0, rz=22.0 * s)
        key(armature, action, frame, "Shoulder.R", ry=-3.0)
        key(armature, action, frame, "UpperArm.R", ry=-ARM_DOWN, rz=-6.0 * ease)
        key(armature, action, frame, "LowerArm.R", ry=-8.0, rz=-9.0 - 12.0 * ease)
        key(armature, action, frame, "Hand.R", ry=-4.0)
    actions["wave"] = (action, frames)

    # --- jump: crouch, leave, tuck, land.
    action = new_action(armature, "jump")
    frames = 36
    steps = [
        # frame, crouch, legs, arms
        (1,   0.00,   0.0,  0.0),
        (7,  -0.18,  46.0, -40.0),
        (12,  0.06, -14.0,  70.0),
        (20,  0.16,  62.0,  36.0),
        (28, -0.20,  52.0, -30.0),
        (36,  0.00,   0.0,  0.0),
    ]
    for frame, crouch, legs, arms in steps:
        key(armature, action, frame, "Hips", rx=max(0.0, -crouch) * 40.0, move=(0, 0, crouch))
        key(armature, action, frame, "Spine", rx=-legs * 0.12)
        key(armature, action, frame, "Chest", rx=-legs * 0.10)
        key(armature, action, frame, "Head", rx=legs * 0.08)
        for side, sign in (("L", 1), ("R", -1)):
            key(armature, action, frame, "UpperLeg." + side, rx=legs)
            key(armature, action, frame, "LowerLeg." + side, rx=-legs * 1.5)
            key(armature, action, frame, "Foot." + side, rx=legs * 0.5)
            key(armature, action, frame, "UpperArm." + side,
                ry=ARM_DOWN * sign, rz=arms * sign, rx=-abs(arms) * 0.2 * sign)
            key(armature, action, frame, "LowerArm." + side, ry=8.0 * sign, rz=(9.0 + abs(arms) * 0.4) * sign)
    actions["jump"] = (action, frames)

    return actions


def stack(armature, actions):
    """Every take on its own NLA track, which is what puts them all in one FBX.

    Blender's exporter skips an object that has no animation data at all, and
    exports one AnimationStack per track - so a take that is only a fake-user
    action never reaches the file.
    """
    armature.animation_data.action = None
    for name, (action, frames) in actions.items():
        track = armature.animation_data.nla_tracks.new()
        track.name = name
        strip = track.strips.new(name, 1, action)
        strip.action_frame_start = 1
        strip.action_frame_end = frames + 1
        track.mute = False


# ---------------------------------------------------------------------------
# The model definition
# ---------------------------------------------------------------------------

def clip(file, name, **rest):
    out = {
        "File": file, "Name": name, "TakeName": name, "Take": 0,
        "SubtractFrom": "", "SubtractFrame": -1, "SubtractModelSpace": False,
        "FirstFrame": -1, "LastFrame": -1,
        "MotionBone": "", "MotionAcross": False, "MotionUp": False,
        "AlignTo": "", "AlignFrame": 0, "AlignToFrame": 0, "AlignBone": "",
        "AlignAcross": False, "AlignUp": False,
        "SmoothFromStart": 0, "SmoothFromEnd": 0,
        "LayerFrom": "", "TurnDegrees": 0.0,
    }
    out.update(rest)
    return out


def jiggle(bone, stiffness, damping, gravity, max_angle, radius, folder, length=0.0):
    return {
        "Bone": bone, "Enabled": True, "Stiffness": stiffness, "Damping": damping,
        "Gravity": gravity, "WorldMotion": 1.0, "MaxAngle": max_angle, "Weight": 1.0,
        "Length": length, "Axis": "Auto", "Radius": radius, "Folder": folder,
    }


def capsule(name, bone, radius, folder="Ragdoll"):
    """A capsule down the bone, in the bone's own space.

    A bone runs along its own local +Y - measured, not assumed; see the module
    docstring - so the capsule is the segment from its origin to its length.
    Nothing here has to know which way the character faces.
    """
    return {
        "__type": "CapsuleHull", "Name": name, "Enabled": True, "Bone": bone,
        "Surface": "", "Tags": "", "Folder": folder,
        "PointA": "0,0,0", "PointB": f"0,{length_of(bone):.4f},0", "Radius": radius,
    }


def joint(name, kind, a, b, swing=40.0, twist=(-20.0, 20.0), anchor=(0.0, 0.0, 0.0),
          hinge=(-90.0, 5.0), folder="Ragdoll"):
    """A ragdoll joint at the child bone's head, written in model space.

    `ModelSpace` means the anchor is the model's own space rather than the
    parent bone's, which is the one an author can write down from the rest pose
    without deriving a bone frame first.

    `anchor` turns that frame, and for a hinge it is the whole of the joint:
    box3d turns a revolute joint about its frame's **z**, so an anchor left at
    nought is a knee that bends sideways. The angles that aim z are measured,
    not guessed - pitch 90 sends it to model +Y, yaw 90 to model +X - so a knee
    is `(0, 90, 0)`, turning about the character's left-to-right axis, and an
    elbow in a T-pose is `(90, 0, 0)`, turning about its upright.

    A ball joint's cone is centred on the bind pose, which is what frameA and
    frameB agreeing means: a limb may swing `swing` degrees from where it rests.
    """
    head = head_of(b)
    return {
        "Name": name, "Enabled": True, "Type": kind, "BoneA": a, "BoneB": b,
        "Position": engine_point(head),
        "Rotation": f"{anchor[0]},{anchor[1]},{anchor[2]}", "ModelSpace": True,
        "EnableCollision": False, "Folder": folder,
        "LinearStrength": 0.0, "AngularStrength": 0.0, "Friction": 0.0,
        "EnableSwingLimit": kind == "Ball", "SwingLimit": swing,
        "SwingOffset": "0,0,0",
        "EnableTwistLimit": kind == "Ball", "MinTwist": twist[0], "MaxTwist": twist[1],
        "Stiffness": 0.0, "Damping": 1.0,
        "MinAngle": hinge[0], "MaxAngle": hinge[1],
        "MinLength": 0.0, "MaxLength": 0.2,
    }


def engine_point(p):
    """Blender (x, y, z) as the engine's (x, z, -y), which is what the FBX
    export does to every vertex - so a number written here in model space
    lands where the same number is in Blender."""
    return f"{p[0]:.4f},{p[2]:.4f},{-p[1]:.4f}"


def attachment(name, bone, offset=(0, 0, 0)):
    """A named point on a bone, in the bone's own space - +Y is down the bone."""
    return {
        "Name": name, "Enabled": True, "Parent": bone,
        "Position": f"{offset[0]:.4f},{offset[1]:.4f},{offset[2]:.4f}", "Rotation": "0,0,0",
        "FacesOneWay": False, "Influences": [], "Folder": "Attachments",
    }


RAGDOLL = [
    # bone, radius
    ("Hips", 0.115), ("Spine", 0.105), ("Chest", 0.115), ("Head", 0.088),
    ("UpperArm.L", 0.048), ("LowerArm.L", 0.038), ("Hand.L", 0.034),
    ("UpperArm.R", 0.048), ("LowerArm.R", 0.038), ("Hand.R", 0.034),
    ("UpperLeg.L", 0.066), ("LowerLeg.L", 0.050), ("Foot.L", 0.042),
    ("UpperLeg.R", 0.066), ("LowerLeg.R", 0.050), ("Foot.R", 0.042),
]

# name, kind, parent bone, child bone, ball swing, ball twist, anchor angles,
# hinge range. A hinge's range is signed about its own axis, so the two elbows
# are not the same numbers: the left forearm rests along +X and the right along
# -X, and bending both forwards turns them opposite ways about the shared
# upright.
JOINTS = [
    ("spine", "Ball", "Hips", "Spine", 30.0, (-25.0, 25.0), (0, 0, 0), (0, 0)),
    ("chest", "Ball", "Spine", "Chest", 25.0, (-20.0, 20.0), (0, 0, 0), (0, 0)),
    ("head", "Ball", "Chest", "Head", 40.0, (-45.0, 45.0), (0, 0, 0), (0, 0)),
    ("shoulder.L", "Ball", "Chest", "UpperArm.L", 80.0, (-45.0, 45.0), (0, 0, 0), (0, 0)),
    ("shoulder.R", "Ball", "Chest", "UpperArm.R", 80.0, (-45.0, 45.0), (0, 0, 0), (0, 0)),
    ("elbow.L", "Hinge", "UpperArm.L", "LowerArm.L", 0.0, (0, 0), (90, 0, 0), (0.0, 140.0)),
    ("elbow.R", "Hinge", "UpperArm.R", "LowerArm.R", 0.0, (0, 0), (90, 0, 0), (-140.0, 0.0)),
    ("wrist.L", "Ball", "LowerArm.L", "Hand.L", 45.0, (-30.0, 30.0), (0, 0, 0), (0, 0)),
    ("wrist.R", "Ball", "LowerArm.R", "Hand.R", 45.0, (-30.0, 30.0), (0, 0, 0), (0, 0)),
    ("hip.L", "Ball", "Hips", "UpperLeg.L", 60.0, (-30.0, 30.0), (0, 0, 0), (0, 0)),
    ("hip.R", "Ball", "Hips", "UpperLeg.R", 60.0, (-30.0, 30.0), (0, 0, 0), (0, 0)),
    ("knee.L", "Hinge", "UpperLeg.L", "LowerLeg.L", 0.0, (0, 0), (0, 90, 0), (-135.0, 2.0)),
    ("knee.R", "Hinge", "UpperLeg.R", "LowerLeg.R", 0.0, (0, 0), (0, 90, 0), (-135.0, 2.0)),
    ("ankle.L", "Ball", "LowerLeg.L", "Foot.L", 35.0, (-20.0, 20.0), (0, 0, 0), (0, 0)),
    ("ankle.R", "Ball", "LowerLeg.R", "Foot.R", 35.0, (-20.0, 20.0), (0, 0, 0), (0, 0)),
]


def definition():
    fbx = f"{OUT}/{NAME}.fbx"

    clips = [
        clip(fbx, "idle"),
        # The walk and the run are drawn travelling forwards; the travel comes
        # off here so the game carries the character and the clip plays on the
        # spot. What came off is what a renderer reports as RootMotion.
        clip(fbx, "walk", MotionBone="Hips", MotionAcross=True),
        clip(fbx, "run", MotionBone="Hips", MotionAcross=True),
        clip(fbx, "wave"),
        clip(fbx, "jump"),
    ]

    jiggles = [
        jiggle("Ponytail1", 5.0, 0.35, 0.35, 55.0, 0.045, "Ponytail"),
        jiggle("Ponytail2", 6.0, 0.32, 0.35, 50.0, 0.035, "Ponytail"),
        jiggle("Ponytail3", 7.0, 0.30, 0.35, 45.0, 0.026, "Ponytail"),
        # The tip has no child to measure, so it says how long it is.
        jiggle("Ponytail4", 8.0, 0.28, 0.35, 40.0, 0.018, "Ponytail",
               length=length_of("Ponytail4")),
        jiggle("Tassel1", 4.0, 0.25, 0.8, 70.0, 0.030, "Tassel"),
        jiggle("Tassel2", 5.0, 0.24, 0.8, 65.0, 0.022, "Tassel"),
        jiggle("Tassel3", 6.0, 0.22, 0.8, 60.0, 0.014, "Tassel",
               length=length_of("Tassel3")),
    ]

    # Spheres the hanging chains are kept out of. Their radii are the largest
    # that still leave every chain's own root outside them: a collider that
    # contains the bone it is meant to guard pushes that bone out on the first
    # frame and holds it there, which reads as hair standing away from a head.
    colliders = [
        {"Bone": "Chest", "Enabled": True, "Position": "0,0,0", "Radius": 0.14, "Folder": "Body"},
        {"Bone": "Head", "Enabled": True, "Position": "0,0.085,0", "Radius": 0.07, "Folder": "Body"},
        {"Bone": "Hips", "Enabled": True, "Position": "0,0,0", "Radius": 0.11, "Folder": "Body"},
    ]

    hulls = [capsule(bone, bone, radius) for bone, radius in RAGDOLL]
    joints = [joint(name, kind, a, b, swing, twist, anchor, hinge)
              for name, kind, a, b, swing, twist, anchor, hinge in JOINTS]

    return {
        "Meshes": [{
            "Name": "", "File": fbx, "Scale": 1.0, "Include": [], "Enabled": True,
            "Position": "0,0,0", "Rotation": "0,0,0", "Parent": "",
        }],
        "Scale": 1.0,
        "Material": "materials/character/body.mat",
        "Materials": ["materials/character/body.mat"],
        "MaterialRemaps": [
            {"Surface": "Body", "Material": "materials/character/body.mat"},
            {"Surface": "Joint", "Material": "materials/character/joint.mat"},
        ],
        "Clips": clips,
        "Transform": {"Enabled": True, "Position": "0,0,0", "Rotation": "0,0,0",
                      "Scale": "1,1,1", "IsIdentity": True},
        "Mirror": {"Enabled": False, "Axis": "X", "FlipWinding": True, "RemapLeftRight": True},
        "Joints": joints,
        "LookAtChains": [{
            "Name": "look", "Bones": [
                {"Bone": "Chest", "Weight": 0.2},
                {"Bone": "Neck", "Weight": 0.35},
                {"Bone": "Head", "Weight": 0.45},
            ],
        }],
        "IkChains": [
            {"Name": "foot.L", "Enabled": True, "Bone": "Foot.L", "StartBone": "UpperLeg.L",
             "MiddleBone": "LowerLeg.L", "UseKneeDirection": False, "TwistWeight": 0.0},
            {"Name": "foot.R", "Enabled": True, "Bone": "Foot.R", "StartBone": "UpperLeg.R",
             "MiddleBone": "LowerLeg.R", "UseKneeDirection": False, "TwistWeight": 0.0},
        ],
        "WeightLists": [{
            "Name": "upper_body", "Enabled": True, "BaseWeight": 0.0,
            "Bones": [
                {"Bone": "Chest", "Weight": 1.0, "Descendants": True},
                {"Bone": "Spine", "Weight": 0.5, "Descendants": False},
            ],
        }],
        "Morphs": [],
        "BodyGroups": [],
        "Folders": ["Ragdoll", "Ponytail", "Tassel", "Body", "Attachments"],
        "CoarseMeshes": [],
        "JiggleBones": jiggles,
        "JiggleColliders": colliders,
        "Hulls": hulls,
        "Attachments": [
            attachment("hand.L", "Hand.L", (0, length_of("Hand.L"), 0)),
            attachment("hand.R", "Hand.R", (0, length_of("Hand.R"), 0)),
            attachment("head", "Head", (0, length_of("Head"), 0)),
            attachment("chest", "Chest", (0, length_of("Chest") * 0.6, 0)),
        ],
        "Bones": [],
        "Constraints": [],
    }


MATERIALS = {
    "body": {"Tint": "0.78,0.58,0.36,1", "Roughness": 0.62},
    "joint": {"Tint": "0.46,0.31,0.19,1", "Roughness": 0.48},
}


def write_materials():
    out = os.path.join(ROOT, "Assets", "materials", "character")
    os.makedirs(out, exist_ok=True)
    for name, over in MATERIALS.items():
        mat = {
            "Shader": "shaders/complex.shader", "Features": {}, "Numbers": {}, "Textures": {},
            "Tint": "1,1,1,1",
            "ColorMap": "materials/default/white.png",
            "Normal": "materials/default/normal.png",
            "RoughMetalAmbient": "materials/default/roughmetal.png",
            "Emission": "materials/default/black.png",
            "Roughness": 0.5, "Metalness": 0.0, "EmissionStrength": 0.0,
            "PhysicsSurface": "", "TwoSided": False, "Filtering": "Smooth",
            "Blend": "Opaque", "AlphaCutoff": 0.5, "__references": [], "__version": 0,
        }
        mat.update(over)
        with open(os.path.join(out, name + ".mat"), "w") as f:
            json.dump(mat, f, indent=2)
            f.write("\n")


def export(armature, body):
    out = os.path.join(ROOT, "Assets", OUT)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, NAME + ".fbx")

    bpy.ops.object.select_all(action="DESELECT")
    armature.select_set(True)
    body.select_set(True)
    bpy.context.view_layer.objects.active = armature

    bpy.ops.export_scene.fbx(
        filepath=path, use_selection=True, object_types={"ARMATURE", "MESH"},
        apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y",
        mesh_smooth_type="FACE", use_mesh_modifiers=False, add_leaf_bones=False,
        bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=True,
        bake_anim_use_all_actions=False, bake_anim_force_startend_keying=True,
        bake_anim_step=1.0, bake_anim_simplify_factor=0.0, path_mode="AUTO")

    with open(os.path.join(out, NAME + ".mdl"), "w") as f:
        json.dump(definition(), f, indent=2)
        f.write("\n")

    return path


def build():
    wipe()
    bpy.context.scene.render.fps = 24
    armature = make_armature()
    body = make_body(armature)
    actions = build_actions(armature)
    stack(armature, actions)
    write_materials()
    path = export(armature, body)
    print(f"[rig] wrote {path}")
    print(f"[rig] {len(BONES)} bones, {len(body.data.vertices)} vertices, "
          f"{len(actions)} takes: {', '.join(actions)}")
    return path


if __name__ == "__main__":
    build()
