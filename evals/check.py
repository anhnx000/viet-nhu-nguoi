#!/usr/bin/env python3
"""Chấm phần tự động của bộ đề thử skill.

Dùng: python3 -I evals/check.py THU_MUC [THU_MUC ...] [--held-out] [--trigger]
THU_MUC chứa mỗi đề một file <id>.md, là nguyên văn câu trả lời của trợ lý khi skill đang bật.
Nếu THU_MUC chỉ có các thư mục con 1/, 2/, 3/ (evals/run.py chạy nhiều lượt) thì chấm từng lượt, báo tỉ lệ qua
kèm khoảng tin cậy 95% và số đề qua cả mọi lượt.
Cách chạy từng đề và phần phải đọc tay nằm ở evals/README.md.

Script chỉ kiểm những thứ đếm được: số câu hỏi có dấu hỏi, số chỗ trống trong ngoặc vuông, dữ kiện còn đủ,
chữ phải có đứng riêng (chữ viết tắt như "ko", "a"), việc chính có nằm ở đầu tin không, độ dài, điểm scan.py, tỉ lệ chữ giữ nguyên so với bài gốc, số liệu tự thêm ngoài lời dặn. Giọng văn có tự nhiên không thì vẫn phải đọc.
Nếu cạnh câu trả lời có <id>.json (vết công cụ do run.py ghi), script chấm riêng phần đường đọc: trợ lý đã mở
file hướng dẫn nào (must_read, must_not_read, max_refs; không đề nào được đọc trọn patterns.md hay sources.md trừ khi
đề ghi allow_read). Đường đọc chỉ để xem skill dẫn đường đúng không, không quyết định đề qua hay trượt.
--trigger chấm lượt chạy trigger.json (run.py --trigger): skill có tự bật ở lời nhờ nên bật và không bật ở lời nhờ
gần giống mà không nên bật. Đề "bat": null chỉ báo số lượt bật, không tính đúng sai. Thêm --held-out thì chấm
trigger-held-out.json.
Thoát mã 1 nếu có đề trượt hoặc thiếu file.
"""
import difflib
import json
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/viet-nhu-nguoi/scripts"))
import check_facts  # noqa: E402
import scan  # noqa: E402

QUESTION = re.compile(r"[?？]+")
# [địa chỉ], [Họ tên]... nhưng không tính link Markdown [chữ](url) và ô đánh dấu [x], [ ]
PLACEHOLDER = re.compile(r"\[(?![ xX]\])[^\]\n]{2,60}\](?!\()")
# Số mục trong danh mục: "mục 45", hoặc dãy số trong ngoặc như "(45, 3, 1)"
REF = re.compile(r"\bmục (\d{1,2}(?:, ?\d{1,2})*)\b|\(((?:mục )?\d{1,2}(?:, ?\d{1,2})*)\)|(?<![\w&])#(\d{1,2})\b", re.IGNORECASE)
LEAD_WORDS = 25
BOLD = re.compile(r"\*\*[^*\n]+\*\*")
# "slide 2", "mục 45, 46": chỉ chỗ trong bài hay trong danh mục, không phải số liệu trợ lý tự thêm
POINTER = re.compile(r"\b(?:slide|mục)\s+\d{1,3}(?:\s*(?:[-–,]|và|đến|tới)\s*\d{1,3})*", re.IGNORECASE)

# Vết công cụ: file hướng dẫn và script của skill mà trợ lý đã mở
REF_FILE = re.compile(r"references/([\w-]+\.md)")
SCRIPT = re.compile(r"scripts/([\w-]+\.py)")
BARE_MD = re.compile(r"(?<![\w/.-])([\w-]+\.md)\b")
PARTIAL_COMMANDS = {"grep", "rg", "sed", "head", "tail", "awk"}
# SKILL.md dặn tra đúng mục trong danh mục và chỉ mở nguồn tham khảo khi cần tra nguồn.
NO_FULL_READ = ("patterns.md", "sources.md")


def overlap(source, reply):
    """Tỉ lệ chữ của bài gốc còn nguyên trong câu trả lời (0-1)."""
    a, b = source.split(), reply.split()
    if not a:
        return 0.0
    blocks = difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks()
    return sum(m.size for m in blocks) / len(a)


def contains(text, term):
    """Cụm bắt đầu và kết thúc bằng chữ thì phải đứng riêng: "ông" không khớp trong "không"."""
    if term[:1].isalnum() and term[-1:].isalnum():
        return re.search(rf"(?<!\w){re.escape(term)}(?!\w)", text) is not None
    return term in text


def load_trace(path):
    """Đọc vết run.py ghi. Nhận cả dạng cũ: danh sách [tên công cụ, tham số], coi như lệnh nào cũng chạy được."""
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    tools = data.get("tools", []) if isinstance(data, dict) else data
    return [(t[0], t[1] if len(t) > 1 else {}, t[2] if len(t) > 2 else True) for t in tools]


def trace_error(path):
    """Lỗi Codex hay Claude ghi trong vết (hết hạn mức, mất mạng), rỗng nếu lượt chạy xong."""
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    return data.get("error") if isinstance(data, dict) and not data.get("tools") else None


def opened(trace):
    """File của skill mà trợ lý đã mở: {tên: True nếu đọc trọn, False nếu chỉ đọc một phần hoặc là script đã chạy}.

    Lệnh bị chặn hoặc lỗi không tính. Read có limit/offset, Grep, sed/head/grep trên file thì là đọc một phần.
    """
    files = {}

    def mark(name, full):
        files[name] = files.get(name, False) or full

    for tool, data, ok in trace:
        if not ok or not isinstance(data, dict):
            continue
        if tool == "Read":
            for name in REF_FILE.findall(str(data.get("file_path", ""))):
                mark(name, "limit" not in data and "offset" not in data)
        elif tool == "Grep":
            for name in REF_FILE.findall(str(data.get("path", ""))):
                mark(name, False)
        elif tool == "Bash":
            command = str(data.get("command", ""))
            inside = re.search(r"\bcd\s+\S*references/?(?:\s|$)", command)
            for part in re.split(r"&&|\|\||[;|\n]", command):
                words = part.split()
                if not words or words[0] == "cd":
                    continue
                refs = REF_FILE.findall(part) or (BARE_MD.findall(part) if inside else [])
                for name in refs:
                    mark(name, words[0] not in PARTIAL_COMMANDS)
                for name in SCRIPT.findall(part):
                    mark(name, False)
    return files


def check_trace(rules, trace):
    """Lỗi về việc mở file hướng dẫn, theo vết công cụ."""
    files, errors = opened(trace), []
    for item in rules.get("must_read", []):
        options = item if isinstance(item, list) else [item]
        if not any(o in files for o in options):
            errors.append(f"không mở {' hay '.join(options)}")
    for name in rules.get("must_not_read", []):
        if name in files:
            errors.append(f"mở {name} dù đề không cần")
    for name in NO_FULL_READ:
        if files.get(name) and name not in rules.get("allow_read", []):
            errors.append(f"đọc trọn {name} thay vì tra phần cần")
    refs = sorted(n for n in files if n.endswith(".md"))
    if "max_refs" in rules and len(refs) > rules["max_refs"]:
        errors.append(f"mở {len(refs)} file hướng dẫn ({', '.join(refs)}), quá {rules['max_refs']}")
    return errors


def check(scenario, reply, root=ROOT):
    """Trả về danh sách lỗi phần nội dung (rỗng nghĩa là qua phần tự động)."""
    rules, errors = scenario.get("kiem", {}), []
    words = len(reply.split())
    if not words:
        return ["câu trả lời rỗng"]
    questions = len(QUESTION.findall(reply))
    # Giới hạn hỏi lại chỉ xét danh sách đánh số: dấu ? trong email soạn hộ
    # có thể là lời nhờ người nhận, không phải hỏi lại người dùng. Đọc tay phần này.
    numbered_questions = len(re.findall(r"(?m)^\s*\d+[.)]\s", reply))
    placeholders = len(PLACEHOLDER.findall(reply))
    source = ""
    needs_source = {"min_overlap", "max_overlap", "max_added_numbers"} & set(rules)
    if scenario.get("tep") and needs_source:
        source = check_facts.read(str(root / scenario["tep"]))  # đọc được cả .pptx

    def need(ok, message):
        if not ok:
            errors.append(message)

    if "min_words" in rules:
        need(words >= rules["min_words"], f"chỉ {words} chữ, cần từ {rules['min_words']}")
    if "max_words" in rules:
        need(words <= rules["max_words"], f"{words} chữ, quá {rules['max_words']}")
    if "min_questions" in rules:
        need(questions >= rules["min_questions"], f"{questions} câu hỏi có dấu hỏi, cần từ {rules['min_questions']}")
    if "max_questions" in rules:
        need(numbered_questions <= rules["max_questions"], f"{numbered_questions} mục hỏi lại đánh số, quá {rules['max_questions']}")
    if "max_placeholders" in rules:
        need(placeholders <= rules["max_placeholders"],
             f"{placeholders} chỗ trống trong ngoặc vuông, quá {rules['max_placeholders']}")
    if "max_bold" in rules:
        bold = len(BOLD.findall(reply))
        need(bold <= rules["max_bold"], f"{bold} chỗ in đậm, quá {rules['max_bold']}")
    for fact in rules.get("must_keep", []):
        # một dữ kiện có thể viết theo vài cách ("21h" hay "9h tối"): đưa vào dạng danh sách.
        # Không phân biệt hoa thường: "Mùng 4" đầu tin vẫn là "mùng 4". Bỏ qua cách xuống dòng:
        # tách ba câu điệp ngữ thành ba dòng vẫn là giữ nguyên câu.
        options = fact if isinstance(fact, list) else [fact]
        flat = " ".join(reply.split()).casefold()
        need(any(" ".join(o.split()).casefold() in flat for o in options), f"mất dữ kiện \"{options[0]}\"")
    # Việc người nhận cần làm phải nằm ở đầu tin: tìm trong LEAD_WORDS chữ đầu tiên.
    lead = " ".join(reply.split()[:LEAD_WORDS]).casefold()
    for fact in rules.get("lead_keep", []):
        options = fact if isinstance(fact, list) else [fact]
        need(any(o.casefold() in lead for o in options), f"\"{options[0]}\" không nằm trong {LEAD_WORDS} chữ đầu")
    for bad in rules.get("must_not", []):
        need(not contains(reply, bad), f"còn \"{bad}\"")
    # Chữ phải đứng riêng: chữ tắt "a", "r" không được khớp nhầm trong "anh", "rồi" như must_keep.
    for item in rules.get("must_word", []):
        options = item if isinstance(item, list) else [item]
        need(any(contains(reply.casefold(), o.casefold()) for o in options), f"thiếu chữ \"{options[0]}\" đứng riêng")
    if "min_refs" in rules:
        refs = len({n for groups in REF.findall(reply) for n in re.findall(r"\d+", "".join(groups))})
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
        lines, _ = check_facts.added(brief, check_facts.facts(POINTER.sub(" ", reply)))
        extra = [n for line in lines if line.startswith("[LỖI] số") for n in line.split(": ", 1)[1].split(", ")]
        need(len(extra) <= rules["max_added_numbers"], f"tự thêm số không có trong lời dặn: {', '.join(extra)}")
    if "scan_max" in rules:
        score = scan.score(reply, scan.scan(reply)[0])["score"]
        need(score <= rules["scan_max"], f"scan.py chấm {score}, quá {rules['scan_max']}")
    return errors


def run_dirs(path):
    """Một thư mục kết quả, hoặc các lượt 1/, 2/, 3/... bên trong nó."""
    path = pathlib.Path(path)
    if not path.is_dir() or any(path.glob("*.md")):
        return [path]
    runs = [p for p in path.iterdir() if p.is_dir() and (any(p.glob("*.md")) or any(p.glob("*.json")))]
    return sorted(runs, key=lambda p: (len(p.name), p.name)) or [path]


def grade(scenario, folder):
    """(lỗi nội dung, lỗi đường đọc) của một đề trong một lượt; None nếu thiếu câu trả lời.

    Lỗi đường đọc là None khi không có vết, hoặc khi lượt chạy không bật skill (run.py --khong-skill).
    """
    answer = folder / f"{scenario['id']}.md"
    if not answer.exists():
        return None
    route = None
    trace_path = folder / f"{scenario['id']}.json"
    if trace_path.exists():
        data = json.loads(trace_path.read_text(encoding="utf-8"))
        if not (isinstance(data, dict) and data.get("skill") is False):
            route = check_trace(scenario.get("kiem", {}), load_trace(trace_path))
    return check(scenario, answer.read_text(encoding="utf-8")), route


def wilson(k, n, z=1.96):
    """Khoảng tin cậy Wilson cho tỉ lệ k/n. Với 3 lượt, 3/3 vẫn chỉ là 44-100%."""
    if not n:
        return 0.0, 1.0
    p, d = k / n, 1 + z * z / n
    center = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, center - half), min(1.0, center + half)


def used_skill(trace):
    """Trợ lý có bật skill không: gọi công cụ Skill, hoặc mở SKILL.md của skill (cách Codex và các trợ lý khác)."""
    for tool, data, _ok in trace:
        if tool == "Skill" and "viet-nhu-nguoi" in str((data or {}).get("skill", "")):
            return True
        if "viet-nhu-nguoi/SKILL.md" in json.dumps(data, ensure_ascii=False):
            return True
    return False


def report_trigger(cases, folders):
    """In số lượt bật skill của từng lời nhờ và tỉ lệ đúng; trả về số đề có lượt sai hoặc thiếu."""
    total, failed, tally = len(folders), 0, {True: [0, 0], False: [0, 0], None: [0, 0]}
    for case in cases:
        # Lượt lỗi (hết hạn mức, mất mạng) tính là thiếu, không tính là không bật.
        paths = [f / f"{case['id']}.json" for f in folders if (f / f"{case['id']}.json").exists()]
        hits = [used_skill(load_trace(p)) for p in paths if not trace_error(p)]
        want = case.get("bat")
        on = sum(hits)
        tally[want][0] += on
        tally[want][1] += len(hits)
        label = {True: "nên bật", False: "không nên bật", None: "tùy"}[want]
        wrong = len(hits) < total or (want is True and on < len(hits)) or (want is False and on > 0)
        failed += wrong
        mark = "THIẾU " if len(hits) < total else "SAI   " if wrong else "ĐÚNG  "
        print(f"{mark} {case['id']} ({label}): bật {on}/{len(hits)} lượt")
    for want, name in ((True, "Nên bật"), (False, "Không nên bật")):
        k, n = tally[want]
        if n:
            low, high = wilson(k, n)
            print(f"\n{name}: bật {k}/{n} lượt ({k / n:.0%}, khoảng tin cậy 95%: {low * 100:.0f}-{high:.0%}).", end="")
    k, n = tally[None]
    if n:
        print(f"\nTùy: bật {k}/{n} lượt.", end="")
    print()
    return failed


def report(scenarios, folders):
    """In kết quả từng đề và dòng tổng; trả về số đề có lượt trượt hoặc thiếu."""
    total = len(folders)
    failed = passed_runs = all_runs = route_ok = route_runs = 0
    for sc in scenarios:
        results = [grade(sc, f) for f in folders]
        ok = sum(r is not None and not r[0] for r in results)
        passed_runs += ok
        all_runs += ok == total
        prefix = (lambda f: f"lượt {f.name}: ") if total > 1 else (lambda f: "")
        routes = [(f, r[1]) for f, r in zip(folders, results) if r is not None and r[1] is not None]
        route_runs += len(routes)
        route_ok += sum(not errors for _, errors in routes)
        wrong = [prefix(f) + "; ".join(errors) for f, errors in routes if errors]
        count = f" ({ok}/{total})" if total > 1 else ""
        road = ("  · đường đọc: " + " | ".join(wrong)) if wrong else ""
        if ok == total:
            print(f"QUA    {sc['id']}{count}{road}")
            continue
        failed += 1
        notes = []
        for folder, result in zip(folders, results):
            if result is None:
                notes.append(prefix(folder) + f"không thấy {sc['id']}.md")
            elif result[0]:
                notes.append(prefix(folder) + "; ".join(result[0]))
        label = "THIẾU " if all(r is None for r in results) else "TRƯỢT "
        print(f"{label} {sc['id']}{count}: " + " | ".join(notes) + road)
    n = len(scenarios)
    if total == 1:
        print(f"\n{n - failed}/{n} đề qua phần tự động.")
    else:
        low, high = wilson(passed_runs, n * total)
        print(f"\n{passed_runs}/{n * total} lượt qua phần tự động ({passed_runs / (n * total):.0%}, "
              f"khoảng tin cậy 95%: {low * 100:.0f}-{high:.0%}). {all_runs}/{n} đề qua cả {total} lượt.")
    if route_runs:
        print(f"Đường đọc đúng ở {route_ok}/{route_runs} lượt có vết.")
    print("Phần còn lại đọc tay theo cột \"mong_doi\" trong file đề.")
    return failed


def main():
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")  # Windows mặc định cp1252, in chữ có dấu sẽ lỗi
    args = sys.argv[1:]
    dirs = [a for a in args if not a.startswith("--")]
    flags = [a for a in args if a.startswith("--")]
    if not dirs or not set(flags) <= {"--held-out", "--trigger"} or len(set(flags)) != len(flags):
        sys.exit(__doc__)
    trigger = "--trigger" in flags
    filename = ("trigger" if trigger else "") + ("-held-out" if "--held-out" in flags else "") + ".json"
    filename = {".json": "scenarios.json", "-held-out.json": "held-out.json"}.get(filename, filename)
    scenarios = json.loads((ROOT / "evals" / filename).read_text(encoding="utf-8"))
    folders = [run for d in dirs for run in run_dirs(d)]
    if trigger:
        sys.exit(1 if report_trigger(scenarios, folders) else 0)
    sys.exit(1 if report(scenarios, folders) else 0)


if __name__ == "__main__":
    main()
