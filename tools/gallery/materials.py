#!/usr/bin/env python3
"""Writes the material gallery: the textures it needs (made here, no image
library), the .mat files under materials/gallery, and scenes/Materials.scene
- rows of spheres and slabs, one material property a station."""
import os, sys, json, math, struct, zlib
sys.path.insert(0, os.path.dirname(__file__))
from common import Scene, ROOT, RENDER, v, yaw, pitch_yaw, register_in_menu

S = Scene("materials", "Materials",
          "Roughness against metalness, tint, emission, cutout and translucency, backfaces, every map, every shader, materials changed at runtime, and what a missing asset looks like.")

MAT_DIR = os.path.join(ROOT, "materials/gallery")
TEX_DIR = os.path.join(ROOT, "textures/gallery")
os.makedirs(MAT_DIR, exist_ok=True)
os.makedirs(TEX_DIR, exist_ok=True)

# ---------------------------------------------------------------- textures

def write_png(path, width, height, pixel):
    """A PNG from a function of (x, y) -> (r, g, b, a), no library needed."""
    raw = bytearray()
    for y in range(height):
        raw.append(0)
        for x in range(width):
            raw.extend(pixel(x, y))
    def chunk(kind, data):
        c = struct.pack(">I", len(data)) + kind + data
        return c + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)

def clamp(x): return max(0, min(255, int(round(x))))

def bumps_normal(x, y, size=256, cells=4):
    """Hemispherical bumps: the normal of a dome in each cell, flat between."""
    cell = size / cells
    cx, cy = (x % cell) - cell / 2 + 0.5, (y % cell) - cell / 2 + 0.5
    r = cell * 0.42
    d2 = cx * cx + cy * cy
    if d2 >= r * r:
        return (128, 128, 255, 255)
    nz = math.sqrt(r * r - d2)
    nx, ny = cx / r, -cy / r
    nz /= r
    return (clamp(128 + nx * 127), clamp(128 + ny * 127), clamp(128 + nz * 127), 255)

def gradient(x, y, size=256):
    g = clamp(x / (size - 1) * 255)
    return (g, g, g, 255)

def split(x, y, size=256):
    g = 255 if x >= size // 2 else 0
    return (g, g, g, 255)

def stripes(x, y, size=256):
    on = ((x // 16) + (y // 16)) % 2 == 0
    return (255, 140, 30, 255) if on else (0, 0, 0, 255)

def checker(x, y, size=256):
    on = ((x // 32) + (y // 32)) % 2 == 0
    return (230, 230, 230, 255) if on else (40, 40, 45, 255)

def leaf(x, y, size=256):
    """A leaf shape with a hard alpha edge, for a cutout."""
    u, w = (x - size / 2) / (size / 2), (y - size / 2) / (size / 2)
    inside = (u * u) / 0.55 + (w * w) / 1.0 < 1.0 and not (abs(u) < 0.03 and w > -0.2)
    return (60, 150, 50, 255) if inside else (60, 150, 50, 0)

def ao_rings(x, y, size=256):
    cx, cy = x - size / 2, y - size / 2
    d = math.sqrt(cx * cx + cy * cy) / (size / 2)
    g = clamp(255 * (0.5 + 0.5 * math.cos(d * 12)))
    return (g, g, g, 255)

TEXTURES = {
    "bumps_normal.png": bumps_normal,
    "roughness_gradient.png": gradient,
    "metal_split.png": split,
    "emission_stripes.png": stripes,
    "checker.png": checker,
    "leaf.png": leaf,
    "ao_rings.png": ao_rings,
}
for name, fn in TEXTURES.items():
    write_png(os.path.join(TEX_DIR, name), 256, 256, fn)
print("wrote", len(TEXTURES), "textures")

def tex(name): return f"textures/gallery/{name}"
def flat(r, g, b, a=1.0):
    return "materials/default/colour/" + "".join(f"{clamp(c * 255):02x}" for c in (r, g, b, a)) + ".png"

# ---------------------------------------------------------------- materials

def mat(name, tint="1,1,1,1", rough=0.5, metal=0.0, color="materials/default/white.png", emission="materials/default/black.png",
        emission_strength=0.0, two_sided=False, blend="Opaque", cutoff=0.5, normal="materials/default/normal.png",
        shader="shaders/complex.shader", numbers=None, features=None, textures=None):
    d = {"Shader": shader, "Features": features or {}, "Numbers": numbers or {}, "Textures": textures or {}, "Tint": tint,
         "ColorMap": color, "Normal": normal, "RoughMetalAmbient": "materials/default/roughmetal.png", "Emission": emission,
         "Roughness": rough, "Metalness": metal, "EmissionStrength": emission_strength, "PhysicsSurface": "", "TwoSided": two_sided,
         "Filtering": "Smooth", "Blend": blend, "AlphaCutoff": cutoff, "__references": [], "__version": 0}
    with open(os.path.join(MAT_DIR, name + ".mat"), "w") as f:
        json.dump(d, f, indent=2)
        f.write("\n")
    return f"materials/gallery/{name}.mat"

WARM = "0.9,0.85,0.75,1"
made = 0

# the grid
GRID = {}
for mi, metal in enumerate((0.0, 0.5, 1.0)):
    for ri, rough in enumerate((0.0, 0.25, 0.5, 0.75, 1.0)):
        GRID[(ri, mi)] = mat(f"grid_r{ri}_m{mi}", tint=WARM, rough=rough, metal=metal)

TINT = {
    "red": mat("tint_red", tint="1,0.2,0.2,1"),
    "green": mat("tint_green", tint="0.2,1,0.3,1"),
    "blue": mat("tint_blue", tint="0.3,0.4,1,1"),
    "dark": mat("tint_dark", tint="0.1,0.1,0.12,1"),
    "half": mat("tint_half", tint="1,1,1,0.5"),
    "hdr": mat("tint_hdr", tint="4,4,4,1"),
}

EMISSION = {
    "0.5": mat("emission_05", emission=flat(1, 0.5, 0.1), emission_strength=0.5),
    "2": mat("emission_2", emission=flat(1, 0.5, 0.1), emission_strength=2),
    "8": mat("emission_8", emission=flat(1, 0.5, 0.1), emission_strength=8),
    "cyan": mat("emission_cyan", emission=flat(0.2, 0.9, 1), emission_strength=3, tint="0.1,0.1,0.1,1"),
    "map": mat("emission_map", emission=tex("emission_stripes.png"), emission_strength=3, tint="0.2,0.2,0.2,1"),
    "black": mat("emission_black", emission="materials/default/black.png", emission_strength=8),
}

BLEND = {
    "opaque": mat("blend_opaque", color="textures/fx/ring.png"),
    "cut01": mat("blend_cut_01", color="textures/fx/ring.png", blend="Masked", cutoff=0.1),
    "cut05": mat("blend_cut_05", color="textures/fx/ring.png", blend="Masked", cutoff=0.5),
    "cut09": mat("blend_cut_09", color="textures/fx/ring.png", blend="Masked", cutoff=0.9),
    "leaf": mat("blend_leaf", color=tex("leaf.png"), blend="Masked", cutoff=0.5, two_sided=True),
    "trans02": mat("blend_trans_02", tint="0.4,0.8,1,0.2", blend="Translucent"),
    "trans05": mat("blend_trans_05", tint="0.4,0.8,1,0.5", blend="Translucent"),
    "trans08": mat("blend_trans_08", tint="0.4,0.8,1,0.8", blend="Translucent"),
    "trans2s": mat("blend_trans_2s", tint="1,0.6,0.2,0.4", blend="Translucent", two_sided=True),
    "additive": mat("blend_additive", tint="0.3,1,0.5,0.6", blend="Additive"),
    "transtex": mat("blend_trans_tex", color="textures/fx/ring.png", tint="1,1,1,0.6", blend="Translucent"),
}

SIDES = {
    "one": mat("sides_one", tint="0.9,0.5,0.2,1"),
    "two": mat("sides_two", tint="0.9,0.5,0.2,1", two_sided=True),
}

MAPS = {
    "colour": mat("map_colour", color=tex("checker.png")),
    "grid": mat("map_grid", color="materials/dev/grid.png"),
    "normal": mat("map_normal", normal=tex("bumps_normal.png"), tint=WARM, features={"F_NORMAL_MAP": 1}),
    "normal_metal": mat("map_normal_metal", normal=tex("bumps_normal.png"), metal=1.0, rough=0.3, features={"F_NORMAL_MAP": 1}),
    "rough": mat("map_roughness", metal=1.0, textures={"g_tRoughness": tex("roughness_gradient.png")}, features={"F_ROUGHNESS": 1}),
    "metal": mat("map_metalness", rough=0.2, textures={"g_tMetalness": tex("metal_split.png")}, features={"F_METALNESS": 1}),
    "ao": mat("map_ao", textures={"g_tAO": tex("ao_rings.png")}, features={"F_AO": 1}),
    "all": mat("map_all", color=tex("checker.png"), normal=tex("bumps_normal.png"), emission=tex("emission_stripes.png"), emission_strength=1.5,
               textures={"g_tRoughness": tex("roughness_gradient.png"), "g_tAO": tex("ao_rings.png")},
               features={"F_NORMAL_MAP": 1, "F_ROUGHNESS": 1, "F_AO": 1}),
}

SHADERS = {
    "complex": mat("shader_complex", tint=WARM),
    "glass": mat("shader_glass", shader="shaders/glass.shader", tint="0.7,0.85,1,0.3", blend="Translucent", two_sided=True, rough=0.05),
    "foliage": mat("shader_foliage", shader="shaders/foliage.shader", color=tex("leaf.png"), blend="Masked", two_sided=True,
                   numbers={"g_flWindStrength": "0.4,0,0,0", "g_flWindSpeed": "2,0,0,0", "g_flWindHeight": "1,0,0,0", "g_vWindDirection": "1,0,0.3,0"},
                   features={"F_WIND": 1}),
    "unlit": mat("shader_unlit", shader="shaders/engine/unlit.shader", tint="1,0.6,0.2,1"),
    "vertex_color": mat("shader_vertex_color", shader="shaders/engine/vertex_color.shader"),
    "stylized": mat("shader_stylized", shader="shaders/effects/stylized.shader", numbers={
        "g_vColourA": "0.9,0.3,0.3,1", "g_vColourB": "0.2,0.2,0.6,1", "g_flNoiseScale": "3,0,0,0", "g_flNoiseOctaves": "2,0,0,0", "g_vScrollDirection": "0,0,0,0"}),
    "error": "materials/error.mat",
    "missing": "materials/gallery/does_not_exist.mat",
    "missing_tex": mat("shader_missing_tex", color="textures/gallery/does_not_exist.png"),
    "missing_shader": mat("shader_missing_shader", shader="shaders/does_not_exist.shader", tint=WARM),
    "no_shader": mat("shader_empty", shader="", tint=WARM),
}

SURFACE = {
    "physics": mat("surface_physics", tint="0.5,0.9,0.5,1"),
}

# ---------------------------------------------------------------- stations

PEDESTAL = "0.2,0.22,0.26,1"

def pedestal(name, size=1.2):
    return S.block(f"Pedestal: {name}", (0, 0.1, 0), (size, 0.2, size), PEDESTAL)

def sign(name, text, y=3.0, scale=0.45):
    return S.label(name, (0, y, 0), text, scale=scale, size=44)

def station(name, text, children, pos, sign_y=3.0, pedestal_size=1.2):
    return S.go(f"Station: {name}", pos, children=[pedestal(name, pedestal_size), sign(name, text, sign_y), *children])

def ball(name, material, pos=(0, 0.9, 0), r=0.7, tint="1,1,1,1", extra=()):
    return S.go(f"Ball: {name}", pos, scale=(r, r, r), components=[S.model(f"ball/{name}", tint, material, "models/dev/sphere.mdl"), *extra])

def slab(name, material, pos=(0, 1.1, 0), size=(1.4, 1.4, 0.05), rot="0,0,0,1", tint="1,1,1,1", extra=()):
    return S.go(f"Slab: {name}", pos, rot=rot, scale=size, components=[S.model(f"slab/{name}", tint, material), *extra])

def cube(name, material, pos=(0, 0.7, 0), size=(0.9, 0.9, 0.9), tint="1,1,1,1", rot="0,0,0,1", extra=()):
    return S.go(f"Cube: {name}", pos, rot=rot, scale=size, components=[S.model(f"cube/{name}", tint, material), *extra])

def probe(name, z=0, size=(30, 12, 16)):
    hx, hy, hz = size[0] / 2, size[1] / 2, size[2] / 2
    return S.go(f"Probe: {name}", (0, 3, z), components=[S.comp("Rinten.EnvmapProbe", "probe/" + name, __version=1, BakedTexture=None,
        Bounds={"Mins": v(-hx, -hy, -hz), "Maxs": v(hx, hy, hz)}, DelayBetweenUpdates=0.1, Feathering=0.2, FrameInterval=5, MaxDistance=20,
        Mode="Baked", MultiBounce=False, Priority=0, Projection="Box", RenderExcludeTags="", Resolution="Small", Texture=None,
        TintColor="1,1,1,1", UpdateStrategy="OnEnabled", ZFar=104, ZNear=0.4)])

def row(tag, items, make, spacing, z):
    n = len(items)
    out = []
    for i, item in enumerate(items):
        x = (i - (n - 1) / 2) * spacing
        out.append(make((f"{tag} {item[0]}" if tag else item[0], *item[1:]), (x, 0, z)))
    return out, n * spacing + 8

ROW_DEPTH = 18
areas = []
z = -8

# -- the grid: five roughnesses along, three metalnesses up ------------------
kids = []
for (ri, mi), m in GRID.items():
    x = (ri - 2) * 2.2
    y = 0.9 + mi * 1.7
    kids.append(ball(f"grid {ri} {mi}", m, (x, y, 0), r=0.7))
for ri, rough in enumerate((0.0, 0.25, 0.5, 0.75, 1.0)):
    kids.append(S.label(f"grid rough {ri}", ((ri - 2) * 2.2, 0.15, 0.9), f"rough {rough}", scale=0.3, size=40))
for mi, metal in enumerate((0.0, 0.5, 1.0)):
    kids.append(S.label(f"grid metal {mi}", (-6.6, 0.9 + mi * 1.7, 0), f"metal {metal}", scale=0.3, size=40))
kids.append(S.block("Grid slab", (0, 0.1, 0), (14, 0.2, 3), PEDESTAL))
kids.append(probe("grid"))
areas.append(S.area("Roughness and Metalness", "fifteen spheres: roughness along, metalness up, a box probe over them", z, 34, children=[S.go("Grid", (0, 0, z), children=kids)]))
z -= ROW_DEPTH

# -- tint and emission ---------------------------------------------------------
TINTS = [
    ("Red", "Tint 1, 0.2, 0.2", TINT["red"]), ("Green", "Tint 0.2, 1, 0.3", TINT["green"]), ("Blue", "Tint 0.3, 0.4, 1", TINT["blue"]),
    ("Dark", "Tint 0.1 - nearly black", TINT["dark"]), ("Half alpha", "Tint alpha 0.5, opaque blend\nshould stay solid", TINT["half"]),
    ("HDR tint", "Tint 4, 4, 4\nbloom should catch it", TINT["hdr"]),
    ("Renderer tint", "the material is white\nModelRenderer.Tint is purple", GRID[(2, 0)]),
    ("Both tints", "material tint red\nrenderer tint blue", TINT["red"]),
]
def tint_station(item, pos):
    name, text, m = item
    rt = "1,1,1,1"
    if name.endswith("Renderer tint"): rt = "0.7,0.3,1,1"
    if name.endswith("Both tints"): rt = "0.3,0.4,1,1"
    return station(name, text, [ball(name, m, tint=rt)], pos)
EMISSIONS = [
    ("0.5", "EmissionStrength 0.5", EMISSION["0.5"]), ("2", "EmissionStrength 2", EMISSION["2"]), ("8", "EmissionStrength 8", EMISSION["8"]),
    ("Cyan", "cyan emission on a dark tint", EMISSION["cyan"]), ("Map", "emission from a striped map", EMISSION["map"]),
    ("Black map", "strength 8, black map\nshould not glow", EMISSION["black"]),
]
def tint_or_emission(item, pos):
    if item[0].startswith("Tint "): return tint_station(item, pos)
    return station(item[0], item[1], [ball(item[0], item[2])], pos)
kids, width = row("", [("Tint " + n, t, m) for n, t, m in TINTS] + [("Emission " + n, t, m) for n, t, m in EMISSIONS], tint_or_emission, 3.6, z)
areas.append(S.area("Tint and Emission", "material tint against renderer tint; emission strengths, colours and a map", z, width, children=kids))
z -= ROW_DEPTH

# -- blending ------------------------------------------------------------------
BLENDS = [
    ("Opaque", "ring.png, Opaque\nthe alpha is ignored", BLEND["opaque"], "slab"),
    ("Cutoff 0.1", "Masked, AlphaCutoff 0.1", BLEND["cut01"], "slab"),
    ("Cutoff 0.5", "Masked, AlphaCutoff 0.5", BLEND["cut05"], "slab"),
    ("Cutoff 0.9", "Masked, AlphaCutoff 0.9", BLEND["cut09"], "slab"),
    ("Leaf", "a cutout leaf, two-sided", BLEND["leaf"], "slab"),
    ("Translucent 0.2", "Translucent, alpha 0.2", BLEND["trans02"], "ball"),
    ("Translucent 0.5", "Translucent, alpha 0.5", BLEND["trans05"], "ball"),
    ("Translucent 0.8", "Translucent, alpha 0.8", BLEND["trans08"], "ball"),
    ("Two-sided glass", "Translucent, two-sided\nthe far side should show", BLEND["trans2s"], "ball"),
    ("Additive", "Blend Additive", BLEND["additive"], "ball"),
    ("Textured", "ring.png, Translucent at 0.6", BLEND["transtex"], "slab"),
]
def blend_station(item, pos):
    name, text, m, kind = item
    thing = ball(name, m) if kind == "ball" else slab(name, m)
    behind = cube(f"{name} behind", GRID[(2, 0)], pos=(0, 0.7, -0.9), size=(0.5, 1.2, 0.5), tint="1,0.5,0.2,1")
    return station(name, text, [thing, behind], pos)
kids, width = row("Blend", BLENDS, blend_station, 3.6, z)
# sorting: three translucent slabs one behind the other, and a translucent ball in front of an opaque cube
x0 = width / 2 + 2
kids.append(station("Sorting", "three translucent slabs, front to back\nblue, green, red - all three should show", [
    slab("Sort A", BLEND["trans05"], (0, 1.1, 0.6), tint="0.3,0.4,1,1"), slab("Sort B", BLEND["trans05"], (0, 1.1, 0.0), tint="0.3,1,0.4,1"),
    slab("Sort C", BLEND["trans05"], (0, 1.1, -0.6), tint="1,0.3,0.3,1")], (x0, 0, z)))
kids.append(station("Inside", "a translucent ball around an opaque cube", [
    ball("Inside ball", BLEND["trans05"], r=1.0), cube("Inside cube", TINT["red"], pos=(0, 0.9, 0), size=(0.4, 0.4, 0.4))], (x0 + 4, 0, z)))
areas.append(S.area("Blending", "opaque, cutout at three cutoffs, translucent at three alphas, two-sided, additive, sorting", z, width + 12, children=kids))
z -= ROW_DEPTH

# -- sides and surfaces --------------------------------------------------------
# plane.mdl lies flat, facing up: stood on edge with a quarter turn about X,
# its face is toward +Z - the spawn - or away from it.
FRONT = "0.7071068,0,0,0.7071068"
BACK = "-0.7071068,0,0,0.7071068"
SIDE = [
    ("One-sided front", "a plane facing you, one-sided", SIDES["one"], FRONT),
    ("One-sided back", "the same plane turned round\nyou see through it", SIDES["one"], BACK),
    ("Two-sided back", "turned round, two-sided\nlit from behind", SIDES["two"], BACK),
    ("Edge on", "a plane edge-on", SIDES["two"], pitch_yaw(90, 90)),
    ("Flat", "a plane lying flat, as the model comes", SIDES["one"], "0,0,0,1"),
]
def side_station(item, pos):
    name, text, m, rot = item
    return station(name, text, [S.go(f"Plane: {name}", (0, 1.1, 0), rot=rot, scale=(1.4, 1.4, 1), components=[S.model(f"plane/{name}", "1,1,1,1", m, "models/dev/plane.mdl")])], pos)
kids, width = row("Side", SIDE, side_station, 3.6, z)
x0 = width / 2 + 2
kids.append(station("Hollow", "one-sided sphere, camera can go in\nthe inside is invisible", [ball("Hollow", SIDES["one"], r=2.0, pos=(0, 2.0, 0))], (x0, 0, z), pedestal_size=0.5))
kids.append(station("Two-sided hollow", "two-sided sphere\nthe inside is a wall", [ball("Hollow 2", SIDES["two"], r=2.0, pos=(0, 2.0, 0))], (x0 + 5, 0, z), pedestal_size=0.5))
kids.append(station("Tiled", "grid on a 6 x 1 x 1 cube\nthe texture stretches with the scale", [cube("Tiled", MAPS["grid"], pos=(0, 0.7, 0), size=(6, 1, 1))], (x0 + 11, 0, z)))
kids.append(station("Thin", "a 0.01 thick slab, both faces", [slab("Thin", MAPS["grid"], size=(1.4, 1.4, 0.01))], (x0 + 16, 0, z)))
areas.append(S.area("Sides and Surfaces", "one-sided and two-sided planes and spheres, texture over scale, a thin slab", z, width + 22, children=kids))
z -= ROW_DEPTH

# -- maps ----------------------------------------------------------------------
MAP = [
    ("Colour", "a checker colour map", MAPS["colour"]),
    ("Grid", "the dev grid", MAPS["grid"]),
    ("Normal", "hemispherical bumps normal map\nthe light should catch them", MAPS["normal"]),
    ("Normal metal", "the same bumps, metal 1, rough 0.3", MAPS["normal_metal"]),
    ("Roughness map", "roughness 0 to 1 left to right\nmetal 1", MAPS["rough"]),
    ("Metalness map", "metal 0 left, 1 right", MAPS["metal"]),
    ("AO map", "rings of ambient occlusion", MAPS["ao"]),
    ("All maps", "colour, normal, roughness, AO, emission", MAPS["all"]),
]
kids, width = row("Map", MAP, lambda it, p: station(it[0], it[1], [ball(it[0], it[2], (-0.7, 0.9, 0), r=0.7), slab(f"{it[0]} slab", it[2], (0.7, 0.9, 0), size=(1.2, 1.2, 0.05))], p), 4.0, z)
kids.append(probe("maps", z))
areas.append(S.area("Maps", "colour, normal, roughness, metalness, ambient occlusion, emission - a ball and a slab each", z, width, children=kids))
z -= ROW_DEPTH

# -- shaders -------------------------------------------------------------------
SHADER = [
    ("Complex", "shaders/complex.shader\nthe standard one", SHADERS["complex"], "ball"),
    ("Glass", "shaders/glass.shader\ntranslucent, two-sided, rough 0.05", SHADERS["glass"], "ball"),
    ("Foliage", "shaders/foliage.shader\ncutout leaf with F_WIND", SHADERS["foliage"], "slab"),
    ("Unlit", "shaders/engine/unlit.shader\nno lighting at all", SHADERS["unlit"], "ball"),
    ("Vertex colour", "shaders/engine/vertex_color.shader\nthe dev models carry none", SHADERS["vertex_color"], "ball"),
    ("Stylized", "shaders/effects/stylized.shader\ntwo colours and noise from Numbers", SHADERS["stylized"], "ball"),
    ("Error material", "materials/error.mat", SHADERS["error"], "ball"),
    ("Missing material", "a .mat that does not exist", SHADERS["missing"], "ball"),
    ("Missing texture", "a colour map that does not exist", SHADERS["missing_tex"], "ball"),
    ("Missing shader", "a shader that does not exist", SHADERS["missing_shader"], "ball"),
    ("No shader", "Shader left empty\nshould be the standard one", SHADERS["no_shader"], "ball"),
    ("No override", "MaterialOverride null\nthe model's own material", None, "ball"),
]
def shader_station(item, pos):
    name, text, m, kind = item
    thing = ball(name, m) if kind == "ball" else slab(name, m)
    return station(name, text, [thing], pos)
kids, width = row("Shader", SHADER, shader_station, 3.8, z)
areas.append(S.area("Shaders", "every shader the project can name, and what a missing material, texture or shader looks like", z, width, children=kids))
z -= ROW_DEPTH

# -- runtime -------------------------------------------------------------------
def probe_comp(name, what, a, b=None, period=4.0):
    return S.comp("TestGround.MaterialProbe", "probe/" + name, What=what, A=a, B=b, Period=period)
RUNTIME = [
    ("Renderer tint", "ModelRenderer.Tint cycles hue", "Tint", GRID[(2, 0)], None),
    ("Roughness", "a copied material, Roughness swept 0..1", "Roughness", GRID[(0, 2)], None),
    ("Material tint", "a copied material, its Tint cycled", "MaterialTint", GRID[(2, 0)], None),
    ("Swap", "MaterialOverride flips red / blue", "Swap", TINT["red"], TINT["blue"]),
    ("Accessor", "Materials.SetOverride( 0 ) flips", "Accessor", TINT["green"], TINT["dark"]),
    ("Setter", "IMaterialSetter.SetMaterial flips", "Setter", MAPS["grid"], MAPS["colour"]),
]
def runtime_station(item, pos):
    name, text, what, a, b = item
    return station(name, text, [ball(name, a, extra=[probe_comp(name, what, a, b)])], pos)
kids, width = row("Runtime", RUNTIME, runtime_station, 4.0, z)
x0 = width / 2 + 2
kids.append(station("Shared", "two balls, one material\ntint on the left renderer only", [
    ball("Shared A", GRID[(2, 0)], (-0.6, 0.9, 0), r=0.6, tint="1,0.3,0.3,1"), ball("Shared B", GRID[(2, 0)], (0.6, 0.9, 0), r=0.6)], (x0, 0, z)))
kids.append(station("Shared copy", "the right one is a copy with Roughness swept\nthe left must not change", [
    ball("Shared copy A", GRID[(0, 2)], (-0.6, 0.9, 0), r=0.6), ball("Shared copy B", GRID[(0, 2)], (0.6, 0.9, 0), r=0.6, extra=[probe_comp("shared copy", "Roughness", GRID[(0, 2)])])], (x0 + 4, 0, z)))
kids.append(probe("runtime", z))
areas.append(S.area("Runtime", "materials changed while the scene runs: tint, copies, swaps, the accessor, the setter, and what is shared", z, width + 10, children=kids))

# ---------------------------------------------------------------- the scene

S.objects = [
    S.environment(sun_brightness=1.4),
    S.block("Ground", (0, -0.6, -60), (200, 0.5, 180), "0.2,0.21,0.24,1"),
    S.go("Areas", children=areas),
    S.player((0, 2.6, 14)),
    S.hud("Seven rows: the roughness-metalness grid, tint and emission, blending, sides, maps, shaders, runtime changes. Q returns."),
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

S.write("Materials.scene")
register_in_menu("materials.scene", "Materials", "Rendering",
                 "Roughness against metalness, tint, emission, cutout and translucency, backfaces, maps, shaders, runtime changes, missing assets")
