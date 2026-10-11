import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-budget.py"

class BudgetTests(unittest.TestCase):
    def test_exact_fit(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "image.bin"
            path.write_bytes(b"x" * 12)
            result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--max-bytes", "12"], capture_output=True)
            self.assertEqual(result.returncode, 0)

    def test_over_budget(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "image.bin"
            path.write_bytes(b"x" * 13)
            result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--max-bytes", "12"], capture_output=True)
            self.assertEqual(result.returncode, 1)

    def test_invalid_budget(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "image.bin"
            path.write_bytes(b"x")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--max-bytes", "0"], capture_output=True)
            self.assertNotEqual(result.returncode, 0)

if __name__ == "__main__":
    unittest.main()
