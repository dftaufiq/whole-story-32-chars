#!/usr/bin/env python3
"""Tell a Whole Story in 32 Characters — make.fun entry.

Writes a single Wi-Fi network name, at most 32 characters, that lands a
joke and implies a whole story in the few words a passer-by sees in a
phone's network list.

The chosen name: "Grandma Joined TikTok, Pray 4 Us" — exactly 32
characters. Two beats with the reveal in the last clause: setup (Grandma
joined TikTok) + punchline (Pray 4 Us). Character (Grandma), situation
(she is on TikTok now), event (she joined), reaction (the family is
praying) — the reader fills in her videos and the family group chat.
Fresh angle: zero TikTok entries among the 120 public titles at build
time, and the only grandma entry in the field is a sad one with no joke.

Deterministic: the same name every run.
"""

import os
import sys


def validate_name(name: str) -> None:
    """Gate: the entry must be 1-32 characters of non-blank text, one line.

    Fails loudly (non-zero exit) so a bad name never ships silently.
    The sealed scorer checks /output/entry.txt is 1-32 characters, so
    the file is written with no trailing newline: exactly the name.
    """
    if not name or not name.strip():
        print("ERROR: entry name is empty or whitespace-only", file=sys.stderr)
        sys.exit(1)
    if "\n" in name or "\r" in name:
        print("ERROR: entry must be a single line", file=sys.stderr)
        sys.exit(1)
    if len(name) > 32:
        print(f"ERROR: entry is {len(name)} chars, over the 32-char limit",
              file=sys.stderr)
        sys.exit(1)


NAME = "Grandma Joined TikTok, Pray 4 Us"


def main() -> None:
    validate_name(NAME)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(NAME)
    # Read back what was written: a partial or mangled write must fail
    # loudly here, never ship silently to the sealed scorer.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != NAME:
        print(f"ERROR: entry.txt holds {written!r}, expected {NAME!r}",
              file=sys.stderr)
        sys.exit(1)
    print(NAME)


if __name__ == "__main__":
    main()
