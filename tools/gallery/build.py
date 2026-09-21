#!/usr/bin/env python3
"""Builds a gallery scene inside the running editor: common.cs and <name>.cs go
to the editor's execute_code as one snippet, the engine makes the objects and
writes the .scene, and whatever the snippet logged or returned is printed.

    python3 build.py shadows            # the editor on Test Ground, MCP on 7269
    RINTEN_MCP_PORT=7270 python3 build.py shadows
"""
import json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = os.environ.get("RINTEN_MCP_PORT", "7269")
USING = re.compile(r"^using [\w.]+;\s*$")


def snippet(name):
    """common.cs and the scene's file as one snippet: every using line first,
    since the snippet is read as a file with top-level statements."""
    usings, body = [], []
    for filename in ("common.cs", name + ".cs"):
        with open(os.path.join(HERE, filename)) as f:
            for line in f:
                (usings if USING.match(line) else body).append(line)
    return "".join(dict.fromkeys(usings)) + "\n" + "".join(body)


def execute(code):
    body = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "execute_code", "arguments": {"code": code}}}
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}/mcp", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read().decode())


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    name = sys.argv[1].removesuffix(".cs")
    reply = execute(snippet(name))
    if "error" in reply:
        sys.exit(reply["error"].get("message", json.dumps(reply["error"])))
    result = reply.get("result", {})
    for c in result.get("content", []):
        if c.get("type") == "text":
            print(c["text"])
    if result.get("isError"):
        sys.exit(1)


if __name__ == "__main__":
    main()
