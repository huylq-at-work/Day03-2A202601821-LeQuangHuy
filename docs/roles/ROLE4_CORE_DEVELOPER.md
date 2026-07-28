# 🚀 ROLE 4 — CORE DEVELOPER / INTEGRATOR

| | |
| :-- | :-- |
| **Người đảm nhận** | Lê Quang Huy — 2A202601821 |
| **Branch** | `role4-core-developer` |
| **File giữ** | `src/app.py` |
| **Trọng số điểm** | 30% (ReAct Implementation & Tools — chia với Role 2) |

---

## ✅ Trạng thái: vòng lặp ReAct đã viết xong

`src/app.py` đã có vòng lặp ReAct thật (không còn hardcode như bản boilerplate). Đã test 7 case bằng provider giả lập — parse đúng, xử lý lỗi đúng, guardrail dừng đúng.

| Hàm | Việc |
| :-- | :-- |
| `parse_action()` | Regex bóc `Action: ten_tool[a, b]` ra tên + danh sách tham số |
| `call_tool()` | Gọi tool, bọc lỗi thành chuỗi `LỖI:` để Agent tự đọc mà xử lý |
| `cut_hallucinated_observation()` | LLM hay tự bịa `Observation` — cắt bỏ để Observation luôn là kết quả tool thật |
| `run_react_agent()` | Vòng lặp chính, nối `history` qua từng vòng, guardrail khi chạm `MAX_ITERATIONS` |

Chạy:

```bash
.venv\Scripts\python.exe src\app.py 3      # test case số 3
.venv\Scripts\python.exe src\app.py all    # cả 5 test case
```

### 🔑 Vì sao đổi đề tài mà không phải sửa `app.py`

Vòng lặp viết **generic**: nó đọc `AVAILABLE_TOOLS` lúc chạy, tool tên gì cũng gọi được. Nhóm đổi từ "đăng ký môn ở trường" sang "marketplace khóa học bên ngoài", Role 2 đổi toàn bộ tên tool — `app.py` vẫn chạy nguyên si.

`src/app.py` chỉ import `AVAILABLE_TOOLS`, **không import tên tool cụ thể**. Giữ nguyên như vậy, đừng thêm `from tools import get_learner` — làm thế là trói app vào file của Role 2, Role 2 đổi tên hàm là app crash.

---

## 🎯 Việc còn lại của bạn

### 1. Lấy API key (làm ngay, không cần chờ ai)

`MockProvider` chỉ trả một câu cố định nên vòng lặp sẽ lặp tới khi chạm guardrail — không demo được `Final Answer`. Bắt buộc phải có LLM thật.

```bash
copy .env.example .env
```

Điền vào `.env` — Gemini có bản miễn phí, lấy key tại [aistudio.google.com](https://aistudio.google.com/app/apikey):

```
LLM_PROVIDER=gemini
GEMINI_API_KEY=<key_cua_ban>
LLM_MODEL=gemini-2.5-flash
```

> 🔒 `.env` đã nằm trong `.gitignore` — **không bao giờ commit key lên GitHub**.

### 2. Đầu mối lắp ráp

Gom code của 3 bạn kia rồi chạy nghiệm thu:

```bash
git checkout main
git pull origin main
git merge origin/role1-product-architect origin/role2-tool-engineer origin/role3-prompt-engineer
```

Mỗi người giữ 1 file riêng nên hầu như không bao giờ conflict.

### 3. Chốt 2 điểm giao giữa các vai

Đây là việc chỉ Integrator mới thấy — cả hai đều làm sập app nếu bỏ qua:

| Cần chốt | Với ai | Vì sao |
| :-- | :-- | :-- |
| **Tên tool khớp nhau** | Role 2 ↔ Role 3 | Prompt của Liên liệt kê `get_learner` mà registry của Hướng đặt là `get_hoc_vien` → Agent gọi tool không tồn tại |
| **`MAX_ITERATIONS = 5`** | Role 3 | Chuỗi demo chính cần 4 vòng. Để 3 là demo đẹp nhất chết ở guardrail |

### 4. Mốc 4 — trình chiếu & phản biện

Bạn là người demo app và chống đỡ câu bẫy từ nhóm khác.

---

## 🧪 Test nhanh khi code Role 2 và Role 3 về

```bash
.venv\Scripts\python.exe src\app.py 3
```

Nhìn vào output, kiểm 4 thứ:

| Dấu hiệu | Nghĩa là |
| :-- | :-- |
| `Tools sẵn có: get_learner, search_courses, ...` | Registry của Role 2 load đúng |
| LLM sinh ra `Thought:` + `Action:` rồi dừng | Prompt của Role 3 đạt |
| `Observation:` là dữ liệu thật, không phải LLM bịa | `cut_hallucinated_observation()` hoạt động |
| Ra `Final Answer` trước khi hết 5 vòng | `MAX_ITERATIONS` đủ rộng |

Nếu thấy `[!] LLM không sinh đúng định dạng Action` → prompt của Role 3 chưa đủ chặt, báo Liên siết lại.

Nếu thấy `LỖI: Không có công cụ nào tên '...'` → tên tool trong prompt lệch với registry, đây là lỗi giao giữa Role 2 và Role 3.

---

## 📦 Dữ liệu

[`config/mock_database.json`](../../config/mock_database.json) — 1000 học viên, 13 khóa, 5 nhà cung cấp, 6 giảng viên. Chi tiết: [DATABASE_SCHEMA.md](../DATABASE_SCHEMA.md).

Hồ sơ để test nhanh:

| SĐT | Ngân sách | Trình độ | Rảnh | Khu vực |
| :-- | :-- | :-- | :-- | :-- |
| `0912345203` | 2tr | mới bắt đầu | T2, T4 tối | Hà Nội |
| `0987654387` | 6tr | cơ bản | T3, T5 tối | Hà Nội |
| `0901234795` | 15tr | trung cấp | T2, T4, T6 tối | Hà Nội |
| `0977888821` | 8tr | cơ bản | T7, CN sáng | TP.HCM |

---

## 🎁 BONUS +10% — Autonomous Agent (Cấp 4) — ĐÃ LÀM

Làm **cả hai** năng lực, đều nằm trong `src/app.py`:

| Thành phần | Hàm | Việc |
| :-- | :-- | :-- |
| **Planning** | `lap_ke_hoach()` | Trước khi vào vòng lặp, hỏi LLM chia mục tiêu thành tối đa 4 bước, rồi chèn kế hoạch vào history |
| **Memory** | `class BoNho` | Nhớ kết quả tool đã tra. Lượt sau hỏi lại cùng thứ thì lấy từ bộ nhớ, không gọi tool |
| Demo | `run_autonomous_agent()` | Ghép cả hai, in kế hoạch và đánh dấu 🧠 khi dùng bộ nhớ |

Chạy demo:

```bash
.venv\Scripts\python.exe src\app.py auto
```

Kịch bản: hỏi 2 lượt về cùng một học viên. Lượt 2 lấy hồ sơ từ bộ nhớ thay vì gọi lại `get_learner` — đó chính là điểm khác so với Cấp 3.

Trên giao diện web có nút **Autonomous** ở header, hiện kế hoạch tự vạch và đánh dấu bước nào lấy từ bộ nhớ.

### Ba quyết định đáng nói khi phản biện

**Chỉ cache tool chỉ-đọc.** `dang_ky_hoc_vien` ghi dữ liệu nên tuyệt đối không cache — cache thì lần đăng ký thứ hai bị bỏ qua, dữ liệu sai. Danh sách trắng nằm ở `TOOL_CHI_DOC`.

**Không nhớ kết quả `LỖI:`.** Người dùng gõ nhầm số điện thoại rồi gõ lại đúng thì phải tra lại thật, không được trả lỗi cũ từ cache.

**Planning tốn thêm khoảng 1 vòng lặp.** Đo thực tế trên cùng câu hỏi: ReAct thường dùng 5 vòng, Autonomous dùng 6/6 vì kế hoạch khiến Agent kiểm tra kỹ hơn (so sánh khóa, thử nhiều khóa). Nếu `MAX_ITERATIONS` để chật quá thì chế độ Autonomous dễ chạm Guardrail hơn Cấp 3 — đây là đánh đổi có thật, không phải lỗi.

---

## 🖥️ Giao diện web — dùng để trình chiếu Mốc 4

```bash
.venv\Scripts\python.exe src\web_ui.py
```

Mở `http://localhost:8765`. Hai cột cạnh nhau trên **cùng một câu hỏi**:

| Cột trái | Cột phải |
|---|---|
| Chatbot thường (Cấp 2) | ReAct Agent (Cấp 3) |
| Trả lời chung chung, không tra được gì | Hiện từng vòng: 💭 Thought · 🛠 Action · 👁 Observation · 🏁 Final Answer |

Bấm sẵn được 5 test case của Role 1. Observation lỗi hiện màu đỏ, Guardrail hiện khung vàng.

Dùng `http.server` có sẵn trong Python — **không cài thêm thư viện nào**, `requirements.txt` giữ nguyên.

> 🔑 UI và CLI dùng chung hàm `react_steps()` trong `app.py`, nên logic không bao giờ lệch nhau. Sửa vòng lặp một chỗ là cả hai cùng đổi.

---

## 🧪 Tự chấm & theo dõi cả nhóm

Phần của bạn (29 mục):

```bash
.venv\Scripts\python.exe tests\test_role4.py
```

Bảng điều khiển cả nhóm — dành riêng cho vai Integrator:

```bash
.venv\Scripts\python.exe tests\run_all.py
```

Chạy cả 4 bộ test, in coverage từng người và danh sách việc còn thiếu. Dùng nó để biết ai đang tắc mà không cần đi hỏi từng bạn:

```
  Vai trò         File giữ                        Coverage
  ----------------------------------------------------------
  Role 1  Đạt     test_cases.json + docs    #######... 14/20  70%
  Role 2  Hướng   src/tools.py              #.........  2/18  11%
  Role 3  Liên    src/prompts.py            ######.... 11/17  65%
  Role 4  Huy     src/app.py                #########. 27/29  93%
```

Test của bạn kiểm cả một thứ dễ vỡ về sau: `app.py` **không được** `from tools import get_learner`. Chỉ import `AVAILABLE_TOOLS` thôi, không thì Role 2 đổi tên hàm là app crash.

---

## ✅ Checklist

- [x] Vòng lặp ReAct thật (`parse_action` + `history` + guardrail)
- [x] Chặn tool không tồn tại, chặn LLM bịa Observation
- [ ] Tạo `.env` + lấy API key Gemini
- [ ] Chốt tên tool giữa Role 2 và Role 3
- [ ] Chốt `MAX_ITERATIONS = 5` với Role 3
- [ ] `git merge` code cả nhóm, chạy đủ 5 test case
- [ ] Giao log cho Role 1 (Đạt) làm trace
- [ ] Mốc 4: chuẩn bị trình chiếu
- [ ] 🎁 Bonus: Planning hoặc Memory

---

## 🔄 Git

```bash
git checkout role4-core-developer
git pull origin main
```

Xong việc:

```bash
git add src/app.py
git commit -m "Role 4: ReAct loop"
git push origin role4-core-developer
```
