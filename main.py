#!/usr/bin/env python3
"""news-image-20261118 upgrade entry.

The entry image is a pre-composed 1024x1024 PNG (37 verified stories
from Wednesday 18 November 2026: 3 leads, 10 cards, 24 briefs, with a
world map, numbers bar, region and field bars, and a date-check line).
This script only copies it byte-exact into the harness output directory
(``MAKEFUN_OUTPUT_DIR``, default ``/output``). It never edits the image.

Guards: the source must exist, must be at most 1 MiB (the rules cap),
and the copy is verified by size before the script reports success.
"""
import hashlib
import os
import shutil
import sys

ENTRY = "entry.png"
DEFAULT_OUT = "/output"
SIZE_CAP = 1048576  # rules cap: 1 MiB


def check_source(src):
    if not os.path.isfile(src):
        raise SystemExit(f"missing entry image: {src}")
    size = os.path.getsize(src)
    if size > SIZE_CAP:
        raise SystemExit(
            f"entry image too large: {size} bytes (cap {SIZE_CAP})")
    return size


def check_result(dst, size, digest):
    if not os.path.isfile(dst):
        raise SystemExit(f"output was not written: {dst}")
    if os.path.getsize(dst) != size:
        raise SystemExit("output size differs from source; copy failed")
    with open(dst, "rb") as fh:
        actual = hashlib.sha256(fh.read()).hexdigest()
    if actual != digest:
        raise SystemExit("output hash differs from source; copy failed")


def emit(source_dir, out_dir):
    src = os.path.join(source_dir, ENTRY)
    size = check_source(src)
    with open(src, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, ENTRY)
    shutil.copyfile(src, dst)
    check_result(dst, size, digest)
    return dst, size


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUT)
    dst, size = emit(here, out_dir)
    print(f"wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
