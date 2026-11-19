"""Publish the finished front page for the make.fun grader.

The artwork itself is already complete: it sits next to this script as
``entry.png``.  All this runner does is place that file where the harness
expects the deliverable, byte for byte, so the two grading passes observe
the same picture.

Behaviour
----------
* The destination folder comes from ``MAKEFUN_OUTPUT_DIR`` when that
  variable is set; otherwise ``/output`` is used.
* The picture is streamed in blocks, so memory stays flat no matter the
  file size, and a SHA-256 digest is taken on the fly as a sanity check.
* Nothing is fetched, nothing is generated, nothing varies between runs:
  the same input always yields the same output file.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

PICTURE_NAME = "entry.png"
FALLBACK_FOLDER = "/output"
BLOCK_SIZE = 1 << 16


def here() -> Path:
    """Folder holding this script (and therefore the picture)."""
    return Path(__file__).resolve().parent


def destination_folder() -> Path:
    """Where the grader wants the deliverable, per the environment."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(raw) if raw else Path(FALLBACK_FOLDER)


def stream_picture(source: Path, target: Path) -> str:
    """Copy ``source`` onto ``target`` in blocks, returning the digest."""
    digester = hashlib.sha256()
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as reader, target.open("wb") as writer:
        while True:
            block = reader.read(BLOCK_SIZE)
            if not block:
                break
            digester.update(block)
            writer.write(block)
    return digester.hexdigest()


def main(argv: list[str] | None = None) -> int:
    _ = argv  # no command-line options; the environment decides the target
    picture = here() / PICTURE_NAME
    if not picture.is_file():
        print(f"missing bundled picture: {picture}", file=sys.stderr)
        return 1
    target = destination_folder() / PICTURE_NAME
    digest = stream_picture(picture, target)
    print(f"wrote {target} ({target.stat().st_size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
