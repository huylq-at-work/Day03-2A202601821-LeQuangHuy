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
c.muc("[6B] 🎁 BONUS — Agent Cấp 4: Planning + Memory")

BoNho = getattr(app, "BoNho", None)
c.ok("Có lớp BoNho (Memory)", BoNho is not None, "Thiếu lớp BoNho trong app.py")
c.ok("Có hàm lap_ke_hoach() (Planning)", callable(getattr(app, "lap_ke_hoach", None)),
     "Thiếu hàm lap_ke_hoach() trong app.py")
c.ok("Có run_autonomous_agent()", callable(getattr(app, "run_autonomous_agent", None)),
     "Thiếu hàm demo run_autonomous_agent()")

if BoNho:
    bn = BoNho()
    t0 = next(iter(app.AVAILABLE_TOOLS), "get_learner")

    c.ok("Chưa gọi thì không nhớ gì", bn.nho_lai(t0, ["x"]) is None,
         "BoNho phải trả None khi chưa từng gọi tool đó")

    bn.ghi_nho(t0, ["x"], "ket qua A")
    c.ok("Nhớ lại đúng kết quả đã ghi", bn.nho_lai(t0, ["x"]) == "ket qua A",
         "BoNho không trả lại đúng observation đã nhớ")
    c.ok("Đếm được số lần tiết kiệm gọi tool", bn.so_lan_dung == 1,
         "BoNho phải đếm số lần tái dùng để chứng minh Memory có tác dụng")

    c.ok("Tham số khác thì không nhầm sang cache cũ", bn.nho_lai(t0, ["y"]) is None,
         "Cache phải phân biệt theo tham số, không được trả nhầm kết quả")

    bn.ghi_nho(t0, ["z"], "LỖI: không tìm thấy")
    c.ok("KHÔNG nhớ kết quả lỗi", bn.nho_lai(t0, ["z"]) is None,
         "Không được cache kết quả LỖI — lần sau người dùng có thể nhập đúng")

    # Tool ghi dữ liệu tuyệt đối không được cache
    if "dang_ky_hoc_vien" in app.AVAILABLE_TOOLS:
        bn.ghi_nho("dang_ky_hoc_vien", ["0900000000"], "Đã tạo hồ sơ")
        c.ok("KHÔNG cache tool ghi dữ liệu (dang_ky_hoc_vien)",
             bn.nho_lai("dang_ky_hoc_vien", ["0900000000"]) is None,
             "Cache tool ghi sẽ khiến lần đăng ký thứ hai bị bỏ qua — dữ liệu sai")

    bn.xoa()
    c.ok("Xóa được bộ nhớ", not bn.cache and bn.so_lan_dung == 0,
         "BoNho.xoa() phải dọn sạch cache và bộ đếm")

# Memory phải thực sự cắt được lời gọi tool trong vòng lặp
if BoNho and app and callable(getattr(app, "run_react_agent", None)) and app.AVAILABLE_TOOLS:
    # Phải dùng tham số cho ra kết quả THÀNH CÔNG — kết quả LỖI cố tình không được cache
    t0, tham_so = ("get_learner", "0912345203") if "get_learner" in app.AVAILABLE_TOOLS \
        else (next(iter(app.AVAILABLE_TOOLS)), "x")
    bn = BoNho()

    def chay_lai():
        p = GiaLap([f"Thought: tra.\nAction: {t0}[{tham_so}]",
                    "Thought: xong.\nFinal Answer: ok."])
        buf = io.StringIO()
        with redirect_stdout(buf):
            return app.react_steps("test", p, None, bn, None)

    b1 = chay_lai()
    b2 = chay_lai()
    tu_nho = [b for b in b2 if b.get("tu_bo_nho")]
    c.ok("Lượt sau lấy observation từ bộ nhớ, không gọi lại tool",
         len(tu_nho) >= 1,
         "react_steps(bo_nho=...) phải đánh dấu tu_bo_nho=True khi tái dùng kết quả")
    c.ok("Observation lấy từ bộ nhớ giống hệt lần gọi thật",
         bool(tu_nho) and tu_nho[0]["observation"] == b1[0]["observation"],
         "Kết quả từ bộ nhớ phải khớp với kết quả gọi tool thật")

c.muc("[7] Môi trường chạy demo")

env = duong_dan(".env")
c.ok("Đã tạo file .env", os.path.exists(env),
     "Chạy 'copy .env.example .env' rồi điền API key")

co_key = False
if os.path.exists(env):
    with open(env, encoding="utf-8") as fh:
        noi = fh.read()
    for k in ("GEMINI_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "OPENROUTER_API_KEY"):
        m = re.search(rf"^{k}=(.*)$", noi, re.M)
        gia_tri = m.group(1).strip() if m else ""
        if gia_tri and not gia_tri.startswith("your_"):
            co_key = True
            break
c.ok("Đã điền API key thật", co_key,
     "Chưa có API key — MockProvider chỉ trả 1 câu cố định nên không demo được Final Answer")

dat, tong = c.ket()
sys.exit(0 if dat == tong else 1)
