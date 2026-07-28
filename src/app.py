"""
CORE AGENT APP (Role 4)
Ghép Tools + Prompts + Test Cases + LLM Provider thành app hoàn chỉnh.
"""

import json
import os
import re
import sys
from dotenv import load_dotenv

# Đảm bảo import các module cùng thư mục src/ hoạt động mượt mà
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from tools import AVAILABLE_TOOLS
from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, MAX_ITERATIONS
from providers import get_llm_provider

load_dotenv()


def load_test_cases():
    """Đọc bộ test cases từ config/test_cases.json của Role 1"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")

    # Fallback kiểm tra nếu file ở thư mục hiện tại
    if not os.path.exists(config_path):
        config_path = "test_cases.json"

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_baseline_chatbot(user_query: str, provider):
    """Chatbot gốc: hỏi thẳng LLM, không có tool nào."""
    print(f"\n[CHATBOT BASELINE] Câu hỏi: {user_query}")
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"Chatbot trả lời:\n{response}")


def parse_action(text: str):
    """
    Bóc tên tool và tham số từ dòng 'Action: ten_tool[a, b]'.
    Trả về (None, []) nếu LLM không viết đúng định dạng.
    """
    match = re.search(r"Action:\s*(\w+)\s*\[(.*?)\]", text, re.DOTALL)
    if not match:
        return None, []

    name = match.group(1)
    raw_args = match.group(2).strip()
    if not raw_args:
        return name, []

    args = [a.strip().strip("'\"") for a in raw_args.split(",")]
    return name, args


def call_tool(name: str, args: list) -> str:
    """Gọi tool trong registry. Mọi lỗi đều trả về chuỗi để Agent tự đọc và xử lý."""
    if name not in AVAILABLE_TOOLS:
        return f"LỖI: Không có công cụ nào tên '{name}'. Chỉ dùng: {', '.join(AVAILABLE_TOOLS)}."

    try:
        return AVAILABLE_TOOLS[name](*args)
    except TypeError:
        return f"LỖI: Sai số lượng tham số khi gọi '{name}' với {args}."
    except Exception as e:
        return f"LỖI: Công cụ '{name}' gặp sự cố: {e}"


def cut_hallucinated_observation(text: str) -> str:
    """
    LLM hay tự bịa luôn phần Observation thay vì dừng lại chờ.
    Cắt bỏ để đảm bảo Observation luôn là kết quả tool thật.
    """
    for marker in ("\nObservation:", "\nObservation ", "Observation:"):
        idx = text.find(marker)
        if idx > 0:
            return text[:idx].rstrip()
    return text.strip()


def tach_thought(text: str) -> str:
    """Lấy phần suy luận sau nhãn 'Thought:' để hiển thị riêng."""
    m = re.search(r"Thought:\s*(.+?)(?:\n\s*(?:Action|Final Answer):|$)", text, re.DOTALL)
    return m.group(1).strip() if m else ""


LOI_XIN_LOI_SAI_DINH_DANG = ("Xin lỗi, mình chưa xử lý được yêu cầu này. "
                             "Bạn thử hỏi lại rõ hơn nhé.")
LOI_XIN_LOI_GUARDRAIL = ("Xin lỗi, mình chưa tra được thông tin bạn cần. "
                         "Bạn kiểm tra lại thông tin đã nhập hoặc liên hệ "
                         "bộ phận hỗ trợ giúp mình nhé.")


def react_steps(user_query: str, provider, lich_su=None):
    """
    Chạy vòng lặp ReAct và trả về danh sách bước dạng dict.

    Đây là phần lõi dùng chung: run_react_agent() in ra terminal,
    còn web_ui.py dựng giao diện — cả hai đều gọi hàm này nên không
    bao giờ lệch logic.

    lich_su: danh sách [(câu hỏi, câu trả lời)] của các lượt trước,
             để hội thoại nhiều lượt vẫn nhớ ngữ cảnh.
    """
    buoc = []
    history = ""
    for q, a in (lich_su or []):
        history += f"Câu hỏi: {q}\nFinal Answer: {a}\n"
    history += f"Câu hỏi: {user_query}\n"

    for vong in range(1, MAX_ITERATIONS + 1):
        # 1. Hỏi LLM xem bước tiếp theo làm gì
        reply = provider.generate(history, system_prompt=REACT_SYSTEM_PROMPT)
        reply = cut_hallucinated_observation(reply)
        thought = tach_thought(reply)

        # 2. LLM đã chốt được câu trả lời cuối chưa
        if "Final Answer:" in reply:
            buoc.append({"vong": vong, "loai": "final", "raw": reply, "thought": thought,
                         "final": reply.split("Final Answer:", 1)[1].strip()})
            return buoc

        # 3. Bóc Action ra
        tool_name, tool_args = parse_action(reply)
        if tool_name is None:
            buoc.append({"vong": vong, "loai": "sai_dinh_dang", "raw": reply,
                         "thought": thought, "final": LOI_XIN_LOI_SAI_DINH_DANG})
            return buoc

        # 4. Gọi tool thật
        observation = call_tool(tool_name, tool_args)
        buoc.append({"vong": vong, "loai": "tool", "raw": reply, "thought": thought,
                     "tool": tool_name, "args": tool_args, "observation": observation,
                     "loi": observation.strip().upper().startswith("LỖI")})

        # 5. Nối vào history để vòng sau LLM còn nhớ ngữ cảnh
        history += f"{reply}\nObservation: {observation}\n"

    # 6. Guardrail: hết số vòng cho phép mà vẫn chưa xong
    buoc.append({"vong": MAX_ITERATIONS, "loai": "guardrail", "final": LOI_XIN_LOI_GUARDRAIL})
    return buoc


def run_react_agent(user_query: str, provider):
    """
    Vòng lặp ReAct: Thought -> Action -> Observation, lặp đến khi có Final Answer
    hoặc chạm MAX_ITERATIONS (guardrail chống lặp vô tận).
    """
    print(f"\n[REACT AGENT] Câu hỏi: {user_query}")

    for b in react_steps(user_query, provider):
        if b["loai"] == "guardrail":
            print(f"\n[GUARDRAIL] Đã chạm giới hạn {MAX_ITERATIONS} bước, ngắt lặp an toàn.")
            print(f"Trả lời: {b['final']}")
            return

        print(f"\n--- Vòng lặp ReAct (Step {b['vong']}/{MAX_ITERATIONS}) ---")
        print(b["raw"])

        if b["loai"] == "final":
            return
        if b["loai"] == "sai_dinh_dang":
            print("[!] LLM không sinh đúng định dạng Action. Dừng an toàn.")
            print(f"Trả lời: {b['final']}")
            return

        print(f"Observation: {b['observation']}")


if __name__ == "__main__":
    print("=" * 50)
    print("ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT")
    print("=" * 50)

    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"LLM Provider: {provider.__class__.__name__} (Model: {model_name})")
    print(f"Tools sẵn có: {', '.join(AVAILABLE_TOOLS)}")

    tests = load_test_cases()
    print(f"Đã tải {len(tests)} test cases từ config/test_cases.json")

    # Chạy 1 test case: python src/app.py 3
    # Chạy tất cả:     python src/app.py all
    arg = sys.argv[1] if len(sys.argv) > 1 else "3"

    if arg == "all":
        selected = tests
    else:
        selected = [t for t in tests if str(t["id"]) == arg] or [tests[0]]

    for case in selected:
        print("\n" + "=" * 50)
        print(f"TEST CASE {case['id']} - {case['category']}")
        print("=" * 50)

        print("\n--- DEMO 1: CHATBOT BASELINE ---")
        run_baseline_chatbot(case["question"], provider)

        print("\n--- DEMO 2: REACT AGENT ---")
        run_react_agent(case["question"], provider)
