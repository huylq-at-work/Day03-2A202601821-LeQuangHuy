"""
Bảng điều khiển cho Role 4 (Integrator): chạy cả 4 bộ test, tổng hợp coverage.

Chạy:.venv\\Scripts\\python.exe tests\\run_all.py
"""

import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

VAI = [
    ("test_role1.py", "Role 1  Đạt", "test_cases.json + docs"),
    ("test_role2.py", "Role 2  Hướng", "src/tools.py"),
    ("test_role3.py", "Role 3  Liên", "src/prompts.py"),
    ("test_role4.py", "Role 4  Huy", "src/app.py"),
]

ket_qua = []
for tep, ten, file_giu in VAI:
    r = subprocess.run([sys.executable, os.path.join(_HERE, tep)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = r.stdout or ""
    m = re.search(r"COVERAGE: (\d+)/(\d+)", out)
    dat, tong = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    can_sua = re.findall(r"^\s{4}\d+\. (.+)$", out, re.M)
    ket_qua.append((ten, file_giu, dat, tong, can_sua, tep))

print("=" * 70)
print("BẢNG ĐIỀU KHIỂN — TIẾN ĐỘ CẢ NHÓM")
print("=" * 70)
print()
print(f"{'Vai trò':<16}{'File giữ':<26}{'Coverage':>14}")
print("" + "-" * 58)

t_dat = t_tong = 0
for ten, file_giu, dat, tong, _, _ in ket_qua:
    t_dat += dat
    t_tong += tong
    pct = round(dat / tong * 100) if tong else 0
    thanh = "#" * (pct // 10) + "." * (10 - pct // 10)
    print(f"{ten:<16}{file_giu:<26}{thanh} {dat:>2}/{tong:<2} {pct:>3}%")

print("" + "-" * 58)
pct = round(t_dat / t_tong * 100) if t_tong else 0
print(f"{'TỔNG':<42}{t_dat:>2}/{t_tong:<2} {pct:>3}%")
print()

for ten, _, dat, tong, can_sua, tep in ket_qua:
    if not can_sua:
        print(f"{ten}: xong hết")
        continue
    print(f"\n  {ten} — còn {len(can_sua)} việc:")
    for x in can_sua[:5]:
        print(f"- {x[:100]}")
    if len(can_sua) > 5:
        print(f"... và {len(can_sua) - 5} việc nữa: python tests/{tep}")

print()
print("=" * 70)
print("Chạy riêng từng vai:  python tests/test_role1.py")
print("=" * 70)
sys.exit(0 if t_dat == t_tong else 1)
