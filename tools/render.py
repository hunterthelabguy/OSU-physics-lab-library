"""Render a converted Markdown file to HTML in one or both themes.

Usage: python tools/render.py FILE.md [FILE.md ...] [--theme faithful|modern]
       [--out DIR]

Both themes render the same Markdown source (ledger 28): one keeps the
original page settings, the other drops them and follows
docs/presentation-evidence.md. Output goes to build/<theme>/<id>.html by
default, with the theme embedded so the file stands alone; build/ is not
committed.

Requires Pandoc on PATH or in the PANDOC environment variable.
"""

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PANDOC = os.environ.get("PANDOC", "pandoc")
THEMES = ("faithful", "modern")


def render(md_path, theme, out_dir):
    name = os.path.splitext(os.path.basename(md_path))[0]
    out = os.path.join(out_dir, theme, name + ".html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    # Absolute, so --embed-resources finds it wherever the output lands.
    css = os.path.join(ROOT, "themes", theme + ".css").replace(os.sep, "/")
    subprocess.run([
        PANDOC, md_path,
        "-f", "markdown-smart",
        "-t", "html5",
        "--standalone",
        # Embed the theme so a downloaded page works on its own.
        "--embed-resources",
        "--template", os.path.join(ROOT, "tools", "template.html"),
        "--lua-filter", os.path.join(ROOT, "tools", "filters", "questions.lua"),
        "-M", "theme=" + theme,
        "-M", "css=" + css,
        "-o", out,
    ], check=True)
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--theme", choices=THEMES)
    ap.add_argument("--out", default=os.path.join(ROOT, "build"))
    args = ap.parse_args(argv)
    themes = (args.theme,) if args.theme else THEMES
    for md in args.files:
        for theme in themes:
            print("wrote", os.path.relpath(render(md, theme, args.out), ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
