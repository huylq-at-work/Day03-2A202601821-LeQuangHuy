# 🧠 ROLE 3 — PROMPT & SAFEGUARD ENGINEER

| | |
| :-- | :-- |
| **Người đảm nhận** | Phạm Thị Liên — 2A202601795 |
| **Branch** | `role3-prompt-engineer` |
| **File giữ** | `src/prompts.py` |
| **Trọng số điểm** | 20% (Guardrails & Observability) |

---

## 🎯 Đề tài & việc của bạn

**Trợ Lý Đăng Ký Khóa Học — marketplace khóa học bên ngoài**. Học viên định danh bằng **số điện thoại**.

Bạn viết **lời chỉ dẫn cho LLM** và lắp **phanh an toàn**.

Đây là vai then chốt: nếu prompt không ép được LLM sinh đúng định dạng `Thought / Action`, code của Role 4 **không đọc ra tên tool** → cả vòng lặp ReAct sập. Prompt của bạn là hợp đồng giữa LLM và code.

> 📖 **Đọc trước khi viết prompt**: [SCHEMA_FOR_PROMPT.md](../SCHEMA_FOR_PROMPT.md) — bản rút gọn 7 KB gồm từ vựng dữ liệu hợp lệ, đủ 13 mã khóa học, và **hình dạng Observation thật** mà mỗi tool trả về. Ví dụ few-shot trong prompt phải khớp với những chuỗi đó, nếu không LLM sẽ học sai định dạng.

---

## 📍 MỐC 1 (20 phút) — Liệt kê Failure Modes

| Failure Mode | Mô tả | Cách chặn |
| :-- | :-- | :-- |
| **Lặp vô tận** | Agent gọi đi gọi lại 1 tool | `MAX_ITERATIONS` |
| **Bịa dữ liệu** | Tool báo lỗi nhưng Agent vẫn tự chế hồ sơ học viên / khóa học | Câu lệnh cấm trong prompt |
| **Sai định dạng** | LLM viết văn xuôi thay vì `Action: ten_tool[tham_so]` | Ví dụ mẫu trong prompt |
| **Gọi tool không tồn tại** | LLM tự nghĩ ra `dang_ky_khoa_hoc[...]` | Liệt kê rõ danh sách tool |
| **Tư vấn ẩu** | Gợi ý khóa 15 triệu cho người có ngân sách 2 triệu | Bắt buộc gọi `check_suitability` trước khi chốt |

---

## 📍 MỐC 2 (30 phút) — Chatbot Baseline Prompt

Prompt này cố tình **không có tool** — để cả nhóm thấy Chatbot thua ở đâu:

```python
CHATBOT_BASELINE_PROMPT = """Bạn là một Chatbot tư vấn khóa học thông thường.
Hãy trả lời câu hỏi của học viên một cách thân thiện dựa trên kiến thức có sẵn của bạn.
Bạn KHÔNG có quyền truy cập vào hệ thống dữ liệu học viên hay danh mục khóa học.
Nếu không biết thông tin thực tế, hãy lịch sự thông báo cho người dùng.
"""
```

> 💡 Đừng làm prompt này quá tệ để "dìm hàng" Chatbot. Nó phải là baseline **công bằng** — có vậy so sánh mới thuyết phục.

---

## 📍 MỐC 3 (60 phút) — ReAct System Prompt

Phải chứa đủ 4 thành phần:

```python
REACT_SYSTEM_PROMPT = """Bạn là Trợ Lý Đăng Ký Khóa Học của một nền tảng tìm kiếm
khóa học, có khả năng sử dụng công cụ (Tools) để tra cứu dữ liệu thật.

# 1. DANH SÁCH CÔNG CỤ
1. get_learner[sdt]: Tra hồ sơ học viên theo số điện thoại (mục tiêu, trình độ,
   ngân sách, lịch rảnh, khu vực).
2. search_courses[chu_de, gia_toi_da]: Tìm khóa học theo chủ đề và mức giá tối đa.
3. get_course_detail[ma_khoa]: Xem chi tiết một khóa (giá, lịch, địa điểm, chỗ trống).
4. check_suitability[sdt, ma_khoa]: Kiểm tra học viên có đăng ký được khóa đó không,
   trả về lý do cụ thể nếu không phù hợp.

# 2. ĐỊNH DẠNG BẮT BUỘC
Mỗi lượt bạn CHỈ được viết đúng 2 dòng rồi DỪNG LẠI chờ Observation:

Thought: <suy luận của bạn về bước tiếp theo>
Action: <tên_công_cụ>[<tham_số>]

Khi đã đủ thông tin, viết:
Thought: Tôi đã có đủ thông tin để trả lời.
Final Answer: <câu trả lời hoàn chỉnh cho học viên>

# 3. VÍ DỤ
Câu hỏi: Em là 0912345203, em muốn học AI thì nên đăng ký khóa nào?
Thought: Tôi cần xem hồ sơ học viên này trước để biết ngân sách và trình độ.
Action: get_learner[0912345203]
Observation: Nguyễn Chí Hướng — mục tiêu: AI, dữ liệu; trình độ: mới bắt đầu;
             ngân sách: 2,000,000đ; rảnh: T2 tối, T4 tối; khu vực: Hà Nội.
Thought: Ngân sách 2 triệu, trình độ mới bắt đầu. Tôi tìm khóa AI trong tầm giá này.
Action: search_courses[AI, 2000000]
Observation: AI302 - AI cho người mới bắt đầu - 1,500,000đ - online.
Thought: Tôi kiểm tra xem học viên có đăng ký được khóa AI302 không.
Action: check_suitability[0912345203, AI302]
Observation: Phù hợp.
Thought: Tôi đã có đủ thông tin để trả lời.
Final Answer: Với ngân sách 2 triệu và trình độ mới bắt đầu, bạn nên đăng ký
              khóa AI302 (1.5 triệu, học online tự do)...

# 4. QUY TẮC AN TOÀN (BẮT BUỘC TUÂN THỦ)
- TUYỆT ĐỐI KHÔNG bịa hồ sơ học viên, tên khóa học, giá tiền hay lịch học.
- Nếu Observation bắt đầu bằng "LỖI:", hãy dừng lại và báo cho học viên một cách
  lịch sự, KHÔNG được thử đoán hay tự chế dữ liệu thay thế.
- Trước khi khuyên học viên đăng ký bất kỳ khóa nào, PHẢI gọi check_suitability
  để xác nhận. Không được tự suy đoán là phù hợp.
- Chỉ dùng đúng 4 công cụ liệt kê ở trên, không tự nghĩ ra công cụ mới.

BẮT ĐẦU:
"""
```

**Phần 3 (VÍ DỤ) là quan trọng nhất** — LLM học định dạng qua ví dụ tốt hơn nhiều so với đọc mô tả suông. Chú ý ví dụ trên có đúng 3 lần gọi tool, khớp với chuỗi demo chính của nhóm.

---

## 🛡️ MỐC 3 (tiếp) — Guardrails

```python
# 🛡️ PHANH AN TOÀN
MAX_ITERATIONS = 5    # Tối đa 5 vòng Thought-Action, tránh lặp vô tận
TIMEOUT_SECONDS = 10  # Timeout mỗi lần gọi tool
```

### ⚠️ Vì sao phải là 5, không phải 3

Chuỗi demo chính của nhóm cần **4 vòng**: 3 lần gọi tool (`get_learner` → `search_courses` → `check_suitability`) cộng 1 vòng chốt `Final Answer`.

Để `MAX_ITERATIONS = 3` thì **demo đẹp nhất của nhóm sẽ chết ở Guardrail** thay vì ra `Final Answer` — mất điểm oan ở cả tiêu chí 2 lẫn tiêu chí 3.

Nhưng cũng đừng để quá cao (10, 15): câu bẫy sẽ chạy lòng vòng cả chục lượt mà không ai thấy phanh đâu. **5 là vừa** — đủ cho chuỗi 3 hop, vẫn đủ chật để câu bẫy chạm phanh.

Chốt lại với Role 1: câu bẫy phải cần ≥6 vòng thì Guardrail mới có đất diễn.

---

## 🧪 Cách tự kiểm tra prompt

Chưa cần chờ Role 2 và Role 4. Dán prompt vào ChatGPT/Gemini web, thêm 1 câu hỏi, xem LLM có trả đúng định dạng 2 dòng không:

- ✅ Trả `Thought:` + `Action: get_learner[0912345203]` rồi **dừng lại**
- ❌ Trả cả đoạn văn dài, hoặc **tự bịa luôn `Observation`** → cần siết prompt chặt hơn

Khi Role 4 đã có app chạy, test nhanh bằng:

```bash
.venv\Scripts\python.exe src\app.py 3
```

---

## 🧪 Tự chấm — chạy bất cứ lúc nào

```bash
.venv\Scripts\python.exe tests\test_role3.py
```

Test này chấm 17 mục và in ra **chính xác còn phải sửa gì**. Quan trọng nhất, nó bắt được lỗi mà mắt thường rất khó thấy:

> **So từng tên tool trong prompt của bạn với `AVAILABLE_TOOLS` của Role 2.**
> Lệch một chữ (`get_learner` vs `get_hoc_vien`) là Agent gọi tool ma, luôn nhận `LỖI:`, và lặp tới khi chạm Guardrail. Nhìn code thì thấy cả hai đều "đúng", chỉ có test mới bắt được.

Ngoài ra nó kiểm: prompt đủ 4 phần chưa, có ví dụ few-shot kèm `Observation` chưa, có quy tắc cấm bịa chưa, `MAX_ITERATIONS` có nằm trong khoảng 5–8 không.

Chạy tới khi thấy `COVERAGE: 17/17` là xong phần bạn.

> ℹ️ Mục so khớp tên tool sẽ hiện `[-]` (bỏ qua) cho tới khi Role 2 làm xong `tools.py`. Nhớ chạy lại sau khi Hướng push code.

---

## ✅ Checklist

- [ ] Mốc 1: Liệt kê ít nhất 5 Failure Modes
- [ ] Mốc 2: `CHATBOT_BASELINE_PROMPT` (công bằng, không dìm hàng)
- [ ] Mốc 3: `REACT_SYSTEM_PROMPT` đủ 4 phần (tool / định dạng / ví dụ / an toàn)
- [ ] Mốc 3: Tên tool trong prompt **khớp chính xác** với `AVAILABLE_TOOLS` của Role 2
- [ ] Mốc 3: Đặt `MAX_ITERATIONS = 5` và giải thích được vì sao
- [ ] Mốc 3: Test prompt thủ công trên web LLM trước khi giao Role 4

---

## 🔄 Git

```bash
git checkout role3-prompt-engineer
git pull origin main
```

Xong việc:

```bash
git add src/prompts.py
git commit -m "Role 3: ReAct prompt va guardrails"
git push origin role3-prompt-engineer
```
