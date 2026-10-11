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

    def test_preserves_opkg_by_default(self):
        source = "CONFIG_PACKAGE_opkg=y\nCONFIG_PACKAGE_luci=y\n"
        self.assertIn("CONFIG_PACKAGE_opkg=y", module.transform(source))

    def test_preserves_apk_by_default(self):
        source = "CONFIG_PACKAGE_apk=y\nCONFIG_PACKAGE_luci=y\n"
        self.assertIn("CONFIG_PACKAGE_apk=y", module.transform(source))

    def test_can_disable_managers(self):
        source = "CONFIG_PACKAGE_opkg=y\nCONFIG_PACKAGE_apk=y\n"
        result = module.transform(source, "none")
        self.assertIn("# CONFIG_PACKAGE_opkg is not set", result)
        self.assertIn("# CONFIG_PACKAGE_apk is not set", result)

    def test_can_select_manager(self):
        result = module.transform("CONFIG_PACKAGE_opkg=y\n", "apk")
        self.assertIn("CONFIG_PACKAGE_apk=y", result)
        self.assertIn("# CONFIG_PACKAGE_opkg is not set", result)

    def test_idempotent(self):
        source = "CONFIG_PACKAGE_luci=y\nCONFIG_PACKAGE_dnsmasq=y\nCONFIG_PACKAGE_opkg=y\n"
        for manager in ("keep", "none", "opkg", "apk"):
            self.assertEqual(module.transform(module.transform(source, manager), manager),
                             module.transform(source, manager))
