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

    def test_required_reserve(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "image.bin"
            path.write_bytes(b"x" * 10)
            cmd = [sys.executable, str(SCRIPT), str(path), "--max-bytes", "12"]
            self.assertEqual(subprocess.run(cmd + ["--reserve-bytes", "2"], capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run(cmd + ["--reserve-bytes", "3"], capture_output=True).returncode, 1)

    def test_negative_reserve_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "image.bin"
            path.write_bytes(b"x")
            cmd = [sys.executable, str(SCRIPT), str(path), "--max-bytes", "12",
                   "--reserve-bytes", "-1"]
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)

    def test_reserve_cannot_exceed_budget(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "image.bin"
            path.write_bytes(b"x")
            cmd = [sys.executable, str(SCRIPT), str(path), "--max-bytes", "12",
                   "--reserve-bytes", "12"]
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)

    def test_invalid_budget(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "image.bin"
            path.write_bytes(b"x")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--max-bytes", "0"], capture_output=True)
            self.assertNotEqual(result.returncode, 0)

if __name__ == "__main__":
    unittest.main()
