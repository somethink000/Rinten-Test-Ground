#!/usr/bin/env python3
"""Writes the FX showcase for the test ground: sprites, .fx effects and the scene."""
import json, uuid, os, math

ROOT = "/home/sampesss/Documents/Rinten Projects/Rinten-Test-Ground/Assets"
TEX = "textures/fx"

def guid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "rinten-fx-showcase/" + name))

# ---------------------------------------------------------------- sprites

def tex(path):
    return {"$compiler": "texture", "$source": "imagefile",
            "data": {"FilePath": path, "MaxSize": 4096}, "compiled": None}

def sprite(name, frames, fps=15, loop="Loop"):
    doc = {"Animations": [{
        "Name": "Default", "FrameRate": fps, "Origin": "0.5,0.5", "LoopMode": loop,
        "LoopStart": -1, "LoopEnd": -1,
        "Frames": [{"Texture": tex(f"{TEX}/{f}.png"), "BroadcastMessages": []} for f in frames]}],
        "__references": [], "__version": 2}
    write(f"sprites/{name}.sprite", doc)

def write(rel, doc):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(doc, f, indent=2)
    print("wrote", rel)

# ---------------------------------------------------------------- values

def rng(a, b):
    """A number picked once per particle, between the two."""
    return {"Type": "Range", "Evaluation": "Seed", "Constants": f"{a},{b},0,0"}

def curve(points, top=1.0, mode="Flat"):
    """A value over the particle's life. points: (t, v) with v in 0..top."""
    frames = [{"x": t, "y": v / top, "in": 0, "out": 0, "mode": mode} for t, v in points]
    c = frames if top == 1.0 else {"rangey": f"0,{top}", "frames": frames}
    return {"Type": "Curve", "Evaluation": "Life", "CurveA": c, "CurveB": c}

def gradient(stops, alphas=None):
    g = {"blend": "Linear", "color": [{"t": t, "c": c} for t, c in stops], "alpha": None}
    if alphas:
        g["alpha"] = [{"t": t, "a": a} for t, a in alphas]
    return {"Type": "Gradient", "Evaluation": "Life", "GradientA": g, "GradientB": g}

def color_range(a, b):
    return {"Type": "Range", "Evaluation": "Particle", "ConstantA": a, "ConstantB": b}

def fb(value=1.0, param=None, mult=1.0, mode="Multiply"):
    """A float binding: the value, times the named parameter (or replaced by it)."""
    return {"UseParameter": param is not None, "Value": value, "ParameterName": param, "Mode": mode, "Multiplier": mult, "IsBound": False}

def vb(x=0.0, y=0.0, z=0.0, param=None, mult=1.0, scale=None):
    """A vector binding: the value or the named vector parameter, times a float parameter."""
    return {"UseParameter": param is not None, "Value": {"X": x, "Y": y, "Z": z}, "ParameterName": param, "Multiplier": mult,
            "ScaleParameterName": scale, "IsBound": False}

def cb(value="1,1,1,1", param=None):
    return {"UseParameter": param is not None, "Value": value, "ParameterName": param, "IsBound": False}

def hexc(h, a=1.0):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return f"{r:.4f},{g:.4f},{b:.4f},{a}"

# ---------------------------------------------------------------- modules

_n = [0]
def mod(type_, stage, name, **props):
    _n[0] += 1
    d = {"__type": f"Rinten.{type_}", "Stage": stage}
    d.update(props)
    d.update({"Identifier": guid(f"module/{_n[0]}"), "Name": name, "Enabled": True})
    return d

def rate(r, param=None, mult=1.0):        return mod("SpawnRateModule", "Spawn", "Spawn Rate", Rate=fb(r, param, mult))
def burst(n, param=None, mult=1.0):       return mod("SpawnBurstModule", "Spawn", "Spawn Burst", Count=fb(n, param, mult))
def position(shape="Point", radius=0.5, box=(1, 1, 1), cone=45, shell=False, line=((0, 0, 0), (0, 1, 0)), follows="Rotation, Scale", offset=(0, 0, 0)):
    return mod("InitializePositionModule", "Initialize", "Position", Shape=shape, Offset=",".join(map(str, offset)), Follows=follows, Radius=radius,
               BoxSize=",".join(map(str, box)), ConeAngle=cone, OnShell=shell,
               LineStart=",".join(map(str, line[0])), LineEnd=",".join(map(str, line[1])))
def velocity(x=0, y=0, z=0, scatter=0.0, local=False, param=None, mult=1.0, drift=(0, 0, 0), inherit=False, scale=None, scatter_param=None):
    sc = scatter if isinstance(scatter, dict) and "UseParameter" in scatter else fb(scatter, scatter_param)
    return mod("InitializeVelocityModule", "Initialize", "Velocity", Velocity=vb(x, y, z, param, mult, scale), Scatter=sc,
               LocalSpace=local, InheritEmitterVelocity=inherit, InheritScale=1,
               Drift={"X": drift[0], "Y": drift[1], "Z": drift[2]})
def lifetime(v, param=None, mult=1.0):    return mod("InitializeLifetimeModule", "Initialize", "Lifetime", Lifetime=fb(v, param, mult))
def size(v, param=None, inherit=True):    return mod("InitializeSizeModule", "Initialize", "Size", Size=fb(v, param), InheritEmitterScale=inherit)
def stretch(v):                           return mod("InitializeStretchModule", "Initialize", "Stretch", Stretch=fb(v))
def color(c="1,1,1,1", alpha=1.0, brightness=1.0, tint="1,1,1,1", param=None, alpha_param=None, bright_param=None):
    return mod("InitializeColorModule", "Initialize", "Color", Color=cb(c, param), Alpha=fb(alpha, alpha_param), Brightness=fb(brightness, bright_param), Tint=tint)
def rotation(x=0, y=0, z=0):              return mod("InitializeRotationModule", "Initialize", "Rotation", Rotation={"X": x, "Y": y, "Z": z})
def collision(radius=0.05, bounce=0.5, friction=0.5, die=0.0, bump=0.0):
    return mod("ParticleCollisionModule", "Initialize", "Collision", Ignore="", Radius=fb(radius), DieOnHitChance=fb(die),
               Prefabs=[], PrefabChance=fb(1), PrefabRotation=fb(0), PrefabAlign=False, Bounce=fb(bounce),
               Friction=fb(friction), Bumpiness=fb(bump), PushStrength=fb(0))
def gravity(x=0, y=-9.8, z=0, param=None, mult=1.0, scale=None): return mod("GravityModule", "Update", "Gravity", Force=vb(x, y, z, param, mult, scale))
def drag(d, param=None):                  return mod("DragModule", "Update", "Drag", Damping=fb(d, param))
def orbit(speed=90, axis=(0, 1, 0), param=None, center=(0, 0, 0), space="Local"):
    return mod("OrbitModule", "Update", "Orbit", Space=space, Center=",".join(map(str, center)), Axis=vb(*axis), Speed=fb(speed, param))
def spin(x=0, y=0, z=0, slot=None):
    v = vb(x, y, z)
    if slot: v.update({"SlotName": slot, "SlotMode": "Multiply"})
    return mod("SpinModule", "Update", "Spin", Speed=v)

def set_row(what="Slot", slot=None, value=(0, 0, 0), w=1.0, multiply=False):
    return {"Enabled": True, "Set": what, "Slot": slot, "Value": vb(*value) if isinstance(value, tuple) else value,
            "W": fb(w) if not isinstance(w, dict) else w, "Multiply": multiply}

def ctx(source, parameter, channel="X", scale=1.0, slot=None):
    return {"Enabled": True, "Source": source, "Slot": slot, "Parameter": parameter, "Channel": channel, "Scale": scale, "FromSlot": slot is not None}

def chunks(name, count, material="materials/fx/stylized_stone.mat", sizes=(0.04, 0.09), up=3.0, spread=4.0, life=(1.5, 3.2),
           count_param=None, spread_param=None, gravity_scale=None, offset=(0, 0, 0), shape_radius=0.05, tint="1,1,1,1", glow=None):
    """3D debris: box chunks with the stylized stone material, tumbling, bouncing, and lying still once down."""
    return emitter(name,
        burst(count, count_param),
        position("Sphere", radius=shape_radius, offset=offset),
        velocity(0, up, 0, scatter=fb(spread, spread_param)),
        lifetime(rng(*life)),
        size(rng(*sizes)),
        color(tint),
        rotation(rng(0, 360), rng(0, 360), rng(0, 360)),
        event("OnBirth", "Spin On", sets=[set_row("Slot", "Spin", (1, 1, 1), 1.0)]),
        event("OnCollision", "Land", sets=[set_row("Slot", "Spin", (0.25, 0.25, 0.25), 1.0, multiply=True)]),
        spin(rng(-500, 500), rng(-500, 500), rng(-500, 500), slot="Spin"),
        collision(radius=0.03, bounce=0.4, friction=0.8),
        gravity(0, -9.8, 0, scale=gravity_scale),
        drag(0.2),
        mesh_render("models/dev/box.mdl", material, scale=1.0, rotate=False, shadows=True,
                    shader=[("Dissolve", 1, fb(curve([(0, 0), (0.8, 0), (1, 1)]))), ("Edge", 1, fb(0.1)),
                            ("Emission", 1, fb(glow if glow is not None else 0.9)), ("Scroll", 1, fb(0.0))]),
        max_particles=int(count * 2))

def event(trigger, name=None, at=1.0, every=0.0, distance=0.05, once=False, chance=1.0, sets=(), effect_=None, scale=1.0,
          align=False, follow=False, max_alive=16, context=(), at_param=None):
    return mod("EventModule", "Update", name or f"Event {trigger}", Trigger=trigger, At=fb(at, at_param), Every=every, Distance=distance, Once=once,
               Chance=chance, Set=list(sets), Effect=f"fx/{effect_}.fx" if effect_ else None, Scale=fb(scale), AlignToVelocity=align,
               Follow=follow, MaxAlive=max_alive, Context=list(context))

def face_velocity():                      return mod("FaceVelocityModule", "Update", "Face Velocity")
def attractor(strength=5, size=0.5, falloff=2.0, invert=False, param=None, mult=1.0, space="Local", at=(0, 0, 0)):
    return mod("AttractorModule", "Update", "Attractor", Space=space, Position=vb(*at), Strength=fb(strength, param, mult), Size=size, Invert=invert, Falloff=falloff)
def vortex(strength=5, axis=(0, 1, 0), param=None, mult=1.0, space="Local"):
    return mod("VortexModule", "Update", "Vortex", Space=space, Center="0,0,0", Axis=vb(*axis), Strength=fb(strength, param, mult))
def noise(strength=1.0, scale=1.0, timescale=1.0, param=None):
    return mod("CurlNoiseModule", "Update", "Curl Noise", Strength=fb(strength, param), Scale=fb(scale), TimeScale=fb(timescale), Offset="0,0,0")
def sprite_render(name, scale=1.0, additive=True, align="LookAtCamera", face=False, lighting=False, sort=False,
                  blur=False, blur_amount=0.5, blur_spacing=0.5, blur_opacity=0.5, fog=1.0, opaque=False):
    return mod("SpriteRenderModule", "Render", "Sprite", Sprite=f"sprites/{name}.sprite", Scale=scale, Alignment=align,
               FaceVelocity=face, Additive=additive, Shadows=False, Lighting=lighting, DepthFeather=0,
               SortMode="ByDistance" if sort else "Unsorted", Opaque=opaque, FogStrength=fog, TextureFilter="Bilinear",
               MotionBlur=blur, LeadingTrail=True, BlurAmount=blur_amount, BlurSpacing=blur_spacing, BlurOpacity=blur_opacity)
def light(c="1,1,1,1", brightness=1.0, radius=1.0, ratio=1.0, max_lights=4, use_particle=True, param=None):
    return mod("LightRenderModule", "Render", "Light", Color=cb(c), Brightness=fb(brightness, param), Radius=fb(radius),
               Attenuation=fb(1), MaxLights=fb(max_lights), Ratio=fb(ratio), UseParticleColor=use_particle, CastShadows=False)

def trail_render(width=0.05, color="1,1,1,1", life=0.5, max_points=32, point_distance=0.05, opaque=False, param=None, width_param=None, scale_from=False, tint=True, additive=False,
                 taper=(1.0, 0.0), fade=(1.0, 0.0)):
    """A ribbon that tapers (width at the particle, at the far end) and fades (alpha at each), by default to a point and to clear."""
    w = fb(curve([(0, width * taper[0]), (1, width * taper[1])], top=max(width, 1e-4), mode="Linear"), width_param) if taper else fb(width, width_param)
    if fade and isinstance(color, str):
        parts = color.split(","); a = float(parts[3]) if len(parts) > 3 else 1.0
        c = gradient([(0, color), (1, color)], alphas=[(0, a * fade[0]), (1, a * fade[1])])
    else:
        c = color
    return mod("TrailRenderModule", "Render", "Trail", Material=None, Width=w, Color=cb(c, param), UnitsPerTexture=0.5,
               Scroll=0, MaxPoints=max_points, PointDistance=point_distance, LifeTime=life, Opaque=opaque, BlendMode="Lighten" if additive else "Normal",
               ScaleFromParticle=scale_from, TintFromParticle=tint)
def model_render(models=("models/dev/box.mdl",), scale=1.0, shadows=True, rotate=False, param=None):
    return mod("ModelRenderModule", "Render", "Model", Models=[{"Model": m, "MaterialGroup": None, "BodyGroups": 18446744073709551615} for m in models],
               Scale=fb(scale, param), RotateWithObject=rotate, CastShadows=shadows)
def on_death(effect, chance=1.0, scale=1.0, align=False, on_collision=True, on_expiry=True, max_alive=16, scale_param=None):
    return mod("SpawnEffectOnDeathModule", "Render", "Effect On Death", Effect=f"fx/{effect}.fx", Chance=fb(chance), Scale=fb(scale, scale_param),
               AlignToVelocity=align, OnCollision=on_collision, OnExpiry=on_expiry, MaxAlive=max_alive)

def mesh_render(model, material, scale=1.0, rotate=True, shadows=False, morphs=(), shader=(), particle_attrs=True, scale_param=None, part_from_particle=False):
    """morphs: (name, binding); shader: (name, width, binding)"""
    return mod("MeshRenderModule", "Render", "Mesh", Model=model, Material=material, Scale=fb(scale, scale_param), RotateWithObject=rotate, CastShadows=shadows,
               PartFromParticle=part_from_particle,
               Morphs=[{"Enabled": True, "Name": n, "Weight": b} for n, b in morphs],
               Shader=[{"Enabled": True, "Name": n, "Width": w,
                        "Value": (b if w < 3 else fb(0)),
                        "Color": (b if (w >= 3 and not (isinstance(b, dict) and "ScaleParameterName" in b)) else cb()),
                        "AsVector": bool(w >= 3 and isinstance(b, dict) and "ScaleParameterName" in b),
                        "Vector": (b if (w >= 3 and isinstance(b, dict) and "ScaleParameterName" in b) else vb()),
                        "Min": 0, "Max": 1} for n, w, b in shader],
               ParticleAttributes=particle_attrs)

STAGES = {"Spawn": "SpawnModules", "Initialize": "InitializeModules", "Update": "UpdateModules", "Render": "RenderModules"}

def by_index(points, top=1.0, mode="Flat"):
    """A curve read by the particle's place among its emitter's - the first born at 0, the last at 1."""
    c = curve(points, top, mode); c["Evaluation"] = "Index"; return c

def gradient_by_index(stops):
    g = gradient(stops); g["Evaluation"] = "Index"; return g

def slot_fb(slot, channel="X", value=1.0, mode="Replace", param=None):
    """A float binding read out of one of the effect's slots, per particle."""
    b = fb(value, param); b.update({"SlotName": slot, "SlotChannel": channel, "SlotMode": mode}); return b

def slot_vb(slot, mode="Replace", x=1.0, y=1.0, z=1.0):
    b = vb(x, y, z); b.update({"SlotName": slot, "SlotMode": mode}); return b

def shape(name, kind, offset=(0, 0, 0), rot=(0, 0, 0), radius=0.5, box=(1, 1, 1), cone=45, shell=False,
          line=((0, 0, 0), (0, 1, 0)), points=(), closed=False, grid=(5, 1, 5), spacing=(0.3, 0.3, 0.3),
          height=2.0, turns=3.0, count=0, anchor=None, line_anchors=(None, None), model=None, model_sample="Parts", model_scale=1.0):
    return {"Name": name, "Identifier": guid("shape/" + name), "Kind": kind, "Anchor": anchor,
            "Model": model, "ModelSampling": model_sample, "ModelScale": model_scale,
            "LineStartAnchor": line_anchors[0], "LineEndAnchor": line_anchors[1],
            "Offset": ",".join(map(str, offset)), "Rotation": ",".join(map(str, rot)), "Radius": radius,
            "BoxSize": ",".join(map(str, box)), "ConeAngle": cone, "OnShell": shell,
            "LineStart": ",".join(map(str, line[0])), "LineEnd": ",".join(map(str, line[1])),
            "Points": [",".join(map(str, p)) for p in points], "Closed": closed,
            "GridCount": ",".join(map(str, grid)), "GridSpacing": ",".join(map(str, spacing)),
            "Height": height, "Turns": turns, "Count": count}

def position_on(shape_name, sample="Random", along=None, align=False, follows="Rotation, Scale", offset=(0, 0, 0)):
    """Born on one of the effect's shapes."""
    m = position(follows=follows, offset=offset)
    m.update({"ShapeName": shape_name, "Sample": sample, "Along": along if along is not None else fb(0.0), "AlignToShape": align})
    return m

def follow(shape_name, along=None, stagger=None, loop=True, weight=None, align=False, name="Follow Shape", sample="ByTime", speed=None):
    return mod("FollowShapeModule", "Update", name, ShapeName=shape_name, Sample=sample,
               Along=along if along is not None else fb(curve([(0, 0), (1, 1)], mode="Linear")),
               Speed=speed if speed is not None else fb(0.0),
               Stagger=stagger if stagger is not None else fb(0.0), Loop=loop,
               Weight=weight if weight is not None else fb(1.0), AlignToShape=align)

def remember(slot, what="Position"):
    return mod("RememberModule", "Initialize", f"Remember {what}", Slot=slot, What=what)

def set_slot(slot, value=None, w=None, what=None, once=False):
    return mod("SetSlotModule", "Update", "Set Slot", Slot=slot, FromParticle=what is not None, What=what or "Position",
               Value=value if value is not None else vb(0, 0, 0), W=w if w is not None else fb(0.0), Once=once)

def local_space(v=1.0):
    """Particles carried with the emitter - what a glow riding an anchor needs."""
    return mod("InitializeLocalSpaceModule", "Initialize", "Local Space", LocalSpace=fb(v))

def anchor(name, offset=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
    return {"Name": name, "Identifier": guid("anchor/" + name), "Offset": ",".join(map(str, offset)),
            "Rotation": ",".join(map(str, rot)), "Scale": ",".join(map(str, scale))}

def goal(target="Anchor", anchor=None, shape_name=None, slot=None, sample="ByIndex", along=None, offset=(0, 0, 0),
         position=None, rotation=None, scale=None, align=False, write_velocity=True):
    return mod("GoalModule", "Update", "Goal", Target=target, ShapeName=shape_name, Sample=sample,
               Along=along if along is not None else fb(0.0), AnchorName=anchor, Offset=",".join(map(str, offset)), SlotName=slot,
               PositionWeight=position if position is not None else fb(curve([(0, 0), (1, 1)], mode="Linear")),
               RotationWeight=rotation if rotation is not None else fb(0.0),
               ScaleWeight=scale if scale is not None else fb(0.0), AlignToMotion=align, WriteVelocity=write_velocity)

def transform_over_life(offset=None, rotation=None, scale=None, space="Local"):
    return mod("TransformOverLifeModule", "Update", "Transform Over Life", Space=space,
               Offset=offset if offset is not None else vb(0, 0, 0),
               Rotation=rotation if rotation is not None else vb(0, 0, 0),
               Scale=scale if scale is not None else fb(1.0))

def emitter(name, *modules, max_particles=1000, delay=0.0, duration=0.0, prewarm=0.0, places=0, offset=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), anchor=None):
    e = {"Name": name, "Identifier": guid(f"emitter/{name}/{_n[0]}"), "Enabled": True, "MaxParticles": max_particles, "Places": places,
         "Offset": ",".join(map(str, offset)), "Rotation": ",".join(map(str, rot)), "Scale": ",".join(map(str, scale)), "Anchor": anchor,
         "Delay": delay, "Duration": duration, "PreWarm": prewarm, "TimeScale": 1, "Timing": "GameTime",
         "SpawnModules": [], "InitializeModules": [], "UpdateModules": [], "RenderModules": []}
    for m in modules:
        e[STAGES[m["Stage"]]].append(m)
    return e

def param_float(name, v=1.0, lo=0.0, hi=3.0):  return {"Name": name, "DefaultValue": v, "Min": lo, "Max": hi, "Identifier": guid("param/" + name)}
def param_vec(name, v):    return {"Name": name, "DefaultValue": ",".join(map(str, v)), "Identifier": guid("param/" + name)}
def param_color(name, v):  return {"Name": name, "DefaultValue": v, "Identifier": guid("param/" + name)}

def effect(name, emitters, duration=5.0, looping=True, floats=(), vectors=(), colors=(), shapes=(), slots=(), anchors=()):
    doc = {"Emitters": emitters, "Duration": duration, "Looping": looping, "Shapes": list(shapes), "Slots": list(slots), "Anchors": list(anchors),
           "FloatParameters": list(floats), "VectorParameters": list(vectors), "ColorParameters": list(colors),
           "__references": [], "__version": 0}
    write(f"fx/{name}.fx", doc)

# ================================================================ SPRITES

sprite("dot", ["dot"])
sprite("glow", ["glow"])
sprite("spark", ["spark"])
sprite("ring", ["ring"])
sprite("flash", ["flash"])
sprite("flake", ["flake"])
sprite("debris", ["debris"])
sprite("paper", ["paper"])
for i in (1, 2, 3, 4):
    sprite(f"smoke{i}", [f"smoke{i}"])
sprite("flame", [f"flame{i}" for i in range(1, 9)], fps=12)

# ================================================================ EFFECTS
#
# Every float parameter is a multiplier over what is authored (Mode=Multiply),
# so 1.0 is the effect as designed and the curves and ranges survive it.

# --- Campfire -------------------------------------------------------------
FIRE = gradient([(0, hexc("fff0b0")), (0.12, hexc("ffa020")), (0.45, hexc("ff5a0a")), (0.8, hexc("a01000")), (1, hexc("200000"))])

effect("ambient/fire", [
    emitter("Flames",
        rate(18, "Intensity"),
        position("Circle", radius=0.22),
        velocity(rng(-0.3, 0.3), rng(1.4, 2.4), rng(-0.3, 0.3), scale="Rise"),
        lifetime(rng(0.55, 0.95), "Lifetime"),
        size(curve([(0, 0.4), (0.35, 0.8), (1, 0.2)], top=0.9), "Size"),
        color(param="Flame", alpha=curve([(0, 0), (0.15, 0.7), (0.7, 0.5), (1, 0)]), brightness=1.0, bright_param="Brightness"),
        rotation(0, 0, rng(-25, 25)),
        gravity(0, 0, 0, param="Wind"),
        noise(0.7, 1.6, 1.5, param="Turbulence"),
        drag(0.6),
        spin(0, 0, rng(-40, 40)),
        sprite_render("flame", additive=True),
        light(hexc("ff9a40"), brightness=6, radius=3.5, ratio=0.06, max_lights=2, use_particle=False, param="Glow"),
        max_particles=300),
    emitter("Embers",
        rate(14, "Embers"),
        position("Sphere", radius=0.2),
        velocity(rng(-0.4, 0.4), rng(1.2, 3.0), rng(-0.4, 0.4), scatter=0.3, scale="Rise"),
        lifetime(rng(1.4, 3.0), "Lifetime"),
        size(rng(0.02, 0.045), "Size"),
        color(hexc("ffc070"), alpha=curve([(0, 1), (0.6, 1), (1, 0)]), brightness=1.5, bright_param="Brightness"),
        stretch(1.8),
        gravity(0, 0.7, 0),
        gravity(0, 0, 0, param="Wind", mult=1.5),
        noise(1.4, 1.2, 2.0, param="Turbulence"),
        drag(0.35),
        sprite_render("spark", additive=True, face=True, blur=True, blur_amount=0.4, blur_spacing=0.3, blur_opacity=0.4),
        max_particles=200),
    emitter("Smoke",
        rate(7, "Smoke"),
        position("Circle", radius=0.15),
        velocity(rng(-0.15, 0.15), rng(0.9, 1.5), rng(-0.15, 0.15), scale="Rise"),
        lifetime(rng(2.5, 4.0), "Lifetime"),
        size(curve([(0, 0.3), (1, 1.4)], top=1.5), "Size"),
        color(gradient([(0, hexc("5a5a5a")), (1, hexc("222222"))]), alpha=curve([(0, 0), (0.15, 0.35), (1, 0)]), alpha_param="Smoke Opacity"),
        rotation(0, 0, rng(0, 360)),
        gravity(0, 0, 0, param="Wind", mult=0.8),
        noise(0.4, 1.0, 0.8, param="Turbulence"),
        spin(0, 0, rng(-20, 20)),
        drag(0.3),
        sprite_render("smoke2", additive=False, lighting=True, sort=True),
        max_particles=100),
], duration=4,
   floats=[param_float("Intensity"), param_float("Rise"), param_float("Lifetime", 1, 0.2, 3), param_float("Size", 1, 0.2, 3),
           param_float("Brightness"), param_float("Turbulence"), param_float("Embers"), param_float("Smoke"),
           param_float("Smoke Opacity", 1, 0, 2), param_float("Glow")],
   vectors=[param_vec("Wind", (0, 0, 0))],
   colors=[param_color("Flame", FIRE)])

# --- Explosion ------------------------------------------------------------
BLAST = gradient([(0, hexc("ffffff")), (0.15, hexc("ffe080")), (0.4, hexc("ff7020")), (0.75, hexc("802010")), (1, hexc("100000"))])

def scatter_velocity(y, amount):
    return velocity(0, y, 0, scatter=fb(amount, "Power"), scale="Power")

effect("combat/explosion", [
    emitter("Flash",
        burst(1),
        position("Point"),
        lifetime(0.14, "Lifetime"),
        size(curve([(0, 1.4), (1, 2.6)], top=3), "Size"),
        color(param="Flash", alpha=curve([(0, 0.8), (1, 0)], mode="Linear"), brightness=1.2, bright_param="Brightness"),
        sprite_render("glow", additive=True),
        light(hexc("ffa040"), brightness=25, radius=9, ratio=1, max_lights=1, use_particle=False, param="Glow"),
        max_particles=4),
    emitter("Shockwave",
        burst(1),
        position("Point"),
        lifetime(0.55, "Lifetime"),
        size(curve([(0, 0.4), (1, 5.5)], top=6), "Size"),
        color(hexc("ffd8a8"), alpha=curve([(0, 0.6), (1, 0)]), brightness=1.0, bright_param="Brightness"),
        rotation(90, 0, 0),
        sprite_render("ring", additive=True, align="Particle"),
        max_particles=4),
    emitter("Fireball",
        burst(20, "Fireball"),
        position("Sphere", radius=0.4),
        scatter_velocity(0.5, 2.2),
        lifetime(rng(0.5, 0.9), "Lifetime"),
        size(curve([(0, 0.6), (0.3, 2.2), (1, 1.8)], top=2.5), "Size"),
        color(param="Blast", alpha=curve([(0, 0.8), (0.5, 0.7), (1, 0)]), brightness=1.0, bright_param="Brightness"),
        rotation(0, 0, rng(0, 360)),
        spin(0, 0, rng(-90, 90)),
        drag(1.2),
        gravity(0, 1.2, 0),
        sprite_render("smoke3", additive=True),
        max_particles=60),
    emitter("Smoke",
        burst(32, "Smoke"),
        position("Sphere", radius=0.5),
        scatter_velocity(0.6, 1.2),
        lifetime(rng(1.6, 2.8), "Lifetime"),
        size(curve([(0, 0.7), (1, 2.4)], top=2.5), "Size"),
        color(gradient([(0, hexc("4a4038")), (0.4, hexc("2a2a2a")), (1, hexc("141414"))]), alpha=curve([(0, 0.7), (0.4, 0.5), (1, 0)]), alpha_param="Smoke Opacity"),
        rotation(0, 0, rng(0, 360)),
        spin(0, 0, rng(-35, 35)),
        drag(0.8),
        gravity(0, 0.9, 0),
        sprite_render("smoke1", additive=False, lighting=True, sort=True),
        max_particles=60, delay=0.12),
    emitter("Sparks",
        burst(160, "Sparks"),
        position("Point"),
        scatter_velocity(2, 6.5),
        lifetime(rng(0.6, 1.3), "Lifetime"),
        size(rng(0.03, 0.05), "Size"),
        color(color_range(hexc("ffd890"), hexc("ff9040")), alpha=curve([(0, 1), (0.7, 1), (1, 0)]), brightness=2.0, bright_param="Brightness"),
        stretch(2.5),
        collision(radius=0.03, bounce=0.45, friction=0.4),
        gravity(0, -9.8, 0, scale="Gravity"),
        drag(0.9),
        sprite_render("spark", additive=True, face=True, blur=True, blur_amount=0.4, blur_spacing=0.3, blur_opacity=0.4),
        max_particles=500),
    chunks("Debris", 22, count_param="Debris", spread_param="Power", gravity_scale="Gravity", glow=curve([(0, 3.0), (0.3, 0.9), (1, 0.9)], top=3)),
], duration=3.5,
   floats=[param_float("Power"), param_float("Size", 1, 0.2, 3), param_float("Lifetime", 1, 0.2, 3), param_float("Brightness"),
           param_float("Sparks"), param_float("Fireball"), param_float("Smoke"), param_float("Debris"),
           param_float("Smoke Opacity", 1, 0, 2), param_float("Gravity", 1, 0, 3), param_float("Glow")],
   colors=[param_color("Blast", BLAST), param_color("Flash", hexc("ffe4b0"))], slots=["Spin"])

# --- Gunshot --------------------------------------------------------------
effect("combat/gunshot", [
    emitter("Flash",
        burst(1),
        position("Point"),
        lifetime(0.07, "Lifetime"),
        size(rng(0.55, 0.85), "Flash Size"),
        color(param="Flash", alpha=curve([(0, 1), (1, 0)], mode="Linear"), brightness=1.5, bright_param="Brightness"),
        rotation(0, 0, rng(0, 360)),
        sprite_render("flash", additive=True),
        light(hexc("ffc070"), brightness=12, radius=4, ratio=1, max_lights=1, use_particle=False, param="Glow"),
        max_particles=4),
    emitter("Core",
        burst(1),
        position("Point"),
        lifetime(0.09, "Lifetime"),
        size(curve([(0, 0.35), (1, 0.6)], top=0.7), "Flash Size"),
        color(hexc("ffb878"), alpha=curve([(0, 0.8), (1, 0)], mode="Linear"), brightness=1.2, bright_param="Brightness"),
        sprite_render("glow", additive=True),
        max_particles=4),
    emitter("Sparks",
        burst(14, "Sparks"),
        position("Point"),
        velocity(0, 0, rng(-13, -22), local=True, scatter=fb(2.5, "Spread"), scale="Speed"),
        lifetime(rng(0.15, 0.32), "Lifetime"),
        size(rng(0.02, 0.035), "Size"),
        color(hexc("ffe0a0"), alpha=curve([(0, 1), (0.6, 1), (1, 0)]), brightness=1.5, bright_param="Brightness"),
        stretch(4),
        gravity(0, -9.8, 0),
        drag(1.5),
        sprite_render("spark", additive=True, face=True, blur=True, blur_amount=0.6, blur_spacing=0.3, blur_opacity=0.5),
        max_particles=60),
    emitter("Smoke",
        burst(9, "Smoke"),
        position("Point"),
        velocity(rng(-0.5, 0.5), rng(0.4, 1.0), rng(-2.5, -4.5), local=True, scatter=fb(0.4, "Spread"), scale="Speed"),
        lifetime(rng(0.7, 1.3), "Lifetime"),
        size(curve([(0, 0.12), (1, 0.6)], top=0.7), "Size"),
        color(hexc("9a9a9a"), alpha=curve([(0, 0.4), (1, 0)]), alpha_param="Smoke Opacity"),
        rotation(0, 0, rng(0, 360)),
        spin(0, 0, rng(-40, 40)),
        drag(1.0),
        gravity(0, 0.5, 0),
        sprite_render("smoke4", additive=False, lighting=True, sort=True),
        max_particles=40, delay=0.02),
    emitter("Tracer",
        burst(1),
        position("Point"),
        velocity(0, 0, -40, local=True, param="Tracer", scale="Speed"),
        lifetime(0.7),
        size(0.045, "Size"),
        color(param="Tracer Color", brightness=2, bright_param="Brightness"),
        stretch(14),
        sprite_render("spark", additive=True, face=True, blur=True, blur_amount=1.0, blur_spacing=0.5, blur_opacity=0.6),
        light(hexc("ffd080"), brightness=3, radius=2, ratio=1, max_lights=1, use_particle=False),
        max_particles=8),
    # The casing: one brass chunk kicked out to the right, tumbling until it
    # lands, then still - the same Spin slot trick as the debris.
    emitter("Casing",
        burst(1),
        position("Point", offset=(0.08, -0.02, 0.15)),
        velocity(2.2, 1.6, 0.3, local=True, scatter=0.4),
        lifetime(2.5),
        size(0.018),
        color(hexc("d8b060")),
        rotation(rng(0, 360), rng(0, 360), rng(0, 360)),
        event("OnBirth", "Spin On", sets=[set_row("Slot", "Spin", (1, 1, 1), 1.0)]),
        event("OnCollision", "Land", sets=[set_row("Slot", "Spin", (0.2, 0.2, 0.2), 1.0, multiply=True)]),
        spin(rng(-900, 900), rng(-900, 900), rng(-900, 900), slot="Spin"),
        collision(radius=0.01, bounce=0.45, friction=0.7),
        gravity(0, -9.8, 0),
        mesh_render("models/dev/box.mdl", "materials/fx/stylized_white.mat", scale=1.0, rotate=False, shadows=True,
                    shader=[("Dissolve", 1, fb(0.0)), ("Edge", 1, fb(0.05)), ("Emission", 1, fb(0.8)), ("Scroll", 1, fb(0.0))]),
        max_particles=4),
], duration=0.42, slots=["Spin"],
   floats=[param_float("Spread"), param_float("Speed"), param_float("Flash Size", 1, 0.2, 3), param_float("Size", 1, 0.2, 3),
           param_float("Lifetime", 1, 0.2, 3), param_float("Brightness"), param_float("Sparks"), param_float("Smoke"),
           param_float("Smoke Opacity", 1, 0, 2), param_float("Glow")],
   vectors=[param_vec("Tracer", (0, 0, -40))],
   colors=[param_color("Flash", hexc("ffd9a0")), param_color("Tracer Color", hexc("ffe8b8"))])

# --- Magic orb ------------------------------------------------------------
AURA = gradient([(0, hexc("40e0ff")), (0.5, hexc("c060ff")), (1, hexc("ff60c0"))])

effect("magic/magic_orb", [
    emitter("Core",
        rate(1.5, "Density"),
        position("Point"),
        lifetime(1.3, "Lifetime"),
        size(curve([(0, 0.25), (0.5, 0.8), (1, 0.3)], top=1), "Size"),
        color(param="Core", alpha=curve([(0, 0), (0.4, 0.35), (1, 0)]), brightness=1.2, bright_param="Brightness"),
        sprite_render("glow", additive=True),
        light(hexc("80c0ff"), brightness=8, radius=4, ratio=0.5, max_lights=1, use_particle=False, param="Glow"),
        max_particles=12),
    emitter("Swirl",
        rate(60, "Density"),
        position("Sphere", radius=1.3, shell=True),
        lifetime(rng(2.4, 3.6), "Lifetime"),
        size(rng(0.035, 0.08), "Size"),
        color(param="Aura", alpha=curve([(0, 0), (0.2, 0.8), (0.8, 0.8), (1, 0)]), brightness=1.2, bright_param="Brightness"),
        orbit(150, (0, 1, 0), "Spin"),
        attractor(strength=3, size=0.3, falloff=0.5, param="Pull", mult=3.0),
        noise(0.2, 1.5, 1.0, param="Wander"),
        drag(0.6),
        sprite_render("spark", additive=True, face=True, blur=True, blur_amount=0.5, blur_spacing=0.3, blur_opacity=0.5),
        max_particles=400),
    emitter("Ring",
        rate(30, "Density"),
        position("Circle", radius=1.7, shell=True),
        lifetime(2.0, "Lifetime"),
        size(rng(0.03, 0.06), "Size"),
        color(gradient([(0, hexc("ffffff")), (1, hexc("c080ff"))]), alpha=curve([(0, 0), (0.3, 0.8), (1, 0)]), brightness=1.0, bright_param="Brightness"),
        orbit(60, (0, 1, 0), "Spin"),
        sprite_render("dot", additive=True),
        max_particles=150),
    emitter("Motes",
        rate(16, "Density"),
        position("Box", box=(2.6, 0.2, 2.6)),
        velocity(0, 0.45, 0),
        lifetime(3.0, "Lifetime"),
        size(rng(0.02, 0.05), "Size"),
        color(hexc("a0f0ff"), alpha=curve([(0, 0), (0.3, 0.8), (1, 0)]), brightness=1.0, bright_param="Brightness"),
        rotation(0, 0, rng(0, 360)),
        spin(0, 0, rng(-60, 60)),
        noise(0.5, 1.0, 0.7, param="Wander"),
        sprite_render("flake", additive=True),
        max_particles=80),
], duration=6,
   floats=[param_float("Spin", 1, -3, 3), param_float("Pull"), param_float("Density"), param_float("Size", 1, 0.2, 3),
           param_float("Lifetime", 1, 0.2, 3), param_float("Brightness"), param_float("Wander"), param_float("Glow")],
   colors=[param_color("Aura", AURA), param_color("Core", gradient([(0, hexc("ffffff")), (1, hexc("80d0ff"))]))])

# --- Fountain -------------------------------------------------------------
effect("ambient/fountain", [
    emitter("Jet",
        rate(250, "Amount"),
        position("Circle", radius=0.05),
        velocity(0, 7.5, 0, scatter=fb(0.9, "Spread"), param="Jet", scale="Pressure"),
        lifetime(2.2, "Lifetime"),
        size(rng(0.035, 0.07), "Droplet"),
        color(param="Water", alpha=curve([(0, 0.5), (0.8, 0.5), (1, 0)]), brightness=1.0, bright_param="Brightness"),
        stretch(2.2),
        collision(radius=0.03, bounce=0.25, friction=0.6, die=0.35),
        gravity(0, -9.8, 0, scale="Gravity"),
        drag(0.05),
        sprite_render("dot", additive=True, face=True),
        max_particles=1200),
    emitter("Mist",
        rate(26, "Mist"),
        position("Line", line=((0, 0.5, 0), (0, 2.8, 0))),
        velocity(rng(-0.3, 0.3), rng(0.2, 0.6), rng(-0.3, 0.3)),
        lifetime(rng(1.5, 2.5), "Lifetime"),
        size(curve([(0, 0.3), (1, 1.0)], top=1), "Droplet"),
        color(hexc("d8ecff"), alpha=curve([(0, 0), (0.3, 0.18), (1, 0)])),
        rotation(0, 0, rng(0, 360)),
        spin(0, 0, rng(-15, 15)),
        noise(0.3, 1.0, 0.6),
        sprite_render("smoke4", additive=False, lighting=True, sort=True),
        max_particles=80),
    emitter("Splash",
        rate(70, "Amount"),
        position("Circle", radius=1.2, shell=True),
        velocity(rng(-0.4, 0.4), rng(0.6, 1.8), rng(-0.4, 0.4), scale="Pressure"),
        lifetime(rng(0.35, 0.6)),
        size(rng(0.02, 0.045), "Droplet"),
        color(hexc("e0f4ff"), alpha=curve([(0, 0.7), (1, 0)]), brightness=1.0, bright_param="Brightness"),
        gravity(0, -9.8, 0, scale="Gravity"),
        sprite_render("dot", additive=True),
        max_particles=100),
], duration=5,
   floats=[param_float("Pressure"), param_float("Amount"), param_float("Spread"), param_float("Droplet", 1, 0.2, 3),
           param_float("Lifetime", 1, 0.2, 3), param_float("Brightness"), param_float("Mist"), param_float("Gravity", 1, 0, 3)],
   vectors=[param_vec("Jet", (0, 7.5, 0))],
   colors=[param_color("Water", gradient([(0, hexc("ffffff")), (0.3, hexc("bfe2ff")), (1, hexc("6fb0ff"))]))])

# --- Snow -----------------------------------------------------------------
effect("ambient/snow", [
    emitter("Flakes",
        rate(160, "Density"),
        position("Box", box=(7, 0.4, 7)),
        velocity(0, -0.7, 0, scale="Fall"),
        lifetime(8.5, "Lifetime"),
        size(rng(0.025, 0.06), "Size"),
        color(param="Color", alpha=curve([(0, 0), (0.08, 1), (0.85, 1), (1, 0)]), alpha_param="Opacity"),
        rotation(0, 0, rng(0, 360)),
        spin(0, 0, rng(-70, 70)),
        gravity(0, -1.4, 0, scale="Fall"),
        gravity(0, 0, 0, param="Wind"),
        drag(1.6),
        noise(0.45, 0.8, 0.6, param="Drift"),
        sprite_render("flake", additive=False, lighting=True),
        max_particles=2500),
    emitter("Haze",
        rate(6, "Haze"),
        position("Box", box=(7, 0.2, 7)),
        velocity(0, -0.3, 0, scale="Fall"),
        lifetime(7, "Lifetime"),
        size(curve([(0, 0.8), (1, 1.6)], top=2), "Size"),
        color(hexc("dfe8f5"), alpha=curve([(0, 0), (0.2, 0.08), (0.8, 0.08), (1, 0)]), alpha_param="Opacity"),
        rotation(0, 0, rng(0, 360)),
        gravity(0, 0, 0, param="Wind", mult=0.6),
        drag(1.0),
        sprite_render("smoke2", additive=False, lighting=True, sort=True),
        max_particles=60),
], duration=6,
   floats=[param_float("Density"), param_float("Fall"), param_float("Size", 1, 0.2, 3), param_float("Lifetime", 1, 0.2, 2),
           param_float("Drift"), param_float("Opacity", 1, 0, 1), param_float("Haze")],
   vectors=[param_vec("Wind", (0.7, 0, 0))],
   colors=[param_color("Color", hexc("ffffff"))])

# --- Portal ---------------------------------------------------------------
GLOW = gradient([(0, hexc("8040ff")), (0.5, hexc("ff60c0")), (1, hexc("ffffff"))])

effect("magic/portal", [
    emitter("Rim",
        rate(90, "Rim"),
        position("Circle", radius=1.5, shell=True),
        lifetime(rng(1.2, 1.8), "Lifetime"),
        size(rng(0.03, 0.06), "Size"),
        color(param="Glow", alpha=curve([(0, 0), (0.15, 0.8), (0.8, 0.8), (1, 0)]), brightness=1.2, bright_param="Brightness"),
        orbit(90, (0, 1, 0), "Speed"),
        noise(0.1, 2.0, 1.5, param="Wander"),
        sprite_render("spark", additive=True, face=True, blur=True, blur_amount=0.6, blur_spacing=0.3, blur_opacity=0.5),
        max_particles=400),
    emitter("Inner",
        rate(120, "Inner"),
        position("Circle", radius=1.4),
        lifetime(rng(0.8, 1.5), "Lifetime"),
        size(rng(0.02, 0.04), "Size"),
        color(param="Inner Color", alpha=curve([(0, 0), (0.3, 0.5), (1, 0)]), brightness=1.0, bright_param="Brightness"),
        orbit(-140, (0, 1, 0), "Speed"),
        attractor(strength=1.5, size=0.2, falloff=0.5, param="Pull", mult=1.5),
        drag(0.5),
        sprite_render("dot", additive=True),
        max_particles=500),
    emitter("Sheet",
        rate(5),
        position("Point"),
        lifetime(1.6, "Lifetime"),
        size(curve([(0, 2.4), (1, 3.0)], top=3), "Size"),
        color(param="Sheet", alpha=curve([(0, 0), (0.4, 0.2), (1, 0)]), brightness=1.0, bright_param="Brightness"),
        sprite_render("glow", additive=True),
        light(hexc("a060ff"), brightness=6, radius=5, ratio=0.5, max_lights=1, use_particle=False, param="Glow Light"),
        max_particles=12),
], duration=6,
   floats=[param_float("Speed", 1, -3, 3), param_float("Pull"), param_float("Rim"), param_float("Inner"), param_float("Size", 1, 0.2, 3),
           param_float("Lifetime", 1, 0.2, 3), param_float("Brightness"), param_float("Wander"), param_float("Glow Light")],
   colors=[param_color("Glow", GLOW), param_color("Inner Color", hexc("c0a0ff")), param_color("Sheet", hexc("6030c0"))])

# --- Chimney smoke --------------------------------------------------------
effect("ambient/chimney", [
    emitter("Smoke",
        rate(9, "Volume"),
        position("Circle", radius=0.25),
        velocity(rng(-0.2, 0.2), rng(1.6, 2.4), rng(-0.2, 0.2), scale="Rise"),
        lifetime(rng(4.5, 7.0), "Lifetime"),
        size(curve([(0, 0.35), (0.3, 1.2), (1, 2.6)], top=3), "Size"),
        color(param="Smoke", alpha=curve([(0, 0), (0.1, 0.5), (0.6, 0.35), (1, 0)]), alpha_param="Opacity"),
        rotation(0, 0, rng(0, 360)),
        spin(0, 0, rng(-12, 12)),
        gravity(0, 0, 0, param="Wind"),
        gravity(0, 0.25, 0, scale="Rise"),
        noise(0.35, 0.6, 0.5, param="Turbulence"),
        drag(0.25),
        sprite_render("smoke1", additive=False, lighting=True, sort=True),
        max_particles=120),
    emitter("Wisps",
        rate(18, "Volume"),
        position("Circle", radius=0.18),
        velocity(rng(-0.3, 0.3), rng(2.0, 3.0), rng(-0.3, 0.3), scale="Rise"),
        lifetime(rng(1.5, 2.5), "Lifetime"),
        size(curve([(0, 0.15), (1, 0.7)], top=1), "Size"),
        color(hexc("7a7672"), alpha=curve([(0, 0), (0.2, 0.3), (1, 0)]), alpha_param="Opacity"),
        rotation(0, 0, rng(0, 360)),
        gravity(0, 0, 0, param="Wind", mult=1.3),
        noise(0.8, 1.4, 1.2, param="Turbulence"),
        drag(0.4),
        sprite_render("smoke3", additive=False, lighting=True, sort=True),
        max_particles=80),
], duration=6,
   floats=[param_float("Volume"), param_float("Rise"), param_float("Size", 1, 0.2, 3), param_float("Lifetime", 1, 0.2, 3),
           param_float("Opacity", 1, 0, 2), param_float("Turbulence")],
   vectors=[param_vec("Wind", (0.9, 0, 0))],
   colors=[param_color("Smoke", gradient([(0, hexc("6a6660")), (0.5, hexc("3c3a38")), (1, hexc("242424"))]))])

# --- Tornado / dust devil -------------------------------------------------
effect("ambient/tornado", [
    emitter("Funnel",
        rate(140, "Density"),
        position("Circle", radius=0.5, shell=True),
        velocity(0, rng(1.0, 1.8), 0, scatter=0.3, scale="Rise"),
        lifetime(rng(3.0, 4.0), "Lifetime"),
        size(curve([(0, 0.25), (1, 0.9)], top=1), "Size"),
        color(param="Dust", alpha=curve([(0, 0), (0.15, 0.45), (0.8, 0.35), (1, 0)]), alpha_param="Opacity"),
        rotation(0, 0, rng(0, 360)),
        spin(0, 0, rng(-90, 90)),
        orbit(240, (0, 1, 0), "Spin"),
        noise(0.2, 0.8, 1.0),
        sprite_render("smoke2", additive=False, lighting=True, sort=True),
        max_particles=700),
    emitter("Debris",
        rate(30, "Debris"),
        position("Circle", radius=0.7),
        velocity(0, rng(1.0, 2.0), 0, scatter=0.25, scale="Rise"),
        lifetime(rng(2.0, 3.0), "Lifetime"),
        size(rng(0.04, 0.09), "Size"),
        color(color_range(hexc("6a5a44"), hexc("a08c6a"))),
        rotation(0, 0, rng(0, 360)),
        spin(0, 0, rng(-400, 400)),
        orbit(320, (0, 1, 0), "Spin"),
        sprite_render("debris", additive=False, lighting=True),
        max_particles=120),
    emitter("Ground Dust",
        rate(40, "Density"),
        position("Circle", radius=1.8),
        velocity(rng(-0.3, 0.3), rng(0.1, 0.5), rng(-0.3, 0.3)),
        lifetime(rng(1.5, 2.5), "Lifetime"),
        size(curve([(0, 0.4), (1, 1.4)], top=1.5), "Size"),
        color(param="Dust", alpha=curve([(0, 0), (0.3, 0.25), (1, 0)]), alpha_param="Opacity"),
        rotation(0, 0, rng(0, 360)),
        orbit(60, (0, 1, 0), "Spin"),
        drag(0.3),
        sprite_render("smoke4", additive=False, lighting=True, sort=True),
        max_particles=120),
], duration=6,
   floats=[param_float("Spin", 1, -3, 3), param_float("Density"), param_float("Rise"), param_float("Size", 1, 0.2, 3),
           param_float("Lifetime", 1, 0.2, 3), param_float("Opacity", 1, 0, 2), param_float("Debris")],
   colors=[param_color("Dust", gradient([(0, hexc("b09a78")), (1, hexc("7a6a52"))]))])

# --- Fireflies ------------------------------------------------------------
effect("ambient/fireflies", [
    emitter("Flies",
        rate(9, "Count"),
        position("Box", box=(5, 2.5, 5)),
        velocity(rng(-0.2, 0.2), rng(-0.1, 0.2), rng(-0.2, 0.2), scale="Speed"),
        lifetime(rng(3.0, 5.0), "Lifetime"),
        size(rng(0.05, 0.09), "Size"),
        color(param="Glow", alpha=curve([(0, 0), (0.2, 1), (0.35, 0.15), (0.5, 1), (0.7, 0.2), (0.85, 1), (1, 0)]), brightness=1.8, bright_param="Brightness"),
        noise(0.7, 0.7, 0.5, param="Wander"),
        drag(0.5),
        sprite_render("dot", additive=True),
        light(hexc("b8ff60"), brightness=1.5, radius=1.2, ratio=0.25, max_lights=6, param="Light"),
        max_particles=80),
    emitter("Sparkle",
        rate(4, "Count"),
        position("Box", box=(5, 2.5, 5)),
        lifetime(rng(0.3, 0.6)),
        size(rng(0.08, 0.14), "Size"),
        color(param="Glow", alpha=curve([(0, 0), (0.5, 0.6), (1, 0)]), brightness=1.2, bright_param="Brightness"),
        rotation(0, 0, rng(0, 360)),
        sprite_render("flake", additive=True),
        max_particles=20),
], duration=5,
   floats=[param_float("Count"), param_float("Size", 1, 0.2, 3), param_float("Lifetime", 1, 0.2, 3), param_float("Speed"),
           param_float("Wander"), param_float("Brightness"), param_float("Light")],
   colors=[param_color("Glow", gradient([(0, hexc("c8ff70")), (1, hexc("70ff90"))]))])

# --- Confetti -------------------------------------------------------------
effect("fireworks/confetti", [
    emitter("Paper",
        burst(160, "Amount"),
        position("Point"),
        velocity(0, 7, 0, scatter=fb(6.0, "Force"), scale="Force"),
        lifetime(rng(3.0, 4.5), "Lifetime"),
        size(rng(0.08, 0.13), "Size"),
        color(color_range(hexc("ff3060"), hexc("30c0ff")), param="Paper"),
        rotation(rng(0, 360), rng(0, 360), rng(0, 360)),
        event("OnBirth", "Spin On", sets=[set_row("Slot", "Spin", (1, 1, 1), 1.0)]),
        event("OnCollision", "Land", sets=[set_row("Slot", "Spin", (0.3, 0.3, 0.3), 1.0, multiply=True)]),
        spin(rng(-300, 300), rng(-300, 300), rng(-300, 300), slot="Spin"),
        collision(radius=0.03, bounce=0.2, friction=0.9),
        gravity(0, -9.8, 0, scale="Gravity"),
        drag(0.6),
        noise(2.0, 1.0, 1.0, param="Flutter"),
        sprite_render("paper", additive=False, align="Particle", lighting=True),
        max_particles=400),
    emitter("Pop",
        burst(1),
        position("Point"),
        lifetime(0.25),
        size(curve([(0, 0.3), (1, 1.2)], top=1.5), "Size"),
        color(hexc("ffffff"), alpha=curve([(0, 0.7), (1, 0)]), brightness=1.0),
        sprite_render("ring", additive=True),
        max_particles=4),
], duration=4.0,
   slots=["Spin"], floats=[param_float("Amount"), param_float("Force"), param_float("Size", 1, 0.2, 3), param_float("Lifetime", 1, 0.2, 3),
           param_float("Gravity", 1, 0, 3), param_float("Flutter")],
   colors=[param_color("Paper", color_range(hexc("ff3060"), hexc("30c0ff")))])

# --- Firework -------------------------------------------------------------
effect("fireworks/firework", [
    emitter("Rocket",
        burst(1),
        position("Point"),
        velocity(rng(-0.4, 0.4), 12, rng(-0.4, 0.4), scale="Height"),
        lifetime(1.0),
        size(0.05, "Size"),
        color(param="Rocket", brightness=2.0, bright_param="Brightness"),
        stretch(6),
        gravity(0, -9.8, 0),
        sprite_render("spark", additive=True, face=True, blur=True, blur_amount=0.8, blur_spacing=0.4, blur_opacity=0.5),
        max_particles=4),
    emitter("Rocket Trail",
        rate(60, "Trail"),
        position("Point"),
        velocity(rng(-0.4, 0.4), 12, rng(-0.4, 0.4), scale="Height"),
        lifetime(rng(0.3, 0.6)),
        size(rng(0.02, 0.04), "Size"),
        color(param="Rocket", alpha=curve([(0, 1), (1, 0)]), brightness=1.5, bright_param="Brightness"),
        gravity(0, -9.8, 0),
        drag(6),
        sprite_render("dot", additive=True),
        max_particles=80, duration=0.9),
    emitter("Burst",
        burst(220, "Stars"),
        position("Line", line=((0, 7.1, 0), (0, 7.1, 0))),
        velocity(0, 0, 0, scatter=fb(7.0, "Spread")),
        lifetime(rng(1.4, 2.4), "Lifetime"),
        size(rng(0.03, 0.06), "Size"),
        color(param="Stars Color", alpha=curve([(0, 1), (0.6, 1), (0.8, 0.3), (0.9, 1), (1, 0)]), brightness=1.8, bright_param="Brightness"),
        stretch(2.5),
        gravity(0, -3.5, 0, scale="Gravity"),
        drag(1.2),
        sprite_render("spark", additive=True, face=True, blur=True, blur_amount=0.6, blur_spacing=0.4, blur_opacity=0.5),
        max_particles=300, delay=1.0),
    emitter("Flash",
        burst(1),
        position("Line", line=((0, 7.1, 0), (0, 7.1, 0))),
        lifetime(0.2),
        size(curve([(0, 1.5), (1, 3.5)], top=4), "Size"),
        color(hexc("fff0d0"), alpha=curve([(0, 0.8), (1, 0)], mode="Linear"), brightness=1.5, bright_param="Brightness"),
        sprite_render("glow", additive=True),
        light(hexc("ffc890"), brightness=15, radius=10, ratio=1, max_lights=1, use_particle=False, param="Glow"),
        max_particles=4, delay=1.0),
], duration=4.0,
   floats=[param_float("Stars"), param_float("Spread"), param_float("Height", 1, 0.5, 1.5), param_float("Size", 1, 0.2, 3),
           param_float("Lifetime", 1, 0.2, 3), param_float("Brightness"), param_float("Gravity", 1, 0, 3), param_float("Trail"), param_float("Glow")],
   colors=[param_color("Stars Color", gradient([(0, hexc("ffffff")), (0.3, hexc("ffd040")), (0.7, hexc("ff4080")), (1, hexc("6030ff"))])),
           param_color("Rocket", hexc("ffd8a0"))])

# --- Energy beam ----------------------------------------------------------
effect("combat/beam", [
    emitter("Core",
        rate(500, "Density"),
        position("Line", line=((0, 0, 0), (0, 0, -6))),
        lifetime(0.5, "Lifetime"),
        size(rng(0.08, 0.13), "Size"),
        color(param="Beam", alpha=0.5, brightness=1.3, alpha_param="Opacity", bright_param="Brightness"),
        sprite_render("glow", additive=True),
        max_particles=400),
    emitter("Motes",
        rate(120, "Motes"),
        position("Line", line=((0, 0, 0), (0, 0, -6))),
        velocity(rng(-0.5, 0.5), rng(-0.5, 0.5), rng(-0.5, 0.5), scale="Scatter"),
        lifetime(rng(0.4, 0.9), "Lifetime"),
        size(rng(0.015, 0.035), "Size"),
        color(param="Beam", alpha=curve([(0, 1), (1, 0)]), brightness=1.5, bright_param="Brightness"),
        drag(0.8),
        sprite_render("spark", additive=True, face=True, blur=True, blur_amount=0.5, blur_spacing=0.3, blur_opacity=0.5),
        max_particles=200),
    emitter("Impact",
        rate(60, "Impact"),
        position("Line", line=((0, 0, -6), (0, 0, -6))),
        velocity(rng(-2, 2), rng(-2, 2), rng(0.5, 2.5), scale="Scatter"),
        lifetime(rng(0.3, 0.7), "Lifetime"),
        size(rng(0.02, 0.04), "Size"),
        color(param="Beam", alpha=curve([(0, 1), (1, 0)]), brightness=1.5, bright_param="Brightness"),
        stretch(3),
        gravity(0, -6, 0),
        sprite_render("spark", additive=True, face=True),
        light(hexc("60c0ff"), brightness=6, radius=3, ratio=0.1, max_lights=2, use_particle=True, param="Glow"),
        max_particles=100),
    emitter("Impact Ring",
        rate(2, "Impact"),
        position("Line", line=((0, 0, -6), (0, 0, -6))),
        lifetime(0.6, "Lifetime"),
        size(curve([(0, 0.2), (1, 1.4)], top=1.5), "Size"),
        color(param="Beam", alpha=curve([(0, 0.6), (1, 0)]), brightness=1.0, bright_param="Brightness"),
        sprite_render("ring", additive=True, align="Particle"),
        max_particles=8),
], duration=5,
   floats=[param_float("Density"), param_float("Motes"), param_float("Impact"), param_float("Size", 1, 0.2, 3),
           param_float("Lifetime", 1, 0.2, 3), param_float("Opacity", 1, 0, 2), param_float("Brightness"), param_float("Scatter"), param_float("Glow")],
   colors=[param_color("Beam", gradient([(0, hexc("ffffff")), (0.5, hexc("60c0ff")), (1, hexc("2060ff"))]))])

# --- Rain -----------------------------------------------------------------
# The player stands on the ground: the drops are born seven metres up and
# the splashes where they land, which is where the effect's origin is.
effect("ambient/rain", [
    emitter("Drops",
        rate(700, "Density"),
        position("Box", box=(7, 0.3, 7), offset=(0, 7, 0)),
        velocity(0, -11, 0, param="Fall", scale="Speed"),
        lifetime(0.75),
        size(rng(0.012, 0.02), "Size"),
        color(param="Water", alpha=0.55, alpha_param="Opacity"),
        stretch(9),
        gravity(0, 0, 0, param="Wind"),
        sprite_render("dot", additive=True, face=True),
        max_particles=1200),
    emitter("Splashes",
        rate(220, "Splash"),
        position("Box", box=(7, 0.05, 7)),
        velocity(rng(-0.5, 0.5), rng(0.6, 1.4), rng(-0.5, 0.5)),
        lifetime(rng(0.2, 0.35)),
        size(rng(0.015, 0.03), "Size"),
        color(param="Water", alpha=curve([(0, 0.8), (1, 0)]), alpha_param="Opacity"),
        gravity(0, -9.8, 0),
        sprite_render("dot", additive=True),
        max_particles=300),
    emitter("Ripples",
        rate(50, "Splash"),
        position("Box", box=(7, 0.02, 7)),
        lifetime(0.5),
        size(curve([(0, 0.02), (1, 0.16)], top=0.2), "Size"),
        color(param="Water", alpha=curve([(0, 0.5), (1, 0)]), alpha_param="Opacity"),
        rotation(90, 0, 0),
        sprite_render("ring", additive=True, align="Particle"),
        max_particles=100),
], duration=5,
   floats=[param_float("Density"), param_float("Speed"), param_float("Splash"), param_float("Size", 1, 0.2, 3), param_float("Opacity", 1, 0, 2)],
   vectors=[param_vec("Fall", (0, -11, 0)), param_vec("Wind", (0, 0, 0))],
   colors=[param_color("Water", hexc("c8dcf0"))])

print("done")

# ================================================================ CHAINED AND 3D
# Sub-effects first: a chained effect is a file of its own, played where a
# particle of another one died - see SpawnEffectOnDeathModule.

# --- Crackle: the last stage of the firework chain -------------------------
effect("fireworks/crackle", [
    emitter("Crackle",
        burst(10, "Count"),
        position("Point"),
        velocity(0, 0, 0, scatter=fb(1.5, "Spread")),
        lifetime(rng(0.2, 0.45), "Lifetime"),
        size(rng(0.02, 0.04), "Size"),
        color(param="Color", alpha=curve([(0, 1), (0.7, 1), (1, 0)]), brightness=1.8, bright_param="Brightness"),
        stretch(2),
        drag(1.0),
        sprite_render("spark", additive=True, face=True),
        max_particles=40),
], duration=0.6, looping=False,
   floats=[param_float("Count"), param_float("Spread"), param_float("Lifetime", 1, 0.2, 3), param_float("Size", 1, 0.2, 3), param_float("Brightness")],
   colors=[param_color("Color", hexc("ffffff"))])

# --- Firework burst: stars with ribbons, each crackling as it goes out ------
effect("fireworks/firework_burst", [
    emitter("Stars",
        burst(70, "Stars"),
        position("Point"),
        velocity(0, 0, 0, scatter=fb(4.5, "Spread")),
        lifetime(rng(1.6, 2.4), "Lifetime"),
        size(rng(0.04, 0.06), "Size"),
        color(param="Stars Color", alpha=curve([(0, 1), (0.7, 1), (1, 0)]), brightness=1.8, bright_param="Brightness"),
        gravity(0, -3.5, 0, scale="Gravity"),
        drag(1.1),
        sprite_render("spark", additive=True, face=True),
        trail_render(width=0.03, color=gradient([(0, hexc("ffffff", 0.9)), (1, hexc("ff8040", 0.0))]), life=0.45, max_points=24, point_distance=0.06),
        on_death("fireworks/crackle", chance=0.6, scale=1.0, max_alive=40),
        max_particles=120),
    emitter("Flash",
        burst(1),
        position("Point"),
        lifetime(0.2),
        size(curve([(0, 1.5), (1, 3.5)], top=4), "Size"),
        color(hexc("fff0d0"), alpha=curve([(0, 0.8), (1, 0)], mode="Linear"), brightness=1.5, bright_param="Brightness"),
        sprite_render("glow", additive=True),
        light(hexc("ffc890"), brightness=15, radius=10, ratio=1, max_lights=1, use_particle=False, param="Glow"),
        max_particles=4),
], duration=2.5, looping=False,
   floats=[param_float("Stars"), param_float("Spread"), param_float("Lifetime", 1, 0.2, 3), param_float("Size", 1, 0.2, 3),
           param_float("Brightness"), param_float("Gravity", 1, 0, 3), param_float("Glow")],
   colors=[param_color("Stars Color", gradient([(0, hexc("ffffff")), (0.3, hexc("ffd040")), (0.7, hexc("ff4080")), (1, hexc("6030ff"))]))])

# --- Firework, chained: rocket -> burst where it actually died -> crackles --
effect("fireworks/firework_chain", [
    emitter("Rocket",
        burst(1),
        position("Point"),
        velocity(rng(-1.5, 1.5), rng(11, 13), rng(-1.5, 1.5), scale="Height"),
        lifetime(rng(0.9, 1.2)),
        size(0.05, "Size"),
        color(param="Rocket", brightness=2.0, bright_param="Brightness"),
        stretch(4),
        gravity(0, -9.8, 0),
        sprite_render("spark", additive=True, face=True),
        trail_render(width=0.035, color=gradient([(0, hexc("ffd8a0", 0.9)), (1, hexc("ff6020", 0.0))]), life=0.6, max_points=40, point_distance=0.08),
        on_death("fireworks/firework_burst", scale=1.0, max_alive=6, scale_param="Burst Size"),
        light(hexc("ffc890"), brightness=3, radius=3, ratio=1, max_lights=1, use_particle=False),
        max_particles=4),
    emitter("Launch Smoke",
        burst(12),
        position("Point"),
        velocity(rng(-0.6, 0.6), rng(0.3, 1.2), rng(-0.6, 0.6)),
        lifetime(rng(1.0, 2.0)),
        size(curve([(0, 0.15), (1, 0.7)], top=0.8)),
        color(hexc("8a8a8a"), alpha=curve([(0, 0.4), (1, 0)])),
        rotation(0, 0, rng(0, 360)),
        drag(0.8),
        sprite_render("smoke4", additive=False, lighting=True, sort=True),
        max_particles=30),
], duration=3.5,
   floats=[param_float("Height", 1, 0.5, 1.5), param_float("Size", 1, 0.2, 3), param_float("Brightness"), param_float("Burst Size", 1, 0.3, 3)],
   colors=[param_color("Rocket", hexc("ffd8a0"))])

# --- Impact: what a meteor leaves - 3D rubble, a shockwave, dust -----------
effect("combat/impact", [
    emitter("Flash",
        burst(1),
        position("Point"),
        lifetime(0.15),
        size(curve([(0, 1.0), (1, 2.6)], top=3), "Size"),
        color(hexc("ffd0a0"), alpha=curve([(0, 0.8), (1, 0)], mode="Linear"), brightness=1.3, bright_param="Brightness"),
        sprite_render("glow", additive=True),
        light(hexc("ff9040"), brightness=20, radius=8, ratio=1, max_lights=1, use_particle=False, param="Glow"),
        max_particles=4),
    emitter("Shockwave",
        burst(1),
        position("Point"),
        lifetime(0.6),
        size(curve([(0, 0.3), (1, 4.5)], top=5), "Size"),
        color(hexc("ffc090"), alpha=curve([(0, 0.6), (1, 0)]), brightness=1.0),
        rotation(90, 0, 0),
        sprite_render("ring", additive=True, align="Particle"),
        max_particles=4),
    emitter("Rubble",
        burst(24, "Rubble"),
        position("Sphere", radius=0.2),
        velocity(0, 4, 0, scatter=fb(4.5, "Power")),
        lifetime(rng(2.5, 4.0), "Lifetime"),
        size(rng(0.08, 0.22), "Size"),
        color(color_range(hexc("4a3a30"), hexc("8a7a68"))),
        rotation(rng(0, 360), rng(0, 360), rng(0, 360)),
        event("OnBirth", "Spin On", sets=[set_row("Slot", "Spin", (1, 1, 1), 1.0)]),
        event("OnCollision", "Land", sets=[set_row("Slot", "Spin", (0.25, 0.25, 0.25), 1.0, multiply=True)]),
        spin(rng(-500, 500), rng(-500, 500), rng(-500, 500), slot="Spin"),
        collision(radius=0.08, bounce=0.35, friction=0.8),
        gravity(0, -9.8, 0),
        drag(0.15),
        mesh_render("models/dev/box.mdl", "materials/fx/stylized_stone.mat", scale=1.0, rotate=False, shadows=True,
                    shader=[("Dissolve", 1, fb(0.0)), ("Edge", 1, fb(0.1)), ("Emission", 1, fb(0.9)), ("Scroll", 1, fb(0.0))]),
        max_particles=60),
    emitter("Embers",
        burst(60, "Power"),
        position("Point"),
        velocity(0, 3, 0, scatter=fb(5.0, "Power")),
        lifetime(rng(0.6, 1.4), "Lifetime"),
        size(rng(0.025, 0.045), "Size"),
        color(color_range(hexc("ffd890"), hexc("ff8030")), alpha=curve([(0, 1), (0.7, 1), (1, 0)]), brightness=2.0, bright_param="Brightness"),
        stretch(2.5),
        collision(radius=0.03, bounce=0.4, friction=0.5),
        gravity(0, -9.8, 0),
        drag(0.8),
        sprite_render("spark", additive=True, face=True, blur=True, blur_amount=0.4, blur_spacing=0.3, blur_opacity=0.4),
        max_particles=200),
    emitter("Dust",
        burst(26, "Dust"),
        position("Sphere", radius=0.5),
        velocity(0, 0.6, 0, scatter=fb(1.6, "Power")),
        lifetime(rng(1.8, 3.0), "Lifetime"),
        size(curve([(0, 0.6), (1, 2.6)], top=3), "Size"),
        color(gradient([(0, hexc("8a7a68")), (1, hexc("3a3430"))]), alpha=curve([(0, 0.6), (0.4, 0.45), (1, 0)])),
        rotation(0, 0, rng(0, 360)),
        spin(0, 0, rng(-30, 30)),
        drag(0.8),
        gravity(0, 0.5, 0),
        sprite_render("smoke1", additive=False, lighting=True, sort=True),
        max_particles=60, delay=0.05),
], duration=4.5, looping=False,
   slots=["Spin"], floats=[param_float("Power"), param_float("Rubble"), param_float("Dust"), param_float("Size", 1, 0.2, 3), param_float("Lifetime", 1, 0.2, 3),
           param_float("Brightness"), param_float("Glow")])

# --- Meteor: a 3D sphere falling with a fire trail, impacting where it lands -
effect("combat/meteor", [
    emitter("Rock",
        burst(1),
        position("Box", box=(3, 0.5, 3), offset=(-7, 9, 0)),
        velocity(rng(6.5, 7.5), rng(-6.5, -7.5), rng(-0.5, 0.5), scale="Speed"),
        lifetime(4.0),
        size(rng(0.22, 0.3), "Size"),
        color(gradient([(0, hexc("ffb070")), (1, hexc("ff6020"))]), brightness=1.3),
        rotation(rng(0, 360), rng(0, 360), rng(0, 360)),
        spin(rng(-300, 300), rng(-300, 300), rng(-300, 300)),
        collision(radius=0.15, bounce=0.0, friction=1.0, die=1.0),
        gravity(0, -4, 0),
        model_render(("models/dev/sphere.mdl",), scale=1.0, shadows=True),
        trail_render(width=0.18, color=gradient([(0, hexc("ffd090", 0.8)), (0.5, hexc("ff6020", 0.5)), (1, hexc("401000", 0.0))]),
                     life=0.7, max_points=48, point_distance=0.1, width_param="Trail"),
        on_death("combat/impact", scale=1.0, max_alive=3, on_expiry=False, scale_param="Impact"),
        light(hexc("ff9040"), brightness=8, radius=5, ratio=1, max_lights=1, use_particle=False, param="Glow"),
        max_particles=4),
    emitter("Fire Puffs",
        rate(70),
        position("Box", box=(3, 0.5, 3), offset=(-7, 9, 0)),
        velocity(rng(6.5, 7.5), rng(-6.5, -7.5), rng(-0.5, 0.5), scale="Speed"),
        lifetime(rng(0.25, 0.5)),
        size(curve([(0, 0.25), (1, 0.7)], top=0.8), "Size"),
        color(param="Fire", alpha=curve([(0, 0.7), (1, 0)]), brightness=1.2),
        rotation(0, 0, rng(0, 360)),
        gravity(0, -4, 0),
        drag(3.0),
        sprite_render("smoke3", additive=True),
        max_particles=80, duration=1.05),
    emitter("Sparks",
        rate(60),
        position("Box", box=(3, 0.5, 3), offset=(-7, 9, 0)),
        velocity(rng(6.5, 7.5), rng(-6.5, -7.5), rng(-0.5, 0.5), scatter=1.5, scale="Speed"),
        lifetime(rng(0.3, 0.8)),
        size(rng(0.02, 0.04), "Size"),
        color(hexc("ffc070"), alpha=curve([(0, 1), (1, 0)]), brightness=1.8),
        stretch(3),
        gravity(0, -9.8, 0),
        drag(1.5),
        sprite_render("spark", additive=True, face=True),
        max_particles=100, duration=1.05),
], duration=3.5,
   floats=[param_float("Speed", 1, 0.5, 2), param_float("Size", 1, 0.2, 3), param_float("Trail", 1, 0, 3), param_float("Impact", 1, 0.3, 3), param_float("Glow")],
   colors=[param_color("Fire", gradient([(0, hexc("fff0c0")), (0.4, hexc("ff9030")), (1, hexc("802000"))]))])

# --- Orrery: planets are meshes parked By Index on Circle shapes and turned
#     by the clock (Follow Shape with Speed - one immortal particle each, no
#     rate-per-life trick); a moon rides its planet through a slot the
#     planet writes and the moon orbits around; the sun is one mesh in the
#     ember shader with a corona and a light; each orbit is a ring of dots
#     parked on the same shape.
def planet(name, shape_name, speed, colour, radius_m, phase=0.0):
    return emitter(name,
        burst(1),
        position_on(shape_name, "ByTime", along=fb(phase)),
        lifetime(10000.0),
        size(radius_m, "Size"),
        color(param=colour, brightness=1.0),
        spin(0, rng(30, 60), 0),
        follow(shape_name, along=fb(phase), speed=fb(speed, "Spin"), loop=True),
        mesh_render("models/dev/sphere.mdl", "materials/fx/stylized_white.mat", scale=1.0, rotate=False, shadows=True,
                    shader=[("Dissolve", 1, fb(0.0)), ("Edge", 1, fb(0.05)), ("Emission", 1, fb(0.9)), ("Fresnel", 1, fb(0.6))]),
        trail_render(width=0.35, color=hexc("ffffff", 0.35), life=0.9, max_points=60, point_distance=0.04, scale_from=True, tint=True),
        light(hexc("ffffff"), brightness=1.2, radius=2.0, ratio=1, max_lights=1, use_particle=True),
        max_particles=1)

def orbit_ring(name, shape_name, count):
    return emitter(name,
        burst(count),
        position_on(shape_name, "ByIndex"),
        lifetime(10000.0),
        size(0.012, "Size"),
        color(hexc("c0d0e0"), alpha=0.22, brightness=1.0),
        follow(shape_name, sample="ByIndex", along=fb(0.0), speed=fb(0.0)),
        sprite_render("dot", additive=True),
        max_particles=count, places=count)

effect("shapes/swarm", [
    emitter("Sun",
        burst(1),
        position("Point"),
        lifetime(10000.0),
        size(0.5, "Size"),
        color(hexc("ffffff"), brightness=1.0),
        spin(0, 20, 0),
        mesh_render("models/dev/sphere.mdl", "materials/fx/stylized_ember.mat", scale=1.0, rotate=False, shadows=False,
                    shader=[("Dissolve", 1, fb(0.0)), ("Edge", 1, fb(0.1)), ("Emission", 1, fb(2.5, "Glow")), ("Scroll", 1, fb(0.15))]),
        max_particles=1),
    emitter("Corona",
        rate(3),
        position("Point"),
        lifetime(1.2),
        size(curve([(0, 0.9), (0.5, 1.3), (1, 0.9)], top=1.5), "Size"),
        color(hexc("ffd8a0"), alpha=curve([(0, 0), (0.5, 0.35), (1, 0)]), brightness=1.2),
        sprite_render("glow", additive=True),
        light(hexc("ffd8a0"), brightness=6, radius=5, ratio=0.5, max_lights=1, use_particle=False, param="Glow"),
        max_particles=8),
    emitter("Flares",
        rate(6, "Glow"),
        position("Sphere", radius=0.5, shell=True),
        velocity(0, 0, 0, scatter=0.0),
        lifetime(rng(0.6, 1.0)),
        size(curve([(0, 0.05), (0.4, 0.22), (1, 0.0)], top=0.3)),
        color(hexc("ffb040"), alpha=curve([(0, 0), (0.3, 0.9), (1, 0)]), brightness=2.0),
        transform_over_life(offset=vb(0, curve([(0, 0), (1, 0.3)], top=0.5), 0)),
        sprite_render("flame", additive=True),
        max_particles=20),
    orbit_ring("Orbit 1", "Orbit 1", 80),
    orbit_ring("Orbit 2", "Orbit 2", 120),
    orbit_ring("Orbit 3", "Orbit 3", 160),
    planet("Inner Planet", "Orbit 1", 0.2, "Inner", 0.16, 0.0),
    planet("Middle Planet", "Orbit 2", -0.11, "Middle", 0.28, 0.4),
    planet("Outer Planet", "Orbit 3", 0.07, "Outer", 0.22, 0.75),
    emitter("Dust",
        rate(25, "Count"),
        position("Circle", radius=2.6),
        lifetime(rng(3, 5), "Lifetime"),
        size(rng(0.012, 0.025), "Size"),
        color(hexc("e0e8ff"), alpha=curve([(0, 0), (0.3, 0.5), (1, 0)]), brightness=1.0),
        orbit(15, (0, 1, 0), "Spin"),
        noise(0.15, 1.0, 0.5),
        sprite_render("dot", additive=True),
        max_particles=150),
], duration=8,
   shapes=[shape("Orbit 1", "Circle", radius=1.0, shell=True, rot=(0, 0, 6)),
           shape("Orbit 2", "Circle", radius=1.7, shell=True, rot=(0, 0, -4)),
           shape("Orbit 3", "Circle", radius=2.5, shell=True, rot=(0, 0, 3))],
   floats=[param_float("Spin", 1, -3, 3), param_float("Count"), param_float("Size", 1, 0.2, 3), param_float("Lifetime", 1, 0.2, 3), param_float("Glow")],
   colors=[param_color("Inner", hexc("60d0ff")), param_color("Middle", hexc("ffb060")), param_color("Outer", hexc("c080ff"))])

# --- Sparkler: sparks with ribbons, thrown from a spinning point -----------
effect("fireworks/sparkler", [
    emitter("Sparks",
        rate(50, "Rate"),
        position("Point"),
        velocity(0, 0, 0, scatter=fb(4.0, "Force")),
        lifetime(rng(0.6, 1.2), "Lifetime"),
        size(rng(0.02, 0.035), "Size"),
        color(param="Color", alpha=curve([(0, 1), (0.6, 1), (1, 0)]), brightness=2.0, bright_param="Brightness"),
        stretch(2),
        collision(radius=0.02, bounce=0.5, friction=0.3),
        gravity(0, -9.8, 0),
        drag(0.6),
        sprite_render("spark", additive=True, face=True),
        trail_render(width=0.018, color=gradient([(0, hexc("ffffff", 0.9)), (0.5, hexc("ffc060", 0.5)), (1, hexc("ff6020", 0.0))]),
                     life=0.35, max_points=20, point_distance=0.04),
        max_particles=250),
    emitter("Core",
        rate(30),
        position("Point"),
        lifetime(0.15),
        size(rng(0.15, 0.3), "Size"),
        color(hexc("fff8e0"), alpha=curve([(0, 0.9), (1, 0)]), brightness=1.5),
        sprite_render("glow", additive=True),
        light(hexc("ffe0a0"), brightness=6, radius=3, ratio=0.2, max_lights=2, use_particle=False, param="Glow"),
        max_particles=12),
], duration=5,
   floats=[param_float("Rate"), param_float("Force"), param_float("Lifetime", 1, 0.2, 3), param_float("Size", 1, 0.2, 3), param_float("Brightness"), param_float("Glow")],
   colors=[param_color("Color", gradient([(0, hexc("ffffff")), (0.5, hexc("ffd080")), (1, hexc("ff8040"))]))])

# --- Singularity: everything falls in, ribbons streak to a 3D core ---------
effect("magic/singularity", [
    emitter("Core",
        rate(1),
        position("Point"),
        lifetime(1.2),
        size(0.35, "Size"),
        color(hexc("100818")),
        rotation(rng(0, 360), rng(0, 360), rng(0, 360)),
        spin(0, rng(60, 120), 0),
        model_render(("models/dev/sphere.mdl",), scale=1.0, shadows=False),
        max_particles=4),
    emitter("Halo",
        rate(4),
        position("Point"),
        lifetime(1.0),
        size(curve([(0, 0.7), (1, 1.1)], top=1.2), "Size"),
        color(param="Halo", alpha=curve([(0, 0), (0.4, 0.5), (1, 0)]), brightness=1.3),
        sprite_render("glow", additive=True),
        light(hexc("a060ff"), brightness=8, radius=6, ratio=0.5, max_lights=1, use_particle=False, param="Glow"),
        max_particles=12),
    emitter("Infall",
        rate(30, "Density"),
        position("Sphere", radius=3.0, shell=True),
        lifetime(rng(2.0, 3.0), "Lifetime"),
        size(rng(0.02, 0.05), "Size"),
        color(param="Streaks", alpha=curve([(0, 0), (0.15, 1), (0.9, 1), (1, 0)]), brightness=1.5, bright_param="Brightness"),
        orbit(90, (0, 1, 0), "Spin"),
        attractor(strength=2.5, size=0.35, falloff=0.6, param="Pull", mult=2.5),
        drag(0.2),
        sprite_render("spark", additive=True, face=True),
        trail_render(width=0.02, color=gradient([(0, hexc("c0a0ff", 0.6)), (1, hexc("4020a0", 0.0))]), life=0.4, max_points=36, point_distance=0.035),
        max_particles=400),
    emitter("Disc",
        rate(120, "Density"),
        position("Circle", radius=1.8, shell=True),
        lifetime(rng(1.5, 2.5), "Lifetime"),
        size(rng(0.015, 0.03), "Size"),
        color(param="Disc", alpha=curve([(0, 0), (0.2, 0.8), (1, 0)]), brightness=1.3, bright_param="Brightness"),
        orbit(220, (0, 1, 0), "Spin"),
        attractor(strength=0.8, size=0.35, falloff=0.6, param="Pull", mult=0.8),
        sprite_render("dot", additive=True),
        max_particles=500),
], duration=6,
   floats=[param_float("Spin", 1, -3, 3), param_float("Pull"), param_float("Density"), param_float("Size", 1, 0.2, 3),
           param_float("Lifetime", 1, 0.2, 3), param_float("Brightness"), param_float("Glow")],
   colors=[param_color("Halo", hexc("8040ff")), param_color("Streaks", gradient([(0, hexc("ffffff")), (1, hexc("a060ff"))])),
           param_color("Disc", gradient([(0, hexc("ffe0c0")), (1, hexc("ff60a0"))]))])

# ================================================================ MESHES
# --- Stylised fire: one flame mesh, its blend shapes and shader driven ------
def wobble(*vals):
    """A curve that starts and ends alike, so a looping one-particle effect does not pop."""
    pts = [(i / (len(vals) - 1), v) for i, v in enumerate(vals)]
    return curve(pts, top=1.0)

effect("ambient/mesh_fire", [
    emitter("Flame",
        burst(1),
        position("Point"),
        lifetime(4.0),
        size(1.0, "Size"),
        color(param="Tint", brightness=1.0),
        mesh_render("models/fx/flame.mdl", "materials/fx/stylized_fire.mat", scale=1.0, rotate=True,
                    morphs=[("Lean", fb(wobble(0.1, 0.7, 0.2, 0.9, 0.4, 0.8, 0.1), "Sway")),
                            ("Flicker", fb(wobble(0.3, 0.9, 0.2, 0.7, 1.0, 0.4, 0.3), "Flicker")),
                            ("Bulge", fb(wobble(0.0, 0.5, 0.1, 0.6, 0.2, 0.0), "Flicker"))],
                    shader=[("Dissolve", 1, fb(wobble(0.3, 0.42, 0.28, 0.45, 0.3), "Burn")),
                            ("Edge", 1, fb(0.1)),
                            ("Emission", 1, fb(1.3, "Intensity")),
                            ("Scroll", 1, fb(1.3, "Speed")),
                            ("Fresnel", 1, fb(0.0))]),
        light(hexc("ff9a40"), brightness=8, radius=4, ratio=1, max_lights=1, use_particle=False, param="Glow"),
        max_particles=4),
    emitter("Inner",
        burst(1),
        position("Point", offset=(0, 0.05, 0)),
        lifetime(4.0),
        size(0.55, "Size"),
        color(hexc("fff4d0"), brightness=1.0),
        mesh_render("models/fx/flame.mdl", "materials/fx/stylized_fire.mat", scale=1.0, rotate=True,
                    morphs=[("Flicker", fb(wobble(0.8, 0.3, 1.0, 0.5, 0.9, 0.8), "Flicker")),
                            ("Lean", fb(wobble(0.0, 0.3, 0.0, 0.4, 0.1, 0.0), "Sway"))],
                    shader=[("Dissolve", 1, fb(0.45, "Burn")), ("Edge", 1, fb(0.15)), ("Emission", 1, fb(1.8, "Intensity")), ("Scroll", 1, fb(2.0, "Speed"))]),
        max_particles=4),
    emitter("Embers",
        rate(10, "Embers"),
        position("Circle", radius=0.2),
        velocity(rng(-0.3, 0.3), rng(1.5, 2.5), rng(-0.3, 0.3)),
        lifetime(rng(1.2, 2.4)),
        size(rng(0.02, 0.04)),
        color(hexc("ffc070"), alpha=curve([(0, 1), (0.7, 1), (1, 0)]), brightness=1.5),
        noise(1.2, 1.2, 2.0),
        drag(0.3),
        sprite_render("spark", additive=True, face=True),
        max_particles=60),
], duration=4.0,
   floats=[param_float("Intensity"), param_float("Flicker", 1, 0, 2), param_float("Sway", 1, 0, 2), param_float("Burn", 1, 0, 3),
           param_float("Speed"), param_float("Size", 1, 0.2, 3), param_float("Embers"), param_float("Glow")],
   colors=[param_color("Tint", hexc("ffffff"))])

# --- Shield: a sphere that breathes, rim-lit, spiking when hit -----------
effect("magic/mesh_shield", [
    emitter("Shell",
        burst(1),
        position("Point"),
        lifetime(3.0),
        size(1.0, "Size"),
        color(param="Tint", brightness=1.0),
        mesh_render("models/fx/shield.mdl", "materials/fx/stylized_shield.mat", scale=1.0, rotate=True,
                    morphs=[("Breathe", fb(wobble(0.0, 1.0, 0.0), "Breathe")),
                            ("Spike", fb(curve([(0, 0), (0.1, 0.8), (0.4, 0.1), (0.7, 0.6), (1, 0)]), "Spikes"))],
                    shader=[("Dissolve", 1, fb(0.35, "Holes")), ("Edge", 1, fb(0.12)), ("Emission", 1, fb(0.9, "Intensity")),
                            ("Scroll", 1, fb(0.6, "Speed")), ("Fresnel", 1, fb(2.0, "Rim"))]),
        light(hexc("60c0ff"), brightness=6, radius=4, ratio=1, max_lights=1, use_particle=False, param="Glow"),
        max_particles=4),
    emitter("Motes",
        rate(30, "Motes"),
        position("Sphere", radius=0.8, shell=True),
        lifetime(rng(1.0, 2.0)),
        size(rng(0.02, 0.04)),
        color(hexc("a0e0ff"), alpha=curve([(0, 0), (0.3, 0.8), (1, 0)]), brightness=1.3),
        orbit(60, (0, 1, 0), "Speed"),
        sprite_render("dot", additive=True),
        max_particles=100),
], duration=3.0,
   floats=[param_float("Intensity"), param_float("Breathe", 1, 0, 2), param_float("Spikes", 1, 0, 2), param_float("Holes", 1, 0, 2),
           param_float("Rim", 1, 0, 2), param_float("Speed"), param_float("Size", 1, 0.2, 3), param_float("Motes"), param_float("Glow")],
   colors=[param_color("Tint", hexc("ffffff"))])

# --- Dissolving shards: 3D chunks that burn away as they lie there --------
effect("combat/mesh_shards", [
    emitter("Shards",
        burst(18, "Count"),
        position("Sphere", radius=0.2),
        velocity(0, 4, 0, scatter=fb(4.0, "Force")),
        lifetime(rng(2.5, 4.0), "Lifetime"),
        size(rng(0.12, 0.25), "Size"),
        color(hexc("ffffff"), brightness=1.0),
        rotation(rng(0, 360), rng(0, 360), rng(0, 360)),
        # The spin is multiplied by slot "Spin": one at birth, cut by each
        # landing - so a shard on the floor lies still instead of turning.
        event("OnBirth", "Spin On", sets=[set_row("Slot", "Spin", (1, 1, 1), 1.0)]),
        event("OnCollision", "Land", sets=[set_row("Slot", "Spin", (0.3, 0.3, 0.3), 1.0, multiply=True)]),
        spin(rng(-400, 400), rng(-400, 400), rng(-400, 400), slot="Spin"),
        collision(radius=0.08, bounce=0.35, friction=0.8),
        gravity(0, -9.8, 0),
        drag(0.15),
        mesh_render("models/dev/box.mdl", "materials/fx/stylized_stone.mat", scale=1.0, rotate=False, shadows=True,
                    shader=[("Dissolve", 1, fb(curve([(0, 0.0), (0.4, 0.05), (1, 0.85)]), "Burn")),
                            ("Edge", 1, fb(0.12)),
                            ("Emission", 1, fb(curve([(0, 2.5), (0.5, 1.5), (1, 0.3)], top=3), "Intensity")),
                            ("Scroll", 1, fb(0.4))]),
        max_particles=60),
    emitter("Flash",
        burst(1),
        position("Point"),
        lifetime(0.15),
        size(curve([(0, 0.8), (1, 2.0)], top=2), "Size"),
        color(hexc("ffd0a0"), alpha=curve([(0, 0.8), (1, 0)], mode="Linear"), brightness=1.3),
        sprite_render("glow", additive=True),
        light(hexc("ff9040"), brightness=15, radius=6, ratio=1, max_lights=1, use_particle=False, param="Glow"),
        max_particles=4),
], duration=4.5,
   floats=[param_float("Count"), param_float("Force"), param_float("Lifetime", 1, 0.2, 3), param_float("Size", 1, 0.2, 3),
           param_float("Burn", 1, 0, 2), param_float("Intensity"), param_float("Glow")], slots=["Spin"])

# --- Formation: one burst parked on a grid, blended to a ring and a helix --
#
# Three shapes and three Follow Shape modules in a row, each pulling the
# particle towards its own shape by a weight: the grid always, the ring and
# the helix by curves over the life, scaled by a parameter each. Colour and
# size are read By Index, so the formation is a rainbow from first born to
# last rather than a random one.
RAINBOW = gradient_by_index([(0, hexc("ff4060")), (0.25, hexc("ffc040")), (0.5, hexc("40ff90")), (0.75, hexc("40a0ff")), (1, hexc("e060ff"))])

effect("shapes/formation", [
    emitter("Beads",
        burst(96),
        position_on("Grid", "ByIndex"),
        lifetime(11.6),
        size(by_index([(0, 0.08), (0.5, 0.16), (1, 0.08)], top=0.2), "Size"),
        color(RAINBOW, alpha=curve([(0, 0), (0.05, 1), (0.95, 1), (1, 0)], mode="Linear"), brightness=1.1),
        follow("Grid", sample="ByIndex", along=fb(0.0), weight=fb(1.0), name="Park On Grid"),
        follow("Ring", sample="ByIndex", along=fb(0.0), speed=fb(0.08, "Spin"), weight=fb(curve([(0, 0), (0.22, 0), (0.32, 1), (0.62, 1), (0.72, 0), (1, 0)]), "Ring"), name="Blend To Ring"),
        follow("Helix", sample="ByIndex", along=fb(0.0), speed=fb(-0.06, "Spin"), weight=fb(curve([(0, 0), (0.52, 0), (0.62, 1), (0.9, 1), (1, 1)]), "Helix"), name="Blend To Helix"),
        sprite_render("glow", additive=True),
        max_particles=128, places=96),
    emitter("Dust",
        rate(40),
        position_on("Ring", "Random"),
        velocity(0, 0.3, 0, scatter=0.2),
        lifetime(rng(0.8, 1.4)),
        size(rng(0.02, 0.05)),
        color(hexc("a0c0ff"), alpha=curve([(0, 0), (0.2, 0.5), (1, 0)]), brightness=1.2),
        sprite_render("dot", additive=True),
        max_particles=100),
], duration=12.0, looping=True,
   shapes=[shape("Grid", "Grid", offset=(0, 1.2, 0), grid=(12, 1, 8), spacing=(0.28, 0.28, 0.28)),
           shape("Ring", "Circle", offset=(0, 1.2, 0), radius=1.6, shell=True, count=96),
           shape("Helix", "Helix", offset=(0, 0.3, 0), radius=1.0, height=2.6, turns=3, count=96)],
   floats=[param_float("Ring", 1, 0, 1), param_float("Helix", 1, 0, 1), param_float("Spin", 1, 0, 3), param_float("Size", 1, 0.2, 3)])

# --- Snake: a spline walked by time, and sparks that remember their home ---
#
# The head rides the spline over its life and the ribbon behind it is the
# body; the scales are a rate of beads walking the same path, so the train
# is the rate. The sparks are born anywhere on the path, remember where
# (Remember -> slot "Home"), and are pulled back to it by an attractor whose
# position is read out of that slot - one attractor, a different target for
# every particle.
SNAKE_PATH = [(-2.2, 0.6, -0.8), (-1.2, 1.6, 0.9), (0.4, 0.5, 1.4), (1.9, 1.3, 0.3), (2.3, 0.7, -1.2), (0.8, 1.9, -1.8), (-0.9, 0.9, -1.9)]

effect("shapes/snake", [
    # One head that never dies, moved by the clock (Speed: a lap every four
    # seconds) rather than by its life - so the ribbon behind it is one ribbon.
    emitter("Head",
        burst(1),
        position_on("Path", "ByTime", along=fb(0.0)),
        lifetime(10000.0),
        size(0.34, "Size"),
        color(hexc("d0ffb0"), brightness=2.0),
        follow("Path", along=fb(0.0), speed=fb(0.25, "Speed"), loop=True, align=True),
        sprite_render("glow", additive=True),
        light(hexc("80ff60"), brightness=6, radius=3, ratio=1, max_lights=1, use_particle=False),
        trail_render(width=0.22, color=hexc("60d040"), life=1.6, max_points=64, point_distance=0.03, scale_from=True, tint=True),
        max_particles=1),
    emitter("Scales",
        rate(30),
        position_on("Path", "ByTime", along=fb(0.0)),
        lifetime(4.0),
        size(by_index([(0, 0.05), (1, 0.12)]), "Size"),
        color(gradient_by_index([(0, hexc("b0ff80")), (1, hexc("2080ff"))]), alpha=curve([(0, 0), (0.05, 0.9), (0.95, 0.9), (1, 0)]), brightness=1.5),
        follow("Path", along=fb(curve([(0, 0), (1, 1)], mode="Linear"), "Speed"), loop=True),
        sprite_render("dot", additive=True),
        max_particles=200, places=30),
    emitter("Sparks",
        rate(50, "Sparks"),
        position_on("Path", "Random"),
        remember("Home", "Position"),
        velocity(0, 0, 0, scatter=2.5),
        lifetime(rng(1.2, 2.0)),
        size(rng(0.015, 0.035)),
        color(hexc("ffe080"), alpha=curve([(0, 1), (0.8, 1), (1, 0)]), brightness=1.8),
        stretch(2.0),
        mod("AttractorModule", "Update", "Pull Home", Space="World", Position=slot_vb("Home"), Strength=fb(14.0, "Pull"), Size=0.05, Invert=False, Falloff=0.0),
        drag(1.2),
        sprite_render("spark", additive=True, face=True),
        max_particles=300),
], duration=8.0, looping=True,
   shapes=[shape("Path", "Spline", points=SNAKE_PATH, closed=True)],
   slots=["Home"],
   floats=[param_float("Speed", 1, 0.2, 3), param_float("Size", 1, 0.2, 3), param_float("Sparks", 1, 0, 3), param_float("Pull", 1, 0, 3)])

# --- Buff aura: the real case - a heal or a level-up on a character ------
#
# What a gameplay effect actually needs from stage 2: eight runes parked
# on a ring By Index and turned by the clock (one immortal burst, so they
# never pop), streamers riding a helix up over their life with ribbons,
# motes born on the rim of a cone. Every shape is offset from the player's
# feet, so the effect is dropped on a character and just fits.
effect("magic/buff_aura", [
    emitter("Runes",
        burst(8),
        position_on("Ring", "ByIndex"),
        lifetime(10000.0),
        size(0.14, "Size"),
        color(gradient_by_index([(0, hexc("ffe680")), (0.5, hexc("ffffff")), (1, hexc("ffe680"))]), brightness=1.8),
        follow("Ring", sample="ByIndex", along=fb(0.0), speed=fb(0.12, "Spin"), name="Turn The Ring"),
        sprite_render("ring", additive=True),
        light(hexc("ffd060"), brightness=1.5, radius=1.2, ratio=1, max_lights=8, use_particle=True),
        max_particles=8, places=8),
    emitter("Streamers",
        rate(10, "Intensity"),
        position_on("Helix", "ByTime", along=fb(0.0)),
        lifetime(1.8),
        size(curve([(0, 0.02), (0.3, 0.06), (1, 0.0)], top=0.1)),
        color(gradient([(0, hexc("80ffb0")), (0.6, hexc("40e0ff")), (1, hexc("ffffff"))]), brightness=2.0),
        follow("Helix", along=fb(curve([(0, 0), (1, 1)], mode="Linear"), "Rise"), loop=False, align=True),
        sprite_render("glow", additive=True),
        trail_render(width=0.05, color=hexc("60ffc0"), life=0.6, max_points=32, point_distance=0.04, scale_from=True, tint=True),
        max_particles=60),
    emitter("Motes",
        rate(40, "Intensity"),
        position_on("Rim", "Random"),
        velocity(0, 0.5, 0, scatter=0.15),
        lifetime(rng(1.2, 2.0)),
        size(rng(0.015, 0.03)),
        color(hexc("c0ffe0"), alpha=curve([(0, 0), (0.2, 0.8), (1, 0)]), brightness=1.5),
        drag(0.4),
        sprite_render("dot", additive=True),
        max_particles=120),
    emitter("Ground Glow",
        burst(1),
        position("Point", offset=(0, 0.05, 0)),
        lifetime(10000.0),
        size(2.2, "Size"),
        color(hexc("60ffb0"), alpha=0.18, brightness=1.0),
        sprite_render("glow", additive=True, align="LookAtCamera"),
        max_particles=1),
], duration=6.0, looping=True,
   shapes=[shape("Ring", "Circle", offset=(0, 0.15, 0), radius=0.9, shell=True, count=8),
           shape("Helix", "Helix", offset=(0, 0.1, 0), radius=0.55, height=2.4, turns=1.5),
           shape("Rim", "Cone", offset=(0, 0.0, 0), radius=0.4, cone=65, shell=True)],
   floats=[param_float("Spin", 1, -3, 3), param_float("Rise", 1, 0.2, 3), param_float("Intensity", 1, 0, 3), param_float("Size", 1, 0.2, 3)])

# --- DNA: two helix shapes, one turned half round, and beads that sit
#     between them - a chain of Follow Shape weights, not a special module.
effect("shapes/dna", [
    emitter("Strand A",
        burst(44),
        position_on("Strand A", "ByIndex"),
        lifetime(10000.0),
        size(0.07, "Size"),
        color(gradient_by_index([(0, hexc("40a0ff")), (1, hexc("80ffff"))]), brightness=1.5),
        follow("Strand A", sample="ByIndex", along=fb(0.0), speed=fb(0.06, "Spin")),
        sprite_render("glow", additive=True),
        max_particles=44, places=44),
    emitter("Strand B",
        burst(44),
        position_on("Strand B", "ByIndex"),
        lifetime(10000.0),
        size(0.07, "Size"),
        color(gradient_by_index([(0, hexc("ff8040")), (1, hexc("ffe080"))]), brightness=1.5),
        follow("Strand B", sample="ByIndex", along=fb(0.0), speed=fb(0.06, "Spin")),
        sprite_render("glow", additive=True),
        max_particles=44, places=44),
    # Parked on A, then pulled halfway to B: the midpoint of each rung.
    emitter("Rungs",
        burst(44),
        position_on("Strand A", "ByIndex"),
        lifetime(10000.0),
        size(0.035, "Size"),
        color(gradient_by_index([(0, hexc("c0c0ff")), (1, hexc("ffffff"))]), brightness=1.2),
        follow("Strand A", sample="ByIndex", along=fb(0.0), speed=fb(0.06, "Spin"), name="Park On A"),
        follow("Strand B", sample="ByIndex", along=fb(0.0), speed=fb(0.06, "Spin"), weight=fb(0.5), name="Halfway To B"),
        sprite_render("dot", additive=True),
        max_particles=44, places=44),
    emitter("Fizz",
        rate(30, "Fizz"),
        position_on("Strand A", "Random"),
        velocity(0, 0, 0, scatter=0.3),
        lifetime(rng(0.5, 1.0)),
        size(rng(0.01, 0.02)),
        color(hexc("a0e0ff"), alpha=curve([(0, 1), (1, 0)]), brightness=1.5),
        sprite_render("dot", additive=True),
        max_particles=60),
], duration=6.0, looping=True,
   shapes=[shape("Strand A", "Helix", offset=(0, 0.2, 0), radius=0.5, height=3.0, turns=2.0, count=44),
           shape("Strand B", "Helix", offset=(0, 0.2, 0), rot=(0, 180, 0), radius=0.5, height=3.0, turns=2.0, count=44)],
   floats=[param_float("Spin", 1, -3, 3), param_float("Size", 1, 0.2, 3), param_float("Fizz", 1, 0, 3)])

# --- Jelly: slots holding a shape together. Four hundred motes fill a box,
#     each remembers where it was born, and one attractor whose position is
#     read out of that slot springs every one of them back home - so noise
#     can shake the cube and it wobbles rather than scatters.
effect("shapes/jelly", [
    emitter("Motes",
        burst(400),
        position_on("Body", "Random"),
        remember("Home", "Position"),
        velocity(0, 0, 0, scatter=0.4),
        lifetime(10000.0),
        size(rng(0.02, 0.035), "Size"),
        color(gradient_by_index([(0, hexc("ff60a0")), (0.5, hexc("c060ff")), (1, hexc("60c0ff"))]), brightness=1.4),
        mod("AttractorModule", "Update", "Spring Home", Space="World", Position=slot_vb("Home"), Strength=fb(24.0, "Stiffness"), Size=0.02, Invert=False, Falloff=0.0),
        noise(strength=2.5, scale=1.2, timescale=1.5, param="Shake"),
        drag(1.5, "Damping"),
        sprite_render("dot", additive=True),
        max_particles=400),
    emitter("Sheen",
        rate(20),
        position_on("Body", "Random"),
        lifetime(rng(0.4, 0.8)),
        size(rng(0.04, 0.08)),
        color(hexc("ffffff"), alpha=curve([(0, 0), (0.3, 0.5), (1, 0)]), brightness=1.5),
        sprite_render("glow", additive=True),
        max_particles=40),
], duration=6.0, looping=True,
   shapes=[shape("Body", "Box", offset=(0, 0.9, 0), box=(1.2, 1.2, 1.2))],
   slots=["Home"],
   floats=[param_float("Stiffness", 1, 0, 3), param_float("Shake", 1, 0, 4), param_float("Damping", 1, 0.2, 3), param_float("Size", 1, 0.2, 3)])

# --- Homing: missiles thrown any which way that a Goal pulls onto a moving
#     anchor over their life; puffs at the launcher shaped by Transform Over
#     Life; a glow that rides the target through an emitter anchor.
effect("combat/homing", [
    emitter("Missiles",
        rate(5, "Rate"),
        position("Sphere", radius=0.15, offset=(0, 0.4, 0)),
        velocity(0, 2.5, 0, scatter=2.5),
        lifetime(1.7),
        size(0.08),
        color(gradient([(0, hexc("ffffff")), (0.5, hexc("ff8040")), (1, hexc("ff2020"))]), brightness=2.0),
        gravity(0, -3, 0),
        drag(1.2),
        goal("Anchor", anchor="Target", position=fb(curve([(0, 0), (0.3, 0.0), (0.75, 0.9), (1, 1)]), "Pull"), align=True),
        sprite_render("glow", additive=True),
        trail_render(width=0.06, color=hexc("ff9040"), life=0.5, max_points=40, point_distance=0.03, scale_from=True, tint=True),
        event("OnGoalReached", "Hit", distance=0.12, effect_="fireworks/crackle", scale=0.5, max_alive=8,
              sets=[set_row("LifeLeft", value=(0, 0, 0))], context=[ctx("Color", "Color")]),
        max_particles=40),
    emitter("Launch Puffs",
        rate(8, "Rate"),
        position("Circle", radius=0.15, offset=(0, 0.3, 0)),
        lifetime(rng(0.9, 1.3)),
        size(0.25),
        color(hexc("707880"), alpha=curve([(0, 0.5), (1, 0)], mode="Linear")),
        rotation(0, 0, rng(0, 360)),
        transform_over_life(offset=vb(0, curve([(0, 0), (1, 1.4)], top=1.5), 0), scale=fb(curve([(0, 0.4), (1, 2.2)], top=2.5))),
        sprite_render("smoke1", additive=False, lighting=True, sort=True),
        max_particles=30),
    emitter("Target Glow",
        rate(30),
        position("Point"),
        lifetime(0.1),
        size(0.5),
        color(hexc("ff6040"), alpha=0.6, brightness=1.4),
        sprite_render("glow", additive=True),
        light(hexc("ff5030"), brightness=4, radius=2.5, ratio=1, max_lights=1, use_particle=False),
        max_particles=6, anchor="Target"),
], duration=4.0, looping=True,
   anchors=[anchor("Target", offset=(0, 1.6, -2.2))],
   floats=[param_float("Rate", 1, 0, 3), param_float("Pull", 1, 0, 1)])

# --- Slash: the cut itself, not a sword. Two crescents in an X: each is one
#     particle riding an arc of a Circle shape over a third of a second, a
#     wide ribbon tapering behind it (width from the particle's size curve),
#     a thin white core over it, sparks sizzling on the arc while it lives,
#     a ring pushed out by Transform Over Life and a flash.
def crescent(tag, arc, delay, colour, core):
    return [
        emitter(f"Crescent {tag}",
            burst(1),
            position_on(arc, "ByTime", along=fb(0.28)),
            lifetime(0.32),
            size(curve([(0, 0.05), (0.25, 0.6), (0.7, 0.55), (1, 0.05)], top=0.7), "Width"),
            color(colour, brightness=2.2),
            follow(arc, along=fb(curve([(0, 0.28), (1, 0.74)], mode="Linear")), loop=False, align=True),
            sprite_render("glow", additive=True, scale=0.6),
            trail_render(width=1.0, color=colour, life=0.28, max_points=40, point_distance=0.01, scale_from=True, tint=True, taper=(1.0, 0.35), fade=(1.0, 0.0)),
            max_particles=1, delay=delay),
        emitter(f"Core {tag}",
            burst(1),
            position_on(arc, "ByTime", along=fb(0.28)),
            lifetime(0.32),
            size(curve([(0, 0.02), (0.3, 0.12), (1, 0.02)], top=0.2), "Width"),
            color(core, brightness=3.0),
            follow(arc, along=fb(curve([(0, 0.28), (1, 0.74)], mode="Linear")), loop=False),
            sprite_render("glow", additive=True, scale=0.5),
            trail_render(width=1.0, color=core, life=0.4, max_points=40, point_distance=0.01, scale_from=True, tint=True, taper=(1.0, 0.5)),
            light(core, brightness=6, radius=3, ratio=1, max_lights=1, use_particle=False),
            max_particles=1, delay=delay),
        emitter(f"Sizzle {tag}",
            rate(400, "Sparks"),
            position_on(arc, "ByTime", along={"Type": "Range", "Evaluation": "Frame", "Constants": "0.28,0.74,0,0"}),
            velocity(0, 0, 0, scatter=fb(1.8, "Sparks")),
            lifetime(rng(0.2, 0.5)),
            size(rng(0.012, 0.03)),
            color(colour, alpha=curve([(0, 1), (0.7, 1), (1, 0)]), brightness=2.0),
            stretch(3.0),
            gravity(0, -6, 0),
            drag(1.5),
            sprite_render("spark", additive=True, face=True),
            max_particles=200, delay=delay, duration=0.3),
    ]

CUT_A, CUT_B = hexc("60d0ff"), hexc("ff70c0")

effect("combat/slash", [
    *crescent("A", "Arc A", 0.0, CUT_A, hexc("e0f8ff")),
    *crescent("B", "Arc B", 0.42, CUT_B, hexc("ffe0f8")),
    emitter("Shockwave",
        burst(1),
        position("Point"),
        lifetime(0.45),
        size(0.6),
        color(hexc("a0e0ff"), alpha=curve([(0, 0.9), (1, 0)], mode="Linear"), brightness=1.5),
        rotation(90, 0, 0),
        transform_over_life(scale=fb(curve([(0, 0.3), (1, 4.0)], top=4), "Width")),
        sprite_render("ring", additive=True, align="Particle"),
        max_particles=1, delay=0.12),
    emitter("Flash",
        burst(1),
        position("Point"),
        lifetime(0.2),
        size(curve([(0, 1.2), (1, 2.2)], top=2.5)),
        color(hexc("ffffff"), alpha=curve([(0, 0.8), (1, 0)], mode="Linear"), brightness=1.5),
        sprite_render("glow", additive=True),
        max_particles=1, delay=0.5),
    emitter("Embers",
        burst(30),
        position("Sphere", radius=0.6),
        velocity(0, 1.5, 0, scatter=3.0),
        lifetime(rng(0.6, 1.2)),
        size(rng(0.015, 0.03)),
        color(gradient([(0, hexc("ffffff")), (0.4, hexc("80c0ff")), (1, hexc("ff60c0"))]), alpha=curve([(0, 1), (0.7, 1), (1, 0)]), brightness=2.0),
        gravity(0, -4, 0),
        drag(1.2),
        sprite_render("dot", additive=True),
        max_particles=40, delay=0.5),
], duration=1.6, looping=True,
   shapes=[shape("Arc A", "Circle", radius=1.3, rot=(90, 0, 35), shell=True),
           shape("Arc B", "Circle", radius=1.3, rot=(90, 0, -35), shell=True)],
   floats=[param_float("Width", 1, 0.2, 3), param_float("Sparks", 1, 0, 3)])

# --- Assemble: mesh shards with the dissolve shader, scattered in a sphere,
#     pulled by a Goal onto a grid wall By Index - position and rotation
#     weights on one curve, so they fly in tumbling and lock flat - hold,
#     then burn away, with ribbons while they fly and a crackle as they go.
GATHER = curve([(0, 0), (0.12, 0), (0.45, 1), (1, 1)])

effect("magic/assemble", [
    emitter("Shards",
        burst(48),
        position_on("Scatter", "Random"),
        velocity(0, 0, 0, scatter=1.5),
        lifetime(4.2),
        size(0.11, "Size"),
        color(hexc("ffffff")),
        rotation(rng(0, 360), rng(0, 360), rng(0, 360)),
        spin(rng(-300, 300), rng(-300, 300), rng(-300, 300)),
        drag(0.6),
        goal("Shape", shape_name="Wall", sample="ByIndex", position=fb(GATHER, "Gather"), rotation=fb(GATHER, "Gather"), write_velocity=True),
        mesh_render("models/dev/box.mdl", "materials/fx/stylized_ember.mat", scale=1.0, rotate=False,
                    shader=[("Dissolve", 1, fb(curve([(0, 0.7), (0.3, 0.05), (0.8, 0.0), (0.92, 0.5), (1, 1.0)]))),
                            ("Edge", 1, fb(0.15)),
                            ("Emission", 1, fb(curve([(0, 3.0), (0.45, 1.2), (0.8, 1.0), (1, 3.5)], top=4), "Glow")),
                            ("Scroll", 1, fb(0.6))]),
        on_death("fireworks/crackle", chance=1.0, scale=0.4, on_collision=False, on_expiry=True, max_alive=16),
        max_particles=48, places=48),
    emitter("Lock Flash",
        burst(1),
        position("Point", offset=(0, 1.5, 0)),
        lifetime(0.35),
        size(curve([(0, 0.5), (1, 2.6)], top=3)),
        color(hexc("ffd0a0"), alpha=curve([(0, 0.8), (1, 0)], mode="Linear"), brightness=1.5),
        sprite_render("glow", additive=True),
        light(hexc("ff9040"), brightness=10, radius=5, ratio=1, max_lights=1, use_particle=False),
        max_particles=1, delay=1.9),
    emitter("Dust",
        rate(25),
        position_on("Scatter", "Random"),
        lifetime(rng(1.0, 2.0)),
        size(rng(0.015, 0.03)),
        color(hexc("ffc080"), alpha=curve([(0, 0), (0.3, 0.6), (1, 0)]), brightness=1.2),
        sprite_render("dot", additive=True),
        max_particles=60),
], duration=4.4, looping=True,
   shapes=[shape("Scatter", "Sphere", offset=(0, 1.5, 0), radius=2.2),
           shape("Wall", "Grid", offset=(0, 1.5, 0), grid=(8, 6, 1), spacing=(0.24, 0.24, 0.24), rot=(0, 0, 0))],
   floats=[param_float("Gather", 1, 0, 1), param_float("Glow", 1, 0, 3), param_float("Size", 1, 0.2, 3)])

# --- Tesla: arcs between two anchors on two swinging arms. A bolt is one
#     short-lived particle whose Goal runs it along the Line between the
#     anchors at weight 0.8 - the other fifth is its own scattered, noised
#     motion, which is the zigzag - drawn by the ribbon behind it. Sparks
#     and glows ride the anchors through emitter anchors.
def bolt(name, rate_, life):
    # One particle crawls the line over its life; its Goal weight is a new
    # random number every frame, so how far it sits off the line - which is
    # its own scattered, noised motion - changes every frame: the zigzag.
    # Two ribbons on one particle: a thin white core and a wide faint haze.
    return emitter(name,
        rate(rate_, "Arcs"),
        position_on("Gap", "ByTime", along=fb(0.0)),
        velocity(0, 0, 0, scatter=0.5),
        lifetime(life),
        size(0.04),
        color(hexc("f0f8ff"), brightness=3.0),
        noise(strength=70.0, scale=10.0, timescale=8.0),
        drag(14.0),
        goal("Shape", shape_name="Gap", sample="ByTime", along=fb(curve([(0, 0), (1, 1)], mode="Linear")),
             position=fb({"Type": "Range", "Evaluation": "Frame", "Constants": "0.5,0.85,0,0"}), write_velocity=False),
        sprite_render("glow", additive=True, scale=1.0),
        trail_render(width=0.006, color=hexc("ffffff"), life=life * 1.2, max_points=110, point_distance=0.04, scale_from=False, tint=True, taper=None, fade=None),
        trail_render(width=0.025, color=hexc("3070ff", 0.3), life=life * 1.2, max_points=110, point_distance=0.04, scale_from=False, tint=False, taper=None, fade=None),
        light(hexc("a0c8ff"), brightness=4, radius=2.5, ratio=1, max_lights=4, use_particle=True),
        max_particles=12)

def tesla_end(anchor_name):
    return [
        emitter(f"Glow {anchor_name}",
            rate(30), position("Point"), lifetime(0.1), size(0.28),
            color(hexc("a0d0ff"), alpha=0.5, brightness=1.4),
            sprite_render("glow", additive=True),
            light(hexc("80b0ff"), brightness=3, radius=2, ratio=1, max_lights=1, use_particle=False),
            max_particles=6, anchor=anchor_name),
        emitter(f"Sparks {anchor_name}",
            rate(12, "Arcs"), position("Sphere", radius=0.06),
            velocity(0, 0.3, 0, scatter=1.2), lifetime(rng(0.2, 0.5)), size(rng(0.008, 0.016)),
            color(hexc("c0e0ff"), alpha=curve([(0, 1), (1, 0)]), brightness=2.0), stretch(2.5),
            gravity(0, -9.8, 0), collision(radius=0.02, bounce=0.4, friction=0.5),
            sprite_render("spark", additive=True, face=True),
            max_particles=60, anchor=anchor_name),
    ]

effect("combat/tesla", [
    bolt("Bolts", 4, 0.35),
    *tesla_end("A"),
    *tesla_end("B"),
], duration=4.0, looping=True,
   anchors=[anchor("A", offset=(-1.5, 1.5, 0)), anchor("B", offset=(1.5, 1.5, 0))],
   shapes=[shape("Gap", "Line", line_anchors=("A", "B"))],
   floats=[param_float("Arcs", 1, 0, 3)])

# --- Shatter: a real broken model. Sixteen pieces of an urn, one particle
#     each, born on the Model shape By Parts - so each particle is told its
#     piece and the Mesh draws only that piece about its own middle. A Goal
#     back to the same shape is the urn whole; while the weight is down the
#     pieces are physics - thrown, falling, bouncing - and the weight coming
#     back gathers them home, turning them upright on the way.
WHOLE = curve([(0, 0), (0.42, 0), (0.62, 1), (1, 1)])

effect("combat/shatter", [
    emitter("Pieces",
        burst(16),
        position_on("Urn", "ByIndex"),
        lifetime(5.0),
        size(1.0),
        color(hexc("ffffff")),
        velocity(0, 2.0, 0, scatter=fb(1.8, "Force")),
        event("OnBirth", "Spin On", sets=[set_row("Slot", "Spin", (1, 1, 1), 1.0)]),
        event("OnCollision", "Land", sets=[set_row("Slot", "Spin", (0.25, 0.25, 0.25), 1.0, multiply=True)]),
        spin(rng(-400, 400), rng(-400, 400), rng(-400, 400), slot="Spin"),
        collision(radius=0.08, bounce=0.35, friction=0.7),
        gravity(0, -9.8, 0),
        drag(0.2),
        goal("Shape", shape_name="Urn", sample="ByIndex", position=fb(WHOLE, "Assemble"), rotation=fb(WHOLE, "Assemble"), write_velocity=False),
        mesh_render("models/props/urn_broken.mdl", "materials/fx/stylized_clay.mat", scale=1.0, rotate=False, shadows=True, part_from_particle=True,
                    shader=[("Dissolve", 1, fb(0.0)), ("Edge", 1, fb(0.1)),
                            ("Emission", 1, fb(curve([(0, 3.0), (0.15, 1.2), (0.7, 1.0), (0.8, 2.5), (1, 0.9)], top=3), "Glow")),
                            ("Scroll", 1, fb(0.1))]),
        max_particles=16, places=16),
    emitter("Burst Flash",
        burst(1),
        position("Point", offset=(0, 0.6, 0)),
        lifetime(0.3),
        size(curve([(0, 0.4), (1, 2.4)], top=3)),
        color(hexc("ffd0a0"), alpha=curve([(0, 0.9), (1, 0)], mode="Linear"), brightness=1.5),
        sprite_render("glow", additive=True),
        light(hexc("ff9040"), brightness=10, radius=5, ratio=1, max_lights=1, use_particle=False),
        max_particles=1, delay=0.0),
    emitter("Dust",
        burst(40),
        position("Sphere", radius=0.35, offset=(0, 0.6, 0)),
        velocity(0, 1.0, 0, scatter=2.5),
        lifetime(rng(0.8, 1.6)),
        size(curve([(0, 0.15), (1, 0.6)], top=1)),
        color(hexc("8a7a68"), alpha=curve([(0, 0.5), (1, 0)], mode="Linear")),
        rotation(0, 0, rng(0, 360)),
        gravity(0, -1.5, 0),
        drag(1.5),
        sprite_render("smoke1", additive=False, lighting=True, sort=True),
        max_particles=40, delay=0.0),
], duration=5.0, looping=True,
   shapes=[shape("Urn", "Model", model="models/props/urn_broken.mdl", model_sample="Parts", offset=(0, 0, 0))],
   slots=["Spin"], floats=[param_float("Assemble", 1, 0, 1), param_float("Force", 1, 0, 3), param_float("Glow", 1, 0, 3)])

# --- Chain reaction: three effects handing colour and direction down.
#     A rocket is born a random colour; at a second it kills itself and
#     spawns a burst told its Color and its Velocity (as the burst's
#     Direction); each spark of the burst that hits the ground spawns a pop
#     told the colour again. Nothing here knows the next effect's insides -
#     only the names of its parameters.
effect("fireworks/chain_pop", [
    emitter("Ring",
        burst(1),
        position("Point"),
        lifetime(0.3),
        size(curve([(0, 0.1), (1, 0.7)], top=1)),
        color(param="Color", alpha=curve([(0, 0.9), (1, 0)], mode="Linear"), brightness=2.0),
        rotation(90, 0, 0),
        sprite_render("ring", additive=True, align="Particle"),
        max_particles=1),
    emitter("Bits",
        burst(8),
        position("Point"),
        velocity(0, 1.2, 0, scatter=1.2),
        lifetime(rng(0.25, 0.5)),
        size(rng(0.012, 0.02)),
        color(param="Color", alpha=curve([(0, 1), (1, 0)]), brightness=2.0),
        stretch(2.0),
        gravity(0, -6, 0),
        sprite_render("spark", additive=True, face=True),
        max_particles=8),
], duration=0.6, looping=False, colors=[param_color("Color", hexc("ffffff"))])

effect("fireworks/chain_burst", [
    emitter("Sparks",
        burst(36),
        position("Sphere", radius=0.05),
        velocity(0, 0, 0, param="Direction", mult=0.35, scatter=3.0),
        lifetime(rng(0.7, 1.3)),
        size(rng(0.02, 0.035)),
        color(param="Color", alpha=curve([(0, 1), (0.8, 1), (1, 0)]), brightness=2.2),
        stretch(2.5),
        collision(radius=0.02, bounce=0.3, friction=0.6),
        gravity(0, -9.8, 0),
        drag(0.5),
        event("OnCollision", "Pop", once=True, chance=0.6, effect_="fireworks/chain_pop", scale=0.6, max_alive=12, context=[ctx("Color", "Color")]),
        sprite_render("spark", additive=True, face=True),
        trail_render(width=0.014, color=hexc("ffffff"), life=0.25, max_points=16, point_distance=0.03, scale_from=False, tint=True),
        max_particles=40),
    emitter("Flash",
        burst(1),
        position("Point"),
        lifetime(0.2),
        size(curve([(0, 0.5), (1, 1.4)], top=1.5)),
        color(param="Color", alpha=curve([(0, 0.9), (1, 0)], mode="Linear"), brightness=1.5),
        sprite_render("glow", additive=True),
        light(brightness=8, radius=4, ratio=1, max_lights=1, use_particle=True),
        max_particles=1),
], duration=1.5, looping=False,
   vectors=[param_vec("Direction", (0, 6, 0))], colors=[param_color("Color", hexc("ffffff"))])

effect("fireworks/chain_rocket", [
    emitter("Rockets",
        rate(1.2, "Rate"),
        position("Circle", radius=0.15),
        velocity(0, 6.0, 0, scatter=1.6),
        lifetime(3.0),
        size(0.06),
        color(color_range(hexc("ff5050"), hexc("50a0ff")), brightness=2.0),
        gravity(0, -3, 0),
        event("OnTime", "Burst", at=1.0, at_param="Fuse", effect_="fireworks/chain_burst", max_alive=6,
              sets=[set_row("LifeLeft", value=(0, 0, 0))],
              context=[ctx("Color", "Color"), ctx("Velocity", "Direction")]),
        sprite_render("glow", additive=True),
        trail_render(width=0.03, color=hexc("ffffff"), life=0.4, max_points=32, point_distance=0.03, scale_from=False, tint=True),
        max_particles=8),
], duration=4.0, looping=True,
   floats=[param_float("Rate", 1, 0, 3), param_float("Fuse", 1, 0.3, 2)])
