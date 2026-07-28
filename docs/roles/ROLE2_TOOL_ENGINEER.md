# 🛠️ ROLE 2 — TOOL ENGINEER

| | |
| :-- | :-- |
| **Người đảm nhận** | Nguyễn Chí Hướng — 2A202601203 |
| **Branch** | `role2-tool-engineer` |
| **File giữ** | `src/tools.py` |
| **Trọng số điểm** | 30% (ReAct Implementation & Tools — chia với Role 4) |

---

## 🎯 Việc của bạn

Viết các **"đồ nghề"** mà Agent gọi được. Mỗi tool là 1 hàm Python bình thường, nhưng có 2 yêu cầu khắt khe:

1. **Docstring phải rõ ràng** — LLM đọc docstring để biết khi nào nên gọi tool nào. Docstring mơ hồ = Agent gọi sai tool.
2. **Không bao giờ được crash** — gặp lỗi phải `return` chuỗi báo lỗi, để Agent đọc `Observation` và tự xử lý.

---

## 📍 MỐC 1 (20 phút) — Liệt kê tool

Đề tài: **#7 — Trợ Lý Tư Vấn Khóa Học Sinh Viên**. Bộ 4 tool đề xuất:

| Tool | Việc | Vì sao cần |
| :-- | :-- | :-- |
| `get_transcript(mssv)` | Trả bảng điểm + môn đã học | Dữ liệu cá nhân, LLM không thể tự biết |
| `search_courses(keyword)` | Tra môn trong danh mục | Danh mục môn thay đổi theo kỳ |
| `check_prerequisites(course_id)` | Trả danh sách môn tiên quyết | Kết quả này phụ thuộc tool trên |
| `check_schedule_conflict(course_ids)` | Kiểm tra trùng lịch | Thao tác tính toán trên dữ liệu thật |

> 💡 Cặp `get_transcript` → `check_prerequisites` chính là chỗ thể hiện **ReAct thật**: Agent phải xem bảng điểm rồi mới biết sinh viên thiếu môn gì.

---

## 📍 MỐC 2 (30 phút) — Viết tool + Docstring chuẩn

### Cấu trúc dữ liệu giả lập

Không cần database thật, chỉ cần `dict` ở đầu file:

```python
# Dữ liệu giả lập — đủ để demo, không cần DB thật
STUDENTS = {
    "2A202601203": {
        "ten": "Nguyễn Chí Hướng",
        "nganh": "Khoa học máy tính",
        "da_hoc": {"Toán rời rạc": "A", "Lập trình Python": "B+", "Cấu trúc dữ liệu": "A-"},
    },
    # ... thêm vài sinh viên nữa
}

COURSES = {
    "ML101": {
        "ten": "Machine Learning",
        "tin_chi": 3,
        "tien_quyet": ["Xác suất thống kê", "Đại số tuyến tính"],
        "lich": "Thứ 3, 08:00-10:00",
    },
    # ... thêm vài môn nữa
}
```

### Mẫu 1 tool chuẩn

```python
def get_transcript(mssv: str) -> str:
    """
    Tra cứu bảng điểm và danh sách môn đã học của một sinh viên.

    Dùng tool này khi cần biết sinh viên ĐÃ HỌC những môn gì,
    ví dụ để kiểm tra điều kiện tiên quyết trước khi đăng ký môn mới.

    Args:
        mssv (str): Mã số sinh viên (Ví dụ: '2A202601203')

    Returns:
        str: Ngành học và danh sách môn đã học kèm điểm.
             Nếu không tìm thấy MSSV, trả về chuỗi báo lỗi.
    """
    sv = STUDENTS.get(mssv.strip().upper())
    if not sv:
        return f"LỖI: Không tìm thấy sinh viên có MSSV '{mssv}' trong hệ thống."

    mon_da_hoc = ", ".join(f"{ten} ({diem})" for ten, diem in sv["da_hoc"].items())
    return f"Sinh viên {sv['ten']} — Ngành {sv['nganh']}. Đã học: {mon_da_hoc}."
```

Ba điểm cần bắt chước ở mẫu trên:

- Dòng **"Dùng tool này khi..."** — dạy LLM biết lúc nào nên gọi
- `Args` / `Returns` đầy đủ
- Trả `"LỖI: ..."` thay vì `raise` hay `None`

### Đăng ký tool

Cuối file phải có registry để Role 4 gọi được:

```python
AVAILABLE_TOOLS = {
    "get_transcript": get_transcript,
    "search_courses": search_courses,
    "check_prerequisites": check_prerequisites,
    "check_schedule_conflict": check_schedule_conflict,
}
```

---

## 📍 MỐC 3 (60 phút) — Chống crash

Role 1 sẽ ném câu bẫy vào Agent. Tool của bạn phải sống sót qua các trường hợp:

| Tình huống | Phải trả về |
| :-- | :-- |
| MSSV không tồn tại | `"LỖI: Không tìm thấy sinh viên..."` |
| Tên môn không có trong danh mục | `"LỖI: Không tìm thấy môn học..."` |
| Tham số rỗng / `None` | `"LỖI: Thiếu tham số..."` |
| Tham số sai kiểu (số thay vì chuỗi) | Ép kiểu bằng `str()` rồi xử lý |

Tự test nhanh:

```bash
.venv\Scripts\python.exe -c "from src.tools import get_transcript; print(get_transcript('9Z999'))"
```

Chạy không văng traceback là đạt.

---

## ✅ Checklist

- [ ] Mốc 1: Chốt danh sách 4 tool với cả nhóm
- [ ] Mốc 2: Viết dữ liệu giả lập (`STUDENTS`, `COURSES`) — ít nhất 3 sinh viên, 5 môn
- [ ] Mốc 2: Viết đủ 4 hàm tool, mỗi hàm có docstring "Dùng tool này khi..."
- [ ] Mốc 2: Khai báo `AVAILABLE_TOOLS`
- [ ] Mốc 3: Mọi tool trả `"LỖI: ..."` thay vì crash
- [ ] Mốc 3: Test thử 4 tình huống lỗi ở bảng trên

---

## 🔄 Git

```bash
git checkout role2-tool-engineer
git pull origin main
```

Sau khi làm xong:

```bash
git add src/tools.py
git commit -m "Role 2: 4 tools tu van khoa hoc + error handling"
git push origin role2-tool-engineer
```
