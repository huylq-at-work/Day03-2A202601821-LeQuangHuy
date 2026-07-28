# 🟢 Role 1: Đánh Giá Agentic Fit & Trace Log

## 1. Scoring Matrix (Đánh giá độ phù hợp của Agent)

| Tiêu chí | Câu hỏi tự vấn | Điểm (1–5) | Lý do cụ thể cho đề tài Trợ lý tư vấn khóa học (Sàn Marketplace) |
| :-- | :-- | :-: | :-- |
| **Cần dữ liệu ngoài?** | Chatbot có biết ngân sách và lịch rảnh của học viên không? | 5 | LLM hoàn toàn mù tịt về ngân sách, lịch rảnh, trình độ và mục tiêu của học viên nếu không gọi tool `get_learner`. |
| **Nhiều bước?** | Có phải tra hồ sơ rồi mới biết lọc khóa thế nào? | 5 | Agent luôn phải gọi `get_learner` lấy thông tin trước, lấy được ngân sách và mục tiêu rồi mới có thể truyền vào `search_courses`. |
| **Có thao tác thật?** | Agent có phải *kiểm tra* điều kiện không, hay chỉ nói chung chung? | 4 | Agent phải đối chiếu 5 chiều (Ngân sách, Trình độ, Lịch, Khu vực, Sĩ số/Hạn) thông qua `check_suitability`. |
| **Rủi ro nếu sai?** | Tư vấn sai khóa 15 triệu thì sao? Có cần Guardrail? | 4 | Nếu tư vấn bừa học viên đăng ký sai lịch hoặc vượt xa ngân sách sẽ gây khiếu nại. Rất cần Guardrail chặn chém gió. |

## 2. Trace Log (Kết quả chạy Test Cases)

*(Chờ Role 4 hoàn thành Agent, bạn chạy 5 câu hỏi trong file `config/test_cases.json` và dán log quá trình suy nghĩ Thought-Action-Observation của Agent vào đây nhé)*

### Test Case 4 — Kiểm tra điều kiện
**Câu hỏi**: Em là 0987654387, em đăng ký khóa EN101 được không?

Thought: Cần xem hồ sơ học viên này trước.
Action: get_learner[0987654387]
Observation: Nguyễn Tiến Đạt — mục tiêu tiếng Anh, trình độ cơ bản,
             ngân sách 6,000,000đ, rảnh T3 tối/T5 tối, khu vực Hà Nội.
Thought: Giờ kiểm tra khóa EN101 có phù hợp không.
Action: check_suitability[0987654387, EN101]
Observation: Không phù hợp. Lý do: lịch không khớp (T2 tối, T4 tối).
Thought: Đã rõ nguyên nhân, trả lời học viên.
Final Answer: Khóa EN101 hợp túi tiền và trình độ của bạn, nhưng học T2/T4 tối
              mà bạn chỉ rảnh T3/T5 tối...

**Nhận xét**: ✅ Gọi đúng 2 tool theo thứ tự, chỉ ra đúng 1 lý do trượt, không bịa.

### Chatbot Baseline trả lời:
*(Ghi lại câu trả lời của Chatbot bình thường không có tool ở đây để so sánh. Chắc chắn Chatbot sẽ trả lời chung chung hoặc bịa thông tin khóa học/học viên)*
