"""Build the site with Quarto into build/quarto-site/ (D-0033, phase 1).

Usage: python tools/quarto_build.py

Generates the pages Quarto renders (gitignored, never hand-edited) from the
same sources and functions tools/render.py uses, runs Quarto, strips the
search markup and search.json Quarto writes even with search off (D-0037),
puts the templates' chrome on every page it rendered (D-0036), then adds
what Quarto does not make. Any Quarto warning line fails the
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
import quarto_chrome
import downloads

ROOT = render.ROOT
QUARTO = os.environ.get("QUARTO", "quarto")
OUT = os.path.join(ROOT, "build", "quarto-site")
GENERATED = ["index.qmd", "404.qmd", "courses", "how-this-site-works", "labs",
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
    # Pages serves this at any unknown path (D-0049); post() gives it a base.
    write("404.qmd", {"title": "Page not found"},
          include("404.qmd", "site/404.md"))

    docs = render.converted_documents()
    meta = render.courses_meta()
    # The course index and each course's page (D-0069, D-0070) take the
    # left-aligned grid in site/site.css by their body class. Quarto would
    # parse a raw HTML table into its own and add Bootstrap's classes, so
    # table processing is off for them.
    courses = {"body-classes": "courses", "html-table-processing": "none"}
    write("courses/index.qmd", dict(title="Course index", **courses),
          render.course_index_markdown(meta, docs))
    write("how-this-site-works/index.qmd", {"title": "How this site works"},
          include("how-this-site-works/index.qmd", "site/how-this-site-works.md"))
    write("sims/index.qmd", {"title": "Sims"},
          render.sims_index_markdown(render.sims()))

    pages = [
        {"html": "index.html", "kind": "site", "depth": 0, "theme": None, "footnote": ""},
        {"html": "404.html", "kind": "site", "depth": 0, "theme": None, "footnote": ""},
        {"html": "courses/index.html", "kind": "site", "depth": 1, "theme": None, "footnote": ""},
        {"html": "how-this-site-works/index.html", "kind": "site", "depth": 1, "theme": None,
         "footnote": render.METHOD_FOOTNOTE},
        {"html": "sims/index.html", "kind": "site", "depth": 1, "theme": None, "footnote": ""},
    ]

    for course in meta["courses"]:
        folder = "courses/" + render.course_slug(course)
        write(folder + "/index.qmd", dict(title=render.course_heading(course), **courses),
              render.course_page_markdown(course, docs))
        pages.append({"html": folder + "/index.html", "kind": "site", "depth": 2,
                      "theme": None, "footnote": "",
                      "tabs": render.course_tabs(meta["courses"], course)})

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
            pages.append({"html": "labs/{}/{}/index.html".format(doc_id, theme),
                          "kind": "doc", "depth": 3, "theme": theme, "footnote": "",
                          # D-0053: downloads come from modern only.
                          "download_id": doc_id if theme == downloads.THEME else ""})
    return pages


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


def dress_pages(pages):
    """Put the templates' chrome on every rendered page (D-0036)."""
    for page in pages:
        path = os.path.join(OUT, *page["html"].split("/"))
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        body_class, top, bottom = quarto_chrome.old_chrome(page)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(quarto_chrome.dress(text, body_class, top, bottom))


def base_404(path):
    """Resolve the 404 page's relative links from the site root.

    Pages serves 404.html at whatever path was asked for. Quarto already
    writes its own links in a 404 page from the root, but the chrome that
    dress_pages() adds afterwards (the nav: courses/, sims/) is relative and
    would miss from /labs/x/. The base goes first in <head>, before any link
    it governs. Assumes the site is served from the root of its host, as it
    is on pages.dev and on a subdomain; Quarto's own rewrite assumes the same.
    """
    with open(path, encoding="utf-8", newline="") as fh:
        text = fh.read()
    if text.count("<head>\n") != 1:
        raise ValueError("404.html: expected exactly one <head>")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text.replace("<head>\n", '<head>\n<base href="/">\n', 1))


def post():
    """What Quarto does not make, written with render.py's own functions."""
    for sim_id, sim in render.sims().items():
        render.render_sim(sim_id, sim, OUT)
    for doc_id in render.converted_documents():
        render.redirect_page(os.path.join(OUT, "labs", doc_id, "index.html"),
                             "modern/")
    # The retired faithful page's address (D-0108).
    for doc_id in render.converted_documents():
        render.redirect_page(os.path.join(OUT, "labs", doc_id, "faithful", "index.html"),
                             "../modern/")
    # The page's old address (D-0072).
    render.redirect_page(os.path.join(OUT, "how-this-was-made", "index.html"),
                         "../" + render.METHOD_PATH, "Continue to How this site works")
    base_404(os.path.join(OUT, "404.html"))
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write("# Unlisted draft while the license is open (ledger 37).\n"
                 "User-agent: *\nDisallow: /\n")


def build():
    check_version(quarto_version())
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    pages = generate()
    run_quarto()
    strip_search()
    dress_pages(pages)
    post()
    downloads.build(OUT, render.converted_documents())


if __name__ == "__main__":
    build()
    sys.exit(0)
