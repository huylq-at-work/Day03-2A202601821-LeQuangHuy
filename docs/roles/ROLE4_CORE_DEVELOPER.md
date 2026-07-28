# 🚀 ROLE 4 — CORE DEVELOPER / INTEGRATOR

| | |
| :-- | :-- |
| **Người đảm nhận** | Lê Quang Huy — 2A202601821 |
| **Branch** | `role4-core-developer` |
| **File giữ** | `src/app.py` |
| **Trọng số điểm** | 30% (ReAct Implementation & Tools — chia với Role 2) |

---

## 🎯 Việc của bạn

Bạn là **đầu mối lắp ráp**: gom code của Role 1, 2, 3 rồi ghép thành app chạy được, và tự viết **vòng lặp ReAct thật**.

Vai nặng nhất, cũng là vai quyết định điểm cao nhất của bài.

---

## 🔴 VIỆC QUAN TRỌNG NHẤT — Vòng lặp ReAct hiện đang là ĐỒ GIẢ

Mở `src/app.py`, xem hàm `run_react_agent()`. Code boilerplate đang **hardcode**:

```python
if step == 1:
    print("🧠 Thought: Câu hỏi này cần tra cứu thời tiết thời gian thực.")
    print("🛠️ Action: get_weather['Hà Nội']")
    obs = get_weather("Hà Nội")   # ← gọi cứng, không hỏi LLM
```

Nó **không gọi LLM lần nào**. Hỏi câu gì nó cũng in ra y hệt về thời tiết Hà Nội. Đây chính là phần bạn phải làm lại — và là chỗ chấm 30% điểm.

### Vòng lặp thật cần làm gì

```
1. Gửi REACT_SYSTEM_PROMPT + câu hỏi cho LLM
2. LLM trả về text chứa "Thought: ... / Action: get_transcript[2A202601203]"
3. Code PARSE text đó ra: tên tool = "get_transcript", tham số = "2A202601203"
4. Tra AVAILABLE_TOOLS["get_transcript"] rồi gọi → được Observation
5. Nối Observation vào lịch sử hội thoại, gửi lại LLM
6. Lặp lại cho tới khi LLM trả "Final Answer:" HOẶC chạm MAX_ITERATIONS
```

### Khung code gợi ý

```python
import re

def parse_action(text: str):
    """Bóc tên tool và tham số từ dòng 'Action: ten_tool[tham_so]'"""
    match = re.search(r"Action:\s*(\w+)\[(.*?)\]", text)
    if not match:
        return None, None
    return match.group(1), match.group(2).strip().strip("'\"")


def run_react_agent(user_query: str, provider):
    history = f"Câu hỏi: {user_query}\n"

    for step in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")

        # 1. Hỏi LLM
        response = provider.generate(history, system_prompt=REACT_SYSTEM_PROMPT)
        print(response)

        # 2. LLM đã có câu trả lời cuối chưa?
        if "Final Answer:" in response:
            print("✅ Agent đã hoàn thành.")
            return

        # 3. Parse Action
        tool_name, tool_arg = parse_action(response)
        if tool_name is None:
            print("⚠️ LLM không sinh đúng định dạng Action. Dừng an toàn.")
            return

        # 4. Gọi tool (có chặn tool không tồn tại)
        if tool_name not in AVAILABLE_TOOLS:
            obs = f"LỖI: Không tồn tại công cụ tên '{tool_name}'."
        else:
            obs = AVAILABLE_TOOLS[tool_name](tool_arg)
        print(f"👁️ Observation: {obs}")

        # 5. Nối vào lịch sử để LLM nhớ ngữ cảnh vòng sau
        history += f"{response}\nObservation: {obs}\n"

    print(f"🛡️ GUARDRAIL: Đã chạm giới hạn {MAX_ITERATIONS} bước. Ngắt lặp an toàn!")
```

> ⚠️ Bước 5 (nối `history`) là chỗ hay quên nhất. Thiếu nó thì mỗi vòng LLM lại quên sạch, gọi mãi 1 tool → lặp vô tận.

> 💡 Tool nhiều tham số (`check_schedule_conflict[ML101, DB202]`) cần tách thêm bằng `tool_arg.split(",")`. Bàn với Role 2 để thống nhất định dạng.

---

## 📍 Việc theo từng Mốc

| Mốc | Việc |
| :-: | :-- |
| **1** | Chạy `python src/app.py` kiểm tra môi trường sẵn sàng |
| **2** | `git pull` code Role 1+2+3 → nối `run_baseline_chatbot()` → chạy thử |
| **3** | `git pull` → **viết vòng lặp ReAct thật** (phần trên) → chạy 5 test case |
| **4** | Trình chiếu app khi cross-audit, chống đỡ câu bẫy của nhóm bạn |

---

## 🔌 Cấu hình API Key

Vòng lặp thật **bắt buộc phải có LLM** (MockProvider chỉ trả 1 câu cố định, không đủ để demo).

```bash
copy .env.example .env
```

Rồi điền vào `.env` — Gemini có bản miễn phí, lấy key tại [aistudio.google.com](https://aistudio.google.com/app/apikey):

```
LLM_PROVIDER=gemini
GEMINI_API_KEY=<key_cua_ban>
LLM_MODEL=gemini-2.5-flash
```

> 🔒 `.env` đã nằm trong `.gitignore` — **không bao giờ commit key lên GitHub**.

Chạy app:

```bash
.venv\Scripts\python.exe src\app.py
```

---

## 🎁 BONUS +10% — Autonomous Agent (Cấp 4)

Nếu còn thời gian, thêm 1 trong 2:

- **Planning**: trước khi vào vòng lặp, hỏi LLM "chia mục tiêu này thành các bước nhỏ" rồi chạy từng bước
- **Memory**: lưu `dict` ghi nhớ MSSV sinh viên đã hỏi, lần sau không cần hỏi lại

Tham khảo `src/ai_levels/level4_autonomous_agent.py`.

---

## ✅ Checklist

- [ ] Mốc 1: `python src/app.py` chạy được
- [ ] Mốc 2: `git pull` gom code cả nhóm, nối `run_baseline_chatbot()`
- [ ] Mốc 3: Viết `parse_action()` bóc tool từ text LLM
- [ ] Mốc 3: Viết vòng lặp ReAct thật, **nhớ nối `history`**
- [ ] Mốc 3: Chặn tool không tồn tại + chạm `MAX_ITERATIONS` là dừng
- [ ] Mốc 3: Chạy đủ 5 test case, giao log cho Role 1
- [ ] Mốc 4: Chuẩn bị trình chiếu app
- [ ] 🎁 Bonus: Planning hoặc Memory

---

## 🔄 Git — bạn là đầu mối merge

Trước khi code, gom code cả nhóm:

```bash
git checkout main
git pull origin main
git merge origin/role1-product-architect origin/role2-tool-engineer origin/role3-prompt-engineer
```

Vì mỗi người giữ 1 file riêng nên hầu như không bao giờ conflict.

Sau khi lắp xong:

```bash
git add src/app.py
git commit -m "Role 4: ReAct loop hoan chinh"
git push origin role4-core-developer
```
