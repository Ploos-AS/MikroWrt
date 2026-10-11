#!/usr/bin/env python3
"""Apply explicit package choices; preserve upstream configuration by default."""
import argparse
from pathlib import Path

GROUPS = {
    "web": ("luci", "luci-base", "luci-ssl", "luci-light"),
    "ppp": ("ppp", "ppp-mod-pppoe", "kmod-ppp", "kmod-pppoe"),
    "ssh": ("dropbear",),
    "dns": ("dnsmasq",),
}
MANAGERS = ("opkg", "apk")

def transform(data: str, package_manager: str = "keep", disable_groups=(), enable_groups=()) -> str:
    if package_manager not in ("keep", "none", "opkg", "apk"):
        raise ValueError("Invalid package manager option")
    disable_groups, enable_groups = set(disable_groups), set(enable_groups)
    unknown = (disable_groups | enable_groups) - GROUPS.keys()
    if unknown or disable_groups & enable_groups:
        raise ValueError("Unknown or conflicting feature group")
    decisions = {}
    for group in disable_groups:
        decisions.update({f"CONFIG_PACKAGE_{pkg}": False for pkg in GROUPS[group]})
    for group in enable_groups:
        decisions.update({f"CONFIG_PACKAGE_{pkg}": True for pkg in GROUPS[group]})
    if package_manager != "keep":
        decisions.update({f"CONFIG_PACKAGE_{pkg}": package_manager == pkg for pkg in MANAGERS})
    lines = [
        line for line in data.splitlines()
        if not any(line.startswith(key + "=") or line == f"# {key} is not set" for key in decisions)
    ]
    lines.extend(f"{key}=y" if enabled else f"# {key} is not set"
                 for key, enabled in sorted(decisions.items()))
    return "\n".join(lines) + "\n"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("config", type=Path)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--package-manager", choices=("keep", "none", "opkg", "apk"), default="keep")
    p.add_argument("--disable", action="append", choices=sorted(GROUPS), default=[],
                   help="Explicitly disable a feature group (repeatable)")
    p.add_argument("--enable", action="append", choices=sorted(GROUPS), default=[],
                   help="Explicitly enable a feature group (repeatable)")
    args = p.parse_args()
    if args.config.resolve() == args.output.resolve():
        p.error("Output must differ from input")
    if not args.config.is_file():
        p.error("Config file not found")
    try:
        result = transform(args.config.read_text(), args.package_manager, args.disable, args.enable)
    except ValueError as exc:
        p.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result)
    print("Wrote candidate configuration; run make defconfig and inspect resulting packages.")

if __name__ == "__main__":
    main()
