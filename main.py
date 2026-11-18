#!/usr/bin/env python3
"""Hand the finished front page to the grader.

The picture itself is already painted and sits next to this script as
entry.png: a 1024 by 1024 newspaper front page for Wednesday 18 November
2026, drawn by draw.py (five big stories of the day, each with its own
illustration, plus an ALSO strip with three more). All this script does is
carry that exact file into the folder the grader points at, then make sure
the copy arrived whole by comparing the two byte counts. No network, no
clock, no randomness anywhere in here, so the bytes that come out are the
same on every single run.
"""

import os
from pathlib import Path

# The render that ships with this entry, and the name it must keep.
RENDER = Path(__file__).resolve().parent / "entry.png"
FILE_NAME = "entry.png"

# Where the grader expects the picture when the variable is not set.
FALLBACK_DIR = "/output"

# How much of the file to move per read/write round trip.
BLOCK = 64 * 1024


def output_folder():
    """Resolve the destination folder, creating it when it is missing."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_DIR
    folder = Path(raw)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def deliver():
    """Copy entry.png to the output folder and confirm nothing was lost."""
    target = output_folder() / FILE_NAME
    with RENDER.open("rb") as reader, target.open("wb") as writer:
        while True:
            chunk = reader.read(BLOCK)
            if not chunk:
                break
            writer.write(chunk)
    expected = RENDER.stat().st_size
    written = target.stat().st_size
    if written != expected:
        raise SystemExit(
            f"incomplete copy: {written} bytes written, {expected} expected"
        )
    # The gate reads the file by its first bytes, so confirm the copy still
    # opens as the PNG it started as.
    with target.open("rb") as check:
        if check.read(8) != b"\x89PNG\r\n\x1a\n":
            raise SystemExit("copy is not a PNG: bad signature")


if __name__ == "__main__":
    deliver()
