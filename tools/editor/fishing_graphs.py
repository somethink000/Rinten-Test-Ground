"""Builds the AnimGraphs of the fishing models: each hinged part is a clip posed by a float parameter.

Run from the project root with the editor open: python3 tools/editor/fishing_graphs.py [model ...]
The clips come from ~/Documents/Blender/tools/fishing/export_*.py. A model re-exported from Blender
loses its graph (the export writes the .mdl afresh), so run this again after every export.
"""
import json, sys, urllib.request


def call(name, args):
    body = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "call_tool", "arguments": {"name": name, "arguments": args}}}
    req = urllib.request.Request("http://127.0.0.1:7269/mcp", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        text = "".join(c.get("text", "") for c in json.loads(r.read())["result"]["content"])
    try:
        return json.loads(text)
    except ValueError:
        raise SystemExit(f"{name}: {text[:1500]}")


def revision(path):
    return call("animgraph_inspect", {"path": path})["Revision"]


def pose(alias, clip, parameter):
    """A clip held at the point a parameter says, nought to one through it."""
    return [
        {"Operation": "add_parameter", "Alias": "p_" + alias, "ParameterType": "Float", "Values": {"Name": parameter}},
        {"Operation": "add_node", "Type": "FloatParameterNode", "Alias": "f_" + alias, "Values": {"ParameterName": parameter}},
        {"Operation": "add_node", "Type": "AnimationPoseNode", "Alias": alias, "Values": {"DefaultVariationData": {"AnimationName": clip}}},
        {"Operation": "connect", "FromNode": "@f_" + alias, "FromOutput": "Value", "ToNode": "@" + alias, "ToInput": "Time"},
    ]


def build(path, poses, layers=()):
    """poses[0] is the base; each of layers is (pose alias, bone) laid over it for that bone only."""
    # The graph tools edit the editor's copy of the model's definition and save that
    # copy whole - so a copy read before the last export from Blender would write
    # the old clips back over the new. Hand it the file as it is on disk first.
    # (asset_write recompiles the file but leaves that copy as it was.)
    call_text("execute_code", {"code": f'''var asset = AssetSystem.FindByPath( "{path}" );
asset.TryLoadResource<ModelDefinition>( out var d ); d.LoadFromJson( System.IO.File.ReadAllText( asset.GetSourceFile( true ) ) ); return 0;'''})

    try:
        call("animgraph_create", {"path": path, "skeleton": path})
    except SystemExit:
        pass  # it has a graph already - it is started over below

    info = call("animgraph_inspect", {"path": path})
    rev = info["Revision"]
    graph = info["Graphs"][0] if "Graphs" in info else info
    nodes = graph.get("Nodes", [])
    result = next(n for n in nodes if "Result" in n.get("Type", ""))["Id"]

    ops = [{"Operation": "remove_node", "Node": n["Id"]} for n in nodes if n["Id"] != result]
    ops += [{"Operation": "remove_parameter", "Parameter": p.get("Id") or p.get("Name")} for p in info.get("Parameters", [])]
    for alias, clip, parameter in poses:
        ops += pose(alias, clip, parameter)

    out = "@" + poses[0][0]
    if layers:
        ops.append({"Operation": "add_node", "Type": "LayerBlendNode", "Alias": "blend"})
        ops.append({"Operation": "connect", "FromNode": out, "FromOutput": "Result", "ToNode": "@blend", "ToInput": "Base"})
        for i, (alias, bone) in enumerate(layers):
            if i: ops.append({"Operation": "add_item", "Node": "@blend", "Property": "Layers", "Index": -1, "Value": {}})
            ops += [
                {"Operation": "add_node", "Type": "BoneMaskNode", "Alias": "m_" + alias, "Values": {"BoneName": bone}},
                {"Operation": "add_node", "Type": "LocalLayerNode", "Alias": "l_" + alias},
                {"Operation": "connect", "FromNode": "@" + alias, "FromOutput": "Result", "ToNode": "@l_" + alias, "ToInput": "Input"},
                {"Operation": "connect", "FromNode": "@m_" + alias, "FromOutput": "Mask", "ToNode": "@l_" + alias, "ToInput": "BoneMask"},
                {"Operation": "connect", "FromNode": "@l_" + alias, "FromOutput": "Layer", "ToNode": "@blend", "ToInput": f"Layer{i}"},
            ]
        out = "@blend"
    ops.append({"Operation": "connect", "FromNode": out, "FromOutput": "Result", "ToNode": result, "ToInput": "Pose"})

    edit = call("animgraph_edit", {"path": path, "expectedRevision": rev, "operations": ops})
    rev = edit.get("Revision") or revision(path)
    saved = call("animgraph_compile", {"path": path, "save": True, "expectedRevision": rev})
    # The engine keeps each model's definition from the first time it was read, and only
    # then learns whether it has a graph; the one it read before this save had none.
    # Its clips are cached the same way, from whenever they were first sampled.
    folder = path.rsplit("/", 1)[0]
    forget = "".join(f'CoreClips.Forget( "{folder}/{clip}.anim_c" ); ' for _, clip, _ in poses)
    call_text("execute_code", {"code": f'CoreSkeletons.Forget( "{path}" ); {forget}return 0;'})
    warnings = [w["Message"] for w in saved.get("Compile", saved).get("Warnings", [])]
    print(path, "warnings:", warnings or "none")


def check(path, parameter, bone, value=1):
    """Spawns the model, poses the parameter at 0 and 1 a frame apart, and returns the bone's local angles at each."""
    import time
    probe = f'ActiveScene.Directory.FindByName("graph_probe").First().Components.Get<SkinnedModelRenderer>()'
    call_text("execute_code", {"code": f'''using var scope = ActiveScene.Push();
foreach ( var old in ActiveScene.Directory.FindByName( "graph_probe" ).ToList() ) old.Destroy();
var go = new GameObject( true, "graph_probe" ); go.WorldPosition = new Vector3( 0, -50, 0 );
var r = go.Components.Create<SkinnedModelRenderer>(); r.Model = Model.Load( "{path}" ); r.CreateBoneObjects = true;
r.Set( "{parameter}", 0f ); return 0;'''})
    angles = []
    for step in (value, None):
        time.sleep(1.0)
        code = f'var r = {probe}; var a = r.GetBoneObject( "{bone}" ).LocalRotation.Angles(); '
        code += f'r.Set( "{parameter}", {step}f ); return a.ToString();' if step is not None else 'r.GameObject.Destroy(); return a.ToString();'
        angles.append(call_text("execute_code", {"code": code}))
    return angles


def call_text(name, args):
    body = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "call_tool", "arguments": {"name": name, "arguments": args}}}
    req = urllib.request.Request("http://127.0.0.1:7269/mcp", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return "".join(c.get("text", "") for c in json.loads(r.read())["result"]["content"]).split("\n")[0]


CHECKS = {"worm_box": [("lid", "lid")], "perch": [("mouth", "jaw")], "carp": [("mouth", "jaw")],
          "rod": [("bail", "bail")]}

GRAPHS = {
    "worm_box": lambda p: build(p, [("lid", "lid", "lid")]),
    "perch": lambda p: build(p, [("mouth", "perch_mouth", "mouth")]),
    "carp": lambda p: build(p, [("mouth", "carp_mouth", "mouth")]),
    # The crank is a separate model the hand turns, not a bone in this graph.
    "rod": lambda p: build(p, [("bail", "bail", "bail")]),
}

if __name__ == "__main__":
    for name in sys.argv[1:] or GRAPHS:
        GRAPHS[name](f"models/fishing/{name}.mdl")
        for parameter, bone in CHECKS[name]:
            closed, opened = check(f"models/fishing/{name}.mdl", parameter, bone, 0.25 if parameter == "crank" else 1)
            print(f"  {parameter} -> {bone}: at 0 {closed} | at 1 {opened}")
