#!/usr/bin/env python3
"""Check firmware size against an explicitly verified firmware-partition budget.

A size pass alone never establishes that firmware is flash-safe.
"""
import argparse
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("image", type=Path)
    p.add_argument("--max-bytes", type=int, required=True,
                   help="Actual firmware partition budget, not nominal flash size")
    p.add_argument("--reserve-bytes", type=int, default=0,
                   help="Optional required free margin inside the firmware partition")
    args = p.parse_args()
    if args.max_bytes <= 0:
        p.error("--max-bytes must be positive")
    if args.reserve_bytes < 0:
        p.error("--reserve-bytes must be nonnegative")
    if args.reserve_bytes >= args.max_bytes:
        p.error("--reserve-bytes must be smaller than --max-bytes")
    size = args.image.stat().st_size
    margin = args.max_bytes - size
    print(f"image={args.image} bytes={size} budget={args.max_bytes} "
          f"margin={margin} reserve={args.reserve_bytes}")
    raise SystemExit(0 if margin >= args.reserve_bytes else 1)


if __name__ == "__main__":
    main()
