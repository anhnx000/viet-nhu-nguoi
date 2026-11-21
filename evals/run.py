#!/usr/bin/env python3
"""Chạy bộ đề qua Claude Code, lưu câu trả lời và vết công cụ cho check.py chấm.

Dùng: python3 -I evals/run.py THU_MUC [--held-out] [--trigger] [--runs N] [--jobs N] [--model opus] [--effort medium]
                                [--khong-skill | --kieu-codex] [ID ...]

Mỗi lượt chạy trong một thư mục tạm ở ~/.cache/vnn-eval, ngoài repo nên trợ lý không thấy đáp án mẫu. Thư mục chỉ có
bản sao skill ở .claude/skills/viet-nhu-nguoi và file đầu vào của đề, rồi gửi "/viet-nhu-nguoi <tin_nhan>" bằng
`claude -p`, chỉ nạp cài đặt của thư mục đó. Trợ lý được đọc file, tìm chữ, chạy ba script của skill và ghi file
nháp trong /tmp (để so dữ kiện), không ghi được vào file đầu vào. --khong-skill chạy cùng đề mà không có skill,
để so xem skill thêm được gì.

--trigger chạy trigger.json: gửi lời nhờ như người dùng gõ thường, không có "/viet-nhu-nguoi", rồi xem trợ lý có tự
bật skill không. Chỉ cần mấy bước đầu nên mỗi lượt dừng sau 4 bước. Chấm: check.py THU_MUC --trigger.
--trigger --held-out chạy trigger-held-out.json, lời nhờ viết sau khi sửa description, chỉ dùng để báo kết quả.
--kieu-codex nạp skill theo cách của Codex: skill nằm ở .agents/skills/viet-nhu-nguoi, không có công cụ Skill, lời
nhắc hệ thống có danh sách skill và luật dùng skill chép từ Codex CLI 0.171, lời nhờ mở bằng "$viet-nhu-nguoi". Mô hình
vẫn là Claude, nên chế độ này thử đường dẫn tương đối, cách đọc SKILL.md và references/ khi không có công cụ Skill,
không thử hành vi của mô hình GPT.

Kết quả nằm ở THU_MUC/<lượt>/:
  <id>.md    nguyên văn câu trả lời
  <id>.json  công cụ trợ lý đã gọi (kèm gọi được hay bị chặn), skill và plugin đã nạp, số lượt, token, chi phí
Đề đã có câu trả lời thì bỏ qua, nên chạy lại cùng lệnh sẽ làm nốt phần còn thiếu.
Lượt 1 của mọi đề chạy trước lượt 2, nên hết hạn mức giữa chừng vẫn còn đủ một lượt.
"""
import argparse
import concurrent.futures
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/viet-nhu-nguoi"
WORK = pathlib.Path.home() / ".cache/vnn-eval"
TOOLS = "Read,Grep,Glob,Skill,Bash,Write"
ALLOWED = ["Read", "Grep", "Glob", "Skill", "Write(//tmp/**)",
           "Bash(python3 *scripts/scan.py*)", "Bash(python3 *scripts/check_facts.py*)",
           "Bash(python3 *scripts/patterns.py*)",
           "Bash(cat *)", "Bash(head *)", "Bash(sed -n *)", "Bash(grep *)", "Bash(ls *)", "Bash(wc *)"]
TIMEOUT = 300
TRIGGER_TURNS = "4"
# Phần hướng dẫn skill của Codex CLI 0.171 (chép từ file chạy, bỏ các dòng về plugin và gói skill từ xa)
CODEX_SKILLS = """## Skills
A skill is a set of local instructions to follow that is stored in a `SKILL.md` file. Below is the list of skills that can be used. Each entry includes a name, description, and file path.
### Available skills
- viet-nhu-nguoi: {description} (file: {path})
### How to use skills
- Discovery: The list above is the skills available in this session (name + description + file path).
- Trigger rules: If the user names a skill (with `$SkillName` or plain text) OR the task clearly matches a skill's description shown above, you must use that skill for that turn. Multiple mentions mean use them all. Do not carry skills across turns unless re-mentioned.
- Missing/blocked: If a named skill isn't in the list or the path can't be read, say so briefly and continue with the best fallback.
- How to use a skill (progressive disclosure):
  1) After deciding to use a skill, open and read its `SKILL.md` completely before taking task actions. If a read is truncated or paginated, continue until EOF.
  2) When `SKILL.md` references relative paths (e.g., `scripts/foo.py`), resolve them relative to the directory containing that `SKILL.md` first, and only consider other paths if needed.
  3) If `SKILL.md` points to extra folders such as `references/`, use its routing instructions to identify the files required for the task. The main agent must read each required instruction or reference file itself before acting on it.
  4) If `scripts/` exist, prefer running or patching them instead of retyping large code blocks.
  5) If `assets/` or templates exist, reuse them instead of recreating from scratch.
- Safety and fallback: If a skill can't be applied cleanly (missing files, unclear instructions), state the issue, pick the next-best approach, and continue."""


def description():
    """Dòng description trong front matter của SKILL.md."""
    for line in (SKILL / "SKILL.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip()
    return ""


def parse(stream):
    """Tách câu trả lời cuối và vết công cụ từ đầu ra stream-json của `claude -p`."""
    calls, done, info, answer = [], {}, {}, ""
    for line in stream.splitlines():
        try:
            item = json.loads(line)
        except ValueError:
            continue
        kind = item.get("type")
        if kind == "system" and item.get("subtype") == "init":
            # Ghi lại skill và plugin đã nạp để biết lượt chạy có sạch không (không lẫn skill cá nhân, plugin đã cài)
            info.update(model=item.get("model"), version=item.get("claude_code_version"),
                        skills=item.get("skills"), plugins=[p.get("source") for p in item.get("plugins") or []])
        elif kind == "assistant":
            for block in item.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    calls.append((block.get("id"), block.get("name"), block.get("input", {})))
        elif kind == "user":
            content = item.get("message", {}).get("content", [])
            for block in content if isinstance(content, list) else []:
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    done[block.get("tool_use_id")] = not block.get("is_error", False)
        elif kind == "result":
            answer = item.get("result") or ""
            info.update(turns=item.get("num_turns"), cost_usd=item.get("total_cost_usd"),
                        duration_ms=item.get("duration_ms"), usage=item.get("usage"),
                        denied=len(item.get("permission_denials") or []))
    # Lệnh bị chặn hay lỗi thì ghi False: check.py không tính là đã đọc file đó.
    tools = [[name, data, done.get(call_id, False)] for call_id, name, data in calls]
    return answer, {"tools": tools, **info}


def run_one(scenario, out, args):
    answer_path = out / f"{scenario['id']}.md"
    if (out / f"{scenario['id']}.json" if args.trigger else answer_path).exists():
        return "có rồi"
    WORK.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="vnn-eval-", dir=WORK) as temp:
        work = pathlib.Path(temp)
        home = work / (".agents" if args.kieu_codex else ".claude") / "skills/viet-nhu-nguoi"
        if not args.khong_skill:
            shutil.copytree(SKILL, home, ignore=shutil.ignore_patterns("__pycache__"))
        prompt = scenario["tin_nhan"]
        if scenario.get("tep"):
            dest = work / pathlib.Path(scenario["tep"]).name
            shutil.copyfile(ROOT / scenario["tep"], dest)
            prompt = prompt.replace("{tep}", str(dest))
        if not (args.khong_skill or args.trigger):
            prompt = ("$viet-nhu-nguoi " if args.kieu_codex else "/viet-nhu-nguoi ") + prompt
        extra = []
        if args.kieu_codex:
            extra += ["--append-system-prompt",
                      CODEX_SKILLS.format(description=description(), path=home / "SKILL.md")]
        if args.trigger:
            extra += ["--max-turns", TRIGGER_TURNS]
        tools = TOOLS.replace("Skill,", "") if args.kieu_codex else TOOLS
        cmd = ["claude", "-p", "--no-session-persistence", "--setting-sources", "project",
               "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
               "--model", args.model, "--effort", args.effort,
               "--tools", tools, "--allowedTools", *ALLOWED, *extra,
               "--output-format", "stream-json", "--verbose", "--", prompt]
        try:
            proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True, encoding="utf-8",
                                  timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            return f"LỖI quá {TIMEOUT} giây"
        answer, trace = parse(proc.stdout)
        trace["skill"] = not args.khong_skill
        if args.kieu_codex:
            trace["kieu"] = "codex"
        # Bỏ đường dẫn thư mục tạm để vết chỉ còn đường dẫn tương đối như references/chat.md
        text = json.dumps(trace, ensure_ascii=False, indent=1).replace(str(work) + "/", "")
        (out / f"{scenario['id']}.json").write_text(text + "\n", encoding="utf-8")
        if args.trigger:
            # Lượt bị cắt sau vài bước nên thường không có câu trả lời; chỉ cần biết skill có bật không
            if answer:
                answer_path.write_text(answer, encoding="utf-8")
            used = any(t[0] == "Skill" or "viet-nhu-nguoi/SKILL.md" in json.dumps(t[1], ensure_ascii=False)
                       for t in trace["tools"])
            return ("bật skill" if used else "không bật") + f", mong đợi {scenario.get('bat')}"
        if proc.returncode or not answer:
            return "LỖI " + (answer or proc.stderr or "không có câu trả lời")[:200].replace("\n", " ")
        answer_path.write_text(answer, encoding="utf-8")
        return f"{len(answer.split())} chữ, {sum(1 for t in trace['tools'] if t[2])} lệnh"


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Chạy bộ đề thử skill qua Claude Code.")
    parser.add_argument("out", help="thư mục kết quả")
    parser.add_argument("ids", nargs="*", help="chỉ chạy các đề này")
    parser.add_argument("--held-out", action="store_true", help="chạy held-out.json thay cho scenarios.json")
    parser.add_argument("--runs", type=int, default=1, help="số lượt mỗi đề (mặc định 1)")
    parser.add_argument("--jobs", type=int, default=6, help="số đề chạy cùng lúc (mặc định 6)")
    parser.add_argument("--model", default="opus")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--trigger", action="store_true", help="chạy trigger.json: skill có tự bật đúng lúc không")
    parser.add_argument("--khong-skill", action="store_true", help="chạy không có skill, để so")
    parser.add_argument("--kieu-codex", action="store_true", help="nạp skill theo cách của Codex")
    args = parser.parse_intermixed_args()
    if args.khong_skill and (args.kieu_codex or args.trigger):
        sys.exit("--khong-skill không đi cùng --kieu-codex hay --trigger.")
    if not shutil.which("claude"):
        sys.exit("Cần Claude Code: không thấy lệnh claude trong PATH.")
    if args.trigger:
        name = "trigger-held-out.json" if args.held_out else "trigger.json"
    else:
        name = "held-out.json" if args.held_out else "scenarios.json"
    cases = json.loads((ROOT / "evals" / name).read_text(encoding="utf-8"))
    unknown = set(args.ids) - {c["id"] for c in cases}
    if unknown:
        sys.exit(f"Không có đề {', '.join(sorted(unknown))} trong {name}.")
    if args.ids:
        cases = [c for c in cases if c["id"] in args.ids]
    jobs = []
    for n in range(1, args.runs + 1):
        out = pathlib.Path(args.out) / str(n)
        out.mkdir(parents=True, exist_ok=True)
        jobs += [(case, out) for case in cases]

    def work(job):
        case, out = job
        status = run_one(case, out, args)
        print(f"lượt {out.name} {case['id']}: {status}", flush=True)
        return status.startswith("LỖI")

    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        errors = sum(pool.map(work, jobs))
    print(f"\nXong {len(jobs) - errors}/{len(jobs)} lượt. Chấm: python3 -I evals/check.py {args.out}"
          + (" --trigger" if args.trigger else "") + (" --held-out" if args.held_out else ""))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
