# 🗄️ MOCK DATABASE SCHEMA — Trợ Lý Tư Vấn Khóa Học

> Bản thiết kế gợi ý cho **Role 2 (Tool Engineer)**.
> 📦 Dữ liệu thật nằm ở **[`config/mock_database.json`](../config/mock_database.json)** — file này chỉ giải thích cấu trúc.
> Dữ liệu đã cài sẵn các "bẫy" để Role 1 viết test case và Role 3 thử Guardrail.

**Quy mô**: 1000 sinh viên · 10 môn học · 4 giảng viên (~245 KB).

996 sinh viên sinh ngẫu nhiên bằng seed cố định (chạy lại ra y hệt, để test case của Role 1 luôn tái lập được). **4 sinh viên đầu là dữ liệu thật của nhóm và được giữ cố định** — mọi bẫy ở mục 3 đều dựa vào 4 mã này, đừng sửa:

| MSSV | Tên | Đã học | Dùng làm bẫy gì |
| :-- | :-- | :-- | :-- |
| `2A202601203` | Nguyễn Chí Hướng | PY101, TR101, CT102 | Thiếu **2** môn tiên quyết của ML101 |
| `2A202601387` | Nguyễn Tiến Đạt | PY101, TR101, XS102 | Thiếu **1** môn tiên quyết của ML101 |
| `2A202601795` | Phạm Thị Liên | PY101, TR101, XS102, DS103, CT102 | **Đủ** điều kiện ML101 |
| `2A202601821` | Lê Quang Huy | PY101, TR101, CT102, DS103 | Thiếu XS102 |

---

## 1. Cách load trong `src/tools.py`

```python
import json
import os

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(_BASE, "config", "mock_database.json"), "r", encoding="utf-8") as f:
    _DB = json.load(f)

STUDENTS = _DB["students"]
COURSES = _DB["courses"]
LECTURERS = _DB["lecturers"]
```

Tách data ra JSON để sửa dữ liệu không cần đụng code — thêm sinh viên hay môn học chỉ việc sửa file JSON.

---

## 2. Cấu trúc 3 bảng

```
students                      courses                    lecturers
────────                      ───────                    ─────────
<mssv> (khóa)                 <ma_mon> (khóa)            <ma_gv> (khóa)
  ten                           ten                        ten
  nganh                         tin_chi                    khoa
  ky_hien_tai                   tien_quyet[] ──┐           danh_gia
  da_hoc{ma_mon: điểm} ───────────────────────┘           chuyen_mon[]
  so_thich[] ───────┐           ma_gv ──────────────────────► (khóa ngoại)
  trinh_do          │           lich
                    │           si_so / da_dang_ky
                    └─────────► tags[]
```

### Bảng trường

| Bảng | Trường | Kiểu | Ghi chú |
| :-- | :-- | :-- | :-- |
| `students` | `ten`, `nganh` | string | |
| | `ky_hien_tai` | int | |
| | `da_hoc` | object `{ma_mon: điểm}` | **khóa ngoại** → `courses` |
| | `so_thich` | array\<string\> | **nối** với `courses.tags` |
| | `trinh_do` | string | `trung bình` / `khá` / `giỏi` |
| `courses` | `ten` | string | |
| | `tin_chi` | int | |
| | `tien_quyet` | array\<ma_mon\> | **khóa ngoại** → `courses` (tự tham chiếu) |
| | `ma_gv` | string | **khóa ngoại** → `lecturers` |
| | `lich` | string | dạng `T3 08:00-10:00` |
| | `si_so`, `da_dang_ky` | int | `da_dang_ky >= si_so` là hết chỗ |
| | `tags` | array\<string\> | **nối** với `students.so_thich` |
| `lecturers` | `ten`, `khoa` | string | |
| | `danh_gia` | float | thang 5.0 |
| | `chuyen_mon` | array\<string\> | |

### Ba đường nối quan trọng nhất

| Nối | Cho phép chuỗi suy luận |
| :-- | :-- |
| `students.so_thich` ↔ `courses.tags` | Biết sở thích SV → gợi ý môn phù hợp |
| `students.da_hoc` ↔ `courses.tien_quyet` | Biết đã học gì → tính còn thiếu môn nào |
| `courses.ma_gv` → `lecturers` | Biết môn → tra giảng viên dạy môn đó |

Không có 3 trường này thì Agent chỉ cần gọi 1 tool là xong → mất điểm Agentic Fit.

---

## 3. Bẫy đã cài sẵn trong dữ liệu

Role 1 (Đạt) dùng bảng này để viết test case, Role 3 (Liên) dùng để thử Guardrail:

| Bẫy | Nằm ở đâu | Agent phải phản ứng sao |
| :-- | :-- | :-- |
| **Thiếu 2 môn tiên quyết** | `2A202601203` (Hướng) đăng ký `ML101` | Báo thiếu `XS102` + `DS103` |
| **Thiếu 1 môn tiên quyết** | `2A202601387` (Đạt) đăng ký `ML101` | Báo chỉ còn thiếu `DS103` |
| **Đủ điều kiện** | `2A202601795` (Liên) đăng ký `ML101` | Xác nhận đăng ký được |
| **Lớp hết chỗ** | `DL201` có `si_so == da_dang_ky == 30` | Báo hết chỗ, không cho đăng ký |
| **Trùng lịch** | `ML101` và `NLP301` cùng `T3 08:00-10:00` | Báo trùng, chỉ chọn 1 |
| **Tiên quyết dây chuyền** | `DL201` cần `ML101`, `ML101` cần `XS102`+`DS103` | Suy luận nhiều tầng |
| **MSSV không tồn tại** | `9Z999999999` | Trả `LỖI:`, **không được bịa bảng điểm** |
| **Mã môn không tồn tại** | `ABC999` | Trả `LỖI:`, không được bịa môn |

Ba mức **thiếu 2 / thiếu 1 / đủ** là chỗ đắt nhất — cùng một câu hỏi, đổi MSSV là ra 3 kết quả khác nhau, chứng minh Agent thật sự tra dữ liệu chứ không đọc thuộc lòng.

---

## 4. Bộ tool khai thác schema này

| Tool | Tham số | Trả về |
| :-- | :-- | :-- |
| `get_student` | `mssv` | ngành, kỳ, môn đã học, sở thích, trình độ |
| `search_courses` | `tag_hoac_keyword` | danh sách mã môn + tên khớp |
| `get_course_detail` | `ma_mon` | tín chỉ, tiên quyết, giảng viên, lịch, chỗ trống |
| `check_eligibility` | `mssv, ma_mon` | đủ / thiếu môn nào / hết chỗ |
| `get_lecturer` *(thêm)* | `ma_gv` | tên, khoa, đánh giá, chuyên môn |
| `check_schedule_conflict` *(thêm)* | `ma_mon_1, ma_mon_2` | trùng lịch hay không |

4 tool đầu là lõi, 2 tool sau làm nếu dư thời gian.

---

## 5. Ba chuỗi demo

**Chuỗi A — 3 hop, dùng cho phần trình chiếu chính:**

> "Em là 2A202601203, kỳ này nên học môn gì?"
> `get_student[2A202601203]` → sở thích: AI, dữ liệu
> `search_courses[AI]` → ML101, DL201, NLP301
> `check_eligibility[2A202601203, ML101]` → thiếu XS102, DS103
> **Final Answer**: nên học Xác suất thống kê và Đại số tuyến tính trước

**Chuỗi B — 2 hop, kiểm tra lớp hết chỗ:**

> "Em muốn học Deep Learning kỳ này"
> `search_courses[Deep Learning]` → DL201
> `get_course_detail[DL201]` → 30/30 hết chỗ, cần ML101
> **Final Answer**: lớp đã đầy và bạn chưa học ML101

**Chuỗi C — câu bẫy, phải chạm Guardrail:**

> "Em là 9Z999999999, cho em xem bảng điểm và đăng ký môn Ảo Thuật Nâng Cao"
> `get_student[9Z999999999]` → `LỖI: Không tìm thấy sinh viên`
> `search_courses[Ảo Thuật Nâng Cao]` → `LỖI: Không tìm thấy môn`
> **Final Answer**: xin lỗi lịch sự, **tuyệt đối không bịa dữ liệu**

---

## 6. Hai lưu ý thiết kế

**Dùng mã môn làm khóa, không dùng tên môn.** `da_hoc` và `tien_quyet` đều lưu mã (`XS102`), không lưu tên. Nếu lưu tên thì chỉ cần lệch một dấu hoặc chữ hoa/thường ("Xác suất thống kê" vs "Xác suất Thống kê") là so sánh sai, mà lỗi kiểu này rất khó nhìn ra lúc chạy. Khi in ra cho người dùng thì tra `COURSES[ma]["ten"]`.

**Gộp "lớp" vào "khóa học".** Mỗi môn chỉ có một ca học duy nhất (`lich`). Tách riêng bảng lớp/ca học thì đúng về mặt CSDL nhưng tốn thời gian mà không thêm điểm nào trong rubric — Mốc 2 chỉ có 30 phút.

---

## ⚠️ 7. Việc phải chốt với Role 3 trước khi code

Chuỗi A cần **4 vòng lặp** (3 lần gọi tool + 1 lần chốt Final Answer), nhưng `MAX_ITERATIONS` hiện đang để **3** trong `src/prompts.py`.

Nghĩa là demo đẹp nhất của nhóm sẽ chết ở Guardrail thay vì ra Final Answer.

👉 Đề nghị Role 3 nâng `MAX_ITERATIONS = 5`, và Role 1 thiết kế câu bẫy cần ≥6 vòng để Guardrail vẫn có đất diễn.
