"""Build the site with Quarto into build/quarto-site/ (D-0033, phase 1).

Usage: python tools/quarto_build.py

Generates the pages Quarto renders (gitignored, never hand-edited) from the
same sources and functions tools/render.py uses, runs Quarto, then adds what
Quarto does not make. Any Quarto warning line fails the build. Requires
Quarto 1.10.18 (QUARTO, or quarto on PATH) and Pandoc for front matter
(PANDOC, as render.py).
"""

import json
import os
import re
import shutil
import subprocess
import sys

import render

ROOT = render.ROOT
QUARTO = os.environ.get("QUARTO", "quarto")
OUT = os.path.join(ROOT, "build", "quarto-site")
GENERATED = ["index.qmd", "courses", "how-this-was-made", "labs",
             os.path.join("sims", "index.qmd")]
WARNING = re.compile(r"^\s*\[?(WARN|WARNING)\b", re.I | re.M)


def rel_to_root(page):
    """Relative path from a generated page's folder back to the repo root."""
    up = os.path.relpath(ROOT, os.path.dirname(os.path.join(ROOT, page)))
    return up.replace(os.sep, "/")


def write(page, front, body):
    path = os.path.join(ROOT, page)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lines = ["---"] + ["{}: {}".format(k, json.dumps(v, ensure_ascii=False)) for k, v in front.items()]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n---\n\n" + body.rstrip("\n") + "\n")


def include(page, target):
    return "{{< include " + rel_to_root(page) + "/" + target + " >}}"


def generate():
    for rel in GENERATED:
        path = os.path.join(ROOT, rel)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    write("index.qmd", {"title": "OSU physics lab library"},
          include("index.qmd", "site/landing.md"))

    docs = render.converted_documents()
    write("courses/index.qmd", {"title": "Course index"},
          render.course_index_markdown(docs, 1))
    write("how-this-was-made/index.qmd", {"title": "How this was made"},
          render.how_this_was_made())
    write("sims/index.qmd", {"title": "Sims"},
          render.sims_index_markdown(render.sims()))

    for doc_id, doc in docs.items():
        source = os.path.relpath(doc["path"], ROOT).replace(os.sep, "/")
        for theme in render.THEMES:
            page = "labs/{}/{}/index.qmd".format(doc_id, theme)
            up = rel_to_root(page)
            write(page, {
                "title": doc["meta"]["title"],
                "theme-name": theme,
                "filters": [up + "/tools/filters/questions.lua"],
                "css": [up + "/themes/" + theme + ".css"],
            }, include(page, source))


def run_quarto():
    proc = subprocess.run([QUARTO, "render"], cwd=ROOT, capture_output=True,
                          text=True, encoding="utf-8")
    log = proc.stdout + proc.stderr
    print(log)
    if proc.returncode != 0:
        raise SystemExit("quarto render failed")
    if WARNING.search(log):
        raise SystemExit("quarto printed a warning; the build fails on any warning")


def post():
    """What Quarto does not make, written with render.py's own functions."""
    for sim_id, sim in render.sims().items():
        render.render_sim(sim_id, sim, OUT)
    for doc_id in render.converted_documents():
        render.redirect_page(os.path.join(OUT, "labs", doc_id, "index.html"),
                             "modern/")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write("# Unlisted draft while the license is open (ledger 37).\n"
                 "User-agent: *\nDisallow: /\n")


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    generate()
    run_quarto()
    post()


if __name__ == "__main__":
    build()
    sys.exit(0)
