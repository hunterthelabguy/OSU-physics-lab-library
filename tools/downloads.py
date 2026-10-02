"""Lab downloads: Markdown, Word, HTML and PDF (D-0052, D-0053).

Run by tools/quarto_build.py after the site is built and dressed; never on
its own. Every file comes from the modern presentation and carries the
draft banner (ledger 37), and is written beside the presentations as
labs/<id>/<id>.<ext>, so a saved file is named after the lab. Markdown is
the source, byte for byte (LEDGER 28). Word is Pandoc's, from the source,
with the banner as its first two paragraphs. HTML is the built modern page
made self-contained: stylesheets and fonts inlined, scripts and both navs
removed, relative links reduced to their words, so it opens from disk. PDF
is the built modern page printed by headless Chrome with the site's print
rules. A missing tool is an error, never a skip (LEDGER 53).
"""

import base64
import os
import re
import shutil
import subprocess

import render

THEME = "modern"
EXTENSIONS = ("md", "docx", "html", "pdf")
# The owner's words in every download, in place of the logo (chat, 2026-10-01).
PHYSICS = "Department of Physics, Oregon State University"
REFERENCE_DOCX = os.path.join(render.ROOT, "tools", "reference.docx")
FILTER = os.path.join(render.ROOT, "tools", "filters", "questions.lua")
FONT_TYPES = {".woff2": "font/woff2", ".woff": "font/woff"}
# Lab pages use no Bootstrap icon; standalone() refuses a page that does.
UNUSED_STYLESHEETS = ("bootstrap-icons.css",)

NAV = re.compile(r'<nav class="(osu-nav|site-nav)"[^>]*>.*?</nav>\n?', re.S)
SCRIPT = re.compile(r"<script\b[^>]*>.*?</script>\n?", re.S)
STYLESHEET = re.compile(r'<link\b[^>]*\brel="stylesheet"[^>]*>\n?')
HREF = re.compile(r'\bhref="([^"]*)"')
ANCHOR = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.S)
ATTR_URL = re.compile(r'\b(?:src|href)="([^"]*)"')
CSS_URL = re.compile(r"""url\(\s*(["']?)([^)"']+)\1\s*\)""")


def is_relative(url):
    """True for a path inside the site; false for a scheme, //host, or #."""
    return not re.match(r"(?:[a-z][a-z0-9+.-]*:|#|//)", url, re.I)


def inline_css(css_text, css_dir):
    """Embed each relative url() (fonts only) as a data: URI."""
    def embed(m):
        url = m.group(2)
        if not is_relative(url):
            return m.group(0)
        path = os.path.normpath(os.path.join(css_dir, url.split("?")[0].split("#")[0]))
        ext = os.path.splitext(path)[1].lower()
        if ext not in FONT_TYPES:
            raise ValueError("unexpected resource in a stylesheet: " + url)
        with open(path, "rb") as fh:
            data = base64.b64encode(fh.read()).decode("ascii")
        return 'url("data:{};base64,{}")'.format(FONT_TYPES[ext], data)
    return CSS_URL.sub(embed, css_text)


def standalone(page_html, page_dir):
    """The built modern page, made to open from disk (D-0053, call 5)."""
    navs = NAV.findall(page_html)
    if sorted(navs) != ["osu-nav", "site-nav"]:
        raise ValueError("expected one osu-nav and one site-nav, found {}".format(navs))
    text = NAV.sub("", page_html)
    text = SCRIPT.sub("", text)
    if re.search(r'class="[^"]*\bbi-', text):
        raise ValueError("the page uses Bootstrap icons; their stylesheet cannot be dropped")

    def link(m):
        href = HREF.search(m.group(0)).group(1)
        if not is_relative(href):
            raise ValueError("external stylesheet: " + href)
        if os.path.basename(href) in UNUSED_STYLESHEETS:
            return ""
        path = os.path.normpath(os.path.join(page_dir, href))
        with open(path, encoding="utf-8") as fh:
            css = inline_css(fh.read(), os.path.dirname(path))
        return "<style>\n" + css + "\n</style>\n"
    text = STYLESHEET.sub(link, text)

    def unwrap(m):
        found = HREF.search(m.group(1))
        return m.group(2) if found and is_relative(found.group(1)) else m.group(0)
    text = ANCHOR.sub(unwrap, text)

    left = sorted({u for u in ATTR_URL.findall(text) if is_relative(u)})
    if left:
        raise ValueError("relative references left: {}".format(left[:5]))
    return text


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


def word(doc, dest):
    """The banner as the first two paragraphs; the department line and page
    count in the page footer, from tools/reference.docx."""
    text = "**{}**\n\n{}\n\n".format(render.BANNER_MAIN, render.BANNER_DETAIL)
    pandoc(doc, text + render.body_after_front_matter(doc["path"]),
           ["-t", "docx", "--reference-doc", REFERENCE_DOCX, "-M", "lang=en", "-o", dest])


def build(out, docs):
    """Write every lab's downloads into out/labs/<id>/."""
    for doc_id, doc in docs.items():
        folder = os.path.join(out, "labs", doc_id)
        markdown(doc, os.path.join(folder, doc_id + ".md"))
        word(doc, os.path.join(folder, doc_id + ".docx"))
