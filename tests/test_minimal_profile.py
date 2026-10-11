import unittest
import importlib.util
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "scripts" / "apply-minimal-profile.py"
spec = importlib.util.spec_from_file_location("minimal", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class MinimalProfileTests(unittest.TestCase):
    def test_preserves_essential_networking(self):
        source = "CONFIG_PACKAGE_dnsmasq=y\nCONFIG_PACKAGE_dropbear=y\nCONFIG_PACKAGE_luci=y\n"
        result = module.transform(source)
        self.assertIn("CONFIG_PACKAGE_dnsmasq=y", result)
        self.assertIn("CONFIG_PACKAGE_dropbear=y", result)
        self.assertIn("# CONFIG_PACKAGE_luci is not set", result)
        self.assertNotIn("CONFIG_PACKAGE_luci=y", result)

    def test_idempotent(self):
        source = "CONFIG_PACKAGE_luci=y\nCONFIG_PACKAGE_dnsmasq=y\n"
        self.assertEqual(module.transform(module.transform(source)), module.transform(source))
