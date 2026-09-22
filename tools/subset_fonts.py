"""Subset Open Sans to Latin and Greek as WOFF2 (DECISIONS D-0025, D-0027).

One-time tool, run by hand; CI imports only UNICODES and covers().
Needs fontTools and brotli: python -m pip install --user fonttools brotli

Usage: python tools/subset_fonts.py SRC_DIR
SRC_DIR holds OpenSans-{Regular,Bold,Italic,BoldItalic}.ttf from
github.com/googlefonts/opensans (fonts/ttf/). Output: site/fonts/*.woff2.
"""

import os
import subprocess
import sys

STYLES = ("Regular", "Bold", "Italic", "BoldItalic")

# Latin: Basic Latin and Latin-1 (includes the degree, plus-minus, micro and
# multiplication signs), the OE ligatures, spacing modifiers for quotes,
# General Punctuation (dashes, quotes, primes, bullets), the euro and trade
# marks, arrows used as hint glyphs, and the true minus sign. Greek: the
# Greek and Coptic block, for symbols in physics text.
UNICODES = [
    (0x0000, 0x00FF), (0x0131, 0x0131), (0x0152, 0x0153),
    (0x02BB, 0x02BC), (0x02C6, 0x02C6), (0x02DA, 0x02DA), (0x02DC, 0x02DC),
    (0x2000, 0x206F), (0x20AC, 0x20AC), (0x2122, 0x2122),
    (0x2190, 0x2193), (0x2212, 0x2212), (0x2215, 0x2215),
    (0xFEFF, 0xFEFF), (0xFFFD, 0xFFFD),
    (0x0370, 0x03FF),
]


def covers(ch):
    cp = ord(ch)
    return any(a <= cp <= b for a, b in UNICODES)


def unicodes_arg():
    return ",".join(f"U+{a:04X}-{b:04X}" if a != b else f"U+{a:04X}" for a, b in UNICODES)


def main(src):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "site", "fonts")
    os.makedirs(out, exist_ok=True)
    for style in STYLES:
        subprocess.run([
            sys.executable, "-m", "fontTools.subset",
            os.path.join(src, f"OpenSans-{style}.ttf"),
            "--unicodes=" + unicodes_arg(),
            "--layout-features=*",
            "--flavor=woff2",
            "--output-file=" + os.path.join(out, f"OpenSans-{style}.woff2"),
        ], check=True)
        print(style, os.path.getsize(os.path.join(out, f"OpenSans-{style}.woff2")), "bytes")


if __name__ == "__main__":
    main(sys.argv[1])
