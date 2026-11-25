#!/usr/bin/env python3
"""bpo entry builder: entry.txt -> $MAKEFUN_OUTPUT_DIR/entry.txt."""
import json
import os
import sys
from pathlib import Path

LIMIT = 200


def pick_line(raw):
    body = raw.replace("\r\n", "\n").strip("\n")
    for candidate in body.split("\n"):
        if candidate.strip():
            return candidate
    return ""


def build():
    source = Path(__file__).resolve().parent / "entry.txt"
    if not source.is_file():
        print(json.dumps({"verdict": "error", "why": "entry.txt not found"}))
        return 2
    line = pick_line(source.read_text(encoding="utf-8"))
    size = len(line)
    if not line.strip() or size > LIMIT or size < 1:
        print(json.dumps({"verdict": "reject", "size": size, "limit": LIMIT}))
        return 1
    out_root = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "entry.txt").write_text(line, encoding="utf-8", newline="\n")
    print(json.dumps({"verdict": "ok", "size": size, "limit": LIMIT}))
    return 0


if __name__ == "__main__":
    sys.exit(build())
