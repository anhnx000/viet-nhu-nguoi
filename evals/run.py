#!/usr/bin/env python3
"""Chạy bộ đề qua Claude Code, lưu câu trả lời và vết công cụ cho check.py chấm.

Dùng: python3 -I evals/run.py THU_MUC [--held-out] [--trigger] [--runs N] [--jobs N] [--model opus] [--effort medium]
                                [--khong-skill | --kieu-codex | --codex [--codex-sandbox MODE]] [ID ...]

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
--codex chạy thẳng `codex exec` (mô hình và mức suy luận lấy từ ~/.codex/config.toml nếu không ghi --model,
--effort). Skill nằm ở .agents/skills/viet-nhu-nguoi; skill cá nhân trong ~/.codex/skills và ~/.agents/skills bị tắt,
không nạp config.toml (nên không có MCP), tắt plugin, app, trình duyệt, hook. Lệnh shell chạy trong sandbox
workspace-write của Codex: ghi được thư mục tạm và /tmp. Trên Ubuntu 24.04 trở lên, sandbox này cần một profile
AppArmor cho bubblewrap (xem evals/README.md); thiếu profile thì lượt chạy báo LỖI chứ không lưu câu trả lời.

Kết quả nằm ở THU_MUC/<lượt>/:
  <id>.md    nguyên văn câu trả lời
  <id>.json  công cụ trợ lý đã gọi (kèm gọi được hay bị chặn), skill và plugin đã nạp, số lượt, token, chi phí
Đề đã có câu trả lời thì bỏ qua, nên chạy lại cùng lệnh sẽ làm nốt phần còn thiếu.
Lượt 1 của mọi đề chạy trước lượt 2, nên hết hạn mức giữa chừng vẫn còn đủ một lượt.
"""
import argparse
import os
import shlex
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


CODEX_TIMEOUT = 600
# Tắt những phần có thể lẫn ngữ cảnh cá nhân hay gọi ra ngoài
CODEX_OFF = ["apps", "browser_use", "browser_use_external", "computer_use", "goals", "hooks", "in_app_browser",
             "plugins", "remote_plugin", "plugin_sharing", "skill_search", "skill_mcp_dependency_install"]
# Dấu hiệu sandbox của Codex không dựng được (thường do AppArmor chặn bubblewrap tạo user namespace)
SANDBOX_BROKEN = ("bwrap:", "Bubblewrap", "bubblewrap")


def codex_home():
    return pathlib.Path(os.environ.get("CODEX_HOME") or pathlib.Path.home() / ".codex")


def codex_defaults():
    """Mô hình và mức suy luận trong config.toml của Codex, để --ignore-user-config không đổi mô hình."""
    try:
        import tomllib
        data = tomllib.loads((codex_home() / "config.toml").read_text(encoding="utf-8"))
    except (ImportError, OSError, ValueError):
        return None, None
    return data.get("model"), data.get("model_reasoning_effort")


def personal_skills():
    """SKILL.md của các skill cá nhân Codex sẽ nạp, để tắt khi chạy đề."""
    roots = [codex_home() / "skills", pathlib.Path.home() / ".agents/skills"]
    return sorted(str(f) for root in roots if root.is_dir() for f in root.glob("*/SKILL.md"))


def unwrap(command):
    """`/bin/bash -lc 'sed -n 1,80p a.md'` thành `sed -n 1,80p a.md`, để check.py nhận ra lệnh đọc một phần."""
    try:
        words = shlex.split(command) if isinstance(command, str) else list(command)
    except ValueError:
        return command
    if len(words) == 3 and pathlib.Path(words[0]).name in ("bash", "sh", "zsh") and words[1] in ("-c", "-lc"):
        return words[2]
    return command if isinstance(command, str) else " ".join(words)


def parse_codex(stream):
    """Tách câu trả lời cuối và vết công cụ từ đầu ra `codex exec --json`, theo cùng dạng với parse()."""
    tools, info, answer, notes = [], {}, "", []
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        kind, item = event.get("type"), event.get("item") or {}
        if kind == "item.completed":
            what = item.get("type")
            if what == "agent_message":
                answer = item.get("text") or ""
                notes.append(answer)
            elif what == "command_execution":
                output = item.get("aggregated_output") or ""
                notes.append(output[:500])
                tools.append(["Bash", {"command": unwrap(item.get("command", ""))},
                              item.get("exit_code") == 0 and item.get("status") == "completed"])
            elif what == "file_change":
                tools.append(["Write", {"changes": item.get("changes")}, item.get("status") == "completed"])
            elif what == "mcp_tool_call":
                tools.append([f"mcp:{item.get('server')}.{item.get('tool')}", item.get("arguments") or {},
                              item.get("status") == "completed"])
            elif what == "error":
                notes.append(item.get("message") or "")
        elif kind == "turn.completed":
            info["usage"] = event.get("usage")
        elif kind in ("turn.failed", "error"):
            info["error"] = (event.get("error") or {}).get("message") or event.get("message")
    info["sandbox_broken"] = any(mark in note for note in notes for mark in SANDBOX_BROKEN)
    return answer, {"tools": tools, **info}


def codex_command(args, work, prompt):
    model, effort = codex_defaults()
    model, effort = args.model or model, args.effort or effort or "medium"
    off = [x for name in CODEX_OFF for x in ("--disable", name)]
    skills = ",".join(f"{{path={json.dumps(path)},enabled=false}}" for path in personal_skills())
    cmd = ["codex", "exec", "--ephemeral", "--skip-git-repo-check", "--ignore-user-config", "--ignore-rules",
           *off, "-c", f"model_reasoning_effort={json.dumps(effort)}", "-c", f"skills.config=[{skills}]",
           "-s", args.codex_sandbox, "--json", "-C", str(work)]
    if model:
        cmd += ["-m", model]
    return cmd + ["--", prompt], model, effort


def codex_shell_works(args):
    """Thử một lệnh shell qua Codex trước khi chạy cả bộ: nhờ cat một file có chuỗi ngẫu nhiên không nằm trong lời nhờ.

    Khi sandbox hỏng, Codex không phát sự kiện command_execution nào mà chỉ trả lời "không mở được file", nên phải thử
    thật thay vì đoán từ vết.
    """
    import secrets
    WORK.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="vnn-codex-check-", dir=WORK) as temp:
        token = secrets.token_hex(8)
        (pathlib.Path(temp) / "token.txt").write_text(token + "\n", encoding="utf-8")
        cmd, _, _ = codex_command(args, pathlib.Path(temp), "Chạy lệnh shell `cat token.txt` rồi trả lại đúng nội dung "
                                  "file, không thêm gì.")
        try:
            proc = subprocess.run(cmd, cwd=temp, capture_output=True, text=True, encoding="utf-8", timeout=180,
                                  stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return False, "quá 180 giây", None
        answer, trace = parse_codex(proc.stdout)
        return token in answer, answer[:200], trace.get("error")


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
        home = work / (".agents" if args.kieu_codex or args.codex else ".claude") / "skills/viet-nhu-nguoi"
        if not args.khong_skill:
            shutil.copytree(args.skill_dir, home, ignore=shutil.ignore_patterns("__pycache__"))
        prompt = scenario["tin_nhan"]
        if scenario.get("tep"):
            dest = work / pathlib.Path(scenario["tep"]).name
            shutil.copyfile(ROOT / scenario["tep"], dest)
            prompt = prompt.replace("{tep}", str(dest))
        if not (args.khong_skill or args.trigger):
            prompt = ("$viet-nhu-nguoi " if args.kieu_codex or args.codex else "/viet-nhu-nguoi ") + prompt
        extra = []
        if args.kieu_codex:
            extra += ["--append-system-prompt",
                      CODEX_SKILLS.format(description=description(), path=home / "SKILL.md")]
        if args.trigger:
            extra += ["--max-turns", TRIGGER_TURNS]
        tools = TOOLS.replace("Skill,", "") if args.kieu_codex else TOOLS
        cmd = ["claude", "-p", "--no-session-persistence", "--setting-sources", "project",
               "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
               "--model", args.model or "opus", "--effort", args.effort or "medium",
               "--tools", tools, "--allowedTools", *ALLOWED, *extra,
               "--output-format", "stream-json", "--verbose", "--", prompt]
        if args.codex:
            cmd, model, effort = codex_command(args, work, prompt)
        limit = CODEX_TIMEOUT if args.codex else TIMEOUT
        try:
            proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True, encoding="utf-8",
                                  timeout=limit, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return f"LỖI quá {limit} giây"
        answer, trace = (parse_codex if args.codex else parse)(proc.stdout)
        trace["skill"] = not args.khong_skill
        if args.skill_dir != SKILL:
            trace["skill_dir"] = str(args.skill_dir)
        if args.kieu_codex:
            trace["kieu"] = "codex"
        if args.codex:
            trace.update(kieu="codex exec", model=model, effort=effort, sandbox=args.codex_sandbox)
            if trace.get("sandbox_broken"):
                return ("LỖI sandbox của Codex không chạy được lệnh shell (bubblewrap bị chặn). "
                        "Xem phần Codex trong evals/README.md.")
        if args.trigger and not trace["tools"] and (proc.returncode or trace.get("error")):
            # Hết hạn mức hay lỗi mạng: không lưu vết, để check.py báo thiếu thay vì đếm là không bật.
            # Lượt bị cắt vì hết số bước thì đã có lệnh trong vết nên không rơi vào đây.
            return "LỖI " + (trace.get("error") or answer or proc.stderr or "không có câu trả lời")[:200].replace("\n", " ")
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
    parser.add_argument("--model", help="mặc định opus; với --codex lấy theo config.toml của Codex")
    parser.add_argument("--effort", help="mặc định medium; với --codex lấy theo config.toml của Codex")
    parser.add_argument("--trigger", action="store_true", help="chạy trigger.json: skill có tự bật đúng lúc không")
    parser.add_argument("--khong-skill", action="store_true", help="chạy không có skill, để so")
    parser.add_argument("--kieu-codex", action="store_true", help="nạp skill theo cách của Codex")
    parser.add_argument("--codex", action="store_true", help="chạy thẳng codex exec thay cho claude -p")
    parser.add_argument("--skill-dir", type=pathlib.Path, default=SKILL,
                        help="thư mục skill để thử thay cho skills/viet-nhu-nguoi, ví dụ một bản dịch")
    parser.add_argument("--codex-sandbox", default="workspace-write",
                        choices=["read-only", "workspace-write", "danger-full-access"],
                        help="sandbox của Codex (mặc định workspace-write)")
    args = parser.parse_intermixed_args()
    args.skill_dir = args.skill_dir.resolve()
    if not (args.skill_dir / "SKILL.md").exists():
        sys.exit(f"Không thấy SKILL.md trong {args.skill_dir}.")
    if args.khong_skill and (args.kieu_codex or args.trigger):
        sys.exit("--khong-skill không đi cùng --kieu-codex hay --trigger.")
    if args.codex and args.kieu_codex:
        sys.exit("--codex đã là Codex thật, không cần --kieu-codex.")
    if args.codex and not shutil.which("codex"):
        sys.exit("Cần Codex CLI: không thấy lệnh codex trong PATH.")
    if not args.codex and not shutil.which("claude"):
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
    if args.codex:
        ok, detail, error = codex_shell_works(args)
        if error:
            sys.exit("Codex báo lỗi trước khi chạy đề: " + error)
        if not ok:
            sys.exit("Codex không chạy được lệnh shell trong sandbox " + args.codex_sandbox + ", nên không đọc được skill "
                     "hay file đầu vào. Codex trả lời: " + detail.replace("\n", " ") +
                     "\nTrên Ubuntu 24.04 trở lên, xem phần Codex trong evals/README.md.")
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
