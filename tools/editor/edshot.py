import json,urllib.request,base64,sys,time
def call(name,args):
    body={"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":name,"arguments":args}}
    req=urllib.request.Request("http://127.0.0.1:7269/mcp",data=json.dumps(body).encode(),headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream"})
    return json.loads(urllib.request.urlopen(req,timeout=90).read().decode())
pos, ang, out = sys.argv[1], sys.argv[2], sys.argv[3]
call("set_editor_camera",{"position":pos,"angles":ang})
time.sleep(float(sys.argv[4]) if len(sys.argv)>4 else 0.5)
d=call("editor_camera_screenshot",{"width":1100,"height":620})
for c in d["result"]["content"]:
    if c.get("type")=="image": open(out,"wb").write(base64.b64decode(c["data"])); print("saved",out)
    elif c.get("type")=="text": print(c["text"][:300])
