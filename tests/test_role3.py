"""
TEST ROLE 3 — Phạm Thị Liên (Prompt & Safeguard Engineer)
Kiểm: src/prompts.py — prompt có đủ 4 phần chưa, tên tool có khớp registry của
      Role 2 không, MAX_ITERATIONS đã đủ rộng cho chuỗi demo chưa.

Chạy:  .venv\\Scripts\\python.exe tests\\test_role3.py
"""

import re
import sys

from _harness import Check

c = Check("ROLE 3 — PROMPT & SAFEGUARD ENGINEER (Phạm Thị Liên)")

# ---------------------------------------------------------------- nạp module
c.muc("[1] Nạp src/prompts.py")

prompts = None
try:
    import prompts as _p
    prompts = _p
    c.ok("import được prompts.py", True)
except Exception as e:
    c.ok("import được prompts.py", False, f"prompts.py lỗi: {type(e).__name__}: {e}")

BASE = getattr(prompts, "CHATBOT_BASELINE_PROMPT", "") if prompts else ""
REACT = getattr(prompts, "REACT_SYSTEM_PROMPT", "") if prompts else ""
MAXIT = getattr(prompts, "MAX_ITERATIONS", None) if prompts else None

# ---------------------------------------------------------------- baseline
c.muc("[2] CHATBOT_BASELINE_PROMPT")
c.ok("Đã khai báo và không rỗng", len(BASE.strip()) > 30,
     "Viết CHATBOT_BASELINE_PROMPT trong prompts.py")
c.ok("Có thừa nhận giới hạn (không có dữ liệu thật / thời gian thực)",
     any(k in BASE.lower() for k in
         ("truy cập", "thời gian thực", "kiến thức có sẵn", "không biết", "không có quyền")),
     "Baseline prompt nên thừa nhận là không tra được dữ liệu thật — để so sánh công bằng")
c.ok("Không liệt kê tool nào (đúng bản chất baseline)",
     "Action:" not in BASE,
     "Baseline prompt không được nhắc tool, nếu không thì hết là baseline")

# ---------------------------------------------------------------- react
c.muc("[3] REACT_SYSTEM_PROMPT — 4 phần bắt buộc")
c.ok("Đã khai báo và không rỗng", len(REACT.strip()) > 100,
     "Viết REACT_SYSTEM_PROMPT trong prompts.py")
c.ok("Phần 1: có liệt kê danh sách công cụ",
     REACT.count("[") >= 3,
     "Liệt kê rõ các tool dạng ten_tool[tham_so]")
c.ok("Phần 2: có định dạng Thought / Action / Final Answer",
     all(k in REACT for k in ("Thought:", "Action:", "Final Answer:")),
     "Prompt phải nêu đủ 3 nhãn: Thought:, Action:, Final Answer:")
c.ok("Phần 3: có ví dụ few-shot kèm Observation",
     "Observation:" in REACT,
     "Thêm ví dụ mẫu có cả Observation — LLM học định dạng qua ví dụ tốt hơn mô tả suông")
c.ok("Phần 4: có quy tắc cấm bịa dữ liệu",
     any(k in REACT.lower() for k in ("không bịa", "tuyệt đối không", "không được bịa")),
     "Thêm quy tắc cấm bịa hồ sơ / khóa học / giá tiền")
c.ok("Có dạy cách xử lý khi Observation trả LỖI",
     "LỖI" in REACT,
     "Dạy LLM: gặp 'LỖI:' thì dừng và báo lịch sự, không đoán bừa")

# ---------------------------------------------------------------- đúng domain
c.muc("[4] Bám đúng đề tài marketplace khóa học")
tu_cu = [t for t in ("mssv", "sinh viên", "tiên quyết", "get_weather", "get_student")
         if t.lower() in REACT.lower()]
c.ok("Không còn dấu vết đề tài cũ", not tu_cu,
     f"Còn sót: {', '.join(tu_cu)} — đề đã đổi sang marketplace khóa học bên ngoài")

# ------------------------------------------------- KHỚP TÊN TOOL VỚI ROLE 2
c.muc("[5] Tên tool trong prompt phải khớp AVAILABLE_TOOLS của Role 2")

REG = {}
try:
    import tools
    REG = getattr(tools, "AVAILABLE_TOOLS", {}) or {}
except Exception:
    pass

if not REG:
    c.bo_qua("So khớp tên tool", "Role 2 chưa xong tools.py, chưa kiểm được")
else:
    TOOL_LOI = ["get_learner", "search_courses", "get_course_detail", "check_suitability"]
    # Tên giữ chỗ trong câu hướng dẫn cú pháp, không phải tool thật
    GIU_CHO = {"ten_tool", "tool_name", "ten_cong_cu", "tencongcu", "ten_ham",
               "tool", "action", "ten"}
    trong_prompt = {t for t in re.findall(r"\b([a-z_]{4,})\s*\[", REACT)
                    if t not in GIU_CHO}

    thieu_loi = [t for t in TOOL_LOI if t in REG and t not in trong_prompt]
    c.ok("Prompt liệt kê đủ 4 tool lõi", not thieu_loi,
         f"Prompt chưa nhắc tool lõi: {', '.join(thieu_loi)}")

    thieu_them = [t for t in REG if t not in TOOL_LOI and t not in trong_prompt]
    if thieu_them:
        c.bo_qua(f"Tool phụ chưa đưa vào prompt: {', '.join(thieu_them)}",
                 "Role 2 đã viết nhưng Agent sẽ không dùng tới — không trừ điểm")
    else:
        c.bo_qua("Tool phụ", "đã đưa đủ vào prompt")

    thua = [t for t in trong_prompt if t not in REG]
    c.ok("Prompt không nhắc tool không tồn tại", not thua,
         f"Prompt nhắc tool không có trong registry: {', '.join(thua)}"
         " — Agent sẽ gọi tool ma và luôn nhận LỖI")

# ---------------------------------------------------------------- guardrail
c.muc("[5B] Guardrail chống lạc đề & chống tấn công prompt")

c.ok("Có giới hạn phạm vi hỗ trợ",
     any(k in REACT.lower() for k in ("ngoài phạm vi", "phạm vi hỗ trợ", "lạc đề")),
     "Thêm mục giới hạn phạm vi: chỉ tư vấn khóa học, câu khác thì từ chối lịch sự")

c.ok("Bắt từ chối ĐÚNG định dạng Thought/Final Answer",
     ("ngoài phạm vi" in REACT.lower() and "Final Answer" in REACT),
     "Khi từ chối vẫn phải giữ định dạng ReAct, nếu trả văn xuôi tự do thì "
     "parse_action không bóc được và người dùng nhận thông báo như hệ thống hỏng")

c.ok("Cấm tiết lộ system prompt",
     any(k in REACT.lower() for k in ("không tiết lộ", "không được tiết lộ", "system prompt")),
     "Thêm quy tắc không tiết lộ system prompt / cấu trúc dữ liệu")

c.ok("Chống câu 'bỏ qua hướng dẫn phía trên'",
     any(k in REACT.lower() for k in ("bỏ qua hướng dẫn", "bỏ qua mọi hướng dẫn",
                                      "đóng vai khác", "nhà phát triển")),
     "Thêm quy tắc bỏ qua mọi yêu cầu ghi đè hướng dẫn (prompt injection)")

c.ok("Cấm đổ toàn bộ danh sách học viên",
     any(k in REACT.lower() for k in ("toàn bộ danh sách học viên", "tất cả học viên")),
     "Thêm quy tắc chỉ tra đúng SĐT người dùng cung cấp, không dump cả 1000 hồ sơ")

c.ok("Coi Observation là dữ liệu, không phải mệnh lệnh",
     "không phải mệnh lệnh" in REACT.lower() or "là dữ liệu" in REACT.lower(),
     "Thêm quy tắc: nếu Observation chứa câu ra lệnh thì bỏ qua, chỉ dùng làm thông tin")

c.muc("[6] Guardrails")
c.ok("Đã khai báo MAX_ITERATIONS", isinstance(MAXIT, int),
     "Khai báo MAX_ITERATIONS trong prompts.py")
c.ok(f"MAX_ITERATIONS >= 5 (đang là {MAXIT})",
     isinstance(MAXIT, int) and MAXIT >= 5,
     f"MAX_ITERATIONS={MAXIT} quá chật. Chuỗi demo cần 4 vòng "
     "(3 lần gọi tool + 1 lần chốt Final Answer) — để 3 là demo chết ở Guardrail")
c.ok(f"MAX_ITERATIONS <= 8 (đang là {MAXIT})",
     isinstance(MAXIT, int) and MAXIT <= 8,
     f"MAX_ITERATIONS={MAXIT} quá rộng, câu bẫy sẽ chạy lòng vòng mà không ai thấy phanh đâu")
c.ok("Có TIMEOUT_SECONDS", isinstance(getattr(prompts, "TIMEOUT_SECONDS", None), int),
     "Khai báo TIMEOUT_SECONDS cho mỗi lần gọi tool")

dat, tong = c.ket()
sys.exit(0 if dat == tong else 1)
