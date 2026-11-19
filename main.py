#!/usr/bin/env python3
"""World news of Thursday 19 November 2026, in one image.

Entry for the make.fun bounty "news-image-20261119": a newspaper
front page holding 50 short stories from six continents, with the
date set large under the masthead.

This program is the entrypoint. It is standard library only, uses no
network, and simply places the pre-built summary image into the
location the grader reads: /output/entry.png. Run it twice and the
two outputs are byte-identical.
"""

import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "news-2026-11-19.png")
TARGET = "/output/entry.png"


def run():
    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    blob = open(TARGET, "rb").read()
    print("wrote %s (%d bytes)" % (TARGET, len(blob)))
    print("sha256 %s" % hashlib.sha256(blob).hexdigest())


if __name__ == "__main__":
    run()
