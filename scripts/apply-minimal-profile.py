#!/usr/bin/env python3
"""Apply a conservative, reversible package-reduction overlay to an OpenWrt .config.

Does not remove core networking packages or assert that an image is flash-safe.
"""
import argparse
from pathlib import Path

DISABLE = (
    "CONFIG_PACKAGE_luci",
    "CONFIG_PACKAGE_luci-base",
    "CONFIG_PACKAGE_luci-ssl",
    "CONFIG_PACKAGE_luci-light",
    "CONFIG_PACKAGE_ppp",
    "CONFIG_PACKAGE_ppp-mod-pppoe",
    "CONFIG_PACKAGE_kmod-ppp",
    "CONFIG_PACKAGE_kmod-pppoe",
    "CONFIG_PACKAGE_opkg",
)
# No package is disabled without an explicit entry above.
def transform(data: str) -> str:
    lines = data.splitlines()
    result = []
    for line in lines:
        if any(line.startswith(key + "=") or line == "# " + key + " is not set" for key in DISABLE):
            continue
        result.append(line)
    result.extend("# " + key + " is not set" for key in DISABLE)
    return "\n".join(result) + "\n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.config.resolve() == args.output.resolve():
        parser.error("Output must differ from input (preserve original config)")
    if not args.config.is_file():
        parser.error("Config file not found")
    args.output.write_text(transform(args.config.read_text()))
    print(f"Candidate minimal overlay written to {args.output}; inspect and run make defconfig.")

if __name__ == "__main__":
    main()
