"""Shared functions for the Quarto build (D-0061).

Once the old build's entry point, this is now a module with no command line:
tools/quarto_build.py, tools/quarto_chrome.py, tools/downloads.py and
tools/make_reference_docx.py import it. It holds the banner wording, the
presentation notes and footnotes, the document nav's metadata, the course
index and the course pages, the "How this was made" page (lifted from
VISION.md, never retyped), the sims and their bar, and the redirect stubs.

Both themes render the same Markdown source (ledger 28): one keeps the
original Word page settings, the other drops them and follows
docs/presentation-evidence.md. Nothing is ever copied into a second file.
Output is plain static files with relative links, so any host serves them
(ledger 39). Every page carries the draft banner and asks search engines not
to index the site (ledger 37).

Requires Pandoc in PANDOC (Quarto's bundled binary, D-0044) or on PATH.
"""

import base64
import glob
import html
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PANDOC = os.environ.get("PANDOC", "pandoc")
THEMES = ("faithful", "modern")

# Official logo files, committed byte for byte (DECISIONS D-0014, D-0020).
BRAND = os.path.join(ROOT, "site", "brand")
SITE_LOGO = os.path.join(BRAND, "OSU_horizontal_2C_W_over_B.png").replace(os.sep, "/")
# The header logo is published once and referenced from every page, so the
# browser caches it (D-0039 amended); data-external in brandheader.html keeps
# --embed-resources from inlining it. Sims keep theirs embedded (D-0026).
SITE_LOGO_URL = "site/brand/" + os.path.basename(SITE_LOGO)
SIM_LOGO = os.path.join(BRAND, "OSU_horizontal_2C_O_over_W.png")


def png_data_uri(path):
    """The sim's policy allows images only as data: URIs (img-src data:)."""
    with open(path, "rb") as fh:
        return "data:image/png;base64," + base64.b64encode(fh.read()).decode("ascii")

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

# The footnote on the "How this was made" page. The landing page's footnote
# named the old build and was not carried (D-0038); phase 4 deleted it.
METHOD_FOOTNOTE = ("This page is built from VISION.md in the project's "
                   "repository; ledger numbers refer to the dated decision "
                   "ledger kept there.")


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


def document_extras(theme, depth=3):
    """The document nav's metadata: the course index link and the switch."""
    other = THEMES[0] if theme == THEMES[1] else THEMES[1]
    return [
        "-M", "uphref=" + up(depth) + "courses/",
        "-M", "uplabel=Course index",
        "-M", "switchhref=" + up(1) + other + "/",
        "-M", "switchlabel=Read it " + THEME_LABEL[other].lower(),
    ]


def site_vars(depth):
    r = up(depth)
    return [
        "-M", "bannermain=" + BANNER_MAIN,
        "-M", "bannerdetail=" + BANNER_DETAIL,
        "-M", "homehref=" + (r or "./"),
        "-M", "indexhref=" + r + "courses/",
        "-M", "methodhref=" + r + "how-this-was-made/",
        "-M", "simshref=" + r + "sims/",
        "-M", "logo=" + r + SITE_LOGO_URL,
    ]


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


def courses_meta():
    """site/courses.md's front matter: the courses, their labs and notes."""
    return pandoc_meta(os.path.join(ROOT, "site", "courses.md"))


def course_slug(course):
    """The course code lowercased with its spaces removed: "PH 211" is ph211.

    It names a course page's folder (D-0069) and its zip (D-0067), so
    neither changes when a course's name is filled in.
    """
    return "".join(course["code"].split()).lower()


def course_heading(course):
    """The code and name, or the code alone while the name is not in hand."""
    return course["code"] + (": " + course["name"] if course.get("name") else "")


def converted_labs(course, docs):
    """The course's labs whose document is converted, in curriculum order."""
    return [lab for lab in course.get("labs") or [] if lab.get("document") in docs]


# The course index (D-0069): a chooser of course tiles. Claude's words,
# proposed with the boards in docs/design/2026-10-06-course-pages/.
COURSE_INDEX_INTRO = "Choose a course to see its labs."


def lab_count(course, docs):
    """A tile's count line, from site/courses.md and the converted documents."""
    listed, done = len(course.get("labs") or []), len(converted_labs(course, docs))
    if not done:
        return "No labs converted yet"
    labs = "lab" if listed == 1 else "labs"
    if done == listed:
        return "{} {}".format(listed, labs)
    return "{} {} listed, {} converted".format(listed, labs, done)


def course_tiles(courses, docs):
    """One tile per course, linking to its page (D-0069). A course with a
    converted lab gets the orange top rule; a name not yet in hand is left
    out rather than shown as a placeholder."""
    e = html.escape
    tiles = []
    for course in courses:
        lines = ['<li><a class="course-tile{}" href="{}/">'.format(
                     " converted" if converted_labs(course, docs) else "", course_slug(course)),
                 '<span class="course-tile-code">{}</span>'.format(e(course["code"]))]
        if course.get("name"):
            lines.append('<span class="course-tile-name">{}</span>'.format(e(course["name"])))
        lines.append('<span class="course-tile-count">{}</span>'.format(e(lab_count(course, docs))))
        tiles.append("\n".join(lines) + "\n</a></li>")
    return '<ul class="course-tiles">\n' + "\n".join(tiles) + "\n</ul>"


def course_tabs(courses, current):
    """The course tabs under the site nav of a course page (D-0069): one link
    per course, from a page two folders down, the current one marked. Passed
    to tools/template-site.html as a variable, which Pandoc inserts as is."""
    e = html.escape
    return "\n".join('<a href="../{0}/"{1}>{2}</a>'.format(
        course_slug(course),
        ' aria-current="page"' if course_slug(course) == course_slug(current) else "",
        e(course["code"])) for course in courses)


# A course page's lab table (D-0070), its column names in order.
LAB_COLUMNS = (("lab-num", "Lab"), ("lab-title", "Title"), ("lab-desc", "Description"))


def lab_table(labs, docs, depth):
    """Labs as one table: Lab, Title, Description, in curriculum order.

    A converted lab's title links to its modern page. The title cell also
    holds "Lab N: ", hidden from sight on wide screens and read by screen
    readers as part of the link; at phone width the rows stack, the Lab
    cell is hidden and the prefix shows, so the link reads "Lab N: Title"
    (D-0070). Descriptions are quoted whole.
    """
    e = html.escape
    rows = []
    for lab in labs:
        number = lab.get("number", "")
        title = e(lab["title"])
        if number:
            title = '<span class="lab-prefix">Lab {}: </span>{}'.format(e(number), title)
        doc_id = lab.get("document")
        if doc_id in docs:
            title = '<a href="{}">{}</a>'.format(
                e(up(depth) + "labs/" + doc_id + "/modern/"), title)
        rows.append('<tr><td class="lab-num">{}</td><td class="lab-title">{}</td>'
                    '<td class="lab-desc">{}</td></tr>'.format(
                        "Lab " + e(number) if number else "", title,
                        e(lab.get("description", ""))))
    head = "".join('<th scope="col" class="{}">{}</th>'.format(c, e(name))
                   for c, name in LAB_COLUMNS)
    return ('<table class="lab-table">\n<thead><tr>{}</tr></thead>\n<tbody>\n{}\n'
            "</tbody>\n</table>".format(head, "\n".join(rows)))


# Before launch only: the labs not yet converted, collapsed under the table
# (the owner's "5 collapsed", 2026-10-06). Every listed lab is to be
# converted by launch, and then this renders nothing.
PENDING_SUMMARY = "Not yet converted ({})"


def pending_labs(course, docs, depth):
    """The collapse of a course's unconverted labs, or "" when there is none."""
    pending = [lab for lab in course.get("labs") or [] if lab.get("document") not in docs]
    if not pending:
        return ""
    return ('<details class="lab-pending">\n<summary>{}</summary>\n{}\n</details>'
            .format(html.escape(PENDING_SUMMARY.format(len(pending))),
                    lab_table(pending, docs, depth)))


def raw_html(fragment):
    """A raw HTML block, so Pandoc passes it as written; read as Markdown,
    inline HTML would be wrapped in a paragraph."""
    return "```{=html}\n" + fragment + "\n```\n"


# Download all (D-0067): D-0053's names for the four formats, in the order of
# the lab page's download row, each with its published file's extension.
DOWNLOAD_FORMATS = (("docx", "Word"), ("html", "HTML"), ("pdf", "PDF"), ("md", "Markdown"))


def download_all(course, docs, depth):
    """The course's Download all control, or "" when no lab is converted.

    A quiet button after the course page's lab table opens a dialog of four
    format checkboxes, none ticked, and a "Download selected" button (D-0067,
    as amended 2026-10-03). Each checkbox carries its format's published
    files for the course's converted labs, written here from the converted
    documents, never typed; site/download-all.js zips the ticked ones in the
    page as <slug>.zip (ph211.zip). The button is hidden until the script
    runs, so a page without it shows no dead control.
    """
    ids = [lab["document"] for lab in converted_labs(course, docs)]
    if not ids:
        return ""
    e = html.escape
    boxes = []
    for ext, label in DOWNLOAD_FORMATS:
        files = " ".join(up(depth) + "labs/{0}/{0}.{1}".format(doc_id, ext)
                         for doc_id in ids)
        boxes.append('<label><input type="checkbox" value="{}" data-files="{}">'
                     ' {}</label>'.format(ext, e(files), e(label)))
    return raw_html(
        '<button type="button" class="download-all-open" aria-haspopup="dialog" hidden>'
        "Download all</button>\n"
        '<dialog class="download-all" data-zip="{}" aria-label="Download all">\n'
        '<div class="download-all-formats">\n{}\n</div>\n'
        '<button type="button" class="download-selected" disabled>Download selected</button>\n'
        "</dialog>".format(e(course_slug(course) + ".zip"), "\n".join(boxes)))


def course_index_markdown(meta, docs):
    """The course index (D-0069): the chooser, one tile per course."""
    return "\n".join(["# Course index\n", COURSE_INDEX_INTRO + "\n",
                      raw_html(course_tiles(meta["courses"], docs))])


def course_page_markdown(course, docs, depth=2):
    """One course's page (D-0069, D-0070): its h1, the intro from
    site/courses.md, its converted labs as one table, D-0067's Download all
    after it, and before launch the labs not yet converted, collapsed.
    A course with no labs shows its note instead of the intro."""
    e = html.escape
    labs = course.get("labs") or []
    parts = ["# " + course_heading(course) + "\n"]
    if labs:
        parts.append(body_after_front_matter(os.path.join(ROOT, "site", "courses.md")))
    if course.get("note"):
        parts.append('<p class="course-note">{}</p>\n'.format(e(course["note"])))
    done = converted_labs(course, docs)
    if done:
        parts.append(raw_html(lab_table(done, docs, depth)))
    control = download_all(course, docs, depth)
    if control:
        parts.append(control)
    pending = pending_labs(course, docs, depth)
    if pending:
        parts.append(raw_html(pending))
    if labs and course.get("source_note"):
        parts.append(
            '<p class="course-note">Lab numbers, titles and descriptions for '
            "{} are quoted from {}. They are quoted, not converted: the "
            "content-unchanged check covers converted documents only.</p>\n"
            .format(e(course["code"]), e(course["source_note"])))
    if control:
        parts.append('<script src="{}site/download-all.js" defer></script>\n'
                     .format(up(depth)))
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


# A sim ships as one self-contained page that must keep working offline from
# disk, so the site chrome is injected into the copy that is published and the
# source file is never touched. It has to be small: the sim's layout is ruled
# to fit a 1280x720 laptop without page scrolling, and every pixel here is
# taken from that budget. So it carries ledger 37's sentence and nothing more,
# not the longer note the other pages show. The bar is Paddletail Black with
# the O over W logo (D-0005, D-0020) and the draft sentence in Luminance
# (D-0022). The sim's own Content Security Policy is `default-src 'none'`
# with inline styles allowed, so an inline <style> works and anything fetched
# would not; the logo travels as a data: URI for the same reason.
SIM_CHROME = """<style>
.lib-bar {{
  flex: 0 0 auto;
  display: flex; flex-wrap: wrap; gap: .1rem .9rem; align-items: center;
  background: #000; color: #fff;
  padding: 0 .75rem;
  font: 400 .85rem/1.4 "Open Sans", ui-sans-serif, system-ui, "Segoe UI", Roboto, Arial, sans-serif;
}}
/* content-box: the sim sets border-box globally, which would shrink the
   22px logo height by the padding instead of adding the padding outside it. */
.lib-bar img {{ display: block; height: 22px; width: auto; padding: 6px 6px 6px 0; box-sizing: content-box; }}
.lib-bar .lib-draft {{ background: #ffb500; color: #000; font-weight: 700; padding: 0 .4rem; }}
.lib-bar a {{ color: #fff; }}
.lib-bar .lib-links {{ display: flex; gap: 1rem; margin-left: auto; }}
@media print {{ .lib-bar {{ display: none; }} }}
</style>
<div class="lib-bar">
<a href="https://oregonstate.edu"><img src="{logo}" alt="Oregon State University"></a>
<span class="lib-draft">{banner}</span>
<span class="lib-links"><a href="{home}">Library home</a><a href="{sims}">Sims</a></span>
</div>
"""

BODY_TAG = re.compile(r"(<body[^>]*>)", re.I)


def sims():
    """Self-contained sim pages: one directory each, holding an index.html."""
    found = {}
    pattern = os.path.join(ROOT, "sims", "*", "index.html")
    for path in sorted(glob.glob(pattern)):
        sim_id = os.path.basename(os.path.dirname(path))
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        m = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
        found[sim_id] = {
            "path": path,
            "title": m.group(1).strip() if m else sim_id,
            "text": text,
        }
    return found


def render_sim(sim_id, sim, site):
    """Publish a sim page with the banner and a way back, source untouched."""
    out = os.path.join(site, "sims", sim_id, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    chrome = SIM_CHROME.format(banner=html.escape(BANNER_MAIN),
                               logo=png_data_uri(SIM_LOGO),
                               home=up(2), sims=up(1))
    text, count = BODY_TAG.subn(lambda m: m.group(1) + "\n" + chrome,
                                sim["text"], count=1)
    if count != 1:
        raise SystemExit("no <body> tag in " + sim["path"])
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return out


def sims_index_markdown(found):
    """The sims page. It says what each sim is and claims nothing else.

    In particular it does not say which lab a sim serves: nothing in the
    original materials states that, and inventing it is not an option.
    """
    e = html.escape
    parts = ["# Sims\n",
             "Small tools students use during a lab. Each one is a single "
             "page that runs in the browser, keeps nothing, and sends "
             "nothing. Which lab each sim belongs to is not recorded here "
             "yet.\n"]
    items = []
    for sim_id, sim in found.items():
        items.append(
            '<li class="converted">\n'
            '<p class="lab-title"><a href="{}/">{}</a></p>\n'
            '<p class="lab-state">Runs in the browser. Nothing is stored and '
            "nothing is sent.</p>\n</li>".format(e(sim_id), e(sim["title"])))
    parts.append('<ul class="lab-list">\n' + "\n".join(items) + "\n</ul>\n")
    return "\n".join(parts)
