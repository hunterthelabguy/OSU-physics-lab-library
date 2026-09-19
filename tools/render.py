"""Render converted Markdown to HTML, one file at a time or as the whole site.

Usage:
  python tools/render.py FILE.md [FILE.md ...] [--theme faithful|modern]
                         [--out DIR]
  python tools/render.py --site [--out DIR]

Both themes render the same Markdown source (ledger 28): one keeps the
original Word page settings, the other drops them and follows
docs/presentation-evidence.md. Nothing is ever copied into a second file.

File mode writes build/<theme>/<id>.html, one standalone page per theme.

Site mode writes build/site/: the landing page, the course index, the public
"How this was made" page (lifted from VISION.md, never retyped), and every
converted document in both presentations with a link that switches between
them. Output is plain static files with relative links, so any host serves
them and they also open from disk (ledger 39). Every page carries the draft
banner and asks search engines not to index the site (ledger 37).

build/ is not committed. Requires Pandoc on PATH or in PANDOC.
"""

import argparse
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PANDOC = os.environ.get("PANDOC", "pandoc")
THEMES = ("faithful", "modern")

# The draft banner, mandatory on every page while the license is open
# (ledger 37). Owner-reviewed wording; change it here only.
BANNER_MAIN = "Draft: license pending, not for distribution."
BANNER_DETAIL = (
    "An unlisted working draft of the OSU introductory physics lab "
    "curriculum, shared for comment. The license for this material is not "
    "settled, so please do not pass these pages on or share the link."
)

THEME_LABEL = {
    "faithful": "As it was written",
    "modern": "Rebuilt for reading",
}

THEME_NOTE = {
    "faithful": (
        "This page reproduces the original Word page settings, including the "
        "ones the presentation review calls into question. The words and the "
        "bold are the original authors', unchanged."
    ),
    "modern": (
        "This page drops the Word page settings and sets typography from the "
        "reading research and WCAG 2.2 SC 1.4.8. The words are the original "
        "authors', unchanged; graded questions are marked by a labeled block "
        "rather than by bold."
    ),
}


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def pandoc_meta(md_path):
    """Front matter as plain data, read by Pandoc so YAML needs no library."""
    out = subprocess.run(
        [PANDOC, md_path, "-f", "markdown-smart", "-t", "html",
         "--template", os.path.join(ROOT, "tools", "meta.template")],
        check=True, capture_output=True, text=True, encoding="utf-8",
    ).stdout
    return json.loads(out)


def body_after_front_matter(md_path):
    with open(md_path, encoding="utf-8") as fh:
        text = fh.read()
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[text.find("\n", end + 1) + 1:]
    return text.lstrip("\n")


def up(depth):
    """Relative prefix from a page `depth` directories below the site root."""
    return "../" * depth if depth else ""


def site_vars(depth):
    r = up(depth)
    return [
        "-M", "bannermain=" + BANNER_MAIN,
        "-M", "bannerdetail=" + BANNER_DETAIL,
        "-M", "homehref=" + (r or "./"),
        "-M", "indexhref=" + r + "courses/",
        "-M", "methodhref=" + r + "how-this-was-made/",
    ]


def render(md_path, theme, out_dir, out_path=None, depth=None, extra=()):
    """Render one converted document in one presentation."""
    name = os.path.splitext(os.path.basename(md_path))[0]
    out = out_path or os.path.join(out_dir, theme, name + ".html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    # Absolute, so --embed-resources finds it wherever the output lands.
    css = os.path.join(ROOT, "themes", theme + ".css").replace(os.sep, "/")
    chrome = os.path.join(ROOT, "site", "site.css").replace(os.sep, "/")
    cmd = [
        PANDOC, md_path,
        "-f", "markdown-smart",
        "-t", "html5",
        "--standalone",
        # Embed the theme so a downloaded page works on its own.
        "--embed-resources",
        "--template", os.path.join(ROOT, "tools", "template.html"),
        "--lua-filter", os.path.join(ROOT, "tools", "filters", "questions.lua"),
        "-M", "theme=" + theme,
        "-M", "css=" + css,
    ]
    if depth is not None:
        cmd += ["-M", "presentationnote=" + THEME_NOTE[theme],
                "-M", "chromecss=" + chrome] + site_vars(depth)
    else:
        cmd += ["-M", "presentationnote=Presentation: " + theme + "."]
    cmd += list(extra) + ["-o", out]
    run(cmd)
    return out


def render_page(md_text, title, out, depth, footnote="", nav=True):
    """Render a site page (landing, course index, method) from Markdown text."""
    os.makedirs(os.path.dirname(out), exist_ok=True)
    chrome = os.path.join(ROOT, "site", "site.css").replace(os.sep, "/")
    cmd = [
        PANDOC,
        "-f", "markdown-smart",
        "-t", "html5",
        "--standalone",
        "--embed-resources",
        "--template", os.path.join(ROOT, "tools", "template-site.html"),
        "-M", "title=" + title,
        "-M", "chromecss=" + chrome,
        "-M", "footnote=" + footnote,
        "-M", "uphref=" + ("1" if nav else ""),
        "-o", out,
    ] + site_vars(depth)
    run(cmd, input=md_text, text=True, encoding="utf-8")
    return out


def converted_documents():
    """Every converted file under curriculum/, keyed by its permanent id."""
    docs = {}
    pattern = os.path.join(ROOT, "curriculum", "**", "*.md")
    for path in sorted(glob.glob(pattern, recursive=True)):
        meta = pandoc_meta(path)
        if "source_file" not in meta:
            continue          # not a converted document
        docs[meta["id"]] = {"path": path, "meta": meta}
    return docs


def how_this_was_made():
    """Lift the section of that name out of VISION.md rather than retyping it.

    Principle 2 of the vision: one copy we edit. The public page is built
    from it, so the two can never disagree.
    """
    with open(os.path.join(ROOT, "VISION.md"), encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"^## How this was made$(.*?)(?=^## )", text, re.M | re.S)
    if not m:
        raise SystemExit("VISION.md has no 'How this was made' section")
    return "# How this was made\n" + m.group(1).rstrip() + "\n"


def lab_entry(lab, docs, depth):
    """One lab in the course index. A lab links only once it is converted."""
    doc_id = lab.get("document")
    doc = docs.get(doc_id) if doc_id else None
    number = lab.get("number", "")
    name = ("Lab " + number + ": " if number else "") + lab["title"]
    e = html.escape
    out = ['<li class="{}">'.format("converted" if doc else "pending")]
    if doc:
        href = up(depth) + "labs/" + doc_id + "/modern/"
        out.append('<p class="lab-title"><a href="{}">{}</a></p>'
                   .format(e(href), e(name)))
    else:
        out.append('<p class="lab-title">{}</p>'.format(e(name)))
    if lab.get("description"):
        out.append('<p class="lab-desc">{}</p>'.format(e(lab["description"])))
    if doc:
        faithful = up(depth) + "labs/" + doc_id + "/faithful/"
        out.append('<p class="lab-state">Converted and checked. '
                   '<a href="{}">Also available as it was written</a>.</p>'
                   .format(e(faithful)))
    else:
        out.append('<p class="lab-state">Not yet converted.</p>')
    out.append("</li>")
    return "\n".join(out)


def course_index_markdown(docs, depth):
    src = os.path.join(ROOT, "site", "courses.md")
    meta = pandoc_meta(src)
    parts = ["# Course index\n", body_after_front_matter(src)]
    e = html.escape
    for course in meta["courses"]:
        heading = course["code"]
        if course.get("name"):
            heading += ": " + course["name"]
        parts.append("\n## " + heading + "\n")
        if course.get("note"):
            parts.append('<p class="course-note">{}</p>\n'
                         .format(e(course["note"])))
        if course.get("labs"):
            items = "\n".join(lab_entry(lab, docs, depth)
                              for lab in course["labs"])
            parts.append('<ul class="lab-list">\n' + items + "\n</ul>\n")
    parts.append(
        '\n<p class="course-note">Lab numbers, titles and descriptions for '
        "PH 211 are quoted from {}. They are quoted, not converted: the "
        "content-unchanged check covers converted documents only.</p>\n"
        .format(e(meta["source_note"])))
    return "\n".join(parts)


def redirect_page(out, target):
    """A plain meta-refresh stub, so a trimmed URL still lands somewhere.

    It carries the banner too, so no page on the site is without it.
    """
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(
            '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
            '<meta charset="utf-8">\n'
            '<meta name="robots" content="noindex, nofollow">\n'
            '<meta http-equiv="refresh" content="0; url={0}">\n'
            "<title>Redirecting</title>\n</head>\n<body>\n"
            "<p>{1}</p>\n"
            '<p><a href="{0}">Continue to the lab</a>.</p>\n'
            "</body>\n</html>\n".format(target, html.escape(BANNER_MAIN)))
    return out


def build_site(out_dir):
    site = os.path.join(out_dir, "site")
    if os.path.isdir(site):
        shutil.rmtree(site)
    os.makedirs(site)
    written = []

    docs = converted_documents()
    for doc_id, doc in docs.items():
        for theme in THEMES:
            other = THEMES[0] if theme == THEMES[1] else THEMES[1]
            out = os.path.join(site, "labs", doc_id, theme, "index.html")
            written.append(render(
                doc["path"], theme, out_dir, out_path=out, depth=3,
                extra=[
                    "-M", "uphref=" + up(3) + "courses/",
                    "-M", "uplabel=Course index",
                    "-M", "switchhref=" + up(1) + other + "/",
                    "-M", "switchlabel=Read it " + THEME_LABEL[other].lower(),
                ]))
        written.append(redirect_page(
            os.path.join(site, "labs", doc_id, "index.html"), "modern/"))

    written.append(render_page(
        body_after_front_matter(os.path.join(ROOT, "site", "landing.md")),
        "OSU physics lab library",
        os.path.join(site, "index.html"), 0, nav=False,
        footnote="This site is built from the repository "
                 "OSU-physics-lab-library with Pandoc and one build script."))

    written.append(render_page(
        course_index_markdown(docs, 1), "Course index",
        os.path.join(site, "courses", "index.html"), 1))

    written.append(render_page(
        how_this_was_made(), "How this was made",
        os.path.join(site, "how-this-was-made", "index.html"), 1,
        footnote="This page is built from VISION.md in the project's "
                 "repository; ledger numbers refer to the dated decision "
                 "ledger kept there."))

    robots = os.path.join(site, "robots.txt")
    with open(robots, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Unlisted draft while the license is open (ledger 37).\n"
                 "User-agent: *\nDisallow: /\n")
    written.append(robots)
    return written


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--site", action="store_true",
                    help="build the whole static site into build/site")
    ap.add_argument("--theme", choices=THEMES)
    ap.add_argument("--out", default=os.path.join(ROOT, "build"))
    args = ap.parse_args(argv)

    if args.site:
        if args.files:
            ap.error("--site builds every converted file; pass no file names")
        for path in build_site(args.out):
            print("wrote", os.path.relpath(path, ROOT))
        return 0

    if not args.files:
        ap.error("pass a file to render, or --site")
    themes = (args.theme,) if args.theme else THEMES
    for md in args.files:
        for theme in themes:
            print("wrote", os.path.relpath(render(md, theme, args.out), ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
