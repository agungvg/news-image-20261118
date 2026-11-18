#!/usr/bin/env python3
"""news-image-20261118 entry: sum up Wednesday 18 November 2026's world news
in one image.

The image (entry.png, 1024x1024, PNG) is a newspaper front page drawn by
draw.py in this repository: five of the day's biggest stories, each with its
own drawn illustration, a headline and a short summary, plus an ALSO strip
with three more stories. The program just copies that image to the grader's
output path. It is fully deterministic: the same bytes go out on every run,
with no network, no clock and no randomness.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # The gate reads exactly these bytes; a short copy would fail it.
    assert os.path.getsize(dst) == os.path.getsize(src)


if __name__ == "__main__":
    main()
