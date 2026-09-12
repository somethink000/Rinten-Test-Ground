import json,urllib.request,base64,sys,time,math
def call(name,args):
    body={"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":name,"arguments":args}}
    req=urllib.request.Request("http://127.0.0.1:7269/mcp",data=json.dumps(body).encode(),headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream"})
    return json.loads(urllib.request.urlopen(req,timeout=90).read().decode())
if __name__=="__main__":
    name, dist, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    r=call("find_game_objects",{"name":name}); items=json.loads(r['result']['content'][0]['text'])['Results']
    go=[i for i in items if i['Name']==name][0]
    g=json.loads(call("get_game_object",{"id":go['Id']})['result']['content'][0]['text'])
    p=[float(x) for x in g['WorldPosition'].split(',')]
    # camera: back toward the origin side, slightly above, looking at the body
    d=math.hypot(p[0],p[2]) or 1
    dx,dz=p[0]/d,p[2]/d
    cam=[p[0]-dx*dist*0.7 - dz*dist*0.7, p[1]+dist*0.3, p[2]-dz*dist*0.7 + dx*dist*0.7]
    yaw=math.degrees(math.atan2(-(p[0]-cam[0]), -(p[2]-cam[2])))
    pitch=math.degrees(math.atan2(cam[1]-p[1], math.hypot(p[0]-cam[0],p[2]-cam[2])))
    call("set_editor_camera",{"position":",".join(f"{v:.2f}" for v in cam),"angles":f"{pitch:.1f},{yaw:.1f},0"})
    time.sleep(float(sys.argv[4]) if len(sys.argv)>4 else 0.6)
    dd=call("editor_camera_screenshot",{"width":1100,"height":620})
    for c in dd["result"]["content"]:
        if c.get("type")=="image": open(out,"wb").write(base64.b64decode(c["data"])); print("saved",out,p)
