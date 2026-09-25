#!/usr/bin/env python3
"""Writes the two character scenes and registers them in the menu:

    scenes/animation/character.scene   clips, the graph, root motion, bones,
                                       attachments and jiggle bones
    scenes/animation/ragdoll.scene     model physics: the switch, the joints,
                                       a pile, and what a slope does to one

Both stand on models/character/mannequin.mdl, which tools/character/rig.py
grows in Blender. Run that first if the model is not there.

    cd tools/character && python3 scenes.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gallery"))
from common import Scene, RENDER, v, yaw, pitch_yaw, register_in_menu  # noqa: E402

MODEL = "models/character/mannequin.mdl"
PEDESTAL = "0.2,0.22,0.26,1"

LOCKING = {"X": False, "Y": False, "Z": False, "Pitch": False, "Yaw": False, "Roll": False}


# ---------------------------------------------------------------------------
# The pieces every station is made of
# ---------------------------------------------------------------------------

def character(S, name, tint="1,1,1,1", bones=False, attachments=False, graph=True, clip=None):
    """A skinned renderer wearing the mannequin.

    `clip` names a sequence to play directly. Naming one turns the graph off,
    which is the engine's own rule rather than this script's - see
    SequenceAccessor.Name.
    """
    sequence = {"Name": clip or "", "Looping": True, "Blending": False}

    return S.comp(
        "Rinten.SkinnedModelRenderer", "char/" + name,
        BodyGroups=18446744073709551615,
        BoneMergeTarget=None,
        CreateAttachments=attachments,
        CreateBoneObjects=bones,
        MaterialGroup=None,
        MaterialOverride=None,
        Materials=None,
        Model=MODEL,
        PlaybackRate=1.0,
        RenderOptions=RENDER,
        RenderType="On",
        Sequence=sequence,
        Tint=tint,
        UseAnimGraph=graph and clip is None,
    )


def model_physics(S, name, go_name, enabled=False):
    return dict(
        S.comp(
            "Rinten.ModelPhysics", "phys/" + name,
            IgnoreRoot=False,
            Locking=LOCKING,
            Model=MODEL,
            MotionEnabled=True,
            Renderer=S.ref_comp("char/" + name, go_name, "SkinnedModelRenderer"),
            RigidbodyFlags=0,
            StartAsleep=False,
        ),
        __enabled=enabled,
    )


def sign_ref(S, name):
    return S.ref_comp("text/label/" + name, "Label: " + name, "TextRenderer")


def stand(S, name, text, pos, components, sign_y=2.6, pedestal=True, sign_text=None):
    """A pedestal, a sign the components can write onto, and the character."""
    kids = []
    if pedestal:
        kids.append(S.block(f"Pedestal: {name}", (0, 0.1, 0), (1.3, 0.2, 1.3), PEDESTAL))
    kids.append(S.label(name, (0, sign_y, 0), sign_text if sign_text is not None else text, scale=0.32, size=44))
    kids.append(S.go(f"Sign: {name}", (0, sign_y + 0.9, 0), components=[
        S.text("head/" + name, S.text_scope(text, size=40, color="0.62,0.72,0.86,1"), scale=0.26)]))
    kids.append(S.go(f"Character: {name}", (0, 0.2, 0), components=components))
    return S.go(f"Station: {name}", pos, children=kids)


def row(count, spacing):
    """x positions for a row of stations, centred on the station's own origin."""
    return [(i - (count - 1) / 2.0) * spacing for i in range(count)]


# ---------------------------------------------------------------------------
# scenes/animation/character.scene
# ---------------------------------------------------------------------------

def character_scene():
    S = Scene("animation-character", "Character",
              "Skinning, clips, an animation graph built in code, root motion, "
              "bone objects, attachments and jiggle bones - a station each.")

    areas = []

    # --- clips: every take the model carries, side by side and looping -----
    clips = ["idle", "walk", "run", "wave", "jump"]
    stands = []
    for x, clip in zip(row(len(clips) + 1, 3.4), clips):
        stands.append(stand(S, clip, clip, (x, 0, 0), [character(S, clip, clip=clip)],
                            sign_text=clip))
    # And one that walks the whole list, which is the path a game takes when
    # it drives a character clip by clip.
    x = row(len(clips) + 1, 3.4)[-1]
    stands.append(stand(S, "cycle", "every clip in turn", (x, 0, 0), [
        character(S, "cycle", tint="0.75,0.9,1,1", clip="idle"),
        S.comp("TestGround.ClipRack", "rack/cycle", Clips=[], Hold=False, Renderer=None,
               Seconds=3.0, Sign=sign_ref(S, "cycle")),
    ], sign_text="cycle"))
    S.stagger_signs(stands)
    areas.append(S.area("Clips", "one sequence each, straight off the model", -14, 24, children=stands))

    # --- the graph ---------------------------------------------------------
    stands = [
        stand(S, "locomotion", "speed 0 -> 5.5, blended", (-4.5, 0, 0), [
            character(S, "locomotion"),
            S.comp("TestGround.CharacterGraph", "graph/locomotion", Renderer=None, Sign=sign_ref(S, "locomotion"),
                   Sweep=9.0, TopSpeed=5.5, WaveEvery=0.0, WaveFor=2.2),
        ], sign_text="locomotion"),
        stand(S, "transition", "a wave crossed in and out", (0, 0, 0), [
            character(S, "transition", tint="1,0.92,0.78,1"),
            S.comp("TestGround.CharacterGraph", "graph/transition", Renderer=None, Sign=sign_ref(S, "transition"),
                   Sweep=0.0, TopSpeed=0.0, WaveEvery=2.0, WaveFor=2.2),
        ], sign_text="transition"),
        stand(S, "both", "walking and waving at once", (4.5, 0, 0), [
            character(S, "both", tint="0.82,1,0.86,1"),
            S.comp("TestGround.CharacterGraph", "graph/both", Renderer=None, Sign=sign_ref(S, "both"),
                   Sweep=7.0, TopSpeed=3.0, WaveEvery=3.0, WaveFor=1.8),
        ], sign_text="both"),
    ]
    S.stagger_signs(stands)
    areas.append(S.area("Animation graph", "built in code: a blend space inside a state machine", -32, 20, children=stands))

    # --- root motion -------------------------------------------------------
    stands = [
        stand(S, "carried", "the clip carries it", (-3.5, 0, 0), [
            character(S, "carried", clip="walk"),
            S.comp("TestGround.RootMotionMover", "motion/carried", Frozen=False, Renderer=None, Run=4.0,
                   Sign=sign_ref(S, "carried")),
        ], pedestal=False, sign_text="carried"),
        stand(S, "on the spot", "the same clip, motion ignored", (3.5, 0, 0), [
            character(S, "on the spot", tint="0.95,0.8,0.8,1", clip="walk"),
            S.comp("TestGround.RootMotionMover", "motion/spot", Frozen=True, Renderer=None, Run=4.0,
                   Sign=sign_ref(S, "on the spot")),
        ], pedestal=False, sign_text="on the spot"),
    ]
    areas.append(S.area("Root motion", "walk and run have their travel lifted by MotionBone; this puts it back",
                        -50, 20, children=stands))

    # --- bones and attachments --------------------------------------------
    markers = []
    for i, (name, bone, colour) in enumerate((
        ("Hand.L", "Hand.L", "1,0.4,0.3,1"),
        ("Hand.R", "Hand.R", "1,0.4,0.3,1"),
        ("Head", "Head", "0.4,0.8,1,1"),
        ("Ponytail4", "Ponytail4", "1,0.9,0.4,1"),
        ("Foot.L", "Foot.L", "0.6,1,0.6,1"),
        ("Foot.R", "Foot.R", "0.6,1,0.6,1"),
    )):
        markers.append(S.go(f"Bone marker {name}", (0, 0, 0), scale=(0.09, 0.09, 0.09), components=[
            S.model(f"marker/{name}", colour, model="models/dev/sphere.mdl"),
            S.comp("TestGround.BoneMarker", f"marker/bone/{name}", HideWhenMissing=True, Name=bone,
                   Offset="0,0,0", Renderer=S.ref_comp("char/bones", "Character: bones", "SkinnedModelRenderer"),
                   TakeRotation=False, What="Bone"),
        ]))

    attached = []
    for name, attachment, colour, scale in (
        ("hand.L", "hand.L", "1,0.6,0.15,1", (0.06, 0.06, 0.45)),
        ("head", "head", "0.6,0.4,1,1", (0.06, 0.32, 0.06)),
        ("chest", "chest", "0.4,1,0.9,1", (0.22, 0.05, 0.22)),
    ):
        attached.append(S.go(f"Attached {name}", (0, 0, 0), scale=scale, components=[
            S.model(f"attached/{name}", colour),
            S.comp("TestGround.BoneMarker", f"marker/att/{name}", HideWhenMissing=True, Name=attachment,
                   Offset="0,0,0", Renderer=S.ref_comp("char/attach", "Character: attachments", "SkinnedModelRenderer"),
                   TakeRotation=True, What="Attachment"),
        ]))

    stands = [
        stand(S, "bones", "a sphere on six named bones", (-3.6, 0, 0), [
            character(S, "bones", bones=True),
            S.comp("TestGround.CharacterGraph", "graph/bones", Renderer=None, Sign=None,
                   Sweep=8.0, TopSpeed=4.0, WaveEvery=4.0, WaveFor=2.0),
        ], sign_text="bones"),
        stand(S, "attachments", "boxes on the model's own attachment points", (3.6, 0, 0), [
            character(S, "attach", tint="0.86,0.86,1,1", attachments=True),
            S.comp("TestGround.CharacterGraph", "graph/attach", Renderer=None, Sign=None,
                   Sweep=8.0, TopSpeed=4.0, WaveEvery=4.0, WaveFor=2.0),
        ], sign_text="attachments"),
    ]
    stands[0]["Children"].extend(markers)
    stands[1]["Children"].extend(attached)
    areas.append(S.area("Bones and attachments", "where the skeleton puts a bone, and where the model declares a point",
                        -68, 20, children=stands))

    # --- jiggle ------------------------------------------------------------
    modes = [
        ("Still", "nothing moves it", 0.0, 2.0),
        ("Slide", "across the floor", 1.5, 2.0),
        ("Spin", "turned on the spot", 150.0, 2.4),
        ("Bounce", "up and down", 0.8, 1.2),
        ("Jerk", "a hard stop each end", 1.1, 1.6),
    ]
    stands = []
    for x, (mode, note, amount, period) in zip(row(len(modes), 4.0), modes):
        stands.append(stand(S, mode, note, (x, 0, 0), [
            character(S, "jiggle" + mode, clip="idle"),
            S.comp("TestGround.JiggleShaker", "shake/" + mode, Amount=amount, Period=period, What=mode),
        ], pedestal=False, sign_text=mode))
    S.stagger_signs(stands)
    areas.append(S.area("Jiggle bones", "the ponytail and the belt tassel are springs; they only move when the body does",
                        -86, 24, children=stands))

    S.objects = [
        S.environment(),
        S.block("Ground", (0, -0.7, -50), (120, 0.5, 130), "0.2,0.21,0.24,1"),
        S.go("Areas", children=areas),
        S.player((0, 2.4, 6)),
        S.hud("Five rows: the model's clips, a graph assembled in code, root motion, bone and attachment "
              "markers, and the jiggle chains under five kinds of motion. Q returns."),
    ]
    return S


# ---------------------------------------------------------------------------
# scenes/animation/ragdoll.scene
# ---------------------------------------------------------------------------

def ragdoll_scene():
    S = Scene("animation-ragdoll", "Ragdoll",
              "Model physics: the switch from animated to ragdoll and back, the joint limits, "
              "a pile of them, and what a slope does to one.")

    areas = []

    def ragdoll(name, pos, standing=3.0, down=5.0, shove=3.0, direction=(0, 0.35, -1), stay=False,
                tint="1,1,1,1", sign=True, pedestal=False, note=""):
        comps = [
            character(S, name, tint=tint),
            model_physics(S, name, f"Character: {name}", enabled=stay),
            S.comp("TestGround.RagdollRack", "rag/" + name, Down=down, Physics=None, Renderer=None,
                   Shove=shove, ShoveDirection=v(*direction), Sign=sign_ref(S, name) if sign else None,
                   Standing=standing, StayDown=stay),
        ]
        if not stay:
            comps.insert(1, S.comp("TestGround.CharacterGraph", "graph/" + name, Renderer=None, Sign=None,
                                   Sweep=0.0, TopSpeed=0.0, WaveEvery=0.0, WaveFor=0.0))
        return stand(S, name, note, pos, comps, pedestal=pedestal, sign_text=name)

    # --- the switch --------------------------------------------------------
    stands = [
        ragdoll("drop", (-5.0, 0, 0), shove=0.0, note="no push, straight down"),
        ragdoll("shove back", (0, 0, 0), shove=4.0, direction=(0, 0.4, 1), tint="1,0.88,0.8,1",
                note="pushed backwards as it goes"),
        ragdoll("spin", (5.0, 0, 0), shove=5.0, direction=(1, 0.6, 0), tint="0.85,0.92,1,1",
                note="pushed sideways"),
    ]
    areas.append(S.area("The switch", "physics on, animation off, a push - then back on its feet",
                        -14, 22, children=stands))

    # --- joints: one left down for good, so the limits can be read ---------
    stands = []
    for i, x in enumerate(row(4, 3.4)):
        stands.append(ragdoll(f"limp {i + 1}", (x, 0, 0), stay=True, shove=2.0 + i * 1.5,
                              direction=(0.3 * (i - 1.5), 0.5, -1), sign=(i == 0),
                              tint="0.92,0.92,0.95,1", note=""))
    areas.append(S.area("Joints", "dropped once and left there: sixteen bodies, fifteen joints, one piece",
                        -32, 20, children=stands))

    # --- a pile, dropped from a height ------------------------------------
    pile = []
    for i in range(6):
        x = (i % 3 - 1) * 0.9
        y = 2.2 + i * 1.3
        z = (i // 3) * 0.9 - 0.45
        pile.append(S.go(f"Pile {i + 1}", (x, y, z), rot=yaw(i * 47), components=[
            character(S, f"pile{i}", tint="0.8,0.82,0.88,1"),
            model_physics(S, f"pile{i}", f"Pile {i + 1}", enabled=True),
        ]))
    areas.append(S.area("A pile", "six of them dropped on each other - bodies against bodies, not just the floor",
                        -50, 20, children=[
                            S.label("pile", (0, 3.4, 4), "a pile", scale=0.6),
                            *pile,
                        ]))

    # --- a slope ----------------------------------------------------------
    slope = S.block("Slope", (0, 1.6, 2.0), (8, 0.4, 9), "0.28,0.3,0.34,1", rot=pitch_yaw(0, 0))
    slope["Rotation"] = "0.1736482,0,0,0.9848078"     # 20 degrees, nose down the row
    sliders = []
    for i, x in enumerate(row(3, 2.4)):
        sliders.append(S.go(f"Slider {i + 1}", (x, 3.6, -0.5), rot=yaw(180 + i * 20), components=[
            character(S, f"slide{i}", tint="1,0.85,0.7,1"),
            model_physics(S, f"slide{i}", f"Slider {i + 1}", enabled=True),
            S.comp("TestGround.ResetOnFall", "slidereset/" + str(i), Height=-4, SpawnPoint=None),
        ]))
    areas.append(S.area("A slope", "dropped on a ramp: friction, the joints under load, and where they end up",
                        -70, 22, depth=18, children=[slope, *sliders]))

    S.objects = [
        S.environment(),
        S.block("Ground", (0, -0.7, -40), (120, 0.5, 110), "0.2,0.21,0.24,1"),
        S.go("Areas", children=areas),
        S.player((0, 2.4, 6)),
        S.hud("Four rows of model physics: the switch both ways, the joint limits held open, a pile "
              "of them against each other, and a ramp. Q returns."),
    ]
    return S


# ---------------------------------------------------------------------------

def check_unique(objects):
    seen = {}

    def walk(o):
        for key, what in ((o["__guid"], o["Name"]), *((c["__guid"], c["__type"]) for c in o["Components"])):
            if key in seen:
                raise SystemExit(f"guid clash: {what} and {seen[key]}")
            seen[key] = what
        for c in o["Children"]:
            walk(c)

    for o in objects:
        walk(o)


def build():
    character_scene_ = character_scene()
    check_unique(character_scene_.objects)
    character_scene_.write("animation/character.scene")
    register_in_menu("animation/character.scene", "Character", "Animation",
                     "Clips, a graph built in code, root motion, bone and attachment markers, and jiggle bones")

    ragdoll = ragdoll_scene()
    check_unique(ragdoll.objects)
    ragdoll.write("animation/ragdoll.scene")
    register_in_menu("animation/ragdoll.scene", "Ragdoll", "Physics",
                     "Model physics: the switch both ways, the joint limits, a pile, and a ramp")


if __name__ == "__main__":
    build()
