# Test Ground

A Rinten project that exercises the engine one feature at a time: a menu of
test scenes, each a walk through one system with what it should look like
written on the wall beside it.

## Layout

```
Assets/
  scenes/            main.scene is the menu; every other scene sits under its menu category
    general/         basics, prefabs, overlay
    physics/         collider, rigidbody, trace, platforms
    rendering/       lights, fog, postprocess, decals, renderers, materials, shadows, clutter
    fx/              particles (the effect showcase), solar (the solar system)
    ui/              showcase, world
  fx/                particle effects, by what they are
    ambient/         fire, chimney, fountain, rain, snow, tornado, fireflies
    combat/          gunshot, impact, explosion, slash, meteor, homing, beam, tesla, shatter
    magic/           magic orb, portal, singularity, buff aura, shield, assemble
    fireworks/       firework and its chained bursts, sparkler, confetti, crackle
    shapes/          formation, snake, dna, jelly, swarm (the orrery)
    solar/           the sun, every planet, belts, comet, probes, orbit lines, stars
  materials/
    common/          glass, trigger - shared by several scenes
    fx/              the stylized shader looks the effects use
    gallery/         the material gallery, one folder per property it shows:
                     grid/ tint/ emission/ blend/ sides/ maps/ shaders/ surface/
    solar/           planets, moons and their atmospheres
  models/            fx/ (flame, shield), props/ (urn), space/ (spacecraft)
  shaders/effects/   planet, atmosphere, sun, stylized
  sprites/ decals/   the effect sprites and the decals cut from the same pictures
  textures/          fx/ (sprite frames), gallery/ (the gallery's maps, generated)
  clutter/           clutter definitions for the clutter scene
  prefabs/           cube, sphere

Code/
  Player/            the template player
  TestGround/        components, by what they test
    Menu/            SceneNavigator, SceneEntry, ReturnToMenu
    Motion/          Orbit, Oscillator, Spinner, Swing
    Physics/         probes and resets: TriggerProbe, ContactFlash, Shooter, Thruster, ...
    Interaction/     Door, PlayerUse, Grabber, Launcher, Spawner, SelfDestruct, Walker
    Rendering/       MaterialProbe, ProceduralMesh, TrailPulse, ShadowRack, PostProcessRack, ...
    Solar/           SolarClock
  UI/
    Menu/            SceneMenu - the main menu
    Hud/             SceneHud, FrameStats, SolarHud
    World/           WorldLabel - the signs in the scenes
    Showcase/        UiShowcase and its badge

tools/               Python that writes Assets/ - regenerate rather than hand-edit what they own
  fx/                fxgen.py (sprites + effects), scenegen.py (the particles scene), solar.py (the solar system)
  gallery/           one gallery scene each, registered in the menu. shadows.cs and jungle.cs are built
                     inside the editor: `python3 build.py shadows` sends common.cs + shadows.cs to
                     execute_code and the engine writes the .scene (the standard for new scenes);
                     materials.py, renderers.py, clutter.py still write the file themselves and are to
                     be ported the same way
  jungle/            the jungle's models and textures: grow.py (bpy, run in Blender) grows the catalogue
                     and writes sockets.json + ground.json, textures.py bakes the sheets and materials;
                     the scene itself is gallery/jungle.cs
  scenes/            gen_scenes.py - the hand-laid scenes: prefabs, trace, overlay, lights, fog, world ui
  editor/            talks to the running editor over MCP: screenshots and camera moves
  shots/             screenshots taken while the effects were being tuned
```

## Conventions

- Asset paths are relative to `Assets/` and lowercase; the engine lowercases
  what it looks up, so `scenes/fx/particles.scene` is the name.
- A folder replaces a prefix. `fx/solar/earth.fx`, not `fx/sol_earth.fx`;
  `materials/gallery/tint/red.mat`, not `tint_red.mat`.
- A scene lives under the menu category it is filed in (`SceneEntry.Category`).
- A generated file says so in the generator's docstring. Run the generator
  from its own folder: `cd tools/fx && python3 solar.py`.
