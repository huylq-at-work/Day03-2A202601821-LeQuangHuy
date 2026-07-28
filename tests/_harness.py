"""
Khung kiểm tra dùng chung cho 4 bộ test của 4 role.
Không cần cài pytest — chạy thẳng bằng python.
"""

import json
import os
import sys

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC = os.path.join(_BASE, "src")
for p in (_BASE, _SRC):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def duong_dan(*phan):
    """Đường dẫn tuyệt đối tính từ gốc repo."""
    return os.path.join(_BASE, *phan)


def nap_database():
    with open(duong_dan("config", "mock_database.json"), encoding="utf-8") as f:
        return json.load(f)


class Check:
    """Đếm số mục đạt, gom danh sách việc còn phải sửa."""

    def __init__(self, tieu_de):
        self.dat = 0
        self.tong = 0
        self.can_sua = []
        print("=" * 64)
        print(f"{tieu_de}")
        print("=" * 64)

    def muc(self, ten):
        print(f"\n{ten}")

    def ok(self, ten, dieu_kien, goi_y=""):
        """Ghi nhận 1 mục kiểm tra. goi_y hiện ở phần 'còn phải sửa' nếu trượt."""
        self.tong += 1
        if dieu_kien:
            self.dat += 1
            print(f"[x] {ten}")
            return True
        print(f"[ ] {ten}")
        self.can_sua.append(goi_y or ten)
        return False

    def thu(self, ten, ham, goi_y=""):
        """Chạy ham(), đạt nếu không văng exception và trả về giá trị thật."""
        self.tong += 1
        try:
            kq = ham()
        except Exception as e:
            print(f"[ ] {ten}  -> CRASH: {type(e).__name__}: {e}")
            self.can_sua.append(goi_y or f"{ten} bị crash: {type(e).__name__}")
            return None
        self.dat += 1
        print(f"[x] {ten}")
        return kq

    def bo_qua(self, ten, ly_do):
        print(f"[-] {ten}  ({ly_do})")

    def ket(self):
        pct = round(self.dat / self.tong * 100) if self.tong else 0
        print()
        print("-" * 64)
        print(f"COVERAGE: {self.dat}/{self.tong} ({pct}%)")
        if self.can_sua:
            print(f"\n  CÒN PHẢI SỬA ({len(self.can_sua)}):")
            for i, x in enumerate(self.can_sua, 1):
                print(f"{i}. {x}")
        else:
            print("\n  Tất cả đạt. Xong phần của bạn!")
        print("-" * 64)
        return self.dat, self.tong
