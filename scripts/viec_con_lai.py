"""
Liet ke moi cho con phai dien tay trong repo.

Danh dau bang chuoi [[CAN-DIEN]] ngay tren muc can dien.

Chay:  .venv\\Scripts\\python.exe scripts\\viec_con_lai.py
"""

import os
import sys

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

MARKER = "[[CAN-DIEN]]"
# Bo qua scripts/ vi do la noi SINH RA dau, khong phai cho can dien.
# Dong co dau trong dau backtick la dang nhac den no trong tai lieu, khong tinh.
BO_QUA_THU_MUC = {".git", ".venv", "__pycache__", "node_modules", "scripts"}


def la_nhac_den(dong: str) -> bool:
    """True neu dau nam trong `...` — tuc la dang viet tai lieu ve no."""
    truoc = dong.split(MARKER)[0]
    return truoc.count("`") % 2 == 1


tim_thay = []
for goc, thu_muc, files in os.walk(_BASE):
    thu_muc[:] = [d for d in thu_muc if d not in BO_QUA_THU_MUC]
    for ten in files:
        if not ten.endswith((".md", ".json", ".mermaid", ".txt")):
            continue
        duong_dan = os.path.join(goc, ten)
        try:
            with open(duong_dan, encoding="utf-8") as f:
                for so, dong in enumerate(f, 1):
                    if MARKER in dong and not la_nhac_den(dong):
                        tim_thay.append((os.path.relpath(duong_dan, _BASE), so,
                                         dong.replace(MARKER, "").strip(" #>*-\n")))
        except Exception:
            continue

print("=" * 66)
print("  NHỮNG CHỖ CÒN PHẢI ĐIỀN TAY")
print("=" * 66)

if not tim_thay:
    print("\n  Không còn chỗ nào. Xong hết rồi.\n")
else:
    for i, (f, so, mo_ta) in enumerate(tim_thay, 1):
        print(f"\n  {i}. {f}  (dòng {so})")
        print(f"     {mo_ta}")
    print(f"\n  Tổng: {len(tim_thay)} chỗ")
    print(f"\n  Mở nhanh: code {tim_thay[0][0]}")

print("=" * 66)
