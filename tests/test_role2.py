"""
TEST ROLE 2 — Nguyễn Chí Hướng (Tool Engineer)
Kiểm: src/tools.py — có đủ tool chưa, docstring chuẩn chưa, có crash không,
      và kết quả check_suitability có khớp 7 trường hợp đã kiểm chứng không.

Chạy:  .venv\\Scripts\\python.exe tests\\test_role2.py
"""

import sys

from _harness import Check, nap_database

c = Check("ROLE 2 — TOOL ENGINEER (Nguyễn Chí Hướng)")
db = nap_database()

TOOL_LOI = ["get_learner", "search_courses", "get_course_detail", "check_suitability"]
TOOL_THEM = ["get_provider", "compare_courses"]

# ---------------------------------------------------------------- nạp module
c.muc("[1] Nạp src/tools.py")

tools = None
try:
    import tools as _t
    tools = _t
    c.ok("import được tools.py", True)
except Exception as e:
    c.ok("import được tools.py", False, f"tools.py lỗi: {type(e).__name__}: {e}")

REG = getattr(tools, "AVAILABLE_TOOLS", None) if tools else None
c.ok("Có biến AVAILABLE_TOOLS kiểu dict", isinstance(REG, dict),
     "Khai báo AVAILABLE_TOOLS = {...} ở cuối tools.py")
REG = REG if isinstance(REG, dict) else {}

c.ok("Đã load mock_database.json (không hardcode dữ liệu)",
     hasattr(tools, "LEARNERS") or hasattr(tools, "COURSES") if tools else False,
     "Load config/mock_database.json thay vì gõ tay dữ liệu vào code")

# ---------------------------------------------------------------- có đủ tool
c.muc("[2] Tool bắt buộc (4 tool lõi)")
for ten in TOOL_LOI:
    c.ok(ten, ten in REG, f"Chưa có '{ten}' trong AVAILABLE_TOOLS")

c.muc("[3] Tool thêm điểm (không bắt buộc)")
for ten in TOOL_THEM:
    if ten in REG:
        c.ok(ten, True)
    else:
        c.bo_qua(ten, "chưa làm, không trừ điểm")

# ---------------------------------------------------------------- docstring
c.muc("[4] Docstring — LLM đọc cái này để biết gọi tool nào")
for ten in TOOL_LOI:
    f = REG.get(ten)
    d = (f.__doc__ or "") if f else ""
    c.ok(f"{ten}: có Args + Returns",
         "Args" in d and "Returns" in d,
         f"{ten} thiếu Args/Returns trong docstring")

if all(t in REG for t in TOOL_LOI):
    co_huong_dan = sum(
        1 for t in TOOL_LOI
        if "ùng tool này" in (REG[t].__doc__ or "") or "ùng khi" in (REG[t].__doc__ or "")
    )
    c.ok(f"Có câu 'Dùng tool này khi...' ({co_huong_dan}/4 tool)",
         co_huong_dan >= 3,
         "Thêm câu 'Dùng tool này khi...' vào docstring để LLM biết lúc nào nên gọi")

# ---------------------------------------------------------------- chạy thật
c.muc("[5] Chạy thật — không được crash")

def goi(ten, *a):
    return lambda: REG[ten](*a)

kq_hv = None
if "get_learner" in REG:
    kq_hv = c.thu("get_learner('0912345203')", goi("get_learner", "0912345203"))
    if kq_hv:
        c.ok("Trả về đúng tên học viên", "Hướng" in str(kq_hv),
             "get_learner trả sai dữ liệu, phải ra 'Nguyễn Chí Hướng'")
        c.ok("Có nhắc ngân sách", "2,000,000" in str(kq_hv) or "2000000" in str(kq_hv),
             "get_learner nên trả cả ngân sách để Agent lọc khóa")

    kq_loi = c.thu("get_learner('0000000000') — SĐT không tồn tại",
                   goi("get_learner", "0000000000"))
    c.ok("Trả chuỗi bắt đầu bằng 'LỖI:'",
         isinstance(kq_loi, str) and kq_loi.strip().upper().startswith("LỖI"),
         "SĐT không tồn tại phải trả 'LỖI: ...', không raise và không trả None")

if "get_course_detail" in REG:
    kq_on = c.thu("get_course_detail('AI302') — khóa online (si_so=null)",
                  goi("get_course_detail", "AI302"))
    c.ok("Không in ra 'None' với khóa online",
         isinstance(kq_on, str) and "None" not in kq_on,
         "Khóa online có si_so/dia_diem/han_dang_ky = null, phải xử lý thay vì in None")

    kq_ks = c.thu("get_course_detail('XYZ999') — mã không tồn tại",
                  goi("get_course_detail", "XYZ999"))
    c.ok("Trả 'LỖI:' cho mã khóa không tồn tại",
         isinstance(kq_ks, str) and kq_ks.strip().upper().startswith("LỖI"),
         "Mã khóa sai phải trả 'LỖI: ...'")

if "search_courses" in REG:
    c.thu("search_courses('AI', 2000000)", goi("search_courses", "AI", "2000000"))
    c.thu("search_courses('chủ đề không có', 1000)",
          goi("search_courses", "xyz không tồn tại", "1000"))

# ---------------------------------------------------------------- 7 ca chuẩn
c.muc("[6] check_suitability — 7 trường hợp đã kiểm chứng")

CA = [
    ("0912345203", "AI301", False, ["ngân sách", "trình độ", "lịch"]),
    ("0987654387", "EN101", False, ["lịch"]),
    ("0901234795", "PR201", True, []),
    ("0977888821", "EN101", False, ["lịch", "khu vực"]),
    ("0977888821", "MK201", True, []),
    ("0987654387", "EN201", False, ["ngân sách", "trình độ", "đầy"]),
    ("0901234795", "EN301", False, ["hạn"]),
]

if "check_suitability" not in REG:
    for sdt, ma, _, _ in CA:
        c.ok(f"{sdt} + {ma}", False, "Chưa có check_suitability")
else:
    f = REG["check_suitability"]
    for sdt, ma, mong_doi_phu_hop, tu_khoa in CA:
        try:
            r = str(f(sdt, ma))
        except Exception as e:
            c.ok(f"{sdt} + {ma}", False,
                 f"check_suitability({sdt}, {ma}) crash: {type(e).__name__}")
            continue
        thap = r.lower()
        la_phu_hop = ("phù hợp" in thap) and ("không phù hợp" not in thap)
        if mong_doi_phu_hop:
            c.ok(f"{sdt} + {ma} -> phù hợp", la_phu_hop,
                 f"{sdt}+{ma} phải ra PHÙ HỢP, đang trả: {r[:70]}")
        else:
            thieu = [k for k in tu_khoa if k not in thap]
            c.ok(f"{sdt} + {ma} -> trượt vì {', '.join(tu_khoa)}",
                 (not la_phu_hop) and not thieu,
                 f"{sdt}+{ma} phải nêu lý do [{', '.join(tu_khoa)}]"
                 + (f", còn thiếu: {', '.join(thieu)}" if thieu else "")
                 + f". Đang trả: {r[:70]}")

# ---------------------------------------------------------------- tham số lạ
c.muc("[7] Chống crash với tham số lạ")
for ten in TOOL_LOI:
    if ten not in REG:
        continue
    f = REG[ten]
    n = f.__code__.co_argcount if hasattr(f, "__code__") else 1
    try:
        f(*([""] * n))
        c.ok(f"{ten}('') — tham số rỗng", True)
    except Exception as e:
        c.ok(f"{ten}('') — tham số rỗng", False,
             f"{ten} crash khi tham số rỗng: {type(e).__name__}. Trả 'LỖI:' thay vì raise")

dat, tong = c.ket()
sys.exit(0 if dat == tong else 1)
