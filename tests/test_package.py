"""Kiểm gói skill: phiên bản, số mục trong danh mục và điểm ví dụ trong README."""

import contextlib
import importlib.util
import io
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/viet-nhu-nguoi/SKILL.md"
PATTERNS = ROOT / "skills/viet-nhu-nguoi/references/patterns.md"

# Mỗi repo trong bảng "Cách tổ chức skill trong các repo nhiều sao" (references/sources.md) ứng với một chỗ
# áp dụng: câu trong hướng dẫn mà trợ lý mở được hoặc ID đề thử. Thêm repo vào bảng thì phải thêm dòng ở đây.
LESSONS = {
    "mattpocock/skills": "hai đến bốn câu gộp một lượt",
    "obra/superpowers": "Sau khi ghi, đọc lại phần vừa sửa trên đĩa",
    "multica-ai/andrej-karpathy-skills": "chép nguyên những câu nằm ngoài phần được nhờ sửa",
    "anthropics/skills": "eval:sua-tin-gian-giu-nguyen",
    "DietrichGebert/ponytail": "chỗ nào không chỉ ra được dấu hiệu cụ thể thì trả về câu gốc",
    "nextlevelbuilder/ui-ux-pro-max-skill": "## Chọn chế độ theo lời người dùng",
    "Graphify-Labs/graphify": "Nếu người dùng nhắc số mục, tra thẳng số đó",
    "garrytan/gstack": "Xong thì báo đã rà bao nhiêu mục",
    "JuliusBrussee/caveman": "scripts/check_facts.py <gốc> <mới>",
    "addyosmani/agent-skills": "thiếu nội dung chính thì hỏi trước",
    "Leonxlnx/taste-skill": "eval:doi-lich-dat-phong",
    "pbakaus/impeccable": "Kiểm trên chính bản sắp gửi",
    "Egonex-AI/Understand-Anything": "File dài thì đọc từng phần cho tới hết",
    "career-ops-hq/career-ops": "ghi một ghi chú Markdown ở nơi họ chọn",
    "ComposioHQ/awesome-claude-skills": "Dữ kiện của bài mới lấy từ lời dặn",
    "cloudflare/security-audit-skill": "Gợi ý thay đúng cụm hoặc câu vừa chỉ ra",
    "blader/humanizer": "Câu nào giữ lại cũng phải cho người đọc điều họ chưa có",
    "mvanhorn/last30days-skill": "ghi riêng việc đã chốt và việc còn chờ",
    "cathrynlavery/diagram-design": "dùng lại những nét giọng đã xác nhận cho đúng người đọc và thể loại",
    "ayghri/i-have-adhd": "Việc người nhận cần làm (trả lời, duyệt, có mặt lúc mấy giờ) đặt ở câu đầu",
    "Nutlope/hallmark": "xưng hô có nhất quán không",
    "zhaoxuya520/reverse-skill": "(references/spoken.md)",
    "virgiliojr94/book-to-skill": "Rà cả tên, số, chuyện kể và chữ chỉ thời điểm lấy từ mẫu",
    "AgriciDaniel/claude-seo": "eval:hop-tom",
    "wheresryan22/anatomy": "eval:hop-got",
    "OthmanAdi/planning-with-files": "Lần sau đọc lại ghi chú khi viết cho đúng đối tượng",
    "earthtojake/text-to-cad": "Sau khi ghi, đọc lại phần vừa sửa trên đĩa",
}


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class Package(unittest.TestCase):
    def test_versions_match(self):
        skill = re.search(r'^\s+version:\s*"([^"]+)"', SKILL.read_text(encoding="utf-8"), re.M).group(1)
        plugin = json.loads(read(".claude-plugin/plugin.json"))["version"]
        market = json.loads(read(".claude-plugin/marketplace.json"))["plugins"][0]["version"]
        changelog = re.search(r"^## (\S+)", read("CHANGELOG.md"), re.M).group(1)
        self.assertEqual({skill, plugin, market, changelog}, {skill})
        self.assertIn(f"\n## {skill}\n", read("RELEASE_NOTES.md"), "thiếu ghi chú phát hành tiếng Anh cho bản này")

    def test_codex_metadata_names_the_skill(self):
        """Codex hiện tên và lời gọi mẫu từ agents/openai.yaml; lời gọi phải trỏ đúng tên skill."""
        meta = read("skills/viet-nhu-nguoi/agents/openai.yaml")
        name = re.search(r"^name:\s*(\S+)", SKILL.read_text(encoding="utf-8"), re.M).group(1)
        self.assertIn("display_name:", meta)
        self.assertIn(f"${name} ", meta)

    def test_each_studied_skill_has_an_application(self):
        """Bài học từ mỗi repo trong bảng top-20 phải có chỗ áp dụng thật trong skill hoặc bộ đề."""
        table = read("skills/viet-nhu-nguoi/references/sources.md").split("## Cách tổ chức skill", 1)[1]
        repos = re.findall(r"^\| \d+ \| \[([^\]]+)\]", table, re.M)
        self.assertGreaterEqual(len(repos), 20)
        self.assertEqual(set(repos), set(LESSONS))
        # Chỉ tính hướng dẫn đi tới được từ file chính, bỏ bảng nguồn tự mô tả.
        pending = [SKILL]
        visited = {}
        while pending:
            path = pending.pop()
            if path in visited:
                continue
            content = path.read_text(encoding="utf-8")
            visited[path] = content
            for link in re.findall(r"\]\(([^():#]+\.md)(?:#[^)]*)?\)", content):
                target = (path.parent / link).resolve()
                self.assertTrue(target.is_file(), f"{path.name} dẫn sai tới {link}")
                if target.name != "sources.md":
                    pending.append(target)
        guides = set(PATTERNS.parent.rglob("*.md")) - {PATTERNS.with_name("sources.md")}
        self.assertEqual(set(visited), guides | {SKILL})
        skill = "\n".join(visited.values())
        ids = {s["id"] for s in json.loads(read("evals/scenarios.json"))}
        for repo, anchor in LESSONS.items():
            if anchor.startswith("eval:"):
                self.assertIn(anchor[5:], ids, repo)
            else:
                self.assertIn(anchor, skill, repo)

    def test_patterns_numbered_without_gaps(self):
        nums = [int(n) for n in re.findall(r"^### (\d+)\.", PATTERNS.read_text(encoding="utf-8"), re.M)]
        self.assertEqual(nums, list(range(1, len(nums) + 1)))

    def test_lookup_returns_only_requested_patterns(self):
        script = SKILL.parent / "scripts/patterns.py"

        def lookup(*keys):
            return subprocess.run(
                [sys.executable, "-I", str(script), *keys], cwd=ROOT,
                capture_output=True, text=True, encoding="utf-8",
            )

        catalog = PATTERNS.read_text(encoding="utf-8")
        index = lookup()
        self.assertEqual(index.stdout.splitlines(), re.findall(r"^#{2,3} (?:[A-Z]|\d+)\. .+", catalog, re.M))
        result = lookup("55", "l")
        self.assertEqual(result.returncode, 0, result.stderr)
        group_l = catalog.split("\n## L. ", 1)[1].split("\n## ", 1)[0]
        numbers = r"^### (\d+)\."
        self.assertEqual(re.findall(numbers, result.stdout, re.M), ["55", *re.findall(numbers, group_l, re.M)])
        self.assertNotIn("## Giữ lại", result.stdout)
        self.assertNotIn("<a id=", result.stdout)
        self.assertIn("**Trước", result.stdout)
        self.assertIn("**Sau", result.stdout)
        error = lookup("1", "0")
        self.assertNotEqual(error.returncode, 0)
        self.assertEqual(error.stdout, "")

    def test_readme_scores_match_scanner(self):
        """Điểm ví dụ ghi trong README (và vẽ trong ảnh assets/) phải đúng điểm bộ kiểm tra chấm bây giờ."""
        spec = importlib.util.spec_from_file_location("scan", ROOT / "skills/viet-nhu-nguoi/scripts/scan.py")
        scan = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(scan)

        def score(name):
            text = read(f"examples/{name}")
            return scan.score(text, scan.scan(text)[0])["score"]

        readme = read("README.md")
        self.assertIn(f"AI viết được {score('truoc.md')}/100", readme)
        self.assertIn(f"Bài gốc, {score('bai-dang-truoc.md')}/100", readme)
        self.assertIn(f"Original, {score('bai-dang-truoc.md')}/100", read("README.en.md"))
        for name in ("sau.md", "sau-co-chi-tiet.md", "bai-dang-sau.md"):
            self.assertEqual(score(name), 0, name)


class Evals(unittest.TestCase):
    """Bộ đề thử skill: file đề hợp lệ, script chấm phân biệt được câu trả lời đúng và sai."""

    def setUp(self):
        spec = importlib.util.spec_from_file_location("evals_check", ROOT / "evals/check.py")
        self.check = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.check)
        cases = json.loads(read("evals/scenarios.json")) + json.loads(read("evals/held-out.json"))
        self.scenarios = {s["id"]: s for s in cases}
        self.assertEqual(len(self.scenarios), len(cases), "trùng ID đề thử")

    def test_scenarios_are_well_formed(self):
        known = {"min_words", "max_words", "min_questions", "max_questions", "max_placeholders", "max_bold",
                 "must_keep", "must_not", "min_refs", "min_overlap", "max_overlap", "scan_max",
                 "max_added_numbers", "lead_keep", "must_read", "must_not_read", "allow_read", "max_refs"}
        self.assertGreaterEqual(len(self.scenarios), 16)
        for sid, sc in self.scenarios.items():
            self.assertTrue(sc["tin_nhan"] and sc["mong_doi"], sid)
            self.assertLessEqual(set(sc["kiem"]), known, sid)
            if "tep" in sc:
                self.assertTrue((ROOT / sc["tep"]).exists(), sc["tep"])
                self.assertIn("{tep}", sc["tin_nhan"], sid)

    def test_refs_accept_capitals_and_comma_lists(self):
        scenario = {"kiem": {"min_refs": 3}}
        for reply in ("Mục 4, 50, 45", "mục 4, mục 50, mục 45", "(4, 50, 45)"):
            self.assertEqual(self.check.check(scenario, reply), [])
        self.assertTrue(self.check.check(scenario, "Mục 4, 4, 4"))
        self.assertTrue(self.check.check(scenario, "Có 4, 50, 45 người."))

    def test_questions_do_not_require_numbering(self):
        scenario = {"kiem": {"min_questions": 2, "max_questions": 2}}
        for reply in ("Quán ở đâu? Bài đăng ở đâu?",
                      "- Quán ở đâu?\n- Bài đăng ở đâu?",
                      "1. Quán ở đâu?\n2. Bài đăng ở đâu?",
                      "Quán ở đâu??? Bài đăng ở đâu?"):
            self.assertEqual(self.check.check(scenario, reply), [])
        self.assertTrue(self.check.check(scenario, "1. Quán rất đẹp.\n2. Món uống rất ngon."))

    def test_asking_passes_and_fill_in_frame_fails(self):
        sc = self.scenarios["viet-bai-thieu-chuyen-rieng"]
        asks = ("Bài kiểu này cần chuyện thật của bạn, mình hỏi mấy câu, trả lời tắt cũng được:\n"
                "1. Năm bài học đó là gì?\n2. Có bài học nào gắn với một lần làm hỏng không?\n"
                "3. Bạn viết cho ai đọc?")
        self.assertEqual(self.check.check(sc, asks), [])
        frame = asks + "\n\nTrong lúc chờ, đây là bản khung:\n" + "\n".join(
            f"{i}. Bài học {i}: [chuyện của bạn]" for i in range(4, 9))
        self.assertTrue(self.check.check(sc, frame))

    def test_invented_number_fails(self):
        sc = self.scenarios["viet-email-du-du-kien"]
        good = ("Anh Huân ơi, máy em (mã LT-0412) không lên nguồn từ sáng thứ Ba 17/11, "
                "anh cho em mượn máy tạm trong lúc chờ sửa được không ạ? Em cảm ơn anh. Huệ")
        self.assertEqual(self.check.check(sc, good), [])
        padded = good.replace("không lên nguồn", "đã bấm nút nguồn 5 lần vẫn không lên nguồn")
        self.assertTrue(any("tự thêm số" in e for e in self.check.check(sc, padded)))

    def test_lost_fact_fails(self):
        sc = self.scenarios["viet-tin-cat-nuoc"]
        good = "Thứ Năm 17/12 tòa B cắt nước từ 9h đến 15h để sửa bể ngầm, có gì gọi ban quản lý 0900 000 000."
        self.assertEqual(self.check.check(sc, good), [])
        self.assertTrue(self.check.check(sc, good.replace("15h", "16h")))

    def test_informal_text_keeps_its_register(self):
        sc = self.scenarios["sua-tin-gian-giu-nguyen"]
        src = read(sc["tep"]).strip()
        self.assertEqual(self.check.check(sc, "Tin này đọc đã tự nhiên, gửi luôn được:\n\n" + src), [])
        polite = ("Chào shop ạ, shop giao sai màu lần 2 rồi. Mình đặt màu đen nhưng nhận màu xám. "
                  "Việc bắt mình tự trả phí ship là vô lý. Nếu không đổi, mình sẽ báo sàn ạ.")
        self.assertTrue(self.check.check(sc, polite))

    def test_ask_must_lead_the_message(self):
        sc = self.scenarios["doi-lich-dat-phong"]
        lead = "Anh ơi, anh đổi giúp em lịch đặt phòng họp từ 9h sang 14h nhé. Phòng đang sửa."
        self.assertEqual(self.check.check(sc, lead), [])
        buried = ("Anh ơi, sáng nay bên em kiểm tra thì thấy phòng họp tầng ba đang sửa điện, thợ báo "
                  "phải làm hết buổi sáng mới xong, cả nhóm đã bàn lại với nhau rồi. Nhờ anh đổi lịch sang 14h.")
        self.assertTrue(self.check.check(sc, buried))

    def test_word_terms_match_whole_words_only(self):
        sc = {"kiem": {"must_keep": ["mùng 4"], "must_not": ["ông", "=))"]}}
        self.assertEqual(self.check.check(sc, "Mùng 4 tau đi được, không ở lại đêm"), [])
        self.assertTrue(self.check.check(sc, "Mùng 4 ông đi không"))
        self.assertTrue(self.check.check(sc, "mùng 4 nha =))"))

    def test_alternative_wording_and_reference_styles(self):
        chat = self.scenarios["chat-tra-loi-pm"]
        self.assertEqual(self.check.check(chat, "dạ 9h tối nay lên chị ạ, Khải trực, test trên staging r, lỗi thì rollback 10 phút"), [])
        audit = dict(self.scenarios["soi-bai-ai"], kiem={"min_refs": 3})
        self.assertEqual(self.check.check(audit, "1. Câu mở (45, 3). 2. Câu kết (mục 50)."), [])
        self.assertTrue(self.check.check(audit, "Bài có vài chỗ nghe giống AI."))

    def test_opened_files_from_trace(self):
        trace = [("Read", {"file_path": ".claude/skills/viet-nhu-nguoi/references/chat.md"}, True),
                 ("Read", {"file_path": "s/references/patterns.md", "offset": 120, "limit": 40}, True),
                 ("Bash", {"command": "cd .claude/skills/viet-nhu-nguoi && cat references/voice.md"}, True),
                 ("Bash", {"command": "cat references/slides.md"}, False),
                 ("Bash", {"command": "cd s/references && sed -n 1,30p sources.md"}, True),
                 ("Bash", {"command": "python3 -I scripts/scan.py review-dan-tu-chat.md"}, True),
                 ("Read", {"file_path": "review-dan-tu-chat.md"}, True)]
        self.assertEqual(self.check.opened(trace), {"chat.md": True, "patterns.md": False, "voice.md": True,
                                                    "sources.md": False, "scan.py": False})

    def test_routing_rules(self):
        rules = {"must_read": ["chat-group.md"], "must_not_read": ["slides.md"], "max_refs": 2}
        route = self.check.check_trace
        chat = ("Read", {"file_path": "s/references/chat.md"}, True)
        group = ("Read", {"file_path": "s/references/chat-group.md"}, True)
        self.assertEqual(route(rules, [chat, group]), [])
        self.assertTrue(route(rules, [chat]))
        self.assertTrue(route(rules, [chat, group[:2] + (False,)]))  # lệnh bị chặn không tính
        self.assertTrue(route(rules, [chat, group, ("Bash", {"command": "cat references/slides.md"}, True)]))
        lookup = {"must_read": [["patterns.py", "patterns.md"]], "max_refs": 0}
        self.assertEqual(route(lookup, [("Bash", {"command": "python3 -I scripts/patterns.py 46"}, True)]), [])

    def test_full_catalog_read_needs_allow_read(self):
        full = [("Read", {"file_path": "s/references/patterns.md"}, True)]
        part = [("Read", {"file_path": "s/references/patterns.md", "offset": 300, "limit": 30}, True)]
        self.assertTrue(self.check.check_trace({}, full))
        self.assertEqual(self.check.check_trace({}, part), [])
        self.assertEqual(self.check.check_trace({"allow_read": ["patterns.md"]}, full), [])

    def test_slide_and_catalog_pointers_are_not_invented_numbers(self):
        sc = {"tin_nhan": "Doanh thu 12,4 tỷ, tăng 8%.", "kiem": {"max_added_numbers": 0}}
        self.assertEqual(self.check.check(sc, "Slide 2 và slide 3-5 chưa có số. Câu mở rơi vào mục 45, 46. Doanh thu 12,4 tỷ."), [])
        self.assertTrue(self.check.check(sc, "Slide 2: doanh thu 12,4 tỷ, lãi 15%."))

    def test_bad_answers_fail(self):
        """Câu trả lời rỗng trượt mọi đề; chép nguyên bài gốc trượt mọi đề có file, trừ đề mà bài gốc đã ổn."""
        source_is_fine = {"sua-nhe-bai-nguoi-viet", "sua-tin-gian-giu-nguyen", "sua-tin-nhan-sep"}
        for sid, sc in self.scenarios.items():
            with self.subTest(sid):
                self.assertTrue(self.check.check(sc, ""))
                if "tep" in sc and sid not in source_is_fine:
                    source = self.check.check_facts.read(str(ROOT / sc["tep"]))
                    self.assertTrue(self.check.check(sc, source), "chép nguyên bài gốc mà vẫn qua")

    def test_old_traces_and_pass_rate_over_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "old.json").write_text(json.dumps([["Read", {"file_path": "s/references/chat.md"}]]))
            self.assertEqual(self.check.load_trace(root / "old.json"), [("Read", {"file_path": "s/references/chat.md"}, True)])
            scenarios = [{"id": "a", "kiem": {"must_keep": ["15h"]}}, {"id": "b", "kiem": {"must_read": ["chat.md"]}}]
            chat = {"tools": [["Read", {"file_path": "s/references/chat.md"}, True]]}
            for run, reply in (("1", "15h"), ("2", "16h"), ("3", "15h")):
                (root / run).mkdir()
                (root / run / "a.md").write_text(reply)
                (root / run / "b.md").write_text("ok")
                (root / run / "b.json").write_text(json.dumps(chat if run != "3" else {"tools": []}))
            # lượt không bật skill: không chấm đường đọc
            (root / "1" / "a.json").write_text(json.dumps({"skill": False, "tools": []}))
            folders = self.check.run_dirs(root)
            self.assertEqual([f.name for f in folders], ["1", "2", "3"])
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(self.check.report(scenarios, folders), 1)
            text = out.getvalue()
            self.assertIn("TRƯỢT  a (2/3): lượt 2: mất dữ kiện", text)
            self.assertIn("QUA    b (3/3)  · đường đọc: lượt 3: không mở chat.md", text)  # đường đọc không làm đề trượt
            self.assertIn("5/6 lượt qua phần tự động (83%, khoảng tin cậy 95%: 44-97%). 1/2 đề qua cả 3 lượt.", text)
            self.assertIn("Đường đọc đúng ở 2/3 lượt có vết.", text)
            self.assertEqual([round(x, 2) for x in self.check.wilson(3, 3)], [0.44, 1.0])

    def test_trigger_set_is_well_formed(self):
        cases = json.loads(read("evals/trigger.json"))
        held = json.loads(read("evals/trigger-held-out.json"))
        ids = [c["id"] for c in cases + held]
        self.assertEqual(len(set(ids)), len(ids), "trùng ID đề bật skill")
        for c in cases + held:
            self.assertIn(c["bat"], (True, False, None), c["id"])
            self.assertTrue(c["tin_nhan"], c["id"])
            self.assertNotIn("viet-nhu-nguoi", c["tin_nhan"], "lời nhờ không được gọi tên skill")
            if "tep" in c:
                self.assertTrue((ROOT / c["tep"]).exists(), c["tep"])
                self.assertIn("{tep}", c["tin_nhan"], c["id"])
        wants = [c["bat"] for c in cases]
        self.assertGreaterEqual(wants.count(True), 15)
        self.assertGreaterEqual(wants.count(False), 10)

    def test_trigger_grading(self):
        skill = ["Skill", {"skill": "viet-nhu-nguoi"}, True]
        codex = ["Bash", {"command": "cat .agents/skills/viet-nhu-nguoi/SKILL.md"}, True]
        other = ["Read", {"file_path": "cong-van.md"}, True]
        self.assertTrue(self.check.used_skill([tuple(skill)]))
        self.assertTrue(self.check.used_skill([tuple(codex)]))
        self.assertFalse(self.check.used_skill([tuple(other)]))
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            cases = [{"id": "nen", "bat": True}, {"id": "khong", "bat": False}, {"id": "tuy", "bat": None}]
            for run in ("1", "2"):
                (root / run).mkdir()
                (root / run / "nen.json").write_text(json.dumps({"tools": [skill] if run == "1" else [other]}))
                (root / run / "khong.json").write_text(json.dumps({"tools": [other]}))
                (root / run / "tuy.json").write_text(json.dumps({"tools": [codex]}))
                for sid in ("nen", "khong", "tuy"):
                    (root / run / f"{sid}.md").write_text("trả lời", encoding="utf-8")
            # Lượt hết hạn mức chỉ có vết, không có câu trả lời: báo thiếu, không đếm là không bật.
            cases.append({"id": "loi", "bat": True})
            (root / "1" / "loi.json").write_text(json.dumps({"tools": [], "error": "out of credits"}))
            (root / "2" / "loi.json").write_text(json.dumps({"tools": [skill]}))
            (root / "2" / "loi.md").write_text("trả lời", encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(self.check.report_trigger(cases, self.check.run_dirs(root)), 2)
            text = out.getvalue()
            self.assertIn("THIẾU  loi (nên bật): bật 1/1 lượt", text)
            self.assertIn("SAI    nen (nên bật): bật 1/2 lượt", text)
            self.assertIn("ĐÚNG   khong (không nên bật): bật 0/2 lượt", text)
            self.assertIn("Nên bật: bật 2/3 lượt", text)
            self.assertIn("Tùy: bật 2/2 lượt.", text)

    def test_codex_output_is_parsed_like_claude_traces(self):
        spec = importlib.util.spec_from_file_location("evals_run", ROOT / "evals/run.py")
        run = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(run)
        self.assertEqual(run.unwrap("/bin/bash -lc 'sed -n 1,80p references/edit.md'"), "sed -n 1,80p references/edit.md")
        self.assertEqual(run.unwrap("cat a.md"), "cat a.md")
        events = [
            {"type": "item.completed", "item": {"type": "agent_message", "text": "Mình dùng skill."}},
            {"type": "item.completed", "item": {"type": "command_execution", "status": "completed", "exit_code": 0,
                                                "command": "/bin/bash -lc 'cat .agents/skills/viet-nhu-nguoi/SKILL.md'"}},
            {"type": "item.completed", "item": {"type": "command_execution", "status": "failed", "exit_code": 1,
                                                "command": "/bin/bash -lc 'cat references/edit.md'"}},
            {"type": "item.completed", "item": {"type": "agent_message", "text": "Bản sửa"}},
            {"type": "turn.completed", "usage": {"input_tokens": 10}},
        ]
        answer, trace = run.parse_codex("\n".join(json.dumps(e) for e in events) + "\nkhông phải JSON\n")
        self.assertEqual(answer, "Bản sửa")
        self.assertEqual(trace["usage"], {"input_tokens": 10})
        self.assertFalse(trace["sandbox_broken"])
        tools = [tuple(t) for t in trace["tools"]]
        self.assertTrue(self.check.used_skill(tools))
        self.assertEqual(self.check.opened(tools), {})  # lệnh lỗi không tính là đã đọc
        broken = {"type": "item.completed", "item": {"type": "agent_message", "text": "Lỗi `bwrap: setting up uid map`"}}
        self.assertTrue(run.parse_codex(json.dumps(broken))[1]["sandbox_broken"])

    def test_kept_facts_ignore_line_breaks(self):
        sc = self.scenarios["lap-giu"]
        self.assertEqual(self.check.check(sc, "Tôi nhớ bến nước.  \nTôi nhớ cây cầu.\nTôi nhớ tiếng dép của mẹ."), [])
        self.assertTrue(self.check.check(sc, "Tôi nhớ bến nước. Tôi nhớ tiếng dép của mẹ."))

    def test_reference_answers_pass(self):
        """Mỗi đề có một đáp án mẫu trong evals/dap-an/ và đáp án ấy phải qua check.py.

        Điều kiện chấm đặt sai (câu trả lời đúng mà vẫn trượt) thì test báo ngay, không đợi tới lượt chạy thật.
        """
        folder = ROOT / "evals/dap-an"
        for sid, sc in self.scenarios.items():
            with self.subTest(sid):
                path = folder / f"{sid}.md"
                self.assertTrue(path.exists(), f"thiếu đáp án mẫu {path.name}")
                self.assertEqual(self.check.check(sc, path.read_text(encoding="utf-8")), [])
        self.assertFalse({p.stem for p in folder.glob("*.md")} - set(self.scenarios), "đáp án không ứng với đề nào")

    def test_routing_rules_name_real_files(self):
        skill = ROOT / "skills/viet-nhu-nguoi"
        names = {p.name for p in (skill / "references").glob("*.md")} | {p.name for p in (skill / "scripts").glob("*.py")}
        for sid, sc in self.scenarios.items():
            for key in ("must_read", "must_not_read", "allow_read"):
                for item in sc["kiem"].get(key, []):
                    for name in item if isinstance(item, list) else [item]:
                        self.assertIn(name, names, f"{sid}: {key} nhắc tới {name}")


if __name__ == "__main__":
    unittest.main()
