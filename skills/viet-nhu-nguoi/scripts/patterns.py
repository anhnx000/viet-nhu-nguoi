"""Tra nhóm hoặc số mục trong danh mục dấu hiệu đi kèm skill."""

import argparse
from pathlib import Path
import re
import sys


CATALOG = Path(__file__).resolve().parents[1] / "references" / "patterns.md"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("muc", nargs="*", help="số mục hoặc chữ cái của nhóm, ví dụ: 46 55 K")
    args = parser.parse_args()
    catalog = CATALOG.read_text(encoding="utf-8")
    # Các mốc HTML phục vụ liên kết cũ, không thuộc ví dụ ở mục ngay trước.
    catalog = re.sub(r'^<a id="[^"]+"></a>\n', "", catalog, flags=re.M)
    sections = {}
    index = []
    for group in re.split(r"(?=^## )", catalog, flags=re.M):
        heading = re.match(r"## ([A-Z])\. .*", group)
        if not heading:
            continue
        sections[heading[1]] = group.rstrip()
        index.append(heading[0])
        for entry in re.split(r"(?=^### \d+\.)", group, flags=re.M):
            title = re.match(r"### (\d+)\. .*", entry)
            if title:
                sections[title[1]] = entry.rstrip()
                index.append(title[0])

    keys = [key.upper() for key in args.muc]
    for key in keys:
        if key not in sections:
            parser.error(f"Không có mục {key}. Chạy lệnh không kèm số để xem danh sách.")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("\n\n".join(sections[key] for key in keys) if keys else "\n".join(index))


if __name__ == "__main__":
    main()
