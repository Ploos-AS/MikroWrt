import unittest
import importlib.util
import tempfile
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
