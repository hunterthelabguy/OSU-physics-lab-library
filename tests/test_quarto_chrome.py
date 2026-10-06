"""The chrome on the Quarto build (D-0036 to D-0039, D-0042, D-0061).

Reads build/quarto-site/. A missing build is an error, never a skip
(LEDGER 53).
"""

import functools
import html
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "tools"))
from test_quarto_site import converted    # noqa: E402
import render                             # noqa: E402
QSITE = ROOT / "build" / "quarto-site"


def setUpModule():
    if not QSITE.is_dir():
        raise RuntimeError("{} is missing: run tools/quarto_build.py first".format(QSITE))


def chrome_pages():
    """Quarto pages that carry the full chrome: not redirect stubs, not sims."""
    for p in sorted(QSITE.rglob("index.html")):
        rel = p.relative_to(QSITE).as_posix()
        text = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text or re.fullmatch(r"sims/[^/]+/index\.html", rel):
            continue
        yield rel, text


class Navigation(unittest.TestCase):
    """D-0037: one nav, no search."""

    def test_no_quarto_navbar_or_search(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                self.assertNotIn('id="quarto-header"', text)
                self.assertNotIn("quarto-search", text)

    def test_no_search_index(self):
        self.assertFalse((QSITE / "search.json").exists())

    def test_one_osu_nav(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                self.assertEqual(text.count('<nav class="osu-nav"'), 1)


def template(name):
    return (ROOT / "tools" / name).read_text(encoding="utf-8")


def from_template(name, pattern):
    """The one match of pattern in a template: the words come from there."""
    found = re.findall(pattern, template(name), re.S)
    if len(found) != 1:
        raise AssertionError("{}: expected one match of {!r}, found {}".format(name, pattern, len(found)))
    return found[0]


def meta(args):
    """{key: value} of render.py's -M arguments."""
    return dict(a.split("=", 1) for a in args[1::2])


def lab_theme(rel):
    """The theme of a lab page's path, or None for a site page."""
    m = re.fullmatch(r"labs/[^/]+/([^/]+)/index\.html", rel)
    return m.group(1) if m else None


def one_line(text):
    return " ".join(text.split())


@functools.lru_cache(maxsize=None)
def courses():
    """site/courses.md's courses, in order, and the converted documents."""
    return tuple(render.courses_meta()["courses"]), render.converted_documents()


def course_page_paths():
    return ["courses/{}/index.html".format(render.course_slug(c)) for c in courses()[0]]


def course_page(course):
    return (QSITE / "courses" / render.course_slug(course) / "index.html").read_text(encoding="utf-8")


def main_of(text):
    return re.search(r"<main>(.*?)</main>", text, re.S).group(1)


def text_of(fragment):
    return one_line(html.unescape(re.sub(r"<[^>]+>", " ", fragment)))


class ChromePieces(unittest.TestCase):
    """D-0038, D-0061: each piece of chrome pinned by its words.

    Replaced ChromeParity's comparisons with the old build. Every expected
    string is read from tools/render.py or the templates, never retyped, so
    a dress that drops or alters a piece fails. Whitespace is compared as
    single spaces, because the templates break the paragraph across lines.
    """

    def pages(self):
        pages = list(chrome_pages())
        labs = [rel for rel, _ in pages if lab_theme(rel)]
        self.assertEqual(len(labs), 2 * len(list(converted())), labs)
        self.assertEqual(sorted(rel for rel, _ in pages if not lab_theme(rel)),
                         sorted(["courses/index.html", "how-this-site-works/index.html",
                                 "index.html", "sims/index.html"] + course_page_paths()))
        return pages

    def test_body_class(self):
        # site/site.css scopes its rules to body.site-page and the themes to
        # body.theme-<name>; the dress puts the template's class first.
        site = from_template("template-site.html", r'<body class="([^"$]+)">')
        doc = from_template("template.html", r'<body class="([^"]+)">')
        for rel, text in self.pages():
            theme = lab_theme(rel)
            want = doc.replace("$theme$", theme) if theme else site
            with self.subTest(page=rel):
                classes = re.search(r'<body class="([^"]*)">', text).group(1).split()
                self.assertEqual(classes[0], want)
                self.assertGreater(len(classes), 1, "Quarto's own classes are kept")

    def test_document_nav(self):
        home = from_template("template.html", r'<a href="\$homehref\$">([^<$]+)</a>')
        for rel, text in self.pages():
            theme = lab_theme(rel)
            if not theme:
                continue
            m = meta(render.document_extras(theme))
            nav = re.findall(r'<nav class="site-nav">.*?</nav>', text, re.S)
            with self.subTest(page=rel):
                self.assertEqual(len(nav), 1)
                links = [(html.unescape(a), one_line(html.unescape(t)))
                         for a, t in re.findall(r"<a ([^>]*)>(.*?)</a>", nav[0], re.S)]
                for piece in (('href="{}"'.format(render.up(3)), home),
                              ('href="{}"'.format(m["uphref"]), m["uplabel"]),
                              ('class="switch" href="{}"'.format(m["switchhref"]), m["switchlabel"])):
                    self.assertEqual(links.count(piece), 1, (piece, links))

    def test_no_document_nav_on_site_pages(self):
        for rel, text in self.pages():
            if not lab_theme(rel):
                with self.subTest(page=rel):
                    self.assertNotIn('<nav class="site-nav">', text)

    def test_presentation_note_and_both_presentations(self):
        both = from_template(
            "template.html",
            r'<footer class="doc-footer">\n<p>\$presentationnote\$</p>\n'
            r'\$if\(homehref\)\$\n<p>([^<$]+)</p>\n\$endif\$\n</footer>')
        for rel, text in self.pages():
            theme = lab_theme(rel)
            footer = re.findall(r'<footer class="doc-footer">\n(.*?)</footer>', text, re.S)
            with self.subTest(page=rel):
                if not theme:
                    self.assertEqual(footer, [])
                    continue
                self.assertEqual(len(footer), 1)
                paras = [one_line(html.unescape(p)) for p in re.findall(r"<p>(.*?)</p>", footer[0], re.S)]
                self.assertEqual(paras, [one_line(render.THEME_NOTE[theme]), one_line(both)])

    def test_method_footnote_only_on_its_page(self):
        shape = from_template(
            "template-site.html",
            r'(<div class="site-foot">\n<p class="print-hide">)\$footnote\$(</p>\n</div>)')
        for rel, text in self.pages():
            found = re.findall(re.escape(shape[0]) + "(.*?)" + re.escape(shape[1]), text, re.S)
            with self.subTest(page=rel):
                if rel == "how-this-site-works/index.html":
                    self.assertEqual([one_line(html.unescape(f)) for f in found],
                                     [one_line(render.METHOD_FOOTNOTE)])
                else:
                    self.assertNotIn('<div class="site-foot">', text)


    def test_landing_footnote_not_carried(self):
        # D-0038: it said the site is built with Pandoc and one build script.
        self.assertNotIn("one build script", (QSITE / "index.html").read_text(encoding="utf-8"))


def site_css():
    return re.sub(r"/\*.*?\*/", "", (ROOT / "site" / "site.css").read_text(encoding="utf-8"), flags=re.S)


def css_rules(selector, css=None):
    """Bodies of the innermost rules whose selector list names selector;
    an @media wrapper is skipped over, so its rules count too."""
    return [body for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", site_css() if css is None else css)
            if selector in [s.strip() for s in sel.split(",")]]


def media_css(query):
    """The rules inside every @media block with this query, as one text."""
    return "\n".join(re.findall(r"@media " + re.escape(query) + r"\s*\{((?:[^{}]*\{[^{}]*\})*[^{}]*)\}",
                                site_css()))


TABLE = re.compile(r'<table class="lab-table">.*?</table>', re.S)
PENDING = re.compile(r'<details class="lab-pending">\s*<summary>([^<]*)</summary>(.*?)</details>', re.S)


def cells(table):
    """[(lab cell, title cell, description cell)] of a lab table's body rows."""
    body = re.search(r"<tbody>(.*?)</tbody>", table, re.S).group(1)
    return re.findall(r'<tr><td class="lab-num">(.*?)</td><td class="lab-title">(.*?)</td>'
                      r'<td class="lab-desc">(.*?)</td></tr>', body, re.S)


class LabRows(unittest.TestCase):
    """D-0068 for the sims page's rows, D-0070 for a course page's table:
    Lab, Title, Description across the shell, no state line, nothing
    clipped; before launch the unconverted labs collapsed under it."""

    def test_sims_rows_one_column_at_every_width(self):
        self.assertNotIn("auto-fill", site_css())
        bodies = css_rules("body.site-page .lab-list")
        self.assertTrue(bodies)
        self.assertEqual([re.search(r"grid-template-columns:\s*([^;]+);", b).group(1).strip()
                          for b in bodies if "grid-template-columns" in b], ["minmax(0, 1fr)"])

    def test_sims_rows_on_the_reading_column(self):
        self.assertEqual(css_rules("body.site-page main > .lab-list"), [])
        # It must outrank `body.site-page ul`, or that rule indents the list.
        self.assertIn("padding: 0", "".join(css_rules("body.site-page .lab-list")))

    def test_descriptions_never_clipped(self):
        for selector in (".lab-desc", "body.site-page .lab-table .lab-desc", "body.site-page .lab-table td"):
            for word in ("line-clamp", "text-overflow", "max-height"):
                with self.subTest(selector=selector, word=word):
                    self.assertNotIn(word, "".join(css_rules(selector)))

    def test_table_spans_the_shell_description_takes_the_rest(self):
        self.assertIn("grid-column: full", "".join(css_rules("body.site-page main > .lab-table")))
        self.assertIn("table-layout: fixed", "".join(css_rules("body.site-page .lab-table")))
        self.assertIn("width: 5.5rem", "".join(css_rules("body.site-page .lab-table .lab-num")))
        self.assertIn("width: 18rem", "".join(css_rules("body.site-page .lab-table .lab-title")))
        self.assertEqual(css_rules("body.site-page .lab-table .lab-desc"), [])

    def test_rows_stack_below_48rem(self):
        # The title cell is reset by name: its 18rem (0,3,1) outranked the
        # cells' reset (0,2,2) and wrapped titles at 288 px (measured 2026-10-06).
        phone = media_css("(max-width: 48rem)")
        for selector in ("body.site-page .lab-table td", "body.site-page .lab-table .lab-title"):
            with self.subTest(selector=selector):
                rule = "".join(css_rules(selector, phone))
                self.assertIn("display: block", rule)
                self.assertIn("width: auto", rule)
        hidden = "".join(css_rules("body.site-page .lab-table .lab-num", phone))
        self.assertIn("display: none", hidden)
        self.assertIn("position: static", "".join(css_rules("body.site-page .lab-table .lab-prefix", phone)))

    def test_one_table_of_the_converted_labs(self):
        listed, docs = courses()
        for course in listed:
            done = render.converted_labs(course, docs)
            with self.subTest(course=course["code"]):
                outside = PENDING.sub("", main_of(course_page(course)))
                tables = TABLE.findall(outside)
                self.assertEqual(len(tables), 1 if done else 0)
                if not done:
                    continue
                self.assertEqual(re.findall(r'<th scope="col"[^>]*>([^<]*)</th>', tables[0]),
                                 ["Lab", "Title", "Description"])
                rows = cells(tables[0])
                self.assertEqual(len(rows), len(done))
                for (num, title, desc), lab in zip(rows, done):
                    href = "../../labs/{}/modern/".format(lab["document"])
                    name = ("Lab " + lab["number"] + ": " if lab.get("number") else "") + lab["title"]
                    self.assertEqual(text_of(num), "Lab " + lab["number"] if lab.get("number") else "")
                    self.assertRegex(title, r'^<a href="{}">'.format(re.escape(href)))
                    self.assertEqual(text_of(title), name, "the link reads Lab N: Title")
                    self.assertEqual(html.unescape(desc), lab["description"], "quoted whole")

    def test_no_state_line_and_no_converted_heading(self):
        for course in courses()[0]:
            with self.subTest(course=course["code"]):
                main = main_of(course_page(course))
                self.assertNotIn("lab-state", main)
                self.assertNotIn("Also available as it was written", main)
                self.assertNotRegex(main, r"<h[2-6][^>]*>\s*Converted")

    def test_unconverted_labs_collapsed_before_launch(self):
        listed, docs = courses()
        for course in listed:
            pending = [lab for lab in course.get("labs") or [] if lab.get("document") not in docs]
            found = PENDING.findall(main_of(course_page(course)))
            with self.subTest(course=course["code"]):
                self.assertEqual(len(found), 1 if pending else 0)
                if not pending:
                    continue
                summary, inside = found[0]
                self.assertEqual(summary, "Not yet converted ({})".format(len(pending)))
                self.assertNotIn("<a ", inside)
                self.assertEqual([html.unescape(d) for _, _, d in cells(TABLE.search(inside).group(0))],
                                 [lab["description"] for lab in pending])


class CoursePages(unittest.TestCase):
    """D-0069: one page per course, the course index as tiles that choose
    one, and course tabs under the site nav. Everything named here is read
    from site/courses.md, never typed."""

    def index(self):
        return main_of((QSITE / "courses" / "index.html").read_text(encoding="utf-8"))

    def test_one_page_per_course(self):
        found = sorted(p.relative_to(QSITE).as_posix() for p in (QSITE / "courses").glob("*/index.html"))
        self.assertEqual(found, sorted(course_page_paths()))
        self.assertEqual(len(found), len(courses()[0]))

    def test_index_chooses_with_one_tile_per_course(self):
        listed, docs = courses()
        tiles = re.findall(r'<a class="course-tile( converted)?" href="([^"]*)">(.*?)</a>', self.index(), re.S)
        self.assertEqual([href for _, href, _ in tiles], [render.course_slug(c) + "/" for c in listed])
        for (orange, _, inner), course in zip(tiles, listed):
            labs, done = course.get("labs") or [], render.converted_labs(course, docs)
            # The count, computed here from the data: none, all, or some.
            n = len(labs)
            count = ("No labs converted yet" if not done else
                     "{} lab{}".format(n, "" if n == 1 else "s") if len(done) == n else
                     "{} lab{} listed, {} converted".format(n, "" if n == 1 else "s", len(done)))
            spans = re.findall(r'<span class="course-tile-([a-z]+)">([^<]*)</span>', inner)
            with self.subTest(course=course["code"]):
                want = [("code", course["code"])]
                if course.get("name"):
                    want.append(("name", course["name"]))
                want.append(("count", count))
                self.assertEqual([(k, html.unescape(v)) for k, v in spans], want)
                self.assertEqual(bool(orange), bool(done))

    def test_no_name_typed_before_it_is_in_hand(self):
        # Q4 of the four-items plan: a course with no name shows its code alone.
        for course in courses()[0]:
            if course.get("name"):
                continue
            with self.subTest(course=course["code"]):
                h1 = re.search(r"<h1[^>]*>(.*?)</h1>", course_page(course), re.S).group(1)
                self.assertEqual(text_of(h1), course["code"])

    def test_heading_names_the_course(self):
        for course in courses()[0]:
            with self.subTest(course=course["code"]):
                h1 = re.search(r"<h1[^>]*>(.*?)</h1>", course_page(course), re.S).group(1)
                self.assertEqual(text_of(h1), render.course_heading(course))

    def test_no_popover_on_load(self):
        text = (QSITE / "courses" / "index.html").read_text(encoding="utf-8")
        for word in ("<dialog", "autofocus", "download-all.js", "popover"):
            with self.subTest(word=word):
                self.assertNotIn(word, text)

    def test_tabs_name_every_course_and_mark_the_current_one(self):
        listed = courses()[0]
        for course in listed:
            text = course_page(course)
            navs = re.findall(r'<nav class="course-tabs" aria-label="Courses">(.*?)</nav>', text, re.S)
            with self.subTest(course=course["code"]):
                self.assertEqual(len(navs), 1)
                # Under the site nav, before <main>.
                self.assertLess(text.index('<nav class="osu-nav"'), text.index('<nav class="course-tabs"'))
                self.assertLess(text.index('<nav class="course-tabs"'), text.index("<main>"))
                tabs = re.findall(r'<a href="([^"]*)"( aria-current="page")?>([^<]*)</a>', navs[0])
                self.assertEqual([(href, html.unescape(code)) for href, _, code in tabs],
                                 [("../{}/".format(render.course_slug(c)), c["code"]) for c in listed])
                self.assertEqual([code for _, current, code in tabs if current], [course["code"]])

    def test_tabs_only_on_course_pages(self):
        pages = set(course_page_paths())
        for rel, text in chrome_pages():
            if rel not in pages:
                with self.subTest(page=rel):
                    self.assertNotIn("course-tabs", text)

    def test_tabs_44px_tall(self):
        rule = "".join(css_rules(".course-tabs a"))
        self.assertIn("min-height: 44px", rule)
        self.assertIn("box-sizing: border-box", rule, "the orange rule counts inside the 44 px")

    def test_footnote_names_the_source_where_labs_are_listed(self):
        for course in courses()[0]:
            notes = re.findall(r'<p class="course-note">(.*?)</p>', main_of(course_page(course)), re.S)
            quoted = [n for n in notes if "are quoted from" in n]
            with self.subTest(course=course["code"]):
                if course.get("labs") and course.get("source_note"):
                    self.assertEqual(len(quoted), 1)
                    self.assertIn(course["source_note"], text_of(quoted[0]))
                    self.assertIn("for {} are".format(course["code"]), text_of(quoted[0]))
                else:
                    self.assertEqual(quoted, [])


class MainBare(unittest.TestCase):
    """D-0036: one bare <main>, no empty title block."""

    def test_main_is_bare(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                self.assertEqual(text.count("<main>"), 1)
                self.assertNotIn("<main ", text)
                self.assertNotIn("title-block-header", text)


class Published(unittest.TestCase):
    """D-0039 amended: the fonts, their license and the header logo go out."""

    def test_fonts_license_and_header_logo_only(self):
        names = sorted(p.name for p in (QSITE / "site" / "fonts").iterdir())
        self.assertEqual(names, ["OFL.txt", "OpenSans-Bold.woff2", "OpenSans-BoldItalic.woff2",
                                 "OpenSans-Italic.woff2", "OpenSans-Regular.woff2"])
        brand = sorted(p.name for p in (QSITE / "site" / "brand").iterdir())
        self.assertEqual(brand, ["OSU_horizontal_2C_W_over_B.png"])

    def test_only_markdown_downloads_published(self):
        # D-0053: each lab's source is a download; no other Markdown goes out.
        want = sorted("labs/{0}/{0}.md".format(doc_id) for doc_id, _ in converted())
        self.assertEqual(sorted(p.relative_to(QSITE).as_posix() for p in QSITE.rglob("*.md")), want)


class PageShell(unittest.TestCase):
    """What the quarto-only CSS in site/site.css depends on in the markup."""

    def test_one_content_opener_around_main(self):
        # Every selector in the block names #quarto-content; D-0036's dressing
        # anchors on the closing comment only, so the opener is guarded here.
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                self.assertEqual(text.count('<div id="quarto-content"'), 1)
                opener = text.index('<div id="quarto-content"')
                self.assertLess(opener, text.index("<main>"))
                self.assertLess(text.index("</main>"), text.index("</div> <!-- /content -->"))

    def test_load_order_bootstrap_site_theme(self):
        # The reverts in the block sit at Bootstrap's specificity and work by
        # coming after it; a bare-element rule above the block in site.css is
        # cancelled the same way. So site.css must load after Bootstrap and
        # before the document theme (docs/agent-reference.md, Measuring and keeping the measured match).
        for rel, text in chrome_pages():
            hrefs = re.findall(r'<link [^>]*href="([^"]+)"[^>]*rel="stylesheet"|'
                               r'<link [^>]*rel="stylesheet"[^>]*href="([^"]+)"', text)
            hrefs = [a or b for a, b in hrefs]
            idx = lambda pat: [i for i, h in enumerate(hrefs) if re.search(pat, h)]
            with self.subTest(page=rel):
                boot, site = idx(r"bootstrap/bootstrap-[0-9a-f]+\.min\.css"), idx(r"site/site\.css")
                self.assertEqual(len(boot), 1)
                self.assertEqual(len(site), 1)
                self.assertLess(boot[0], site[0])
                for theme in idx(r"themes/"):
                    self.assertLess(site[0], theme)


class QuartoOnlyCss(unittest.TestCase):
    """Rules added for Quarto must not reach the HTML download, which embeds
    site/site.css through tools/template.html without Quarto's markup
    (D-0054, D-0061)."""

    def test_block_present_and_scoped(self):
        css = (ROOT / "site" / "site.css").read_text(encoding="utf-8")
        m = re.search(r"/\* quarto-only: start \(D-0036\) \*/(.*?)/\* quarto-only: end \*/", css, re.S)
        self.assertIsNotNone(m, "no quarto-only block")
        body = re.sub(r"/\*.*?\*/", "", m.group(1), flags=re.S)
        selectors = [s.strip() for sel in re.findall(r"([^{}]+)\{", body) for s in sel.split(",")]
        self.assertTrue(selectors)
        for s in selectors:
            if s.startswith("@media"):
                continue
            with self.subTest(selector=s):
                self.assertTrue("#quarto-content" in s or ".quarto-light" in s)

    def block(self):
        css = (ROOT / "site" / "site.css").read_text(encoding="utf-8")
        return re.search(r"/\* quarto-only: start \(D-0036\) \*/(.*?)/\* quarto-only: end \*/", css, re.S).group(1)

    def test_load_order_is_noted_where_the_rules_live(self):
        self.assertIn("themes/*.css", self.block())
        self.assertIn("after", self.block())

    def test_dd_margins_reverted(self):
        # Measured 2026-10-01 against the old build: Bootstrap gives dd
        # margin-left 0 (browser default 40px) and margin-bottom .5rem.
        body = re.sub(r"/\*.*?\*/", "", self.block(), flags=re.S)
        m = re.search(r"dd\s*\{([^}]*)\}", body)
        self.assertIsNotNone(m, "no dd revert")
        self.assertIn("margin-left: revert", m.group(1))
        self.assertIn("margin-bottom: revert", m.group(1))

    def test_download_buttons(self):
        # D-0059: the landing hero's primary button (D-0031) at nav scale,
        # [44] px tall; measured 2026-10-01 on the mockups at 375 px.
        body = re.sub(r"/\*.*?\*/", "", self.block(), flags=re.S)
        m = re.search(r"\.quarto-light \.site-nav a\.download-button\s*\{([^}]*)\}", body)
        self.assertIsNotNone(m, "no download-button rule")
        for decl in ("min-height: 44px", "background: var(--chrome-accent)", "color: #fff", "font-weight: 700"):
            with self.subTest(decl=decl):
                self.assertIn(decl, m.group(1))


if __name__ == "__main__":
    unittest.main()
