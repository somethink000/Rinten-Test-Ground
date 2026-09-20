#!/usr/bin/env python3
"""Procedural jungle textures and the .mat files that wear them.

Albedo, tangent normals and roughness, written under Assets/textures/jungle
and Assets/materials/jungle. A leaf is a leaf (2x2 atlas, cutout, midrib and
veins), bark tiles along a trunk, moss is clumpy and wet. No image library:
numpy if it is there, otherwise a slower pure-python path.

    python3 tools/jungle/textures.py
"""
from __future__ import annotations

import json
import math
import os
import struct
import zlib

try:
    import numpy as np
except ImportError:
    np = None

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "../.."))
TEX = os.path.join(ROOT, "Assets/textures/jungle")
MAT = os.path.join(ROOT, "Assets/materials/jungle")
MDL = os.path.join(ROOT, "Assets/models/jungle")
SIZE = 1024

SLOT_MATERIALS = {
    "Bark": "materials/jungle/bark.mat",
    "Leaf": "materials/jungle/leaf.mat",
    "Frond": "materials/jungle/frond.mat",
    "Bamboo": "materials/jungle/bamboo.mat",
    "Rock": "materials/jungle/rock.mat",
    "Ground": "materials/jungle/ground.mat",
    "Vine": "materials/jungle/vine.mat",
    "Moss": "materials/jungle/moss.mat",
    "Fungus": "materials/jungle/fungus.mat",
    "Litter": "materials/jungle/litter.mat",
}


# ---------------------------------------------------------------------------
# PNG
# ---------------------------------------------------------------------------

def write_png(path, rgba):
    """rgba is HxWx4 uint8."""
    h, w = rgba.shape[:2]
    filtered = np.zeros((h, 1 + w * 4), np.uint8)
    filtered[:, 1:] = rgba.reshape(h, -1)
    def chunk(kind, data):
        c = struct.pack(">I", len(data)) + kind + data
        return c + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(filtered.tobytes(), 6)) + chunk(b"IEND", b"")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)


def to_srgb(c):
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(c, 1.0 / 2.4) - 0.055)


def encode_albedo(rgb, alpha=None):
    a = np.ones(rgb.shape[:2], np.float64) if alpha is None else alpha
    out = np.empty(rgb.shape[:2] + (4,), np.uint8)
    s = np.clip(to_srgb(rgb) * 255.0 + 0.5, 0, 255)
    out[..., 0] = s[..., 0]
    out[..., 1] = s[..., 1]
    out[..., 2] = s[..., 2]
    out[..., 3] = np.clip(a * 255.0 + 0.5, 0, 255)
    return out


def encode_normal(height, strength=6.0):
    gy, gx = np.gradient(height)
    nx = -gx * strength
    ny = gy * strength
    nz = np.ones_like(height)
    inv = 1.0 / np.sqrt(nx * nx + ny * ny + nz * nz)
    out = np.empty(height.shape + (4,), np.uint8)
    out[..., 0] = np.clip((nx * inv * 0.5 + 0.5) * 255.0 + 0.5, 0, 255)
    out[..., 1] = np.clip((ny * inv * 0.5 + 0.5) * 255.0 + 0.5, 0, 255)
    out[..., 2] = np.clip((nz * inv * 0.5 + 0.5) * 255.0 + 0.5, 0, 255)
    out[..., 3] = 255
    return out


def encode_rough(rough):
    g = np.clip(rough * 255.0 + 0.5, 0, 255).astype(np.uint8)
    out = np.empty(rough.shape + (4,), np.uint8)
    out[..., 0] = g
    out[..., 1] = g
    out[..., 2] = g
    out[..., 3] = 255
    return out


def save(name, rgb, height, rough, alpha=None, nstr=6.0):
    write_png(os.path.join(TEX, name + ".png"), encode_albedo(rgb, alpha))
    write_png(os.path.join(TEX, name + "_n.png"), encode_normal(height, nstr))
    write_png(os.path.join(TEX, name + "_r.png"), encode_rough(rough))
    print(" ", name)


# ---------------------------------------------------------------------------
# Noise
# ---------------------------------------------------------------------------

def _hash(ix, iy, seed):
    n = (ix.astype(np.int64) * 374761393 + iy.astype(np.int64) * 668265263 + seed * 1274126177) & np.int64(0xffffffff)
    n = (n ^ (n >> 13)) * np.int64(1274126177)
    n = (n ^ (n >> 16)) & np.int64(0xffffffff)
    return n.astype(np.float64) / 4294967295.0


def value_noise(x, y, seed=0):
    x0 = np.floor(x)
    y0 = np.floor(y)
    fx = x - x0
    fy = y - y0
    sx = fx * fx * (3.0 - 2.0 * fx)
    sy = fy * fy * (3.0 - 2.0 * fy)
    ix = x0.astype(np.int64)
    iy = y0.astype(np.int64)
    n00 = _hash(ix, iy, seed)
    n10 = _hash(ix + 1, iy, seed)
    n01 = _hash(ix, iy + 1, seed)
    n11 = _hash(ix + 1, iy + 1, seed)
    return (n00 * (1 - sx) + n10 * sx) * (1 - sy) + (n01 * (1 - sx) + n11 * sx) * sy


def fbm(x, y, octaves=5, lac=2.0, gain=0.5, seed=1):
    amp, freq, total, norm = 1.0, 1.0, 0.0, 0.0
    for i in range(octaves):
        total += amp * value_noise(x * freq, y * freq, seed + i * 19)
        norm += amp
        amp *= gain
        freq *= lac
    return total / norm


def ridged(x, y, octaves=4, seed=3):
    n = fbm(x, y, octaves=octaves, seed=seed)
    return 1.0 - np.abs(n * 2.0 - 1.0)


def grid(n=SIZE):
    v, u = np.mgrid[0:n, 0:n]
    return u.astype(np.float64) / (n - 1), v.astype(np.float64) / (n - 1)


# ---------------------------------------------------------------------------
# Surfaces
# ---------------------------------------------------------------------------

def mix3(a, b, t):
    t = t[..., None] if t.ndim == 2 else t
    return a * (1.0 - t) + b * t


def leaf_atlas(dry=False):
    """2x2 of distinct blades. Each cell is one leaf, petiole at v=0, tip at v=1."""
    u, v = grid()
    rgb = np.zeros((SIZE, SIZE, 3))
    height = np.zeros((SIZE, SIZE))
    rough = np.ones((SIZE, SIZE)) * 0.55
    alpha = np.zeros((SIZE, SIZE))

    specs = [
        dict(w=0.42, p=0.58, curve=0.05, holes=0.0, dark=0.0, ruffle=0.03, seed=11, theta=50),
        dict(w=0.30, p=0.78, curve=-0.06, holes=0.0, dark=-0.1, ruffle=0.02, seed=23, theta=46),
        dict(w=0.50, p=0.52, curve=0.02, holes=0.04, dark=0.05, ruffle=0.04, seed=41, theta=58),
        dict(w=0.36, p=0.66, curve=0.09, holes=0.012, dark=0.12, ruffle=0.055, seed=67, theta=53),
    ]
    for i, spec in enumerate(specs):
        cu, cv = (i % 2) * 0.5, (i // 2) * 0.5
        in_cell = (u >= cu) & (u < cu + 0.5) & (v >= cv) & (v < cv + 0.5)
        lu = np.clip((u - cu) / 0.5, 0, 1)
        lv = np.clip((v - cv) / 0.5, 0, 1)
        lx = (lu - 0.5) * 2.0
        ly = lv
        nedge = (fbm(lu * 20, lv * 16, 3, seed=spec["seed"]) - 0.5) * spec["ruffle"]
        width = spec["w"] * np.sin(np.pi * np.clip(ly, 0, 1) ** spec["p"]) ** 0.72
        width = np.maximum(width * (1.0 + spec["curve"] * lx) + nedge, 0.0)
        stem = np.exp(-(ly / 0.05) ** 2) * 0.05
        width = np.maximum(width, stem)
        dist = np.abs(lx) - width
        a = np.clip(0.5 - dist * (SIZE / 2) * 0.35, 0.0, 1.0)
        a = np.where((lu < 0.015) | (lu > 0.985) | (lv < 0.008) | (lv > 0.992), 0.0, a)
        if spec["holes"] > 0:
            holes = fbm(lu * 24, lv * 20, 3, seed=spec["seed"] + 9)
            a = np.where((holes > 1.0 - spec["holes"]) & (np.abs(lx) < width * 0.65) & (ly > 0.22) & (ly < 0.82), 0.0, a)

        mx = spec["curve"] * 0.18 * np.sin(ly * math.pi)
        dx = lx - mx
        mid = np.exp(-(dx / 0.028) ** 2)
        # Pinnate veins: a diagonal sine, so they leave the midrib and run toward the tip.
        tan = math.tan(math.radians(spec["theta"]))
        diag = ly * 13.0 - np.abs(dx) * tan * 0.55
        vein = np.exp(-(np.sin(diag * math.pi) ** 2) * 22.0)
        vein = vein * (1.0 - np.exp(-(np.abs(dx) / 0.05) ** 2)) * np.clip(ly * 8.0, 0, 1)
        tert = ridged(lu * 32 + dx * 4, lv * 26, 3, seed=spec["seed"] + 3) * 0.2 * (1.0 - mid)
        h = (mid * 0.7 + vein * 0.45 + tert * 0.15) * a

        if dry:
            base = np.array([0.18, 0.10, 0.04])
            lit = np.array([0.36, 0.22, 0.08])
            vein_c = np.array([0.28, 0.16, 0.06])
            edge_c = np.array([0.12, 0.07, 0.03])
        else:
            base = np.array([0.028, 0.075, 0.016]) * (1.0 + spec["dark"])
            lit = np.array([0.055, 0.14, 0.028])
            vein_c = np.array([0.09, 0.17, 0.035])
            edge_c = np.array([0.016, 0.042, 0.01])
            if spec["dark"] < 0:
                lit = np.array([0.09, 0.17, 0.038])

        inside = np.clip(1.0 - np.abs(lx) / (width + 1e-4), 0, 1)
        mottling = fbm(lu * 10, lv * 9, 4, seed=spec["seed"] + 5)
        col = mix3(edge_c, base, inside ** 0.55)
        col = mix3(col, lit, mottling * 0.4 + mid * 0.2)
        col = mix3(col, vein_c, np.clip(vein * 1.1 + mid * 0.65, 0, 1))
        speckle = np.clip(fbm(lu * 42, lv * 38, 2, seed=spec["seed"] + 7) - 0.64, 0, 1) * 2.2
        col = col + speckle[..., None] * (np.array([0.04, 0.07, 0.015]) if not dry else np.array([0.06, 0.04, 0.01]))
        col = col * a[..., None]

        rgh = (0.36 + 0.28 * (1.0 - mid) + 0.1 * mottling) if not dry else (0.7 + 0.18 * mottling)

        rgb = np.where(in_cell[..., None], col, rgb)
        height = np.where(in_cell, h, height)
        rough = np.where(in_cell, rgh, rough)
        alpha = np.where(in_cell, a, alpha)

    return rgb, height, rough, alpha


def frond_sheet():
    """Tiles along V: midrib down the middle, leaflets as density, parallel veins."""
    u, v = grid()
    x = (u - 0.5) * 2.0
    n = fbm(u * 8, v * 14, 4, seed=5)
    mid = np.exp(-(x / 0.08) ** 2)
    # Leaflet pulse along V so a pinnate strip reads as many small leaves.
    leaflets = np.clip(np.sin(v * math.pi * 16.0) ** 4, 0, 1)
    vein = np.exp(-((np.abs(x) - 0.15 - 0.55 * ((v * 16.0) % 1.0)) * 18.0) ** 2)
    grain = ridged(u * 22, v * 40, 3, seed=8)
    h = mid * 0.5 + vein * 0.3 + grain * 0.12 + leaflets * 0.08
    base = np.array([0.04, 0.10, 0.02])
    lit = np.array([0.08, 0.17, 0.035])
    rib = np.array([0.09, 0.16, 0.03])
    col = mix3(base, lit, n * 0.5 + (1.0 - np.abs(x)) * 0.25)
    col = mix3(col, rib, mid * 0.55 + vein * 0.35)
    # Soft edge so a grass blade thins without a rectangle.
    alpha = np.clip(1.05 - np.abs(x) ** 8, 0.0, 1.0)
    rough = 0.42 + 0.2 * (1.0 - mid) + 0.08 * n
    return col, h, rough, alpha


def bark_sheet(green=0.0, rings=9.0, seed=2):
    u, v = grid()
    wobble = fbm(u * 5, v * 2.4, 4, seed=seed) * 0.35
    groove = np.abs(np.sin((u * rings + wobble) * math.pi)) ** 1.6
    grain = ridged(u * 22, v * 7, 5, seed=seed + 4)
    cracks = np.clip(ridged(u * 8, v * 2.6, 3, seed=seed + 8) - 0.62, 0, 1) * 2.4
    knots = np.clip(fbm(u * 6, v * 6, 2, seed=seed + 11) - 0.82, 0, 1) * 6.0
    h = (1.0 - groove) * 0.55 + grain * 0.28 - cracks * 0.35 + knots * 0.2
    dark = np.array([0.028, 0.018, 0.010])
    wood = np.array([0.11, 0.065, 0.032])
    crease = np.array([0.02, 0.012, 0.007])
    col = mix3(wood, dark, groove * 0.85)
    col = mix3(col, crease, np.clip(cracks, 0, 1))
    if green:
        lichen = np.clip(fbm(u * 8, v * 8, 4, seed=seed + 17) - (0.58 - green * 0.1), 0, 1) ** 1.4 * 1.8
        col = mix3(col, np.array([0.08, 0.13, 0.035]), np.clip(lichen, 0, 1))
        h = h + lichen * 0.1
    rough = 0.55 + 0.28 * groove + 0.12 * grain
    return col, h, np.clip(rough, 0.32, 0.95)


def moss_sheet():
    u, v = grid()
    clumps = ridged(u * 14, v * 14, 5, seed=21)
    fine = fbm(u * 55, v * 55, 3, seed=24)
    tips = np.clip(clumps * 1.45 - 0.4, 0, 1)
    dead = np.clip(fbm(u * 7, v * 7, 3, seed=29) - 0.68, 0, 1) * 2.6
    h = clumps * 0.75 + fine * 0.3
    green = np.array([0.03, 0.09, 0.018])
    bright = np.array([0.09, 0.20, 0.035])
    brown = np.array([0.09, 0.06, 0.025])
    col = mix3(green, bright, tips ** 0.7)
    col = mix3(col, brown, np.clip(dead, 0, 1))
    col = col * (0.7 + 0.45 * fine[..., None])
    rough = 0.8 - 0.18 * tips + 0.1 * fine
    return col, h, np.clip(rough, 0.5, 0.95)


def rock_sheet():
    u, v = grid()
    big = fbm(u * 4.5, v * 4.5, 6, seed=31)
    pit = ridged(u * 11, v * 11, 4, seed=34)
    grit = fbm(u * 64, v * 64, 2, seed=37)
    h = big * 0.5 + pit * 0.32 + grit * 0.18
    stone = np.array([0.12, 0.11, 0.10])
    dark = np.array([0.035, 0.033, 0.030])
    col = mix3(dark, stone, np.clip(pit * 0.7 + big * 0.3, 0, 1))
    stain = np.clip(fbm(u * 6, v * 6, 4, seed=40) - 0.55, 0, 1) ** 1.3 * 1.6
    col = mix3(col, np.array([0.04, 0.07, 0.025]), np.clip(stain * (1.15 - pit), 0, 1))
    speckle = (grit - 0.5) * 0.04
    col = np.clip(col + speckle[..., None], 0, 1)
    rough = 0.48 + 0.3 * grit - 0.1 * pit
    return col, h, np.clip(rough, 0.25, 0.92)


def ground_sheet():
    u, v = grid()
    humus = fbm(u * 5, v * 5, 5, seed=44)
    litter = np.clip(fbm(u * 22, v * 22, 4, seed=47) - 0.52, 0, 1) ** 1.2 * 1.8
    # Short broken fibres, not long drips.
    twigs = np.clip(ridged(u * 28 + fbm(u * 4, v * 4, 2, seed=49) * 3, v * 18, 3, seed=50) - 0.72, 0, 1) * 3.5
    grit = fbm(u * 48, v * 48, 2, seed=53)
    h = humus * 0.35 + litter * 0.4 + twigs * 0.15 + grit * 0.12
    soil = np.array([0.045, 0.03, 0.016])
    damp = np.array([0.025, 0.018, 0.01])
    leaf = np.array([0.10, 0.07, 0.025])
    twig_c = np.array([0.07, 0.045, 0.02])
    col = mix3(damp, soil, humus)
    col = mix3(col, leaf, np.clip(litter, 0, 1))
    col = mix3(col, twig_c, np.clip(twigs, 0, 1))
    rough = 0.76 + 0.14 * grit - 0.06 * humus
    return col, h, np.clip(rough, 0.55, 0.95)


def bamboo_sheet():
    u, v = grid()
    # Vertical grain, a darker node band that tiles with the scars on the culm.
    grain = fbm(u * 14, v * 3, 4, seed=58)
    node = np.exp(-(((v * 4.0) % 1.0 - 0.5) / 0.06) ** 2)
    h = grain * 0.35 + node * 0.4
    green = np.array([0.18, 0.22, 0.07])
    yellow = np.array([0.28, 0.26, 0.08])
    ring = np.array([0.10, 0.09, 0.04])
    col = mix3(green, yellow, grain * 0.6 + u * 0.15)
    col = mix3(col, ring, node)
    rough = 0.38 + 0.2 * grain + 0.15 * node
    return col, h, np.clip(rough, 0.25, 0.75)


def fungus_sheet():
    u, v = grid()
    # Concentric growth rings from the centre of the shelf (v is radial-ish).
    rings = 0.5 + 0.5 * np.sin((v * 9.0 + fbm(u * 4, v * 4, 3, seed=61) * 0.8) * math.pi * 2)
    pores = fbm(u * 50, v * 50, 2, seed=64)
    h = rings * 0.55 + pores * 0.2
    cream = np.array([0.42, 0.32, 0.16])
    orange = np.array([0.35, 0.18, 0.06])
    edge = np.array([0.22, 0.12, 0.05])
    col = mix3(orange, cream, rings)
    col = mix3(col, edge, np.clip(v * 0.4, 0, 1))
    col = col * (0.85 + 0.2 * pores[..., None])
    rough = 0.68 + 0.15 * pores - 0.08 * rings
    return col, h, np.clip(rough, 0.45, 0.9)


def make_all():
    os.makedirs(TEX, exist_ok=True)
    print("textures")
    rgb, h, r, a = leaf_atlas(dry=False)
    save("leaf", rgb, h, r, a, nstr=10.0)
    rgb, h, r, a = frond_sheet()
    save("frond", rgb, h, r, a, nstr=8.0)
    rgb, h, r = bark_sheet(green=0.35, rings=10, seed=2)
    save("bark", rgb, h, r, nstr=7.0)
    rgb, h, r = bark_sheet(green=0.7, rings=7, seed=9)
    save("vine", rgb, h, r, nstr=6.0)
    rgb, h, r = moss_sheet()
    save("moss", rgb, h, r, nstr=9.0)
    rgb, h, r = rock_sheet()
    save("rock", rgb, h, r, nstr=8.0)
    rgb, h, r = ground_sheet()
    save("ground", rgb, h, r, nstr=5.0)
    rgb, h, r = bamboo_sheet()
    save("bamboo", rgb, h, r, nstr=5.0)
    rgb, h, r = fungus_sheet()
    save("fungus", rgb, h, r, nstr=6.0)
    rgb, h, r, a = leaf_atlas(dry=True)
    save("litter", rgb, h, r, a, nstr=8.0)


# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------

def mat(name, shader, color, normal, rough_tex, roughness, two_sided=False, blend="Opaque",
        cutoff=0.5, features=None, numbers=None, textures=None):
    d = {
        "Shader": shader,
        "Features": features or {},
        "Numbers": numbers or {},
        "Textures": textures or {},
        "Tint": "1,1,1,1",
        "ColorMap": color,
        "Normal": normal,
        "RoughMetalAmbient": "materials/default/roughmetal.png",
        "Emission": "materials/default/black.png",
        "Roughness": roughness,
        "Metalness": 0.0,
        "EmissionStrength": 0.0,
        "PhysicsSurface": "",
        "TwoSided": two_sided,
        "Filtering": "Smooth",
        "Blend": blend,
        "AlphaCutoff": cutoff,
        "__references": [],
        "__version": 0,
    }
    path = os.path.join(MAT, name + ".mat")
    os.makedirs(MAT, exist_ok=True)
    with open(path, "w") as f:
        json.dump(d, f, indent=2)
        f.write("\n")
    return f"materials/jungle/{name}.mat"


def maps(name):
    return f"textures/jungle/{name}.png", f"textures/jungle/{name}_n.png", f"textures/jungle/{name}_r.png"


def write_materials():
    print("materials")
    wind = {
        "g_flWindStrength": "0.12,0,0,0",
        "g_flWindSpeed": "1.8,0,0,0",
        "g_flWindHeight": "8,0,0,0",
        "g_vWindDirection": "1,0,0.25,0",
        "g_flRoughness": "0.42,0,0,0",
        "g_flOpacityMipBoost": "0.35,0,0,0",
        "g_flAlphaCutoff": "0.4,0,0,0",
    }
    c, n, r = maps("leaf")
    mat("leaf", "shaders/foliage.shader", c, n, r, 0.42, True, "Masked", 0.4,
        features={"F_WIND": 1, "F_NORMAL_MAP": 1, "F_ROUGHNESS": 1, "F_ALPHA": 1, "F_BACKFACES": 1},
        numbers=wind, textures={"g_tRoughness": r})
    c, n, r = maps("frond")
    frond_wind = dict(wind)
    frond_wind["g_flWindStrength"] = "0.18,0,0,0"
    frond_wind["g_flWindHeight"] = "2.5,0,0,0"
    frond_wind["g_flOpacityMipBoost"] = "0.0,0,0,0"
    mat("frond", "shaders/foliage.shader", c, n, r, 0.45, True, "Masked", 0.15,
        features={"F_WIND": 1, "F_NORMAL_MAP": 1, "F_ROUGHNESS": 1, "F_ALPHA": 1, "F_BACKFACES": 1},
        numbers=frond_wind, textures={"g_tRoughness": r})
    c, n, r = maps("litter")
    litter_wind = dict(wind)
    litter_wind["g_flWindStrength"] = "0.04,0,0,0"
    litter_wind["g_flWindHeight"] = "0.4,0,0,0"
    mat("litter", "shaders/foliage.shader", c, n, r, 0.75, True, "Masked", 0.4,
        features={"F_WIND": 1, "F_NORMAL_MAP": 1, "F_ROUGHNESS": 1, "F_ALPHA": 1, "F_BACKFACES": 1},
        numbers=litter_wind, textures={"g_tRoughness": r})

    for name, rough, nfeat in (
        ("bark", 0.68, 1),
        ("vine", 0.62, 1),
        ("moss", 0.84, 1),
        ("rock", 0.5, 1),
        ("ground", 0.8, 1),
        ("bamboo", 0.4, 1),
        ("fungus", 0.7, 1),
    ):
        c, n, r = maps(name)
        mat(name, "shaders/complex.shader", c, n, r, rough, False, "Opaque", 0.5,
            features={"F_NORMAL_MAP": 1, "F_ROUGHNESS": 1},
            numbers={"g_flRoughness": f"{rough},0,0,0"},
            textures={"g_tRoughness": r})


def patch_remaps():
    if not os.path.isdir(MDL):
        return 0
    remaps = [{"Surface": s, "Material": m} for s, m in SLOT_MATERIALS.items()]
    n = 0
    for fn in os.listdir(MDL):
        if not fn.endswith(".mdl"):
            continue
        path = os.path.join(MDL, fn)
        with open(path) as f:
            mdl = json.load(f)
        mdl["MaterialRemaps"] = remaps
        with open(path, "w") as f:
            json.dump(mdl, f, indent=2)
            f.write("\n")
        n += 1
    print("remaps", n)
    return n


if __name__ == "__main__":
    if np is None:
        raise SystemExit("numpy is required: pip install numpy")
    make_all()
    write_materials()
    patch_remaps()
    print("done")
