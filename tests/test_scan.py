"""Kiểm máy quét: bắt được dấu hiệu văn AI, không báo nhầm câu tự nhiên.

Chạy: python3 -m unittest discover -s tests
"""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "scan", ROOT / "skills/vietnamese-humanizer/scripts/scan.py")
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


if __name__ == "__main__":
    unittest.main()
