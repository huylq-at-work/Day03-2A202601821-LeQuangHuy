# Role 1: Đánh Giá Agentic Fit & Trace Log

## 1. Scoring Matrix (Đánh giá độ phù hợp của Agent)

| Tiêu chí | Câu hỏi tự vấn | Điểm (1–5) | Lý do cụ thể cho đề tài Trợ lý tư vấn khóa học (Sàn Marketplace) |
| :-- | :-- | :-: | :-- |
| **Cần dữ liệu ngoài?** | Chatbot có biết ngân sách và lịch rảnh của học viên không? | 5 | LLM hoàn toàn mù tịt về ngân sách, lịch rảnh, trình độ và mục tiêu của học viên nếu không gọi tool `get_learner`. |
| **Nhiều bước?** | Có phải tra hồ sơ rồi mới biết lọc khóa thế nào? | 5 | Agent luôn phải gọi `get_learner` lấy thông tin trước, lấy được ngân sách và mục tiêu rồi mới có thể truyền vào `search_courses`. |
| **Có thao tác thật?** | Agent có phải *kiểm tra* điều kiện không, hay chỉ nói chung chung? | 4 | Agent phải đối chiếu 5 chiều (Ngân sách, Trình độ, Lịch, Khu vực, Sĩ số/Hạn) thông qua `check_suitability`. |
| **Rủi ro nếu sai?** | Tư vấn sai khóa 15 triệu thì sao? Có cần Guardrail? | 4 | Nếu tư vấn bừa học viên đăng ký sai lịch hoặc vượt xa ngân sách sẽ gây khiếu nại. Rất cần Guardrail chặn chém gió. |

<!-- BEGIN AUTO-TRACE -->

## 2. Trace Log — output thật của chương trình

> Sinh tự động bằng `scripts/gen_trace_eval.py`, chạy trên `OpenAIProvider` (model `gpt-4o-mini`) với `MAX_ITERATIONS = 6`.
> Chạy lại script là ra lại toàn bộ log này — không chép tay.

### Test Case 1 —  Đơn giản (Chỉ cần LLM)

**Câu hỏi**: Học IELTS thì nên bắt đầu từ đâu?

**Kỳ vọng**: Chatbot trả lời từ kiến thức có sẵn, không cần tool.

#### Chatbot baseline (không có tool)

> Khi bắt đầu học IELTS, bạn có thể làm theo những bước sau để xây dựng nền tảng vững chắc:
>
> 1. **Hiểu cấu trúc bài thi**: Tìm hiểu về từng phần của bài thi IELTS (Listening, Reading, Writing, Speaking). Mỗi phần có yêu cầu và format riêng nên việc nắm rõ sẽ giúp bạn có kế hoạch học tập hiệu quả hơn.
>
> 2. **Đánh giá trình độ hiện tại**: Trước khi bắt đầu học, hãy tự kiểm tra trình độ tiếng Anh của mình. Bạn có thể làm một bài kiểm tra mẫu để biết mình đang ở mức nào và điểm mạnh, yếu của bản thân.
>
> 3. **Lên kế hoạch học tập**: Dựa trên mục tiêu của bạn (ví dụ: điểm số mong muốn, thời gian chuẩn bị), hãy lập một kế hoạch học tập cụ thể. Duy trì thói quen học tập hàng ngày sẽ giúp bạn tiến bộ nhanh chóng.
>
> 4. **Tài liệu học tập**: Sử dụng sách giáo trình, tài liệu trực tuyến hoặc các khóa học online dành cho IELTS. Có nhiều nguồn tài liệu chất lượng, giúp bạn rèn luyện cả bốn kỹ năng.
>
> 5. **Thực hành thường xuyên**: Thực hành là cách tốt nhất để cải thiện. Hãy thử làm các bài thi mẫu, luyện nghe qua podcast hoặc video, tham gia các câu lạc bộ tiếng Anh để rèn luyện kỹ năng nói.
>
> 6. **Nhận xét và cải thiện**: Nếu có thể, hãy nhờ người có kinh nghiệm hoặc giáo viên xem xét bài viết và phát âm của bạn. Nhận được phản hồi sẽ giúp bạn tiến bộ hơn.
>
> 7. **Tham gia các lớp học hoặc nhóm học**: Nếu có điều kiện, hãy tham gia các khóa học IELTS hoặc nhóm học để có sự hướng dẫn từ giảng viên và trao đổi với bạn bè.
>
> Hãy nhớ rằng sự kiên nhẫn và kiên trì là yếu tố quan trọng trong việc học tiếng Anh và đạt được kết quả tốt trong kỳ thi IELTS! Chúc bạn học tập hiệu quả!

#### ReAct Agent

```
Thought: Tôi sẽ tìm kiếm khóa học IELTS để gợi ý cho người dùng.
Action: search_courses[IELTS, ]
Observation: EN201 - IELTS 6.5 cấp tốc - 8,000,000đ - offline - trung cấp
Thought: Khóa học EN201 là IELTS 6.5 cấp tốc, tuy nhiên trình độ yêu cầu là trung cấp. Tôi sẽ tìm thêm khóa học khác phù hợp hơn cho người mới bắt đầu.
Action: search_courses[IELTS, 2000000]
Observation: Không tìm thấy khóa học nào về 'IELTS' dưới 2,000,000đ.
Thought: Tôi chưa tìm thấy khóa học IELTS nào phù hợp với ngân sách của bạn. Có thể bạn muốn nới ngân sách lên một chút hoặc chọn chủ đề khác không?
Final Answer: Hiện tại không có khóa học IELTS nào dưới 2.000.000đ. Bạn có muốn nới ngân sách hoặc tìm khóa học ở chủ đề khác không?
```

**Nhận xét**: Gọi 2 tool theo thứ tự: search_courses -> search_courses. Kết thúc bằng Final Answer trong 3/6 vòng.

---

### Test Case 2 —  Đơn giản (Chỉ cần LLM)

**Câu hỏi**: Làm sao để tập trung khi học code tại nhà?

**Kỳ vọng**: Chatbot trả lời chung chung bằng kiến thức có sẵn, không tra cứu thông tin học viên.

#### Chatbot baseline (không có tool)

> Để tập trung khi học code tại nhà, bạn có thể thử áp dụng một số mẹo sau:
>
> 1. **Thiết lập không gian học tập**: Tạo một không gian học tập riêng biệt, gọn gàng và thoải mái. Đảm bảo nơi đó yên tĩnh và ít bị phân tâm.
>
> 2. **Lên lịch học**: Đặt lịch học cụ thể mỗi ngày. Thời gian này nên được duy trì như một thói quen để giúp bạn vào guồng nhanh chóng.
>
> 3. **Sử dụng kỹ thuật Pomodoro**: Thử học trong khoảng 25 phút và nghỉ 5 phút. Sau bốn chu kỳ, hãy nghỉ dài hơn. Kỹ thuật này giúp duy trì sự tập trung mà không cảm thấy quá mệt mỏi.
>
> 4. **Giảm thiểu yếu tố phân tâm**: Tắt thông báo trên điện thoại, đóng các tab không cần thiết trên trình duyệt và giữ cho môi trường học tập tránh xa những yếu tố có thể gây sao nhãng.
>
> 5. **Đặt mục tiêu học tập**: Xác định rõ mục tiêu cần đạt được trong mỗi buổi học. Điều này sẽ giúp bạn dễ dàng hơn trong việc tập trung vào những gì cần làm.
>
> 6. **Thay đổi phương pháp học**: Nếu bạn cảm thấy chán nản, thử đổi mới cách học như xem video, tham gia các diễn đàn hoặc làm bài tập thực hành.
>
> 7. **Tự thưởng cho bản thân**: Sau khi hoàn thành một mục tiêu học tập, hãy tự thưởng cho mình một thứ gì đó nhỏ để tạo động lực.
>
> Hy vọng những mẹo này giúp bạn có thể tập trung hơn khi học code tại nhà! Chúc bạn học tập hiệu quả!

#### ReAct Agent

```
Thought: Câu hỏi này nằm ngoài phạm vi tư vấn khóa học.
Final Answer: Mình chỉ hỗ trợ tìm và đăng ký khóa học thôi ạ. Bạn muốn mình gợi ý khóa nào không? Mình có thể tìm theo chủ đề, mức giá hoặc lịch rảnh của bạn.
```

**Nhận xét**: Agent **từ chối vì ngoài phạm vi** (guardrail mục 1C), không gọi tool nào. Kết thúc bằng Final Answer trong 1/6 vòng.

---

### Test Case 3 —  Multi-step (Tool sau phụ thuộc tool trước)

**Câu hỏi**: Em là 0912345203, em muốn học AI thì nên đăng ký khóa nào?

**Kỳ vọng**: get_learner(0912345203)  biết ngân sách 2tr, mới bắt đầu, rảnh T2/T4 tối  search_courses(AI, 2000000)  check_suitability  gợi ý khóa học phù hợp (như AI302).

#### Chatbot baseline (không có tool)

> Chào bạn! Học trí tuệ nhân tạo (AI) là một lĩnh vực rất thú vị và có nhiều cơ hội nghề nghiệp. Tuy nhiên, mình không thể cung cấp thông tin cụ thể về các khóa học.
>
> Mình khuyên bạn nên tìm hiểu về các khóa học liên quan đến những chủ đề như:
>
> 1. **Cơ bản về AI và Machine Learning**: Nên tìm khóa học phù hợp cho người mới bắt đầu để nắm được các khái niệm cơ bản.
>
> 2. **Deep Learning**: Khi bạn đã nắm chắc kiến thức cơ bản, có thể tìm các khóa học chuyên sâu hơn về mạng nơ-ron và Deep Learning.
>
> 3. **Xử lý hình ảnh và video**: Nếu bạn hứng thú với việc làm việc với hình ảnh, tìm các khóa học liên quan đến computer vision.
>
> 4. **Xử lý ngôn ngữ tự nhiên (NLP)**: Nếu bạn quan tâm đến việc hiểu và phân tích ngôn ngữ, các khóa học về NLP cũng rất hữu ích.
>
> Bạn nên tìm khóa học từ các nền tảng uy tín và xem xét các đánh giá để chọn lựa đúng cho bản thân. Chúc bạn tìm được khóa học phù hợp và học tập hiệu quả!

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
Thought: Tôi đã tìm thấy một số khóa học AI phù hợp với mục tiêu và ngân sách của bạn. Trước khi khuyên đăng ký bất kỳ khóa nào, tôi cần kiểm tra độ phù hợp của từng khóa.
Action: check_suitability[0912345203, AIX101]
Observation: Không phù hợp. Lý do: lịch không khớp (T6 tối, T7 sáng).
Thought: Tôi cần kiểm tra khóa tiếp theo, AIX102, để xem nó có phù hợp với hồ sơ học viên không.
Action: check_suitability[0912345203, AIX102]
Observation: Phù hợp.
Thought: Tôi cần kiểm tra khóa tiếp theo, AI302, để xem nó có phù hợp với hồ sơ học viên không.
Action: check_suitability[0912345203, AI302]
Observation: Phù hợp.
Thought: Tôi đã có đủ thông tin để trả lời.
Final Answer: Với mục tiêu học AI, trình độ mới bắt đầu và ngân sách 2.000.000đ, bạn có thể chọn AIX102 - Trí tuệ nhân tạo cơ bản với học phí 1.140.000đ (online), hoặc AI302 - AI cho người mới bắt đầu với học phí 1.500.000đ (online). Cả hai khóa này đều phù hợp với hồ sơ của bạn.
```

**Nhận xét**: Gọi 5 tool theo thứ tự: get_learner -> search_courses -> check_suitability -> check_suitability -> check_suitability. Kết thúc bằng Final Answer trong 6/6 vòng.

---

### Test Case 4 —  Multi-step (Kiểm tra điều kiện)

**Câu hỏi**: Em là 0987654387, em đăng ký khóa EN101 được không?

**Kỳ vọng**: Agent phải chỉ ra ĐÚNG 1 lý do trượt: lịch khóa học không khớp khung rảnh T3/T5 tối của học viên.

#### Chatbot baseline (không có tool)

> Chào bạn! Rất vui khi bạn quan tâm đến khóa học EN101. Tuy nhiên, mình không có khả năng truy cập thông tin về tình trạng đăng ký hoặc các khóa học cụ thể.
>
> Mình khuyên bạn nên kiểm tra trên trang web của trung tâm hoặc liên hệ với bộ phận hỗ trợ để biết rõ hơn về tình trạng đăng ký cũng như thông tin chi tiết về khóa học. Nếu cần, mình có thể giúp bạn với những thông tin chung về khóa học online. Bạn có cần thêm thông tin gì không?

#### ReAct Agent

```
Thought: Tôi cần lấy hồ sơ học viên trước khi kiểm tra mã khóa EN101.
Action: get_learner[0987654387]
Observation: Nguyễn Tiến Đạt — mục tiêu: tiếng Anh; trình độ: cơ bản; ngân sách: 6,000,000đ; rảnh: T3 tối, T5 tối; khu vực: Hà Nội.
Thought: Người dùng hỏi đăng ký một khóa cụ thể nên tôi kiểm tra độ phù hợp trực tiếp.
Action: check_suitability[0987654387, EN101]
Observation: Không phù hợp. Lý do: lịch không khớp (T2 tối, T4 tối).
Thought: Tôi đã có đủ thông tin để trả lời.
Final Answer: Bạn chưa nên đăng ký khóa EN101 vì lịch học T2/T4 tối không khớp với lịch rảnh của bạn là T3 tối và T5 tối.
```

**Nhận xét**: Gọi 2 tool theo thứ tự: get_learner -> check_suitability. Kết thúc bằng Final Answer trong 3/6 vòng.

---

### Test Case 5 —  Edge Case (Bẫy Guardrail)

**Câu hỏi**: Em là 0000000000, đăng ký giúp em khóa Thôi Miên Nâng Cao mã XYZ999 ạ.

**Kỳ vọng**: Cả 2 tool trả LỖI. Agent KHÔNG được bịa hồ sơ hay bịa khóa học. Guardrail ngắt sau MAX_ITERATIONS bước, trả lời lịch sự.

#### Chatbot baseline (không có tool)

> Xin chào! Rất vui được hỗ trợ bạn. Tuy nhiên, mình không thể truy cập thông tin cụ thể để đăng ký khóa học cho bạn. Bạn có thể tự đăng ký khóa "Thôi Miên Nâng Cao" mã XYZ999 thông qua nền tảng học trực tuyến hoặc liên hệ với bộ phận hỗ trợ của họ để được hướng dẫn thêm. Nếu bạn cần tư vấn về nội dung khóa học hay cách học hiệu quả, mình rất sẵn lòng giúp!

#### ReAct Agent

```
Thought: Tôi cần kiểm tra hồ sơ học viên trước khi xác nhận yêu cầu đăng ký khóa XYZ999.
Action: get_learner[0000000000]
Observation: LỖI: Không tìm thấy học viên có số điện thoại '0000000000'.
Thought: Tôi sẽ thông báo về việc không tìm thấy hồ sơ và mời học viên tạo hồ sơ mới, yêu cầu đủ thông tin cần thiết.
Final Answer: Mình không tìm thấy hồ sơ của bạn với số điện thoại này. Bạn có muốn tạo hồ sơ mới không? Vui lòng cung cấp cho mình số điện thoại, họ tên, chủ đề muốn học, trình độ (mới bắt đầu/cơ bản/trung cấp/nâng cao), ngân sách tối đa, khu vực đang ở và các buổi rảnh trong tuần nhé!
```

**Nhận xét**: Gọi 1 tool theo thứ tự: get_learner. Tool trả `LỖI:` và Agent **không bịa dữ liệu thay thế**. Kết thúc bằng Final Answer trong 2/6 vòng.

---

### 2.6. Kết luận nhanh

Trên các câu cần dữ liệu thật, Chatbot baseline chỉ đưa lời khuyên chung vì không truy cập được hồ sơ học viên hay danh mục khóa học. ReAct Agent gọi tool tra đúng dữ liệu rồi mới kết luận, và nêu được lý do cụ thể khi học viên không đủ điều kiện.

Ngược lại, với câu hỏi kiến thức chung thì Chatbot trả lời tốt mà không cần tool — đây là lý do cần luồng Hybrid trong `docs/hybrid_flowchart.mermaid` thay vì đẩy mọi câu hỏi qua Agent.

<!-- END AUTO-TRACE -->

---

---

## 3. So sánh thực nghiệm — Chatbot thường và ReAct Agent

### 3.1. Kịch bản

Người dùng thử đăng ký tài khoản, cung cấp nhu cầu học Vật Lý, trình độ mới bắt
đầu, ngân sách 100 triệu và yêu cầu hệ thống gợi ý khóa. Tình huống này cần:

1. Ghi nhớ thông tin qua nhiều lượt.
2. Kiểm tra dữ liệu đăng ký còn thiếu.
3. Tìm khóa học từ dữ liệu thật.
4. Kiểm tra khóa có phù hợp với hồ sơ hay không.

### 3.2. Chatbot thường

Với yêu cầu **“tôi muốn đăng ký tài khoản”**, Chatbot hướng dẫn chung rằng người
dùng cần truy cập website, tìm nút đăng ký, nhập tên/email/SĐT và chờ email xác
nhận. Đây là kiến thức chung, không phải quy trình của marketplace trong đề tài.

Khi người dùng muốn học Vật Lý, Chatbot chỉ nêu các tiêu chí nên xem xét như cấp
độ, nội dung, giảng viên, lịch và chứng chỉ. Đến câu **“khóa nào cũng được, gợi
ý đi”**, Chatbot không đưa được khóa Vật Lý cụ thể mà chuyển sang lập trình,
Digital Marketing, quản lý dự án, phân tích dữ liệu và ngoại ngữ.

```text
User prompt

provider.generate()

LLM trả lời trực tiếp bằng kiến thức có sẵn

Không gọi tool, không truy vấn mock database
```

### 3.3. ReAct Agent

Agent hỏi đúng bảy trường mà tool `dang_ky_hoc_vien` cần:

- Số điện thoại
- Họ tên
- Chủ đề muốn học
- Trình độ
- Ngân sách
- Khu vực
- Lịch rảnh

Người dùng cung cấp:

```text
0283736282, A, mới bắt đầu, 100 triệu, Hà Nội, cả tuần
```

Agent nhận ra tên `A` chưa hợp lệ và còn thiếu chủ đề nên hỏi lại. Sau khi nhận
`Nguyễn Văn A, Vật Lý`, Agent gợi ý:

> PH101 - Vật lý đại cương, online, học phí 1.200.000đ và phù hợp với hồ sơ.

Khi người dùng hỏi thêm, Agent trả các khóa cụ thể từ danh mục:

```text
PHX101 - Vật lý nhập môn - 870.000đ - offline - mới bắt đầu
PH101  - Vật lý đại cương - 1.200.000đ - online - mới bắt đầu
PHX102 - Vật lý cơ bản - 1.570.000đ - online - mới bắt đầu
PHX103 - Vật lý thực hành - 3.480.000đ - online - cơ bản
PH201  - Vật lý luyện thi THPT - 4.500.000đ - offline - cơ bản
PHX104 - Vật lý chuyên sâu - 5.540.000đ - offline - trung cấp
PHX105 - Vật lý nâng cao - 12.790.000đ - online - nâng cao
```

Luồng tool tương ứng dự kiến:

```text
Agent thu thập đủ bảy trường

Action: dang_ky_hoc_vien[...]

Observation: hồ sơ được tạo hoặc thông báo dữ liệu còn thiếu

Action: search_courses[vật lý, 100000000]

Observation: danh sách khóa Vật Lý

Action: check_suitability[0283736282, PH101]

Observation: Phù hợp.

Final Answer: gợi ý PH101 kèm lý do
```

### 3.4. Bảng so sánh

| Tiêu chí | Chatbot thường | ReAct Agent |
| :-- | :-- | :-- |
| **Nguồn dữ liệu** | Kiến thức chung của LLM | Kết quả tool và mock database |
| **Đăng ký tài khoản** | Hướng dẫn chung, suy đoán có email xác nhận | Hỏi đúng bảy trường của hồ sơ marketplace |
| **Kiểm tra thông tin thiếu** | Không kiểm tra theo schema | Phát hiện thiếu họ tên hợp lệ và chủ đề |
| **Ghi nhớ nhiều lượt** | Không tạo hồ sơ có cấu trúc | Dùng lịch sử để hoàn thiện hồ sơ |
| **Tìm khóa Vật Lý** | Không đưa được khóa cụ thể | Trả mã, tên, giá, hình thức và trình độ |
| **Cá nhân hóa** | Không đối chiếu hồ sơ với khóa | Gọi `check_suitability` theo SĐT và mã khóa |
| **Khả năng giải thích** | Lời khuyên chung | Có Observation và lý do cụ thể |
| **Rủi ro bịa dữ liệu** | Cao | Thấp hơn nhờ ràng buộc bằng tool |
| **Kết quả** | Người dùng chưa chọn được khóa Vật Lý | Có PH101 và thêm bảy lựa chọn |

### 3.5. Chấm điểm

Quy ước: 0 là không thực hiện được, 1 là thực hiện một phần, 2 là thực hiện
đúng và có dữ liệu kiểm chứng.

| Tiêu chí | Chatbot | Agent | Bằng chứng |
| :-- | :-: | :-: | :-- |
| Hiểu nghiệp vụ đăng ký | 0 | 2 | Agent hỏi đúng dữ liệu hồ sơ |
| Phát hiện thông tin thiếu | 0 | 2 | Agent hỏi lại họ tên và chủ đề |
| Giữ mục tiêu Vật Lý | 0 | 2 | Agent tiếp tục truy vấn đúng chủ đề |
| Đưa khóa học cụ thể | 0 | 2 | Agent trả mã, tên, giá và hình thức |
| Có raw trace tool | 0 | 1 | Kết quả phù hợp dữ liệu nhưng bản chép chưa có raw trace |
| **Tổng** | **0/10** | **9/10** | Agent hoàn thành nghiệp vụ, còn thiếu log tool gốc |

### 3.6. Giới hạn

- Bản hội thoại chỉ có câu trả lời cuối, chưa có raw Thought–Action–Observation.
- Hai chuỗi chưa dùng câu chữ và thứ tự thông tin hoàn toàn giống nhau, nên chưa
  phải A/B test kiểm soát tuyệt đối.
- Danh sách gợi ý có cả khóa trung cấp/nâng cao cho người mới bắt đầu. Agent cần
  gọi `check_suitability` trước khi khuyên đăng ký từng khóa.
- Nên bật `LOG_PROMPT=1` và chạy lại để lưu Action, tham số, Observation thật.

### 3.7. Kết luận

Chatbot thường phù hợp với câu hỏi kiến thức chung nhưng không thực hiện được
nghiệp vụ marketplace vì không truy cập hồ sơ và danh mục thật. ReAct Agent tốt
hơn trong kịch bản này vì biết thu thập dữ liệu thiếu, gọi tool theo nhiều bước,
kiểm tra điều kiện và trả kết quả có thể đối chiếu với database. Agent đạt
**9/10**, trong khi Chatbot đạt **0/10**; điểm còn thiếu là raw trace xác nhận
chuỗi tool đã thực thi.
