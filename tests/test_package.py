"""Kiểm gói skill: phiên bản khớp nhau, danh mục đánh số liền, README ghi đúng số dấu hiệu, SKILL.md không phình."""

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


if __name__ == "__main__":
    unittest.main()
