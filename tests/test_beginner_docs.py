from pathlib import Path
import re
import unittest


class BeginnerDocsTests(unittest.TestCase):
    def _quickstart(self, path: str) -> str:
        text = Path(path).read_text(encoding="utf-8")
        start = text.index("<!-- QUICKSTART:START -->")
        end = text.index("<!-- QUICKSTART:END -->")
        return text[start:end]

    def test_english_and_chinese_quickstarts_have_five_steps(self):
        for path in ("docs/BEGINNER.md", "docs/BEGINNER.zh-CN.md"):
            quickstart = self._quickstart(path)
            steps = re.findall(r"(?m)^([1-5])\. \*\*", quickstart)
            self.assertEqual(steps, ["1", "2", "3", "4", "5"])

    def test_quickstart_hides_advanced_internal_terms(self):
        banned = ("attestation", "AC-001", "AC-002", "firstwindowzero")
        for path in ("docs/BEGINNER.md", "docs/BEGINNER.zh-CN.md"):
            quickstart = self._quickstart(path)
            for term in banned:
                self.assertNotIn(term, quickstart)

    def test_guides_link_to_each_other(self):
        english = Path("docs/BEGINNER.md").read_text(encoding="utf-8")
        chinese = Path("docs/BEGINNER.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("[简体中文](BEGINNER.zh-CN.md)", english)
        self.assertIn("[English](BEGINNER.md)", chinese)

    def test_readme_surfaces_both_beginner_guides(self):
        readme = Path("README.md").read_text(encoding="utf-8")
        self.assertIn("docs/BEGINNER.md", readme)
        self.assertIn("docs/BEGINNER.zh-CN.md", readme)


if __name__ == "__main__":
    unittest.main()
