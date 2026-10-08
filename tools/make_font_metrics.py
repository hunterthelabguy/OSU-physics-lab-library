"""Font metrics for the drawn figures' labels (D-0117): tools/font-metrics.json.

One-time tool, run by hand; tools/figures.py reads only the JSON. Standard
library only.

Usage: python tools/make_font_metrics.py LIBERATION_DIR CARLITO_DIR WINDOWS_FONTS_DIR

Word stores no line breaks for a wrapped label, so tools/figures.py breaks
lines by advance widths, places a word too wide for its box at the left
inset as Word does, and places lines by each font's vertical metrics.

- Times New Roman's widths and vertical metrics come from Liberation Serif
  2.1.5 (SIL OFL), metric-compatible with it (D-0117): LIBERATION_DIR is
  the unpacked liberation-fonts-ttf-2.1.5 release
  (github.com/liberationfonts/liberation-fonts, release 2.1.5).
- Calibri's come from Carlito (SIL OFL), metric-compatible with it:
  CARLITO_DIR holds Carlito-{Regular,Bold,Italic,BoldItalic}.ttf from
  github.com/google/fonts, ofl/carlito.
- Cambria Math and Script MT Bold have no free metric-compatible face, so
  their numbers (advance widths, ascent, descent, line gap; no glyphs) are
  read from the Windows font files in WINDOWS_FONTS_DIR.

Checked when made (2026-10-08): Liberation Serif's widths equal Times New
Roman's on 733 of 744 shared characters, the 11 others invisible direction
marks and the sound-recording sign; Carlito's equal Calibri's on 736 of
737, all but the florin.

Each entry records its file's name and SHA-256, so the table can be checked
against the files it came from.
"""

import hashlib
import json
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "font-metrics.json")

# Measured faces: (family, bold, italic) -> Liberation file.
LIBERATION = {
    ("Times New Roman", False, False): "LiberationSerif-Regular.ttf",
    ("Times New Roman", True, False): "LiberationSerif-Bold.ttf",
    ("Times New Roman", False, True): "LiberationSerif-Italic.ttf",
    ("Times New Roman", True, True): "LiberationSerif-BoldItalic.ttf",
}
CARLITO = {
    ("Calibri", False, False): "Carlito-Regular.ttf",
    ("Calibri", True, False): "Carlito-Bold.ttf",
    ("Calibri", False, True): "Carlito-Italic.ttf",
    ("Calibri", True, True): "Carlito-BoldItalic.ttf",
}
# Word's own faces: family -> (Windows file, index in a collection).
WINDOWS = {
    "Cambria Math": ("cambria.ttc", 1),
    "Script MT Bold": ("SCRIPTBL.TTF", 0),
}
# Code points whose widths are kept: Latin, Greek, punctuation, letterlike
# symbols, arrows and mathematical operators.
RANGES = ((0x0020, 0x024F), (0x0370, 0x03FF), (0x2000, 0x206F),
          (0x2100, 0x214F), (0x2190, 0x22FF))


def tables(data, offset=0):
    if data[:4] == b"ttcf":
        offset = struct.unpack(">I", data[12 + 4 * offset:16 + 4 * offset])[0]
    count = struct.unpack(">H", data[offset + 4:offset + 6])[0]
    out = {}
    for i in range(count):
        rec = data[offset + 12 + 16 * i:offset + 28 + 16 * i]
        tag, _, start, length = struct.unpack(">4sIII", rec)
        out[tag.decode("latin-1")] = data[start:start + length]
    return out


def vertical(t):
    units = struct.unpack(">H", t["head"][18:20])[0]
    ascent, descent, gap = struct.unpack(">hhh", t["hhea"][4:10])
    os2 = t["OS/2"]
    win_ascent, win_descent = struct.unpack(">HH", os2[74:78])
    return {"units_per_em": units, "hhea_ascent": ascent, "hhea_descent": -descent,
            "hhea_line_gap": gap, "win_ascent": win_ascent, "win_descent": win_descent}


def cmap(t):
    """Code point -> glyph id, from a format 4 or 12 Unicode subtable."""
    data = t["cmap"]
    n = struct.unpack(">H", data[2:4])[0]
    best = None
    for i in range(n):
        pid, eid, off = struct.unpack(">HHI", data[4 + 8 * i:12 + 8 * i])
        fmt = struct.unpack(">H", data[off:off + 2])[0]
        if (pid, eid) in ((3, 10), (0, 4)) and fmt == 12:
            best = (off, 12)
        elif (pid, eid) in ((3, 1), (0, 3)) and fmt == 4 and best is None:
            best = (off, 4)
    off, fmt = best
    out = {}
    if fmt == 4:
        segs = struct.unpack(">H", data[off + 6:off + 8])[0] // 2
        arr = lambda k: struct.unpack(">%dH" % segs, data[off + 14 + k * 2 * segs + (2 if k else 0):
                                                          off + 14 + (k + 1) * 2 * segs + (2 if k else 0)])
        ends, starts, deltas, ranges = arr(0), arr(1), arr(2), arr(3)
        range_base = off + 16 + 6 * segs
        for s in range(segs):
            for cp in range(starts[s], ends[s] + 1):
                if cp == 0xFFFF:
                    continue
                if ranges[s] == 0:
                    gid = (cp + deltas[s]) & 0xFFFF
                else:
                    at = range_base + 2 * s + ranges[s] + 2 * (cp - starts[s])
                    gid = struct.unpack(">H", data[at:at + 2])[0]
                    gid = (gid + deltas[s]) & 0xFFFF if gid else 0
                if gid:
                    out[cp] = gid
    else:
        groups = struct.unpack(">I", data[off + 12:off + 16])[0]
        for g in range(groups):
            a, b, gid = struct.unpack(">III", data[off + 16 + 12 * g:off + 28 + 12 * g])
            for cp in range(a, b + 1):
                out[cp] = gid + cp - a
    return out


def widths(t):
    n = struct.unpack(">H", t["hhea"][34:36])[0]
    hmtx = t["hmtx"]
    adv = [struct.unpack(">H", hmtx[4 * i:4 * i + 2])[0] for i in range(n)]
    out = {}
    for cp, gid in cmap(t).items():
        if any(a <= cp <= b for a, b in RANGES):
            out[chr(cp)] = adv[min(gid, n - 1)]
    return dict(sorted(out.items()))


def entry(path, index=0):
    data = open(path, "rb").read()
    return data, tables(data, index), {"file": os.path.basename(path),
                                       "sha256": hashlib.sha256(data).hexdigest()}


def main(liberation, carlito, windows):
    faces = {}
    for folder, table in ((liberation, LIBERATION), (carlito, CARLITO)):
        for (family, bold, italic), name in table.items():
            _, t, rec = entry(os.path.join(folder, name))
            rec.update(vertical(t), widths=widths(t))
            faces["{}|{}|{}".format(family, int(bold), int(italic))] = rec
    for family, (name, index) in WINDOWS.items():
        _, t, rec = entry(os.path.join(windows, name), index)
        rec.update(vertical(t), widths=widths(t))
        faces["{}|0|0".format(family)] = rec
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"source": "tools/make_font_metrics.py", "faces": faces}, fh,
                  ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
