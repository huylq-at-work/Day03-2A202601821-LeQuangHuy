"""
GIAO DIỆN CHAT — Trợ Lý Đăng Ký Khóa Học

Khung chat nhiều lượt. Phần suy luận và gọi công cụ được thu gọn,
bấm vào mới mở ra xem — giống cách ChatGPT hiện phần thinking.

Dùng http.server có sẵn trong Python, không cần cài thêm thư viện nào.

Chạy:  .venv\\Scripts\\python.exe src\\web_ui.py
Mở:    http://localhost:8765
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from tools import AVAILABLE_TOOLS
from prompts import CHATBOT_BASELINE_PROMPT, MAX_ITERATIONS
from providers import get_llm_provider
from app import react_steps, load_test_cases, BoNho, lap_ke_hoach

PORT = 8765
provider = get_llm_provider()

# Bộ nhớ cho chế độ Autonomous (Cấp 4), dùng chung cả phiên, xóa khi bấm "Xóa hội thoại"
bo_nho = BoNho()

PAGE = r"""<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trợ Lý Đăng Ký Khóa Học</title>
<style>
:root{--bg:#ffffff;--bg2:#f7f7f4;--line:#e7e4de;--tx:#1a1917;--mu:#767168;
      --ac:#5b4ac4;--ok:#0f6e56;--er:#a32d2d;--wa:#8a5209;--tl:#185fa5;--bub:#f1efeb;
      --sh:0 1px 2px rgba(0,0,0,.05)}
:root[data-theme="dark"]{--bg:#1b1a18;--bg2:#232120;--line:#38352f;
      --tx:#ece9e4;--mu:#a09b93;--ac:#a79ae8;--ok:#5dcaa5;--er:#f09595;--wa:#efa532;
      --tl:#85b7eb;--bub:#2c2a27;--sh:0 1px 2px rgba(0,0,0,.3)}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--tx);
     font:15.5px/1.65 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
     display:flex;flex-direction:column}

header{border-bottom:1px solid var(--line);padding:11px 18px;display:flex;
       align-items:center;gap:14px;flex-wrap:wrap;background:var(--bg);position:sticky;top:0;z-index:5}
.brand{font-weight:600;font-size:15px}
.seg{display:flex;border:1px solid var(--line);border-radius:99px;padding:2px;background:var(--bg2)}
.seg button{border:0;background:none;color:var(--mu);font:inherit;font-size:13px;
            padding:5px 14px;border-radius:99px;cursor:pointer}
.seg button.on{background:var(--bg);color:var(--tx);font-weight:500;box-shadow:var(--sh)}
.spacer{flex:1}
.badge{font-size:12px;color:var(--mu);border:1px solid var(--line);border-radius:99px;padding:3px 10px}
.badge.warn{color:var(--wa);border-color:var(--wa)}
.icobtn{border:1px solid var(--line);background:var(--bg);border-radius:99px;width:30px;height:30px;
        font-size:14px;cursor:pointer;color:var(--mu);line-height:1;padding:0}
.icobtn:hover{color:var(--tx);border-color:var(--mu)}

main{flex:1;overflow-y:auto}
.thread{max-width:760px;margin:0 auto;padding:26px 18px 10px}

.empty{text-align:center;padding:52px 0 10px;color:var(--mu)}
.empty h2{color:var(--tx);font-size:21px;font-weight:600;margin:0 0 6px}
.empty p{margin:0 0 26px;font-size:14px}
.sugg{display:grid;grid-template-columns:1fr 1fr;gap:9px;text-align:left}
@media(max-width:640px){.sugg{grid-template-columns:1fr}}
.sugg button{border:1px solid var(--line);background:var(--bg);color:var(--tx);
   border-radius:11px;padding:12px 14px;font:inherit;font-size:13.5px;cursor:pointer;line-height:1.45}
.sugg button:hover{border-color:var(--ac);background:var(--bg2)}

.msg{margin-bottom:24px;display:flex;flex-direction:column}
.msg.u{align-items:flex-end}
.bub{background:var(--bub);padding:10px 15px;border-radius:17px;max-width:86%;white-space:pre-wrap}
.who{font-size:11.5px;color:var(--mu);margin-bottom:5px;letter-spacing:.02em}
.ans{white-space:pre-wrap}

details.trace{margin:0 0 11px;border:1px solid var(--line);border-radius:11px;
              background:var(--bg2);overflow:hidden}
details.trace>summary{cursor:pointer;list-style:none;padding:9px 13px;font-size:13px;
              color:var(--mu);display:flex;align-items:center;gap:8px;user-select:none}
details.trace>summary::-webkit-details-marker{display:none}
details.trace>summary:hover{color:var(--tx)}
.chev{transition:transform .15s;display:inline-block;font-size:10px;opacity:.7}
details.trace[open]>summary .chev{transform:rotate(90deg)}
.tbody{padding:4px 13px 13px;border-top:1px solid var(--line)}

.step{border-left:2px solid var(--line);padding:11px 0 3px 13px;margin-left:3px}
.vg{font-size:10.5px;color:var(--mu);letter-spacing:.05em;text-transform:uppercase;margin-bottom:5px}
.row{display:flex;gap:8px;margin-bottom:6px;font-size:13.5px;align-items:flex-start}
.ico{flex:0 0 16px;text-align:center;opacity:.8;line-height:1.5}
.th{color:var(--mu);font-style:italic}
.act{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;color:var(--tl);
     background:color-mix(in srgb,var(--tl) 10%,transparent);padding:4px 8px;border-radius:6px;
     word-break:break-all}
.obs{color:var(--tx)}
.obs.bad{color:var(--er)}
.note{border-left:2px solid var(--wa);background:color-mix(in srgb,var(--wa) 12%,transparent);
      padding:9px 12px;border-radius:0 8px 8px 0;font-size:13.5px;margin:8px 0 2px}

.dots span{display:inline-block;width:6px;height:6px;margin-right:4px;border-radius:50%;
   background:var(--mu);animation:bl 1.3s infinite}
.dots span:nth-child(2){animation-delay:.18s}.dots span:nth-child(3){animation-delay:.36s}
@keyframes bl{0%,60%,100%{opacity:.25}30%{opacity:1}}

footer{border-top:1px solid var(--line);background:var(--bg);padding:13px 18px 18px}
.composer{max-width:760px;margin:0 auto;display:flex;gap:9px;align-items:flex-end;
   border:1px solid var(--line);border-radius:15px;padding:7px 7px 7px 15px;background:var(--bg2)}
.composer textarea{flex:1;border:0;background:none;color:var(--tx);font:inherit;resize:none;
   outline:none;max-height:150px;padding:7px 0;line-height:1.5}
.send{border:0;border-radius:11px;background:var(--ac);color:#fff;width:35px;height:35px;
   font-size:16px;cursor:pointer;flex:0 0 auto}
.send:disabled{opacity:.35;cursor:default}
.hint{max-width:760px;margin:8px auto 0;font-size:11.5px;color:var(--mu);text-align:center}
</style>

<header>
  <span class="brand">Trợ Lý Đăng Ký Khóa Học</span>
  <div class="seg">
    <button id="m-agent" class="on">ReAct Agent</button>
    <button id="m-bot">Chatbot thường</button>
    <button id="m-auto" title="Cấp 4: tự lập kế hoạch + nhớ dữ kiện đã tra">Autonomous</button>
  </div>
  <span class="spacer"></span>
  <span class="badge" id="bd-prov"></span>
  <button class="badge" id="clear" style="cursor:pointer;background:none;font:inherit">Xóa hội thoại</button>
  <button class="icobtn" id="theme" title="Đổi giao diện sáng/tối">🌙</button>
</header>
<script>
(function(){
  const t = localStorage.getItem("theme") || "light";
  document.documentElement.setAttribute("data-theme", t);
})();
</script>

<main><div class="thread" id="thread"></div></main>

<footer>
  <div class="composer">
    <textarea id="q" rows="1" placeholder="Nhắn gì đó cho trợ lý…"></textarea>
    <button class="send" id="go">↑</button>
  </div>
  <div class="hint" id="hint"></div>
</footer>

<script>
const esc = s => (s||"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
let msgs = [], mode = "agent", info = {}, busy = false;

const $ = id => document.getElementById(id);
const thread = $("thread");

fetch("/api/info").then(r=>r.json()).then(d=>{
  info = d;
  $("bd-prov").textContent = d.provider;
  if(d.mock){ $("bd-prov").className = "badge warn"; $("bd-prov").title =
    "Máy trạng thái mô phỏng, không phải LLM thật. Điền API key vào .env để dùng LLM thật."; }
  $("hint").textContent = d.mock
    ? "Đang chạy MockProvider — suy luận được lập trình sẵn, không phải LLM thật."
    : `${d.tools.length} công cụ · tối đa ${d.max_iterations} vòng lặp`;
  render();
});

function veTrace(steps, ke_hoach){
  const nTool = steps.filter(b=>b.loai==="tool").length;
  const nNho = steps.filter(b=>b.tu_bo_nho).length;
  const coLoi = steps.some(b=>b.loi);
  const guard = steps.some(b=>b.loai==="guardrail");
  let nhan = `Đã suy nghĩ ${steps.length} bước`;
  if(ke_hoach && ke_hoach.length) nhan += ` · lập ${ke_hoach.length} bước kế hoạch`;
  if(nTool) nhan += ` · gọi ${nTool} công cụ`;
  if(nNho) nhan += ` · ${nNho} lần dùng bộ nhớ`;
  if(coLoi) nhan += " · có lỗi tra cứu";
  if(guard) nhan += " · chạm Guardrail";

  const kh = (ke_hoach && ke_hoach.length)
    ? `<div class="step"><div class="vg">📋 Kế hoạch tự vạch</div>` +
      ke_hoach.map((b,i)=>`<div class="row"><span class="ico">${i+1}</span><span class="th">${esc(b)}</span></div>`).join("") +
      `</div>` : "";

  const body = kh + steps.map(b=>{
    if(b.loai==="guardrail")
      return `<div class="note"><b>Guardrail ngắt vòng lặp</b><br>Đã chạm giới hạn ${b.vong} vòng mà chưa ra kết quả.</div>`;
    let h = `<div class="step"><div class="vg">Vòng ${b.vong}</div>`;
    if(b.thought) h += `<div class="row"><span class="ico">💭</span><span class="th">${esc(b.thought)}</span></div>`;
    if(b.loai==="tool"){
      h += `<div class="row"><span class="ico">🛠</span><span class="act">${esc(b.tool)}[${esc((b.args||[]).join(", "))}]</span></div>`;
      const nho = b.tu_bo_nho ? ` <b>🧠 lấy từ bộ nhớ, không gọi tool</b>` : "";
    h += `<div class="row"><span class="ico">👁</span><span class="obs ${b.loi?"bad":""}">${esc(b.observation)}${nho}</span></div>`;
    }
    if(b.loai==="sai_dinh_dang")
      h += `<div class="note"><b>LLM trả sai định dạng</b><br>Không bóc được Action nên dừng an toàn.</div>`;
    if(b.loai==="final") h += `<div class="row"><span class="ico">🏁</span><span class="th">Chốt câu trả lời</span></div>`;
    return h+`</div>`;
  }).join("");

  return `<details class="trace"><summary><span class="chev">▶</span>${nhan}</summary>
          <div class="tbody">${body}</div></details>`;
}

function render(){
  if(!msgs.length){
    const s = (info.samples||[]).slice(0,4).map(q=>
      `<button onclick="hoi(${JSON.stringify(q).replace(/"/g,'&quot;')})">${esc(q)}</button>`).join("");
    thread.innerHTML = `<div class="empty"><h2>Mình giúp gì cho bạn?</h2>
      <p>Tra hồ sơ học viên, tìm khóa theo ngân sách, kiểm tra điều kiện đăng ký.</p>
      <div class="sugg">${s}</div></div>`;
    return;
  }
  thread.innerHTML = msgs.map(m=>{
    if(m.role==="user") return `<div class="msg u"><div class="bub">${esc(m.content)}</div></div>`;
    if(m.dang) return `<div class="msg"><div class="who">${m.nhan}</div>
      <div class="dots"><span></span><span></span><span></span></div></div>`;
    return `<div class="msg"><div class="who">${m.nhan}</div>
      ${m.steps && m.steps.length ? veTrace(m.steps, m.ke_hoach) : ""}
      <div class="ans">${esc(m.content)}</div></div>`;
  }).join("");
  thread.parentElement.scrollTop = thread.parentElement.scrollHeight;
}

async function hoi(q){
  if(busy || !q.trim()) return;
  busy = true; $("go").disabled = true;
  const nhan = mode==="agent" ? "ReAct Agent" : mode==="auto" ? "Autonomous Agent (Cấp 4)" : "Chatbot thường";
  msgs.push({role:"user", content:q});
  msgs.push({role:"bot", dang:true, nhan});
  render();

  const lich_su = [];
  for(let i=0;i<msgs.length-2;i++)
    if(msgs[i].role==="user" && msgs[i+1] && msgs[i+1].role==="bot" && !msgs[i+1].dang)
      lich_su.push([msgs[i].content, msgs[i+1].content]);

  try{
    const r = await fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},
              body:JSON.stringify({question:q, mode, lich_su})});
    const d = await r.json();
    msgs[msgs.length-1] = {role:"bot", nhan, content:d.answer, steps:d.steps||[], ke_hoach:d.ke_hoach||[]};
  }catch(e){
    msgs[msgs.length-1] = {role:"bot", nhan, content:"Lỗi kết nối: "+e, steps:[]};
  }
  busy = false; $("go").disabled = false;
  render();
}

const ta = $("q");
ta.addEventListener("input", ()=>{ ta.style.height="auto"; ta.style.height=ta.scrollHeight+"px"; });
ta.addEventListener("keydown", e=>{
  if(e.key==="Enter" && !e.shiftKey){ e.preventDefault(); const v=ta.value; ta.value=""; ta.style.height="auto"; hoi(v); }
});
$("go").onclick = ()=>{ const v=ta.value; ta.value=""; ta.style.height="auto"; hoi(v); };
$("clear").onclick = ()=>{ msgs=[]; render(); fetch("/api/reset",{method:"POST"}); };

function apDungTheme(t){
  document.documentElement.setAttribute("data-theme", t);
  localStorage.setItem("theme", t);
  $("theme").textContent = t === "dark" ? "☀️" : "🌙";
}
apDungTheme(localStorage.getItem("theme") || "light");
$("theme").onclick = ()=>
  apDungTheme(document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark");
function chonCheDo(m){ mode=m;
  ["agent","bot","auto"].forEach(x=>$("m-"+x).className = (x===m ? "on" : "")); }
$("m-agent").onclick = ()=>chonCheDo("agent");
$("m-bot").onclick   = ()=>chonCheDo("bot");
$("m-auto").onclick  = ()=>chonCheDo("auto");
</script>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith("/api/info"):
            try:
                mau = [t["question"] for t in load_test_cases()]
            except Exception:
                mau = []
            self._send(200, json.dumps({
                "provider": provider.__class__.__name__,
                "mock": provider.__class__.__name__ == "MockProvider",
                "max_iterations": MAX_ITERATIONS,
                "tools": list(AVAILABLE_TOOLS),
                "samples": mau,
            }, ensure_ascii=False), "application/json")
        else:
            self._send(200, PAGE, "text/html")

    def do_POST(self):
        # Xóa bộ nhớ Cấp 4 — gửi không kèm body nên phải xử lý trước khi parse JSON
        if self.path.startswith("/api/reset"):
            bo_nho.xoa()
            return self._send(200, '{"ok":true}', "application/json")

        n = int(self.headers.get("Content-Length", 0))
        try:
            d = json.loads(self.rfile.read(n))
            cau_hoi = d["question"]
        except Exception:
            return self._send(400, '{"error":"thiếu question"}', "application/json")

        che_do = d.get("mode", "agent")
        lich_su = [tuple(x) for x in d.get("lich_su", [])]

        # Chatbot thường: hỏi thẳng LLM, không có công cụ nào
        if che_do == "bot":
            try:
                tra_loi = provider.generate(cau_hoi, system_prompt=CHATBOT_BASELINE_PROMPT)
            except Exception as e:
                tra_loi = f"[Lỗi gọi LLM]: {e}"
            return self._send(200, json.dumps({"answer": tra_loi, "steps": []},
                                              ensure_ascii=False), "application/json")

        # ReAct Agent (Cấp 3) hoặc Autonomous (Cấp 4: Planning + Memory)
        ke_hoach = []
        try:
            if che_do == "auto":
                ke_hoach = lap_ke_hoach(cau_hoi, provider, lich_su)
                buoc = react_steps(cau_hoi, provider, lich_su, bo_nho, ke_hoach)
            else:
                buoc = react_steps(cau_hoi, provider, lich_su)
            cuoi = buoc[-1] if buoc else {}
            tra_loi = cuoi.get("final") or "Mình chưa đưa ra được câu trả lời."
        except Exception as e:
            buoc, tra_loi = [], f"Lỗi khi chạy vòng lặp: {e}"

        self._send(200, json.dumps({"answer": tra_loi, "steps": buoc, "ke_hoach": ke_hoach},
                                   ensure_ascii=False), "application/json")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    ten = provider.__class__.__name__
    print("=" * 58)
    print("  TRỢ LÝ ĐĂNG KÝ KHÓA HỌC — GIAO DIỆN CHAT")
    print("=" * 58)
    print(f"  LLM Provider : {ten}")
    print(f"  Tools        : {', '.join(AVAILABLE_TOOLS)}")
    print(f"  Max vòng lặp : {MAX_ITERATIONS}")
    if ten == "MockProvider":
        print("\n  [!] MockProvider là máy trạng thái mô phỏng, KHÔNG phải LLM thật.")
        print("      Điền API key vào .env để chạy bằng LLM thật.")
    print(f"\n  Mở trình duyệt: http://localhost:{PORT}")
    print("  Dừng: Ctrl+C")
    print("=" * 58)
    try:
        HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng.")
