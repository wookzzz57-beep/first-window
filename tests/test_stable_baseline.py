from pathlib import Path
import unittest

from check_stable_baseline import validate_stable_baseline


class StableBaselineTests(unittest.TestCase):
    def test_repository_matches_stable_baseline(self):
        self.assertEqual(validate_stable_baseline(Path(".")), [])


if __name__ == "__main__":
    unittest.main()
