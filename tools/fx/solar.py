"""The solar system: effects for the sun, every planet with its moons and rings,
the asteroid belt, a comet, the orbit lines and the stars - and the scene that
puts them together. Not to scale, but everything in it is what it is."""
import json, os, math
from fxgen import *          # the helpers; this also regenerates the showcase effects
import scenegen as sg        # the scene helpers (go, comp, label, ...); this regenerates the particles scene too

SUN = (0.0, 3.0, 0.0)
M = "materials/solar/"

# ------------------------------------------------------------------ helpers

def publish(anchor_name):
    """Every step, the particle's pose (and size) becomes the anchor named - what the HUD's focus list reads."""
    e = event("EveryStep", f"Publish {anchor_name}", sets=[set_row("Anchor", value=(0, 0, 0))])
    e["Set"][0]["AnchorName"] = anchor_name
    return e

def shadow_rows(caster):
    """The shader rows a body needs to be shadowed by the anchor named: Shadow as a vector read off it."""
    return [("Shadow", 3, vb(param=caster))] if caster else []

def body(name, material, diameter, spin_deg=0.0, shadows=True, emission=None, caster=None, wobble=None):
    """One immortal mesh sphere: the planet, the moon, the star. Wobble puts it on a small circle - a barycentre."""
    if wobble:
        wr, wp, wphase = wobble
        pin = follow("Wobble", along=fb(wphase), speed=fb(1.0 / wp, "Speed"), loop=True)
    else:
        pin = follow("Centre", along=fb(0.0))
    return emitter(name,
        burst(1),
        position("Point"),
        lifetime(10000.0),
        size(diameter),
        color(hexc("ffffff")),
        spin(0, spin_deg, 0),
        # Pinned to the effect's own origin every step, so a body whose
        # player is carried round an orbit goes with it - and published as
        # the "Planet" anchor, size and all, for anything that wants it.
        pin,
        publish("Planet"),
        mesh_render("models/dev/sphere.mdl", material, scale=1.0, rotate=False, shadows=shadows,
                    shader=[("Emission", 1, fb(1.0) if emission is None else emission), ("Dissolve", 1, fb(0.0))] + shadow_rows(caster)),
        max_particles=1)

CENTRE = shape("Centre", "Point")

def shell(name, material, diameter):
    """The atmosphere: a translucent shell a little over the world, in the atmosphere shader."""
    return emitter(name,
        burst(1),
        position("Point"),
        lifetime(10000.0),
        size(diameter),
        color(hexc("ffffff")),
        follow("Centre", along=fb(0.0)),
        mesh_render("models/dev/sphere.mdl", material, scale=1.0, rotate=False, shadows=False,
                    shader=[("Emission", 1, fb(1.0))], particle_attrs=False),
        max_particles=1)

def glow(name, colour, size_, alpha=0.18, light_=None):
    """A soft haze round a body - an atmosphere seen from far, a corona."""
    mods = [rate(3), position("Point"), local_space(), lifetime(1.0),
            size(curve([(0, size_ * 0.96), (0.5, size_), (1, size_ * 0.96)], top=size_)),
            color(colour, alpha=curve([(0, 0), (0.5, alpha), (1, 0)]), brightness=1.2),
            sprite_render("glow", additive=True)]
    if light_: mods.append(light_)
    return emitter(name, *mods, max_particles=6)

def moon(name, shape_name, material, diameter, period, phase=0.0, trail=True, child=None, eclipsed=True):
    mods = [burst(1), position_on(shape_name, "ByTime", along=fb(phase)), lifetime(10000.0), size(diameter), color(hexc("ffffff")),
            # Tidally locked: one turn a lap, the same face to the planet.
            spin(0, 360.0 / period, 0),
            follow(shape_name, along=fb(phase), speed=fb(1.0 / period, "Speed"), loop=True),
            mesh_render("models/dev/sphere.mdl", material, scale=1.0, rotate=False, shadows=True,
                        shader=[("Emission", 1, fb(1.0)), ("Dissolve", 1, fb(0.0))] + (shadow_rows("Planet") if eclipsed else []))]
    # Where the moon is, as the anchor of its name - what the planet's shadow
    # row reads for the caster, and what the HUD focuses on for all of them.
    mods.append(publish(name))
    if child:
        mods.append(event("OnBirth", "Rides", effect_=child, follow=True, max_alive=1, context=[]))
    if trail:
        mods.append(trail_render(width=diameter * 0.35, color=hexc("ffffff", 0.25), life=period * 0.12, max_points=48, point_distance=0.03, scale_from=False, tint=False))
    return emitter(name, *mods, max_particles=1)

SP = "models/space/"

def craft(name, shape_name, model, diameter, period, phase=0.0, material=None, trail=True, spin_deg=15.0, light_=None):
    """A spacecraft on a circle: the model, small, with a thin trail."""
    mods = [burst(1), position_on(shape_name, "ByTime", along=fb(phase)), lifetime(10000.0), size(diameter), color(hexc("ffffff")),
            spin(spin_deg * 0.3, spin_deg, 0),
            follow(shape_name, along=fb(phase), speed=fb(1.0 / period, "Speed"), loop=True),
            publish(name),
            mesh_render(SP + model + ".mdl", material, scale=1.0, rotate=False, shadows=True,
                        shader=[("Emission", 1, fb(1.0)), ("Dissolve", 1, fb(0.0))], particle_attrs=False)]
    if trail:
        mods.append(trail_render(width=diameter * 0.25, color=hexc("c0e0ff", 0.4), life=period * 0.15, max_points=40, point_distance=0.02, scale_from=False, tint=False))
    if light_:
        mods.append(light_)
    return emitter(name, *mods, max_particles=1)

def lander(name, model, diameter, place, radius):
    """A model standing on a world's surface: parked By Index on a sphere shell the size of the world, facing out."""
    return emitter(name,
        burst(1),
        position_on(place, "ByIndex", align=True),
        lifetime(10000.0),
        size(diameter),
        color(hexc("ffffff")),
        follow(place, sample="ByIndex", along=fb(0.0), align=True),
        publish(name),
        mesh_render(SP + model + ".mdl", None, scale=1.0, rotate=False, shadows=True,
                    shader=[("Emission", 1, fb(1.0)), ("Dissolve", 1, fb(0.0))], particle_attrs=False),
        max_particles=1, places=1)

def ring_band(name, shape_name, count, size_, colour, alpha, speed):
    """Dust parked By Index on a circle and turned by the clock - one band of a ring."""
    return emitter(name,
        burst(count),
        position_on(shape_name, "ByIndex"),
        lifetime(10000.0),
        size(rng(size_ * 0.6, size_ * 1.4)),
        color(colour, alpha=alpha, brightness=1.1),
        follow(shape_name, sample="ByIndex", along=fb(0.0), speed=fb(speed, "Speed")),
        sprite_render("dot", additive=False, lighting=False),
        max_particles=count, places=count)

def orbit_shape(name, radius, tilt=0.0, count=0):
    return shape(name, "Circle", radius=radius, shell=True, rot=(tilt, 0, 0), count=count)

# ------------------------------------------------------------------ the sun

effect("solar/sun", [
    body("Star", M + "sun.mat", 5.0, spin_deg=2.0, shadows=False, emission=fb(1.0, "Glow")),
    glow("Corona", hexc("ffc070"), 8.0, alpha=0.14,
         light_=light(hexc("fff0d0"), brightness=40, radius=90, ratio=1, max_lights=1, use_particle=False, param="Glow")),
    glow("Halo", hexc("ff9040"), 14.0, alpha=0.05),
    # The corona proper: long streamers standing off the limb, each a
    # stretched sprite thrown straight out and facing its motion.
    emitter("Streamers",
        rate(4, "Activity"),
        position("Sphere", radius=2.7, shell=True),
        lifetime(rng(2.5, 4.0)),
        size(curve([(0, 0.2), (0.3, 0.8), (1, 0.3)], top=1.0)),
        color(hexc("ffb060"), alpha=curve([(0, 0), (0.25, 0.06), (1, 0)]), brightness=1.4),
        stretch(3.0),
        attractor(strength=2.2, size=1.0, falloff=0.0, invert=True, space="Local"),
        drag(0.4),
        sprite_render("flame", additive=True, face=True),
        max_particles=60),
    # A coronal mass ejection, now and then: a bubble of plasma thrown
    # clear of the star, growing as it goes, with a skin of sparks.
    emitter("Ejections",
        rate(0.02, "Activity"),
        position("Sphere", radius=2.6, shell=True),
        lifetime(rng(6.0, 8.0)),
        size(curve([(0, 0.5), (0.5, 5.0), (1, 9.0)], top=10)),
        color(gradient([(0, hexc("fff0c0")), (0.4, hexc("ff9040")), (1, hexc("ff4010"))]), alpha=curve([(0, 0.7), (0.5, 0.3), (1, 0)]), brightness=2.0),
        attractor(strength=5.0, size=1.0, falloff=0.0, invert=True, space="Local"),
        event("OnBirth", "Skin", effect_="solar/cme_skin", follow=True, max_alive=3, context=[]),
        sprite_render("glow", additive=True),
        light(hexc("ffa060"), brightness=6, radius=20, ratio=1, max_lights=2, use_particle=False),
        max_particles=3),
    # Zodiacal light: the dust of the ecliptic, a faint flat disc round the star.
    emitter("Zodiacal Dust",
        burst(1400),
        position("Circle", radius=24.0, shell=False),
        lifetime(10000.0),
        size(rng(0.06, 0.16)),
        color(hexc("ffe8c0"), alpha=rng(0.05, 0.16), brightness=1.0),
        orbit(0.4, (0, 1, 0)),
        sprite_render("dot", additive=True),
        max_particles=1400),
    # Prominences: arcs of flame lifting off the surface and falling back.
    emitter("Prominences",
        rate(1.2, "Activity"),
        position("Sphere", radius=2.5, shell=True),
        lifetime(rng(2.0, 3.5)),
        size(curve([(0, 0.15), (0.3, 0.7), (1, 0.0)], top=0.8)),
        color(gradient([(0, hexc("fff0c0")), (0.4, hexc("ff8020")), (1, hexc("802000"))]), alpha=curve([(0, 0), (0.2, 0.6), (1, 0)]), brightness=2.0),
        rotation(0, 0, rng(0, 360)),
        spin(0, 0, rng(-30, 30)),
        attractor(strength=2.2, size=0.5, falloff=0.0, invert=True, space="Local"),
        drag(0.6),
        sprite_render("flame", additive=True),
        max_particles=20),
    # The wind: a faint stream of everything the star throws off, straight out.
    emitter("Solar Wind",
        rate(30, "Activity"),
        position("Sphere", radius=2.6, shell=True),
        lifetime(rng(4.0, 7.0)),
        size(rng(0.02, 0.05)),
        color(hexc("ffe0b0"), alpha=curve([(0, 0), (0.1, 0.5), (1, 0)]), brightness=1.5),
        attractor(strength=6.0, size=1.0, falloff=0.0, invert=True, space="Local"),
        sprite_render("dot", additive=True),
        max_particles=700),
    # Flares: rare bright arcs thrown far, with a ribbon.
    emitter("Flares",
        rate(0.12, "Activity"),
        position("Sphere", radius=2.5, shell=True),
        velocity(0, 0, 0, scatter=0.0),
        lifetime(rng(2.5, 4.0)),
        size(0.25),
        color(hexc("fff8e0"), alpha=curve([(0, 1), (0.7, 1), (1, 0)]), brightness=3.0),
        attractor(strength=9.0, size=1.0, falloff=0.0, invert=True, space="Local"),
        noise(2.0, 0.6, 1.0),
        drag(0.9),
        sprite_render("glow", additive=True),
        trail_render(width=0.16, color=hexc("ffb060", 0.9), life=1.2, max_points=64, point_distance=0.05, scale_from=False, tint=True),
        max_particles=4),
], duration=10, looping=True, shapes=[CENTRE], anchors=[anchor("Planet")],
   floats=[param_float("Glow", 1, 0, 3), param_float("Activity", 1, 0, 3)])

# ------------------------------------------------------------------ planets

def planet_effect(name, material, diameter, atmosphere=None, moons=(), rings=(), spin_deg=0.0, extra=(), extra_shapes=(), wobble=None):
    """A planet effect: the body, its haze, its moons on tilted circles, its rings.
    The first moon casts the eclipse shadow on the planet; every moon is shadowed by the planet."""
    caster = moons[0][0] if moons else None
    emitters = [body("Body", M + material, diameter, spin_deg=spin_deg, caster=caster, wobble=wobble)] + list(extra)
    shapes_ = [CENTRE] + list(extra_shapes)
    anchors_ = [anchor("Planet")] + [anchor(m_[0]) for m_ in moons] + [anchor(e["Name"]) for e in extra if any(m["__type"].endswith("EventModule") and m["Name"].startswith("Publish") for m in e["UpdateModules"])]
    if wobble:
        shapes_.append(orbit_shape("Wobble", wobble[0], 0.0))
    if atmosphere:
        colour, size_mult, alpha = atmosphere
        emitters.append(glow("Haze", colour, diameter * size_mult, alpha * 0.5))
        emitters.append(shell("Atmosphere", M + f"{name}_atmo.mat", diameter * 1.06))
    for m_ in moons:
        mname, mmat, mdiam, distance, period, tilt, phase = m_[:7]
        child = m_[7] if len(m_) > 7 else None
        sname = f"Orbit {mname}"
        shapes_.append(orbit_shape(sname, distance, tilt))
        emitters.append(moon(mname, sname, M + mmat, mdiam, period, phase, child=child))
    for i, (inner, outer, bands, count, size_, colour, alpha, tilt) in enumerate(rings):
        for b in range(bands):
            r = inner + (outer - inner) * (b + 0.5) / bands
            sname = f"Ring {i}.{b}"
            shapes_.append(orbit_shape(sname, r, tilt, count))
            emitters.append(ring_band(f"Ring {i}.{b}", sname, count, size_, colour, alpha, 0.02 * (inner / r)))
    effect(f"solar/{name}", emitters, duration=10, looping=True, shapes=shapes_, anchors=anchors_,
           floats=[param_float("Speed", 1, 0, 3)])

# Io's volcanoes: plumes of sulphur thrown up and falling back, riding the
# moon through an Event on its birth that spawns this and carries it along.
effect("solar/io_plumes", [
    emitter("Plumes",
        rate(14),
        position("Sphere", radius=0.1, shell=True),
        velocity(0, 0, 0, scatter=0.0),
        lifetime(rng(0.8, 1.4)),
        size(curve([(0, 0.02), (0.4, 0.09), (1, 0.0)], top=0.1)),
        color(gradient([(0, hexc("fff0a0")), (0.5, hexc("e0b040")), (1, hexc("806020"))]), alpha=curve([(0, 0), (0.15, 0.8), (1, 0)]), brightness=1.6),
        attractor(strength=1.6, size=0.05, falloff=0.0, invert=True, space="Local"),
        drag(1.2),
        sprite_render("glow", additive=True),
        max_particles=40),
], duration=100000, looping=False)

# Earth's aurorae: curtains of green light standing over each pole, on two
# small circles, the curtain a flame sprite that stands up from it.
def aurora(name, y):
    return emitter(name,
        rate(18),
        position_on(f"Aurora {name}", "Random"),
        local_space(),
        lifetime(rng(1.2, 2.2)),
        size(curve([(0, 0.05), (0.4, 0.22), (1, 0.05)], top=0.25)),
        color(gradient([(0, hexc("40ff90")), (0.6, hexc("30d0a0")), (1, hexc("6040ff"))]), alpha=curve([(0, 0), (0.3, 0.55), (1, 0)]), brightness=1.8),
        rotation(0, 0, 0),
        sprite_render("flame", additive=True),
        max_particles=40)

# name, material, diameter | moons: (name, material, diameter, distance, period s, tilt deg, phase)
planet_effect("mercury", "mercury.mat", 0.38)
planet_effect("venus", "venus.mat", 0.95, atmosphere=(hexc("ffd890"), 1.5, 0.25))
planet_effect("earth", "earth.mat", 1.0, atmosphere=(hexc("80b0ff"), 1.45, 0.22),
              moons=[("Moon", "moon.mat", 0.27, 1.6, 18.0, 5.0, 0.0, "solar/apollo")], spin_deg=0,
              extra=[aurora("North", 0.46), aurora("South", -0.46),
                     craft("ISS", "LEO", "iss", 0.09, 3.2, 0.0, light_=light(hexc("ffffff"), brightness=0.6, radius=0.5, ratio=1, max_lights=1, use_particle=False)),
                     craft("Hubble", "LEO High", "hubble", 0.05, 3.6, 0.5),
                     craft("Weather Satellite", "GEO", "satellite", 0.04, 12.0, 0.2, trail=False)],
              extra_shapes=[shape("Aurora North", "Circle", offset=(0, 0.46, 0), radius=0.22, shell=True),
                            shape("Aurora South", "Circle", offset=(0, -0.46, 0), radius=0.22, shell=True),
                            orbit_shape("LEO", 0.62, 51.6), orbit_shape("LEO High", 0.66, 28.5), orbit_shape("GEO", 1.1, 0.0)])
planet_effect("mars", "mars.mat", 0.53, atmosphere=(hexc("ff9060"), 1.35, 0.12),
              moons=[("Phobos", "rock.mat", 0.07, 0.7, 6.0, 1.0, 0.0), ("Deimos", "rock.mat", 0.05, 1.0, 11.0, 2.0, 0.5)],
              extra_shapes=[shape("Surface", "Sphere", radius=0.265, shell=True, count=1), orbit_shape("Mars Orbit", 0.42, 93.0)],
              # A dust storm every so often: a rust haze that grows over the
              # surface, swirls, and thins out again - on the effect's own clock.
              extra=[emitter("Dust Storm",
                  rate(40),
                  position("Sphere", radius=0.28, shell=True),
                  local_space(),
                  lifetime(rng(2.5, 4.0)),
                  size(curve([(0, 0.05), (0.3, 0.16), (1, 0.02)], top=0.2)),
                  color(hexc("d08050"), alpha=curve([(0, 0), (0.2, 0.35), (1, 0)]), brightness=1.0),
                  rotation(0, 0, rng(0, 360)),
                  orbit(25, (0.2, 1, 0)),
                  sprite_render("smoke1", additive=False, lighting=True),
                  max_particles=200, delay=28.0, duration=14.0),
                     lander("Rover", "rover", 0.05, "Surface", 0.265),
                     craft("Orbiter", "Mars Orbit", "satellite", 0.03, 4.0, 0.0)])
planet_effect("jupiter", "jupiter.mat", 2.6, atmosphere=(hexc("ffd0a0"), 1.25, 0.12),
              moons=[("Io", "io.mat", 0.2, 2.2, 9.0, 1.0, 0.0, "solar/io_plumes"), ("Europa", "europa.mat", 0.18, 2.8, 14.0, 0.5, 0.3),
                     ("Ganymede", "moon.mat", 0.28, 3.5, 22.0, 0.2, 0.6), ("Callisto", "mercury.mat", 0.26, 4.4, 36.0, 0.3, 0.85)],
              # Jupiter's own ring: faint, thin, close in.
              rings=[(1.55, 1.75, 2, 160, 0.025, hexc("b0a090"), 0.3, 3.0)],
              extra=[craft("Juno", "Polar", "juno", 0.1, 11.0, 0.0)],
              extra_shapes=[orbit_shape("Polar", 1.9, 90.0)])
planet_effect("saturn", "saturn.mat", 2.2, atmosphere=(hexc("ffe8b0"), 1.2, 0.1),
              moons=[("Titan", "titan.mat", 0.24, 4.2, 30.0, 0.5, 0.2), ("Rhea", "europa.mat", 0.1, 3.3, 16.0, 0.3, 0.7),
                     ("Enceladus", "europa.mat", 0.06, 2.95, 9.0, 26.7, 0.4, "solar/geysers"),
                     ("Mimas", "mimas.mat", 0.06, 2.78, 7.5, 26.7, 0.1),
                     # The shepherds either side of the F ring, keeping it thin.
                     ("Prometheus", "rock.mat", 0.035, 2.58, 6.2, 26.7, 0.0), ("Pandora", "rock.mat", 0.03, 2.71, 6.6, 26.7, 0.5)],
              extra=[craft("Cassini", "Cassini Orbit", "cassini", 0.09, 20.0, 0.3)],
              extra_shapes=[orbit_shape("Cassini Orbit", 3.6, 45.0)],
              rings=[(1.45, 2.05, 8, 320, 0.07, hexc("e8d8b0"), 0.85, 26.7),   # the B ring
                     (2.17, 2.4, 3, 300, 0.06, hexc("e0d0a8"), 0.7, 26.7),    # the A ring, past the Cassini Division...
                     (2.44, 2.5, 1, 300, 0.06, hexc("e0d0a8"), 0.7, 26.7),    # ...with the Encke Gap cut through it
                     (2.63, 2.65, 1, 260, 0.035, hexc("d0c0a0"), 0.6, 26.7)])  # the F ring
planet_effect("uranus", "uranus.mat", 1.6, atmosphere=(hexc("a0f0ff"), 1.3, 0.14),
              moons=[("Titania", "europa.mat", 0.12, 1.9, 16.0, 97.0, 0.0), ("Oberon", "moon.mat", 0.11, 2.4, 24.0, 97.0, 0.5)],
              rings=[(1.25, 1.6, 5, 220, 0.035, hexc("c0d0d8"), 0.6, 97.0)])
planet_effect("neptune", "neptune.mat", 1.55, atmosphere=(hexc("6090ff"), 1.3, 0.16),
              moons=[("Triton", "europa.mat", 0.18, 1.7, 14.0, 157.0, 0.0, "solar/cryo")])
planet_effect("pluto", "pluto.mat", 0.25, moons=[("Charon", "moon.mat", 0.12, 0.45, 8.0, 120.0, 0.0)], wobble=(0.06, 8.0, 0.5))

# ------------------------------------------------------------------ the belts, the comet, the orbits, the stars

def belt(name, inner, outer, bands, count, size_, tilt_spread=2.0, speed=0.006):
    shapes_, emitters = [], []
    for b in range(bands):
        r = inner + (outer - inner) * (b + 0.5) / bands
        sname = f"Band {b}"
        shapes_.append(orbit_shape(sname, r, tilt=(b - bands / 2) * tilt_spread / bands, count=count))
        emitters.append(emitter(f"Rocks {b}",
            burst(count),
            position_on(sname, "ByIndex"),
            lifetime(10000.0),
            size(rng(size_ * 0.4, size_ * 1.6)),
            color(hexc("ffffff")),
            rotation(rng(0, 360), rng(0, 360), rng(0, 360)),
            spin(rng(-20, 20), rng(-20, 20), rng(-20, 20)),
            follow(sname, sample="ByIndex", along=fb(rng(0, 0.004)), speed=fb(speed * inner / r, "Speed")),
            mesh_render("models/dev/box.mdl", M + "rock.mat", scale=1.0, rotate=False, shadows=False,
                        shader=[("Dissolve", 1, fb(0.0)), ("Emission", 1, fb(0.8))]),
            max_particles=count, places=count))
    emitters.append(emitter("Dust",
        rate(60),
        position("Circle", radius=outer, shell=False),
        lifetime(rng(4, 8)),
        size(rng(0.03, 0.06)),
        color(hexc("d0c8b8"), alpha=curve([(0, 0), (0.3, 0.35), (1, 0)])),
        orbit(0.6, (0, 1, 0)),
        sprite_render("dot", additive=True),
        max_particles=500))
    effect(name, emitters, duration=10, looping=True, shapes=shapes_, floats=[param_float("Speed", 1, 0, 3)])

belt("solar/belt", 22.0, 26.0, 7, 90, 0.07)

# The Trojans: two swarms sixty degrees ahead of and behind Jupiter on its
# own orbit, riding round with it.
def trojans(name, along_lo, along_hi):
    return emitter(name,
        burst(70),
        position_on("Jupiter Orbit", "ByTime", along={"Type": "Range", "Evaluation": "Seed", "Constants": f"{along_lo},{along_hi},0,0"}),
        lifetime(10000.0),
        size(rng(0.04, 0.1)),
        color(hexc("ffffff")),
        rotation(rng(0, 360), rng(0, 360), rng(0, 360)),
        spin(rng(-20, 20), rng(-20, 20), rng(-20, 20)),
        follow("Jupiter Orbit", along={"Type": "Range", "Evaluation": "Seed", "Constants": f"{along_lo},{along_hi},0,0"}, speed=fb(1.0 / 260.0, "Speed")),
        mesh_render("models/dev/box.mdl", M + "rock.mat", scale=1.0, rotate=False, shadows=False,
                    shader=[("Dissolve", 1, fb(0.0)), ("Emission", 1, fb(0.8))]),
        max_particles=70)

effect("solar/trojans", [trojans("Greeks (L4)", 0.30 + 0.1667 - 0.02, 0.30 + 0.1667 + 0.02), trojans("Trojans (L5)", 0.30 - 0.1667 - 0.02, 0.30 - 0.1667 + 0.02)],
       duration=10, looping=True, shapes=[orbit_shape("Jupiter Orbit", 32.0, 1.3)], floats=[param_float("Speed", 1, 0, 3)])
belt("solar/kuiper", 62.0, 72.0, 5, 120, 0.12, tilt_spread=8.0, speed=0.003)

# The comet: a rock on a long loop, a dust tail behind it and an ion tail
# blown straight away from the sun by an attractor pushing from the star.
COMET_PATH = [(-4.0, 0.5, -3.0), (10.0, 1.5, 12.0), (34.0, 3.0, 40.0), (60.0, 2.0, 30.0), (52.0, -1.0, -8.0), (24.0, -2.0, -30.0), (2.0, -0.5, -18.0)]
effect("solar/comet", [
    emitter("Nucleus",
        burst(1),
        position_on("Path", "ByTime", along=fb(0.0)),
        lifetime(10000.0),
        size(0.35),
        color(hexc("ffffff")),
        spin(rng(-40, 40), rng(-40, 40), rng(-40, 40)),
        follow("Path", along=fb(0.0), speed=fb(1.0 / 70.0, "Speed"), loop=True),
        publish("Comet"),
        mesh_render("models/dev/box.mdl", M + "rock.mat", scale=1.0, rotate=False, shadows=False,
                    shader=[("Dissolve", 1, fb(0.0)), ("Emission", 1, fb(0.9))]),
        # The dust tail: narrow at the nucleus, spreading wide behind it.
        trail_render(width=1.4, color=hexc("e0f0ff", 0.35), life=6.0, max_points=120, point_distance=0.1, scale_from=False, tint=False, taper=(0.2, 1.0), fade=(1.0, 0.0)),
        light(hexc("c0e0ff"), brightness=2, radius=6, ratio=1, max_lights=1, use_particle=False),
        event("OnBirth", "Tail", effect_="solar/comet_tail", follow=True, max_alive=1, context=[]),
        max_particles=1),
], duration=10, looping=True,
   shapes=[shape("Path", "Spline", points=COMET_PATH, closed=True)], anchors=[anchor("Comet")],
   floats=[param_float("Speed", 1, 0.1, 5), param_float("Tail", 1, 0, 3)])

# The tail is its own effect, spawned once by the nucleus at birth and carried
# along with it (Event, Follow): the coma glow, and an ion tail born on the
# nucleus and pushed off by an attractor at the sun - so it points away from
# the star whichever way the comet is going, the way a real one does.
effect("solar/comet_tail", [
    emitter("Coma",
        rate(30),
        position("Sphere", radius=0.15),
        lifetime(rng(0.8, 1.4)),
        size(curve([(0, 0.3), (1, 1.4)], top=1.5)),
        color(hexc("d0e8ff"), alpha=curve([(0, 0), (0.2, 0.25), (1, 0)]), brightness=1.5),
        sprite_render("glow", additive=True),
        max_particles=60),
    emitter("Ion Tail",
        rate(120, "Tail"),
        position("Sphere", radius=0.2),
        lifetime(rng(3.0, 5.0)),
        size(rng(0.06, 0.12)),
        color(hexc("80c0ff"), alpha=curve([(0, 0), (0.1, 0.5), (1, 0)]), brightness=2.0),
        mod("AttractorModule", "Update", "Sun Wind", Space="World", Position=vb(*SUN), Strength=fb(180.0), Size=1.0, Invert=True, Falloff=1.0),
        noise(0.8, 0.5, 0.8),
        sprite_render("dot", additive=True),
        max_particles=800),
    emitter("Dust Tail",
        rate(40, "Tail"),
        position("Sphere", radius=0.25),
        velocity(0, 0, 0, scatter=0.3),
        lifetime(rng(4.0, 7.0)),
        size(curve([(0, 0.1), (1, 0.6)], top=0.8)),
        color(hexc("fff0d0"), alpha=curve([(0, 0), (0.15, 0.3), (1, 0)]), brightness=1.3),
        mod("AttractorModule", "Update", "Sun Push", Space="World", Position=vb(*SUN), Strength=fb(45.0), Size=1.0, Invert=True, Falloff=1.0),
        sprite_render("glow", additive=True),
        max_particles=300),
], duration=100000, looping=False, floats=[param_float("Tail", 1, 0, 3)])

# Orbit lines: dots parked By Index on each planet's circle, faint.
planet_effect("ceres", "moon.mat", 0.12)
planet_effect("eris", "europa.mat", 0.24, moons=[("Dysnomia", "moon.mat", 0.05, 0.4, 7.0, 60.0, 0.0)])

PLANETS = [  # name, orbit radius, period s, tilt deg, phase
    ("mercury", 7.5, 24.0, 7.0, 0.1), ("venus", 10.0, 40.0, 3.4, 0.55), ("earth", 13.0, 60.0, 0.0, 0.0),
    ("mars", 17.0, 100.0, 1.8, 0.8), ("jupiter", 32.0, 260.0, 1.3, 0.3), ("saturn", 44.0, 420.0, 2.5, 0.65),
    ("uranus", 54.0, 700.0, 0.8, 0.2), ("neptune", 60.0, 900.0, 1.8, 0.45), ("pluto", 68.0, 1200.0, 17.0, 0.9),
    ("ceres", 24.0, 160.0, 10.6, 0.4), ("eris", 74.0, 1500.0, 44.0, 0.15),
]
effect("solar/orbits", [
    ring_band(f"Orbit {n}", f"Orbit {n}", int(60 + r * 6), 0.03, hexc("8090b0"), 0.35, 0.0) for n, r, p, t, ph in PLANETS
], duration=10, looping=True,
   shapes=[orbit_shape(f"Orbit {n}", r, t, int(60 + r * 6)) for n, r, p, t, ph in PLANETS],
   floats=[param_float("Speed", 1, 0, 3)])

# Stars: parked once on a far shell, twinkling by a curve read by seed.
effect("solar/stars", [
    emitter("Stars",
        burst(1600),
        position("Sphere", radius=160.0, shell=True),
        lifetime(10000.0),
        size(rng(0.12, 0.45)),
        color(color_range(hexc("ffffff"), hexc("b0c8ff")), alpha=rng(0.5, 1.0), brightness=1.6),
        sprite_render("dot", additive=True, fog=0.0),
        max_particles=1600),
    # The Milky Way: a band of stars round a tilted great circle, thrown a
    # little off it and held by the drag, so it is a band and not a line.
    emitter("Milky Way",
        burst(2200),
        position_on("Galaxy", "Random"),
        velocity(0, 0, 0, scatter=30.0),
        lifetime(10000.0),
        size(rng(0.1, 0.35)),
        color(color_range(hexc("ffffff"), hexc("d0d8ff")), alpha=rng(0.25, 0.7), brightness=1.3),
        drag(2.0),
        sprite_render("dot", additive=True, fog=0.0),
        max_particles=2200),
    emitter("Galactic Haze",
        burst(120),
        position_on("Galaxy", "Random"),
        velocity(0, 0, 0, scatter=14.0),
        lifetime(10000.0),
        size(rng(5.0, 9.0)),
        color(color_range(hexc("8090c0"), hexc("c0a0b0")), alpha=0.035, brightness=1.0),
        drag(2.0),
        sprite_render("glow", additive=True, fog=0.0),
        max_particles=120),
    emitter("Bright Stars",
        burst(60),
        position("Sphere", radius=155.0, shell=True),
        lifetime(10000.0),
        size(rng(0.8, 1.4)),
        color(color_range(hexc("ffffff"), hexc("ffe0c0")), alpha=0.9, brightness=2.0),
        sprite_render("glow", additive=True, fog=0.0),
        max_particles=60),
], duration=10, looping=True, shapes=[shape("Galaxy", "Circle", radius=156.0, shell=True, rot=(62, 0, 20))])

# ------------------------------------------------------------------ the scene

def player_at(name, fx, pos=(0, 0, 0)):
    return sg.go(name, pos, components=[sg.comp("Rinten.ParticlePlayer", "solar/" + name, Definition=f"fx/{fx}.fx",
        DestroyOnEnd=False, FloatOverrides={}, VectorOverrides={}, ColorOverrides={})])

def orbiting(name, fx, radius, period, tilt, phase):
    return sg.go(name, (radius, SUN[1], 0), components=[
        sg.comp("TestGround.Orbit", "orbit/" + name, Centre=sg.guid("go/Sun"), Radius=radius, Period=period, Tilt=tilt, Phase=phase),
        sg.comp("Rinten.ParticlePlayer", "solar/" + name, Definition=f"fx/{fx}.fx", DestroyOnEnd=False, FloatOverrides={}, VectorOverrides={}, ColorOverrides={}),
    ])

objects = [
    sg.go("Environment", children=[
        sg.go("Ambient", components=[sg.comp("Rinten.AmbientLight", "solar/ambient", Color="0.02,0.02,0.04,1")]),
        sg.go("2D Skybox", tags="skybox", components=[sg.comp("Rinten.SkyBox2D", "solar/sky", SkyIndirectLighting=False,
            SkyMaterial="materials/skybox/procedural.mat", Tint="0,0,0,1")]),
    ]),
    sg.go("Sun", SUN, children=[player_at("Sun Effect", "solar/sun")]),
    sg.go("Planets", children=[orbiting(n.capitalize(), f"solar/{n}", r, p, t, ph) for n, r, p, t, ph in PLANETS]),
    sg.go("Belts", SUN, children=[player_at("Asteroid Belt", "solar/belt"), player_at("Kuiper Belt", "solar/kuiper"), player_at("Trojans", "solar/trojans")]),
    sg.go("Probes", (0, 0, 0), children=[player_at("Voyager 1", "solar/voyager1"), player_at("Voyager 2", "solar/voyager2"), player_at("New Horizons", "solar/newhorizons")]),
    sg.go("Orbits", SUN, children=[player_at("Orbit Lines", "solar/orbits")]),
    sg.go("Stars", SUN, children=[player_at("Starfield", "solar/stars")]),
    sg.go("Player", (0, 8, 40), components=[sg.comp("Template.Player", "solar/player",
        Camera={"_type": "component", "component_id": sg.guid("comp/solar/camera"), "go": sg.guid("go/Camera"), "component_type": "CameraComponent"},
        PitchClamp=89, RunScale=4, Speed=12)], children=[
        sg.go("Camera", rot="-0.0697565,0,0,0.9975641", tags="maincamera", components=[
            sg.comp("Rinten.CameraComponent", "solar/camera", BackgroundColor="0.01,0.01,0.02,1", ClearFlags="All", EnablePostProcessing=True,
                 FieldOfView=75, FovAxis="Horizontal", IsMainCamera=True, Orthographic=False, OrthographicHeight=10,
                 PostProcessAnchor=None, Priority=1, RenderExcludeTags="", RenderTags="", RenderTexture=None, TargetEye="None",
                 Viewport="0,0,1,1", ZFar=600, ZNear=0.05),
            sg.comp("Rinten.Bloom", "solar/bloom", __version=1, Mode="Additive", Spread=0.7, Strength=1.0, Threshold=1, Tint="1,1,1,1"),
        ])]),
    sg.go("HUD", components=[
        sg.comp("Rinten.ScreenPanel", "solar/hud/panel", AutoScreenScale=True, Opacity=1, Scale=1, ScaleStrategy="ConsistentHeight", TargetCamera=None, ZIndex=100),
        sg.comp("TestGround.SolarClock", "solar/clock", Scale=1.0, SecondsPerYear=60.0, Epoch="2026-01-01"),
        sg.comp("TestGround.SolarHud", "solar/hud/scene", Clock={"_type": "component", "component_id": sg.guid("comp/solar/clock"), "go": sg.guid("go/HUD"), "component_type": "SolarClock"},
                Player=sg.guid("go/Player")),
        sg.comp("TestGround.ReturnToMenu", "solar/hud/return", Key="Q", MenuScene=None),
    ]),
]

scene = {
    "__guid": "7c1d3a52-0e8b-4a1f-9f0e-5b2c6d7e8f90",
    "SceneProperties": {
        "NetworkInterpolation": True, "TimeScale": 1, "WantsSystemScene": True, "Metadata": {},
        "NavMesh": {"Enabled": False, "IncludeStaticBodies": True, "IncludeKeyframedBodies": True, "EditorAutoUpdate": False,
                    "AgentHeight": 1.6, "AgentRadius": 0.4, "AgentStepSize": 0.45, "AgentMaxSlope": 40,
                    "ExcludedBodies": "", "IncludedBodies": "", "DeferGeneration": False, "CustomBounds": False},
        "GameObjectSystems": {"Rinten.SelectionSetsSystem": {"Data": {"SelectionSets": []}}},
    },
    "GameObjects": objects,
    "ResourceVersion": 4, "Title": "Solar System", "Description": "The sun, nine worlds with moons and rings, two belts and a comet - every one an effect from the FX editor.",
    "__references": [], "__version": 4,
}

path = os.path.join(sg.ROOT, "scenes/fx/solar.scene")
with open(path, "w") as f:
    json.dump(scene, f, indent=2)
print("wrote", path)

# The skin of a coronal mass ejection: sparks flung along with the bubble.
effect("solar/cme_skin", [
    emitter("Sparks",
        rate(80),
        position("Sphere", radius=0.6, shell=True),
        velocity(0, 0, 0, scatter=1.5),
        lifetime(rng(1.0, 2.0)),
        size(rng(0.04, 0.1)),
        color(hexc("ffd090"), alpha=curve([(0, 1), (1, 0)]), brightness=2.5),
        stretch(2.0),
        sprite_render("spark", additive=True, face=True),
        max_particles=200),
], duration=100000, looping=False)

# Enceladus: water-ice geysers from the south pole; Triton: dark nitrogen
# plumes. The same shape as Io's volcanoes, a followed child on the moon.
def plume_effect(name, colours, size_, rate_, up):
    effect(name, [
        emitter("Plumes",
            rate(rate_),
            position("Sphere", radius=0.06, shell=True),
            velocity(0, up, 0, scatter=0.0),
            lifetime(rng(1.0, 1.8)),
            size(curve([(0, 0.01), (0.4, size_), (1, 0.0)], top=size_ * 1.2)),
            color(gradient(colours), alpha=curve([(0, 0), (0.15, 0.7), (1, 0)]), brightness=1.4),
            attractor(strength=1.2, size=0.05, falloff=0.0, invert=True, space="Local"),
            drag(1.0),
            sprite_render("glow", additive=True),
            max_particles=int(rate_ * 2)),
    ], duration=100000, looping=False)

plume_effect("solar/geysers", [(0, hexc("ffffff")), (0.5, hexc("c0e8ff")), (1, hexc("80a0c0"))], 0.06, 12, -0.4)
plume_effect("solar/cryo", [(0, hexc("606070")), (0.5, hexc("404050")), (1, hexc("202030"))], 0.05, 6, 0.3)

# Apollo: the lander and the flag, standing on the Moon - a followed child of
# the Moon's particle, parked on a sphere the Moon's size, facing out.
effect("solar/apollo", [
    lander("Eagle", "apollo", 0.06, "Moon Surface", 0.135),
], duration=100000, looping=False, shapes=[shape("Moon Surface", "Sphere", radius=0.137, shell=True, count=1)])

# The probes on their way out: Voyager 1 up and out of the plane past Saturn,
# Voyager 2 out past Neptune, New Horizons past Pluto - each on its own long
# spline, a faint trail behind, a beam of telemetry back to the sun's side.
def probe(name, model, path_points, period, diameter, material=None):
    return effect(name, [
        emitter("Probe",
            burst(1),
            position_on("Route", "ByTime", along=fb(0.0)),
            lifetime(period),
            size(diameter),
            color(hexc("ffffff")),
            spin(0, 6, 0),
            follow("Route", along=fb(curve([(0, 0), (1, 1)], mode="Linear"), "Speed"), loop=False, align=True),
            publish("Probe"),
            mesh_render(SP + model + ".mdl", material, scale=1.0, rotate=False, shadows=False,
                        shader=[("Emission", 1, fb(1.0)), ("Dissolve", 1, fb(0.0))], particle_attrs=False),
            trail_render(width=diameter * 0.3, color=hexc("a0c8ff", 0.35), life=period * 0.08, max_points=80, point_distance=0.1, scale_from=False, tint=False),
            max_particles=1),
    ], duration=period, looping=True, shapes=[shape("Route", "Spline", points=path_points, closed=False)], anchors=[anchor("Probe")],
       floats=[param_float("Speed", 1, 0.1, 5)])

probe("solar/voyager1", "voyager", [(13.0, 3.0, 0.0), (30.0, 3.5, -12.0), (44.0, 6.0, -20.0), (70.0, 22.0, -40.0), (110.0, 48.0, -70.0)], 240.0, 0.16, M + "gold.mat")
probe("solar/voyager2", "voyager", [(13.0, 3.0, 0.0), (32.0, 2.6, 8.0), (44.0, 2.4, 14.0), (56.0, 1.5, 30.0), (62.0, -4.0, 50.0), (100.0, -30.0, 90.0)], 300.0, 0.16, M + "gold.mat")
probe("solar/newhorizons", "newhorizons", [(13.0, 3.0, 0.0), (32.0, 4.0, -6.0), (68.0, 8.0, -14.0), (120.0, 12.0, -30.0)], 260.0, 0.12, M + "gold.mat")
