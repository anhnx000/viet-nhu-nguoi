#!/usr/bin/env python3
"""Chấm phần tự động của bộ đề thử skill.

Dùng: python3 -I evals/check.py THU_MUC_KET_QUA
THU_MUC_KET_QUA chứa mỗi đề một file <id>.md, là nguyên văn câu trả lời của trợ lý khi skill đang bật.
Cách chạy từng đề và phần phải đọc tay nằm ở evals/README.md.

Script chỉ kiểm những thứ đếm được: số câu hỏi đánh số, số chỗ trống trong ngoặc vuông, dữ kiện còn đủ,
độ dài, điểm scan.py, tỉ lệ chữ giữ nguyên so với bài gốc, số liệu tự thêm ngoài lời dặn. Giọng văn có tự nhiên không thì vẫn phải đọc.
Thoát mã 1 nếu có đề trượt hoặc thiếu file.
"""
import difflib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/viet-nhu-nguoi/scripts"))
import check_facts  # noqa: E402
import scan  # noqa: E402

QUESTION = re.compile(r"(?m)^\s*\d+[.)]\s")
# [địa chỉ], [Họ tên]... nhưng không tính link Markdown [chữ](url) và ô đánh dấu [x], [ ]
PLACEHOLDER = re.compile(r"\[(?![ xX]\])[^\]\n]{2,60}\](?!\()")
# Số mục trong danh mục: "mục 45", hoặc dãy số trong ngoặc như "(45, 3, 1)"
REF = re.compile(r"\bmục (\d{1,2})\b|\(((?:mục )?\d{1,2}(?:, ?\d{1,2})*)\)")
BOLD = re.compile(r"\*\*[^*\n]+\*\*")


def overlap(source, reply):
    """Tỉ lệ chữ của bài gốc còn nguyên trong câu trả lời (0-1)."""
    a, b = source.split(), reply.split()
    if not a:
        return 0.0
    blocks = difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks()
    return sum(m.size for m in blocks) / len(a)


def check(scenario, reply, root=ROOT):
    """Trả về danh sách lỗi (rỗng nghĩa là qua phần tự động)."""
    rules, errors = scenario.get("kiem", {}), []
    words = len(reply.split())
    questions = len(QUESTION.findall(reply))
    placeholders = len(PLACEHOLDER.findall(reply))
    source = ""
    if scenario.get("tep"):
        source = (root / scenario["tep"]).read_text(encoding="utf-8")

    def need(ok, message):
        if not ok:
            errors.append(message)

    if "min_words" in rules:
        need(words >= rules["min_words"], f"chỉ {words} chữ, cần từ {rules['min_words']}")
    if "max_words" in rules:
        need(words <= rules["max_words"], f"{words} chữ, quá {rules['max_words']}")
    if "min_questions" in rules:
        need(questions >= rules["min_questions"], f"{questions} câu hỏi đánh số, cần từ {rules['min_questions']}")
    if "max_questions" in rules:
        need(questions <= rules["max_questions"], f"{questions} câu hỏi đánh số, quá {rules['max_questions']}")
    if "max_placeholders" in rules:
        need(placeholders <= rules["max_placeholders"],
             f"{placeholders} chỗ trống trong ngoặc vuông, quá {rules['max_placeholders']}")
    if "max_bold" in rules:
        bold = len(BOLD.findall(reply))
        need(bold <= rules["max_bold"], f"{bold} chỗ in đậm, quá {rules['max_bold']}")
    for fact in rules.get("must_keep", []):
        # một dữ kiện có thể viết theo vài cách ("21h" hay "9h tối"): đưa vào dạng danh sách
        options = fact if isinstance(fact, list) else [fact]
        need(any(o in reply for o in options), f"mất dữ kiện \"{options[0]}\"")
    for bad in rules.get("must_not", []):
        need(bad not in reply, f"còn \"{bad}\"")
    if "min_refs" in rules:
        refs = len({n for a, b in REF.findall(reply) for n in re.findall(r"\d+", a or b)})
        need(refs >= rules["min_refs"], f"dẫn {refs} mục trong danh mục, cần từ {rules['min_refs']}")
    if "min_overlap" in rules or "max_overlap" in rules:
        ratio = overlap(source, reply)
        if "min_overlap" in rules:
            need(ratio >= rules["min_overlap"], f"chỉ giữ {ratio:.0%} số chữ gốc, cần từ {rules['min_overlap']:.0%}")
        if "max_overlap" in rules:
            need(ratio <= rules["max_overlap"], f"chép lại {ratio:.0%} bài gốc, quá {rules['max_overlap']:.0%}")
    if "max_added_numbers" in rules:
        # số có trong câu trả lời mà không có trong lời người dùng hay file đầu vào: chi tiết trợ lý tự thêm
        brief = check_facts.facts(scenario["tin_nhan"] + "\n" + source)
        lines, _ = check_facts.added(brief, check_facts.facts(reply))
        extra = [n for line in lines if line.startswith("[LỖI] số") for n in line.split(": ", 1)[1].split(", ")]
        need(len(extra) <= rules["max_added_numbers"], f"tự thêm số không có trong lời dặn: {', '.join(extra)}")
    if "scan_max" in rules:
        score = scan.score(reply, scan.scan(reply)[0])["score"]
        need(score <= rules["scan_max"], f"scan.py chấm {score}, quá {rules['scan_max']}")
    return errors


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = pathlib.Path(sys.argv[1])
    scenarios = json.loads((ROOT / "evals/scenarios.json").read_text(encoding="utf-8"))
    failed = 0
    for sc in scenarios:
        path = out / f"{sc['id']}.md"
        if not path.exists():
            print(f"THIẾU  {sc['id']}: không thấy {path.name}")
            failed += 1
            continue
        errors = check(sc, path.read_text(encoding="utf-8"))
        if errors:
            failed += 1
            print(f"TRƯỢT  {sc['id']}: " + "; ".join(errors))
        else:
            print(f"QUA    {sc['id']}")
    print(f"\n{len(scenarios) - failed}/{len(scenarios)} đề qua phần tự động. "
          "Phần còn lại đọc tay theo cột \"mong_doi\" trong scenarios.json.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
