# 📖 SCHEMA RÚT GỌN CHO PROMPT ENGINEER (Role 3)

> File này **sinh tự động** từ [`config/mock_database.json`](../config/mock_database.json) — không chỉnh tay, dữ liệu đổi thì chạy lại script.
> Mục đích: để Role 3 viết ví dụ few-shot trong `REACT_SYSTEM_PROMPT` **dùng đúng dữ liệu có thật**.

**Quy mô**: 1,000 học viên · 13 khóa học · 5 nhà cung cấp · 6 giảng viên.  
**Ngày hệ thống (cố định)**: `2026-07-28`

---

## 1. Từ vựng dữ liệu — chỉ những giá trị này là hợp lệ

Viết ví dụ trong prompt thì phải dùng đúng các giá trị dưới đây, bịa giá trị lạ sẽ dạy LLM gọi tool sai.

| Khái niệm | Giá trị hợp lệ |
| :-- | :-- |
| **Trình độ** (có thứ tự) | `mới bắt đầu` < `cơ bản` < `trung cấp` < `nâng cao` |
| Trình độ học viên thực tế | `mới bắt đầu`, `cơ bản`, `trung cấp` |
| **Chủ đề khóa học** | `AI`, `IELTS`, `công việc`, `dữ liệu`, `giao tiếp`, `lập trình`, `marketing`, `python`, `thiết kế`, `tiếng Anh`, `web` |
| Mục tiêu học viên | `AI`, `IELTS`, `dữ liệu`, `lập trình`, `marketing`, `thiết kế`, `tiếng Anh`, `web` |
| **Khu vực** | `Cần Thơ`, `Hà Nội`, `Hải Phòng`, `TP.HCM`, `Đà Nẵng` |
| **Hình thức** | khóa học: `online` / `offline` · ưu tiên HV: `cả hai`, `offline`, `online` |
| **Buổi rảnh** | `T2`–`T7`, `CN` × `sáng` / `chiều` / `tối` (vd `CN chiều`) |
| **Ngân sách** | 500,000đ – 20,000,000đ |
| **Giá khóa** | 890,000đ – 15,000,000đ |

---

## 2. Toàn bộ 13 khóa học

Dùng bảng này để viết ví dụ — mọi mã khóa, giá, lịch đều có thật.

| Mã | Tên | Chủ đề | Trình độ | HT | Giá | Lịch | Nơi | Chỗ | Hạn ĐK |
| :-- | :-- | :-- | :-- | :-: | --: | :-- | :-- | :-: | :-- |
| `EN101` | Tiếng Anh giao tiếp cơ bản | tiếng Anh, giao tiếp | mới bắt đầu | of | 3,500,000 | T2 19:00-21:00, T4 19:00-21:00 | Hà Nội | 18/25 | 2026-08-10 |
| `EN201` ⛔ | IELTS 6.5 cấp tốc | tiếng Anh, IELTS | trung cấp | of | 8,000,000 | T3 19:00-21:00, T5 19:00-21:00 | Hà Nội | 20/20 | 2026-08-15 |
| `EN301` ⏰ | Tiếng Anh thương mại | tiếng Anh, công việc | trung cấp | of | 5,000,000 | T2 19:00-21:00, T4 19:00-21:00 | Hà Nội | 14/20 | 2026-07-15 |
| `EN102` | Tiếng Anh giao tiếp online | tiếng Anh, giao tiếp | mới bắt đầu | on | 1,200,000 | tự học | — | ∞ | — |
| `PR101` | Nhập môn lập trình Python | lập trình, python | mới bắt đầu | on | 990,000 | tự học | — | ∞ | — |
| `PR201` | Lập trình Web Fullstack | lập trình, web | cơ bản | of | 12,000,000 | T2 19:00-21:30, T4 19:00-21:30, T6 19:00-21:30 | Hà Nội | 22/30 | 2026-08-25 |
| `PR202` | React nâng cao | lập trình, web | trung cấp | on | 2,500,000 | tự học | — | ∞ | — |
| `AI301` | Machine Learning thực chiến | AI, dữ liệu | trung cấp | of | 15,000,000 | T3 19:00-21:00, T5 19:00-21:00 | Hà Nội | 9/25 | 2026-08-18 |
| `AI302` | AI cho người mới bắt đầu | AI | mới bắt đầu | on | 1,500,000 | tự học | — | ∞ | — |
| `DA201` | Phân tích dữ liệu với Excel & SQL | dữ liệu | cơ bản | on | 1,800,000 | tự học | — | ∞ | — |
| `DE101` | Thiết kế đồ họa Canva & Figma | thiết kế | mới bắt đầu | on | 1,100,000 | tự học | — | ∞ | — |
| `MK101` | Content Marketing cơ bản | marketing | mới bắt đầu | on | 890,000 | tự học | — | ∞ | — |
| `MK201` | Digital Marketing tổng quan | marketing | cơ bản | of | 6,000,000 | T7 09:00-11:30, CN 09:00-11:30 | TP.HCM | 31/35 | 2026-08-17 |

⛔ = lớp đã đầy · ⏰ = hết hạn đăng ký · ∞ = online không giới hạn chỗ

---

## 3. Bốn học viên dùng để viết ví dụ

| SĐT | Họ tên | Mục tiêu | Trình độ | Ngân sách | Rảnh | Khu vực |
| :-- | :-- | :-- | :-- | --: | :-- | :-- |
| `0912345203` | Nguyễn Chí Hướng | AI, dữ liệu | mới bắt đầu | 2,000,000 | T2 tối, T4 tối | Hà Nội |
| `0987654387` | Nguyễn Tiến Đạt | tiếng Anh | cơ bản | 6,000,000 | T3 tối, T5 tối | Hà Nội |
| `0901234795` | Phạm Thị Liên | lập trình, web | trung cấp | 15,000,000 | T2 tối, T4 tối, T6 tối | Hà Nội |
| `0977888821` | Lê Quang Huy | marketing | cơ bản | 8,000,000 | T7 sáng, CN sáng | TP.HCM |

996 học viên còn lại sinh ngẫu nhiên (seed cố định). 4 người trên là dữ liệu cố định, mọi bẫy đều dựa vào họ.

---

## 4. Cấu trúc JSON — bản rút gọn

```json
{
  "_meta": {
    "ngay_hien_tai": "2026-07-28",
    "cap_do": [
      "mới bắt đầu",
      "cơ bản",
      "trung cấp",
      "nâng cao"
    ],
    "ghi_chu": "si_so = null nghia la khoa online khong gioi han cho"
  },
  "learners": {
    "0912345203": {
      "ho_ten": "Nguyễn Chí Hướng",
      "muc_tieu": [
        "AI",
        "dữ liệu"
      ],
      "trinh_do": "mới bắt đầu",
      "ngan_sach": 2000000,
      "lich_ranh": [
        "T2 tối",
        "T4 tối"
      ],
      "khu_vuc": "Hà Nội",
      "hinh_thuc_uu_tien": "cả hai",
      "da_hoc": []
    }
  },
  "courses": {
    "AI302": {
      "ten": "AI cho người mới bắt đầu",
      "ma_ncc": "NT01",
      "chu_de": [
        "AI"
      ],
      "trinh_do_yeu_cau": "mới bắt đầu",
      "hinh_thuc": "online",
      "gia": 1500000,
      "thoi_luong": "18 giờ",
      "lich_hoc": [],
      "khai_giang": null,
      "han_dang_ky": null,
      "dia_diem": null,
      "si_so": null,
      "da_dang_ky": 2050,
      "rating": 4.2,
      "chung_chi": true,
      "ma_gv": "GV03"
    },
    "AI301": {
      "ten": "Machine Learning thực chiến",
      "ma_ncc": "TT02",
      "chu_de": [
        "AI",
        "dữ liệu"
      ],
      "trinh_do_yeu_cau": "trung cấp",
      "hinh_thuc": "offline",
      "gia": 15000000,
      "thoi_luong": "40 buổi",
      "lich_hoc": [
        "T3 19:00-21:00",
        "T5 19:00-21:00"
      ],
      "khai_giang": "2026-08-25",
      "han_dang_ky": "2026-08-18",
      "dia_diem": "Hà Nội",
      "si_so": 25,
      "da_dang_ky": 9,
      "rating": 4.9,
      "chung_chi": true,
      "ma_gv": "GV03"
    }
  },
  "providers": {
    "TT02": {
      "ten": "CodeCamp Academy",
      "loai": "trung tâm offline",
      "khu_vuc": "Hà Nội",
      "danh_gia": 4.7
    }
  },
  "instructors": {
    "GV03": {
      "ten": "Lê Thanh Hà",
      "chuyen_mon": [
        "AI",
        "Machine Learning"
      ],
      "danh_gia": 4.9,
      "kinh_nghiem": 10
    }
  }
}
```

> ⚠️ Khóa **online** có `lich_hoc: []`, `khai_giang/han_dang_ky/dia_diem: null`, `si_so: null` (không giới hạn chỗ). Khóa **offline** thì đủ cả.

---

## 5. Observation sẽ trông như thế nào

Đây là phần quan trọng nhất với Role 3: ví dụ few-shot trong prompt phải khớp với chuỗi mà tool thật sự trả về, nếu không LLM sẽ học sai định dạng.

**`get_learner[0912345203]`**

```
Nguyễn Chí Hướng — mục tiêu: AI, dữ liệu; trình độ: mới bắt đầu; ngân sách: 2,000,000đ; rảnh: T2 tối, T4 tối; khu vực: Hà Nội.
```

**`search_courses[AI, 2000000]`**

```
AI302 - AI cho người mới bắt đầu - 1,500,000đ - online - mới bắt đầu
```

**`get_course_detail[AI301]`**

```
Machine Learning thực chiến (15,000,000đ) — offline, 40 buổi, trình độ trung cấp. Lịch: T3 19:00-21:00, T5 19:00-21:00 tại Hà Nội. Còn 16/25 chỗ, hạn đăng ký 2026-08-18. Rating 4.9.
```

**`check_suitability[0912345203, AI302]`** — trường hợp phù hợp

```
Phù hợp.
```

**`check_suitability[0912345203, AI301]`** — trường hợp trượt

```
Không phù hợp. Lý do: vượt ngân sách (15,000,000 > 2,000,000); trình độ chưa đạt (mới bắt đầu < trung cấp); lịch không khớp (T3 tối, T5 tối).
```

**`get_learner[0000000000]`** — trường hợp lỗi

```
LỖI: Không tìm thấy học viên có số điện thoại '0000000000'.
```

> 🔑 Mọi lỗi đều bắt đầu bằng `LỖI:`. Prompt phải dạy LLM: gặp `LỖI:` thì **dừng và báo lịch sự**, tuyệt đối không đoán hay bịa dữ liệu thay thế.

---

## 6. Bảy kết quả `check_suitability` đã kiểm chứng

| SĐT | Khóa | Kết quả |
| :-- | :-- | :-- |
| `0912345203` | `AI301` | 3 lỗi: ngân sách, trình độ, lịch |
| `0987654387` | `EN101` | 1 lỗi: lịch |
| `0901234795` | `PR201` | **PHÙ HỢP** |
| `0977888821` | `EN101` | 2 lỗi: lịch, khu vực |
| `0977888821` | `MK201` | **PHÙ HỢP** |
| `0987654387` | `EN201` | 3 lỗi: ngân sách, trình độ, lớp đầy |
| `0901234795` | `EN301` | 1 lỗi: hết hạn đăng ký |

Dùng những cặp này để viết ví dụ trong prompt — chắc chắn đúng với dữ liệu.
