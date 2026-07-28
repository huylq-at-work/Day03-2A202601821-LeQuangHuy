"""
TEST ROLE 2 — Nguyễn Chí Hướng (Tool Engineer)
Kiểm: src/tools.py — có đủ tool chưa, docstring chuẩn chưa, có crash không,
      và kết quả check_suitability có khớp 7 trường hợp đã kiểm chứng không.

Chạy:.venv\\Scripts\\python.exe tests\\test_role2.py
"""

import json
import os
import sys

from _harness import Check, nap_database

c = Check("ROLE 2 — TOOL ENGINEER (Nguyễn Chí Hướng)")
db = nap_database()

TOOL_LOI = ["get_learner", "search_courses", "get_course_detail", "check_suitability"]
TOOL_THEM = ["get_provider", "compare_courses", "list_topics"]

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

    r_mh = c.thu("search_courses('khác', ...) — từ mơ hồ",
                 goi("search_courses", "khác", "99000000"))
    c.ok("Từ mơ hồ 'khác' không bị coi là tên chủ đề",
         isinstance(r_mh, str) and "Không tìm thấy" not in r_mh,
         "Người dùng hỏi 'còn môn khác không' thì LLM hay truyền chữ 'khác'. "
         "Phải duyệt toàn danh mục thay vì đi tìm đúng chữ đó")

    r_dai = c.thu("search_courses trả nhiều kết quả — có cắt bớt không",
                  goi("search_courses", "lập trình", "99000000"))
    c.ok("Kết quả dài được cắt và nói rõ đã cắt",
         isinstance(r_dai, str) and (r_dai.count("\n") <= 16),
         "128 khóa mà đổ hết ra thì Observation quá dài, phải giới hạn và ghi rõ còn bao nhiêu")

# Cac muc duoi day co GHI du lieu that. Don so du tu lan chay truoc de test
# chay lai bao nhieu lan cung ra ket qua giong nhau.
SDT_THU_NGHIEM = ["0900000199", "0900000288", "0977111222", "0955111222"]


def don_du_lieu_thu():
    from _harness import duong_dan as _dd
    p_moi = _dd("config", "hoc_vien_moi.json")
    try:
        moi = json.load(open(p_moi, encoding="utf-8")) if os.path.exists(p_moi) else {}
    except Exception:
        moi = {}
    for s in SDT_THU_NGHIEM:
        moi.pop(s, None)
        if tools and hasattr(tools, "LEARNERS"):
            tools.LEARNERS.pop(s, None)
    with open(p_moi, "w", encoding="utf-8") as fh:
        json.dump(moi, fh, ensure_ascii=False, indent=2)


don_du_lieu_thu()

c.muc("[5B] Ngân sách không giới hạn")

if "search_courses" in REG:
    for cach_noi in ["", "không giới hạn", "bao nhiêu cũng được"]:
        r = c.thu(f"search_courses('vật lý', {cach_noi!r})",
                  goi("search_courses", "vật lý", cach_noi))
        c.ok(f"-> không báo lỗi với {cach_noi!r}",
             isinstance(r, str) and not r.strip().upper().startswith("LỖI"),
             f"Ngân sách {cach_noi!r} nghĩa là không giới hạn, không được trả LỖI")

    r = c.thu("search_courses('vật lý', 'abc') — nhập bậy",
              goi("search_courses", "vật lý", "abc"))
    c.ok("Vẫn từ chối giá trị vô nghĩa",
         isinstance(r, str) and r.strip().upper().startswith("LỖI"),
         "'abc' không phải 'không giới hạn', phải trả LỖI")

if "dang_ky_hoc_vien" in REG and "check_suitability" in REG and "get_learner" in REG:
    sdt_vh = "0900000288"
    r = c.thu("Đăng ký học viên ngân sách không giới hạn",
              lambda: REG["dang_ky_hoc_vien"](sdt_vh, "Học Viên Vô Hạn", "vật lý",
                                              "cơ bản", "không giới hạn", "Hà Nội", "T2 tối"))
    c.ok("Tạo được hồ sơ không giới hạn ngân sách",
         isinstance(r, str) and not r.strip().upper().startswith("LỖI"),
         "Phải cho phép đăng ký khi học viên không đặt trần giá")

    r = c.thu("get_learner hiển thị ngân sách", lambda: REG["get_learner"](sdt_vh))
    c.ok("Hiển thị 'không giới hạn', không in None",
         isinstance(r, str) and "không giới hạn" in r and "None" not in r,
         "get_learner phải ghi rõ 'không giới hạn' thay vì None")

    r = c.thu("check_suitability với ngân sách None",
              lambda: REG["check_suitability"](sdt_vh, "AI301"))
    c.ok("Không crash và không báo vượt ngân sách",
         isinstance(r, str) and "ngân sách" not in r.lower(),
         "Ngân sách None thì phải BỎ QUA chiều ngân sách, "
         "không được so None với số (crash) cũng không được báo vượt")

c.muc("[5C] Lọc theo hình thức online/offline")

if "search_courses" in REG:
    f_sc = REG["search_courses"]

    r2 = c.thu("search_courses 2 tham số vẫn chạy (tương thích ngược)",
               lambda: f_sc("vật lý", ""))
    c.ok("Không vỡ khi thiếu tham số hình thức",
         isinstance(r2, str) and not r2.strip().upper().startswith("LỖI"),
         "Thêm tham số thứ 3 không được làm hỏng lời gọi 2 tham số cũ")

    r_on = c.thu("search_courses(..., 'online')", lambda: f_sc("vật lý", "", "online"))
    c.ok("Lọc online chỉ trả khóa online",
         isinstance(r_on, str) and "offline" not in r_on,
         "Lọc 'online' mà kết quả còn khóa offline — người ở xa không học được")

    r_off = c.thu("search_courses(..., 'offline')", lambda: f_sc("vật lý", "", "offline"))
    c.ok("Lọc offline chỉ trả khóa offline",
         isinstance(r_off, str) and "- online -" not in r_off,
         "Lọc 'offline' mà kết quả còn khóa online")

    r_vn = c.thu("Hiểu cách nói tiếng Việt ('trực tuyến')",
                 lambda: f_sc("vật lý", "", "trực tuyến"))
    c.ok("'trực tuyến' hiểu là online",
         isinstance(r_vn, str) and "offline" not in r_vn,
         "Người dùng hay nói 'trực tuyến' thay vì 'online'")

    r_la = c.thu("Hình thức vô nghĩa -> không lọc", lambda: f_sc("vật lý", "", "abcxyz"))
    c.ok("Giá trị lạ thì bỏ qua bộ lọc, không trả LỖI",
         isinstance(r_la, str) and not r_la.strip().upper().startswith("LỖI"),
         "Hình thức không nhận diện được thì coi như không lọc, đừng chặn cả câu tra cứu")

if "list_topics" in REG:
    r_lt_on = c.thu("list_topics(hình thức online)", lambda: REG["list_topics"]("", "online"))
    c.ok("list_topics lọc được theo hình thức",
         isinstance(r_lt_on, str) and "online" in r_lt_on,
         "list_topics phải nhận tham số hình thức để dùng cho học viên ở xa")

if "list_topics" in REG:
    r_lt = c.thu("list_topics() — không lọc giá", goi("list_topics", ""))
    c.ok("Trả về danh sách chủ đề kèm số khóa",
         isinstance(r_lt, str) and "chủ đề" in r_lt and "khóa" in r_lt,
         "list_topics phải liệt kê chủ đề kèm số lượng khóa")
    c.thu("list_topics('1000000') — có lọc giá", goi("list_topics", "1000000"))

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
c.muc("[7] dang_ky_hoc_vien — tool ghi dữ liệu")

if "dang_ky_hoc_vien" not in REG:
    c.ok("Có tool dang_ky_hoc_vien", False, "Chưa có tool đăng ký học viên mới")
else:
    dk = REG["dang_ky_hoc_vien"]
    c.ok("Có tool dang_ky_hoc_vien", True)

    def thu_dk(*a):
        try:
            return str(dk(*a))
        except Exception as e:
            return f"CRASH {type(e).__name__}"

    r = thu_dk("123", "Trần Văn Nam", "AI", "cơ bản", "5000000", "Hà Nội", "T2 tối")
    c.ok("SĐT sai định dạng -> LỖI", r.upper().startswith("LỖI"),
         f"SĐT '123' phải bị từ chối, đang trả: {r[:60]}")

    r = thu_dk("0912345203", "Trần Văn Nam", "AI", "cơ bản", "5000000", "Hà Nội", "T2 tối")
    c.ok("SĐT đã tồn tại -> LỖI", r.upper().startswith("LỖI"),
         "Không được ghi đè hồ sơ đã có")

    r = thu_dk("0977111222", "Trần Văn Nam", "AI", "siêu cấp", "5000000", "Hà Nội", "T2 tối")
    c.ok("Trình độ không hợp lệ -> LỖI", r.upper().startswith("LỖI"),
         f"Trình độ 'siêu cấp' phải bị từ chối, đang trả: {r[:60]}")

    r = thu_dk("0977111222", "Trần Văn Nam", "AI", "cơ bản", "abc", "Hà Nội", "T2 tối")
    c.ok("Ngân sách không phải số -> LỖI", r.upper().startswith("LỖI"),
         "Ngân sách 'abc' phải bị từ chối")

    r = thu_dk("0977111222", "", "AI", "cơ bản", "5000000", "Hà Nội", "T2 tối")
    c.ok("Thiếu họ tên -> LỖI", r.upper().startswith("LỖI"), "Họ tên rỗng phải bị từ chối")

    # Đăng ký thật rồi kiểm tra file gốc có bị đụng vào không
    import hashlib
    from _harness import duong_dan as _dd

    def _bam():
        with open(_dd("config", "mock_database.json"), "rb") as fh:
            return hashlib.md5(fh.read()).hexdigest()

    truoc = _bam()
    sdt_thu = "0900000199"
    thu_dk(sdt_thu, "Học Viên Kiểm Thử", "AI", "cơ bản", "4000000", "Hà Nội", "T2 tối|T4 tối")
    c.ok("mock_database.json KHÔNG bị ghi đè", truoc == _bam(),
         "Hồ sơ mới phải lưu sang config/hoc_vien_moi.json, không được sửa file dữ liệu gốc "
         "(sửa là script tái lập và test của Role 1 hỏng theo)")

    r = thu_dk(sdt_thu, "Trùng", "AI", "cơ bản", "4000000", "Hà Nội", "T2 tối")
    c.ok("Hồ sơ vừa tạo tra lại được", r.upper().startswith("LỖI") and "đã có hồ sơ" in r,
         "Sau khi tạo, gọi lại cùng SĐT phải báo đã tồn tại")

c.muc("[8] Chống crash với tham số lạ")
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
