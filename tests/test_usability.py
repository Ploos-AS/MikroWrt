import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "scripts" / "check-usability.py"
spec = importlib.util.spec_from_file_location("usability", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class UsabilityTests(unittest.TestCase):
    def test_ssh_and_dns(self):
        data = "CONFIG_PACKAGE_dropbear=y\nCONFIG_PACKAGE_dnsmasq=y\nCONFIG_PACKAGE_apk=y\n"
        self.assertEqual(module.inspect(data)["errors"], [])
        self.assertEqual(module.inspect(data)["warnings"], [])

    def test_missing_management_is_error(self):
        self.assertTrue(module.inspect("CONFIG_PACKAGE_dnsmasq=y\n")["errors"])

    def test_no_manager_is_warning_not_error(self):
        result = module.inspect("CONFIG_PACKAGE_dropbear=y\nCONFIG_PACKAGE_dnsmasq=y\n")
        self.assertEqual(result["errors"], [])
        self.assertTrue(any("package manager" in w for w in result["warnings"]))

    def test_require_ssh(self):
        result = module.inspect("CONFIG_PACKAGE_luci=y\n", require_ssh=True)
        self.assertTrue(any("SSH" in e for e in result["errors"]))

    def test_dhcp_optional(self):
        result = module.inspect("CONFIG_PACKAGE_dropbear=y\n")
        self.assertEqual(result["errors"], [])
        self.assertTrue(any("DHCP" in w for w in result["warnings"]))
