"""hungrX cloud poster (GitHub Actions). Posts ONE reel per run from a batch, Reels tab only.
Env: IG_ACCESS_TOKEN, IG_USER_ID (repo secrets), BATCH, START (YYYY-MM-DD, IST), DRY=1 for a test.
Never prints the token."""
import json,os,sys,time,datetime,urllib.request,urllib.parse
T=os.environ["IG_ACCESS_TOKEN"].strip(); U=os.environ.get("IG_USER_ID","17841468871070733").strip()
BATCH=os.environ.get("BATCH","mcd_2026_11"); START=os.environ.get("START","2026-11-20"); DRY=os.environ.get("DRY")=="1"
B="https://graph.instagram.com/v23.0"; LOG="posted_log.csv"
ist=datetime.datetime.utcnow()+datetime.timedelta(hours=5,minutes=30)
if not DRY and ist.strftime("%Y-%m-%d")<START: print("Before start date",START,"- nothing to do"); sys.exit(0)
ALL=json.load(open(f"batches/{BATCH}.json"))
done=open(LOG).read() if os.path.exists(LOG) else ""
if not DRY and ist.strftime("%Y-%m-%d") in done: print("Already posted today (IST) - skip"); sys.exit(0)
todo=[k for k in sorted(ALL) if f",{BATCH}:{k}," not in done]
if not todo: print("ALL POSTED for",BATCH); sys.exit(0)
PID=todo[0]; M=ALL[PID]
def g(p,q):q=dict(q);q["access_token"]=T;return json.load(urllib.request.urlopen(B+"/"+p+"?"+urllib.parse.urlencode(q),timeout=60))
def p(path,q):q=dict(q);q["access_token"]=T;return json.load(urllib.request.urlopen(urllib.request.Request(B+"/"+path,urllib.parse.urlencode(q).encode()),timeout=120))
Q={"media_type":"REELS","video_url":M["video_url"],"caption":M["caption"],"share_to_feed":"true" if M.get("grid") else "false"}
try: c=p(U+"/media",Q)["id"]
except urllib.error.HTTPError as e: sys.exit("container error: "+e.read().decode()[:300])
s=None
for _ in range(50):
    time.sleep(6); s=g(c,{"fields":"status_code"}).get("status_code")
    if s in("FINISHED","ERROR","EXPIRED"): break
if s!="FINISHED": sys.exit("processing failed: "+str(s))
if DRY: print("DRY RUN OK (container ready, not published)",PID); sys.exit(0)
mid=p(U+"/media_publish",{"creation_id":c})["id"]; info=g(mid,{"fields":"permalink"})
open(LOG,"a").write(f"{ist:%Y-%m-%d %H:%M},{BATCH}:{PID},{mid},{info.get('permalink')}\n")
print("PUBLISHED",PID,info.get("permalink"))
