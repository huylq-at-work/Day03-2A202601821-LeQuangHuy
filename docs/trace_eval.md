# 🟢 Role 1: Đánh Giá Agentic Fit & Trace Log

## 1. Scoring Matrix (Đánh giá độ phù hợp của Agent)

| Tiêu chí | Câu hỏi tự vấn | Điểm (1–5) | Lý do cụ thể cho đề tài Trợ lý tư vấn khóa học (Sàn Marketplace) |
| :-- | :-- | :-: | :-- |
| **Cần dữ liệu ngoài?** | Trả lời được không nếu không tra cứu gì? | 5 | Bắt buộc phải tra cứu thông tin học viên (get_learner), danh sách khóa học (search_courses), giá tiền, và nhà cung cấp (get_provider). LLM không thể tự biết khóa học nào đang có trên sàn. |
| **Nhiều bước?** | Có phải gọi tool này rồi mới biết gọi tool kia? | 5 | Thường xuyên phải tìm khóa học (search_courses), có mã khóa (ma_khoa) rồi mới xem chi tiết (get_course_detail) hoặc kiểm tra độ phù hợp (check_suitability). |
| **Có thao tác thật?** | Agent có phải *làm* gì không, hay chỉ nói? | 2 | Chủ yếu là truy vấn đọc (Read) dữ liệu để tư vấn, so sánh khóa học, không có thao tác mua/thanh toán trực tiếp. |
| **Rủi ro nếu sai?** | Sai thì hậu quả thế nào, có cần Guardrail? | 4 | Tư vấn sai giá, sai nhà cung cấp hoặc sai thông tin khóa học sẽ làm sai lệch quyết định mua của khách hàng. Cần guardrail không bịa khóa học. |

## 2. Trace Log (Kết quả chạy Test Cases)

*(Chờ Role 4 hoàn thành Agent, bạn chạy 5 câu hỏi trong file `config/test_cases.json` và dán log quá trình suy nghĩ Thought-Action-Observation của Agent vào đây nhé)*

### Test Case 3 — Multi-step
**Câu hỏi**: Tìm cho tôi khóa học về Python giá tối đa 500k, sau đó xem chi tiết nội dung của khóa học đó.
**Log**:
*(Dán nội dung log vào đây - ví dụ gọi search_courses rồi get_course_detail)*
**Nhận xét**: *(Ví dụ: Agent tìm được khóa học và gọi đúng tool xem chi tiết dựa trên mã khóa học tìm được)*

### Test Case 4 — Multi-step
**Câu hỏi**: Tôi có số điện thoại 0912345678, khóa học mã CS101 và CS102 khóa nào phù hợp với tôi hơn?
**Log**:
*(Dán nội dung log vào đây - ví dụ gọi check_suitability và compare_courses)*
**Nhận xét**: *(Ví dụ: Agent phân tích thông tin trả về, so sánh các điểm tương đồng và tư vấn rất chính xác)*

### Test Case 5 — Edge Case (Bẫy)
**Câu hỏi**: Kiểm tra độ phù hợp của tôi (SĐT 0999999999) với khóa học mã MAGIC999.
**Log**:
*(Dán nội dung log vào đây)*
**Nhận xét**: *(Ví dụ: Agent báo lỗi lịch sự khi không tìm thấy học viên hoặc khóa học, Guardrail hoạt động tốt)*
