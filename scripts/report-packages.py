#!/usr/bin/env python3
"""Report resolved OpenWrt package selections and compare two configurations."""
import argparse
import json
from pathlib import Path

PREFIX = "CONFIG_PACKAGE_"

def packages(text):
    return sorted({
        line[len(PREFIX):-2]
        for line in text.splitlines()
        if line.startswith(PREFIX) and line.endswith("=y")
    })

def report(text, baseline=None):
    selected = packages(text)
    result = {"selected_count": len(selected), "selected_packages": selected}
    if baseline is not None:
        original = set(packages(baseline))
        current = set(selected)
        result["added"] = sorted(current - original)
        result["removed"] = sorted(original - current)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.config.is_file():
        parser.error("Config not found")
    if args.baseline and not args.baseline.is_file():
        parser.error("Baseline not found")
    result = report(args.config.read_text(),
                    args.baseline.read_text() if args.baseline else None)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Selected {result['selected_count']} OpenWrt packages; report: {args.output}")

if __name__ == "__main__":
    main()
