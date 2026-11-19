"""Read the built handbook and Lab 3: where each address really lives, and
what the plan's h2 regex matches.

Run from the scratch tree's root after a build: python -X utf8 built_probe.py
"""
import re
import sys
from pathlib import Path

Q = Path("build/quarto-site/labs")
page = (Q / "ph21x-lab-handbook" / "modern" / "index.html").read_text(encoding="utf-8")
print("h1:", re.findall(r"<h1[^>]*>.*?</h1>", page, re.S))
for tag in re.findall(r"<h2[^>]*>", page):
    print("h2 tag:", tag)
print("plan regex finds:", re.findall(r'<h2[^>]*\bid="([^"]+)"', page))
print("real id= on h2:", re.findall(r'<h2[^>]*\s id="([^"]+)"', page.replace("<h2 ", "<h2  ")))
for addr in ["plot-elements", "linearization", "what-is-uncertainty", "sources-of-uncertainty",
             "predictions-hypotheses-models", "graphical-analysis-tips", "variables-and-parameters"]:
    owners = re.findall(r'<(\w+)[^>]*\sid="' + re.escape(addr) + '"', page)
    print(addr, "id on:", owners)
print("alt texts:", re.findall(r'alt="([^"]*)"', page))
if len(sys.argv) > 1:
    lab3 = (Q / "ph211-uncertainty-handout" / "modern" / "index.html").read_text(encoding="utf-8")
    print("lab3 handbook links:", re.findall(r'href="([^"]*ph21x-lab-handbook[^"]*)"', lab3))
