#!/usr/bin/env python3
"""Entrypoint for the news-image-20261119 entry.

Copies the bundled front page (entry.png, drawn by build_image.py)
to the grader's output directory. Python 3.13 standard library only:
no network, no randomness, no clock, so both grader runs write
byte-identical output.

The output directory is $MAKEFUN_OUTPUT_DIR when set, else /output.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    print("wrote", target)


if __name__ == "__main__":
    main()
