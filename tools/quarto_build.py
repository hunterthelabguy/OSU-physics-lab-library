"""Build the site with Quarto into build/quarto-site/ (D-0033, phase 1).

Usage: python tools/quarto_build.py

Generates the pages Quarto renders (gitignored, never hand-edited) from the
same sources and functions tools/render.py uses, runs Quarto, strips the
search markup and search.json Quarto writes even with search off (D-0037),
then adds what Quarto does not make. Any Quarto warning line fails the
build. Requires Quarto (QUARTO, or quarto on PATH), and the driver checks that
it is exactly QUARTO_VERSION before doing anything; it also needs Pandoc for
front matter (PANDOC, as render.py).
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
QUARTO_VERSION = "1.10.18"


def check_version(reported):
    """Fail unless Quarto reports exactly the pinned version (D-0033)."""
    if reported.strip() != QUARTO_VERSION:
        raise SystemExit(
            "Quarto {} is pinned; this Quarto reports {!r}. Upgrade the pin on "
            "purpose, in its own PR.".format(QUARTO_VERSION, reported.strip()))


def quarto_version():
    return subprocess.run([QUARTO, "--version"], capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout


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


QUARTO_GENERATOR = '<meta name="generator" content="quarto-'
SEARCH_FRAGMENTS = (
    ("search options script",
     re.compile(r'<script id="quarto-search-options"[^>]*>.*?</script>\n', re.S)),
    ("search results div",
     re.compile(r'<div id="quarto-search-results"></div>\n')),
)


def strip_search_page(text, page):
    """Remove exactly one of each search fragment from a Quarto page.

    Strict as D-0036's anchors: a page with none, or two, of either fragment
    is a ValueError naming the page. Nothing else in the page changes.
    """
    for name, pattern in SEARCH_FRAGMENTS:
        found = len(pattern.findall(text))
        if found != 1:
            raise ValueError("{}: expected exactly one {}, found {}".format(page, name, found))
        text = pattern.sub("", text)
    return text


def strip_search(out=OUT):
    """Remove Quarto's search leftovers from every page it wrote, and search.json.

    website.search: false does not suppress the search markup or search.json
    in Quarto 1.10.18, so this is the guard that holds D-0037's "no search".
    Runs before post(). Only pages Quarto wrote (they carry its generator tag)
    are touched: Quarto also copies a sim's source page into the output as is,
    and post() replaces that copy, so it is left alone here.
    """
    for folder, dirs, files in os.walk(out):
        dirs[:] = [d for d in dirs if d != "site_libs"]
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(folder, name)
            rel = os.path.relpath(path, out).replace(os.sep, "/")
            with open(path, encoding="utf-8", newline="") as fh:
                text = fh.read()
            if QUARTO_GENERATOR not in text:
                continue
            text = strip_search_page(text, rel)
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(text)
    index = os.path.join(out, "search.json")
    if os.path.isfile(index):
        os.remove(index)


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
    check_version(quarto_version())
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    generate()
    run_quarto()
    strip_search()
    post()


if __name__ == "__main__":
    build()
    sys.exit(0)
