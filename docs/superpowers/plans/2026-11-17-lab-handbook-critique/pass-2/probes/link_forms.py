"""Which link forms media.lua rewrites against which bad_links() validates.
Run from the tree root after T2."""
import os
import subprocess
import sys

sys.path.insert(0, "tests")
sys.path.insert(0, "tools")
import render  # noqa: E402
import test_lab_handbook as t  # noqa: E402

PANDOC = os.environ.get("PANDOC", "pandoc")
forms = ["ph21x-lab-handbook#plot-elements", "PH21X-lab-handbook#plot-elements",
         "ph21x-lab-handbook#plot-elements \"Plot elements\"", "ph21x-lab-handbook#Plot_Elements",
         "<ph21x-lab-handbook#plot-elements>"]
for f in forms:
    md = "[x](" + f + ")\n"
    out = subprocess.run([PANDOC, "-f", render.FROM, "-t", "html", "--lua-filter", "tools/filters/media.lua",
                          "-M", "library-url=" + render.LIBRARY_URL], input=md, capture_output=True,
                         encoding="utf-8").stdout.strip()
    rewritten = render.LIBRARY_URL in out
    validated = bool(t.LINK.findall(md))
    print("{:55} rewritten={!s:5} validated={}".format(f, rewritten, validated))
