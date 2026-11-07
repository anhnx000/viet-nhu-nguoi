"""Kiểm máy quét: bắt được dấu hiệu văn AI, không báo nhầm câu tự nhiên.

Chạy: python3 -m unittest discover -s tests
"""
import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCAN_PATH = ROOT / "skills/viet-nhu-nguoi/scripts/scan.py"
FACTS_PATH = ROOT / "skills/viet-nhu-nguoi/scripts/check_facts.py"
SPEC = importlib.util.spec_from_file_location("scan", SCAN_PATH)
scan = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scan)


def groups(text):
    hits, _ = scan.scan(text)
    return set(hits)


class DetectsAiTells(unittest.TestCase):
    def test_translationese_passive(self):
        self.assertIn("văn dịch (vi)", groups("Tính năng được phát triển bởi đội kỹ sư."))

    def test_this_it_sentence_start(self):
        self.assertIn('"Điều này"/"Nó" mở câu', groups("Hệ thống chạy. Điều này giúp tiết kiệm."))

    def test_empty_verbs(self):
        self.assertIn("động từ rỗng (vi)", groups("Nhóm tiến hành thực hiện việc rà soát."))

    def test_nominalisation(self):
        self.assertIn("danh hóa (vi)", groups("Làm việc một cách hiệu quả."))

    def test_redundancy(self):
        self.assertIn("thừa nghĩa (vi)", groups("Dự án hiện nay đang chạy."))

    def test_chain_of_cua(self):
        self.assertIn('chuỗi "của"', groups("Sự tăng của năng suất của nhân viên của công ty."))

    def test_english_gloss(self):
        self.assertIn("chêm tiếng Anh", groups("Cải thiện hiệu suất (performance) rõ."))

    def test_false_contrast(self):
        self.assertIn("đối lập giả", groups("Đây không chỉ là công cụ mà còn là người bạn."))

    def test_chatbot_closing(self):
        self.assertIn("lời chatbot", groups("Hy vọng những thông tin trên sẽ hữu ích cho bạn!"))

    def test_em_dash(self):
        self.assertIn("gạch ngang dài", groups("Kết quả — như dự đoán — rất tốt."))

    def test_example_before(self):
        text = (ROOT / "examples/truoc.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(groups(text)), 6)


class KeepsHumanText(unittest.TestCase):
    def test_casual_chat(self):
        self.assertEqual(groups("Mai mình ghé muộn chút nhé, bạn cứ ăn trước đi."), set())

    def test_dev_jargon(self):
        self.assertEqual(groups("Deploy xong rồi, anh check giúp em cái PR nhé."), set())

    def test_acronym_in_parens(self):
        self.assertEqual(groups("Phát hành theo giấy phép mã nguồn mở (MIT)."), set())

    def test_code_block_ignored(self):
        self.assertEqual(groups("```\nx = 'được gọi bởi' — tiến hành\n```"), set())

    def test_examples_after(self):
        for name in ("sau.md", "sau-co-chi-tiet.md"):
            text = (ROOT / "examples" / name).read_text(encoding="utf-8")
            self.assertEqual(groups(text), set(), name)


class Score(unittest.TestCase):
    def test_ai_draft_scores_high(self):
        text = (ROOT / "examples/truoc.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(scan.score(text, scan.scan(text)[0])["score"], 60)

    def test_rewrite_scores_zero(self):
        text = (ROOT / "examples/sau-co-chi-tiet.md").read_text(encoding="utf-8")
        result = scan.score(text, scan.scan(text)[0])
        self.assertEqual((result["score"], result["band"]), (0, "sạch"))

    def test_max_flag_exit_code(self):
        cmd = [sys.executable, "-I", str(SCAN_PATH), str(ROOT / "examples/truoc.md"), "--max", "30"]
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)
        cmd[3] = str(ROOT / "examples/sau.md")
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)


class CheckFacts(unittest.TestCase):
    def run_check(self, old, new):
        with tempfile.TemporaryDirectory() as d:
            a, b = pathlib.Path(d, "a.md"), pathlib.Path(d, "b.md")
            a.write_text(old, encoding="utf-8")
            b.write_text(new, encoding="utf-8")
            return subprocess.run([sys.executable, "-I", str(FACTS_PATH), str(a), str(b)],
                                  capture_output=True, text=True)

    def test_same_facts_pass(self):
        r = self.run_check("Bản 2.3 được phát hành bởi đội Android lúc 15:00 ngày 30/4.",
                           "Đội Android phát hành bản 2.3 lúc 15:00 ngày 30/4.")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_changed_number_fails(self):
        r = self.run_check("Doanh thu tăng 12% theo https://example.com/a.",
                           "Doanh thu tăng mạnh 15% theo https://example.com/a.")
        self.assertEqual(r.returncode, 1)
        self.assertIn("12%", r.stdout)
        self.assertIn("15%", r.stdout)

    def test_lost_code_fails(self):
        r = self.run_check("Chạy `npm test` trước khi push.", "Chạy test trước khi push.")
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
