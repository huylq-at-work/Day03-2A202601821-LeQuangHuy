"""
TEST ROLE 4 — Lê Quang Huy (Core Developer / Integrator)
Kiểm: src/app.py — vòng lặp ReAct chạy đúng chưa, 3 lớp phòng thủ có hoạt động
      không, và app có bị trói vào file của Role 2 không.

Chạy:  .venv\\Scripts\\python.exe tests\\test_role4.py
"""

import io
import os
import sys
from contextlib import redirect_stdout

from _harness import Check, duong_dan

c = Check("ROLE 4 — CORE DEVELOPER / INTEGRATOR (Lê Quang Huy)")

# ---------------------------------------------------------------- nạp module
c.muc("[1] Nạp src/app.py")

app = None
try:
    import app as _a
    app = _a
    c.ok("import được app.py", True)
except Exception as e:
    c.ok("import được app.py", False, f"app.py lỗi: {type(e).__name__}: {e}")

for ten in ("parse_action", "call_tool", "run_react_agent", "run_baseline_chatbot"):
    c.ok(f"Có hàm {ten}()", callable(getattr(app, ten, None)) if app else False,
         f"Thiếu hàm {ten}() trong app.py")

# ---------------------------------------------------------------- độc lập
c.muc("[2] app.py không được trói vào tên tool cụ thể")

src = ""
p = duong_dan("src", "app.py")
if os.path.exists(p):
    with open(p, encoding="utf-8") as f:
        src = f.read()

import re
dong_import = [l for l in src.splitlines() if l.startswith("from tools import")]
xau = [l for l in dong_import if re.search(r"import\s+.*\b(get_|search_|check_)", l)]
c.ok("Chỉ import AVAILABLE_TOOLS, không import tên hàm tool",
     not xau,
     f"Dòng {xau} trói app vào tools.py — Role 2 đổi tên hàm là app crash. "
     "Chỉ nên 'from tools import AVAILABLE_TOOLS'")

# ---------------------------------------------------------------- parse
c.muc("[3] parse_action() — bóc tool từ text LLM")

if app and callable(getattr(app, "parse_action", None)):
    pa = app.parse_action
    CA = [
        ("Thought: abc\nAction: get_learner[0912345203]", "get_learner", ["0912345203"]),
        ("Action: search_courses[AI, 2000000]", "search_courses", ["AI", "2000000"]),
        ("Action: get_learner['0912345203']", "get_learner", ["0912345203"]),
        ("Action:get_learner[ 0912345203 ]", "get_learner", ["0912345203"]),
    ]
    for text, ten, args in CA:
        try:
            got = pa(text)
        except Exception as e:
            c.ok(f"parse {text[:34]!r}", False, f"parse_action crash: {type(e).__name__}")
            continue
        c.ok(f"parse -> {ten}{args}", got == (ten, args),
             f"parse_action trả {got}, mong đợi {(ten, args)}")

    try:
        r = pa("Chào bạn, hôm nay trời đẹp quá!")
        c.ok("Văn xuôi -> trả None (không có Action)", r[0] is None,
             f"parse_action phải trả (None, []) khi không có Action, đang trả {r}")
    except Exception as e:
        c.ok("Văn xuôi -> trả None", False, f"crash: {type(e).__name__}")
else:
    c.ok("parse_action() hoạt động", False, "Chưa có parse_action()")

# ---------------------------------------------------------------- call_tool
c.muc("[4] call_tool() — bọc lỗi thay vì crash")

if app and callable(getattr(app, "call_tool", None)):
    r = c.thu("Tool không tồn tại", lambda: app.call_tool("tool_ma_quy", ["x"]))
    c.ok("Trả 'LỖI:' cho tool không tồn tại",
         isinstance(r, str) and r.strip().upper().startswith("LỖI"),
         "call_tool phải trả chuỗi LỖI, không raise KeyError")

    ten_that = next(iter(app.AVAILABLE_TOOLS), None)
    if ten_that:
        r2 = c.thu("Sai số lượng tham số",
                   lambda: app.call_tool(ten_that, ["a", "b", "c", "d", "e"]))
        c.ok("Trả 'LỖI:' khi sai số tham số",
             isinstance(r2, str) and r2.strip().upper().startswith("LỖI"),
             "call_tool phải bắt TypeError và trả chuỗi LỖI")
else:
    c.ok("call_tool() hoạt động", False, "Chưa có call_tool()")

# ---------------------------------------------------------------- vòng lặp
c.muc("[5] Vòng lặp ReAct — chạy bằng provider giả lập")


class GiaLap:
    """Trả lần lượt các câu đã soạn sẵn, giả làm LLM."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []

    def generate(self, prompt, system_prompt=""):
        self.calls.append(prompt)
        return self.replies.pop(0) if self.replies else "Thought: hết.\nAction: khong_co[x]"


def chay(provider, cau="câu hỏi test"):
    buf = io.StringIO()
    with redirect_stdout(buf):
        app.run_react_agent(cau, provider)
    return buf.getvalue()


if app and callable(getattr(app, "run_react_agent", None)) and app.AVAILABLE_TOOLS:
    t0 = next(iter(app.AVAILABLE_TOOLS))

    p = GiaLap([f"Thought: thử.\nAction: {t0}[x]",
                "Thought: xong.\nFinal Answer: Đây là câu trả lời cuối."])
    out = c.thu("Luồng đủ 2 vòng -> Final Answer", lambda: chay(p))
    c.ok("Dừng ngay khi gặp Final Answer", len(p.calls) == 2,
         f"Gọi LLM {len(p.calls)} lần, mong đợi 2 — phải return ngay khi thấy Final Answer")
    c.ok("Có nối Observation vào history cho vòng sau",
         len(p.calls) >= 2 and "Observation" in p.calls[1],
         "Vòng 2 phải nhận được Observation của vòng 1. Thiếu bước này thì LLM "
         "quên sạch mỗi vòng và gọi mãi 1 tool")

    maxit = getattr(app, "MAX_ITERATIONS", 3)
    p2 = GiaLap([f"Thought: lặp.\nAction: {t0}[x]"] * (maxit + 5))
    out2 = c.thu("LLM lặp vô tận -> Guardrail chặn", lambda: chay(p2))
    c.ok(f"Dừng đúng ở {maxit} vòng", len(p2.calls) == maxit,
         f"Gọi LLM {len(p2.calls)} lần, mong đợi {maxit} (MAX_ITERATIONS)")
    c.ok("In thông báo Guardrail", "UARDRAIL" in (out2 or ""),
         "Khi chạm giới hạn phải in rõ là Guardrail đã ngắt")

    p3 = GiaLap(["Chào bạn, mình nghĩ hôm nay trời đẹp lắm!"])
    out3 = c.thu("LLM trả sai định dạng -> dừng an toàn", lambda: chay(p3))
    c.ok("Không lặp tiếp khi không parse được Action", len(p3.calls) == 1,
         "Không có Action thì phải dừng ngay, đừng lặp tiếp vô ích")

    p4 = GiaLap(["Thought: thử tool tự chế.\nAction: dat_ve_may_bay[x]",
                 "Thought: không có tool đó.\nFinal Answer: Xin lỗi bạn."])
    out4 = c.thu("LLM gọi tool không tồn tại -> báo LỖI rồi đi tiếp", lambda: chay(p4))
    c.ok("Observation chứa LỖI và vòng lặp vẫn tiếp tục",
         "LỖI" in (out4 or "") and len(p4.calls) == 2,
         "Tool ma phải cho Observation LỖI để LLM tự sửa, không được dừng cả vòng lặp")
else:
    c.ok("Vòng lặp ReAct chạy được", False, "Chưa có run_react_agent() hoặc chưa có tool nào")

# ---------------------------------------------- chống LLM bịa Observation
c.muc("[6] Chặn LLM tự bịa Observation")

f = getattr(app, "cut_hallucinated_observation", None) if app else None
if callable(f):
    bia = "Thought: tra cứu.\nAction: get_learner[0912345203]\nObservation: 99 tỷ đồng"
    r = c.thu("Cắt phần Observation do LLM tự bịa", lambda: f(bia))
    c.ok("Đã cắt bỏ Observation giả",
         isinstance(r, str) and "99 tỷ" not in r and "Action:" in r,
         "cut_hallucinated_observation phải cắt từ 'Observation:' trở đi")
else:
    c.ok("Có cut_hallucinated_observation()", False,
         "Thiếu hàm chặn LLM tự bịa Observation")

# ---------------------------------------------------------------- môi trường
c.muc("[7] Môi trường chạy demo")

env = duong_dan(".env")
c.ok("Đã tạo file .env", os.path.exists(env),
     "Chạy 'copy .env.example .env' rồi điền API key")

co_key = False
if os.path.exists(env):
    with open(env, encoding="utf-8") as fh:
        noi = fh.read()
    co_key = any(
        f"{k}=" in noi and not noi.split(f"{k}=")[1].split("\n")[0].strip().startswith(("your_", ""))
        for k in ("GEMINI_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "OPENROUTER_API_KEY")
    )
c.ok("Đã điền API key thật", co_key,
     "Chưa có API key — MockProvider chỉ trả 1 câu cố định nên không demo được Final Answer")

dat, tong = c.ket()
sys.exit(0 if dat == tong else 1)
