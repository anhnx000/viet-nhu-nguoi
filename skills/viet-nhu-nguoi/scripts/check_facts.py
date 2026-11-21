#!/usr/bin/env python3
"""So bản gốc với bản viết lại: có mất hay thêm số liệu, ngày giờ, link, code, tên riêng không.

Dùng: python3 -I check_facts.py GOC.md MOI.md       (hoặc GOC.pptx MOI.pptx)
Thoát mã 1 nếu số, link hoặc code bị mất hay được thêm. Các mục "xem lại" chỉ cảnh báo, không
đổi mã thoát: tên riêng (sửa câu có thể đổi chữ đứng đầu câu hoặc lược bớt tên lặp lại), số viết
bằng chữ, thứ trong tuần, tháng, và các từ giữ nghĩa ("chưa", "vẫn", "chỉ", "có thể", "khoảng"...).

Số được so theo giá trị: "1.250" và "1250", "12,5%" và "12.5%", "3 khách" và "ba khách" coi là một.

Bài viết mới thì so với lời dặn: python3 -I check_facts.py --brief LOI_DAN.txt BAI.md
LOI_DAN là ghi chú, tin nhắn hay dàn ý người dùng đưa cho trợ lý. Script liệt kê những gì có trong bài mà
không có trong lời dặn (số liệu, ngày giờ, tên riêng, lời người khác nói), tức là chi tiết trợ lý tự thêm.
Thoát mã 1 nếu bài có số liệu hay link không có trong lời dặn.
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


DATE = re.compile(r"(\d{1,2})/(\d{1,2})(?:/(\d{4}))?")


def canon(number):
    """Đưa số về một dạng để so: bỏ dấu phân cách hàng nghìn, phẩy thập phân thành chấm, 01/03 thành 1/3."""
    n = number.replace("–", "-")
    core = n.rstrip("%")
    date = DATE.fullmatch(core)
    if date:
        return "/".join(str(int(x)) for x in date.groups() if x)
    if re.fullmatch(r"\d{1,3}(?:[.,]\d{3})+", core):
        core = re.sub(r"[.,]", "", core)
    elif re.fullmatch(r"\d+,\d+", core):
        core = core.replace(",", ".")
    return core + n[len(n.rstrip("%")):]


def without_year(number, pool):
    """"31/12" khi bên kia có "31/12/2026": cùng một ngày, chỉ bỏ năm."""
    return DATE.fullmatch(number) is not None and number.count("/") == 1 and \
        any(p.startswith(number + "/") for p in pool)


# Số thứ tự đầu dòng ("1.", "**2.", "## 3)") là cách trình bày, không phải dữ kiện
LIST_NUMBER = re.compile(r"(?m)^[\s#>*_-]*\d{1,2}[.)](?=\s)")


def facts(text):
    no_code = LIST_NUMBER.sub("", CODE.sub(" ", URL.sub(" ", text)))
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
# Lời người khác nói trích trong ngoặc kép: sau động từ nói, hoặc một câu hỏi, câu cảm
SPEECH = re.compile(
    r'\b(?:nói|bảo|dặn|hỏi|la|hét|kể|cười|nhắn|đáp|trả lời|khuyên|thì thầm|gọi)\b[^."“”\n]{0,25}["“]([^"“”\n]{10,160})["”]|'
    r'["“]([^"“”\n]{10,160}[?!])["”]')


def added(brief, draft):
    """Bài viết mới so với lời dặn: trả về (danh sách dòng báo, bài có số liệu hay link tự thêm không)."""
    lines, failed = [], False
    for kind in ("số", "link"):
        new = sorted(draft[kind] - brief[kind])
        if kind == "số":
            new = [draft["_numbers"][n] for n in new
                   if n not in brief["_quantities"] and not without_year(n, brief["số"])]
        if new:
            failed = True
            lines.append(f"[LỖI] {kind} không có trong lời dặn: {', '.join(new)}")
    words = sorted(w for v, w in draft["_quantities"].items() if v not in brief["_quantities"] and v not in brief["số"])
    if words:
        lines.append(f"[xem lại] số viết bằng chữ không có trong lời dặn: {', '.join(words)}")
    low = brief["_low"]
    for kind in ("thứ, tháng", "tên riêng", "viết tắt"):
        # chữ viết hoa mà chỗ khác trong bài viết thường ("Hãy", "Nơi") là chữ đầu câu, không phải tên riêng
        new = sorted(x for x in draft[kind] - brief[kind]
                     if x.lower() not in low and not re.search(rf"\b{re.escape(x.lower())}\b", draft["_raw"]))
        if new:
            lines.append(f"[xem lại] {kind} không có trong lời dặn: {', '.join(new)}")
    said = [m.group(1) or m.group(2) for m in SPEECH.finditer(draft["_raw"])]
    said = [q for q in said if q.lower().strip(" .!?") not in low]
    if said:
        lines.append("[xem lại] lời thoại không có trong lời dặn: " + "; ".join(f'"{q}"' for q in said))
    missing = sorted(brief["_numbers"][n] for n in brief["số"] - draft["số"]
                     if n not in draft["_quantities"] and not any(without_year(d, [n]) for d in draft["số"]))
    if missing:
        lines.append(f"[xem lại] số trong lời dặn chưa vào bài: {', '.join(missing)}")
    return lines, failed


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
            # "31/12/2026" viết gọn thành "31/12": vẫn là ngày đó, chỉ nhắc xem năm có cần không
            short = sorted(old["_numbers"][n] for n in lost if any(without_year(a, [n]) for a in added))
            if short:
                lines.append(f"[xem lại] ngày bỏ năm: {', '.join(short)}")
            # "3 khách" viết lại thành "ba khách" (hoặc ngược lại) thì số vẫn còn
            lost = [old["_numbers"][n] for n in lost
                    if n not in new["_quantities"] and old["_numbers"][n] not in short
                    and not without_year(n, new["số"])]
            added = [new["_numbers"][n] for n in added
                     if n not in old["_quantities"] and not without_year(n, old["số"])]
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
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")  # Windows mặc định cp1252, in chữ có dấu sẽ lỗi
    args = sys.argv[1:]
    brief = "--brief" in args
    args = [a for a in args if a != "--brief"]
    if len(args) != 2:
        sys.exit(__doc__)
    old, new = facts(read(args[0])), facts(read(args[1]))
    lines, failed = added(old, new) if brief else compare(old, new)
    print("\n".join(lines)) if lines else None
    if not failed:
        print("Bài không có số liệu hay link nào ngoài lời dặn." if brief else "Số liệu, link, code khớp với bản gốc.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
