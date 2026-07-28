"""
Chạy thật cả 5 test case rồi ghi trace log vào docs/trace_eval.md.

Giữ nguyên phần Scoring Matrix (mục 1) do Role 1 tự viết, chỉ sinh lại mục 2
là phần trace log — vốn bắt buộc phải là output thật của chương trình.

Chạy:  .venv\\Scripts\\python.exe scripts\\gen_trace_eval.py
Cần có API key thật trong .env, chạy bằng MockProvider sẽ ra trace giả lập.
"""

import json
import os
import sys

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_BASE, "src"))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from providers import get_llm_provider          # noqa: E402
from prompts import CHATBOT_BASELINE_PROMPT, MAX_ITERATIONS  # noqa: E402
from app import react_steps                     # noqa: E402

OUT = os.path.join(_BASE, "docs", "trace_eval.md")
TESTS = os.path.join(_BASE, "config", "test_cases.json")

provider = get_llm_provider()
ten_provider = provider.__class__.__name__
if ten_provider == "MockProvider":
    print("[!] Đang dùng MockProvider — trace sinh ra là giả lập, KHÔNG dùng để nộp bài.")
    print("    Điền API key thật vào .env rồi chạy lại.")

with open(TESTS, encoding="utf-8") as f:
    cases = json.load(f)


def nhan_xet(steps):
    """Tự sinh nhận xét dựa trên các bước Agent thực sự đã chạy."""
    so_tool = sum(1 for b in steps if b["loai"] == "tool")
    ten_tool = [b["tool"] for b in steps if b["loai"] == "tool"]
    co_loi = any(b.get("loi") for b in steps)
    guardrail = any(b["loai"] == "guardrail" for b in steps)
    sai_dd = any(b["loai"] == "sai_dinh_dang" for b in steps)

    tu_choi = any("ngoài phạm vi" in (b.get("thought") or "").lower() for b in steps)

    y = []
    if so_tool == 0:
        if tu_choi:
            y.append("Agent **từ chối vì ngoài phạm vi** (guardrail mục 1C), không gọi tool nào")
        else:
            y.append("Agent tự nhận không cần tool, trả lời thẳng — đúng với câu đơn giản")
    else:
        y.append(f"Gọi {so_tool} tool theo thứ tự: {' -> '.join(ten_tool)}")
    if co_loi:
        y.append("Tool trả `LỖI:` và Agent **không bịa dữ liệu thay thế**")
    if guardrail:
        y.append(f"**Guardrail ngắt** sau {MAX_ITERATIONS} vòng")
    if sai_dd:
        y.append("LLM sinh sai định dạng, vòng lặp dừng an toàn")
    if not guardrail and not sai_dd:
        y.append(f"Kết thúc bằng Final Answer trong {len(steps)}/{MAX_ITERATIONS} vòng")
    return ". ".join(y) + "."


phan = []
for case in cases:
    q = case["question"]
    print(f"Đang chạy test case {case['id']}...")

    try:
        baseline = provider.generate(q, system_prompt=CHATBOT_BASELINE_PROMPT).strip()
    except Exception as e:
        baseline = f"[Lỗi gọi LLM]: {e}"

    steps = react_steps(q, provider)

    dong = []
    for b in steps:
        if b.get("thought"):
            dong.append(f"Thought: {b['thought']}")
        if b["loai"] == "tool":
            dong.append(f"Action: {b['tool']}[{', '.join(b['args'])}]")
            dong.append(f"Observation: {b['observation']}")
        elif b["loai"] == "guardrail":
            dong.append(f"[GUARDRAIL] Chạm giới hạn {MAX_ITERATIONS} vòng, ngắt lặp an toàn.")
            dong.append(f"Final Answer: {b['final']}")
        elif b.get("final"):
            dong.append(f"Final Answer: {b['final']}")

    phan.append(
        f"### Test Case {case['id']} — {case['category']}\n\n"
        f"**Câu hỏi**: {q}\n\n"
        f"**Kỳ vọng**: {case['expected_behavior']}\n\n"
        f"#### Chatbot baseline (không có tool)\n\n"
        f"> {baseline.replace(chr(10), chr(10) + '> ')}\n\n"
        f"#### ReAct Agent\n\n```\n" + "\n".join(dong) + "\n```\n\n"
        f"**Nhận xét**: {nhan_xet(steps)}\n"
    )

# Chỉ thay phần nằm giữa 2 mốc dưới đây. Mọi nội dung do người khác viết thêm
# (mục 3 trở đi) được giữ nguyên — script này không được phép xóa bài của ai.
BAT_DAU = "<!-- BEGIN AUTO-TRACE -->"
KET_THUC = "<!-- END AUTO-TRACE -->"

cu = ""
if os.path.exists(OUT):
    with open(OUT, encoding="utf-8") as f:
        cu = f.read()

if BAT_DAU in cu and KET_THUC in cu:
    dau = cu.split(BAT_DAU)[0].rstrip()
    duoi = cu.split(KET_THUC, 1)[1].lstrip()
else:
    # Lần đầu chạy: mục 1 là phần đầu, từ mục 3 trở đi là phần đuôi cần giữ
    dau = cu.split("## 2.")[0].rstrip() if "## 2." in cu else \
        "# 🟢 Role 1: Đánh Giá Agentic Fit & Trace Log"
    duoi = ""
    for moc in ("## 3.", "## 4."):
        if moc in cu:
            duoi = moc + cu.split(moc, 1)[1].lstrip(moc).rstrip() + "\n"
            break

mo_hinh = getattr(provider, "model_name", "?")
than = (
    f"{dau}\n\n"
    f"{BAT_DAU}\n\n"
    f"## 2. Trace Log — output thật của chương trình\n\n"
    f"> Sinh tự động bằng `scripts/gen_trace_eval.py`, chạy trên "
    f"`{ten_provider}` (model `{mo_hinh}`) với `MAX_ITERATIONS = {MAX_ITERATIONS}`.\n"
    f"> Chạy lại script là ra lại toàn bộ log này — không chép tay.\n\n"
    + "\n---\n\n".join(phan)
    + "\n---\n\n### 2.6. Kết luận nhanh\n\n"
    "Trên các câu cần dữ liệu thật, Chatbot baseline chỉ đưa lời khuyên chung vì không "
    "truy cập được hồ sơ học viên hay danh mục khóa học. ReAct Agent gọi tool tra đúng "
    "dữ liệu rồi mới kết luận, và nêu được lý do cụ thể khi học viên không đủ điều kiện.\n\n"
    "Ngược lại, với câu hỏi kiến thức chung thì Chatbot trả lời tốt mà không cần tool — "
    "đây là lý do cần luồng Hybrid trong `docs/hybrid_flowchart.mermaid` thay vì đẩy mọi "
    "câu hỏi qua Agent.\n\n"
    f"{KET_THUC}\n"
)

if duoi:
    than += "\n---\n\n" + duoi

with open(OUT, "w", encoding="utf-8") as f:
    f.write(than)

print(f"\nĐã ghi {OUT}")
print(f"  {len(cases)} test case, provider: {ten_provider}")
