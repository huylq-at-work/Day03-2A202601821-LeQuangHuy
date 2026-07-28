"""
TEST ROLE 1 — Nguyễn Tiến Đạt (Product Architect & Observability)
Kiểm: config/test_cases.json + docs/trace_eval.md + docs/hybrid_flowchart.mermaid

Chạy:  .venv\\Scripts\\python.exe tests\\test_role1.py
"""

import json
import os
import re
import sys

from _harness import Check, duong_dan, nap_database

c = Check("ROLE 1 — PRODUCT ARCHITECT & OBSERVABILITY (Nguyễn Tiến Đạt)")
db = nap_database()
SDT_THAT = set(db["learners"])
MA_KHOA_THAT = set(db["courses"])

# ---------------------------------------------------------------- test_cases
c.muc("[1] File config/test_cases.json")

p = duong_dan("config", "test_cases.json")
tests = []
if c.ok("File tồn tại", os.path.exists(p), "Tạo file config/test_cases.json"):
    try:
        with open(p, encoding="utf-8") as f:
            tests = json.load(f)
        c.ok("JSON hợp lệ", True)
    except Exception as e:
        c.ok("JSON hợp lệ", False, f"test_cases.json lỗi cú pháp: {e}")

c.ok("Có đủ 5 test case", len(tests) >= 5,
     f"Mới có {len(tests)}/5 test case")

truong_du = all(
    all(k in t for k in ("id", "category", "question", "expected_behavior"))
    for t in tests
) if tests else False
c.ok("Mọi case đủ 4 trường (id/category/question/expected_behavior)", truong_du,
     "Thiếu trường trong test_cases.json")

# ---------------------------------------------------------------- phân loại
c.muc("[2] Phân bố loại câu hỏi")

def dem(dau):
    return sum(1 for t in tests if dau in t.get("category", ""))

n_de, n_multi, n_bay = dem("🟢"), dem("🟡"), dem("🔴")
c.ok(f"Có >=2 câu đơn giản (đang có {n_de})", n_de >= 2,
     "Thêm câu đơn giản, category chứa 🟢")
c.ok(f"Có >=2 câu multi-step (đang có {n_multi})", n_multi >= 2,
     "Thêm câu multi-step, category chứa 🟡")
c.ok(f"Có >=1 câu bẫy (đang có {n_bay})", n_bay >= 1,
     "Thêm câu edge case, category chứa 🔴")

# ---------------------------------------------------------------- đúng domain
c.muc("[3] Bám đúng đề tài marketplace khóa học")

noi_dung = json.dumps(tests, ensure_ascii=False)
tu_cu = [t for t in ("mssv", "sinh viên", "tiên quyết", "kỳ học", "môn học")
         if t.lower() in noi_dung.lower()]
c.ok("Không còn từ ngữ của đề tài cũ (trường đại học)", not tu_cu,
     f"Còn sót từ đề cũ: {', '.join(tu_cu)} — đề đã đổi sang marketplace bên ngoài")

sdt_dung = set(re.findall(r"\b0\d{9}\b", noi_dung))
sdt_co_that = sdt_dung & SDT_THAT
c.ok(f"Có dùng SĐT có thật trong DB ({len(sdt_co_that)} số)", bool(sdt_co_that),
     "Câu multi-step phải dùng SĐT có thật, vd 0912345203")

ma_dung = set(re.findall(r"\b[A-Z]{2,3}\d{3}\b", noi_dung))
ma_sai = ma_dung - MA_KHOA_THAT
c.ok("Mã khóa nhắc tới đều có thật (trừ câu bẫy)",
     len(ma_sai) <= 1,
     f"Mã khóa không tồn tại trong DB: {', '.join(sorted(ma_sai))}")

# ---------------------------------------------------------------- câu bẫy
c.muc("[4] Chất lượng câu bẫy")

cau_bay = [t for t in tests if "🔴" in t.get("category", "")]
bay_txt = json.dumps(cau_bay, ensure_ascii=False)
sdt_bay = set(re.findall(r"\b0\d{9}\b", bay_txt))
c.ok("Câu bẫy dùng dữ liệu KHÔNG tồn tại", bool(sdt_bay - SDT_THAT) or "999" in bay_txt,
     "Câu bẫy nên dùng SĐT/mã khóa không có trong DB, vd 0000000000")

c.ok("Câu bẫy có mô tả hành vi mong đợi rõ ràng",
     any(len(t.get("expected_behavior", "")) > 40 for t in cau_bay),
     "expected_behavior của câu bẫy cần nói rõ: không được bịa dữ liệu, Guardrail phải ngắt")

# ---------------------------------------------------------------- trace_eval
c.muc("[5] Báo cáo docs/trace_eval.md")

p2 = duong_dan("docs", "trace_eval.md")
noi = ""
if c.ok("File tồn tại", os.path.exists(p2), "Tạo docs/trace_eval.md"):
    with open(p2, encoding="utf-8") as f:
        noi = f.read()

c.ok("Có bảng Scoring Matrix", "coring" in noi or "Agentic Fit" in noi,
     "Thêm bảng Scoring Matrix chấm 1-5 cho 4 tiêu chí Agentic Fit")
c.ok("Có trace log đủ chuỗi Thought/Action/Observation",
     all(k in noi for k in ("Thought", "Action", "Observation")),
     "Dán ít nhất 1 trace log hoàn chỉnh có đủ Thought -> Action -> Observation")
c.ok("Trace có Final Answer", "Final Answer" in noi,
     "Trace log phải chạy tới Final Answer, không dừng giữa chừng")
c.ok("Có ghi lại câu trả lời của Chatbot baseline để so sánh",
     "aseline" in noi or "hatbot" in noi,
     "Ghi lại Chatbot baseline trả lời gì — đây là bằng chứng so sánh quan trọng nhất")

# ---------------------------------------------------------------- flowchart
c.muc("[6] Hybrid Flowchart")

p3 = duong_dan("docs", "hybrid_flowchart.mermaid")
noi3 = ""
if c.ok("File tồn tại", os.path.exists(p3), "Tạo docs/hybrid_flowchart.mermaid"):
    with open(p3, encoding="utf-8") as f:
        noi3 = f.read()

c.ok("Có nhánh Chatbot và nhánh Agent",
     ("hatbot" in noi3) and ("gent" in noi3),
     "Flowchart phải thể hiện rõ khi nào đi Chatbot path, khi nào đi ReAct path")
c.ok("Có nhắc tới Guardrail / giới hạn vòng lặp",
     ("uardrail" in noi3) or ("ITERATION" in noi3),
     "Vẽ thêm nhánh Guardrail ngắt vòng lặp")

dat, tong = c.ket()
sys.exit(0 if dat == tong else 1)
