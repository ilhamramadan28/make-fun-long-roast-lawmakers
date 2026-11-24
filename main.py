#!/usr/bin/env python3
"""The Long Roast: Lawmakers and the File They Cannot Convert - write entry.txt to /output/entry.txt."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.txt")
OUT = "/output/entry.txt"


def main() -> int:
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()
    # Guard: the gate is 1-320 chars of UTF-8, not only whitespace, one sentence.
    # Length is measured on the stripped entry, not the raw file bytes, so a
    # trailing newline in entry.txt never counts against the 320-char gate.
    stripped = text.strip()
    if not 1 <= len(stripped) <= 320 or not stripped or "\n" in stripped:
        print("entry fails gate: must be 1-320 chars, not only whitespace, one line",
              file=sys.stderr)
        return 1
    if stripped.count(".") != 1 or not stripped.endswith("."):
        print("entry fails gate: must be exactly one sentence", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copyfile(SRC, OUT)
    os.chmod(OUT, 0o644)
    with open(SRC, "rb") as a, open(OUT, "rb") as b:
        if a.read() != b.read():
            print("byte-verify failed", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
