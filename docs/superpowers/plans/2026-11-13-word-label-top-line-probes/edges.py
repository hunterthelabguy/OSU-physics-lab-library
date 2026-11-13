"""Measure, on a 300 dpi PPM of one box (pdftoppm, no PIL), the orange
rule's x-range and the tint's right edge on two rows: one through the
label line, one through the stem. Prints points (1 pt = 300/72 px)."""
import sys

def read_ppm(path):
    data = open(path, "rb").read()
    parts, i = [], 0
    while len(parts) < 4:
        while data[i:i + 1].isspace(): i += 1
        j = i
        while not data[j:j + 1].isspace(): j += 1
        parts.append(data[i:j]); i = j
    i += 1
    w, h = int(parts[1]), int(parts[2])
    return w, h, data[i:]

w, h, px = read_ppm(sys.argv[1])
pt = 300 / 72

def row(y):
    return [tuple(px[(y * w + x) * 3:(y * w + x) * 3 + 3]) for x in range(w)]

def orange(c): return c[0] > 180 and c[1] < 110 and c[2] < 60
def tint(c): return abs(c[0] - 0xF4) < 6 and abs(c[1] - 0xF7) < 6 and abs(c[2] - 0xF9) < 6

for name, y in (("label", int(sys.argv[2])), ("stem", int(sys.argv[3]))):
    r = row(y)
    xs = [x for x, c in enumerate(r) if orange(c)]
    ts = [x for x, c in enumerate(r) if tint(c)]
    print(f"{name:5} y={y}: rule {xs[0] / pt:.2f}-{(xs[-1] + 1) / pt:.2f} pt, tint right edge {(ts[-1] + 1) / pt:.2f} pt" if xs and ts else f"{name}: nothing found")
