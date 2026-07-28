# Hướng dẫn cài đặt và chạy

Trợ Lý Đăng Ký Khóa Học — Chatbot vs ReAct Agent.
Marketplace khóa học bên ngoài: 1000 học viên, 128 khóa, 8 tool, học viên định danh bằng số điện thoại.

---

## 1. Cài đặt

Cần Python 3.10 trở lên.

```bash
git clone git@github.com:huylq-at-work/Day03-2A202601821-LeQuangHuy.git
cd Day03-2A202601821-LeQuangHuy
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Trên macOS/Linux thay `.venv\Scripts\python.exe` bằng `.venv/bin/python` ở mọi lệnh phía dưới.

## 2. Cấu hình API key

```bash
copy .env.example .env
```

Mở `.env` và điền key của một nhà cung cấp. Gemini có bản miễn phí tại
[aistudio.google.com](https://aistudio.google.com/app/apikey):

```
LLM_PROVIDER=gemini
GEMINI_API_KEY=AIza...
LLM_MODEL=gemini-2.5-flash
```

Hoặc OpenAI:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
LLM_MODEL=gpt-4o-mini
```

Key Gemini bắt đầu bằng `AIza` và dài khoảng 39 ký tự. Key bắt đầu bằng `sk-` là của OpenAI —
điền nhầm ô sẽ báo `API_KEY_INVALID`.

Không có key thì chương trình vẫn chạy bằng `MockProvider`, nhưng đó là máy trạng thái
mô phỏng chứ không phải LLM thật, chỉ dùng để thử giao diện.

`.env` đã nằm trong `.gitignore`, không bao giờ được commit.

## 3. Bốn lệnh chính

| Việc | Lệnh |
| :-- | :-- |
| Chạy 1 test case trên terminal | `.venv\Scripts\python.exe src\app.py 3` |
| Chạy cả 5 test case | `.venv\Scripts\python.exe src\app.py all` |
| Demo Agent Cấp 4 (Planning + Memory) | `.venv\Scripts\python.exe src\app.py auto` |
| Mở giao diện chat | `.venv\Scripts\python.exe src\web_ui.py` rồi vào http://localhost:8765 |

Giao diện chat có 3 chế độ chuyển ở đầu trang: **ReAct Agent**, **Chatbot thường**
(để so sánh), **Autonomous** (Cấp 4). Phần suy luận và gọi tool thu gọn, bấm vào mới mở.

Dừng server bằng `Ctrl+C`.

## 4. Kiểm tra tiến độ

```bash
.venv\Scripts\python.exe tests\run_all.py
```

In bảng coverage của cả 4 vai và danh sách việc còn thiếu. Chạy riêng từng vai:
`tests\test_role1.py` … `test_role4.py`. Dùng Python thuần, không cần cài `pytest`.

## 5. Sinh lại dữ liệu và báo cáo

Các file này sinh tự động, chạy lại là ra y hệt (seed cố định):

| Lệnh | Sinh ra |
| :-- | :-- |
| `scripts\gen_database.py` | `config/mock_database.json` — 1000 học viên, 128 khóa |
| `scripts\gen_schema_doc.py` | `docs/SCHEMA_FOR_PROMPT.md` — schema rút gọn cho Role 3 |
| `scripts\gen_trace_eval.py` | `docs/trace_eval.md` mục 2 — trace log 5 test case |
| `scripts\gen_cross_audit.py` | `docs/cross_audit.md` — 12 đòn tấn công |
| `scripts\viec_con_lai.py` | Liệt kê chỗ còn phải điền tay |

`gen_trace_eval.py` chỉ thay phần giữa hai mốc `BEGIN/END AUTO-TRACE`, không xóa nội dung
người khác viết thêm.

## 6. Xem prompt gửi lên LLM

Đổi trong `.env`:

```
LOG_PROMPT=1
```

Mỗi vòng lặp sẽ in nguyên văn system prompt và toàn bộ history gửi lên LLM. Dùng để chứng
minh Agent chạy bằng prompt thật chứ không hardcode. Nhớ trả về `0` khi trình chiếu.

## 7. Còn phải điền tay

```bash
.venv\Scripts\python.exe scripts\viec_con_lai.py
```

Lệnh này quét toàn repo tìm dấu `[[CAN-DIEN]]` và in ra file nào, dòng bao nhiêu.
Hiện còn: biên bản buổi cross-audit trên lớp trong `docs/cross_audit.md` mục 5.

## 8. Ai giữ file nào

| Vai | Người | File |
| :-- | :-- | :-- |
| Role 1 — Product Architect & Observability | Nguyễn Tiến Đạt | `config/test_cases.json`, `docs/trace_eval.md` |
| Role 2 — Tool Engineer | Nguyễn Chí Hướng | `src/tools.py` |
| Role 3 — Prompt & Safeguard Engineer | Phạm Thị Liên | `src/prompts.py` |
| Role 4 — Core Developer / Integrator | Lê Quang Huy | `src/app.py`, `src/web_ui.py` |

Mỗi người làm trên nhánh riêng (`role1-product-architect` … `role4-core-developer`),
Role 4 merge vào `main`. Chi tiết ở [TEAMMATES.md](TEAMMATES.md).

## 9. Tài liệu

| File | Nội dung |
| :-- | :-- |
| [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) | Cấu trúc 4 bảng, các bẫy cài sẵn |
| [docs/SCHEMA_FOR_PROMPT.md](docs/SCHEMA_FOR_PROMPT.md) | Từ vựng dữ liệu, hình dạng Observation |
| [docs/trace_eval.md](docs/trace_eval.md) | Scoring Matrix + trace log thật |
| [docs/cross_audit.md](docs/cross_audit.md) | 12 đòn tấn công và kết quả phòng thủ |
| [docs/hybrid_flowchart.mermaid](docs/hybrid_flowchart.mermaid) | Khi nào đi Chatbot path, khi nào đi Agent path |
| [docs/roles/](docs/roles/) | Hướng dẫn chi tiết cho từng vai |
