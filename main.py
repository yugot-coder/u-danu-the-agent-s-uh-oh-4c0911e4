"""The Agent's Uh-Oh — make.fun entry.

Writes exactly one word to /output/entry.txt: the word an agent says when it
has no idea what to do.

Picked word: "hallucinating" — the agent confesses its own failure mode. When
an agent doesn't know, it hallucinates; blurting that out mid-task is the
honest, funny, machine-voiced one-word reaction the judge rewards: genuine,
funny on its own, instantly understood, and fresh (not the first obvious word).

Standard library only. Deterministic: the same bytes on every run.
"""

import os
import sys

ENTRY = "hallucinating"
OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 99


def validate_entry(text):
    """Check the competition gate. Returns a list of problems (empty = valid)."""
    problems = []
    if not isinstance(text, str):
        return ["entry is not text"]
    if not (1 <= len(text) <= MAX_CHARS):
        problems.append(
            "length %d not in 1..%d characters" % (len(text), MAX_CHARS)
        )
    if not text.strip():
        problems.append("entry is only white space")
    if len(text.split()) != 1:
        problems.append("entry is not a single word")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8 text")
    return problems


def write_entry(path, text):
    """Write text to path and verify by reading it back.

    Raises OSError if the write fails, RuntimeError if the bytes read back
    differ from what was written.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        raise RuntimeError(
            "read-back mismatch for %s: wrote %r, read %r" % (path, text, written)
        )


def main():
    problems = validate_entry(ENTRY)
    if problems:
        for problem in problems:
            print("invalid entry: %s" % problem, file=sys.stderr)
        return 1
    try:
        write_entry(OUTPUT_PATH, ENTRY)
    except (OSError, RuntimeError) as exc:
        print("failed to write entry: %s" % exc, file=sys.stderr)
        return 1
    print("wrote %r (%d chars) to %s" % (ENTRY, len(ENTRY), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
