"""Kiểm gói skill: phiên bản khớp nhau, danh mục đánh số liền, README ghi đúng số dấu hiệu, SKILL.md không phình."""

import importlib.util
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/viet-nhu-nguoi/SKILL.md"
PATTERNS = ROOT / "skills/viet-nhu-nguoi/references/patterns.md"


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class Package(unittest.TestCase):
    def test_versions_match(self):
        skill = re.search(r'^\s+version:\s*"([^"]+)"', SKILL.read_text(encoding="utf-8"), re.M).group(1)
        plugin = json.loads(read(".claude-plugin/plugin.json"))["version"]
        market = json.loads(read(".claude-plugin/marketplace.json"))["plugins"][0]["version"]
        changelog = re.search(r"^## (\S+)", read("CHANGELOG.md"), re.M).group(1)
        self.assertEqual({skill, plugin, market, changelog}, {skill})

    def test_patterns_numbered_without_gaps(self):
        nums = [int(n) for n in re.findall(r"^### (\d+)\.", PATTERNS.read_text(encoding="utf-8"), re.M)]
        self.assertEqual(nums, list(range(1, len(nums) + 1)))

    def test_readmes_state_pattern_count(self):
        count = len(re.findall(r"^### \d+\.", PATTERNS.read_text(encoding="utf-8"), re.M))
        self.assertIn(f"{count} dấu hiệu", read("README.md"))
        self.assertIn(f"{count} AI-writing patterns", read("README.en.md"))

    def test_skill_length_cap(self):
        body = SKILL.read_text(encoding="utf-8").split("---", 2)[2]
        self.assertLessEqual(len(body.split()), 6000, "SKILL.md đọc lại mỗi lần dùng; cắt bớt trước khi thêm")


class Evals(unittest.TestCase):
    """Bộ đề thử skill: file đề hợp lệ, script chấm phân biệt được câu trả lời đúng và sai."""

    def setUp(self):
        spec = importlib.util.spec_from_file_location("evals_check", ROOT / "evals/check.py")
        self.check = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.check)
        self.scenarios = {s["id"]: s for s in json.loads(read("evals/scenarios.json"))}

    def test_scenarios_are_well_formed(self):
        known = {"min_words", "max_words", "min_questions", "max_questions", "max_placeholders", "max_bold",
                 "must_keep", "must_not", "min_refs", "min_overlap", "max_overlap", "scan_max"}
        self.assertGreaterEqual(len(self.scenarios), 16)
        for sid, sc in self.scenarios.items():
            self.assertTrue(sc["tin_nhan"] and sc["mong_doi"], sid)
            self.assertLessEqual(set(sc["kiem"]), known, sid)
            if "tep" in sc:
                self.assertTrue((ROOT / sc["tep"]).exists(), sc["tep"])
                self.assertIn("{tep}", sc["tin_nhan"], sid)

    def test_asking_passes_and_fill_in_frame_fails(self):
        sc = self.scenarios["viet-bai-thieu-chuyen-rieng"]
        asks = ("Bài kiểu này cần chuyện thật của bạn, mình hỏi mấy câu, trả lời tắt cũng được:\n"
                "1. Năm bài học đó là gì?\n2. Có bài học nào gắn với một lần làm hỏng không?\n"
                "3. Bạn viết cho ai đọc?")
        self.assertEqual(self.check.check(sc, asks), [])
        frame = asks + "\n\nTrong lúc chờ, đây là bản khung:\n" + "\n".join(
            f"{i}. Bài học {i}: [chuyện của bạn]" for i in range(4, 9))
        self.assertTrue(self.check.check(sc, frame))

    def test_lost_fact_fails(self):
        sc = self.scenarios["viet-tin-cat-nuoc"]
        good = "Thứ Năm 17/12 tòa B cắt nước từ 9h đến 15h để sửa bể ngầm, có gì gọi ban quản lý 0900 000 000."
        self.assertEqual(self.check.check(sc, good), [])
        self.assertTrue(self.check.check(sc, good.replace("15h", "16h")))

    def test_alternative_wording_and_reference_styles(self):
        chat = self.scenarios["chat-tra-loi-pm"]
        self.assertEqual(self.check.check(chat, "dạ 9h tối nay lên chị ạ, Tú trực, test trên staging r, lỗi thì rollback 10 phút"), [])
        audit = dict(self.scenarios["soi-bai-ai"], kiem={"min_refs": 3})
        self.assertEqual(self.check.check(audit, "1. Câu mở (45, 3). 2. Câu kết (mục 50)."), [])
        self.assertTrue(self.check.check(audit, "Bài có vài chỗ nghe giống AI."))


if __name__ == "__main__":
    unittest.main()
