"""hungrX: publish one approved reel. Usage: IG_TOKEN=... python3 post_reel.py P01"""
import json,os,sys,time,urllib.request,urllib.parse
PID=sys.argv[1]; T=os.environ["IG_TOKEN"]; U="17841468871070733"; B="https://graph.instagram.com/v23.0"
M=json.load(urllib.request.urlopen("https://raw.githubusercontent.com/febbinchacko7t-lgtm/hungrx-reels/main/batches/b01.json?t=%d"%time.time(),timeout=60))[PID]
CAP,VID=M["caption"],M["video_url"]
def g(p,q):q["access_token"]=T;return json.load(urllib.request.urlopen(B+"/"+p+"?"+urllib.parse.urlencode(q),timeout=60))
def p(path,q):q["access_token"]=T;return json.load(urllib.request.urlopen(urllib.request.Request(B+"/"+path,urllib.parse.urlencode(q).encode()),timeout=120))
first=CAP.split("\n")[0]
for m in g("me/media",{"fields":"caption,permalink","limit":"10"}).get("data",[]):
    if (m.get("caption") or "").startswith(first): print("SKIP already posted",m.get("permalink"));sys.exit(0)
Q={"media_type":"REELS","video_url":VID,"caption":CAP,"share_to_feed":"true"}
if M.get("thumb_offset") is not None: Q["thumb_offset"]=str(M["thumb_offset"])
c=p(U+"/media",Q)["id"]
s=None
for _ in range(50):
    time.sleep(6);s=g(c,{"fields":"status_code"}).get("status_code")
    if s in("FINISHED","ERROR","EXPIRED"):break
if s!="FINISHED":sys.exit("processing failed: "+str(s))
if os.environ.get("DRY"): print("DRY RUN OK",PID,c); sys.exit(0)
mid=p(U+"/media_publish",{"creation_id":c})["id"];info=g(mid,{"fields":"permalink,timestamp"})
print("PUBLISHED",json.dumps({"media_id":mid,"permalink":info.get("permalink"),"posted_at":info.get("timestamp")}))
