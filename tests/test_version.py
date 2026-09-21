from pathlib import Path
import re
import tomllib
import unittest

import firstwindow


class VersionConsistencyTests(unittest.TestCase):
    def test_package_and_runtime_versions_match(self):
        project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(firstwindow.__version__, project["project"]["version"])

    def test_release_candidate_version(self):
        project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
        version = project["project"]["version"]
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        init_text = Path("src/firstwindow/__init__.py").read_text(encoding="utf-8")
        match = re.search(r'__version__\s*=\s*"([^"]+)"', init_text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), version)


if __name__ == "__main__":
    unittest.main()
