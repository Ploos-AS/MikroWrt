import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "select-mango.sh"

class MangoSelectionTests(unittest.TestCase):
    def invoke(self, root):
        return subprocess.run(["sh", str(SCRIPT)], env={**os.environ, "OPENWRT_DIR": str(root)},
                              capture_output=True, text=True)

    def test_missing_tree(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertNotEqual(self.invoke(Path(d)).returncode, 0)

    def test_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "Makefile").write_text("all:\n")
            (root / ".config").write_text("existing\n")
            self.assertNotEqual(self.invoke(root).returncode, 0)
            self.assertEqual((root / ".config").read_text(), "existing\n")

    def test_requires_device_definition(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "Makefile").write_text("all:\n")
            (root / "target/linux/ramips/image").mkdir(parents=True)
            self.assertNotEqual(self.invoke(root).returncode, 0)

    def test_writes_candidate_config(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "Makefile").write_text("all:\n")
            image = root / "target/linux/ramips/image"
            image.mkdir(parents=True)
            (image / "mt76x8.mk").write_text("TARGET_DEVICES += glinet_gl-mt300n-v2\n")
            result = self.invoke(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("CONFIG_TARGET_ramips_mt76x8_DEVICE_glinet_gl-mt300n-v2=y",
                          (root / ".config").read_text())

if __name__ == "__main__":
    unittest.main()
