"""
Tool registry cho ReAct Agent tư vấn đăng ký khóa học.

Dữ liệu được đọc từ ``config/mock_database.json`` để mọi tool cùng sử dụng
một nguồn thông tin và ngày kiểm thử cố định.
"""

import json
import os
from typing import Optional


_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATABASE_PATH = os.path.join(_BASE, "config", "mock_database.json")

# File JSON chỉ được đọc một lần khi module tools.py được import.
# Sau bước này, các tool tra cứu dictionary trong RAM chứ không mở lại file.
with open(_DATABASE_PATH, "r", encoding="utf-8") as database_file:
    _DB = json.load(database_file)

# Tách từng "bảng" trong JSON thành biến toàn cục dùng chung cho các tool.
LEARNERS = _DB["learners"]
COURSES = _DB["courses"]
PROVIDERS = _DB["providers"]
INSTRUCTORS = _DB["instructors"]

# Học viên đăng ký mới lưu riêng, KHÔNG ghi đè mock_database.json.
# Giữ file gốc bất biến để scripts/gen_database.py luôn tái lập được
# và bộ test của Role 1 không bị lệch kết quả.
_HOC_VIEN_MOI_PATH = os.path.join(_BASE, "config", "hoc_vien_moi.json")

if os.path.exists(_HOC_VIEN_MOI_PATH):
    try:
        with open(_HOC_VIEN_MOI_PATH, "r", encoding="utf-8") as f:
            LEARNERS.update(json.load(f))
    except Exception:
        pass

CAP_DO = _DB["_meta"]["cap_do"]
NGAY_HIEN_TAI = _DB["_meta"]["ngay_hien_tai"]


# ---------------------------------------------------------------------------
# HÀM HỖ TRỢ NỘI BỘ
# Các hàm bắt đầu bằng "_" không được đăng ký cho AI gọi trực tiếp.
# Chúng chỉ chuẩn hóa dữ liệu hoặc dùng lại logic chung cho các tool bên dưới.
# ---------------------------------------------------------------------------

def _clean(value: object) -> str:
    """Chuẩn hóa tham số chuỗi do Agent truyền vào."""
    return "" if value is None else str(value).strip()


def _money(value: int) -> str:
    """Định dạng số tiền theo đơn vị đồng."""
    return f"{value:,}đ"


def _parse_price(value: object) -> Optional[int]:
    """Đổi giá dạng số hoặc chuỗi có dấu phân cách về số nguyên."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value if value >= 0 else None
    if isinstance(value, float):
        return int(value) if value >= 0 and value.is_integer() else None

    text = _clean(value).lower()
    for token in ("vnđ", "vnd", "đ", " "):
        text = text.replace(token, "")
    text = text.replace(",", "").replace(".", "").replace("_", "")
    if not text.isdigit():
        return None
    return int(text)


# Cách người dùng diễn đạt "không giới hạn ngân sách". Để trống cũng tính là không giới hạn.
KHONG_GIOI_HAN = {
    "", "không giới hạn", "khong gioi han", "ko giới hạn", "ko gioi han",
    "không có giới hạn", "bao nhiêu cũng được", "bao nhieu cung duoc",
    "bao nhiêu cũng đc", "tùy", "tuy", "không rõ", "khong ro", "chưa rõ",
    "thoải mái", "thoai mai", "unlimited", "any", "none", "null", "-",
}


def _parse_ngan_sach(value: object):
    """
    Đọc ngân sách, chấp nhận cả trường hợp không giới hạn.

    Returns:
        (gia_tri, hop_le) — gia_tri là None nghĩa là KHÔNG GIỚI HẠN.
        hop_le = False khi người dùng nhập bậy (chữ vô nghĩa, số âm).
    """
    if _clean(value).casefold() in KHONG_GIOI_HAN:
        return None, True
    so = _parse_price(value)
    if so is None or so <= 0:
        return None, False
    return so, True


def _mo_ta_ngan_sach(gia_tri) -> str:
    """Hiển thị ngân sách cho người đọc, None thì ghi rõ là không giới hạn."""
    return "không giới hạn" if gia_tri is None else _money(gia_tri)


def _course(ma_khoa: object):
    """Lấy khóa học theo mã đã chuẩn hóa, không phân biệt hoa thường."""
    code = _clean(ma_khoa).upper()
    return code, COURSES.get(code)


def _provider(ma_ncc: object):
    """Lấy nhà cung cấp theo mã đã chuẩn hóa, không phân biệt hoa thường."""
    code = _clean(ma_ncc).upper()
    return code, PROVIDERS.get(code)


def _buoi_cua(lich: str) -> str:
    """Quy đổi ``T2 19:00-21:00`` thành ``T2 tối``."""
    thu, khoang_gio = lich.split(maxsplit=1)
    gio_bat_dau = int(khoang_gio.split(":", 1)[0])
    if gio_bat_dau < 12:
        buoi = "sáng"
    elif gio_bat_dau < 18:
        buoi = "chiều"
    else:
        buoi = "tối"
    return f"{thu} {buoi}"


def _certificate(value: bool) -> str:
    """Đổi giá trị True/False thành câu mô tả chứng chỉ dễ đọc."""
    return "có chứng chỉ" if value else "không có chứng chỉ"


# ---------------------------------------------------------------------------
# TOOL ĐỌC HỒ SƠ HỌC VIÊN
# AI truyền SĐT vào; Python tra LEARNERS trong RAM và chỉ trả đúng một hồ sơ.
# ---------------------------------------------------------------------------

def get_learner(sdt: str) -> str:
    """
    Tra cứu hồ sơ học viên theo số điện thoại.

    Dùng tool này ĐẦU TIÊN khi câu hỏi có xuất hiện số điện thoại. Kết quả
    cung cấp mục tiêu, trình độ, ngân sách, lịch rảnh và khu vực để Agent
    dùng làm ràng buộc cho các bước tìm và kiểm tra khóa học tiếp theo.

    Args:
        sdt (str): Số điện thoại học viên, ví dụ ``0912345203``.

    Returns:
        str: Hồ sơ tóm tắt của học viên, hoặc chuỗi bắt đầu bằng ``LỖI:``
        nếu thiếu số điện thoại hay không tìm thấy học viên.
    """
    # Chuẩn hóa SĐT trước khi dùng làm khóa tra dictionary.
    phone = _clean(sdt)
    if not phone:
        return "LỖI: Thiếu tham số số điện thoại."

    # dict.get() trả None nếu SĐT không tồn tại, tránh phát sinh KeyError.
    learner = LEARNERS.get(phone)
    if learner is None:
        return f"LỖI: Không tìm thấy học viên có số điện thoại '{phone}'."

    # Tool chỉ trả 5 nhóm ràng buộc cần thiết, không đưa toàn bộ DB cho AI.
    return (
        f"{learner['ho_ten']} — mục tiêu: {', '.join(learner['muc_tieu'])}; "
        f"trình độ: {learner['trinh_do']}; "
        f"ngân sách: {_mo_ta_ngan_sach(learner['ngan_sach'])}; "
        f"rảnh: {', '.join(learner['lich_ranh'])}; "
        f"khu vực: {learner['khu_vuc']}."
    )


# ---------------------------------------------------------------------------
# TOOL TÌM KHÓA HỌC
# Lọc danh sách COURSES bằng chủ đề và trần giá, sau đó trả tối đa 15 kết quả.
# ---------------------------------------------------------------------------

def search_courses(chu_de: str, gia_toi_da: int) -> str:
    """
    Tìm các khóa có chủ đề khớp và giá không vượt quá ngân sách.

    Dùng tool này SAU ``get_learner``: lấy một mục tiêu trong ``muc_tieu``
    làm ``chu_de`` và lấy ``ngan_sach`` làm ``gia_toi_da``. Chủ đề phải
    khớp với một phần tử trong mảng ``chu_de`` của khóa học.

    Args:
        chu_de (str): Chủ đề cần học, ví dụ ``AI`` hoặc ``dữ liệu``.
        gia_toi_da (int): Mức giá tối đa bằng VNĐ, ví dụ ``2000000``.

    Returns:
        str: Danh sách ngắn gồm mã, tên, giá, hình thức và trình độ.
        Không có khóa khớp là kết quả rỗng hợp lệ, không phải lỗi hệ thống.
    """
    # Chuẩn hóa chủ đề và chuyển ngân sách từ chuỗi của AI sang số nguyên.
    topic = _clean(chu_de)
    if not topic:
        return "LỖI: Thiếu tham số chủ đề."

    max_price, hop_le = _parse_ngan_sach(gia_toi_da)
    if not hop_le:
        return ("LỖI: Giá tối đa phải là số dương. "
                "Nếu học viên không giới hạn ngân sách thì để trống tham số này.")

    # Người dùng hỏi mơ hồ ("còn môn khác không?") thì duyệt toàn bộ danh mục
    # thay vì đi tìm đúng chữ "khác" — vốn không phải chủ đề nào cả.
    MO_HO = {"khác", "khac", "môn khác", "mon khac", "tất cả", "tat ca", "toàn bộ",
             "bất kỳ", "gì cũng được", "all", "any", "*"}
    topic_key = topic.casefold()
    tim_tat_ca = topic_key in MO_HO

    matches = []
    # Việc tìm kiếm diễn ra bằng Python trên dữ liệu trong RAM, không phải AI tự
    # đọc file JSON. Mỗi khóa phải đúng chủ đề và không vượt trần giá.
    for code, course in COURSES.items():
        has_topic = tim_tat_ca or any(
            topic_key == _clean(course_topic).casefold()
            for course_topic in course["chu_de"]
        )
        if has_topic and (max_price is None or course["gia"] <= max_price):
            matches.append((course["gia"], code, course))

    if not matches:
        gioi_han = "" if max_price is None else f" dưới {_money(max_price)}"
        return f"Không tìm thấy khóa học nào về '{topic}'{gioi_han}."

    matches.sort(key=lambda item: (item[0], item[1]))

    # 128 khóa mà đổ hết ra thì Observation quá dài, cắt bớt nhưng nói rõ đã cắt
    GIOI_HAN = 15
    if len(matches) > GIOI_HAN:
        con_lai = len(matches) - GIOI_HAN
        matches = matches[:GIOI_HAN]
        phan_du = (f"\n(Hiển thị {GIOI_HAN} khóa rẻ nhất, còn {con_lai} khóa khác. "
                   f"Thu hẹp chủ đề hoặc hạ trần giá để xem chính xác hơn.)")
    else:
        phan_du = ""
    return "\n".join(
        f"{code} - {course['ten']} - {_money(course['gia'])} - "
        f"{course['hinh_thuc']} - {course['trinh_do_yeu_cau']}"
        for _, code, course in matches
    ) + phan_du


# ---------------------------------------------------------------------------
# TOOL DUYỆT DANH MỤC CHỦ ĐỀ
# Tổng hợp chủ đề từ tất cả khóa để xử lý câu hỏi mơ hồ như "có môn gì?".
# ---------------------------------------------------------------------------

def list_topics(gia_toi_da: str = "") -> str:
    """
    Liệt kê tất cả chủ đề đang có trong danh mục kèm số khóa và giá rẻ nhất.

    Dùng tool này khi người dùng hỏi mơ hồ và chưa nêu rõ chủ đề, ví dụ
    "có những khóa gì?", "còn môn nào khác không?", "gợi ý cho tôi vài môn".
    KHÔNG được truyền chữ "khác" hay "tất cả" vào search_courses — dùng tool này.

    Args:
        gia_toi_da (str): Trần giá lọc theo, để trống nghĩa là không lọc.

    Returns:
        str: Danh sách chủ đề, mỗi dòng gồm tên chủ đề, số khóa và giá thấp nhất.
    """
    tran, _ = _parse_ngan_sach(gia_toi_da)

    thong_ke = {}
    # Một khóa có thể thuộc nhiều chủ đề; mỗi chủ đề lưu [số khóa, giá rẻ nhất].
    for course in COURSES.values():
        if tran is not None and course["gia"] > tran:
            continue
        for cd in course["chu_de"]:
            cd = _clean(cd)
            if cd not in thong_ke:
                thong_ke[cd] = [0, course["gia"]]
            thong_ke[cd][0] += 1
            thong_ke[cd][1] = min(thong_ke[cd][1], course["gia"])

    if not thong_ke:
        return f"Không có chủ đề nào có khóa dưới {_money(tran)}."

    dong = [f"{cd}: {so} khóa, từ {_money(gia)}"
            for cd, (so, gia) in sorted(thong_ke.items(), key=lambda x: -x[1][0])]
    dau = f"Có {len(thong_ke)} chủ đề"
    dau += f" với khóa dưới {_money(tran)}" if tran is not None else f" trong {len(COURSES)} khóa"
    return dau + ":\n" + "\n".join(dong)


# ---------------------------------------------------------------------------
# TOOL XEM CHI TIẾT KHÓA
# Tìm một mã khóa và định dạng dữ liệu khác nhau cho online/offline.
# ---------------------------------------------------------------------------

def get_course_detail(ma_khoa: str) -> str:
    """
    Lấy thông tin chi tiết của một khóa học.

    Dùng tool này khi người dùng hỏi thẳng về một mã khóa, hoặc khi Agent
    cần biết lịch, địa điểm, chỗ trống, hạn đăng ký và mã nhà cung cấp
    trước khi tư vấn. Với khóa online, lịch được mô tả là tự học và số chỗ
    là không giới hạn; không trả các giá trị ``None``.

    Args:
        ma_khoa (str): Mã khóa học, ví dụ ``AI301``.

    Returns:
        str: Chi tiết đầy đủ của khóa học, hoặc chuỗi bắt đầu bằng ``LỖI:``
        nếu thiếu mã hay mã khóa không tồn tại.
    """
    # _course() chuẩn hóa mã thành chữ hoa rồi tra COURSES trong RAM.
    code, course = _course(ma_khoa)
    if not code:
        return "LỖI: Thiếu tham số mã khóa học."
    if course is None:
        return f"LỖI: Không tìm thấy khóa học có mã '{code}'."

    first_line = (
        f"{course['ten']} ({_money(course['gia'])}) — "
        f"{course['hinh_thuc']}, {course['thoi_luong']}, "
        f"trình độ {course['trinh_do_yeu_cau']}."
    )

    # Khóa online không có lịch cố định, địa điểm, sĩ số và hạn đăng ký.
    # Tách nhánh để không trả các giá trị None/null cho AI.
    if course["hinh_thuc"] == "online":
        schedule_line = (
            "Lịch: tự học; địa điểm: học trực tuyến. "
            "Không giới hạn chỗ, hạn đăng ký: không áp dụng."
        )
        opening = "Khai giảng: tự học bất kỳ lúc nào."
    else:
        # Khóa offline có sĩ số hữu hạn nên cần tính số chỗ còn lại.
        remaining = max(course["si_so"] - course["da_dang_ky"], 0)
        schedule_line = (
            f"Lịch: {', '.join(course['lich_hoc'])} tại {course['dia_diem']}.\n"
            f"Còn {remaining}/{course['si_so']} chỗ, "
            f"hạn đăng ký {course['han_dang_ky']}."
        )
        opening = f"Khai giảng: {course['khai_giang']}."

    metadata = (
        f"Rating {course['rating']}. {opening} "
        f"{_certificate(course['chung_chi']).capitalize()}. "
        f"Nhà cung cấp: {course['ma_ncc']}; giảng viên: {course['ma_gv']}."
    )
    return f"{first_line}\n{schedule_line}\n{metadata}"


# ---------------------------------------------------------------------------
# TOOL KIỂM TRA ĐỘ PHÙ HỢP
# Đây là logic nghiệp vụ cứng: Python kiểm tra mọi điều kiện và liệt kê lý do.
# AI chỉ nhận kết quả "Phù hợp" hoặc "Không phù hợp", không tự tính thay.
# ---------------------------------------------------------------------------

def check_suitability(sdt: str, ma_khoa: str) -> str:
    """
    Kiểm tra một học viên có phù hợp với một khóa học theo 5 chiều.

    Dùng tool này trước khi khuyên học viên đăng ký. Tool đọc đồng thời hồ
    sơ học viên và khóa học, rồi kiểm tra ngân sách, trình độ, lịch, khu
    vực, chỗ trống và hạn đăng ký. Khóa online bỏ qua lịch, khu vực, chỗ
    và hạn nhưng vẫn phải đạt ngân sách và trình độ.

    Args:
        sdt (str): Số điện thoại học viên.
        ma_khoa (str): Mã khóa học cần kiểm tra.

    Returns:
        str: ``Phù hợp.`` hoặc ``Không phù hợp. Lý do: ...`` với toàn bộ
        lý do cụ thể. Dữ liệu đầu vào không tồn tại trả chuỗi ``LỖI:``.
    """
    # Tool cần đồng thời một hồ sơ học viên và một khóa học hợp lệ.
    phone = _clean(sdt)
    code, course = _course(ma_khoa)
    if not phone or not code:
        return "LỖI: Thiếu tham số số điện thoại hoặc mã khóa học."

    learner = LEARNERS.get(phone)
    if learner is None:
        return f"LỖI: Không tìm thấy học viên có số điện thoại '{phone}'."
    if course is None:
        return f"LỖI: Không tìm thấy khóa học có mã '{code}'."

    reasons = []

    # Chiều 1 - ngân sách:
    # ngan_sach = None nghĩa là học viên không đặt trần giá -> bỏ qua chiều này.
    if learner["ngan_sach"] is not None and course["gia"] > learner["ngan_sach"]:
        reasons.append(
            "vượt ngân sách "
            f"({course['gia']:,} > {learner['ngan_sach']:,})"
        )

    # Chiều 2 - trình độ:
    # So sánh vị trí trong CAP_DO thay vì so sánh chuỗi trực tiếp.
    try:
        learner_level = CAP_DO.index(learner["trinh_do"])
        course_level = CAP_DO.index(course["trinh_do_yeu_cau"])
    except ValueError:
        return "LỖI: Dữ liệu trình độ không hợp lệ trong hệ thống."

    if learner_level < course_level:
        reasons.append(
            "trình độ chưa đạt "
            f"({learner['trinh_do']} < {course['trinh_do_yeu_cau']})"
        )

    # Chiều 3, 4, 5 chỉ áp dụng cho lớp offline.
    # Khóa online tự học nên bỏ qua lịch, khu vực, chỗ và hạn đăng ký.
    if course["hinh_thuc"] == "offline":
        # Chiều 3 - lịch: đổi giờ cụ thể thành buổi rồi so với lịch rảnh.
        try:
            required_sessions = [_buoi_cua(item) for item in course["lich_hoc"]]
        except (AttributeError, IndexError, TypeError, ValueError):
            return f"LỖI: Dữ liệu lịch học của khóa '{code}' không hợp lệ."

        unavailable_sessions = [
            session
            for session in required_sessions
            if session not in learner["lich_ranh"]
        ]
        if unavailable_sessions:
            reasons.append(
                f"lịch không khớp ({', '.join(unavailable_sessions)})"
            )

        # Chiều 4 - khu vực: địa điểm lớp phải trùng khu vực học viên.
        if course["dia_diem"] != learner["khu_vuc"]:
            reasons.append(
                "khác khu vực "
                f"({course['dia_diem']} != {learner['khu_vuc']})"
            )

        # Chiều 5a - chỗ trống: số đã đăng ký phải nhỏ hơn sĩ số.
        if course["da_dang_ky"] >= course["si_so"]:
            reasons.append(
                "lớp đã đầy "
                f"({course['da_dang_ky']}/{course['si_so']})"
            )

        # Chiều 5b - hạn đăng ký: dùng ngày cố định trong mock database.
        if course["han_dang_ky"] < NGAY_HIEN_TAI:
            reasons.append(
                "hết hạn đăng ký "
                f"({course['han_dang_ky']} < {NGAY_HIEN_TAI})"
            )

    # Không có lý do loại nào nghĩa là học viên đáp ứng toàn bộ điều kiện.
    if not reasons:
        return "Phù hợp."
    return f"Không phù hợp. Lý do: {'; '.join(reasons)}."


# ---------------------------------------------------------------------------
# TOOL TRA NHÀ CUNG CẤP
# Nhận mã NCC lấy từ chi tiết khóa và tra bảng PROVIDERS trong RAM.
# ---------------------------------------------------------------------------

def get_provider(ma_ncc: str) -> str:
    """
    Tra cứu uy tín của nhà cung cấp khóa học.

    Dùng tool này sau ``get_course_detail`` khi cần đánh giá đơn vị tổ
    chức. Lấy ``ma_ncc`` từ kết quả chi tiết khóa làm tham số.

    Args:
        ma_ncc (str): Mã nhà cung cấp, ví dụ ``TT02``.

    Returns:
        str: Tên, loại hình, khu vực và đánh giá của nhà cung cấp, hoặc
        chuỗi bắt đầu bằng ``LỖI:`` nếu không tìm thấy.
    """
    code, provider = _provider(ma_ncc)
    if not code:
        return "LỖI: Thiếu tham số mã nhà cung cấp."
    if provider is None:
        return f"LỖI: Không tìm thấy nhà cung cấp có mã '{code}'."

    return (
        f"{provider['ten']} — {provider['loai']} tại "
        f"{provider['khu_vuc']}, đánh giá {provider['danh_gia']}/5."
    )


# ---------------------------------------------------------------------------
# TOOL SO SÁNH KHÓA
# Tra hai mã độc lập rồi đưa các thuộc tính chính về cùng một định dạng.
# ---------------------------------------------------------------------------

def compare_courses(ma1: str, ma2: str) -> str:
    """
    So sánh nhanh hai khóa học cạnh nhau.

    Dùng tool này khi người dùng muốn so sánh hai mã khóa. Cú pháp Action
    bắt buộc là ``compare_courses[PR201, PR202]`` vì hệ thống tách hai
    tham số bằng dấu phẩy.

    Args:
        ma1 (str): Mã khóa học thứ nhất.
        ma2 (str): Mã khóa học thứ hai.

    Returns:
        str: Hai dòng gồm giá, hình thức, thời lượng, trình độ, rating và
        chứng chỉ; hoặc chuỗi ``LỖI:`` nếu một mã không tồn tại.
    """
    code1, course1 = _course(ma1)
    code2, course2 = _course(ma2)
    if not code1 or not code2:
        return "LỖI: Thiếu một trong hai mã khóa học cần so sánh."
    if course1 is None:
        return f"LỖI: Không tìm thấy khóa học có mã '{code1}'."
    if course2 is None:
        return f"LỖI: Không tìm thấy khóa học có mã '{code2}'."

    def summary(code, course):
        return (
            f"{code} {course['ten']}: {_money(course['gia'])}, "
            f"{course['hinh_thuc']}, {course['thoi_luong']}, "
            f"{course['trinh_do_yeu_cau']}, rating {course['rating']}, "
            f"{_certificate(course['chung_chi'])}."
        )

    return f"{summary(code1, course1)}\n{summary(code2, course2)}"


# ---------------------------------------------------------------------------
# TOOL GHI HỒ SƠ HỌC VIÊN MỚI
# Khác các tool trên, hàm này có thay đổi trạng thái: cập nhật RAM và ghi vào
# hoc_vien_moi.json, nhưng vẫn giữ nguyên mock_database.json ban đầu.
# ---------------------------------------------------------------------------

def dang_ky_hoc_vien(sdt: str, ho_ten: str, muc_tieu: str, trinh_do: str,
                     ngan_sach: str, khu_vuc: str, lich_ranh: str) -> str:
    """
    Tạo hồ sơ học viên mới cho người chưa có trong hệ thống.

    Dùng tool này khi get_learner báo không tìm thấy số điện thoại, HOẶC khi
    người dùng nói muốn đăng ký tài khoản mới. TUYỆT ĐỐI không tự bịa thông tin:
    phải hỏi người dùng đủ 7 trường rồi mới được gọi.

    Args:
        sdt (str): Số điện thoại, 10 chữ số, bắt đầu bằng 0 (Ví dụ: '0912345678')
        ho_ten (str): Họ tên đầy đủ
        muc_tieu (str): Chủ đề muốn học, nhiều mục ngăn bằng dấu | (Ví dụ: 'AI|dữ liệu')
        trinh_do (str): Một trong: mới bắt đầu, cơ bản, trung cấp, nâng cao
        ngan_sach (str): Ngân sách tối đa tính bằng đồng (Ví dụ: '5000000')
        khu_vuc (str): Tỉnh/thành đang ở (Ví dụ: 'Hà Nội')
        lich_ranh (str): Các buổi rảnh, ngăn bằng dấu | (Ví dụ: 'T2 tối|CN sáng')

    Returns:
        str: Xác nhận đã tạo hồ sơ, hoặc chuỗi báo lỗi nếu dữ liệu không hợp lệ.
    """
    # Kiểm tra định dạng và tính duy nhất của SĐT trước khi tạo hồ sơ.
    sdt = _clean(sdt)
    if not (sdt.isdigit() and len(sdt) == 10 and sdt.startswith("0")):
        return (f"LỖI: Số điện thoại '{sdt}' không hợp lệ. "
                "Cần đúng 10 chữ số và bắt đầu bằng 0.")

    if sdt in LEARNERS:
        return (f"LỖI: Số điện thoại {sdt} đã có hồ sơ mang tên "
                f"{LEARNERS[sdt]['ho_ten']}. Dùng get_learner để xem thay vì tạo mới.")

    ho_ten = _clean(ho_ten)
    if len(ho_ten) < 2:
        return "LỖI: Thiếu họ tên học viên."

    trinh_do = _clean(trinh_do).lower()
    if trinh_do not in CAP_DO:
        return (f"LỖI: Trình độ '{trinh_do}' không hợp lệ. "
                f"Chỉ nhận: {', '.join(CAP_DO)}.")

    tien, hop_le = _parse_ngan_sach(ngan_sach)
    if not hop_le:
        return (f"LỖI: Ngân sách '{ngan_sach}' không hợp lệ. Cần là số tiền dương, "
                "hoặc ghi 'không giới hạn' nếu học viên không đặt trần giá.")

    # AI truyền danh sách mục tiêu/lịch bằng dấu "|"; vẫn hỗ trợ dấu phẩy.
    def _tach(chuoi):
        return [x.strip() for x in _clean(chuoi).replace(",", "|").split("|") if x.strip()]

    ds_muc_tieu = _tach(muc_tieu)
    ds_lich = _tach(lich_ranh)
    if not ds_muc_tieu:
        return "LỖI: Thiếu mục tiêu học. Ví dụ: 'AI|dữ liệu'."
    if not ds_lich:
        return "LỖI: Thiếu lịch rảnh. Ví dụ: 'T2 tối|CN sáng'."

    ho_so = {
        "ho_ten": ho_ten,
        "muc_tieu": ds_muc_tieu,
        "trinh_do": trinh_do,
        "ngan_sach": tien,
        "lich_ranh": ds_lich,
        "khu_vuc": _clean(khu_vuc) or "Không rõ",
        "hinh_thuc_uu_tien": "cả hai",
        "da_hoc": [],
    }

    # Cập nhật RAM trước để các tool khác dùng được hồ sơ ngay trong phiên chạy.
    LEARNERS[sdt] = ho_so
    try:
        # Ghi riêng học viên mới để lần khởi động sau có thể nạp lại.
        moi = {}
        if os.path.exists(_HOC_VIEN_MOI_PATH):
            with open(_HOC_VIEN_MOI_PATH, "r", encoding="utf-8") as f:
                moi = json.load(f)
        moi[sdt] = ho_so
        with open(_HOC_VIEN_MOI_PATH, "w", encoding="utf-8") as f:
            json.dump(moi, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # Nếu ghi file thất bại, hoàn tác thay đổi RAM để dữ liệu nhất quán.
        del LEARNERS[sdt]
        return f"LỖI: Không lưu được hồ sơ ({e}). Vui lòng thử lại."

    return (f"Đã tạo hồ sơ cho {ho_ten} — số điện thoại {sdt}; "
            f"mục tiêu: {', '.join(ds_muc_tieu)}; trình độ: {trinh_do}; "
            f"ngân sách: {_mo_ta_ngan_sach(tien)}; rảnh: {', '.join(ds_lich)}; "
            f"khu vực: {ho_so['khu_vuc']}. Giờ có thể tìm khóa phù hợp cho học viên này.")


# ---------------------------------------------------------------------------
# TOOL REGISTRY
# app.py lấy tên Action do AI sinh ra, tìm hàm tương ứng trong dictionary này
# rồi gọi hàm với các tham số đã parse. Hàm không có trong registry thì AI
# không thể gọi qua vòng lặp ReAct.
# ---------------------------------------------------------------------------

AVAILABLE_TOOLS = {
    "get_learner": get_learner,
    "search_courses": search_courses,
    "get_course_detail": get_course_detail,
    "check_suitability": check_suitability,
    "get_provider": get_provider,
    "compare_courses": compare_courses,
    "dang_ky_hoc_vien": dang_ky_hoc_vien,
    "list_topics": list_topics,
}
