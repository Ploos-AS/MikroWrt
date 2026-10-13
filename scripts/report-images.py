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
        image_kind = ("sysupgrade" if "sysupgrade" in path.name else
                      "factory" if "factory" in path.name else "unknown")
        records.append({
            "image_kind": image_kind,
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
    p.add_argument("--reserve-bytes", type=int, default=0)
    p.add_argument("--require-images", action="store_true", help="Fail if no firmware images were found")
    p.add_argument("--require-name", help="Require at least one image filename containing this text")
    p.add_argument("--require-kind", choices=("factory", "sysupgrade"), help="Require matching filename-indicated image kind")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if not args.directory.is_dir():
        p.error("Image directory does not exist")
    if args.budget_bytes is not None and args.budget_bytes <= 0:
        p.error("Budget must be positive")
    if args.reserve_bytes < 0:
        p.error("Reserve must be nonnegative")
    if args.reserve_bytes and args.budget_bytes is None:
        p.error("--reserve-bytes requires --budget-bytes")
    if args.budget_bytes is not None and args.reserve_bytes >= args.budget_bytes:
        p.error("Reserve must be smaller than budget")
    data = report(args.directory, args.budget_bytes)
    data["required_reserve_bytes"] = args.reserve_bytes
    for item in data["images"]:
        item["meets_reserve"] = (item["budget_margin_bytes"] >= args.reserve_bytes
                                 if args.budget_bytes is not None else None)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Recorded {len(data['images'])} candidate images in {args.output}")
    if args.require_images and not data["images"]:
        p.exit(1, "No firmware images found; refusing to mark build successful.\n")
    matching = [item for item in data["images"]
                if (not args.require_name or args.require_name in Path(item["path"]).name)
                and (not args.require_kind or item["image_kind"] == args.require_kind)]
    if (args.require_name or args.require_kind) and not matching:
        p.exit(1, "No firmware image matches required device name and image kind.\n")

if __name__ == "__main__":
    main()
