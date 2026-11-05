"""Shared functions for the Quarto build (D-0061).

Once the old build's entry point, this is now a module with no command line:
tools/quarto_build.py, tools/quarto_chrome.py, tools/downloads.py and
tools/make_reference_docx.py import it. It holds the
presentation notes and footnotes, the document nav's metadata, the course
index and the course pages, the "How this site works" page's footnote,
the sims and their bar, and the redirect stubs.

One presentation, modern, renders the Markdown source (D-0108, amending
ledger 28): it drops the original Word page settings and follows
docs/presentation-evidence.md. The faithful presentation was retired, its
address redirecting. Nothing is ever copied into a second file.
Output is plain static files with relative links, so any host serves them
(ledger 39). Every page asks search engines not to index the site (ledger 37);
no page carries a draft banner (D-0156).

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
THEMES = ("modern",)
# How every step reads a source: no smart quotes, so words match the
# originals, and no implicit figures, so a lone picture is not given its alt
# text as a visible caption Word does not have (D-0118). _quarto.yml's
# `from` and tools/check_unchanged.py's FROM say the same (tested).
FROM = "markdown-smart-implicit_figures"
# The library's address, the one place it is written for content (D-0165):
# a link to a lab's own file (front matter `files:`) points here in every
# output, so a saved Word, HTML or PDF download still reaches it. A move to
# another host changes this line.
LIBRARY_URL = "https://osu-physics-labs.pages.dev/"

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

THEME_NOTE = {
    "modern": (
        "This page drops the Word page settings and sets typography from the "
        "reading research and WCAG 2.2 SC 1.4.8. The words are the original "
        "authors', unchanged; graded questions are marked by a labeled block "
        "rather than by bold."
    ),
}

# The footnote on the "How this site works" page (D-0072). The landing
# page's footnote named the old build and was not carried (D-0038).
METHOD_FOOTNOTE = ("This page's source is site/how-this-site-works.md in the "
                   "project's repository; ledger numbers refer to the dated "
                   "decision ledger kept there.")
# Its address; the old one, /how-this-was-made/, redirects here.
METHOD_PATH = "how-this-site-works/"


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def pandoc_meta(md_path):
    """Front matter as plain data, read by Pandoc so YAML needs no library.

    The HTML writer escapes each value ("&" becomes "&amp;"), and every
    caller escapes what it writes, so the values are unescaped here once:
    a PH 212 title, "Sharing & Comparing", showed as "&amp;" (2026-10-07).
    """
    out = subprocess.run(
        [PANDOC, md_path, "-f", FROM, "-t", "html",
         "--template", os.path.join(ROOT, "tools", "meta.template")],
        check=True, capture_output=True, text=True, encoding="utf-8",
    ).stdout
    return plain_text(json.loads(out))


def plain_text(value):
    """Every string in a JSON value, HTML character references resolved."""
    if isinstance(value, str):
        return html.unescape(value)
    if isinstance(value, list):
        return [plain_text(v) for v in value]
    if isinstance(value, dict):
        return {k: plain_text(v) for k, v in value.items()}
    return value


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
    """The document nav's metadata: the course index link."""
    return [
        "-M", "uphref=" + up(depth) + "courses/",
        "-M", "uplabel=Course index",
    ]


def site_vars(depth):
    r = up(depth)
    return [
        "-M", "homehref=" + (r or "./"),
        "-M", "indexhref=" + r + "courses/",
        "-M", "methodhref=" + r + METHOD_PATH,
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


# The course download (D-0067, amended by D-0071): D-0053's names for the
# four formats, in the order of the lab page's download row, each with its
# published file's extension.
DOWNLOAD_FORMATS = (("docx", "Word"), ("html", "HTML"), ("pdf", "PDF"), ("md", "Markdown"))
# Claude's words, for the owner's approval (D-0071): the button and the
# dialog's title name the course and say files; the note says what the zip
# holds; the formats are grouped as the handouts they apply to.
DOWNLOAD_LABEL = "Download {} files"
DOWNLOAD_NOTE = "One zip, a folder per lab. Only converted labs are included."
DOWNLOAD_HANDOUTS = "Handouts"
# The control is hidden under this many files (the owner's "6 hide").
DOWNLOAD_MIN_FILES = 2


def downloadable_files(course, docs):
    """The files a course's download offers, as D-0071's rule counts them.

    Each format of each converted lab's handout is a file, so one handout
    in four formats is four (the owner, 2026-10-06: "Four files"), and a
    course with a converted lab always shows the control. A lab's data files
    and simulations would count one each, but no way to attach them to a lab
    is designed, so none is counted or listed.
    """
    return len(converted_labs(course, docs)) * len(DOWNLOAD_FORMATS)


def download_all(course, docs, depth):
    """The course download control (HTML), or "" under two files.

    A quiet button beside the course page's h1, "Download PH 211 files",
    opens a dialog with the same title, a note, the four formats as
    checkboxes under "Handouts", none ticked, and "Download selected" and
    "Close" (D-0067 as amended by D-0071). Each checkbox carries its
    format's published files for the course's converted labs, written here
    from the converted documents, never typed; site/download-all.js zips the
    ticked ones in the page as <slug>.zip (ph211.zip), a folder per lab. The
    button is hidden until the script runs, so a page without the script
    shows no dead control; "Close" closes the dialog without it.
    """
    if downloadable_files(course, docs) < DOWNLOAD_MIN_FILES:
        return ""
    ids = [lab["document"] for lab in converted_labs(course, docs)]
    e = html.escape
    boxes = []
    for ext, name in DOWNLOAD_FORMATS:
        paths = ["labs/{0}/{0}.{1}".format(doc_id, ext) for doc_id in ids]
        if ext == "md":
            # A Markdown file names its pictures and figures by relative
            # path, so they travel with it (four-items call 4.3).
            paths += ["labs/{0}/{0}-media/{1}".format(doc_id, f)
                      for doc_id in ids for f in docs[doc_id].get("published", [])]
        files = " ".join(up(depth) + p for p in paths)
        boxes.append('<label><input type="checkbox" value="{}" data-files="{}">'
                     ' {}</label>'.format(ext, e(files), e(name)))
    return (
        '<button type="button" class="download-all-open" aria-haspopup="dialog" hidden>'
        "{label}</button>\n"
        '<dialog class="download-all" data-zip="{zip}" aria-labelledby="{title}">\n'
        '<h2 id="{title}">{label}</h2>\n'
        '<p class="download-all-note">{note}</p>\n'
        "<fieldset>\n<legend>{handouts}</legend>\n"
        '<div class="download-all-formats">\n{boxes}\n</div>\n</fieldset>\n'
        '<div class="download-all-actions">\n'
        '<button type="button" class="download-selected" disabled>Download selected</button>\n'
        '<form method="dialog"><button class="download-all-close">Close</button></form>\n'
        "</div>\n</dialog>").format(
            label=e(DOWNLOAD_LABEL.format(course["code"])),
            zip=e(course_slug(course) + ".zip"), title="download-" + course_slug(course),
            note=e(DOWNLOAD_NOTE), handouts=e(DOWNLOAD_HANDOUTS), boxes="\n".join(boxes))


def course_index_markdown(meta, docs):
    """The course index (D-0069): the chooser, one tile per course."""
    return "\n".join(["# Course index\n", COURSE_INDEX_INTRO + "\n",
                      raw_html(course_tiles(meta["courses"], docs))])


def course_page_markdown(course, docs, depth=2):
    """One course's page (D-0069 to D-0071): a heading row of its h1 and the
    course download, the intro from site/courses.md, its converted labs as
    one table, and before launch the labs not yet converted, collapsed. A
    course with no labs shows its note instead of the intro."""
    e = html.escape
    labs = course.get("labs") or []
    control = download_all(course, docs, depth)
    # The heading row is a fenced div, which Quarto writes as a <section>
    # holding the h1 and taking its id. A raw <div> before the "#" heading
    # does not work: Quarto then lifts the h1 into its title block, past
    # the empty partial (probed 2026-10-06).
    head = "::: {.course-head}\n# " + course_heading(course) + "\n"
    if control:
        head += "\n" + raw_html(control)
    parts = [head + ":::\n"]
    if labs:
        parts.append(body_after_front_matter(os.path.join(ROOT, "site", "courses.md")))
    if course.get("note"):
        parts.append('<p class="course-note">{}</p>\n'.format(e(course["note"])))
    done = converted_labs(course, docs)
    if done:
        parts.append(raw_html(lab_table(done, docs, depth)))
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


def redirect_page(out, target, label="Continue to the lab"):
    """A plain meta-refresh stub, so a trimmed or old URL still lands somewhere."""
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(
            '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
            '<meta charset="utf-8">\n'
            '<meta name="robots" content="noindex, nofollow">\n'
            '<meta http-equiv="refresh" content="0; url={0}">\n'
            "<title>Redirecting</title>\n</head>\n<body>\n"
            '<p><a href="{0}">{1}</a>.</p>\n'
            "</body>\n</html>\n".format(target, html.escape(label)))
    return out


# A sim ships as one self-contained page that must keep working offline from
# disk, so the site chrome is injected into the copy that is published and the
# source file is never touched. It has to be small: the sim's layout is ruled
# to fit a 1280x720 laptop without page scrolling, and every pixel here is
# taken from that budget. So it carries the logo and two links and nothing
# more (no draft sentence since D-0156). The bar is Paddletail Black with the
# O over W logo (D-0005, D-0020). The sim's own Content Security Policy is `default-src 'none'`
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
.lib-bar a {{ color: #fff; }}
.lib-bar .lib-links {{ display: flex; gap: 1rem; margin-left: auto; }}
@media print {{ .lib-bar {{ display: none; }} }}
</style>
<div class="lib-bar">
<a href="https://oregonstate.edu"><img src="{logo}" alt="Oregon State University"></a>
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
    """Publish a sim page with a way back, source untouched."""
    out = os.path.join(site, "sims", sim_id, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    chrome = SIM_CHROME.format(logo=png_data_uri(SIM_LOGO),
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
