"""Trich xuat schema tu mock_database.json ra tai lieu cho Prompt Engineer."""
import json, io, os

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(_BASE, "config", "mock_database.json")
OUT = os.path.join(_BASE, "docs", "SCHEMA_FOR_PROMPT.md")

with open(DB, encoding="utf-8") as f:
    db = json.load(f)

L, C, P, I = db["learners"], db["courses"], db["providers"], db["instructors"]
meta = db["_meta"]

def uniq(vals):
    out = []
    for v in vals:
        if v not in out:
            out.append(v)
    return out

trinh_do   = uniq(x["trinh_do"] for x in L.values())
khu_vuc    = sorted({x["khu_vuc"] for x in L.values()})
hinh_thuc  = sorted({x["hinh_thuc_uu_tien"] for x in L.values()})
muc_tieu   = sorted({t for x in L.values() for t in x["muc_tieu"]})
buoi       = sorted({b for x in L.values() for b in x["lich_ranh"]})
ns         = sorted({x["ngan_sach"] for x in L.values()})
chu_de     = sorted({t for c in C.values() for t in c["chu_de"]})
gia        = sorted(c["gia"] for c in C.values())

b = io.StringIO()
w = b.write

w("# 📖 SCHEMA RÚT GỌN CHO PROMPT ENGINEER (Role 3)\n\n")
w("> File này **sinh tự động** từ [`config/mock_database.json`](../config/mock_database.json) — "
  "không chỉnh tay, dữ liệu đổi thì chạy lại script.\n")
w("> Mục đích: để Role 3 viết ví dụ few-shot trong `REACT_SYSTEM_PROMPT` **dùng đúng dữ liệu có thật**.\n\n")
w(f"**Quy mô**: {len(L):,} học viên · {len(C)} khóa học · {len(P)} nhà cung cấp · {len(I)} giảng viên.  \n")
w(f"**Ngày hệ thống (cố định)**: `{meta['ngay_hien_tai']}`\n\n")
w("---\n\n")

w("## 1. Từ vựng dữ liệu — chỉ những giá trị này là hợp lệ\n\n")
w("Viết ví dụ trong prompt thì phải dùng đúng các giá trị dưới đây, "
  "bịa giá trị lạ sẽ dạy LLM gọi tool sai.\n\n")
w("| Khái niệm | Giá trị hợp lệ |\n| :-- | :-- |\n")
w(f"| **Trình độ** (có thứ tự) | {' < '.join('`'+x+'`' for x in meta['cap_do'])} |\n")
w(f"| Trình độ học viên thực tế | {', '.join('`'+x+'`' for x in trinh_do)} |\n")
w(f"| **Chủ đề khóa học** | {', '.join('`'+x+'`' for x in chu_de)} |\n")
w(f"| Mục tiêu học viên | {', '.join('`'+x+'`' for x in muc_tieu)} |\n")
w(f"| **Khu vực** | {', '.join('`'+x+'`' for x in khu_vuc)} |\n")
w(f"| **Hình thức** | khóa học: `online` / `offline` · ưu tiên HV: {', '.join('`'+x+'`' for x in hinh_thuc)} |\n")
w(f"| **Buổi rảnh** | `T2`–`T7`, `CN` × `sáng` / `chiều` / `tối` (vd `{buoi[0]}`) |\n")
w(f"| **Ngân sách** | {ns[0]:,}đ – {ns[-1]:,}đ |\n")
w(f"| **Giá khóa** | {gia[0]:,}đ – {gia[-1]:,}đ |\n")
w("\n---\n\n")

w("## 2. Toàn bộ 13 khóa học\n\n")
w("Dùng bảng này để viết ví dụ — mọi mã khóa, giá, lịch đều có thật.\n\n")
w("| Mã | Tên | Chủ đề | Trình độ | HT | Giá | Lịch | Nơi | Chỗ | Hạn ĐK |\n")
w("| :-- | :-- | :-- | :-- | :-: | --: | :-- | :-- | :-: | :-- |\n")
for ma, c in C.items():
    lich = ", ".join(c["lich_hoc"]) if c["lich_hoc"] else "tự học"
    cho = "∞" if c["si_so"] is None else f"{c['da_dang_ky']}/{c['si_so']}"
    han = c["han_dang_ky"] or "—"
    dd = c["dia_diem"] or "—"
    note = ""
    if c["si_so"] and c["da_dang_ky"] >= c["si_so"]:
        note = " ⛔"
    if c["han_dang_ky"] and c["han_dang_ky"] < meta["ngay_hien_tai"]:
        note += " ⏰"
    w(f"| `{ma}`{note} | {c['ten']} | {', '.join(c['chu_de'])} | {c['trinh_do_yeu_cau']} | "
      f"{c['hinh_thuc'][:2]} | {c['gia']:,} | {lich} | {dd} | {cho} | {han} |\n")
w("\n⛔ = lớp đã đầy · ⏰ = hết hạn đăng ký · ∞ = online không giới hạn chỗ\n\n")
w("---\n\n")

w("## 3. Bốn học viên dùng để viết ví dụ\n\n")
FIXED = ["0912345203", "0987654387", "0901234795", "0977888821"]
w("| SĐT | Họ tên | Mục tiêu | Trình độ | Ngân sách | Rảnh | Khu vực |\n")
w("| :-- | :-- | :-- | :-- | --: | :-- | :-- |\n")
for s in FIXED:
    h = L[s]
    w(f"| `{s}` | {h['ho_ten']} | {', '.join(h['muc_tieu'])} | {h['trinh_do']} | "
      f"{h['ngan_sach']:,} | {', '.join(h['lich_ranh'])} | {h['khu_vuc']} |\n")
w("\n996 học viên còn lại sinh ngẫu nhiên (seed cố định). 4 người trên là dữ liệu cố định, "
  "mọi bẫy đều dựa vào họ.\n\n")
w("---\n\n")

w("## 4. Cấu trúc JSON — bản rút gọn\n\n")
w("```json\n")
skeleton = {
    "_meta": meta,
    "learners": {FIXED[0]: L[FIXED[0]]},
    "courses": {"AI302": C["AI302"], "AI301": C["AI301"]},
    "providers": {"TT02": P["TT02"]},
    "instructors": {"GV03": I["GV03"]},
}
w(json.dumps(skeleton, ensure_ascii=False, indent=2))
w("\n```\n\n")
w("> ⚠️ Khóa **online** có `lich_hoc: []`, `khai_giang/han_dang_ky/dia_diem: null`, "
  "`si_so: null` (không giới hạn chỗ). Khóa **offline** thì đủ cả.\n\n")
w("---\n\n")

w("## 5. Observation sẽ trông như thế nào\n\n")
w("Đây là phần quan trọng nhất với Role 3: ví dụ few-shot trong prompt phải khớp "
  "với chuỗi mà tool thật sự trả về, nếu không LLM sẽ học sai định dạng.\n\n")

h = L["0912345203"]
w("**`get_learner[0912345203]`**\n\n```\n")
w(f"{h['ho_ten']} — mục tiêu: {', '.join(h['muc_tieu'])}; trình độ: {h['trinh_do']}; "
  f"ngân sách: {h['ngan_sach']:,}đ; rảnh: {', '.join(h['lich_ranh'])}; khu vực: {h['khu_vuc']}.\n```\n\n")

w("**`search_courses[AI, 2000000]`**\n\n```\n")
for ma, c in C.items():
    if "AI" in c["chu_de"] and c["gia"] <= 2_000_000:
        w(f"{ma} - {c['ten']} - {c['gia']:,}đ - {c['hinh_thuc']} - {c['trinh_do_yeu_cau']}\n")
w("```\n\n")

c = C["AI301"]
w("**`get_course_detail[AI301]`**\n\n```\n")
w(f"{c['ten']} ({c['gia']:,}đ) — {c['hinh_thuc']}, {c['thoi_luong']}, trình độ {c['trinh_do_yeu_cau']}. "
  f"Lịch: {', '.join(c['lich_hoc'])} tại {c['dia_diem']}. "
  f"Còn {c['si_so']-c['da_dang_ky']}/{c['si_so']} chỗ, hạn đăng ký {c['han_dang_ky']}. "
  f"Rating {c['rating']}.\n```\n\n")

w("**`check_suitability[0912345203, AI302]`** — trường hợp phù hợp\n\n```\nPhù hợp.\n```\n\n")
w("**`check_suitability[0912345203, AI301]`** — trường hợp trượt\n\n```\n")
w("Không phù hợp. Lý do: vượt ngân sách (15,000,000 > 2,000,000); "
  "trình độ chưa đạt (mới bắt đầu < trung cấp); lịch không khớp (T3 tối, T5 tối).\n```\n\n")
w("**`get_learner[0000000000]`** — trường hợp lỗi\n\n```\n")
w("LỖI: Không tìm thấy học viên có số điện thoại '0000000000'.\n```\n\n")
w("> 🔑 Mọi lỗi đều bắt đầu bằng `LỖI:`. Prompt phải dạy LLM: gặp `LỖI:` thì **dừng và báo lịch sự**, "
  "tuyệt đối không đoán hay bịa dữ liệu thay thế.\n\n")
w("---\n\n")

w("## 6. Bảy kết quả `check_suitability` đã kiểm chứng\n\n")
w("| SĐT | Khóa | Kết quả |\n| :-- | :-- | :-- |\n")
for row in [
    ("0912345203", "AI301", "3 lỗi: ngân sách, trình độ, lịch"),
    ("0987654387", "EN101", "1 lỗi: lịch"),
    ("0901234795", "PR201", "**PHÙ HỢP**"),
    ("0977888821", "EN101", "2 lỗi: lịch, khu vực"),
    ("0977888821", "MK201", "**PHÙ HỢP**"),
    ("0987654387", "EN201", "3 lỗi: ngân sách, trình độ, lớp đầy"),
    ("0901234795", "EN301", "1 lỗi: hết hạn đăng ký"),
]:
    w(f"| `{row[0]}` | `{row[1]}` | {row[2]} |\n")
w("\nDùng những cặp này để viết ví dụ trong prompt — chắc chắn đúng với dữ liệu.\n")

with open(OUT, "w", encoding="utf-8") as f:
    f.write(b.getvalue())

print(f"Da ghi {OUT}")
print(f"Kich thuoc: {len(b.getvalue())/1024:.1f} KB")
print(f"Tu vung: {len(trinh_do)} trinh do, {len(chu_de)} chu de, {len(khu_vuc)} khu vuc, {len(buoi)} buoi")
