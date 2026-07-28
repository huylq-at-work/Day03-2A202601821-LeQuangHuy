"""Sinh mock database marketplace khoa hoc ben ngoai: 1000 hoc vien + kiem tra bay."""
import json, random, io, os, sys

try:  # console Windows mac dinh cp1252, khong in duoc tieng Viet
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

random.seed(2026)  # seed co dinh -> chay lai ra y het, test case luon tai lap duoc

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(_BASE, "config", "mock_database.json")
NGAY_HIEN_TAI = "2026-07-28"

CAP = ["mới bắt đầu", "cơ bản", "trung cấp", "nâng cao"]

PROVIDERS = {
    "NT01": {"ten": "EduNow", "loai": "nền tảng online", "khu_vuc": "toàn quốc", "danh_gia": 4.5},
    "NT02": {"ten": "SkillHub", "loai": "nền tảng online", "khu_vuc": "toàn quốc", "danh_gia": 4.3},
    "TT01": {"ten": "Trung tâm Anh ngữ BrightPath", "loai": "trung tâm offline", "khu_vuc": "Hà Nội", "danh_gia": 4.6},
    "TT02": {"ten": "CodeCamp Academy", "loai": "trung tâm offline", "khu_vuc": "Hà Nội", "danh_gia": 4.7},
    "TT03": {"ten": "MarketPro Training", "loai": "trung tâm offline", "khu_vuc": "TP.HCM", "danh_gia": 4.4},
    "NT03": {"ten": "LearnHub", "loai": "nền tảng online", "khu_vuc": "toàn quốc", "danh_gia": 4.2},
    "TT04": {"ten": "Trung tâm Ngoại ngữ Sakura", "loai": "trung tâm offline", "khu_vuc": "TP.HCM", "danh_gia": 4.5},
    "TT05": {"ten": "STEM Academy", "loai": "trung tâm offline", "khu_vuc": "Hà Nội", "danh_gia": 4.6},
}

INSTRUCTORS = {
    "GV01": {"ten": "Nguyễn Minh Anh", "chuyen_mon": ["tiếng Anh", "IELTS"], "danh_gia": 4.7, "kinh_nghiem": 8},
    "GV02": {"ten": "Trần Quốc Bảo", "chuyen_mon": ["lập trình", "web"], "danh_gia": 4.8, "kinh_nghiem": 6},
    "GV03": {"ten": "Lê Thanh Hà", "chuyen_mon": ["AI", "Machine Learning"], "danh_gia": 4.9, "kinh_nghiem": 10},
    "GV04": {"ten": "Phạm Đức Cường", "chuyen_mon": ["dữ liệu", "SQL"], "danh_gia": 4.5, "kinh_nghiem": 5},
    "GV05": {"ten": "Vũ Thị Mai", "chuyen_mon": ["thiết kế", "đồ họa"], "danh_gia": 4.3, "kinh_nghiem": 4},
    "GV06": {"ten": "Đỗ Hoàng Nam", "chuyen_mon": ["marketing", "content"], "danh_gia": 4.4, "kinh_nghiem": 7},
    "GV07": {"ten": "Nguyễn Hải Sơn", "chuyen_mon": ["vật lý", "toán"], "danh_gia": 4.6, "kinh_nghiem": 9},
    "GV08": {"ten": "Trần Thu Hà", "chuyen_mon": ["tiếng Nhật", "tiếng Hàn"], "danh_gia": 4.5, "kinh_nghiem": 6},
    "GV09": {"ten": "Lê Minh Quân", "chuyen_mon": ["tài chính", "kế toán"], "danh_gia": 4.4, "kinh_nghiem": 8},
    "GV10": {"ten": "Phạm Ngọc Lan", "chuyen_mon": ["nhiếp ảnh", "thiết kế"], "danh_gia": 4.3, "kinh_nghiem": 5},
    "GV11": {"ten": "Đỗ Văn Kiên", "chuyen_mon": ["âm nhạc"], "danh_gia": 4.7, "kinh_nghiem": 12},
    "GV12": {"ten": "Vũ Thị Hạnh", "chuyen_mon": ["kỹ năng mềm", "quản trị"], "danh_gia": 4.5, "kinh_nghiem": 7},
}


def on(ma, ten, ncc, chu_de, cap, gia, thoi_luong, hoc_vien, rating, cc, gv):
    """Khoa online: tu hoc, khong gioi han si so, khong co lich/dia diem."""
    return ma, {"ten": ten, "ma_ncc": ncc, "chu_de": chu_de, "trinh_do_yeu_cau": cap,
                "hinh_thuc": "online", "gia": gia, "thoi_luong": thoi_luong,
                "lich_hoc": [], "khai_giang": None, "han_dang_ky": None, "dia_diem": None,
                "si_so": None, "da_dang_ky": hoc_vien, "rating": rating,
                "chung_chi": cc, "ma_gv": gv}


def off(ma, ten, ncc, chu_de, cap, gia, thoi_luong, lich, kg, han, dd, si_so, dk, rating, cc, gv):
    return ma, {"ten": ten, "ma_ncc": ncc, "chu_de": chu_de, "trinh_do_yeu_cau": cap,
                "hinh_thuc": "offline", "gia": gia, "thoi_luong": thoi_luong,
                "lich_hoc": lich, "khai_giang": kg, "han_dang_ky": han, "dia_diem": dd,
                "si_so": si_so, "da_dang_ky": dk, "rating": rating,
                "chung_chi": cc, "ma_gv": gv}


COURSES = dict([
    off("EN101", "Tiếng Anh giao tiếp cơ bản", "TT01", ["tiếng Anh", "giao tiếp"], "mới bắt đầu",
        3_500_000, "24 buổi", ["T2 19:00-21:00", "T4 19:00-21:00"],
        "2026-08-15", "2026-08-10", "Hà Nội", 25, 18, 4.5, False, "GV01"),
    off("EN201", "IELTS 6.5 cấp tốc", "TT01", ["tiếng Anh", "IELTS"], "trung cấp",
        8_000_000, "32 buổi", ["T3 19:00-21:00", "T5 19:00-21:00"],
        "2026-08-20", "2026-08-15", "Hà Nội", 20, 20, 4.7, True, "GV01"),      # HET CHO
    off("EN301", "Tiếng Anh thương mại", "TT01", ["tiếng Anh", "công việc"], "trung cấp",
        5_000_000, "20 buổi", ["T2 19:00-21:00", "T4 19:00-21:00"],
        "2026-07-20", "2026-07-15", "Hà Nội", 20, 14, 4.5, True, "GV01"),      # HET HAN
    on("EN102", "Tiếng Anh giao tiếp online", "NT01", ["tiếng Anh", "giao tiếp"], "mới bắt đầu",
       1_200_000, "30 giờ", 1240, 4.3, True, "GV01"),
    on("PR101", "Nhập môn lập trình Python", "NT01", ["lập trình", "python"], "mới bắt đầu",
       990_000, "25 giờ", 3120, 4.6, True, "GV02"),
    off("PR201", "Lập trình Web Fullstack", "TT02", ["lập trình", "web"], "cơ bản",
        12_000_000, "48 buổi", ["T2 19:00-21:30", "T4 19:00-21:30", "T6 19:00-21:30"],
        "2026-09-01", "2026-08-25", "Hà Nội", 30, 22, 4.8, True, "GV02"),
    on("PR202", "React nâng cao", "NT02", ["lập trình", "web"], "trung cấp",
       2_500_000, "20 giờ", 860, 4.4, True, "GV02"),
    off("AI301", "Machine Learning thực chiến", "TT02", ["AI", "dữ liệu"], "trung cấp",
        15_000_000, "40 buổi", ["T3 19:00-21:00", "T5 19:00-21:00"],
        "2026-08-25", "2026-08-18", "Hà Nội", 25, 9, 4.9, True, "GV03"),
    on("AI302", "AI cho người mới bắt đầu", "NT01", ["AI"], "mới bắt đầu",
       1_500_000, "18 giờ", 2050, 4.2, True, "GV03"),
    on("DA201", "Phân tích dữ liệu với Excel & SQL", "NT02", ["dữ liệu"], "cơ bản",
       1_800_000, "28 giờ", 1470, 4.5, True, "GV04"),
    on("DE101", "Thiết kế đồ họa Canva & Figma", "NT02", ["thiết kế"], "mới bắt đầu",
       1_100_000, "22 giờ", 980, 4.3, False, "GV05"),
    on("MK101", "Content Marketing cơ bản", "NT01", ["marketing"], "mới bắt đầu",
       890_000, "15 giờ", 1630, 4.1, True, "GV06"),
    off("MK201", "Digital Marketing tổng quan", "TT03", ["marketing"], "cơ bản",
        6_000_000, "24 buổi", ["T7 09:00-11:30", "CN 09:00-11:30"],
        "2026-08-22", "2026-08-17", "TP.HCM", 35, 31, 4.4, True, "GV06"),

    # --- Khoa hoc tu nhien ---
    on("PH101", "Vật lý đại cương", "NT03", ["vật lý", "khoa học"], "mới bắt đầu",
       1_200_000, "26 giờ", 740, 4.4, True, "GV07"),
    off("PH201", "Vật lý luyện thi THPT", "TT05", ["vật lý", "khoa học"], "cơ bản",
        4_500_000, "36 buổi", ["T3 19:00-21:00", "T5 19:00-21:00"],
        "2026-09-05", "2026-08-30", "Hà Nội", 30, 17, 4.6, True, "GV07"),
    on("MA101", "Toán cao cấp cơ bản", "NT03", ["toán", "khoa học"], "mới bắt đầu",
       950_000, "24 giờ", 1120, 4.3, True, "GV07"),
    on("MA201", "Toán tư duy cho lập trình", "NT03", ["toán", "lập trình"], "cơ bản",
       1_700_000, "20 giờ", 630, 4.5, True, "GV07"),

    # --- Ngoai ngu khac ---
    off("JP101", "Tiếng Nhật N5", "TT04", ["tiếng Nhật", "ngoại ngữ"], "mới bắt đầu",
        4_200_000, "30 buổi", ["T2 18:30-20:30", "T4 18:30-20:30"],
        "2026-09-08", "2026-09-01", "TP.HCM", 25, 12, 4.5, True, "GV08"),
    on("JP102", "Tiếng Nhật giao tiếp online", "NT03", ["tiếng Nhật", "giao tiếp"], "mới bắt đầu",
       1_350_000, "28 giờ", 880, 4.2, True, "GV08"),
    off("KR101", "Tiếng Hàn sơ cấp", "TT04", ["tiếng Hàn", "ngoại ngữ"], "mới bắt đầu",
        3_900_000, "28 buổi", ["T3 18:30-20:30", "T5 18:30-20:30"],
        "2026-09-08", "2026-09-01", "TP.HCM", 25, 20, 4.4, True, "GV08"),

    # --- Tai chinh, ke toan ---
    on("FI101", "Quản lý tài chính cá nhân", "NT03", ["tài chính"], "mới bắt đầu",
       790_000, "12 giờ", 2410, 4.5, True, "GV09"),
    on("FI201", "Đầu tư chứng khoán cơ bản", "NT02", ["tài chính", "đầu tư"], "cơ bản",
       2_300_000, "22 giờ", 1360, 4.3, True, "GV09"),
    on("AC101", "Kế toán cho người mới", "NT03", ["kế toán"], "mới bắt đầu",
       1_600_000, "30 giờ", 690, 4.4, True, "GV09"),

    # --- Nang khieu, ky nang ---
    on("PT101", "Nhiếp ảnh cơ bản với điện thoại", "NT02", ["nhiếp ảnh"], "mới bắt đầu",
       690_000, "14 giờ", 1580, 4.6, False, "GV10"),
    on("UX201", "Thiết kế UI/UX", "NT02", ["thiết kế", "web"], "cơ bản",
       3_200_000, "32 giờ", 940, 4.7, True, "GV10"),
    off("MU101", "Guitar đệm hát cho người mới", "TT05", ["âm nhạc"], "mới bắt đầu",
        2_800_000, "20 buổi", ["T7 09:00-11:00", "CN 09:00-11:00"],
        "2026-08-29", "2026-08-24", "Hà Nội", 20, 11, 4.8, False, "GV11"),
    on("SK101", "Kỹ năng thuyết trình", "NT01", ["kỹ năng mềm"], "mới bắt đầu",
       1_100_000, "10 giờ", 1930, 4.4, True, "GV12"),
    off("SK201", "Quản trị dự án cho người đi làm", "TT02", ["kỹ năng mềm", "quản trị"], "cơ bản",
        7_500_000, "24 buổi", ["T6 18:30-20:30", "T7 09:00-11:00"],
        "2026-09-12", "2026-09-05", "Hà Nội", 28, 19, 4.6, True, "GV12"),
])

# ---------- Sinh them 100 khoa hoc phu kin cac chu de va cap do ----------
# 28 khoa viet tay o tren giu nguyen vi cac bay phu thuoc vao chung.
CHU_DE_100 = [
    ("Tiếng Anh", "ENX", ["tiếng Anh", "ngoại ngữ"]),
    ("Tiếng Nhật", "JPX", ["tiếng Nhật", "ngoại ngữ"]),
    ("Tiếng Hàn", "KRX", ["tiếng Hàn", "ngoại ngữ"]),
    ("Tiếng Trung", "ZHX", ["tiếng Trung", "ngoại ngữ"]),
    ("Lập trình Python", "PRX", ["lập trình", "python"]),
    ("Lập trình Web", "WBX", ["web", "lập trình"]),
    ("Lập trình Mobile", "MBX", ["mobile", "lập trình"]),
    ("Trí tuệ nhân tạo", "AIX", ["AI", "dữ liệu"]),
    ("Phân tích dữ liệu", "DAX", ["dữ liệu"]),
    ("An toàn thông tin", "SCX", ["bảo mật"]),
    ("Thiết kế đồ họa", "DGX", ["thiết kế"]),
    ("Nhiếp ảnh", "PTX", ["nhiếp ảnh"]),
    ("Digital Marketing", "MKX", ["marketing"]),
    ("Tài chính cá nhân", "FIX", ["tài chính"]),
    ("Kế toán", "ACX", ["kế toán"]),
    ("Kỹ năng mềm", "SKX", ["kỹ năng mềm"]),
    ("Quản trị dự án", "PMX", ["quản trị", "kỹ năng mềm"]),
    ("Vật lý", "PHX", ["vật lý", "khoa học"]),
    ("Toán học", "MAX", ["toán", "khoa học"]),
    ("Âm nhạc", "MUX", ["âm nhạc"]),
]

HAU_TO = ["nhập môn", "cơ bản", "thực hành", "chuyên sâu", "nâng cao"]
CAP_THEO_MUC = ["mới bắt đầu", "mới bắt đầu", "cơ bản", "trung cấp", "nâng cao"]
GIA_THEO_CAP = {"mới bắt đầu": (690_000, 1_800_000), "cơ bản": (1_500_000, 3_500_000),
                "trung cấp": (3_000_000, 7_000_000), "nâng cao": (6_000_000, 14_000_000)}
NCC_ONLINE = ["NT01", "NT02", "NT03"]
NCC_OFFLINE = ["TT01", "TT02", "TT03", "TT04", "TT05"]
GV_THEO_CHU_DE = {"tiếng Anh": "GV01", "tiếng Nhật": "GV08", "tiếng Hàn": "GV08",
                  "tiếng Trung": "GV08", "lập trình": "GV02", "web": "GV02",
                  "mobile": "GV02", "AI": "GV03", "dữ liệu": "GV04", "bảo mật": "GV04",
                  "thiết kế": "GV05", "nhiếp ảnh": "GV10", "marketing": "GV06",
                  "tài chính": "GV09", "kế toán": "GV09", "kỹ năng mềm": "GV12",
                  "quản trị": "GV12", "vật lý": "GV07", "toán": "GV07", "âm nhạc": "GV11"}
CA_HOC = [["T2 19:00-21:00", "T4 19:00-21:00"], ["T3 19:00-21:00", "T5 19:00-21:00"],
          ["T6 18:30-20:30", "T7 09:00-11:00"], ["T7 09:00-11:30", "CN 09:00-11:30"],
          ["T2 18:00-20:00", "T6 18:00-20:00"]]

for ten_cd, tien_to, tags in CHU_DE_100:
    for i, hau_to in enumerate(HAU_TO):
        ma = f"{tien_to}{101 + i}"
        cap = CAP_THEO_MUC[i]
        lo, hi = GIA_THEO_CAP[cap]
        gia = round(random.randint(lo, hi), -4)
        gv = GV_THEO_CHU_DE.get(tags[0], "GV12")
        ten = f"{ten_cd} {hau_to}"

        if i % 3 == 0:  # cu 3 khoa thi co 1 khoa offline
            ncc = random.choice(NCC_OFFLINE)
            si_so = random.randint(20, 40)
            ma_out, kh = off(ma, ten, ncc, tags, cap, gia, f"{random.randint(16, 40)} buổi",
                             random.choice(CA_HOC),
                             f"2026-09-{random.randint(10, 28):02d}",
                             f"2026-09-{random.randint(1, 9):02d}",
                             PROVIDERS[ncc]["khu_vuc"],
                             si_so, random.randint(0, si_so),
                             round(random.uniform(3.9, 4.9), 1),
                             random.random() < 0.75, gv)
        else:
            ncc = random.choice(NCC_ONLINE)
            ma_out, kh = on(ma, ten, ncc, tags, cap, gia, f"{random.randint(10, 40)} giờ",
                            random.randint(80, 3000),
                            round(random.uniform(3.9, 4.9), 1),
                            random.random() < 0.8, gv)
        COURSES[ma_out] = kh

FIXED = {
    "0912345203": {"ho_ten": "Nguyễn Chí Hướng", "muc_tieu": ["AI", "dữ liệu"], "trinh_do": "mới bắt đầu",
                   "ngan_sach": 2_000_000, "lich_ranh": ["T2 tối", "T4 tối"],
                   "khu_vuc": "Hà Nội", "hinh_thuc_uu_tien": "cả hai", "da_hoc": []},
    "0987654387": {"ho_ten": "Nguyễn Tiến Đạt", "muc_tieu": ["tiếng Anh"], "trinh_do": "cơ bản",
                   "ngan_sach": 6_000_000, "lich_ranh": ["T3 tối", "T5 tối"],
                   "khu_vuc": "Hà Nội", "hinh_thuc_uu_tien": "cả hai", "da_hoc": ["PR101"]},
    "0901234795": {"ho_ten": "Phạm Thị Liên", "muc_tieu": ["lập trình", "web"], "trinh_do": "trung cấp",
                   "ngan_sach": 15_000_000, "lich_ranh": ["T2 tối", "T4 tối", "T6 tối"],
                   "khu_vuc": "Hà Nội", "hinh_thuc_uu_tien": "cả hai", "da_hoc": ["PR101", "DA201"]},
    "0977888821": {"ho_ten": "Lê Quang Huy", "muc_tieu": ["marketing"], "trinh_do": "cơ bản",
                   "ngan_sach": 8_000_000, "lich_ranh": ["T7 sáng", "CN sáng"],
                   "khu_vuc": "TP.HCM", "hinh_thuc_uu_tien": "cả hai", "da_hoc": ["PR101"]},
}

# ---------- Sinh 996 hoc vien ngau nhien ----------
HO = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng",
      "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đinh", "Trịnh", "Mai", "Cao"]
DEM = ["Văn", "Thị", "Chí", "Minh", "Tiến", "Quang", "Thanh", "Hữu", "Ngọc", "Anh",
       "Đức", "Thu", "Hoài", "Xuân", "Bảo", "Gia", "Khánh", "Nhật", "Phương", "Trung"]
TEN = ["An", "Bình", "Chi", "Dũng", "Duy", "Giang", "Hà", "Hải", "Hạnh", "Hiếu",
       "Hoa", "Huy", "Hùng", "Hương", "Khoa", "Lan", "Linh", "Long", "Mai", "Nam",
       "Nga", "Ngân", "Nhung", "Phong", "Phúc", "Quân", "Quyên", "Sơn", "Tâm", "Thảo",
       "Thắng", "Thúy", "Tiến", "Toàn", "Trang", "Trâm", "Tuấn", "Tú", "Vy", "Yến"]

CHU_DE = ["tiếng Anh", "lập trình", "AI", "dữ liệu", "thiết kế", "marketing", "web", "IELTS"]
KHU_VUC = ["Hà Nội", "TP.HCM", "Đà Nẵng", "Hải Phòng", "Cần Thơ"]
HINH_THUC = ["online", "offline", "cả hai"]
BUOI = [f"{t} {b}" for t in ["T2", "T3", "T4", "T5", "T6", "T7", "CN"] for b in ["sáng", "chiều", "tối"]]
NGAN_SACH = [500_000, 1_000_000, 2_000_000, 3_000_000, 5_000_000, 8_000_000, 12_000_000, 20_000_000]
ONLINE_IDS = [ma for ma, c in COURSES.items() if c["hinh_thuc"] == "online"]

learners = dict(FIXED)
used = set(FIXED)
dau_so = ["03", "05", "07", "08", "09"]
while len(learners) < 1000:
    sdt = random.choice(dau_so) + "".join(random.choice("0123456789") for _ in range(8))
    if sdt in used:
        continue
    used.add(sdt)
    learners[sdt] = {
        "ho_ten": f"{random.choice(HO)} {random.choice(DEM)} {random.choice(TEN)}",
        "muc_tieu": random.sample(CHU_DE, random.randint(1, 2)),
        "trinh_do": random.choice(CAP[:3]),
        "ngan_sach": random.choice(NGAN_SACH),
        "lich_ranh": random.sample(BUOI, random.randint(2, 4)),
        "khu_vuc": random.choice(KHU_VUC),
        "hinh_thuc_uu_tien": random.choice(HINH_THUC),
        "da_hoc": random.sample(ONLINE_IDS, random.randint(0, 2)),
    }

db = {"_meta": {"ngay_hien_tai": NGAY_HIEN_TAI,
                "cap_do": CAP,
                "ghi_chu": "si_so = null nghia la khoa online khong gioi han cho"},
      "learners": learners, "courses": COURSES,
      "providers": PROVIDERS, "instructors": INSTRUCTORS}

buf = io.StringIO()
buf.write("{\n")
buf.write('  "_meta": ' + json.dumps(db["_meta"], ensure_ascii=False, indent=2).replace("\n", "\n  ") + ",\n\n")
buf.write('  "learners": {\n')
items = list(learners.items())
for i, (k, v) in enumerate(items):
    comma = "," if i < len(items) - 1 else ""
    buf.write(f'    "{k}": {json.dumps(v, ensure_ascii=False, separators=(", ", ": "))}{comma}\n')
buf.write("  },\n\n")
for key in ("courses", "providers", "instructors"):
    body = json.dumps(db[key], ensure_ascii=False, indent=2)
    body = "\n".join("  " + ln for ln in body.splitlines()).lstrip()
    tail = ",\n\n" if key != "instructors" else "\n"
    buf.write(f'  "{key}": {body}{tail}')
buf.write("}\n")

with open(OUT, "w", encoding="utf-8") as f:
    f.write(buf.getvalue())

# ---------- Kiem tra bay ----------
def buoi_cua(lich):
    """'T2 19:00-21:00' -> 'T2 tối'"""
    thu, gio = lich.split(" ", 1)
    h = int(gio[:2])
    return f"{thu} {'sáng' if h < 12 else 'chiều' if h < 18 else 'tối'}"


def kiem_tra(sdt, ma):
    hv, kh = learners[sdt], COURSES[ma]
    loi = []
    if kh["gia"] > hv["ngan_sach"]:
        loi.append(f"vượt ngân sách ({kh['gia']:,} > {hv['ngan_sach']:,})")
    if CAP.index(hv["trinh_do"]) < CAP.index(kh["trinh_do_yeu_cau"]):
        loi.append(f"trình độ chưa đạt ({hv['trinh_do']} < {kh['trinh_do_yeu_cau']})")
    if kh["hinh_thuc"] == "offline":
        thieu = [b for b in map(buoi_cua, kh["lich_hoc"]) if b not in hv["lich_ranh"]]
        if thieu:
            loi.append(f"lịch không khớp ({', '.join(thieu)})")
        if kh["dia_diem"] != hv["khu_vuc"]:
            loi.append(f"khác khu vực ({kh['dia_diem']} vs {hv['khu_vuc']})")
        if kh["si_so"] is not None and kh["da_dang_ky"] >= kh["si_so"]:
            loi.append("lớp đã đầy")
        if kh["han_dang_ky"] and kh["han_dang_ky"] < NGAY_HIEN_TAI:
            loi.append(f"hết hạn đăng ký ({kh['han_dang_ky']})")
    return loi


with open(OUT, encoding="utf-8") as f:
    check = json.load(f)
print(f"learners={len(check['learners'])} courses={len(check['courses'])} "
      f"providers={len(check['providers'])} instructors={len(check['instructors'])} "
      f"size={os.path.getsize(OUT)/1024:.0f}KB")
print()
for sdt, ma in [("0912345203", "AI301"), ("0987654387", "EN101"),
                ("0901234795", "PR201"), ("0977888821", "EN101"),
                ("0977888821", "MK201"), ("0987654387", "EN201"),
                ("0901234795", "EN301")]:
    loi = kiem_tra(sdt, ma)
    ten = learners[sdt]["ho_ten"]
    print(f"{ten:18} + {ma:6} -> " + (f"{len(loi)} lỗi: " + "; ".join(loi) if loi else "PHÙ HỢP"))
