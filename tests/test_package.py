"""Kiểm gói skill: phiên bản, số mục trong danh mục và điểm ví dụ trong README."""

import importlib.util
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/viet-nhu-nguoi/SKILL.md"
PATTERNS = ROOT / "skills/viet-nhu-nguoi/references/patterns.md"

# Mỗi repo trong bảng "Cách tổ chức skill trong các repo nhiều sao" (references/sources.md) ứng với một chỗ
# áp dụng: câu trong SKILL.md hoặc ID đề thử. Thêm repo vào bảng thì phải thêm dòng ở đây.
LESSONS = {
    "mattpocock/skills": "hai đến bốn câu gộp một lượt",
    "obra/superpowers": "## Những lúc dễ tự bào chữa",
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
        skill = SKILL.read_text(encoding="utf-8")
        ids = {s["id"] for s in json.loads(read("evals/scenarios.json"))}
        for repo, anchor in LESSONS.items():
            if anchor.startswith("eval:"):
                self.assertIn(anchor[5:], ids, repo)
            else:
                self.assertIn(anchor, skill, repo)

    def test_patterns_numbered_without_gaps(self):
        nums = [int(n) for n in re.findall(r"^### (\d+)\.", PATTERNS.read_text(encoding="utf-8"), re.M)]
        self.assertEqual(nums, list(range(1, len(nums) + 1)))

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
                 "max_added_numbers", "lead_keep"}
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


if __name__ == "__main__":
    unittest.main()
