# 📖 SCHEMA RÚT GỌN CHO PROMPT ENGINEER (Role 3)

> File này **sinh tự động** từ [`config/mock_database.json`](../config/mock_database.json) — không chỉnh tay, dữ liệu đổi thì chạy lại script.
> Mục đích: để Role 3 viết ví dụ few-shot trong `REACT_SYSTEM_PROMPT` **dùng đúng dữ liệu có thật**.

**Quy mô**: 1,000 học viên · 128 khóa học · 8 nhà cung cấp · 12 giảng viên.  
**Ngày hệ thống (cố định)**: `2026-07-28`

---

## 1. Từ vựng dữ liệu — chỉ những giá trị này là hợp lệ

Viết ví dụ trong prompt thì phải dùng đúng các giá trị dưới đây, bịa giá trị lạ sẽ dạy LLM gọi tool sai.

| Khái niệm | Giá trị hợp lệ |
| :-- | :-- |
| **Trình độ** (có thứ tự) | `mới bắt đầu` < `cơ bản` < `trung cấp` < `nâng cao` |
| Trình độ học viên thực tế | `mới bắt đầu`, `cơ bản`, `trung cấp` |
| **Chủ đề khóa học** | `AI`, `IELTS`, `bảo mật`, `công việc`, `dữ liệu`, `giao tiếp`, `khoa học`, `kế toán`, `kỹ năng mềm`, `lập trình`, `marketing`, `mobile`, `ngoại ngữ`, `nhiếp ảnh`, `python`, `quản trị`, `thiết kế`, `tiếng Anh`, `tiếng Hàn`, `tiếng Nhật`, `tiếng Trung`, `toán`, `tài chính`, `vật lý`, `web`, `âm nhạc`, `đầu tư` |
| Mục tiêu học viên | `AI`, `IELTS`, `dữ liệu`, `lập trình`, `marketing`, `thiết kế`, `tiếng Anh`, `web` |
| **Khu vực** | `Cần Thơ`, `Hà Nội`, `Hải Phòng`, `TP.HCM`, `Đà Nẵng` |
| **Hình thức** | khóa học: `online` / `offline` · ưu tiên HV: `cả hai`, `offline`, `online` |
| **Buổi rảnh** | `T2`–`T7`, `CN` × `sáng` / `chiều` / `tối` (vd `CN chiều`) |
| **Ngân sách** | 500,000đ – 20,000,000đ |
| **Giá khóa** | 690,000đ – 15,000,000đ |

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
| `PH101` | Vật lý đại cương | vật lý, khoa học | mới bắt đầu | on | 1,200,000 | tự học | — | ∞ | — |
| `PH201` | Vật lý luyện thi THPT | vật lý, khoa học | cơ bản | of | 4,500,000 | T3 19:00-21:00, T5 19:00-21:00 | Hà Nội | 17/30 | 2026-08-30 |
| `MA101` | Toán cao cấp cơ bản | toán, khoa học | mới bắt đầu | on | 950,000 | tự học | — | ∞ | — |
| `MA201` | Toán tư duy cho lập trình | toán, lập trình | cơ bản | on | 1,700,000 | tự học | — | ∞ | — |
| `JP101` | Tiếng Nhật N5 | tiếng Nhật, ngoại ngữ | mới bắt đầu | of | 4,200,000 | T2 18:30-20:30, T4 18:30-20:30 | TP.HCM | 12/25 | 2026-09-01 |
| `JP102` | Tiếng Nhật giao tiếp online | tiếng Nhật, giao tiếp | mới bắt đầu | on | 1,350,000 | tự học | — | ∞ | — |
| `KR101` | Tiếng Hàn sơ cấp | tiếng Hàn, ngoại ngữ | mới bắt đầu | of | 3,900,000 | T3 18:30-20:30, T5 18:30-20:30 | TP.HCM | 20/25 | 2026-09-01 |
| `FI101` | Quản lý tài chính cá nhân | tài chính | mới bắt đầu | on | 790,000 | tự học | — | ∞ | — |
| `FI201` | Đầu tư chứng khoán cơ bản | tài chính, đầu tư | cơ bản | on | 2,300,000 | tự học | — | ∞ | — |
| `AC101` | Kế toán cho người mới | kế toán | mới bắt đầu | on | 1,600,000 | tự học | — | ∞ | — |
| `PT101` | Nhiếp ảnh cơ bản với điện thoại | nhiếp ảnh | mới bắt đầu | on | 690,000 | tự học | — | ∞ | — |
| `UX201` | Thiết kế UI/UX | thiết kế, web | cơ bản | on | 3,200,000 | tự học | — | ∞ | — |
| `MU101` | Guitar đệm hát cho người mới | âm nhạc | mới bắt đầu | of | 2,800,000 | T7 09:00-11:00, CN 09:00-11:00 | Hà Nội | 11/20 | 2026-08-24 |
| `SK101` | Kỹ năng thuyết trình | kỹ năng mềm | mới bắt đầu | on | 1,100,000 | tự học | — | ∞ | — |
| `SK201` | Quản trị dự án cho người đi làm | kỹ năng mềm, quản trị | cơ bản | of | 7,500,000 | T6 18:30-20:30, T7 09:00-11:00 | Hà Nội | 19/28 | 2026-09-05 |
| `ENX101` | Tiếng Anh nhập môn | tiếng Anh, ngoại ngữ | mới bắt đầu | of | 940,000 | T2 19:00-21:00, T4 19:00-21:00 | TP.HCM | 26/36 | 2026-09-09 |
| `ENX102` | Tiếng Anh cơ bản | tiếng Anh, ngoại ngữ | mới bắt đầu | on | 1,720,000 | tự học | — | ∞ | — |
| `ENX103` | Tiếng Anh thực hành | tiếng Anh, ngoại ngữ | cơ bản | on | 2,100,000 | tự học | — | ∞ | — |
| `ENX104` | Tiếng Anh chuyên sâu | tiếng Anh, ngoại ngữ | trung cấp | of | 5,850,000 | T6 18:30-20:30, T7 09:00-11:00 | TP.HCM | 25/26 | 2026-09-06 |
| `ENX105` | Tiếng Anh nâng cao | tiếng Anh, ngoại ngữ | nâng cao | on | 11,350,000 | tự học | — | ∞ | — |
| `JPX101` | Tiếng Nhật nhập môn | tiếng Nhật, ngoại ngữ | mới bắt đầu | of | 1,290,000 | T2 18:00-20:00, T6 18:00-20:00 | TP.HCM | 22/24 | 2026-09-01 |
| `JPX102` | Tiếng Nhật cơ bản | tiếng Nhật, ngoại ngữ | mới bắt đầu | on | 880,000 | tự học | — | ∞ | — |
| `JPX103` | Tiếng Nhật thực hành | tiếng Nhật, ngoại ngữ | cơ bản | on | 2,390,000 | tự học | — | ∞ | — |
| `JPX104` | Tiếng Nhật chuyên sâu | tiếng Nhật, ngoại ngữ | trung cấp | of | 5,200,000 | T7 09:00-11:30, CN 09:00-11:30 | TP.HCM | 1/33 | 2026-09-09 |
| `JPX105` | Tiếng Nhật nâng cao | tiếng Nhật, ngoại ngữ | nâng cao | on | 12,860,000 | tự học | — | ∞ | — |
| `KRX101` | Tiếng Hàn nhập môn | tiếng Hàn, ngoại ngữ | mới bắt đầu | of | 1,590,000 | T3 19:00-21:00, T5 19:00-21:00 | TP.HCM | 21/24 | 2026-09-08 |
| `KRX102` | Tiếng Hàn cơ bản | tiếng Hàn, ngoại ngữ | mới bắt đầu | on | 1,220,000 | tự học | — | ∞ | — |
| `KRX103` | Tiếng Hàn thực hành | tiếng Hàn, ngoại ngữ | cơ bản | on | 2,860,000 | tự học | — | ∞ | — |
| `KRX104` | Tiếng Hàn chuyên sâu | tiếng Hàn, ngoại ngữ | trung cấp | of | 3,850,000 | T2 19:00-21:00, T4 19:00-21:00 | TP.HCM | 25/28 | 2026-09-08 |
| `KRX105` | Tiếng Hàn nâng cao | tiếng Hàn, ngoại ngữ | nâng cao | on | 13,730,000 | tự học | — | ∞ | — |
| `ZHX101` | Tiếng Trung nhập môn | tiếng Trung, ngoại ngữ | mới bắt đầu | of | 1,730,000 | T2 19:00-21:00, T4 19:00-21:00 | TP.HCM | 29/37 | 2026-09-06 |
| `ZHX102` | Tiếng Trung cơ bản | tiếng Trung, ngoại ngữ | mới bắt đầu | on | 1,770,000 | tự học | — | ∞ | — |
| `ZHX103` | Tiếng Trung thực hành | tiếng Trung, ngoại ngữ | cơ bản | on | 2,500,000 | tự học | — | ∞ | — |
| `ZHX104` | Tiếng Trung chuyên sâu | tiếng Trung, ngoại ngữ | trung cấp | of | 3,820,000 | T2 19:00-21:00, T4 19:00-21:00 | TP.HCM | 14/24 | 2026-09-01 |
| `ZHX105` | Tiếng Trung nâng cao | tiếng Trung, ngoại ngữ | nâng cao | on | 6,700,000 | tự học | — | ∞ | — |
| `PRX101` | Lập trình Python nhập môn | lập trình, python | mới bắt đầu | of | 1,250,000 | T6 18:30-20:30, T7 09:00-11:00 | TP.HCM | 22/24 | 2026-09-08 |
| `PRX102` | Lập trình Python cơ bản | lập trình, python | mới bắt đầu | on | 1,160,000 | tự học | — | ∞ | — |
| `PRX103` | Lập trình Python thực hành | lập trình, python | cơ bản | on | 2,560,000 | tự học | — | ∞ | — |
| `PRX104` | Lập trình Python chuyên sâu | lập trình, python | trung cấp | of | 6,290,000 | T7 09:00-11:30, CN 09:00-11:30 | Hà Nội | 16/29 | 2026-09-03 |
| `PRX105` | Lập trình Python nâng cao | lập trình, python | nâng cao | on | 6,890,000 | tự học | — | ∞ | — |
| `WBX101` | Lập trình Web nhập môn | web, lập trình | mới bắt đầu | of | 1,430,000 | T7 09:00-11:30, CN 09:00-11:30 | Hà Nội | 14/20 | 2026-09-05 |
| `WBX102` | Lập trình Web cơ bản | web, lập trình | mới bắt đầu | on | 1,670,000 | tự học | — | ∞ | — |
| `WBX103` | Lập trình Web thực hành | web, lập trình | cơ bản | on | 2,410,000 | tự học | — | ∞ | — |
| `WBX104` | Lập trình Web chuyên sâu | web, lập trình | trung cấp | of | 3,290,000 | T3 19:00-21:00, T5 19:00-21:00 | Hà Nội | 3/32 | 2026-09-01 |
| `WBX105` | Lập trình Web nâng cao | web, lập trình | nâng cao | on | 7,580,000 | tự học | — | ∞ | — |
| `MBX101` | Lập trình Mobile nhập môn | mobile, lập trình | mới bắt đầu | of | 1,150,000 | T3 19:00-21:00, T5 19:00-21:00 | Hà Nội | 13/24 | 2026-09-05 |
| `MBX102` | Lập trình Mobile cơ bản | mobile, lập trình | mới bắt đầu | on | 1,490,000 | tự học | — | ∞ | — |
| `MBX103` | Lập trình Mobile thực hành | mobile, lập trình | cơ bản | on | 3,140,000 | tự học | — | ∞ | — |
| `MBX104` | Lập trình Mobile chuyên sâu | mobile, lập trình | trung cấp | of | 4,860,000 | T6 18:30-20:30, T7 09:00-11:00 | Hà Nội | 14/36 | 2026-09-04 |
| `MBX105` | Lập trình Mobile nâng cao | mobile, lập trình | nâng cao | on | 9,810,000 | tự học | — | ∞ | — |
| `AIX101` | Trí tuệ nhân tạo nhập môn | AI, dữ liệu | mới bắt đầu | of | 1,070,000 | T6 18:30-20:30, T7 09:00-11:00 | Hà Nội | 13/31 | 2026-09-09 |
| `AIX102` | Trí tuệ nhân tạo cơ bản | AI, dữ liệu | mới bắt đầu | on | 1,140,000 | tự học | — | ∞ | — |
| `AIX103` | Trí tuệ nhân tạo thực hành | AI, dữ liệu | cơ bản | on | 1,710,000 | tự học | — | ∞ | — |
| `AIX104` | Trí tuệ nhân tạo chuyên sâu | AI, dữ liệu | trung cấp | of | 6,180,000 | T2 19:00-21:00, T4 19:00-21:00 | TP.HCM | 8/25 | 2026-09-06 |
| `AIX105` | Trí tuệ nhân tạo nâng cao | AI, dữ liệu | nâng cao | on | 13,820,000 | tự học | — | ∞ | — |
| `DAX101` | Phân tích dữ liệu nhập môn | dữ liệu | mới bắt đầu | of | 1,230,000 | T2 19:00-21:00, T4 19:00-21:00 | TP.HCM | 9/20 | 2026-09-01 |
| `DAX102` | Phân tích dữ liệu cơ bản | dữ liệu | mới bắt đầu | on | 1,420,000 | tự học | — | ∞ | — |
| `DAX103` | Phân tích dữ liệu thực hành | dữ liệu | cơ bản | on | 2,790,000 | tự học | — | ∞ | — |
| `DAX104` | Phân tích dữ liệu chuyên sâu | dữ liệu | trung cấp | of | 4,940,000 | T6 18:30-20:30, T7 09:00-11:00 | TP.HCM | 12/23 | 2026-09-05 |
| `DAX105` | Phân tích dữ liệu nâng cao | dữ liệu | nâng cao | on | 6,480,000 | tự học | — | ∞ | — |
| `SCX101` | An toàn thông tin nhập môn | bảo mật | mới bắt đầu | of | 1,380,000 | T7 09:00-11:30, CN 09:00-11:30 | TP.HCM | 17/23 | 2026-09-01 |
| `SCX102` | An toàn thông tin cơ bản | bảo mật | mới bắt đầu | on | 810,000 | tự học | — | ∞ | — |
| `SCX103` | An toàn thông tin thực hành | bảo mật | cơ bản | on | 1,760,000 | tự học | — | ∞ | — |
| `SCX104` | An toàn thông tin chuyên sâu | bảo mật | trung cấp | of | 3,120,000 | T6 18:30-20:30, T7 09:00-11:00 | TP.HCM | 24/38 | 2026-09-07 |
| `SCX105` | An toàn thông tin nâng cao | bảo mật | nâng cao | on | 7,840,000 | tự học | — | ∞ | — |
| `DGX101` | Thiết kế đồ họa nhập môn | thiết kế | mới bắt đầu | of | 1,520,000 | T2 19:00-21:00, T4 19:00-21:00 | TP.HCM | 17/24 | 2026-09-05 |
| `DGX102` | Thiết kế đồ họa cơ bản | thiết kế | mới bắt đầu | on | 1,350,000 | tự học | — | ∞ | — |
| `DGX103` | Thiết kế đồ họa thực hành | thiết kế | cơ bản | on | 2,660,000 | tự học | — | ∞ | — |
| `DGX104` | Thiết kế đồ họa chuyên sâu | thiết kế | trung cấp | of | 5,180,000 | T2 19:00-21:00, T4 19:00-21:00 | TP.HCM | 1/21 | 2026-09-08 |
| `DGX105` | Thiết kế đồ họa nâng cao | thiết kế | nâng cao | on | 13,230,000 | tự học | — | ∞ | — |
| `PTX101` | Nhiếp ảnh nhập môn | nhiếp ảnh | mới bắt đầu | of | 1,180,000 | T3 19:00-21:00, T5 19:00-21:00 | Hà Nội | 14/28 | 2026-09-06 |
| `PTX102` | Nhiếp ảnh cơ bản | nhiếp ảnh | mới bắt đầu | on | 1,680,000 | tự học | — | ∞ | — |
| `PTX103` | Nhiếp ảnh thực hành | nhiếp ảnh | cơ bản | on | 1,820,000 | tự học | — | ∞ | — |
| `PTX104` | Nhiếp ảnh chuyên sâu | nhiếp ảnh | trung cấp | of | 6,500,000 | T3 19:00-21:00, T5 19:00-21:00 | Hà Nội | 23/33 | 2026-09-05 |
| `PTX105` | Nhiếp ảnh nâng cao | nhiếp ảnh | nâng cao | on | 12,000,000 | tự học | — | ∞ | — |
| `MKX101` | Digital Marketing nhập môn | marketing | mới bắt đầu | of | 1,330,000 | T7 09:00-11:30, CN 09:00-11:30 | Hà Nội | 20/21 | 2026-09-09 |
| `MKX102` | Digital Marketing cơ bản | marketing | mới bắt đầu | on | 910,000 | tự học | — | ∞ | — |
| `MKX103` | Digital Marketing thực hành | marketing | cơ bản | on | 1,590,000 | tự học | — | ∞ | — |
| `MKX104` | Digital Marketing chuyên sâu | marketing | trung cấp | of | 4,230,000 | T6 18:30-20:30, T7 09:00-11:00 | TP.HCM | 12/37 | 2026-09-07 |
| `MKX105` | Digital Marketing nâng cao | marketing | nâng cao | on | 13,110,000 | tự học | — | ∞ | — |
| `FIX101` | Tài chính cá nhân nhập môn | tài chính | mới bắt đầu | of | 1,050,000 | T6 18:30-20:30, T7 09:00-11:00 | Hà Nội | 5/20 | 2026-09-03 |
| `FIX102` | Tài chính cá nhân cơ bản | tài chính | mới bắt đầu | on | 690,000 | tự học | — | ∞ | — |
| `FIX103` | Tài chính cá nhân thực hành | tài chính | cơ bản | on | 2,760,000 | tự học | — | ∞ | — |
| `FIX104` | Tài chính cá nhân chuyên sâu | tài chính | trung cấp | of | 3,450,000 | T2 18:00-20:00, T6 18:00-20:00 | Hà Nội | 22/32 | 2026-09-02 |
| `FIX105` | Tài chính cá nhân nâng cao | tài chính | nâng cao | on | 10,660,000 | tự học | — | ∞ | — |
| `ACX101` | Kế toán nhập môn | kế toán | mới bắt đầu | of | 1,410,000 | T2 19:00-21:00, T4 19:00-21:00 | Hà Nội | 8/22 | 2026-09-05 |
| `ACX102` | Kế toán cơ bản | kế toán | mới bắt đầu | on | 1,370,000 | tự học | — | ∞ | — |
| `ACX103` | Kế toán thực hành | kế toán | cơ bản | on | 3,020,000 | tự học | — | ∞ | — |
| `ACX104` | Kế toán chuyên sâu | kế toán | trung cấp | of | 6,380,000 | T6 18:30-20:30, T7 09:00-11:00 | TP.HCM | 26/27 | 2026-09-07 |
| `ACX105` | Kế toán nâng cao | kế toán | nâng cao | on | 7,300,000 | tự học | — | ∞ | — |
| `SKX101` | Kỹ năng mềm nhập môn | kỹ năng mềm | mới bắt đầu | of | 1,250,000 | T6 18:30-20:30, T7 09:00-11:00 | TP.HCM | 4/23 | 2026-09-05 |
| `SKX102` | Kỹ năng mềm cơ bản | kỹ năng mềm | mới bắt đầu | on | 1,390,000 | tự học | — | ∞ | — |
| `SKX103` | Kỹ năng mềm thực hành | kỹ năng mềm | cơ bản | on | 2,830,000 | tự học | — | ∞ | — |
| `SKX104` | Kỹ năng mềm chuyên sâu | kỹ năng mềm | trung cấp | of | 4,720,000 | T7 09:00-11:30, CN 09:00-11:30 | TP.HCM | 6/23 | 2026-09-09 |
| `SKX105` | Kỹ năng mềm nâng cao | kỹ năng mềm | nâng cao | on | 6,500,000 | tự học | — | ∞ | — |
| `PMX101` | Quản trị dự án nhập môn | quản trị, kỹ năng mềm | mới bắt đầu | of | 1,220,000 | T2 18:00-20:00, T6 18:00-20:00 | Hà Nội | 27/30 | 2026-09-08 |
| `PMX102` | Quản trị dự án cơ bản | quản trị, kỹ năng mềm | mới bắt đầu | on | 770,000 | tự học | — | ∞ | — |
| `PMX103` | Quản trị dự án thực hành | quản trị, kỹ năng mềm | cơ bản | on | 2,180,000 | tự học | — | ∞ | — |
| `PMX104` | Quản trị dự án chuyên sâu | quản trị, kỹ năng mềm | trung cấp | of | 5,610,000 | T3 19:00-21:00, T5 19:00-21:00 | TP.HCM | 3/22 | 2026-09-01 |
| `PMX105` | Quản trị dự án nâng cao | quản trị, kỹ năng mềm | nâng cao | on | 13,910,000 | tự học | — | ∞ | — |
| `PHX101` | Vật lý nhập môn | vật lý, khoa học | mới bắt đầu | of | 870,000 | T2 18:00-20:00, T6 18:00-20:00 | Hà Nội | 8/33 | 2026-09-09 |
| `PHX102` | Vật lý cơ bản | vật lý, khoa học | mới bắt đầu | on | 1,570,000 | tự học | — | ∞ | — |
| `PHX103` | Vật lý thực hành | vật lý, khoa học | cơ bản | on | 3,480,000 | tự học | — | ∞ | — |
| `PHX104` | Vật lý chuyên sâu | vật lý, khoa học | trung cấp | of | 5,540,000 | T6 18:30-20:30, T7 09:00-11:00 | TP.HCM | 20/28 | 2026-09-01 |
| `PHX105` | Vật lý nâng cao | vật lý, khoa học | nâng cao | on | 12,790,000 | tự học | — | ∞ | — |
| `MAX101` | Toán học nhập môn | toán, khoa học | mới bắt đầu | of | 1,530,000 | T2 19:00-21:00, T4 19:00-21:00 | TP.HCM | 23/26 | 2026-09-02 |
| `MAX102` | Toán học cơ bản | toán, khoa học | mới bắt đầu | on | 1,320,000 | tự học | — | ∞ | — |
| `MAX103` | Toán học thực hành | toán, khoa học | cơ bản | on | 2,750,000 | tự học | — | ∞ | — |
| `MAX104` | Toán học chuyên sâu | toán, khoa học | trung cấp | of | 3,330,000 | T6 18:30-20:30, T7 09:00-11:00 | Hà Nội | 12/25 | 2026-09-09 |
| `MAX105` | Toán học nâng cao | toán, khoa học | nâng cao | on | 7,800,000 | tự học | — | ∞ | — |
| `MUX101` | Âm nhạc nhập môn | âm nhạc | mới bắt đầu | of | 1,790,000 | T6 18:30-20:30, T7 09:00-11:00 | Hà Nội | 35/36 | 2026-09-03 |
| `MUX102` | Âm nhạc cơ bản | âm nhạc | mới bắt đầu | on | 1,450,000 | tự học | — | ∞ | — |
| `MUX103` | Âm nhạc thực hành | âm nhạc | cơ bản | on | 1,820,000 | tự học | — | ∞ | — |
| `MUX104` | Âm nhạc chuyên sâu | âm nhạc | trung cấp | of | 3,550,000 | T2 19:00-21:00, T4 19:00-21:00 | Hà Nội | 5/21 | 2026-09-05 |
| `MUX105` | Âm nhạc nâng cao | âm nhạc | nâng cao | on | 11,810,000 | tự học | — | ∞ | — |

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
AIX101 - Trí tuệ nhân tạo nhập môn - 1,070,000đ - offline - mới bắt đầu
AIX102 - Trí tuệ nhân tạo cơ bản - 1,140,000đ - online - mới bắt đầu
AIX103 - Trí tuệ nhân tạo thực hành - 1,710,000đ - online - cơ bản
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
