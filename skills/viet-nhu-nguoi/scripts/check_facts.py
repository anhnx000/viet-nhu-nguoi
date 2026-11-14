#!/usr/bin/env python3
"""So bản gốc với bản viết lại: có mất hay thêm số liệu, ngày giờ, link, code, tên riêng không.

Dùng: python3 -I check_facts.py GOC.md MOI.md       (hoặc GOC.pptx MOI.pptx)
Thoát mã 1 nếu số, link hoặc code bị mất hay được thêm. Các mục "xem lại" chỉ cảnh báo, không
đổi mã thoát: tên riêng (sửa câu có thể đổi chữ đứng đầu câu hoặc lược bớt tên lặp lại), số viết
bằng chữ, thứ trong tuần, tháng, và các từ giữ nghĩa ("chưa", "vẫn", "chỉ", "có thể", "khoảng"...).

Số được so theo giá trị: "1.250" và "1250", "12,5%" và "12.5%", "3 khách" và "ba khách" coi là một.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I bỏ thư mục script khỏi sys.path
import slides  # noqa: E402

URL = re.compile(r"https?://[^\s)>\]]+")
CODE = re.compile(r"`([^`\n]+)`")
# 15:00, 30/4, 2026-11-07, 1.000.000, 2.3, 30%, v1.2.0, 5–10
NUMBER = re.compile(r"\bv?\d+(?:[.,:/\-–]\d+)*%?")
ACRONYM = re.compile(r"\b[A-ZĐ]{2,}[0-9]*\b")
UPPER = "A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬĐÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ"
# Từ viết hoa không đứng sau dấu kết câu hay đầu dòng: thường là tên riêng
NAME = re.compile(rf"(?<![.!?:\n>\-*#]\s)(?<!^)(?<=\s)[{UPPER}][\w]+", re.MULTILINE)

NUM_WORDS = {"hai": "2", "ba": "3", "bốn": "4", "năm": "5", "sáu": "6", "bảy": "7", "tám": "8",
             "chín": "9", "mười": "10"}
# Số viết bằng chữ đứng trước một danh từ. Bỏ "một" (quá nhiều nghĩa), bỏ "năm 2026", "năm nay",
# "ba mẹ", và số nằm trong "thứ ba", "tháng năm", "mùng hai".
QUANTITY = re.compile(
    r"(?<!thứ )(?<!tháng )(?<!mùng )(?<!mồng )(?<!mười )\b(hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\s+"
    r"(?!\d|nay\b|ngoái\b|trước\b|sau\b|tới\b|qua\b|đó\b|này\b|kia\b|mới\b|học\b|mẹ\b|má\b|tôi\b|em\b|"
    r"con\b|ơi\b|là\b|mươi\b|trăm\b|nghìn\b|ngàn\b|triệu\b|tỷ\b|tỉ\b|hai\b|ba\b|bốn\b|năm\b|sáu\b|bảy\b|"
    r"tám\b|chín\b|mười\b)[^\W\d_]+")
WEEKDAY = re.compile(r"\bthứ (hai|ba|tư|năm|sáu|bảy|[2-7])\b|\bchủ nhật\b")
MONTH = re.compile(r"\btháng (giêng|chạp|mười một|mười hai|một|hai|ba|tư|bốn|năm|sáu|bảy|tám|chín|mười|\d{1,2})\b")
# Từ nhỏ mà bỏ đi thì câu đổi nghĩa: "vẫn chưa xong" khác "xong", "có thể giảm" khác "giảm".
SHADES = {
    "chưa": r"\bchưa\b", "vẫn": r"\bvẫn\b", "chỉ": r"\bchỉ\b(?! (ra|đạo|số|tiêu|định|dẫn|thị|huy|trích)\b)",
    "có thể": r"\bcó thể\b", "có lẽ": r"\bcó lẽ\b", "khoảng": r"\b(khoảng|chừng|tầm|gần)\s+\d",
    "ít nhất": r"\b(ít nhất|tối thiểu)\b", "tối đa": r"\b(tối đa|nhiều nhất|không quá)\b",
    "dự kiến": r"\bdự kiến\b", "hầu hết": r"\b(hầu hết|phần lớn|đa số)\b",
}


def canon(number):
    """Đưa số về một dạng để so: bỏ dấu phân cách hàng nghìn, phẩy thập phân thành chấm."""
    n = number.replace("–", "-")
    core = n.rstrip("%")
    if re.fullmatch(r"\d{1,3}(?:[.,]\d{3})+", core):
        core = re.sub(r"[.,]", "", core)
    elif re.fullmatch(r"\d+,\d+", core):
        core = core.replace(",", ".")
    return core + n[len(n.rstrip("%")):]


def facts(text):
    no_code = CODE.sub(" ", URL.sub(" ", text))
    low = no_code.lower()
    # Dòng viết hoa cả (tiêu đề mục của bài đăng) không phải tên viết tắt hay tên riêng
    mixed = "\n".join(line for line in no_code.splitlines()
                      if not (line == line.upper() and len(line.split()) >= 2 and any(c.isalpha() for c in line)))
    numbers = {}
    for n in NUMBER.findall(no_code):
        n = n.rstrip(".,")
        numbers.setdefault(canon(n), n)
    return {
        "_raw": text,
        "_low": low,
        "_numbers": numbers,
        "_quantities": {NUM_WORDS[m.group(1)]: m.group(1) for m in QUANTITY.finditer(low)},
        "link": set(URL.findall(text)),
        "code": set(CODE.findall(text)),
        "số": set(numbers),
        "viết tắt": set(ACRONYM.findall(mixed)),
        "thứ, tháng": {m.group(0) for rx in (WEEKDAY, MONTH) for m in rx.finditer(low)},
        "tên riêng": set(NAME.findall(mixed)),
    }


SOFT = {"tên riêng", "thứ, tháng"}


def compare(old, new):
    """Trả về (danh sách dòng báo, có lỗi nặng hay không)."""
    lines, failed = [], False
    for kind in old:
        if kind.startswith("_"):
            continue
        lost, added = sorted(old[kind] - new[kind]), sorted(new[kind] - old[kind])
        if kind == "code":
            # Đoạn code được tách, gộp hay chuyển vào khối lệnh mà nội dung còn nguyên thì không tính
            lost = [c for c in lost if c not in new["_raw"]]
            added = [c for c in added if c not in old["_raw"]]
        if kind == "số":
            # "3 khách" viết lại thành "ba khách" (hoặc ngược lại) thì số vẫn còn
            lost = [old["_numbers"][n] for n in lost if n not in new["_quantities"]]
            added = [new["_numbers"][n] for n in added if n not in old["_quantities"]]
        if not lost and not added:
            continue
        strict = kind not in SOFT
        failed |= strict
        tag = "LỖI" if strict else "xem lại"
        if lost:
            lines.append(f"[{tag}] {kind} bị mất: {', '.join(lost)}")
        if added:
            lines.append(f"[{tag}] {kind} mới thêm: {', '.join(added)}")
    q_old, q_new = old["_quantities"], new["_quantities"]
    lost = sorted(w for v, w in q_old.items() if v not in q_new and v not in new["số"])
    added = sorted(w for v, w in q_new.items() if v not in q_old and v not in old["số"])
    if lost:
        lines.append(f"[xem lại] số viết bằng chữ bị mất: {', '.join(lost)}")
    if added:
        lines.append(f"[xem lại] số viết bằng chữ mới thêm: {', '.join(added)}")
    fewer = []
    for word, rx in SHADES.items():
        a, b = len(re.findall(rx, old["_low"])), len(re.findall(rx, new["_low"]))
        if b < a:
            fewer.append(f"{word} {a}→{b}")
    if fewer:
        lines.append(f"[xem lại] từ giữ nghĩa ít đi, đọc lại từng chỗ xem nghĩa có đổi không: {', '.join(fewer)}")
    return lines, failed


def read(path):
    if path.lower().endswith(".pptx"):
        return slides.to_text(slides.read_pptx(path))[0]
    with open(path, encoding="utf-8") as f:
        return f.read()


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    lines, failed = compare(facts(read(sys.argv[1])), facts(read(sys.argv[2])))
    print("\n".join(lines)) if lines else None
    if not failed:
        print("Số liệu, link, code khớp với bản gốc.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
