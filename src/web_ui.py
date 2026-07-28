"""
GIAO DIỆN WEB — so sánh trực quan Chatbot vs ReAct Agent.

Hiện rõ từng bước Thought -> Action -> Observation để trình chiếu ở Mốc 4.
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
from app import react_steps, load_test_cases

PORT = 8765
provider = get_llm_provider()

PAGE = r"""<!doctype html>
<meta charset="utf-8">
<title>Trợ Lý Đăng Ký Khóa Học — Chatbot vs ReAct Agent</title>
<style>
:root{--bg:#faf9f7;--card:#fff;--line:#e4e1db;--tx:#1f1e1c;--mu:#6b6862;
      --ac:#5b4ac4;--ok:#0f6e56;--er:#a32d2d;--wa:#854f0b;--tool:#185fa5}
@media(prefers-color-scheme:dark){:root{--bg:#1a1917;--card:#242220;--line:#3a3733;
      --tx:#eceae6;--mu:#a8a49c;--ac:#a79ae8;--ok:#5dcaa5;--er:#f09595;--wa:#ef9f27;--tool:#85b7eb}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:24px 20px 60px}
h1{font-size:20px;font-weight:600;margin:0 0 4px}
.sub{color:var(--mu);font-size:13px;margin-bottom:20px}
.bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
input[type=text]{flex:1;min-width:280px;padding:11px 14px;border:1px solid var(--line);
  border-radius:8px;background:var(--card);color:var(--tx);font-size:15px}
button{padding:11px 20px;border:0;border-radius:8px;background:var(--ac);color:#fff;
  font-size:15px;font-weight:500;cursor:pointer}
button:disabled{opacity:.5;cursor:default}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:22px}
.chip{padding:5px 11px;border:1px solid var(--line);border-radius:99px;background:var(--card);
  font-size:12.5px;color:var(--mu);cursor:pointer}
.chip:hover{border-color:var(--ac);color:var(--ac)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:860px){.cols{grid-template-columns:1fr}}
.col{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
.col h2{font-size:14px;font-weight:600;margin:0 0 2px}
.col .lbl{font-size:12px;color:var(--mu);margin-bottom:14px}
.step{border-left:2px solid var(--line);padding:0 0 14px 14px;margin-left:4px;position:relative}
.step:last-child{padding-bottom:0}
.vong{font-size:11px;color:var(--mu);letter-spacing:.04em;text-transform:uppercase;margin-bottom:6px}
.row{display:flex;gap:7px;margin-bottom:7px;font-size:14px}
.ico{flex:0 0 17px;text-align:center;opacity:.85}
.think{color:var(--mu);font-style:italic}
.act{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;color:var(--tool);
  background:color-mix(in srgb,var(--tool) 9%,transparent);padding:5px 9px;border-radius:6px;
  word-break:break-all}
.obs{font-size:13.5px}
.obs.bad{color:var(--er)}
.final{background:color-mix(in srgb,var(--ok) 11%,transparent);border-left:2px solid var(--ok);
  padding:11px 13px;border-radius:0 8px 8px 0;margin-top:4px}
.guard{background:color-mix(in srgb,var(--wa) 13%,transparent);border-left:2px solid var(--wa);
  padding:11px 13px;border-radius:0 8px 8px 0}
.muted{color:var(--mu);font-size:13px}
.pill{display:inline-block;font-size:11px;padding:2px 8px;border-radius:99px;
  background:color-mix(in srgb,var(--mu) 15%,transparent);color:var(--mu);margin-left:6px}
.warn{background:color-mix(in srgb,var(--wa) 13%,transparent);border:1px solid var(--wa);
  border-radius:8px;padding:9px 13px;font-size:13px;margin-bottom:16px}
</style>
<div class="wrap">
  <h1>Trợ Lý Đăng Ký Khóa Học</h1>
  <div class="sub">Bài Lab 3 — so sánh Chatbot thường và ReAct Agent trên cùng một câu hỏi</div>
  <div id="warn"></div>
  <div class="bar">
    <input type="text" id="q" placeholder="Ví dụ: Em là 0912345203, em muốn học AI thì nên đăng ký khóa nào?">
    <button id="go">Chạy thử</button>
  </div>
  <div class="chips" id="chips"></div>
  <div class="cols">
    <div class="col">
      <h2>Chatbot thường <span class="pill">Cấp 2</span></h2>
      <div class="lbl">Chỉ dùng LLM, không có công cụ</div>
      <div id="bot" class="muted">Chưa chạy.</div>
    </div>
    <div class="col">
      <h2>ReAct Agent <span class="pill">Cấp 3</span></h2>
      <div class="lbl" id="albl">Thought → Action → Observation</div>
      <div id="agent" class="muted">Chưa chạy.</div>
    </div>
  </div>
</div>
<script>
const esc = s => (s||"").replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));

fetch("/api/info").then(r=>r.json()).then(d=>{
  document.getElementById("albl").textContent =
    "Thought → Action → Observation · tối đa " + d.max_iterations + " vòng · " + d.tools.length + " tool";
  document.getElementById("chips").innerHTML =
    d.samples.map(s=>`<span class="chip" data-q="${esc(s)}">${esc(s.slice(0,64))}${s.length>64?"…":""}</span>`).join("");
  document.querySelectorAll(".chip").forEach(c=>c.onclick=()=>{
    document.getElementById("q").value=c.dataset.q; run();});
  if(d.mock) document.getElementById("warn").innerHTML =
    '<div class="warn">Đang chạy <b>MockProvider</b> — máy trạng thái mô phỏng, <b>không phải LLM thật</b>. '+
    'Tool và dữ liệu là thật, nhưng phần suy luận được lập trình sẵn. '+
    'Điền API key vào <code>.env</code> để chạy bằng LLM thật trước khi nộp bài.</div>';
});

function veBuoc(b){
  if(b.loai==="guardrail")
    return `<div class="guard"><b>Guardrail ngắt</b><br>Đã chạm giới hạn ${b.vong} vòng.<br><br>${esc(b.final)}</div>`;
  let h = `<div class="step"><div class="vong">Vòng ${b.vong}</div>`;
  if(b.thought) h += `<div class="row"><span class="ico">💭</span><span class="think">${esc(b.thought)}</span></div>`;
  if(b.loai==="tool"){
    h += `<div class="row"><span class="ico">🛠</span><span class="act">${esc(b.tool)}[${esc((b.args||[]).join(", "))}]</span></div>`;
    h += `<div class="row"><span class="ico">👁</span><span class="obs ${b.loi?"bad":""}">${esc(b.observation)}</span></div>`;
  }
  if(b.loai==="final") h += `<div class="final">${esc(b.final)}</div>`;
  if(b.loai==="sai_dinh_dang")
    h += `<div class="guard"><b>LLM trả sai định dạng</b><br>Không bóc được Action nên dừng an toàn.<br><br>${esc(b.final)}</div>`;
  return h+`</div>`;
}

async function run(){
  const q = document.getElementById("q").value.trim();
  if(!q) return;
  const btn = document.getElementById("go");
  btn.disabled = true; btn.textContent = "Đang chạy…";
  document.getElementById("bot").className="muted";
  document.getElementById("bot").textContent="Đang hỏi LLM…";
  document.getElementById("agent").className="muted";
  document.getElementById("agent").textContent="Đang chạy vòng lặp…";
  try{
    const r = await fetch("/api/ask",{method:"POST",headers:{"Content-Type":"application/json"},
                                     body:JSON.stringify({question:q})});
    const d = await r.json();
    document.getElementById("bot").className="";
    document.getElementById("bot").textContent = d.chatbot;
    document.getElementById("agent").className="";
    document.getElementById("agent").innerHTML = d.steps.map(veBuoc).join("");
  }catch(e){
    document.getElementById("agent").textContent = "Lỗi: " + e;
  }
  btn.disabled = false; btn.textContent = "Chạy thử";
}
document.getElementById("go").onclick = run;
document.getElementById("q").addEventListener("keydown", e=>{if(e.key==="Enter") run();});
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
        n = int(self.headers.get("Content-Length", 0))
        try:
            cau_hoi = json.loads(self.rfile.read(n))["question"]
        except Exception:
            return self._send(400, '{"error":"thiếu question"}', "application/json")

        try:
            tra_loi = provider.generate(cau_hoi, system_prompt=CHATBOT_BASELINE_PROMPT)
        except Exception as e:
            tra_loi = f"[Lỗi gọi LLM]: {e}"

        try:
            buoc = react_steps(cau_hoi, provider)
        except Exception as e:
            buoc = [{"vong": 0, "loai": "sai_dinh_dang", "thought": "",
                     "final": f"Lỗi khi chạy vòng lặp: {e}"}]

        self._send(200, json.dumps({"chatbot": tra_loi, "steps": buoc},
                                   ensure_ascii=False), "application/json")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    ten = provider.__class__.__name__
    print("=" * 58)
    print("  GIAO DIỆN WEB — CHATBOT VS REACT AGENT")
    print("=" * 58)
    print(f"  LLM Provider : {ten}")
    print(f"  Tools        : {', '.join(AVAILABLE_TOOLS)}")
    print(f"  Max vòng lặp : {MAX_ITERATIONS}")
    if ten == "MockProvider":
        print("\n  [!] Chưa có API key — Agent sẽ lặp tới khi Guardrail ngắt.")
        print("      Điền key vào .env để thấy đủ luồng tới Final Answer.")
    print(f"\n  Mở trình duyệt: http://localhost:{PORT}")
    print("  Dừng: Ctrl+C")
    print("=" * 58)
    try:
        HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng.")
