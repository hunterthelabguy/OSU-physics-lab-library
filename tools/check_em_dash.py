"""No em dash (U+2014) in what publishes to students and the public.

Usage: python tools/check_em_dash.py

Scans only the published sources (2026-10-03 ruling): the files that
_quarto.yml, tools/quarto_build.py and tools/render.py turn into pages.
Internal docs are not scanned. A converted file, whose front matter names a
`source_file`, is skipped unless its status is `ruled-change`: it keeps every
em dash its original holds, and the word check proves its words are the
original's (D-0103). A `ruled-change` file is the site's own wording and is
scanned (D-0195). Binary files are skipped. Exit code 1 and the files listed
when any other file has one.
"""

import os
import sys

from check_unchanged import rebaselined  # D-0195

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLISHED = (
    "curriculum", "site", "sims", "themes", "VISION.md", "title-block.html",
    "tools/template.html", "tools/template-site.html", "tools/brandheader.html",
    "tools/brandfooter.html", "tools/render.py", "tools/quarto_chrome.py",
    "tools/downloads.py", "tools/filters",
)
EM_DASH = "\u2014".encode("utf-8")


def converted(path):
    """True when the file opens with front matter that names a source_file."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")
    if lines[0].rstrip("\r") != "---":
        return False
    for line in lines[1:]:
        if line.rstrip("\r") == "---":
            return False
        if line.startswith("source_file:"):
            return True
    return False


def files(root, paths):
    for p in paths:
        full = os.path.join(root, p)
        if os.path.isfile(full):
            yield full
        for dirpath, _, names in os.walk(full):
            for name in sorted(names):
                yield os.path.join(dirpath, name)


def scan(root=ROOT, paths=PUBLISHED):
    found = []
    for path in files(root, paths):
        with open(path, "rb") as fh:
            data = fh.read()
        if b"\0" in data or EM_DASH not in data:
            continue
        if path.endswith(".md") and converted(path) and not rebaselined(path):
            continue
        found.append(os.path.relpath(path, root).replace(os.sep, "/"))
    return found


def main():
    found = scan()
    for path in found:
        print(path)
    if found:
        print("em dash found in the files above")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
