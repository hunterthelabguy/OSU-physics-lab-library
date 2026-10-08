"""Lab downloads: Markdown, Word, HTML and PDF (D-0052, D-0053).

Run by tools/quarto_build.py after the site is built and dressed; never on
its own. Every file comes from the modern presentation, carries the draft
banner (ledger 37) and names the Department of Physics in place of the
logo, and is written beside the presentations as labs/<id>/<id>.<ext>, so
a saved file is named after the lab. Markdown is the source, byte for
byte (LEDGER 28). Word is Pandoc's, from the source, with the banner in
its page header and the department in its page footer, both from
tools/reference.docx with the page size and question label (D-0057). HTML is
a plain Pandoc render of the source: the banner, the department line and
the modern theme, everything embedded and no site chrome, so it opens
from disk. A missing tool is an error, never a skip (LEDGER 53).
"""

import os
import pathlib
import re
import shutil
import subprocess

import render

THEME = "modern"
CHROME = os.environ.get("CHROME", "google-chrome")
EXTENSIONS = ("md", "docx", "html", "pdf")
# The owner's words in every download, in place of the logo (chat, 2026-10-01).
PHYSICS = "Department of Physics, Oregon State University"
REFERENCE_DOCX = os.path.join(render.ROOT, "tools", "reference.docx")
FILTER = os.path.join(render.ROOT, "tools", "filters", "questions.lua")


def is_relative(url):
    """True for a path inside the site; false for a scheme, //host, or #."""
    return not re.match(r"(?:[a-z][a-z0-9+.-]*:|#|//)", url, re.I)


def pandoc(doc, text, args):
    """Pandoc on the source text, modern question labels; a warning fails."""
    proc = subprocess.run(
        [render.PANDOC, "-f", "markdown-smart", "--lua-filter", FILTER,
         "-M", "theme=" + THEME] + args,
        input=text, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0 or "[WARNING]" in proc.stderr:
        raise SystemExit("Pandoc failed on {}:\n{}".format(doc["path"], proc.stderr))


def markdown(doc, dest):
    shutil.copyfile(doc["path"], dest)


def box_colours():
    """The Word boxes' rules and fills, from the light :root block of
    themes/modern.css, as Pandoc metadata for tools/filters/questions.lua: a
    question's --accent and --tint (D-0057, D-0082), a checkpoint's
    --checkpoint-rule and --checkpoint-fill (D-0115)."""
    with open(os.path.join(render.ROOT, "themes", THEME + ".css"), encoding="utf-8") as fh:
        root = re.search(r":root\s*\{(.*?)\}", fh.read(), re.S).group(1)
    tokens = dict(re.findall(r"(--[\w-]+):\s*#([0-9a-fA-F]{6})\b", root))
    meta = {"box-rule": "--accent", "box-fill": "--tint",
            "checkpoint-rule": "--checkpoint-rule", "checkpoint-fill": "--checkpoint-fill"}
    args = []
    for key, token in meta.items():
        args += ["-M", key + "=" + tokens[token].upper()]
    return args


def word(doc, dest):
    """The source alone in the body; tools/reference.docx supplies the draft
    notice as the page header, the department line and page count as the
    page footer, the page, and the question label's style (D-0057); the
    filter draws each question as a one-cell table (D-0082)."""
    pandoc(doc, render.body_after_front_matter(doc["path"]),
           ["-t", "docx", "--reference-doc", REFERENCE_DOCX, "-M", "lang=en"]
           + box_colours() + ["-o", dest])


def html(doc, dest):
    """The old template with only its banner variables set: no header, nav
    or footer chrome, so nothing in it links into the site."""
    css = lambda *p: os.path.join(render.ROOT, *p).replace(os.sep, "/")
    pandoc(doc, PHYSICS + "\n\n" + render.body_after_front_matter(doc["path"]),
           ["-t", "html5", "--standalone", "--embed-resources",
            "--template", os.path.join(render.ROOT, "tools", "template.html"),
            "-M", "title=" + doc["meta"]["title"],
            "-M", "css=" + css("themes", THEME + ".css"),
            "-M", "chromecss=" + css("site", "site.css"),
            "-M", "presentationnote=" + render.THEME_NOTE[THEME],
            "-M", "bannermain=" + render.BANNER_MAIN,
            "-M", "bannerdetail=" + render.BANNER_DETAIL,
            "-o", dest])
    with open(dest, encoding="utf-8") as fh:
        left = [u for u in re.findall(r'\b(?:src|href)="([^"]*)"', fh.read()) if is_relative(u)]
    if left:
        raise SystemExit("{} links into the site, which a download cannot: {}".format(dest, left[:5]))


def pdf(page_path, dest):
    """Headless Chrome prints the built modern page with the site's print
    rules, which hide the header, nav and footer and supply the running
    header, the department line and page numbers (site/site.css, @page).
    --no-pdf-header-footer turns off Chrome's own."""
    if shutil.which(CHROME) is None and not os.path.isfile(CHROME):
        raise SystemExit("Chrome not found; set CHROME to the browser (LEDGER 53)")
    proc = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
         "--print-to-pdf=" + os.path.abspath(dest),
         pathlib.Path(os.path.abspath(page_path)).as_uri()],
        capture_output=True, text=True)
    if proc.returncode != 0 or not os.path.isfile(dest) or os.path.getsize(dest) == 0:
        raise SystemExit("Chrome did not print {}:\n{}".format(page_path, proc.stderr[-2000:]))


def build(out, docs):
    """Write every lab's downloads into out/labs/<id>/."""
    for doc_id, doc in docs.items():
        folder = os.path.join(out, "labs", doc_id)
        markdown(doc, os.path.join(folder, doc_id + ".md"))
        word(doc, os.path.join(folder, doc_id + ".docx"))
        html(doc, os.path.join(folder, doc_id + ".html"))
        pdf(os.path.join(folder, THEME, "index.html"), os.path.join(folder, doc_id + ".pdf"))
