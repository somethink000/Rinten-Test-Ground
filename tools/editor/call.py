import json,urllib.request,sys
def call(name,args):
    body={"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":name,"arguments":args}}
    req=urllib.request.Request("http://127.0.0.1:7269/mcp",data=json.dumps(body).encode(),headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream"})
    with urllib.request.urlopen(req,timeout=60) as r:
        d=json.loads(r.read().decode())
    for c in d.get("result",{}).get("content",[]):
        if c.get("type")=="text": print(c["text"])
if __name__=="__main__":
    call(sys.argv[1], json.loads(sys.argv[2]) if len(sys.argv)>2 else {})
