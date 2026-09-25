#!/usr/bin/env python3
"""What the engine will actually see in an fbx skeleton, read through the same
ufbx it reads with - the rn_fbx_* shim in rintencore, called straight from here.

    python3 tools/character/probe.py Assets/models/character/mannequin.fbx [bones...]

Each row is a bone's rest in the engine's own space (Y-up, metres): where it
stands, and its three local axes as directions in model space. That last part
is the answer to the only question a .mdl cannot be written without - which way
a bone points in its own space, because that is the space hulls, attachments
and jiggle offsets are written in. For this rig it is +Y, the same as Blender's:
the export turns the armature and leaves the bone frames alone.

Point it at any fbx, not just this one. A character whose limbs collide in the
wrong place is this listing disagreeing with what the .mdl assumed.
"""
import ctypes, sys, os

LIB = os.environ.get("RINTENCORE",
    os.path.expanduser("~/Documents/Rinten-Engine/game/bin/linuxsteamrt64/rintencore.so"))
path = sys.argv[1]

lib = ctypes.CDLL(LIB)
lib.rn_fbx_load.restype = ctypes.c_void_p
lib.rn_fbx_load.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
lib.rn_fbx_node_count.argtypes = [ctypes.c_void_p]
lib.rn_fbx_node_name.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
lib.rn_fbx_node_parent.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.rn_fbx_node_flags.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.rn_fbx_deformer_count.argtypes = [ctypes.c_void_p]
lib.rn_fbx_cluster_count.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.rn_fbx_cluster_node.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
lib.rn_fbx_cluster_inverse_bind.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float)]

err = ctypes.create_string_buffer(512)
scene = lib.rn_fbx_load(path.encode(), err, 512)
if not scene:
    print("failed:", err.value)
    sys.exit(1)


def name(i):
    buf = ctypes.create_string_buffer(256)
    lib.rn_fbx_node_name(scene, i, buf, 256)
    return buf.value.decode()


def invert(m):
    """Invert a rigid 4x4 given row-major with translation in the last row."""
    r = [m[0:3], m[4:7], m[8:11]]
    t = m[12:15]
    # rest = inverse of (R, t) where p_world = p_local * R + t
    rt = [[r[0][0], r[1][0], r[2][0]], [r[0][1], r[1][1], r[2][1]], [r[0][2], r[1][2], r[2][2]]]
    # inverse rotation is the transpose of R for a rigid matrix; here m is the
    # inverse bind, so inverting it gives the rest.
    pos = [-(t[0] * rt[0][0] + t[1] * rt[1][0] + t[2] * rt[2][0]),
           -(t[0] * rt[0][1] + t[1] * rt[1][1] + t[2] * rt[2][1]),
           -(t[0] * rt[0][2] + t[1] * rt[1][2] + t[2] * rt[2][2])]
    # rows of the rest rotation are the bone's local axes in model space
    return rt, pos


deformers = lib.rn_fbx_deformer_count(scene)
print(f"deformers: {deformers}")
want = set(sys.argv[2:]) if len(sys.argv) > 2 else None
for d in range(deformers):
    for c in range(lib.rn_fbx_cluster_count(scene, d)):
        node = lib.rn_fbx_cluster_node(scene, d, c)
        n = name(node)
        if want and n not in want:
            continue
        out = (ctypes.c_float * 16)()
        lib.rn_fbx_cluster_inverse_bind(scene, d, c, out)
        m = list(out)
        rt, pos = invert(m)
        # rt rows: the bone's local x, y, z axes expressed in model space.
        fmt = lambda v: "(" + ",".join(f"{x:+.3f}" for x in v) + ")"
        print(f"{n:12s} pos={fmt(pos)}  x={fmt(rt[0])} y={fmt(rt[1])} z={fmt(rt[2])}")
