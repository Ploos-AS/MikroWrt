import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build-firmware.sh"

class BuildArtifactGateTests(unittest.TestCase):
    def test_build_with_no_images_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            tree = base / "openwrt"
            tree.mkdir()
            (tree / ".config").write_text(
                "CONFIG_TARGET_ramips_mt76x8_DEVICE_glinet_gl-mt300n-v2=y\n"
                "CONFIG_PACKAGE_dropbear=y\n"
                "CONFIG_PACKAGE_dnsmasq=y\n"
            )
            (tree / "Makefile").write_text(
                "defconfig:\n\t@true\n"
                "download:\n\t@true\n"
                "all:\n\t@true\n"
            )
            env = {**os.environ, "OPENWRT_DIR": str(tree), "BUILD_JOBS": "1"}
            result = subprocess.run(
                ["sh", str(SCRIPT)], cwd=ROOT, env=env,
                capture_output=True, text=True
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Image directory does not exist", result.stderr)

    def test_shell_syntax(self):
        result = subprocess.run(["sh", "-n", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
