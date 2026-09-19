#!/usr/bin/env python3
"""What the gallery scenes share: objects, components, the environment, a
player, a HUD, and areas laid out in rows away from the spawn - the same
shape tools/fx/scenegen.py gives the particle scene."""
import json, uuid, os

ROOT = "/home/sampesss/Documents/Rinten Projects/Rinten-Test-Ground/Assets"

EVENTS = {"OnComponentDestroy": None, "OnComponentDisabled": None, "OnComponentEnabled": None,
          "OnComponentFixedUpdate": None, "OnComponentStart": None, "OnComponentUpdate": None}

RENDER = {"GameLayer": True, "OverlayLayer": False, "BloomLayer": False, "AfterUILayer": False}

def v(*a): return ",".join(str(x) for x in a)


class Scene:
    """One scene's worth of ids: every guid is a name under the scene's own
    root, so a regenerated scene keeps its ids and the editor's references
    into it stay good."""

    def __init__(self, key, title, description):
        self.key = key
        self.title = title
        self.description = description
        self.objects = []

    def guid(self, name):
        return str(uuid.uuid5(uuid.NAMESPACE_URL, f"rinten-gallery/{self.key}/{name}"))

    # -- objects and components --------------------------------------------

    def go(self, name, pos=(0, 0, 0), rot="0,0,0,1", scale=(1, 1, 1), tags="", components=(), children=(), enabled=True):
        return {"__guid": self.guid("go/" + name), "__version": 2, "Flags": 0, "Name": name,
                "Position": v(*pos), "Rotation": rot, "Scale": v(*scale) if not isinstance(scale, str) else scale,
                "Tags": tags, "Enabled": enabled,
                "NetworkMode": 2, "NetworkFlags": 0, "NetworkOrphaned": 0, "NetworkTransmit": True, "OwnerTransfer": 1,
                "Components": list(components), "Children": list(children)}

    def comp(self, type_, name, **props):
        d = {"__type": type_, "__guid": self.guid("comp/" + name), "__enabled": True, "Flags": 0}
        d.update(props)
        d.update(EVENTS)
        return d

    def ref_go(self, name):
        return {"_type": "gameobject", "go": self.guid("go/" + name)}

    def ref_comp(self, comp_name, go_name, type_name):
        return {"_type": "component", "component_id": self.guid("comp/" + comp_name), "go": self.guid("go/" + go_name), "component_type": type_name}

    def model(self, name, tint="1,1,1,1", material=None, model="models/dev/box.mdl", render="On", options=None, materials=None):
        return self.comp("Rinten.ModelRenderer", "model/" + name, BodyGroups=18446744073709551615, CreateAttachments=False,
                         MaterialGroup=None, MaterialOverride=material, Materials=materials, Model=model,
                         RenderOptions=options or RENDER, RenderType=render, Tint=tint)

    def box_collider(self, name, static=True, trigger=False):
        return self.comp("Rinten.BoxCollider", "collider/" + name, Center="0,0,0", ColliderFlags=0, Elasticity=None, Friction=None,
                         IsTrigger=trigger, OnObjectTriggerEnter=None, OnObjectTriggerExit=None, OnTriggerEnter=None, OnTriggerExit=None,
                         RollingResistance=None, Scale="1,1,1", Static=static, Surface=None, SurfaceVelocity="0,0,0")

    def block(self, name, pos, scale, tint, material=None, model="models/dev/box.mdl", tags="world", render="On", collide=True, rot="0,0,0,1"):
        comps = [self.model(name, tint, material, model, render)]
        if collide: comps.append(self.box_collider(name))
        return self.go(name, pos, rot=rot, scale=scale, tags=tags, components=comps)

    def text_scope(self, text, color="0.9,0.94,1,1", font="Poppins", size=50, weight=700, italic=False, line_height=1.1,
                   letter_spacing=0, outline=None, shadow=True):
        return {"Text": text, "TextColor": color, "FontName": font, "FontSize": size, "FontWeight": weight,
                "FontItalic": italic, "FontVariantNumeric": "Normal", "LineHeight": line_height, "LetterSpacing": letter_spacing,
                "WordSpacing": 0, "FilterMode": "Bilinear", "FontSmooth": "Auto",
                "Outline": outline or {"Enabled": False, "Size": 4, "Color": "0,0,1,1"},
                "Shadow": {"Enabled": shadow, "Size": 6, "Color": "0,0,0,0.8", "Offset": "3,3"},
                "OutlineUnder": {"Enabled": False, "Size": 4, "Color": "0,1,0,1"},
                "ShadowUnder": {"Enabled": False, "Size": 4, "Color": "0,0,0,1", "Offset": "4,4"}}

    def text(self, name, scope, scale=0.26, billboard="YOnly", blend="Normal", fog=1, halign="Center", valign="Center", options=None):
        return self.comp("Rinten.TextRenderer", "text/" + name, __version=2, Billboard=billboard, BlendMode=blend, FogStrength=fog,
                         HorizontalAlignment=halign, RenderOptions=options or RENDER, Scale=scale, TextScope=scope, VerticalAlignment=valign)

    def label(self, name, pos, text, scale=0.26, color="0.9,0.94,1,1", size=50):
        return self.go(f"Label: {name}", pos, components=[self.text("label/" + name, self.text_scope(text, color=color, size=size), scale=scale)])

    # -- the furniture every scene has --------------------------------------

    def environment(self, sun_brightness=1.2, sun_rot="-0.4508033,0.1919843,0.0999407,0.8659851", sun_color="1,0.95,0.88,1",
                    ambient="0.2,0.22,0.3,1", sky_tint="0.75,0.8,0.9,1", shadows=True, shadow_detail=64, source_radius=0.05, sky_indirect=True):
        return self.go("Environment", children=[
            self.go("Sun", rot=sun_rot, tags="light_directional,light", components=[
                self.comp("Rinten.DirectionalLight", "sun", __version=1, Attenuation=1, Brightness=sun_brightness,
                          Contribution="Diffuse, Specular, Transmissive", FogMode="Enabled", FogStrength=1, LightColor=sun_color,
                          ShadowAngle=0.6, ShadowDetail=shadow_detail, Shadows=shadows, SkyColor="0,0,0,0", SourceRadius=source_radius)]),
            self.go("Ambient", components=[self.comp("Rinten.AmbientLight", "ambient", Color=ambient)]),
            self.go("2D Skybox", tags="skybox", components=[self.comp("Rinten.SkyBox2D", "sky", SkyIndirectLighting=sky_indirect,
                    SkyMaterial="materials/skybox/procedural.mat", Tint=sky_tint)]),
        ])

    def player(self, pos, pitch_rot="-0.0697565,0,0,0.9975641", fov=75, speed=7, bloom=True):
        cam = [self.comp("Rinten.CameraComponent", "camera", BackgroundColor="0.05,0.06,0.08,1", ClearFlags="All", EnablePostProcessing=True,
                         FieldOfView=fov, FovAxis="Horizontal", IsMainCamera=True, Orthographic=False, OrthographicHeight=10,
                         PostProcessAnchor=None, Priority=1, RenderExcludeTags="", RenderTags="", RenderTexture=None, TargetEye="None",
                         Viewport="0,0,1,1", ZFar=400, ZNear=0.05)]
        if bloom:
            cam.append(self.comp("Rinten.Bloom", "bloom", __version=1, Mode="Additive", Spread=0.6, Strength=0.6, Threshold=1, Tint="1,1,1,1"))
        return self.go("Player", pos, components=[self.comp("Template.Player", "player",
            Camera=self.ref_comp("camera", "Camera", "CameraComponent"), PitchClamp=89, RunScale=3, Speed=speed)],
            children=[self.go("Camera", rot=pitch_rot, tags="maincamera", components=cam)])

    def hud(self, note, extra=()):
        return self.go("HUD", components=[
            self.comp("Rinten.ScreenPanel", "hud/panel", AutoScreenScale=True, Opacity=1, Scale=1, ScaleStrategy="ConsistentHeight", TargetCamera=None, ZIndex=100),
            self.comp("TestGround.SceneHud", "hud/scene", Note=note, Title=self.title),
            self.comp("TestGround.ReturnToMenu", "hud/return", Key="Q", MenuScene=None),
            *extra])

    # -- areas: rows away from the spawn -----------------------------------

    SLAB = "0.34,0.36,0.4,1"
    WALL = "0.11,0.12,0.15,1"

    def area(self, title, note, z, width, depth=14, wall=True, wall_height=6, slab_material="materials/dev/grid.mat", slab_tint=None, children=()):
        kids = [self.block(f"Slab: {title}", (0, -0.2, z), (width, 0.4, depth), slab_tint or self.SLAB, slab_material)]
        if wall:
            kids.append(self.block(f"Wall: {title}", (0, wall_height / 2, z - depth / 2), (width, wall_height, 0.5), self.WALL))
        # Just over the wall: from the spawn's height the next row's title is
        # behind this row's wall rather than stacked over it.
        kids.append(self.label(f"Area: {title}", (0, wall_height + 0.9, z - depth / 2 + 1), f"{title}\n{note}", scale=0.9))
        kids.extend(children)
        return self.go(f"Area: {title}", children=kids)

    @staticmethod
    def stagger_signs(stations, rise=0.9):
        """Every other station's sign a step higher, so two signs wider than
        the gap between their stands never sit side by side."""
        for i, station in enumerate(stations):
            if i % 2 == 0: continue
            for child in station.get("Children", []):
                if child["Name"].startswith("Label:"):
                    x, y, z = (float(c) for c in child["Position"].split(","))
                    child["Position"] = v(x, y + rise, z)
        return stations

    # -- out ------------------------------------------------------------------

    def write(self, filename, nav=False):
        scene = {
            "__guid": self.guid("scene"),
            "SceneProperties": {
                "NetworkInterpolation": True, "TimeScale": 1, "WantsSystemScene": True, "Metadata": {},
                "NavMesh": {"Enabled": nav, "IncludeStaticBodies": True, "IncludeKeyframedBodies": True, "EditorAutoUpdate": False,
                            "AgentHeight": 1.6, "AgentRadius": 0.4, "AgentStepSize": 0.45, "AgentMaxSlope": 40,
                            "ExcludedBodies": "", "IncludedBodies": "", "DeferGeneration": False, "CustomBounds": False},
                "GameObjectSystems": {"Rinten.SelectionSetsSystem": {"Data": {"SelectionSets": []}}},
            },
            "GameObjects": self.objects,
            "ResourceVersion": 4, "Title": self.title, "Description": self.description,
            "__references": [], "__version": 4,
        }
        path = os.path.join(ROOT, "scenes", filename)
        with open(path, "w") as f:
            json.dump(scene, f, indent=2)
        print("wrote", path)
        return path


def yaw(deg):
    """A rotation about Y as the quaternion string the scene wants."""
    import math
    h = math.radians(deg) / 2
    return v(0, round(math.sin(h), 7), 0, round(math.cos(h), 7))


def pitch_yaw(pitch_deg, yaw_deg):
    """Pitch about X then yaw about Y, as a quaternion string. A negative
    pitch turns forward (-Z) downward: a sun or a spot pointing at the floor
    is pitch_yaw(-90, 0)."""
    import math
    cp, sp = math.cos(math.radians(pitch_deg) / 2), math.sin(math.radians(pitch_deg) / 2)
    cy, sy = math.cos(math.radians(yaw_deg) / 2), math.sin(math.radians(yaw_deg) / 2)
    # q = qy * qx
    x = cy * sp
    y = sy * cp
    z = -sy * sp
    w = cy * cp
    return v(round(x, 7), round(y, 7), round(z, 7), round(w, 7))


def register_in_menu(scene_file, title, category, description):
    """Adds the scene's card to the main menu once, in place of an older card for the same file."""
    path = os.path.join(ROOT, "scenes/main.scene")
    with open(path) as f:
        main = json.load(f)
    entry = {"Scene": f"scenes/{scene_file}", "Title": title, "Category": category, "Description": description, "DisplayName": title}
    def walk(o):
        for c in o.get("Components", []):
            if c.get("__type") == "TestGround.SceneMenu":
                entries = c.setdefault("Scenes", [])
                for i, e in enumerate(entries):
                    if (e.get("Scene") or "").lower() == entry["Scene"].lower():
                        entries[i] = entry
                        return True
                entries.append(entry)
                return True
        for ch in o.get("Children", []):
            if walk(ch): return True
        return False
    if not walk({"Children": main["GameObjects"]}):
        raise SystemExit("no SceneMenu in main.scene")
    with open(path, "w") as f:
        json.dump(main, f, indent=2)
    print("registered", title, "in the menu")
