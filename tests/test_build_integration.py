import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build-firmware.sh"

class BuildIntegrationTests(unittest.TestCase):
    def test_unusable_config_fails_before_download(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            tree = root / "openwrt"
            tree.mkdir()
            (tree / ".config").write_text("CONFIG_TARGET_ramips_mt76x8_DEVICE_glinet_gl-mt300n-v2=y\n")
            (tree / "Makefile").write_text(
                "defconfig:\n\t@true\n"
                "download:\n\t@touch DOWNLOAD_WAS_RUN\n"
                "all:\n\t@touch BUILD_WAS_RUN\n"
            )
            env = {**os.environ, "OPENWRT_DIR": str(tree)}
            # Git revision command is diagnostic only; git absence is not fatal here.
            result = subprocess.run(["sh", str(SCRIPT)], cwd=Path(__file__).resolve().parents[1],
                                    env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((tree / "DOWNLOAD_WAS_RUN").exists())
            self.assertFalse((tree / "BUILD_WAS_RUN").exists())
