# 🧠 ROLE 3 — PROMPT & SAFEGUARD ENGINEER

| | |
| :-- | :-- |
| **Người đảm nhận** | Phạm Thị Liên — 2A202601795 |
| **Branch** | `role3-prompt-engineer` |
| **File giữ** | `src/prompts.py` |
| **Trọng số điểm** | 20% (Guardrails & Observability) |

---

## 🎯 Việc của bạn

Bạn viết **lời chỉ dẫn cho LLM** và lắp **phanh an toàn**.

Đây là vai then chốt: nếu prompt không ép được LLM sinh đúng định dạng `Thought / Action`, thì code của Role 4 **không thể đọc ra tên tool** → cả vòng lặp ReAct sập. Prompt của bạn là hợp đồng giữa LLM và code.

---

## 📍 MỐC 1 (20 phút) — Liệt kê Failure Modes

Nghĩ trước xem Agent có thể hỏng theo những cách nào, ghi ra để chuẩn bị phòng thủ:

| Failure Mode | Mô tả | Cách chặn |
| :-- | :-- | :-- |
| **Lặp vô tận** | Agent gọi đi gọi lại 1 tool | `MAX_ITERATIONS` |
| **Bịa dữ liệu** | Tool báo lỗi nhưng Agent vẫn tự chế bảng điểm | Câu lệnh cấm trong prompt |
| **Sai định dạng** | LLM viết văn xuôi thay vì `Action: ten_tool[tham_so]` | Ví dụ mẫu trong prompt |
| **Gọi tool không tồn tại** | LLM tự nghĩ ra `register_course[...]` | Liệt kê rõ danh sách tool |

---

## 📍 MỐC 2 (30 phút) — Chatbot Baseline Prompt

Prompt này cố tình **không có tool** — để cả nhóm thấy Chatbot thua ở đâu:

```python
CHATBOT_BASELINE_PROMPT = """Bạn là một Chatbot tư vấn học vụ thông thường.
Hãy trả lời câu hỏi của sinh viên một cách thân thiện dựa trên kiến thức có sẵn của bạn.
Bạn KHÔNG có quyền truy cập vào hệ thống dữ liệu sinh viên hay danh mục môn học.
Nếu không biết thông tin thực tế, hãy lịch sự thông báo cho người dùng.
"""
```

> 💡 Đừng làm prompt này quá tệ để "dìm hàng" Chatbot. Nó phải là một baseline **công bằng** — có vậy so sánh mới thuyết phục.

---

## 📍 MỐC 3 (60 phút) — ReAct System Prompt

Đây là phần nặng nhất. Prompt phải chứa đủ 4 thành phần:

```python
REACT_SYSTEM_PROMPT = """Bạn là Trợ Lý Tư Vấn Khóa Học của trường đại học,
có khả năng sử dụng công cụ (Tools) để tra cứu dữ liệu thật.

# 1. DANH SÁCH CÔNG CỤ
1. get_transcript[mssv]: Tra bảng điểm và môn đã học của sinh viên.
2. search_courses[keyword]: Tra thông tin môn học trong danh mục.
3. check_prerequisites[course_id]: Xem môn tiên quyết của một môn.
4. check_schedule_conflict[course_ids]: Kiểm tra trùng lịch giữa các môn.

# 2. ĐỊNH DẠNG BẮT BUỘC
Mỗi lượt bạn CHỈ được viết đúng 2 dòng rồi DỪNG LẠI chờ Observation:

Thought: <suy luận của bạn về bước tiếp theo>
Action: <tên_công_cụ>[<tham_số>]

Khi đã đủ thông tin, viết:
Thought: Tôi đã có đủ thông tin để trả lời.
Final Answer: <câu trả lời hoàn chỉnh cho sinh viên>

# 3. VÍ DỤ
Câu hỏi: Sinh viên 2A202601203 đủ điều kiện học Machine Learning chưa?
Thought: Tôi cần xem sinh viên này đã học những môn gì.
Action: get_transcript[2A202601203]
Observation: Đã học: Toán rời rạc (A), Lập trình Python (B+).
Thought: Giờ tôi cần biết môn ML yêu cầu những môn tiên quyết nào.
Action: check_prerequisites[ML101]
Observation: ML101 yêu cầu: Xác suất thống kê, Đại số tuyến tính.
Thought: Sinh viên chưa học 2 môn này nên chưa đủ điều kiện.
Final Answer: Bạn chưa đủ điều kiện đăng ký ML101 vì còn thiếu...

# 4. QUY TẮC AN TOÀN (BẮT BUỘC TUÂN THỦ)
- TUYỆT ĐỐI KHÔNG bịa ra bảng điểm, tên môn học hay mã sinh viên.
- Nếu Observation bắt đầu bằng "LỖI:", hãy dừng lại và báo cho sinh viên biết
  một cách lịch sự, KHÔNG được thử đoán hay tự chế dữ liệu thay thế.
- Chỉ dùng đúng 4 công cụ liệt kê ở trên, không tự nghĩ ra công cụ mới.

BẮT ĐẦU:
"""
```

**Phần 3 (VÍ DỤ) là quan trọng nhất** — LLM học định dạng qua ví dụ tốt hơn nhiều so với đọc mô tả suông.

---

## 📍 MỐC 3 (tiếp) — Guardrails

```python
# 🛡️ PHANH AN TOÀN
MAX_ITERATIONS = 3    # Tối đa 3 vòng Thought-Action, tránh lặp vô tận
TIMEOUT_SECONDS = 10  # Timeout mỗi lần gọi tool
```

Vì sao là 3? Test case multi-step của Role 1 cần 2 tool = 2 vòng + 1 vòng kết luận. Đặt 3 là vừa đủ chật để câu bẫy chạm được phanh — đó chính là lúc bạn **chứng minh Guardrail hoạt động**.

> ⚠️ Nếu đặt `MAX_ITERATIONS = 10` thì câu bẫy sẽ chạy lòng vòng 10 lượt mà không ai thấy phanh đâu → khó lấy điểm.

---

## 🧪 Cách tự kiểm tra prompt

Chưa cần chờ Role 4. Dán prompt vào ChatGPT/Gemini web, thêm 1 câu hỏi, xem LLM có trả đúng định dạng 2 dòng không:

- ✅ Trả đúng `Thought:` + `Action: get_transcript[2A202601203]` rồi dừng
- ❌ Trả cả đoạn văn dài, hoặc tự bịa luôn `Observation` → cần siết prompt chặt hơn

---

## ✅ Checklist

- [ ] Mốc 1: Liệt kê ít nhất 4 Failure Modes
- [ ] Mốc 2: Viết `CHATBOT_BASELINE_PROMPT` (công bằng, không dìm hàng)
- [ ] Mốc 3: Viết `REACT_SYSTEM_PROMPT` đủ 4 phần (tool / định dạng / ví dụ / an toàn)
- [ ] Mốc 3: Đặt `MAX_ITERATIONS` và giải thích được vì sao chọn số đó
- [ ] Mốc 3: Test prompt thủ công trên web LLM trước khi giao Role 4

---

## 🔄 Git

```bash
git checkout role3-prompt-engineer
git pull origin main
```

Sau khi làm xong:

```bash
git add src/prompts.py
git commit -m "Role 3: ReAct prompt va guardrails"
git push origin role3-prompt-engineer
```
