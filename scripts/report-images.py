#!/usr/bin/env python3
"""Create deterministic metadata for candidate firmware images; no flashing."""
import argparse
import hashlib
import json
from pathlib import Path

def report(folder: Path, limit: int | None):
    records = []
    for path in sorted(folder.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".bin", ".img", ".trx", ".itb"}:
            continue
        size = path.stat().st_size
        digest_obj = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest_obj.update(chunk)
        digest = digest_obj.hexdigest()
        records.append({
            "path": str(path.relative_to(folder)),
            "bytes": size,
            "sha256": digest,
            "budget_bytes": limit,
            "budget_margin_bytes": limit - size if limit is not None else None,
            "within_budget": size <= limit if limit is not None else None,
        })
    return {"qualification": "UNTESTED — DO NOT FLASH", "images": records}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("directory", type=Path)
    p.add_argument("--budget-bytes", type=int)
    p.add_argument("--require-images", action="store_true", help="Fail if no firmware images were found")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if not args.directory.is_dir():
        p.error("Image directory does not exist")
    if args.budget_bytes is not None and args.budget_bytes <= 0:
        p.error("Budget must be positive")
    data = report(args.directory, args.budget_bytes)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Recorded {len(data['images'])} candidate images in {args.output}")
    if args.require_images and not data["images"]:
        p.exit(1, "No firmware images found; refusing to mark build successful.\n")

if __name__ == "__main__":
    main()
