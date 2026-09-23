# The bow, the arrow and the target for the VR lab, built from numbers.
#
# Run inside Blender (the Blender MCP, or `blender -b -P build_archery.py`):
# each asset is made here, exported as FBX with its .mdl, .mat files and
# pictures into Assets/models/vr/archery/<asset>/.
#
# Blender is Z up and the exports say -Z forward, Y up, so a Blender +Y is the
# engine's forward (-Z) and Blender (x, y, z) lands at engine (x, z, -y). Every
# asset shoots or faces along Blender +Y:
#
#   bow     origin at the grip. Vertical, the string towards the archer (-Y).
#           One morph, "draw": the limbs bend back and the string's nocking
#           point goes back to full draw. The string is a mesh like the rest -
#           each of its vertices sits on the straight line between the tips at
#           rest and on the V through the nocking point at full draw, so every
#           weight between is a straight V too and nothing else draws it.
#   arrow   origin at the nock, the point forward.
#   target  origin at the centre of the face, which looks back at the archer.
#           Ring radii are in RINGS, for scoring.
#
# Positions the game needs are attachments in each .mdl - see ATTACHMENTS.
import bpy, bmesh, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, "..", ".."))
REL = "models/vr/archery"
OUT = os.path.join(PROJECT, "Assets", REL)

# -- the bow's numbers, in metres -----------------------------------------------

HALF = 0.75            # grip to tip
RISER = 0.10           # half the riser's length
NOCK_Z = 0.06          # nocking point's height above the grip: level with the rest
DRAW = 0.70            # how far behind the grip the nock is at full draw
TIP_S = 0.97           # where along the limb the string is tied
STRING_RADIUS = 0.0015


def limb_s(a):
    """How far along the limb a height is, 0 at the riser, 1 at the tip."""
    return max(0.0, (a - RISER) / (HALF - RISER))


def bow_centre(z, drawn):
    """The bow's centre line at a height: (y, z). Drawn bends it back and in."""
    a = abs(z)
    s = limb_s(a)
    y = -0.21 * s ** 1.7 + 0.025 * s ** 8
    if drawn:
        y += -0.12 * s ** 2
        z = math.copysign(a - 0.05 * s ** 2.5, z)
    return y, z


def bow_section(z):
    """Width (x) and thickness (y) at a height."""
    a = abs(z)
    if a < RISER:
        return 0.034, 0.040
    s = limb_s(a)
    blend = min(1.0, (a - RISER) / 0.06)  # the riser eases into the limb
    width = 0.034 + (0.012 - 0.034) * s
    thick = 0.040 + (0.020 - 0.040) * blend + (0.009 - 0.020) * s
    return width, thick


def string_tie(sign, drawn):
    """Where the string is tied at a tip, on the archer's side of the limb."""
    z = sign * (RISER + TIP_S * (HALF - RISER))
    y, zz = bow_centre(z, drawn)
    return (0.0, y - bow_section(z)[1] * 0.5, zz)


def nock_point(drawn):
    top = string_tie(1, False)
    return (0.0, -DRAW if drawn else top[1], NOCK_Z)


# -- building ---------------------------------------------------------------------

def clear():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
        for d in list(coll):
            if d.users == 0:
                coll.remove(d)


def material(name, colour, picture=None, rough=0.6, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*colour, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if picture:
        img = bpy.data.images.load(picture, check_existing=True)
        tex = m.node_tree.nodes.new("ShaderNodeTexImage")
        tex.image = img
        m.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    m["rinten"] = {"colour": colour, "picture": picture or "", "rough": rough, "metal": metal}
    return m


def mesh_object(name, verts, faces, uvs=None, mat=None, smooth=True):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    if uvs:
        layer = me.uv_layers.new(name="UVMap")
        for poly in me.polygons:
            for li in poly.loop_indices:
                layer.data[li].uv = uvs[me.loops[li].vertex_index]
    me.update()
    if smooth:
        me.shade_smooth()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    if mat:
        o.data.materials.append(mat)
    return o


def sweep(centres, sections, sides, close_ends=True, u_scale=1.0):
    """
    A tube along a path: centres[i] a point, sections[i] (half_x, half_y) of an
    ellipse in the plane across the path's local tangent. UV u around, v along.
    """
    verts, faces, uvs = [], [], []
    n = len(centres)
    length = [0.0]
    for i in range(1, n):
        d = [centres[i][k] - centres[i - 1][k] for k in range(3)]
        length.append(length[-1] + math.sqrt(sum(c * c for c in d)))
    for i, (c, (hx, hy)) in enumerate(zip(centres, sections)):
        a = centres[max(0, i - 1)]
        b = centres[min(n - 1, i + 1)]
        t = np.array(b) - np.array(a)
        t /= np.linalg.norm(t)
        x = np.array([1.0, 0.0, 0.0])
        y = np.cross(t, x)
        y /= np.linalg.norm(y)
        for j in range(sides + 1):
            ang = 2 * math.pi * j / sides
            p = np.array(c) + x * math.cos(ang) * hx + y * math.sin(ang) * hy
            verts.append(tuple(p))
            uvs.append((j / sides * u_scale, length[i]))
    ring = sides + 1
    for i in range(n - 1):
        for j in range(sides):
            a0 = i * ring + j
            faces.append((a0, a0 + 1, a0 + ring + 1, a0 + ring))
    if close_ends:
        for i, flip in ((0, True), (n - 1, False)):
            centre = len(verts)
            verts.append(tuple(centres[i]))
            uvs.append((0.5, length[i]))
            for j in range(sides):
                a0, a1 = i * ring + j, i * ring + j + 1
                faces.append((centre, a1, a0) if flip else (centre, a0, a1))
    return verts, faces, uvs


# -- pictures ---------------------------------------------------------------------

def save_picture(name, rgb):
    h, w, _ = rgb.shape
    img = bpy.data.images.new(name, w, h, alpha=False)
    rgba = np.ones((h, w, 4), dtype=np.float32)
    rgba[..., :3] = np.clip(rgb, 0, 1)
    img.pixels.foreach_set(rgba.ravel())
    path = os.path.join(OUT_ASSET, f"{name}.png")
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()
    return path


def wood_picture(name, base, dark, seed):
    """Grain along v, which is along the stave."""
    rng = np.random.default_rng(seed)
    h, w = 512, 128
    v = np.linspace(0, 1, h)[:, None]
    u = np.linspace(0, 1, w)[None, :]
    wobble = sum(rng.uniform(0.002, 0.01) * np.sin(2 * np.pi * (rng.integers(1, 6) * v + rng.random()))
                 for _ in range(4))
    streaks = 0.5 + 0.5 * np.sin(2 * np.pi * (u * 9 + wobble * 40))
    fine = rng.random((h, w)) * 0.15
    t = np.clip(streaks * 0.6 + fine, 0, 1)[..., None]
    rgb = np.array(base)[None, None, :] * (1 - t) + np.array(dark)[None, None, :] * t
    return save_picture(name, rgb)


# The target's rings, from the outside in, as (radius, colour, score) - a
# six-ring 80 cm face: blue 5 and 6, red 7 and 8, yellow 9 and 10, and the inner
# ten (X) half the ten.
FACE_RADIUS = 0.40
BLUE, RED, YELLOW = (0.0, 0.62, 0.87), (0.89, 0.12, 0.14), (1.0, 0.92, 0.0)
RINGS = [(FACE_RADIUS * (6 - i) / 6, c, 5 + i)
         for i, c in enumerate((BLUE, BLUE, RED, RED, YELLOW, YELLOW))]
RINGS.append((FACE_RADIUS / 12, YELLOW, 11))  # X


def face_picture(name):
    size = 1024
    ax = (np.arange(size) + 0.5) / size * 2 - 1
    r = np.sqrt(ax[None, :] ** 2 + ax[:, None] ** 2) * FACE_RADIUS
    rgb = np.ones((size, size, 3)) * np.array(BLUE)
    for radius, colour, _ in RINGS:
        rgb[r <= radius] = colour
    # The lines between rings: black between colours, thinner inside a colour.
    px = FACE_RADIUS * 2 / size
    for i, (radius, _, score) in enumerate(RINGS):
        line = 1.6 * px if score in (5, 7, 9) else 0.8 * px
        rgb[np.abs(r - radius) < line] = (0.05, 0.05, 0.05)
    # The centre cross.
    c = np.abs(ax) * FACE_RADIUS
    cross = ((c[None, :] < 0.004) & (c[:, None] < px * 0.6)) | ((c[:, None] < 0.004) & (c[None, :] < px * 0.6))
    rgb[cross] = (0.05, 0.05, 0.05)
    return save_picture(name, rgb[::-1])


# -- the assets -------------------------------------------------------------------

def build_bow():
    wood = material("bow_wood", (1, 1, 1), wood_picture("bow_wood", (0.80, 0.62, 0.38), (0.55, 0.37, 0.18), 3), rough=0.55)
    wrap = material("bow_grip", (0.10, 0.20, 0.24), rough=0.85)
    string = material("bow_string", (0.08, 0.08, 0.08), rough=0.7)

    steps = 121
    zs = [-HALF + 2 * HALF * i / (steps - 1) for i in range(steps)]

    def stave(drawn):
        centres, sections = [], []
        for z in zs:
            y, zz = bow_centre(z, drawn)
            centres.append((0.0, y, zz))
            w, t = bow_section(z)
            sections.append((w * 0.5, t * 0.5))
        return sweep(centres, sections, 12, u_scale=0.1)

    v0, f, uv = stave(False)
    v1, _, _ = stave(True)
    body = mesh_object("bow", v0, f, uv, wood)
    parts = [(body, v1)]

    # The leather wrap on the grip; the riser does not bend, so it has no draw.
    wz = [-0.055 + 0.11 * i / 10 for i in range(11)]
    v, f, uv = sweep([(0, 0, z) for z in wz], [(0.0195, 0.0225)] * len(wz), 16, u_scale=0.2)
    parts.append((mesh_object("bow_grip", v, f, uv, wrap), v))

    # The shelf the arrow lies on, on the left of the riser.
    v, f = [], []
    x0, x1, y0, y1, z0, z1 = -0.030, -0.012, -0.012, 0.012, NOCK_Z - 0.012, NOCK_Z - 0.006
    for x in (x0, x1):
        for y in (y0, y1):
            for z in (z0, z1):
                v.append((x, y, z))
    f = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    parts.append((mesh_object("bow_rest", v, f, None, wrap, smooth=False), v))

    # The string: tie, nocking point, tie - a vertex ring at each end of each half
    # and many between, so a V at any weight is straight on both sides.
    def string_path(drawn):
        top, bottom, nock = string_tie(1, drawn), string_tie(-1, drawn), nock_point(drawn)
        pts = []
        for a, b, n in ((top, nock, 40), (nock, bottom, 40)):
            for i in range(n + (1 if b is bottom else 0)):
                t = i / n
                pts.append(tuple(a[k] + (b[k] - a[k]) * t for k in range(3)))
        return pts

    rest_path, drawn_path = string_path(False), string_path(True)
    rs = [(STRING_RADIUS, STRING_RADIUS)] * len(rest_path)
    v0, f, uv = sweep(rest_path, rs, 6)
    v1, _, _ = sweep(drawn_path, rs, 6)
    parts.append((mesh_object("bow_string", v0, f, uv, string), v1))

    for obj, drawn in parts:
        obj.shape_key_add(name="Basis", from_mix=False)
        key = obj.shape_key_add(name="draw", from_mix=False)
        for i, co in enumerate(drawn):
            key.data[i].co = co

    bow = join(parts[0][0], [p[0] for p in parts], "archery_bow", outward=True)
    return bow, {
        "Morphs": ["draw"],
        # Where the hand holds it, where the arrow lies, and where it is nocked
        # at rest and at full draw - in Blender's space, turned on the way out.
        "Attachments": [
            ("grip", (0, 0, 0)),
            ("arrow_rest", (-0.021, 0, NOCK_Z - 0.002)),
            ("nock_rest", nock_point(False)),
            ("nock_drawn", nock_point(True)),
        ],
    }


def build_arrow():
    wood = material("arrow_shaft", (1, 1, 1), wood_picture("arrow_shaft", (0.86, 0.72, 0.50), (0.68, 0.52, 0.32), 7), rough=0.6)
    point = material("arrow_point", (0.05, 0.05, 0.05), rough=0.35, metal=1.0)
    red = material("arrow_red", (0.85, 0.10, 0.08), rough=0.5)
    yellow = material("arrow_yellow", (0.98, 0.80, 0.05), rough=0.5)

    length = 0.78
    objs = []
    ys = [0.012 + (length - 0.04 - 0.012) * i / 20 for i in range(21)]
    v, f, uv = sweep([(0, y, 0) for y in ys], [(0.004, 0.004)] * len(ys), 12, u_scale=0.05)
    objs.append(mesh_object("arrow_shaft", v, f, uv, wood))

    # The point: a cone ahead of the shaft.
    ys = [length - 0.04 + 0.04 * i / 6 for i in range(7)]
    rs = [0.0048 * (1 - i / 6) ** 0.8 + 0.0002 for i in range(7)]
    v, f, uv = sweep([(0, y, 0) for y in ys], [(r, r) for r in rs], 12)
    objs.append(mesh_object("arrow_point", v, f, uv, point))

    # The nock: a red cap with the slot the string sits in.
    ys = [0.0, 0.004, 0.012, 0.016]
    rs = [0.0042, 0.0046, 0.0046, 0.004]
    v, f, uv = sweep([(0, y, 0) for y in ys], [(r, r) for r in rs], 12)
    objs.append(mesh_object("arrow_nock", v, f, uv, red))

    # Three vanes, a third of a turn apart: the cock vane red, pointing up.
    for k, colour in enumerate((red, yellow, yellow)):
        ang = math.pi / 2 + k * 2 * math.pi / 3
        out = (math.cos(ang), 0, math.sin(ang))
        side = (-math.sin(ang), 0, math.cos(ang))
        v, f = [], []
        n = 10
        for i in range(n + 1):
            t = i / n
            y = 0.03 + 0.085 * t
            height = 0.013 * math.sin(math.pi * min(1.0, t * 1.25) * 0.5) * (1 - 0.35 * t ** 3)
            for h in (0.0035, 0.0035 + max(height, 0.0005)):
                for s in (-0.0005, 0.0005):
                    v.append((out[0] * h + side[0] * s, y, out[2] * h + side[2] * s))
        for i in range(n):
            a = i * 4
            f += [(a, a + 4, a + 6, a + 2), (a + 1, a + 3, a + 7, a + 5),
                  (a + 2, a + 6, a + 7, a + 3), (a, a + 1, a + 5, a + 4)]
        f += [(0, 2, 3, 1), (n * 4, n * 4 + 1, n * 4 + 3, n * 4 + 2)]
        objs.append(mesh_object(f"arrow_vane{k}", v, f, None, colour, smooth=False))

    arrow = join(objs[0], objs, "archery_arrow", outward=True)
    return arrow, {
        "Morphs": [],
        "Attachments": [("nock", (0, 0.002, 0)), ("tip", (0, length, 0))],
    }


def build_target():
    face = material("target_face", (1, 1, 1), face_picture("target_face"), rough=0.9)
    straw = material("target_straw", (0.78, 0.66, 0.38), rough=1.0)

    sides = 96
    depth = 0.12
    objs = []

    # The face: a disc at y = 0 looking back along -Y, the picture on it flat.
    v, f, uv = [(0, 0, 0)], [], [(0.5, 0.5)]
    for j in range(sides):
        a = 2 * math.pi * j / sides
        v.append((FACE_RADIUS * math.cos(a), 0, FACE_RADIUS * math.sin(a)))
        uv.append((0.5 + 0.5 * math.cos(a), 0.5 + 0.5 * math.sin(a)))
    for j in range(sides):
        f.append((0, 1 + j, 1 + (j + 1) % sides))  # facing -Y, at the archer
    objs.append(mesh_object("target_face", v, f, uv, face, smooth=False))

    # The boss behind it: a straw drum, rim and back.
    v, f, uv = [], [], []
    for j in range(sides + 1):
        a = 2 * math.pi * j / sides
        for y in (0.0005, depth):
            v.append((FACE_RADIUS * math.cos(a), y, FACE_RADIUS * math.sin(a)))
            uv.append((j / sides * 4, y * 4))
    for j in range(sides):
        a = j * 2
        f.append((a, a + 1, a + 3, a + 2))  # outwards
    back = len(v)
    v.append((0, depth, 0))
    uv.append((0.5, 0.5))
    for j in range(sides):
        f.append((back, (j + 1) * 2 + 1, j * 2 + 1))  # facing +Y, away
    rim = mesh_object("target_straw", v, f, uv, straw, smooth=False)
    objs.append(rim)

    target = join(objs[0], objs, "archery_target")
    return target, {
        "Morphs": [],
        "Attachments": [("centre", (0, 0, 0))],
        "Rings": [{"Score": s if s <= 10 else "X", "Radius": round(r, 4)} for r, _, s in RINGS],
    }


def join(active, objs, name, outward=False):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = active
    bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    obj.data.name = name
    if outward:
        # Every part is closed, so outward is well defined; the sweeps' winding
        # is whatever their frames made it.
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(obj.data)
        bm.free()
    return obj


# -- writing ----------------------------------------------------------------------

def blender_to_engine(p):
    return (p[0], p[2], -p[1])


def fmt(v):
    return ",".join(f"{c:.4f}".rstrip("0").rstrip(".") if c else "0" for c in v)


def write(asset, obj, info):
    fbx = os.path.join(OUT_ASSET, f"{asset}.fbx")
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, object_types={"MESH"},
                             use_mesh_modifiers=True, add_leaf_bones=False, bake_anim=False,
                             path_mode="STRIP", embed_textures=False, use_metadata=False,
                             axis_forward="-Z", axis_up="Y")

    mats, remaps = [], []
    for slot in obj.material_slots:
        m = slot.material
        props = m["rinten"].to_dict()
        path = f"{REL}/{asset}/{m.name}.mat"
        picture = props.get("picture")
        body = {
            "Shader": "shaders/complex.shader",
            "Tint": ",".join(str(round(c, 4)) for c in list(props["colour"]) + [1.0]),
            "ColorMap": f"{REL}/{asset}/{os.path.basename(picture)}" if picture else "",
            "Normal": "", "RoughMetalAmbient": "", "Emission": "",
            "Roughness": props["rough"], "Metalness": props["metal"], "EmissionStrength": 0.0,
            "TwoSided": False, "Blend": "Opaque", "AlphaCutoff": 0.5,
        }
        with open(os.path.join(PROJECT, "Assets", path), "w") as f:
            f.write(json.dumps(body, indent=2) + "\n")
        mats.append(path)
        remaps.append({"Surface": m.name, "Material": path})

    mdl = {
        "Steps": [],
        "Meshes": [{"Name": "", "File": f"{REL}/{asset}/{asset}.fbx", "Scale": 1, "Include": [], "Enabled": True,
                    "Position": "0,0,0", "Rotation": "0,0,0", "Parent": ""}],
        "Scale": 1, "Material": "", "Materials": mats, "MaterialRemaps": remaps, "Clips": [],
        "Transform": {"Enabled": True, "Position": "0,0,0", "Rotation": "0,0,0", "Scale": "1,1,1", "IsIdentity": True},
        "Mirror": {"Enabled": False, "Axis": "X", "FlipWinding": True, "RemapLeftRight": True},
        "Joints": [], "LookAtChains": [], "IkChains": [], "WeightLists": [],
        "Morphs": [{"Name": n, "Enabled": True, "Preview": 0} for n in info["Morphs"]],
        "BodyGroups": [], "Folders": [], "CoarseMeshes": [], "MaterialGroups": [], "Hulls": [],
        "Surface": "", "Mass": 0, "OverrideBounds": False,
        "Bounds": {"Mins": "-64,-64,-64", "Maxs": "64,64,64"},
        "JiggleBones": [], "JiggleColliders": [],
        "Attachments": [{"Name": n, "Enabled": True, "Parent": "", "Position": fmt(blender_to_engine(p)), "Rotation": "0,0,0"}
                        for n, p in info["Attachments"]],
        "Bones": [], "Constraints": [], "__references": [], "__version": 2,
    }
    with open(os.path.join(OUT_ASSET, f"{asset}.mdl"), "w") as f:
        f.write(json.dumps(mdl, indent=2) + "\n")

    if "Rings" in info:
        with open(os.path.join(OUT_ASSET, "rings.json"), "w") as f:
            f.write(json.dumps(info["Rings"], indent=2) + "\n")


OUT_ASSET = OUT


def main(which=("bow", "arrow", "target")):
    global OUT_ASSET
    built = {}
    for asset in which:
        OUT_ASSET = os.path.join(OUT, asset)
        os.makedirs(OUT_ASSET, exist_ok=True)
        clear()
        obj, info = {"bow": build_bow, "arrow": build_arrow, "target": build_target}[asset]()
        write(asset, obj, info)
        built[asset] = {"verts": len(obj.data.vertices), "materials": [s.material.name for s in obj.material_slots],
                        "keys": [k.name for k in obj.data.shape_keys.key_blocks] if obj.data.shape_keys else []}
    return built


if __name__ == "__main__":
    main()
