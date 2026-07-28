# 🟢 Role 1: Đánh Giá Agentic Fit & Trace Log

## 1. Scoring Matrix (Đánh giá độ phù hợp của Agent)

| Tiêu chí | Câu hỏi tự vấn | Điểm (1–5) | Lý do cụ thể cho đề tài Trợ lý tư vấn khóa học (Sàn Marketplace) |
| :-- | :-- | :-: | :-- |
| **Cần dữ liệu ngoài?** | Chatbot có biết ngân sách và lịch rảnh của học viên không? | 5 | LLM hoàn toàn mù tịt về ngân sách, lịch rảnh, trình độ và mục tiêu của học viên nếu không gọi tool `get_learner`. |
| **Nhiều bước?** | Có phải tra hồ sơ rồi mới biết lọc khóa thế nào? | 5 | Agent luôn phải gọi `get_learner` lấy thông tin trước, lấy được ngân sách và mục tiêu rồi mới có thể truyền vào `search_courses`. |
| **Có thao tác thật?** | Agent có phải *kiểm tra* điều kiện không, hay chỉ nói chung chung? | 4 | Agent phải đối chiếu 5 chiều (Ngân sách, Trình độ, Lịch, Khu vực, Sĩ số/Hạn) thông qua `check_suitability`. |
| **Rủi ro nếu sai?** | Tư vấn sai khóa 15 triệu thì sao? Có cần Guardrail? | 4 | Nếu tư vấn bừa học viên đăng ký sai lịch hoặc vượt xa ngân sách sẽ gây khiếu nại. Rất cần Guardrail chặn chém gió. |

## 2. Trace Log — output thật của chương trình

> Sinh tự động bằng `scripts/gen_trace_eval.py`, chạy trên `OpenAIProvider` (model `gpt-4o-mini`) với `MAX_ITERATIONS = 6`.
> Chạy lại script là ra lại toàn bộ log này — không chép tay.

### Test Case 1 — 🟢 Đơn giản (Chỉ cần LLM)

**Câu hỏi**: Học IELTS thì nên bắt đầu từ đâu?

**Kỳ vọng**: Chatbot trả lời từ kiến thức có sẵn, không cần tool.

#### Chatbot baseline (không có tool)

> Chào bạn! Để bắt đầu học IELTS, bạn có thể tham khảo các bước sau:
> 
> 1. **Hiểu rõ về IELTS**: Nắm rõ cấu trúc của bài thi, bao gồm các phần Listening, Reading, Writing và Speaking. Bạn nên tìm hiểu cách thức đánh giá và khung điểm của từng phần.
> 
> 2. **Đánh giá trình độ hiện tại**: Trước khi bắt đầu học, hãy kiểm tra trình độ tiếng Anh hiện tại của bạn để xác định mục tiêu IELTS của mình.
> 
> 3. **Lập kế hoạch học tập**: Tạo một kế hoạch học tập rõ ràng, xác định thời gian và nguồn tài liệu bạn sẽ sử dụng. Tạo một lịch học đều đặn để có thể ôn tập thường xuyên.
> 
> 4. **Sử dụng tài liệu học tập phù hợp**: Chọn sách và tài liệu uy tín, như các cuốn sách chuẩn bị cho IELTS hoặc các khóa học trực tuyến chất lượng.
> 
> 5. **Luyện tập các kỹ năng**: Thực hành từng phần của bài thi. Lắng nghe, đọc các bài viết, viết bài luận và luyện nói với người khác hoặc qua các ứng dụng.
> 
> 6. **Tham gia các khóa học**: Nếu có điều kiện, bạn có thể tham gia các khóa học IELTS để có sự hướng dẫn từ giảng viên và kết nối với những người cùng học.
> 
> 7. **Luyện thi thử**: Tham gia các bài kiểm tra mô phỏng để quen với áp lực thi cử và thời gian làm bài.
> 
> 8. **Phân tích kết quả**: Sau mỗi lần luyện tập, hãy xem xét những phần nào bạn còn cần cải thiện và điều chỉnh kế hoạch học tập của mình cho phù hợp.
> 
> Hãy nhớ rằng việc kiên trì và thực hành liên tục là rất quan trọng trong quá trình ôn luyện. Chúc bạn học tốt và đạt được kết quả mong muốn!

#### ReAct Agent

```
Thought: Tôi sẽ tìm các khóa học liên quan đến IELTS để gợi ý cho người dùng.
Action: search_courses[IELTS, ]
Observation: EN201 - IELTS 6.5 cấp tốc - 8,000,000đ - offline - trung cấp
Thought: Tôi đã tìm thấy một khóa học IELTS, nhưng chỉ có một khóa cho trình độ trung cấp. Tôi sẽ kiểm tra xem nó có phù hợp với nhu cầu học của người dùng hay không.
Action: search_courses[IELTS, 8000000]
Observation: EN201 - IELTS 6.5 cấp tốc - 8,000,000đ - offline - trung cấp
Thought: Tôi cần kiểm tra xem khóa EN201 có phù hợp với hồ sơ của người dùng hay không, nhưng chưa có thông tin về hồ sơ của họ.
Final Answer: Mình rất tiếc, nhưng trước tiên bạn cần cung cấp số điện thoại để mình có thể kiểm tra hồ sơ của bạn và xét xem khóa học IELTS này có phù hợp không nhé!
```

**Nhận xét**: Gọi 2 tool theo thứ tự: search_courses -> search_courses. Kết thúc bằng Final Answer trong 3/6 vòng.

---

### Test Case 2 — 🟢 Đơn giản (Chỉ cần LLM)

**Câu hỏi**: Làm sao để tập trung khi học code tại nhà?

**Kỳ vọng**: Chatbot trả lời chung chung bằng kiến thức có sẵn, không tra cứu thông tin học viên.

#### Chatbot baseline (không có tool)

> Để tập trung khi học code tại nhà, bạn có thể thử áp dụng một số mẹo sau đây:
> 
> 1. **Tạo không gian học tập riêng**: Chọn một nơi yên tĩnh, thoáng đãng mà bạn chỉ sử dụng cho việc học. Đảm bảo nơi đó được trang bị đầy đủ ánh sáng và ít bị làm phiền.
> 
> 2. **Thời gian biểu cụ thể**: Lên kế hoạch cho thời gian học của bạn. Chia nhỏ thời gian học thành các khoảng ngắn khoảng 25-50 phút, sau đó nghỉ khoảng 5-10 phút để tránh căng thẳng.
> 
> 3. **Giảm thiểu chi tiết phân tâm**: Tắt thông báo từ điện thoại và các ứng dụng không cần thiết trong khi học. Cố gắng giữ cho laptop và không gian làm việc của bạn sạch sẽ và không có những thứ gây sao nhãng.
> 
> 4. **Sử dụng các công cụ hỗ trợ**: Bạn có thể thử các công cụ như Pomodoro Technique để tăng cường năng suất, hoặc các ứng dụng giúp bạn tập trung như Forest, Focus@Will.
> 
> 5. **Đặt mục tiêu rõ ràng**: Xác định những gì bạn cần học hoặc cần hoàn thành trong buổi học. Đặt mục tiêu cụ thể và theo dõi tiến độ của bạn.
> 
> 6. **Thực hành thường xuyên**: Việc thực hành là rất quan trọng trong lập trình. Hãy dành thời gian viết code, giải quyết bài tập hoặc tham gia các dự án nhỏ để củng cố kỹ năng.
> 
> 7. **Kết nối với cộng đồng**: Tham gia các nhóm hoặc diễn đàn trực tuyến liên quan đến lập trình. Chia sẻ với người khác và học hỏi từ họ có thể tạo động lực cho bạn.
> 
> Hy vọng những gợi ý này sẽ giúp bạn tập trung hơn trong quá trình học coding tại nhà! Chúc bạn thành công!

#### ReAct Agent

```
Thought: Câu hỏi này nằm ngoài phạm vi tư vấn khóa học.
Final Answer: Mình chỉ hỗ trợ tìm và đăng ký khóa học thôi ạ. Bạn muốn mình gợi ý khóa nào không? Mình có thể tìm theo chủ đề, mức giá hoặc lịch rảnh của bạn.
```

**Nhận xét**: Agent **từ chối vì ngoài phạm vi** (guardrail mục 1C), không gọi tool nào. Kết thúc bằng Final Answer trong 1/6 vòng.

---

### Test Case 3 — 🟡 Multi-step (Tool sau phụ thuộc tool trước)

**Câu hỏi**: Em là 0912345203, em muốn học AI thì nên đăng ký khóa nào?

**Kỳ vọng**: get_learner(0912345203) → biết ngân sách 2tr, mới bắt đầu, rảnh T2/T4 tối → search_courses(AI, 2000000) → check_suitability → gợi ý khóa học phù hợp (như AI302).

#### Chatbot baseline (không có tool)

> Chào bạn! Rất vui khi bạn quan tâm đến việc học về trí tuệ nhân tạo (AI). Mặc dù mình không thể cung cấp thông tin cụ thể về các khóa học, nhưng mình có thể cho bạn một số gợi ý chung để bạn có thể chọn khóa học phù hợp:
> 
> 1. **Cấp độ kiến thức**: Nếu bạn mới bắt đầu, hãy tìm khóa học dành cho người mới. Ngược lại, nếu bạn đã có một số kiến thức cơ bản, bạn có thể tìm các khóa học nâng cao.
> 
> 2. **Nội dung khóa học**: Hãy xem xét nội dung khóa học có bao gồm những chủ đề bạn quan tâm, chẳng hạn như học máy (machine learning), học sâu (deep learning), xử lý ngôn ngữ tự nhiên (natural language processing), hay thị giác máy tính (computer vision).
> 
> 3. **Thực hành**: Nên chọn những khóa học có phần thực hành hoặc dự án thực tế, vì việc thực hành sẽ giúp bạn hiểu sâu hơn về kiến thức lý thuyết.
> 
> 4. **Chứng chỉ**: Nếu bạn cần một chứng chỉ để xác minh kỹ năng, hãy xem xét các khóa học có cấp chứng chỉ sau khi hoàn thành.
> 
> 5. **Ý kiến từ người học trước**: Tìm những đánh giá từ người đã học các khóa đó để có cái nhìn thực tế về chất lượng giảng dạy.
> 
> Hy vọng những gợi ý này sẽ hữu ích cho bạn trong việc tìm kiếm khóa học phù hợp. Chúc bạn học tốt!

#### ReAct Agent

```
Thought: Tôi cần xem hồ sơ học viên trước vì câu hỏi có số điện thoại.
Action: get_learner[0912345203]
Observation: Nguyễn Chí Hướng — mục tiêu: AI, dữ liệu; trình độ: mới bắt đầu; ngân sách: 2,000,000đ; rảnh: T2 tối, T4 tối; khu vực: Hà Nội.
Thought: Tôi dùng mục tiêu AI và ngân sách 2000000 để tìm khóa phù hợp về giá.
Action: search_courses[AI, 2000000]
Observation: AIX101 - Trí tuệ nhân tạo nhập môn - 1,070,000đ - offline - mới bắt đầu
AIX102 - Trí tuệ nhân tạo cơ bản - 1,140,000đ - online - mới bắt đầu
AI302 - AI cho người mới bắt đầu - 1,500,000đ - online - mới bắt đầu
AIX103 - Trí tuệ nhân tạo thực hành - 1,710,000đ - online - cơ bản
Thought: Tôi đã tìm thấy 3 khóa học phù hợp với mục tiêu và ngân sách, là AIX101, AIX102 và AI302. Tôi sẽ kiểm tra độ phù hợp của khóa AIX101 trước.
Action: check_suitability[0912345203, AIX101]
Observation: Không phù hợp. Lý do: lịch không khớp (T6 tối, T7 sáng).
Thought: Khóa AIX101 không phù hợp do lịch học không khớp với thời gian rảnh của học viên. Tôi sẽ kiểm tra khóa AIX102 tiếp theo.
Action: check_suitability[0912345203, AIX102]
Observation: Phù hợp.
Thought: Khóa AIX102 - Trí tuệ nhân tạo cơ bản phù hợp với mục tiêu, trình độ, ngân sách và có hình thức học online.
Final Answer: Với mục tiêu học AI, trình độ mới bắt đầu và ngân sách 2.000.000đ, bạn nên chọn AIX102 - Trí tuệ nhân tạo cơ bản. Khóa này học online, học phí 1.140.000đ và đã được kiểm tra là phù hợp với hồ sơ của bạn.
```

**Nhận xét**: Gọi 4 tool theo thứ tự: get_learner -> search_courses -> check_suitability -> check_suitability. Kết thúc bằng Final Answer trong 5/6 vòng.

---

### Test Case 4 — 🟡 Multi-step (Kiểm tra điều kiện)

**Câu hỏi**: Em là 0987654387, em đăng ký khóa EN101 được không?

**Kỳ vọng**: Agent phải chỉ ra ĐÚNG 1 lý do trượt: lịch khóa học không khớp khung rảnh T3/T5 tối của học viên.

#### Chatbot baseline (không có tool)

> Xin chào! Rất tiếc, nhưng mình không thể xác minh thông tin đăng ký hoặc trạng thái của khóa học cụ thể. Bạn có thể kiểm tra trên trang web hoặc liên hệ với bộ phận hỗ trợ của nhà cung cấp khóa học để biết thêm thông tin chi tiết về việc đăng ký khoá EN101. Nếu bạn cần bất kỳ lời khuyên nào về việc lựa chọn khóa học, mình sẵn sàng hỗ trợ nhé!

#### ReAct Agent

```
Thought: Tôi cần lấy hồ sơ học viên trước khi kiểm tra mã khóa EN101.
Action: get_learner[0987654387]
Observation: Nguyễn Tiến Đạt — mục tiêu: tiếng Anh; trình độ: cơ bản; ngân sách: 6,000,000đ; rảnh: T3 tối, T5 tối; khu vực: Hà Nội.
Thought: Người dùng hỏi đăng ký một khóa cụ thể nên tôi kiểm tra độ phù hợp trực tiếp.
Action: check_suitability[0987654387, EN101]
Observation: Không phù hợp. Lý do: lịch không khớp (T2 tối, T4 tối).
Thought: Tôi đã có đủ thông tin để trả lời.
Final Answer: Bạn chưa nên đăng ký khóa EN101 vì lịch học của khóa này không khớp với lịch rảnh của bạn (T3 tối, T5 tối). Bạn có thể xem xét các khóa khác phù hợp hơn.
```

**Nhận xét**: Gọi 2 tool theo thứ tự: get_learner -> check_suitability. Kết thúc bằng Final Answer trong 3/6 vòng.

---

### Test Case 5 — 🔴 Edge Case (Bẫy Guardrail)

**Câu hỏi**: Em là 0000000000, đăng ký giúp em khóa Thôi Miên Nâng Cao mã XYZ999 ạ.

**Kỳ vọng**: Cả 2 tool trả LỖI. Agent KHÔNG được bịa hồ sơ hay bịa khóa học. Guardrail ngắt sau MAX_ITERATIONS bước, trả lời lịch sự.

#### Chatbot baseline (không có tool)

> Xin chào! Cảm ơn bạn đã quan tâm đến khóa học Thôi Miên Nâng Cao. Tuy nhiên, mình không có quyền truy cập vào hệ thống để thực hiện việc đăng ký cho bạn. 
> 
> Mình khuyên bạn nên kiểm tra website hoặc nền tảng nơi khóa học được cung cấp để tìm hiểu cách đăng ký và thông tin chi tiết về khóa học. Nếu cần thêm thông tin hay hướng dẫn, bạn cũng có thể liên hệ trực tiếp với bộ phận hỗ trợ của nơi tổ chức khóa học. Chúc bạn tìm được khóa học phù hợp!

#### ReAct Agent

```
Thought: Tôi cần xem hồ sơ học viên trước để kiểm tra độ phù hợp cho khóa học.
Action: get_learner[0000000000]
Observation: LỖI: Không tìm thấy học viên có số điện thoại '0000000000'.
Thought: Người dùng chưa có hồ sơ học viên, tôi cần mời họ tạo hồ sơ với đầy đủ thông tin.
Final Answer: Mình không tìm thấy hồ sơ của bạn. Bạn có thể cung cấp cho mình số điện thoại, họ tên, chủ đề muốn học, trình độ (mới bắt đầu/cơ bản/trung cấp/nâng cao), ngân sách tối đa, khu vực đang ở, và các buổi rảnh trong tuần để mình giúp bạn tạo hồ sơ nhé!
```

**Nhận xét**: Gọi 1 tool theo thứ tự: get_learner. Tool trả `LỖI:` và Agent **không bịa dữ liệu thay thế**. Kết thúc bằng Final Answer trong 2/6 vòng.

---

## 3. Kết luận so sánh

Trên các câu cần dữ liệu thật, Chatbot baseline chỉ đưa lời khuyên chung vì không truy cập được hồ sơ học viên hay danh mục khóa học. ReAct Agent gọi tool tra đúng dữ liệu rồi mới kết luận, và nêu được lý do cụ thể khi học viên không đủ điều kiện.

Ngược lại, với câu hỏi kiến thức chung thì Chatbot trả lời tốt mà không cần tool — đây là lý do cần luồng Hybrid trong `docs/hybrid_flowchart.mermaid` thay vì đẩy mọi câu hỏi qua Agent.
