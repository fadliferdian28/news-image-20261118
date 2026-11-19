#!/usr/bin/env python3
"""news-image-20261118 entrypoint.

Copies the finished entry image (entry.png, stored beside this file) to
the output directory the harness asks for: $MAKEFUN_OUTPUT_DIR, or
/output when the variable is unset.

Standard library only. No network, no randomness, no timestamps: every
run writes exactly the same bytes.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def output_dir() -> Path:
    """Where the harness wants the entry: env var first, else /output."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(raw) if raw else Path("/output")


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"error: {source} is missing", file=sys.stderr)
        return 1
    dest = output_dir() / "entry.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    # Verify the copy byte for byte: a partial write must fail loudly
    # rather than hand the judge a corrupt image.
    if sha256_file(source) != sha256_file(dest):
        print(f"error: copy to {dest} does not match {source}",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
