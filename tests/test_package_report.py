import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "scripts" / "report-packages.py"
spec = importlib.util.spec_from_file_location("package_report", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class PackageReportTests(unittest.TestCase):
    def test_selected_packages_only(self):
        config = "CONFIG_PACKAGE_dropbear=y\n# CONFIG_PACKAGE_luci is not set\nCONFIG_PACKAGE_dnsmasq=m\n"
        self.assertEqual(module.packages(config), ["dropbear"])

    def test_comparison(self):
        baseline = "CONFIG_PACKAGE_dropbear=y\nCONFIG_PACKAGE_luci=y\n"
        current = "CONFIG_PACKAGE_dropbear=y\nCONFIG_PACKAGE_apk=y\n"
        result = module.report(current, baseline)
        self.assertEqual(result["added"], ["apk"])
        self.assertEqual(result["removed"], ["luci"])

    def test_deduplicates(self):
        self.assertEqual(module.packages("CONFIG_PACKAGE_apk=y\nCONFIG_PACKAGE_apk=y\n"), ["apk"])
