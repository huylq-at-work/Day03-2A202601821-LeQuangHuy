# MOCK DATABASE SCHEMA — Trợ Lý Đăng Ký Khóa Học (Marketplace)

> Bản thiết kế cho **Role 2 (Tool Engineer)**.
>  Dữ liệu thật: **[`config/mock_database.json`](../config/mock_database.json)** — file này giải thích cấu trúc.

**Bối cảnh**: marketplace khóa học bên ngoài — có cả khóa **online tự học** lẫn **lớp offline tại trung tâm**, nhiều nhà cung cấp. Học viên định danh bằng **số điện thoại**.

**Quy mô**: 1000 học viên · 13 khóa học · 5 nhà cung cấp · 6 giảng viên (~268 KB).

>  Đây **không phải** hệ thống đăng ký môn của trường. Không có `mssv`, `ngành`, `kỳ học`, `môn tiên quyết`. Trục suy luận là **ngân sách + lịch rảnh + trình độ + khu vực + hình thức**.

---

## 1. Cách load trong `src/tools.py`

```python
import json, os

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(_BASE, "config", "mock_database.json"), "r", encoding="utf-8") as f:
    _DB = json.load(f)

LEARNERS    = _DB["learners"]
COURSES     = _DB["courses"]
PROVIDERS   = _DB["providers"]
INSTRUCTORS = _DB["instructors"]

CAP_DO = _DB["_meta"]["cap_do"]                    # thứ tự trình độ, dùng để so sánh
NGAY_HIEN_TAI = _DB["_meta"]["ngay_hien_tai"]      # "2026-07-28"
```

>  Dùng `NGAY_HIEN_TAI` từ file, **đừng dùng `datetime.now()`**. Ngày cố định thì test case của Role 1 chạy lúc nào cũng ra kết quả giống nhau — bẫy "hết hạn đăng ký" mới tái lập được.

---

## 2. Cấu trúc 4 bảng

```
learners                      courses                     providers
────────                      ───────                     ─────────
<sdt> (khóa)                  <ma_khoa> (khóa)            <ma_ncc> (khóa)
  ho_ten                        ten                         ten
  muc_tieu[] ──────────┐        ma_ncc ───────────────────► loai
  trinh_do ─────────┐  │        chu_de[] ◄──────────────┘   khu_vuc
  ngan_sach ─────┐  │  └─────►  trinh_do_yeu_cau ◄──────┘   danh_gia
  lich_ranh[] ─┐ │  └────────►  hinh_thuc
  khu_vuc ───┐ │ └───────────►  gia                       instructors
  hinh_thuc_ │ │                thoi_luong                ───────────
    uu_tien  │ └─────────────►  lich_hoc[]                <ma_gv> (khóa)
  da_hoc[]   └───────────────►  dia_diem                    ten
                                khai_giang / han_dang_ky    chuyen_mon[]
                                si_so / da_dang_ky          danh_gia
                                rating / chung_chi          kinh_nghiem
                                ma_gv ────────────────────► (khóa ngoại)
```

### `learners` — học viên

| Trường | Kiểu | Ghi chú |
| :-- | :-- | :-- |
| *(khóa)* | string | Số điện thoại, dạng `0912345203` |
| `ho_ten` | string | |
| `muc_tieu` | array\<string\> | **nối** với `courses.chu_de` |
| `trinh_do` | string | 1 trong `_meta.cap_do` |
| `ngan_sach` | int | VNĐ |
| `lich_ranh` | array\<string\> | dạng `"T2 tối"`, `"CN sáng"` |
| `khu_vuc` | string | Hà Nội / TP.HCM / … |
| `hinh_thuc_uu_tien` | string | `online` / `offline` / `cả hai` |
| `da_hoc` | array\<ma_khoa\> | khóa đã hoàn thành |

### `courses` — khóa học

| Trường | Kiểu | Ghi chú |
| :-- | :-- | :-- |
| *(khóa)* | string | `EN101`, `PR201`, … |
| `ten` | string | |
| `ma_ncc` | string | **khóa ngoại**  `providers` |
| `chu_de` | array\<string\> | **nối** với `learners.muc_tieu` |
| `trinh_do_yeu_cau` | string | trình độ đầu vào tối thiểu |
| `hinh_thuc` | string | `online` / `offline` |
| `gia` | int | VNĐ |
| `thoi_luong` | string | `"24 buổi"` (offline) / `"30 giờ"` (online) |
| `lich_hoc` | array\<string\> | `"T2 19:00-21:00"`. **Rỗng `[]` với khóa online** |
| `khai_giang`, `han_dang_ky` | string \| null | `YYYY-MM-DD`. **null với khóa online** |
| `dia_diem` | string \| null | **null với khóa online** |
| `si_so` | int \| **null** | **`null` = online, không giới hạn chỗ** |
| `da_dang_ky` | int | |
| `rating` | float | thang 5.0 |
| `chung_chi` | bool | có cấp chứng chỉ không |
| `ma_gv` | string | **khóa ngoại**  `instructors` |

### Ba đường nối quan trọng nhất

| Nối | Cho phép chuỗi suy luận |
| :-- | :-- |
| `learners.muc_tieu`  `courses.chu_de` | Biết mục tiêu  lọc ra khóa phù hợp |
| `learners.ngan_sach` + `lich_ranh` + `trinh_do` + `khu_vuc`  `courses.*` | Lọc 5 chiều  tìm khóa khả thi |
| `courses.ma_ncc`  `providers` | Biết khóa  tra uy tín trung tâm |

---

## 3. Quy tắc so khớp lịch

`lich_hoc` ghi giờ cụ thể, `lich_ranh` ghi buổi. Quy đổi bằng giờ bắt đầu:

| Giờ bắt đầu | Buổi |
| :-- | :-- |
| < 12:00 | sáng |
| 12:00 – 17:59 | chiều |
| ≥ 18:00 | tối |

Ví dụ: `"T2 19:00-21:00"`  `"T2 tối"`. Khóa khớp lịch khi **mọi buổi học** đều nằm trong `lich_ranh`.

---

## 4. Bẫy cài sẵn — đã kiểm chứng

Chạy thật trên dữ liệu, kết quả đúng như thiết kế:

| Học viên | Khóa | Kết quả |
| :-- | :-- | :-- |
| Hướng `0912345203` | `AI301` | **3 lỗi**: vượt ngân sách (15tr > 2tr), trình độ chưa đạt, lịch không khớp |
| Đạt `0987654387` | `EN101` | **1 lỗi**: lịch không khớp (T2/T4 tối vs rảnh T3/T5 tối) |
| Liên `0901234795` | `PR201` | **PHÙ HỢP** |
| Huy `0977888821` | `EN101` | **2 lỗi**: lịch không khớp + khác khu vực (HN vs TP.HCM) |
| Huy `0977888821` | `MK201` | **PHÙ HỢP** |
| Đạt `0987654387` | `EN201` | **3 lỗi**: vượt ngân sách, trình độ chưa đạt, **lớp đã đầy** (20/20) |
| Liên `0901234795` | `EN301` | **1 lỗi**: **hết hạn đăng ký** (2026-07-15 < 2026-07-28) |

Bẫy khác trong dữ liệu:

| Bẫy | Ở đâu |
| :-- | :-- |
| SĐT không tồn tại | `0000000000`  phải trả `LỖI:`, **không được bịa hồ sơ** |
| Mã khóa không tồn tại | `XYZ999`  phải trả `LỖI:` |
| `si_so = null` | Mọi khóa online — code không được crash khi so sánh với `None` |
| Khóa online không có lịch | `lich_hoc = []`  không được báo "lịch không khớp" |

>  Ba mức **3 lỗi / 1 lỗi / phù hợp** là chỗ đắt nhất: cùng một câu hỏi, đổi SĐT là ra kết quả khác hẳn — chứng minh Agent thật sự tra dữ liệu chứ không đọc thuộc lòng.

---

## 5. Bộ tool

| Tool | Tham số | Trả về |
| :-- | :-- | :-- |
| `get_learner` | `sdt` | mục tiêu, trình độ, ngân sách, lịch rảnh, khu vực |
| `search_courses` | `chu_de, gia_toi_da` | danh sách mã khóa + tên + giá khớp điều kiện |
| `get_course_detail` | `ma_khoa` | giá, trình độ, lịch, địa điểm, chỗ trống, hạn ĐK, rating |
| `check_suitability` | `sdt, ma_khoa` | **phù hợp / danh sách lý do trượt** |
| `get_provider` *(thêm)* | `ma_ncc` | tên, loại, khu vực, đánh giá |
| `compare_courses` *(thêm)* | `ma1, ma2` | so giá / thời lượng / rating / chứng chỉ |

### `check_suitability` — tool ăn điểm nhất

Kiểm đủ 5 chiều và **trả về lý do cụ thể**, không trả `True/False`:

```
ngân sách   gia <= ngan_sach
trình độ    cap_do.index(trinh_do) >= cap_do.index(trinh_do_yeu_cau)
lịch        mọi buổi trong lich_hoc phải thuộc lich_ranh     (bỏ qua nếu online)
khu vực     dia_diem == khu_vuc                              (bỏ qua nếu online)
chỗ + hạn   da_dang_ky < si_so, và han_dang_ky >= NGAY_HIEN_TAI  (bỏ qua nếu online)
```

Trả về nên có dạng:

> `Không phù hợp. Lý do: vượt ngân sách (15,000,000 > 2,000,000); trình độ chưa đạt (mới bắt đầu < trung cấp); lịch không khớp (T3 tối, T5 tối).`

Có lý do cụ thể thì Agent mới giải thích được cho người dùng — đó chính là chỗ Chatbot thường bó tay.

---

## 6. Ba chuỗi demo

**Chuỗi A — 3 hop, dùng trình chiếu chính:**

> "Em là 0912345203, em muốn học AI thì nên đăng ký khóa nào?"
> `get_learner[0912345203]`  mục tiêu AI, ngân sách 2tr, mới bắt đầu, rảnh T2/T4 tối
> `search_courses[AI, 2000000]`  AI302 (1.5tr, online, mới bắt đầu)
> `check_suitability[0912345203, AI302]`  phù hợp
> **Final Answer**: gợi ý AI302, giải thích vì sao AI301 không hợp

**Chuỗi B — 2 hop, so sánh:**

> "So sánh giúp em khóa PR201 và PR202"
> `compare_courses[PR201, PR202]`  12tr offline 48 buổi vs 2.5tr online 20 giờ
> `get_provider[TT02]`  CodeCamp Academy, 4.7
> **Final Answer**: tùy ngân sách và hình thức mong muốn

**Chuỗi C — câu bẫy, phải chạm Guardrail:**

> "Em là 0000000000, đăng ký giúp em khóa Thôi Miên Nâng Cao"
> `get_learner[0000000000]`  `LỖI: Không tìm thấy học viên`
> `search_courses[Thôi Miên Nâng Cao]`  `LỖI: Không tìm thấy khóa`
> **Final Answer**: xin lỗi lịch sự, **tuyệt đối không bịa dữ liệu**

---

## 7. Ba lưu ý thiết kế

**`si_so = null` nghĩa là không giới hạn.** Mọi khóa online đều vậy. Code phải kiểm `if si_so is not None` trước khi so sánh, không thì `None > int` văng `TypeError` ngay.

**Khóa online bỏ qua 3 chiều kiểm tra**: lịch, khu vực, chỗ + hạn. Chỉ còn ngân sách và trình độ. Quên điều này thì mọi khóa online đều bị báo "lịch không khớp".

**Dùng ngày cố định `_meta.ngay_hien_tai`**, không dùng `datetime.now()` — để bẫy hết hạn đăng ký luôn tái lập được.

---

## 8. Việc phải chốt với Role 3

Chuỗi A cần **4 vòng lặp** (3 lần gọi tool + 1 lần chốt Final Answer), nhưng `MAX_ITERATIONS` đang để **3** trong `src/prompts.py`  demo đẹp nhất sẽ chết ở Guardrail thay vì ra Final Answer.

 Role 3 nâng `MAX_ITERATIONS = 5`, Role 1 thiết kế câu bẫy cần ≥6 vòng để Guardrail vẫn có đất diễn.
