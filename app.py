"""
╔══════════════════════════════════════════╗
║        MITTU AI - by Shreechand         ║
║     Python Flask Assistant App          ║
╚══════════════════════════════════════════╝

Chalane ka tarika:
    python3 app.py

Phir browser mein kholo:
    http://localhost:5000
"""

from flask import Flask, request, jsonify, render_template_string
import urllib.request
import urllib.error
import json
import os

app = Flask(__name__)

CREATOR = "Shreechand"
BOT_NAME = "Mittu"
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")  # .env se ya seedha yahan likho

SYSTEM_PROMPT = f"""Aap {BOT_NAME} hain — ek smart, friendly aur helpful AI assistant jo {CREATOR} ne banaya hai.

Aap office kaam mein madad karti hain: emails likhna, reports banana, calculations, planning, news, mausam — sab kuch.

Rules:
1. Hamesha Hindi ya Hinglish mein jawab dein.
2. Naam poochha jaye to bolein: "Mera naam {BOT_NAME} hai!"
3. Creator poochha jaye to bolein: "{CREATOR} ne mujhe banaya hai!"
4. Jawab helpful, clear aur friendly rakhein.
5. Thodi emojis use karein."""

HTML_PAGE = """<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1"/>
<meta name="theme-color" content="#7c3aed"/>
<meta name="mobile-web-app-capable" content="yes"/>
<meta name="apple-mobile-web-app-capable" content="yes"/>
<meta name="apple-mobile-web-app-title" content="Mittu AI"/>
<title>Mittu AI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{
  --bg:#0d0d1a; --surface:#13102a; --card:#1e1040;
  --border:#2a1f4e; --purple:#7c3aed; --pink:#ec4899;
  --text:#f3e8ff; --muted:#7c6b9a; --green:#10b981;
}
html,body{
  height:100%;width:100%;overflow:hidden;
  background:var(--bg);
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Tahoma,sans-serif;
  color:var(--text);
}
body{display:flex;flex-direction:column;height:100dvh;max-width:480px;margin:0 auto}

/* HEADER */
#hdr{
  background:linear-gradient(135deg,#3b0764,#831843);
  padding:12px 14px;display:flex;align-items:center;gap:11px;flex-shrink:0;
}
#av{
  width:46px;height:46px;border-radius:50%;position:relative;flex-shrink:0;
  background:linear-gradient(135deg,#f472b6,#a855f7);
  display:flex;align-items:center;justify-content:center;font-size:22px;
  border:2px solid rgba(255,255,255,.25);
}
#od{
  position:absolute;bottom:1px;right:1px;
  width:12px;height:12px;background:var(--green);
  border-radius:50%;border:2px solid #3b0764;
  animation:blink 2s infinite;
}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
#hi{flex:1;min-width:0}
#hi h1{font-size:16px;font-weight:700;color:#fff}
#hi p{font-size:11px;color:#c4b5d8;margin-top:1px}
#vbtn{
  background:rgba(255,255,255,.12);border:none;border-radius:50%;
  width:36px;height:36px;color:#fff;font-size:16px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
}

/* SPEAKING */
#spk{display:none;align-items:center;justify-content:center;gap:4px;padding:5px;
  background:rgba(124,58,237,.12);font-size:11px;color:var(--purple);flex-shrink:0}
#spk.on{display:flex}
.wv{width:3px;border-radius:2px;background:var(--purple);animation:wv .9s ease-in-out infinite}
.wv:nth-child(1){height:6px}.wv:nth-child(2){height:14px;animation-delay:.1s}
.wv:nth-child(3){height:10px;animation-delay:.2s}.wv:nth-child(4){height:18px;animation-delay:.3s}
.wv:nth-child(5){height:8px;animation-delay:.4s}
@keyframes wv{0%,100%{transform:scaleY(.3)}50%{transform:scaleY(1)}}

/* MESSAGES */
#msgs{
  flex:1;overflow-y:auto;padding:12px 10px;
  display:flex;flex-direction:column;gap:9px;
  -webkit-overflow-scrolling:touch;scroll-behavior:smooth;
}
#msgs::-webkit-scrollbar{width:2px}
#msgs::-webkit-scrollbar-thumb{background:var(--border)}
.row{display:flex;align-items:flex-end;gap:7px}
.row.me{flex-direction:row-reverse}
.av2{
  width:28px;height:28px;border-radius:50%;flex-shrink:0;font-size:13px;
  background:linear-gradient(135deg,#f472b6,#a855f7);
  display:flex;align-items:center;justify-content:center;
}
.row.me .av2{background:linear-gradient(135deg,#5b21b6,#3b0764)}
.bw{display:flex;flex-direction:column;max-width:78%}
.row.me .bw{align-items:flex-end}
.bub{
  padding:9px 13px;border-radius:16px;font-size:14px;
  line-height:1.5;word-break:break-word;white-space:pre-wrap;
}
.row.ai .bub{
  background:var(--card);border:1px solid var(--border);
  color:var(--text);border-bottom-left-radius:3px;
}
.row.me .bub{background:var(--purple);color:#fff;border-bottom-right-radius:3px}
.ts{font-size:10px;color:var(--muted);margin-top:2px;padding:0 3px}

/* TYPING */
#typ{display:none;align-items:flex-end;gap:7px;padding:0 10px 4px}
#typ.on{display:flex}
.tbub{
  background:var(--card);border:1px solid var(--border);
  border-radius:16px;border-bottom-left-radius:3px;
  padding:11px 14px;display:flex;gap:4px;
}
.dot{width:6px;height:6px;background:var(--purple);border-radius:50%;animation:bd 1.1s infinite}
.dot:nth-child(2){animation-delay:.15s}.dot:nth-child(3){animation-delay:.3s}
@keyframes bd{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-7px)}}

/* CHIPS */
#chips{
  padding:7px 10px 2px;display:flex;gap:6px;
  overflow-x:auto;flex-shrink:0;scrollbar-width:none;
}
#chips::-webkit-scrollbar{display:none}
.chip{
  background:var(--card);border:1px solid var(--border);border-radius:18px;
  padding:6px 11px;font-size:12px;white-space:nowrap;cursor:pointer;
  color:#c4b5d8;flex-shrink:0;
}
.chip:active{background:var(--purple);color:#fff}

/* INPUT */
#inp-area{
  background:var(--surface);border-top:1px solid var(--border);
  padding:8px 10px 12px;display:flex;align-items:flex-end;gap:7px;flex-shrink:0;
}
#inp{
  flex:1;background:var(--card);border:1.5px solid var(--border);
  border-radius:20px;padding:10px 14px;font-size:15px;color:var(--text);
  outline:none;resize:none;max-height:110px;min-height:42px;
  line-height:1.4;font-family:inherit;
}
#inp::placeholder{color:var(--muted)}
#inp:focus{border-color:var(--purple)}
.ibtn{
  width:42px;height:42px;min-width:42px;border-radius:50%;border:none;
  cursor:pointer;display:flex;align-items:center;justify-content:center;
  font-size:18px;flex-shrink:0;transition:transform .1s;
}
.ibtn:active{transform:scale(.88)}
#micbtn{background:var(--card);border:1.5px solid var(--border);color:#c4b5d8}
#micbtn.on{background:#7f1d1d;border-color:#ef4444;animation:mp 1s infinite}
@keyframes mp{0%,100%{box-shadow:0 0 0 0 rgba(239,68,68,.4)}50%{box-shadow:0 0 0 8px rgba(239,68,68,0)}}
#sndbtn{background:linear-gradient(135deg,#ec4899,#7c3aed);color:#fff}
#sndbtn:disabled{opacity:.35;cursor:not-allowed}

/* KEY MISSING BANNER */
#keybanner{
  display:none;background:#450a0a;border-bottom:1px solid #7f1d1d;
  padding:8px 12px;font-size:12px;color:#fca5a5;flex-shrink:0;
  align-items:center;gap:8px;
}
#keybanner.on{display:flex}
#keybanner a{color:#f87171;text-decoration:underline}
</style>
</head>
<body>
<div id="keybanner">
  <span>⚠️ API Key nahi mila! <a href="#" onclick="showKeyInput()">Yahan click karke key daalo</a></span>
</div>
<div id="hdr">
  <div id="av">🌸<div id="od"></div></div>
  <div id="hi">
    <h1>Mittu AI ✨</h1>
    <p id="stxt">Online • Net se connected</p>
  </div>
  <button id="vbtn" onclick="toggleV()">🔊</button>
</div>
<div id="spk">
  <div class="wv"></div><div class="wv"></div><div class="wv"></div>
  <div class="wv"></div><div class="wv"></div>
  <span style="margin-left:4px">Mittu bol rahi hai…</span>
</div>
<div id="msgs"></div>
<div id="typ">
  <div class="av2">🌸</div>
  <div class="tbub"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
</div>
<div id="chips">
  <div class="chip" onclick="quick('Tumhara naam kya hai aur tumhe kisne banaya?')">🤖 Kaun ho?</div>
  <div class="chip" onclick="quick('Aaj ka mausam kaisa hai?')">🌤 Mausam</div>
  <div class="chip" onclick="quick('Ek professional email likhne mein madad karo')">✉️ Email</div>
  <div class="chip" onclick="quick('Ek funny joke sunao')">😄 Joke</div>
  <div class="chip" onclick="quick('Mujhe aaj ke kaam ke liye motivate karo')">💪 Motivation</div>
  <div class="chip" onclick="quick('Aaj ki top news kya hai?')">📰 News</div>
  <div class="chip" onclick="quick('Mujhe ek weekly work plan banana mein madad karo')">📋 Plan</div>
</div>
<div id="inp-area">
  <button class="ibtn" id="micbtn" onclick="toggleMic()">🎤</button>
  <textarea id="inp" placeholder="Mittu se kuch bhi puchho…" rows="1"></textarea>
  <button class="ibtn" id="sndbtn" onclick="doSend()">➤</button>
</div>
<script>
let voiceOn=true,micOn=false,busy=false,recog=null,voices=[];

function now(){return new Date().toLocaleTimeString('hi-IN',{hour:'2-digit',minute:'2-digit'})}
function esc(t){return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}

function addMsg(role,text){
  const m=document.getElementById('msgs');
  const d=document.createElement('div');
  d.className='row '+role;
  const av=role==='ai'?'🌸':'🧑';
  d.innerHTML=`<div class="av2">${av}</div><div class="bw"><div class="bub">${esc(text)}</div><div class="ts">${now()}</div></div>`;
  m.appendChild(d);
  m.scrollTop=m.scrollHeight;
  if(role==='ai'&&voiceOn) speak(text);
}

async function doSend(ov){
  if(busy)return;
  const inp=document.getElementById('inp');
  const txt=(ov||inp.value||'').trim();
  if(!txt)return;
  inp.value='';inp.style.height='auto';
  addMsg('user',txt);
  busy=true;
  document.getElementById('sndbtn').disabled=true;
  document.getElementById('typ').classList.add('on');
  document.getElementById('msgs').scrollTop=9999;
  try{
    const r=await fetch('/chat',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({message:txt})
    });
    const data=await r.json();
    document.getElementById('typ').classList.remove('on');
    if(data.error){addMsg('ai','❌ '+data.error);}
    else{addMsg('ai',data.reply);}
  }catch(e){
    document.getElementById('typ').classList.remove('on');
    addMsg('ai','Server se connect nahi ho pa raha. app.py chal raha hai? 🌐');
  }
  busy=false;
  document.getElementById('sndbtn').disabled=false;
}

function quick(t){doSend(t);}

function speak(text){
  if(!window.speechSynthesis)return;
  window.speechSynthesis.cancel();
  const c=text.replace(/[\\u{1F300}-\\u{1FFFF}]/gu,'').replace(/[*_#`]/g,'').trim();
  if(!c)return;
  const u=new SpeechSynthesisUtterance(c);
  u.lang='hi-IN';u.rate=0.92;u.pitch=1.25;u.volume=1;
  const fv=voices.find(v=>v.lang.startsWith('hi')&&/female|woman|girl/i.test(v.name))
    ||voices.find(v=>v.lang.startsWith('hi'))
    ||voices.find(v=>/female|woman/i.test(v.name));
  if(fv)u.voice=fv;
  u.onstart=()=>document.getElementById('spk').classList.add('on');
  u.onend=u.onerror=()=>document.getElementById('spk').classList.remove('on');
  window.speechSynthesis.speak(u);
}

function toggleV(){
  voiceOn=!voiceOn;
  const b=document.getElementById('vbtn');
  if(voiceOn){b.textContent='🔊';}
  else{window.speechSynthesis?.cancel();b.textContent='🔇';document.getElementById('spk').classList.remove('on');}
}

function toggleMic(){
  if(!recog){alert('Browser mic support nahi karta');return;}
  if(micOn){recog.stop();stopMic();}
  else{
    window.speechSynthesis?.cancel();
    recog.start();micOn=true;
    const b=document.getElementById('micbtn');
    b.classList.add('on');b.textContent='🔴';
  }
}
function stopMic(){
  micOn=false;
  const b=document.getElementById('micbtn');
  b.classList.remove('on');b.textContent='🎤';
}

// Auto resize textarea
document.getElementById('inp').addEventListener('input',function(){
  this.style.height='auto';
  this.style.height=Math.min(this.scrollHeight,110)+'px';
});
document.getElementById('inp').addEventListener('keydown',function(e){
  if(e.key==='Enter'&&!e.shiftKey&&window.innerWidth>600){e.preventDefault();doSend();}
});

// Send button - touch support
document.getElementById('sndbtn').addEventListener('touchend',function(e){
  e.preventDefault();doSend();
},{passive:false});

// Mic button - touch support
document.getElementById('micbtn').addEventListener('touchend',function(e){
  e.preventDefault();toggleMic();
},{passive:false});

if(window.speechSynthesis){
  const lv=()=>{voices=window.speechSynthesis.getVoices();};
  lv();window.speechSynthesis.onvoiceschanged=lv;
}
const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
if(SR){
  recog=new SR();recog.lang='hi-IN';recog.interimResults=false;
  recog.onresult=e=>{
    document.getElementById('inp').value=e.results[0][0].transcript;
    stopMic();doSend();
  };
  recog.onerror=recog.onend=stopMic;
}

addMsg('ai','Namaste! Main Mittu hoon 🌸\\n\\nShreedhand ne mujhe aapke liye banaya hai — aapki AI assistant!\\n\\nNet se connected hoon, kuch bhi puchho! 💜');
</script>
</body>
</html>"""


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Koi message nahi mila"})

    api_key = API_KEY
    if not api_key:
        return jsonify({"error": "API Key nahi mili! app.py mein API_KEY variable set karein."})

    try:
        payload = json.dumps({
            "model": "claude-sonnet-4-6",
            "max_tokens": 1000,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": user_message}]
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))

        reply = ""
        for block in result.get("content", []):
            if block.get("type") == "text":
                reply += block["text"]

        if not reply:
            reply = "Kuch samajh nahi aaya, dobara puchho 🌸"

        return jsonify({"reply": reply})

    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            err_msg = json.loads(err_body).get("error", {}).get("message", str(e))
        except Exception:
            err_msg = str(e)
        return jsonify({"error": f"API Error: {err_msg}"})

    except Exception as e:
        return jsonify({"error": f"Error aaya: {str(e)}"})


if __name__ == "__main__":
    print("=" * 50)
    print("  🌸 MITTU AI - by Shreechand")
    print("=" * 50)
    print()
    if not API_KEY:
        print("⚠️  API KEY NAHI MILI!")
        print("   app.py mein line 18 par apni key daalo:")
        print('   API_KEY = "sk-ant-..."')
        print()
        print("   Ya command line se chalao:")
        print('   ANTHROPIC_API_KEY="sk-ant-..." python3 app.py')
        print()
    else:
        print("✅ API Key mili!")
    print("🚀 Server start ho raha hai...")
    print()
    print("📱 Phone/Browser mein kholo:")
    print("   http://localhost:5000")
    print()
    print("   (Agar same WiFi par ho to phone mein:")
    print("    http://<aapka-PC-ka-IP>:5000)")
    print()
    print("   Press Ctrl+C to stop")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=False)
