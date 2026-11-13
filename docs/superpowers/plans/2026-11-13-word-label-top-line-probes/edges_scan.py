"""Every row of an edges.py crop: the rule's x-range and the tint's right
edge, printed where they differ from the row before (so a seam between the
label paragraph and the table shows), plus the first row of tint and the
first row of label ink (the --quiet text colour 0D5257). Usage: PPM."""
import sys
sys.path.insert(0, sys.path[0])
data = open(sys.argv[1], "rb").read()
parts, i = [], 0
while len(parts) < 4:
    while data[i:i + 1].isspace(): i += 1
    j = i
    while not data[j:j + 1].isspace(): j += 1
    parts.append(data[i:j]); i = j
i += 1
w, h, px = int(parts[1]), int(parts[2]), data[i:]
pt = 300 / 72


def c(x, y): return tuple(px[(y * w + x) * 3:(y * w + x) * 3 + 3])
def orange(v): return v[0] > 180 and v[1] < 110 and v[2] < 60
def tint(v): return abs(v[0] - 0xF4) < 6 and abs(v[1] - 0xF7) < 6 and abs(v[2] - 0xF9) < 6
def ink(v): return v[0] < 90 and 60 < v[1] < 120 and 60 < v[2] < 120


prev, first_tint, first_ink = None, None, None
for y in range(h):
    row = [c(x, y) for x in range(w)]
    xs = [x for x, v in enumerate(row) if orange(v)]
    ts = [x for x, v in enumerate(row) if tint(v)]
    if ts and first_tint is None: first_tint = y
    if first_ink is None and any(ink(v) for v in row[200:900]): first_ink = y
    cur = (f"rule {xs[0] / pt:.2f}-{(xs[-1] + 1) / pt:.2f}" if xs else "no rule",
           f"tint right {(ts[-1] + 1) / pt:.2f}" if ts else "no tint")
    if cur != prev:
        print(f"y={y} ({y / pt:.2f} pt): {cur[0]} pt, {cur[1]} pt")
        prev = cur
print(f"first tint row {first_tint} ({first_tint / pt:.2f} pt), first label ink row {first_ink} ({first_ink / pt:.2f} pt)")
