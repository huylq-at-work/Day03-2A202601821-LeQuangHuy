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
    ↓
provider.generate()
    ↓
LLM trả lời trực tiếp bằng kiến thức có sẵn
    ↓
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
    ↓
Action: dang_ky_hoc_vien[...]
    ↓
Observation: hồ sơ được tạo hoặc thông báo dữ liệu còn thiếu
    ↓
Action: search_courses[vật lý, 100000000]
    ↓
Observation: danh sách khóa Vật Lý
    ↓
Action: check_suitability[0283736282, PH101]
    ↓
Observation: Phù hợp.
    ↓
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
