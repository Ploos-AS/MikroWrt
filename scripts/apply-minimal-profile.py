#!/usr/bin/env python3
"""Apply optional reductions without crippling baseline router functionality."""
import argparse
from pathlib import Path

OPTIONAL = (
    "CONFIG_PACKAGE_luci", "CONFIG_PACKAGE_luci-base",
    "CONFIG_PACKAGE_luci-ssl", "CONFIG_PACKAGE_luci-light",
    "CONFIG_PACKAGE_ppp", "CONFIG_PACKAGE_ppp-mod-pppoe",
    "CONFIG_PACKAGE_kmod-ppp", "CONFIG_PACKAGE_kmod-pppoe",
)
MANAGERS = ("CONFIG_PACKAGE_opkg", "CONFIG_PACKAGE_apk")

def transform(data: str, package_manager: str = "keep") -> str:
    if package_manager not in ("keep", "none", "opkg", "apk"):
        raise ValueError("Invalid package manager option")
    keys = list(OPTIONAL)
    if package_manager != "keep":
        keys.extend(MANAGERS)
    lines = [
        line for line in data.splitlines()
        if not any(line.startswith(key + "=") or line == "# " + key + " is not set" for key in keys)
    ]
    lines.extend("# " + key + " is not set" for key in OPTIONAL)
    if package_manager == "none":
        lines.extend("# " + key + " is not set" for key in MANAGERS)
    elif package_manager in ("opkg", "apk"):
        selected = "CONFIG_PACKAGE_" + package_manager
        lines.extend(key + "=y" if key == selected else "# " + key + " is not set" for key in MANAGERS)
    return "\n".join(lines) + "\n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--package-manager", choices=("keep", "none", "opkg", "apk"),
                        default="keep", help="keep upstream selection (default), disable, or request one manager")
    args = parser.parse_args()
    if args.config.resolve() == args.output.resolve():
        parser.error("Output must differ from input (preserve original config)")
    if not args.config.is_file():
        parser.error("Config file not found")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(transform(args.config.read_text(), args.package_manager))
    print("Wrote candidate overlay. Run make defconfig and verify selected package availability.")

if __name__ == "__main__":
    main()
