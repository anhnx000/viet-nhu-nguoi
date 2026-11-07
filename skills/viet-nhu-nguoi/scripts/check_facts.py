#!/usr/bin/env python3
"""So bản gốc với bản viết lại: có mất hay thêm số liệu, ngày giờ, link, code, tên riêng không.

Dùng: python3 -I check_facts.py GOC.md MOI.md
Thoát mã 1 nếu số, link hoặc code bị mất hay được thêm. Tên riêng chỉ cảnh báo, vì sửa câu
có thể đổi chữ đứng đầu câu hoặc lược bớt tên lặp lại.
"""
import re
import sys

URL = re.compile(r"https?://[^\s)>\]]+")
CODE = re.compile(r"`([^`\n]+)`")
# 15:00, 30/4, 2026-11-07, 1.000.000, 2.3, 30%, v1.2.0, 5–10
NUMBER = re.compile(r"\bv?\d+(?:[.,:/\-–]\d+)*%?")
ACRONYM = re.compile(r"\b[A-ZĐ]{2,}[0-9]*\b")
UPPER = "A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬĐÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ"
# Từ viết hoa không đứng sau dấu kết câu hay đầu dòng: thường là tên riêng
NAME = re.compile(rf"(?<![.!?:\n>\-*#]\s)(?<!^)(?<=\s)[{UPPER}][\w]+", re.MULTILINE)


def facts(text):
    no_code = CODE.sub(" ", URL.sub(" ", text))
    return {
        "link": set(URL.findall(text)),
        "code": set(CODE.findall(text)),
        "số": {n.rstrip(".,") for n in NUMBER.findall(no_code)},
        "viết tắt": set(ACRONYM.findall(no_code)),
        "tên riêng": set(NAME.findall(no_code)),
    }


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        old = facts(f.read())
    with open(sys.argv[2], encoding="utf-8") as f:
        new = facts(f.read())
    failed = False
    for kind in old:
        lost, added = sorted(old[kind] - new[kind]), sorted(new[kind] - old[kind])
        if not lost and not added:
            continue
        strict = kind != "tên riêng"
        failed |= strict
        tag = "LỖI" if strict else "xem lại"
        if lost:
            print(f"[{tag}] {kind} bị mất: {', '.join(lost)}")
        if added:
            print(f"[{tag}] {kind} mới thêm: {', '.join(added)}")
    if not failed:
        print("Số liệu, link, code khớp với bản gốc.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
