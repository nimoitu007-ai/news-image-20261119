"""World news of Thursday 19 November 2026, in one image.

Entry for make.fun bounty "news-image-20261119".
Newspaper front page: 50 short stories from six continents,
date prominent in the masthead. Deterministic, offline, standard
library only: it copies the pre-built summary image in this
repository to /output/entry.png. Running it twice writes the same
bytes both times.
"""

import hashlib
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "news-2026-11-19.png"
OUTPUT = Path("/output/entry.png")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
