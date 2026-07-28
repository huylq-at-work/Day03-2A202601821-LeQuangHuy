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


# Bật bằng LOG_PROMPT=1 trong .env để soi đúng thứ gửi lên LLM.
# Cần cho tiêu chí Observability: chứng minh Agent chạy bằng prompt thật,
# không phải kết quả hardcode.
LOG_PROMPT = os.getenv("LOG_PROMPT", "").strip().lower() in ("1", "true", "yes", "on")


def log_prompt(system_prompt: str, user_prompt: str, nhan: str = ""):
    """In nguyên văn prompt gửi lên LLM (chỉ khi LOG_PROMPT bật)."""
    if not LOG_PROMPT:
        return
    print(f"\n{'~' * 62}")
    print(f"PROMPT GỬI LÊN LLM {nhan}")
    print(f"{'~' * 62}")
    print("--- SYSTEM PROMPT ---")
    print(system_prompt.strip() or "(rỗng)")
    print("--- USER / HISTORY ---")
    print(user_prompt.strip())
    print("~" * 62)


def run_baseline_chatbot(user_query: str, provider):
    """Chatbot gốc: hỏi thẳng LLM, không có tool nào."""
    print(f"\n[CHATBOT BASELINE] Câu hỏi: {user_query}")
    log_prompt(CHATBOT_BASELINE_PROMPT, user_query, "(Chatbot baseline)")
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


# ===========================================================================
# 🎁 BONUS — AI CẤP 4: AUTONOMOUS AGENT
# Cấp 3 (ReAct) chỉ phản ứng từng bước. Cấp 4 thêm hai năng lực:
#   - Planning: tự chia mục tiêu thành các bước nhỏ TRƯỚC khi hành động
#   - Memory  : nhớ dữ kiện đã tra, lượt sau không phải gọi lại tool
# ===========================================================================

# Tool chỉ đọc dữ liệu -> an toàn để nhớ lại kết quả.
# dang_ky_hoc_vien GHI dữ liệu nên TUYỆT ĐỐI không được cache.
TOOL_CHI_DOC = {"get_learner", "search_courses", "get_course_detail",
                "check_suitability", "get_provider", "compare_courses", "list_topics"}


class BoNho:
    """
    Memory cho Agent Cấp 4.

    Nhớ kết quả các tool chỉ-đọc đã gọi trong phiên. Sang lượt hội thoại sau,
    Agent hỏi lại cùng thứ thì lấy từ bộ nhớ thay vì gọi tool lần nữa.
    """

    def __init__(self):
        self.cache = {}       # {(ten_tool, tham_so): observation}
        self.so_lan_dung = 0  # đếm số lần thực sự tiết kiệm được một lần gọi tool

    def _khoa(self, ten_tool, args):
        return (ten_tool, tuple(args))

    def nho_lai(self, ten_tool, args):
        """Trả observation đã nhớ, hoặc None nếu chưa từng gọi."""
        if ten_tool not in TOOL_CHI_DOC:
            return None
        obs = self.cache.get(self._khoa(ten_tool, args))
        if obs is not None:
            self.so_lan_dung += 1
        return obs

    def ghi_nho(self, ten_tool, args, observation):
        # Không nhớ kết quả lỗi — lần sau có thể người dùng nhập đúng
        if ten_tool in TOOL_CHI_DOC and not observation.strip().upper().startswith("LỖI"):
            self.cache[self._khoa(ten_tool, args)] = observation

    def tom_tat(self):
        if not self.cache:
            return "(chưa nhớ gì)"
        return "; ".join(f"{t}[{', '.join(a)}]" for t, a in self.cache)

    def xoa(self):
        self.cache.clear()
        self.so_lan_dung = 0


def lap_ke_hoach(user_query: str, provider, lich_su=None):
    """
    Planning cho Agent Cấp 4: tự rã mục tiêu thành các bước nhỏ trước khi hành động.

    Trả về danh sách bước dạng chuỗi. Lỗi thì trả list rỗng — Agent vẫn chạy
    bình thường theo ReAct, chỉ mất phần lập kế hoạch.
    """
    ngu_canh = ""
    for q, a in (lich_su or [])[-2:]:
        ngu_canh += f"- Đã hỏi: {q}\n"

    nhac = (
        "Bạn là bộ phận lập kế hoạch của một trợ lý tư vấn khóa học.\n"
        "Chia yêu cầu của người dùng thành TỐI ĐA 4 bước ngắn gọn, mỗi bước một dòng,\n"
        "đánh số 1. 2. 3. — không giải thích, không viết gì thêm.\n"
        "Nếu yêu cầu đơn giản, chỉ cần 1 bước.\n\n"
        "Các công cụ có thể dùng: " + ", ".join(AVAILABLE_TOOLS) + "\n\n"
        + (f"Ngữ cảnh trước đó:\n{ngu_canh}\n" if ngu_canh else "")
        + f"Yêu cầu: {user_query}"
    )
    try:
        tra_loi = provider.generate(nhac, system_prompt="")
    except Exception:
        return []

    buoc = []
    for dong in (tra_loi or "").splitlines():
        dong = dong.strip()
        if re.match(r"^\d+[.)]\s+", dong):
            buoc.append(re.sub(r"^\d+[.)]\s+", "", dong))
    return buoc[:4]


def react_steps(user_query: str, provider, lich_su=None, bo_nho=None, ke_hoach=None):
    """
    Chạy vòng lặp ReAct và trả về danh sách bước dạng dict.

    Đây là phần lõi dùng chung: run_react_agent() in ra terminal,
    còn web_ui.py dựng giao diện — cả hai đều gọi hàm này nên không
    bao giờ lệch logic.

    lich_su: danh sách [(câu hỏi, câu trả lời)] của các lượt trước,
             để hội thoại nhiều lượt vẫn nhớ ngữ cảnh.
    bo_nho:  đối tượng BoNho (Cấp 4). Có thì tái dùng kết quả tool đã tra.
    ke_hoach: danh sách bước do lap_ke_hoach() sinh ra (Cấp 4).
    """
    buoc = []
    history = ""
    for q, a in (lich_su or []):
        history += f"Câu hỏi: {q}\nFinal Answer: {a}\n"
    history += f"Câu hỏi: {user_query}\n"

    if ke_hoach:
        history += ("Kế hoạch đã vạch sẵn, hãy bám theo:\n"
                    + "\n".join(f"  {i}. {b}" for i, b in enumerate(ke_hoach, 1)) + "\n")

    for vong in range(1, MAX_ITERATIONS + 1):
        # 1. Hỏi LLM xem bước tiếp theo làm gì
        log_prompt(REACT_SYSTEM_PROMPT, history, f"(ReAct — vòng {vong}/{MAX_ITERATIONS})")
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

        # 4. Gọi tool thật — hoặc lấy lại từ bộ nhớ nếu đã tra rồi (Cấp 4)
        tu_bo_nho = False
        observation = bo_nho.nho_lai(tool_name, tool_args) if bo_nho else None
        if observation is not None:
            tu_bo_nho = True
        else:
            observation = call_tool(tool_name, tool_args)
            if bo_nho:
                bo_nho.ghi_nho(tool_name, tool_args, observation)

        buoc.append({"vong": vong, "loai": "tool", "raw": reply, "thought": thought,
                     "tool": tool_name, "args": tool_args, "observation": observation,
                     "loi": observation.strip().upper().startswith("LỖI"),
                     "tu_bo_nho": tu_bo_nho})

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


def run_autonomous_agent(user_query: str, provider, bo_nho=None, lich_su=None):
    """
    🎁 BONUS — Agent Cấp 4: Planning + Memory.

    Khác run_react_agent() ở hai chỗ:
      1. Lập kế hoạch trước rồi mới vào vòng lặp
      2. Dùng BoNho để không gọi lại tool đã tra
    """
    print(f"\n[AUTONOMOUS AGENT] Câu hỏi: {user_query}")

    ke_hoach = lap_ke_hoach(user_query, provider, lich_su)
    if ke_hoach:
        print("\n--- 📋 PLANNING: tự chia mục tiêu ---")
        for i, b in enumerate(ke_hoach, 1):
            print(f"  {i}. {b}")
    else:
        print("\n--- 📋 PLANNING: không lập được kế hoạch, chạy ReAct thường ---")

    if bo_nho is None:
        bo_nho = BoNho()
    truoc = bo_nho.so_lan_dung

    for b in react_steps(user_query, provider, lich_su, bo_nho, ke_hoach):
        if b["loai"] == "guardrail":
            print(f"\n[GUARDRAIL] Đã chạm giới hạn {MAX_ITERATIONS} bước, ngắt lặp an toàn.")
            print(f"Trả lời: {b['final']}")
            return bo_nho

        print(f"\n--- Vòng lặp ReAct (Step {b['vong']}/{MAX_ITERATIONS}) ---")
        print(b["raw"])
        if b["loai"] == "final":
            break
        if b["loai"] == "sai_dinh_dang":
            print("[!] LLM không sinh đúng định dạng Action. Dừng an toàn.")
            print(f"Trả lời: {b['final']}")
            return bo_nho
        nguon = " 🧠 (lấy từ bộ nhớ, không gọi tool)" if b.get("tu_bo_nho") else ""
        print(f"Observation: {b['observation']}{nguon}")

    tiet_kiem = bo_nho.so_lan_dung - truoc
    print(f"\n--- 🧠 MEMORY: đang nhớ {len(bo_nho.cache)} kết quả tool"
          f"{f', tiết kiệm {tiet_kiem} lần gọi ở lượt này' if tiet_kiem else ''} ---")
    return bo_nho


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

    # python src/app.py 3      -> chạy test case số 3
    # python src/app.py all    -> chạy cả 5 test case
    # python src/app.py auto   -> 🎁 demo Agent Cấp 4 (Planning + Memory)
    arg = sys.argv[1] if len(sys.argv) > 1 else "3"

    if arg == "auto":
        print("\n" + "=" * 50)
        print("🎁 BONUS — AI CẤP 4: AUTONOMOUS AGENT")
        print("=" * 50)
        print("Hai lượt hỏi cùng một học viên. Lượt 2 phải lấy hồ sơ từ bộ nhớ,")
        print("không gọi lại get_learner — đó là điểm khác so với Cấp 3.")

        bo_nho = BoNho()
        q1 = "Em là 0912345203, em muốn học AI thì nên đăng ký khóa nào?"
        q2 = "Thế với ngân sách đó em học được môn thiết kế nào không?"

        print("\n" + "-" * 50)
        print("LƯỢT 1")
        print("-" * 50)
        bo_nho = run_autonomous_agent(q1, provider, bo_nho)

        print("\n" + "-" * 50)
        print("LƯỢT 2 (bộ nhớ đã có sẵn hồ sơ học viên)")
        print("-" * 50)
        run_autonomous_agent(q2, provider, bo_nho, lich_su=[(q1, "")])
        sys.exit(0)

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
