#!/usr/bin/env python3
"""Validate candidate package configuration against basic usability policies.

This is a static preflight, not proof of working network access or recovery.
"""
import argparse
import json
from pathlib import Path

MANAGEMENT = ("dropbear", "openssh-server", "luci", "luci-base")
NETWORK = ("dnsmasq", "dnsmasq-full", "odhcpd", "odhcpd-ipv6only")

def enabled(config: str, package: str) -> bool:
    return f"CONFIG_PACKAGE_{package}=y" in config.splitlines()

def inspect(config: str, *, require_ssh=False):
    errors = []
    warnings = []
    if not any(enabled(config, x) for x in MANAGEMENT):
        errors.append("No recognized management package selected; confirm another tested management path.")
    if require_ssh and not any(enabled(config, x) for x in ("dropbear", "openssh-server")):
        errors.append("SSH management required but no recognized SSH server selected.")
    if not any(enabled(config, x) for x in NETWORK):
        warnings.append("No recognized DHCP service selected; this may be intentional for a bridge or static network.")
    if not any(enabled(config, x) for x in ("opkg", "apk")):
        warnings.append("No package manager selected; runtime package installation may not be available.")
    return {"errors": errors, "warnings": warnings}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("config", type=Path)
    p.add_argument("--require-ssh", action="store_true")
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    if not args.config.is_file():
        p.error("Config file not found")
    result = inspect(args.config.read_text(), require_ssh=args.require_ssh)
    data = json.dumps(result, indent=2)
    print(data)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data + "\n")
    raise SystemExit(1 if result["errors"] else 0)

if __name__ == "__main__":
    main()
