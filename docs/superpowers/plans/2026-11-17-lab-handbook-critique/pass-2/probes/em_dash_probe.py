"""The em-dash scan on the real ruled-change files: each, given an em dash in
a temporary copy, is reported; a converted file given one is not. Run from
the tree root after T4."""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tools")
import check_em_dash  # noqa: E402
import check_unchanged  # noqa: E402

files = sorted(str(p).replace("\\", "/") for p in Path("curriculum").rglob("*.md"))
ruled = [f for f in files if check_unchanged.rebaselined(f)]
print("ruled-change files:", ruled)
with tempfile.TemporaryDirectory() as d:
    for f in files:
        dst = Path(d) / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(f, dst)
        with open(dst, "a", encoding="utf-8") as fh:
            fh.write("\nInjected — dash.\n")
    found = check_em_dash.scan(d, ("curriculum",))
print("reported with a dash injected in every file:", found)
print("ruled-change all reported:", sorted(found) == sorted(ruled))
print("real repository scan:", check_em_dash.scan())
