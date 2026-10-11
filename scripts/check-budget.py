#!/usr/bin/env python3
"""Check firmware file against an explicit image budget.

This does not establish that a firmware image is flash-safe.
"""
import argparse
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("image", type=Path)
    p.add_argument("--max-bytes", type=int, required=True,
                   help="Actual firmware partition budget, not nominal flash size")
    args = p.parse_args()
    if args.max_bytes <= 0:
        p.error("--max-bytes must be positive")
    size = args.image.stat().st_size
    margin = args.max_bytes - size
    print(f"image={args.image} bytes={size} budget={args.max_bytes} margin={margin}")
    raise SystemExit(0 if margin >= 0 else 1)

if __name__ == "__main__":
    main()
