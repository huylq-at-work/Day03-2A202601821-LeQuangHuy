# 🛠️ ROLE 2 — TOOL ENGINEER

| | |
| :-- | :-- |
| **Người đảm nhận** | Nguyễn Chí Hướng — 2A202601203 |
| **Branch** | `role2-tool-engineer` |
| **File giữ** | `src/tools.py` |
| **Trọng số điểm** | 30% (ReAct Implementation & Tools — chia với Role 4) |

---

## 🎯 Đề tài & việc của bạn

**Trợ Lý Đăng Ký Khóa Học — marketplace khóa học bên ngoài** (online tự học + lớp offline tại trung tâm). Học viên định danh bằng **số điện thoại**.

Bạn viết các **"đồ nghề"** mà Agent gọi được. Hai yêu cầu khắt khe:

1. **Docstring phải rõ** — LLM đọc docstring để biết khi nào gọi tool nào. Mơ hồ = Agent gọi sai tool.
2. **Không bao giờ crash** — gặp lỗi phải `return` chuỗi báo lỗi, để Agent đọc `Observation` rồi tự xử lý.

📦 Dữ liệu đã có sẵn: [`config/mock_database.json`](../../config/mock_database.json) — 1000 học viên, 13 khóa, 5 nhà cung cấp, 6 giảng viên.
📘 Chi tiết từng trường: [DATABASE_SCHEMA.md](../DATABASE_SCHEMA.md).

---

## 📍 MỐC 1 (20 phút) — Load database & chốt danh sách tool

```python
import json, os

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(_BASE, "config", "mock_database.json"), "r", encoding="utf-8") as f:
    _DB = json.load(f)

LEARNERS    = _DB["learners"]
COURSES     = _DB["courses"]
PROVIDERS   = _DB["providers"]
INSTRUCTORS = _DB["instructors"]

CAP_DO = _DB["_meta"]["cap_do"]                 # ["mới bắt đầu","cơ bản","trung cấp","nâng cao"]
NGAY_HIEN_TAI = _DB["_meta"]["ngay_hien_tai"]   # "2026-07-28"
```

### Bộ tool

| Tool | Tham số | Trả về |
| :-- | :-- | :-- |
| `get_learner` | `sdt` | mục tiêu, trình độ, ngân sách, lịch rảnh, khu vực |
| `search_courses` | `chu_de, gia_toi_da` | danh sách mã khóa + tên + giá khớp |
| `get_course_detail` | `ma_khoa` | giá, trình độ, lịch, địa điểm, chỗ trống, hạn ĐK, rating |
| `check_suitability` | `sdt, ma_khoa` | **phù hợp / danh sách lý do trượt** |
| `get_provider` *(thêm)* | `ma_ncc` | tên, loại, khu vực, đánh giá |
| `compare_courses` *(thêm)* | `ma1, ma2` | so giá / thời lượng / rating / chứng chỉ |

4 tool đầu là lõi. 2 tool sau làm nếu dư thời gian.

---

## 📍 MỐC 2 (30 phút) — Viết tool + Docstring chuẩn

### Mẫu một tool chuẩn

```python
def get_learner(sdt: str) -> str:
    """
    Tra cứu hồ sơ học viên theo số điện thoại.

    Dùng tool này ĐẦU TIÊN khi câu hỏi có nhắc tới số điện thoại,
    để biết mục tiêu học, trình độ, ngân sách, lịch rảnh và khu vực của học viên.

    Args:
        sdt (str): Số điện thoại học viên (Ví dụ: '0912345203')

    Returns:
        str: Thông tin hồ sơ học viên.
             Nếu không tìm thấy số điện thoại, trả về chuỗi báo lỗi.
    """
    hv = LEARNERS.get(sdt.strip())
    if not hv:
        return f"LỖI: Không tìm thấy học viên có số điện thoại '{sdt}'."

    return (f"{hv['ho_ten']} — mục tiêu: {', '.join(hv['muc_tieu'])}; "
            f"trình độ: {hv['trinh_do']}; ngân sách: {hv['ngan_sach']:,}đ; "
            f"rảnh: {', '.join(hv['lich_ranh'])}; khu vực: {hv['khu_vuc']}.")
```

Ba điểm cần bắt chước:

- Dòng **"Dùng tool này khi..."** — dạy LLM biết lúc nào nên gọi
- `Args` / `Returns` đầy đủ
- Trả `"LỖI: ..."` thay vì `raise` hay `None`

### Đăng ký tool

Cuối file phải có registry để Role 4 gọi được:

```python
AVAILABLE_TOOLS = {
    "get_learner": get_learner,
    "search_courses": search_courses,
    "get_course_detail": get_course_detail,
    "check_suitability": check_suitability,
}
```

---

## 📍 MỐC 3 (60 phút) — `check_suitability`, tool ăn điểm nhất

Kiểm **5 chiều**, và phải trả về **lý do cụ thể** chứ không phải `True/False`:

```
ngân sách  → gia <= ngan_sach
trình độ   → CAP_DO.index(trinh_do) >= CAP_DO.index(trinh_do_yeu_cau)
lịch       → mọi buổi trong lich_hoc phải thuộc lich_ranh        (bỏ qua nếu online)
khu vực    → dia_diem == khu_vuc                                 (bỏ qua nếu online)
chỗ + hạn  → da_dang_ky < si_so, và han_dang_ky >= NGAY_HIEN_TAI (bỏ qua nếu online)
```

Kết quả mong muốn:

> `Không phù hợp. Lý do: vượt ngân sách (15,000,000 > 2,000,000); trình độ chưa đạt (mới bắt đầu < trung cấp); lịch không khớp (T3 tối, T5 tối).`

Có lý do cụ thể thì Agent mới giải thích được cho học viên — đó chính là chỗ Chatbot bó tay.

### Quy đổi lịch

`lich_hoc` ghi giờ, `lich_ranh` ghi buổi. Quy đổi bằng giờ bắt đầu:

```python
def buoi_cua(lich: str) -> str:
    """'T2 19:00-21:00' -> 'T2 tối'"""
    thu, gio = lich.split(" ", 1)
    h = int(gio[:2])
    return f"{thu} {'sáng' if h < 12 else 'chiều' if h < 18 else 'tối'}"
```

---

## ⚠️ Ba cái bẫy trong dữ liệu dễ làm code văng

| Bẫy | Ở đâu | Xử lý |
| :-- | :-- | :-- |
| **`si_so = null`** | Mọi khóa online (không giới hạn chỗ) | Phải `if si_so is not None` trước khi so sánh, không thì `None > int` văng `TypeError` |
| **`lich_hoc = []`** | Mọi khóa online (tự học) | Không được báo "lịch không khớp" cho khóa online |
| **`han_dang_ky = null`** | Mọi khóa online | Không được so sánh `None < "2026-07-28"` |

Cách gọn nhất: kiểm `if kh["hinh_thuc"] == "offline"` rồi mới chạy 3 chiều lịch / khu vực / chỗ + hạn.

> 🔒 Dùng `NGAY_HIEN_TAI` từ file, **đừng dùng `datetime.now()`**. Ngày cố định thì test case của Role 1 chạy lúc nào cũng ra kết quả giống nhau.

---

## 🧪 Tự test chống crash

Role 1 sẽ ném câu bẫy vào Agent. Tool phải sống sót:

| Tình huống | Phải trả về |
| :-- | :-- |
| SĐT không tồn tại (`0000000000`) | `"LỖI: Không tìm thấy học viên..."` |
| Mã khóa không tồn tại (`XYZ999`) | `"LỖI: Không tìm thấy khóa học..."` |
| Tham số rỗng / `None` | `"LỖI: Thiếu tham số..."` |
| Khóa online đem đi kiểm lịch | Bỏ qua, không báo lỗi lịch |

```bash
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'src'); from tools import get_learner; print(get_learner('0000000000'))"
```

Chạy không văng traceback là đạt.

### Kết quả đúng để đối chiếu

| Học viên | Khóa | Kết quả |
| :-- | :-- | :-- |
| `0912345203` | `AI301` | 3 lỗi: ngân sách, trình độ, lịch |
| `0987654387` | `EN101` | 1 lỗi: lịch |
| `0901234795` | `PR201` | PHÙ HỢP |
| `0977888821` | `EN101` | 2 lỗi: lịch, khu vực |
| `0987654387` | `EN201` | 3 lỗi: ngân sách, trình độ, lớp đầy |
| `0901234795` | `EN301` | 1 lỗi: hết hạn đăng ký |

Tool của bạn phải ra đúng 6 dòng này.

---

## 🧪 Tự chấm — chạy bất cứ lúc nào

```bash
.venv\Scripts\python.exe tests\test_role2.py
```

Test này chấm 18 mục và in ra **chính xác còn phải sửa gì**. Nó tự chạy hộ bạn:

- Đủ 4 tool lõi trong `AVAILABLE_TOOLS` chưa
- Docstring có `Args` / `Returns` / câu "Dùng tool này khi..." chưa
- Gọi thật với SĐT sai, mã khóa sai, tham số rỗng → có trả `LỖI:` hay **crash**
- Khóa online có bị in ra `None` không (bẫy `si_so = null`)
- **Đủ 7 kết quả `check_suitability` ở bảng trên** — sai chiều nào nó chỉ đúng chiều đó

Chạy tới khi thấy `COVERAGE: 18/18` là xong phần bạn.

---

## ✅ Checklist

- [ ] Mốc 1: Load được `mock_database.json`, chốt danh sách tool với nhóm
- [ ] Mốc 2: Viết 4 tool lõi, mỗi tool có docstring "Dùng tool này khi..."
- [ ] Mốc 2: Khai báo `AVAILABLE_TOOLS`
- [ ] Mốc 3: `check_suitability` kiểm đủ 5 chiều, trả **lý do cụ thể**
- [ ] Mốc 3: Xử lý `si_so = null`, `lich_hoc = []`, `han_dang_ky = null`
- [ ] Mốc 3: Đối chiếu đúng 6 dòng kết quả ở bảng trên

---

## 🔄 Git

```bash
git checkout role2-tool-engineer
git pull origin main
```

Xong việc:

```bash
git add src/tools.py
git commit -m "Role 2: tools marketplace khoa hoc + error handling"
git push origin role2-tool-engineer
```
