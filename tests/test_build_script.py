import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build-firmware.sh"

class BuildScriptTests(unittest.TestCase):
    def test_refuses_missing_checkout(self):
        with tempfile.TemporaryDirectory() as d:
            p = subprocess.run(["sh", str(SCRIPT)], cwd=d,
                               env={**os.environ, "OPENWRT_DIR": "nonexistent"},
                               capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("Missing OpenWrt checkout", p.stderr)

    def test_refuses_unconfigured_checkout(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "Makefile").write_text("all:\n\t@true\n")
            p = subprocess.run(["sh", str(SCRIPT)], cwd=d,
                               env={**os.environ, "OPENWRT_DIR": str(root)},
                               capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("Configure OpenWrt first", p.stderr)

    def test_refuses_no_device(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "Makefile").write_text("all:\n\t@true\n")
            (root / ".config").write_text("CONFIG_TARGET_ramips=y\n")
            p = subprocess.run(["sh", str(SCRIPT)], cwd=d,
                               env={**os.environ, "OPENWRT_DIR": str(root)},
                               capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("No selected device/profile", p.stderr)

if __name__ == "__main__":
    unittest.main()
