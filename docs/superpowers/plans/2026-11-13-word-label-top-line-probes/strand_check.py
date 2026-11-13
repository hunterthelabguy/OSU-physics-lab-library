"""For each lab's Word renders A (as built) and D2 (label as the box's top
line): page counts, and every page whose last line before the footer is a
question or checkpoint label (a stranded label)."""
import os, pathlib, re, subprocess, sys

root = pathlib.Path(sys.argv[1])
pdftotext = os.environ["PDFTOTEXT"]
label = re.compile(r"^(QUESTION|CHECKPOINT) \d+$")


def pages(pdf):
    text = subprocess.run([pdftotext, "-layout", str(pdf), "-"], capture_output=True, text=True, encoding="utf-8").stdout
    return [p for p in text.split("\f") if p.strip()]


total = {"A": 0, "D2": 0}
for lab in sorted(root.iterdir()):
    row = []
    for name in ("A", "D2"):
        ps = pages(lab / f"{name}.pdf")
        stranded = []
        for i, p in enumerate(ps, 1):
            lines = [l.strip() for l in p.splitlines() if l.strip() and not l.strip().startswith("Department of Physics")]
            if lines and label.match(lines[-1]):
                stranded.append(f"p{i} {lines[-1]}")
        total[name] += len(stranded)
        row.append(f"{name} {len(ps)}pp stranded {stranded}")
    print(f"{lab.name}: " + " | ".join(row))
print("TOTAL stranded", total)
