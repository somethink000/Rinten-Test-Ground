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
    animation/       character (clips, graph, root motion, bones, jiggle), ragdoll
    rendering/       lights, fog, postprocess, decals, renderers, materials, shadows, clutter, jungle, terrain
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
                     grid/ tint/ emission/ blend/ sides/ maps/ shaders/ surface/ terrain/
    solar/           planets, moons and their atmospheres
  models/            fx/ (flame, shield), props/ (urn), space/ (spacecraft),
                     character/ (the rigged mannequin: 28 bones, 5 clips, a
                     ragdoll and two jiggle chains)
  shaders/effects/   planet, atmosphere, sun, stylized
  sprites/ decals/   the effect sprites and the decals cut from the same pictures
  textures/          fx/ (sprite frames), gallery/ (the gallery's maps, generated)
  clutter/           clutter definitions for the clutter scene
  prefabs/           cube, sphere

Code/
  Player/            the template player
  TestGround/        components, by what they test
    Animation/       ClipRack, CharacterGraph, RootMotionMover, BoneMarker,
                     RagdollRack, JiggleShaker
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
  character/         rig.py (the mannequin, its takes and its .mdl, built in
                     Blender), scenes.py (the two character scenes),
                     probe.py (what the engine's own ufbx sees in an fbx)
  fx/                fxgen.py (sprites + effects), scenegen.py (the particles scene), solar.py (the solar system)
  gallery/           one gallery scene each, registered in the menu. shadows.cs, jungle.cs and
                     terrain.cs are built inside the editor: `python3 build.py terrain` sends
                     common.cs + terrain.cs to execute_code and the engine writes the .scene
                     (the standard for new scenes); materials.py, renderers.py, clutter.py still
                     write the file themselves and are to be ported the same way
  jungle/            sockets.json + ground.json, which the jungle's generators write and gallery/jungle.cs
                     reads; the scene itself is gallery/jungle.cs
  scenes/            gen_scenes.py - the hand-laid scenes: prefabs, trace, overlay, lights, fog, world ui
  editor/            talks to the running editor over MCP: screenshots and camera moves
  shots/             screenshots taken while the effects were being tuned
```

The Blender scripts and the texture generators live outside this checkout, in
`~/Documents/Blender/tools/`, and write into it (`RINTEN_TEST_GROUND` overrides
where): `jungle/grow.py` and `jungle/textures.py` (the jungle's models, textures
and materials), `archery/build_archery.py` (bow, arrow, target) and
`weapons/build_pistol.py` (pistol, magazines, casing, round).

## Conventions

- Asset paths are relative to `Assets/` and lowercase; the engine lowercases
  what it looks up, so `scenes/fx/particles.scene` is the name.
- A folder replaces a prefix. `fx/solar/earth.fx`, not `fx/sol_earth.fx`;
  `materials/gallery/tint/red.mat`, not `tint_red.mat`.
- A scene lives under the menu category it is filed in (`SceneEntry.Category`).
- A generated file says so in the generator's docstring. Run the generator
  from its own folder: `cd tools/fx && python3 solar.py`.
- Nothing under `tools/` writes down where the checkout is; each script reads
  that off its own path, because the project has moved and every absolute path
  in here went stale at once.
- The character is built by Blender rather than drawn by hand:
  `blender -b -P tools/character/rig.py` writes the fbx and the .mdl, and
  `cd tools/character && python3 scenes.py` lays the scenes that use them.
