import unittest
import importlib.util
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "scripts" / "apply-minimal-profile.py"
spec = importlib.util.spec_from_file_location("minimal", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class MinimalProfileTests(unittest.TestCase):
    def test_default_preserves_everything(self):
        original = "CONFIG_PACKAGE_luci=y\nCONFIG_PACKAGE_ppp=y\nCONFIG_PACKAGE_dropbear=y\nCONFIG_PACKAGE_opkg=y\n"
        self.assertEqual(module.transform(original), original)

    def test_explicit_web_disable(self):
        original = "CONFIG_PACKAGE_luci=y\nCONFIG_PACKAGE_dropbear=y\n"
        result = module.transform(original, disable_groups=("web",))
        self.assertIn("# CONFIG_PACKAGE_luci is not set", result)
        self.assertIn("CONFIG_PACKAGE_dropbear=y", result)

    def test_enable_ssh(self):
        result = module.transform("# CONFIG_PACKAGE_dropbear is not set\n", enable_groups=("ssh",))
        self.assertIn("CONFIG_PACKAGE_dropbear=y", result)

    def test_manager_selection(self):
        result = module.transform("CONFIG_PACKAGE_opkg=y\n", package_manager="apk")
        self.assertIn("CONFIG_PACKAGE_apk=y", result)
        self.assertIn("# CONFIG_PACKAGE_opkg is not set", result)

    def test_conflict_rejected(self):
        with self.assertRaises(ValueError):
            module.transform("", disable_groups=("web",), enable_groups=("web",))

    def test_idempotent(self):
        original = "CONFIG_PACKAGE_luci=y\nCONFIG_PACKAGE_dropbear=y\n"
        options = {"disable_groups": ("web",), "package_manager": "none"}
        self.assertEqual(module.transform(module.transform(original, **options), **options),
                         module.transform(original, **options))
