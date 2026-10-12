import unittest
import importlib.util
import tempfile
import subprocess
import sys
from pathlib import Path
path = Path(__file__).resolve().parents[1] / "scripts" / "report-images.py"
spec = importlib.util.spec_from_file_location("report_images", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ReportImagesTests(unittest.TestCase):
    def test_budget_and_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "firmware.bin").write_bytes(b"abc")
            (root / "notes.txt").write_text("ignore")
            data = module.report(root, 2)
            self.assertEqual(len(data["images"]), 1)
            self.assertEqual(data["images"][0]["bytes"], 3)
            self.assertFalse(data["images"][0]["within_budget"])
            self.assertEqual(len(data["images"][0]["sha256"]), 64)

    def test_no_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "image.img").write_bytes(b"x")
            self.assertIsNone(module.report(root, None)["images"][0]["within_budget"])

    def test_empty_directory_has_no_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(module.report(Path(tmp), None)["images"], [])

    def test_streamed_digest_matches_known_sha256(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "image.trx").write_bytes(b"abc")
            self.assertEqual(
                module.report(root, None)["images"][0]["sha256"],
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )

    def test_require_name_rejects_wrong_device(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "other-router-sysupgrade.bin").write_bytes(b"test")
            output = root / "report.json"
            result = subprocess.run(
                [sys.executable, str(path), str(root),
                 "--require-images", "--require-name", "gl-mt300n-v2",
                 "--output", str(output)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("No firmware image filename matches", result.stderr)

    def test_require_name_accepts_mango(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "openwrt-glinet_gl-mt300n-v2-sysupgrade.bin").write_bytes(b"test")
            result = subprocess.run(
                [sys.executable, str(path), str(root),
                 "--require-images", "--require-name", "gl-mt300n-v2",
                 "--output", str(root / "report.json")],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
