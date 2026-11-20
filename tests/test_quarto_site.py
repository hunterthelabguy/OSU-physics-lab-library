"""Checks on the Quarto build (build/quarto-site/), migration phase 1 (D-0033).

A missing build is an error, never a skip (LEDGER 53). The chrome suite,
test_site_chrome.py, is phase 2's contract and is not asserted here.
"""

import html
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QSITE = ROOT / "build" / "quarto-site"
PANDOC = os.environ.get("PANDOC", "pandoc")
FILTER = ROOT / "tools" / "filters" / "questions.lua"
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "tools"))
import test_site_chrome as chrome         # noqa: E402  (for SimBar.BAR only)
import render                             # noqa: E402
import test_lab_handbook                  # noqa: E402  (ADDRESSES)


def setUpModule():
    if not QSITE.is_dir():
        raise RuntimeError("build/quarto-site is missing: run tools/quarto_build.py first")


def converted():
    """(id, path) of every converted curriculum document."""
    for p in sorted((ROOT / "curriculum").rglob("*.md")):
        text = p.read_text(encoding="utf-8")
        if text.startswith("---") and re.search(r"^source_file:", text, re.M):
            yield re.search(r"^id:\s*(\S+)", text, re.M).group(1), p


def question_numbers(source_text):
    """The number each question block shows, in order, as
    tools/filters/questions.lua counts them: from 1, again from 1 at a
    `.restart` (S9). Checkpoints are counted apart and are not here."""
    numbers, n = [], 0
    for classes in re.findall(r"^:::+ *\{([^}]*)\}", source_text, re.M):
        names = re.findall(r"\.([\w-]+)", classes)
        if "question" not in names:
            continue
        n = 1 if "restart" in names else n + 1
        numbers.append(n)
    return numbers


def split_figures(fragment):
    """(the markup without its inline drawn figures, [each figure's
    markup]), a figure's nested <svg> included. The word check reads a
    figure's words from the original (D-0117)."""
    out, found, i = [], [], 0
    opener = re.compile(r'<svg\b[^>]*class="drawn-figure"')
    while True:
        m = opener.search(fragment, i)
        if m is None:
            return "".join(out) + fragment[i:], found
        out.append(fragment[i:m.start()] + " ")
        depth = 0
        for tag in re.finditer(r"<(/?)svg\b[^>]*>", fragment[m.start():]):
            depth += -1 if tag.group(1) else 1
            if depth == 0:
                i = m.start() + tag.end()
                break
        else:
            raise ValueError("an unclosed drawn figure")
        found.append(fragment[m.start():i])


def is_redirect(text):
    return 'http-equiv="refresh"' in text


def is_sim(rel):
    return re.fullmatch(r"sims/[^/]+/index\.html", rel) is not None


def html_pages():
    for p in sorted(QSITE.rglob("*.html")):
        rel = p.relative_to(QSITE).as_posix()
        if rel.startswith("site_libs/"):
            continue
        yield rel, p, p.read_text(encoding="utf-8")


def words(fragment):
    fragment = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", fragment)).split()


class Pages(unittest.TestCase):

    def test_expected_pages(self):
        want = ["index.html", "404.html", "courses/index.html",
                "how-this-site-works/index.html", "sims/index.html"]
        # One page per course in site/courses.md (D-0069).
        want += ["courses/{}/index.html".format(render.course_slug(c))
                 for c in render.courses_meta()["courses"]]
        for doc_id, _ in converted():
            want += [f"labs/{doc_id}/modern/index.html"]
        for rel in want:
            with self.subTest(page=rel):
                self.assertTrue((QSITE / rel).is_file())


    def test_functions_grouped_with_their_brackets(self):
        # D-0181: no function's name sits in an mrow of its own before a
        # bracket, on a lab page or its HTML download; the two that had one
        # (PH 212 Lab 6's cosine, PH 213 Data Analysis's sine) are grouped.
        apply = "(?:\u2061|&#8289;|&#x2061;)"
        apart = re.compile(r'<mrow><mi[^>]*>[^<]+</mi><mo>' + apply + r'</mo></mrow>'
                           r'(?:<mrow>)?<mo[^>]*>\(</mo>')
        for doc_id, _ in converted():
            for rel in (f"labs/{doc_id}/modern/index.html", f"labs/{doc_id}/{doc_id}.html"):
                with self.subTest(page=rel):
                    self.assertIsNone(apart.search((QSITE / rel).read_text(encoding="utf-8")))
        for doc_id, name in (("ph212-capstone-handout", "cos"), ("ph213-data-analysis-handout", "sin")):
            for rel in (f"labs/{doc_id}/modern/index.html", f"labs/{doc_id}/{doc_id}.html"):
                with self.subTest(grouped=rel):
                    self.assertRegex((QSITE / rel).read_text(encoding="utf-8"),
                                     '<mi mathvariant="normal">' + name + '</mi><mo>' + apply
                                     + '</mo><mrow><mo')

    def test_course_index_links_course_wide_documents(self):
        # D-0160: under their own heading, each to its modern page.
        shared = render.course_wide(render.converted_documents())
        self.assertTrue(shared)
        # Quarto wraps a link's text, so whitespace is compared collapsed.
        page = " ".join((QSITE / "courses" / "index.html").read_text(encoding="utf-8").split())
        self.assertIn(render.COURSE_WIDE_HEADING + "</h2>", page)
        for doc_id, doc in shared:
            with self.subTest(doc=doc_id):
                self.assertIn('href="../labs/{}/modern/">{}</a>'.format(
                    doc_id, doc["meta"]["title"]), page)

    def test_404_page_resolves_links_from_the_root(self):
        # Pages serves 404.html at whatever path was asked for, so the
        # chrome's relative nav links need a base (D-0049).
        text = (QSITE / "404.html").read_text(encoding="utf-8")
        self.assertEqual(text.count("<base "), 1)
        head = text.split("</head>", 1)[0]
        self.assertIn('<base href="/">', head)
        self.assertLess(head.index("<base "), head.index("<link "))

    def test_noindex_on_every_page(self):
        for rel, _, text in html_pages():
            if is_sim(rel):
                continue
            with self.subTest(page=rel):
                self.assertIn('<meta name="robots" content="noindex', text)

    def test_no_draft_banner_on_any_page(self):
        # D-0156: no page, redirect stub or sim carries the banner or says
        # the license is pending.
        for rel, _, text in html_pages():
            with self.subTest(page=rel):
                self.assertNotIn("draft-banner", text)
                self.assertNotIn("lib-draft", text)
                self.assertNotIn("license pending", " ".join(text.split()).lower())

    def test_one_h1_per_page(self):
        for rel, _, text in html_pages():
            if is_sim(rel) or is_redirect(text):
                continue
            with self.subTest(page=rel):
                self.assertEqual(len(re.findall(r"<h1\b", text)), 1)

    def test_source_front_matter_not_rendered(self):
        for rel, _, text in html_pages():
            with self.subTest(page=rel):
                self.assertNotIn("source_sha256", text)

    def test_stylesheets_resolve(self):
        for rel, path, text in html_pages():
            # Every <link> tag, whatever order its attributes come in: Quarto
            # writes its own as href-then-rel and ours as rel-then-href.
            for tag in re.findall(r"<link\b[^>]*>", text):
                found = re.search(r'href="([^"]+)"', tag)
                if 'rel="stylesheet"' not in tag or not found:
                    continue
                href = found.group(1)
                if href.startswith("data:"):
                    continue
                # Quarto writes a 404 page's links from the site root.
                base = QSITE if href.startswith("/") else path.parent
                with self.subTest(page=rel, href=href):
                    self.assertTrue((base / href.split("?")[0].lstrip("/")).resolve().is_file())


class LabHandbook(unittest.TestCase):
    """D-0188, D-0190: the handbook page and its fixed addresses."""

    ADDRESSES = test_lab_handbook.ADDRESSES   # one list (spec 4.3)

    def page(self):
        return (QSITE / "labs" / "ph21x-lab-handbook" / "modern" / "index.html").read_text(encoding="utf-8")

    def test_addresses_on_its_sections(self):
        found = re.findall(r'<h2[^>]*\bid="([^"]+)"', self.page())
        self.assertEqual(found, self.ADDRESSES)

    def test_titled_lab_handbook_with_contents_links(self):
        page = self.page()
        self.assertRegex(page, r"<h1[^>]*>Lab Handbook</h1>")
        for address in self.ADDRESSES:
            self.assertIn('href="#' + address + '"', page)


class NoThirdParty(unittest.TestCase):
    """D-0033: no theme or setting that loads a third-party resource."""

    TAG = re.compile(r'<(?:script|link|img|iframe)\b[^>]*(?:src|href)="(?:https?:)?//', re.I)
    CSS = re.compile(r'(?:@import\s*(?:url\()?|url\()\s*["\']?(?:https?:)?//', re.I)

    def test_pages(self):
        for rel, _, text in html_pages():
            with self.subTest(page=rel):
                self.assertIsNone(self.TAG.search(text))

    def test_stylesheets(self):
        for css in QSITE.rglob("*.css"):
            with self.subTest(css=css.relative_to(QSITE).as_posix()):
                self.assertIsNone(self.CSS.search(css.read_text(encoding="utf-8")))


class Documents(unittest.TestCase):
    """LEDGER 28 and the question filter, as Quarto renders them."""

    def reference_words(self, source, theme):
        # Read as the build reads (D-0118), its math as MathML (D-0040).
        out = subprocess.run(
            [PANDOC, str(source), "-f", render.FROM, "-t", "html", "--mathml",
             "--lua-filter", str(FILTER), "-M", "theme-name=" + theme],
            check=True, capture_output=True, text=True, encoding="utf-8").stdout
        return words(out)

    def test_words_match_a_plain_pandoc_render(self):
        # The document's words, in order, appear unbroken inside Quarto's
        # <main>; a drawn figure's are the word check's (D-0117).
        for doc_id, source in converted():
            for theme in ("modern",):
                with self.subTest(doc=doc_id, theme=theme):
                    page = (QSITE / "labs" / doc_id / theme / "index.html").read_text(encoding="utf-8")
                    main, _ = split_figures(re.search(r"<main\b.*?</main>", page, re.S).group(0))
                    want = "\x00".join(self.reference_words(source, theme))
                    self.assertIn(want, "\x00".join(words(main)))

    def test_questions_numbered(self):
        # In order, as the source counts them; a `.restart` starts again
        # at 1 (S9, D-0112).
        shared = {doc_id for doc_id, _ in render.course_wide(render.converted_documents())}
        for doc_id, source in converted():
            want = question_numbers(source.read_text(encoding="utf-8"))
            # A course-wide document is no lab and may have none (D-0160).
            self.assertTrue(want or doc_id in shared)
            modern = (QSITE / "labs" / doc_id / "modern" / "index.html").read_text(encoding="utf-8")
            with self.subTest(doc=doc_id):
                self.assertEqual([int(k) for k in re.findall(r"Question (\d+)<", modern)], want)


class Helpers(unittest.TestCase):
    """The helpers above, on made-up markup."""

    def test_question_numbers_restart(self):
        text = ("::: {.question #a}\nA\n:::\n\n::: {.checkpoint #c}\nC\n:::\n\n"
                "::: {.question #b}\nB\n:::\n\n:::: {.question .restart #d}\nD\n::::\n\n"
                "::: action\n- x\n:::\n\n::: {.question #e}\nE\n:::\n")
        self.assertEqual(question_numbers(text), [1, 2, 1, 2])

    def test_split_figures_takes_only_drawn_figures(self):
        page = ('<p>Before</p><svg class="drawn-figure" viewbox="0 0 1 1"><svg class="figure-picture">'
                '<image></image></svg><text>Label</text></svg><p>After</p>'
                '<svg class="other"><text>Kept</text></svg>')
        rest, figures = split_figures(page)
        self.assertEqual(words(rest), ["Before", "After", "Kept"])
        self.assertEqual([words(f) for f in figures], [["Label"]])


class SimsAndStubs(unittest.TestCase):
    """LEDGER 51 (sims), LEDGER 37 (robots), and the trimmed-URL stubs."""

    def test_sim_is_source_plus_bar_only(self):
        for src in sorted((ROOT / "sims").glob("*/index.html")):
            with self.subTest(sim=src.parent.name):
                pub = (QSITE / "sims" / src.parent.name / "index.html").read_text(encoding="utf-8")
                m = chrome.SimBar.BAR.search(pub)
                self.assertIsNotNone(m, "no bar after <body>")
                self.assertEqual(pub.replace(m.group(1), "", 1), src.read_text(encoding="utf-8"))

    def test_robots_disallows_everything(self):
        text = (QSITE / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("User-agent: *\nDisallow: /\n", text)
        self.assertIn("# Shared by link, not indexed (D-0156).\n", text)
        self.assertNotIn("Sitemap", text)

    def test_faithful_address_redirects_to_modern(self):
        # D-0108: the faithful page is retired; its address lands on modern,
        # and no lab page is built in its place.
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                text = (QSITE / "labs" / doc_id / "faithful" / "index.html").read_text(encoding="utf-8")
                self.assertTrue(is_redirect(text))
                self.assertIn("url=../modern/", text)
                self.assertNotIn("<main", text)
        self.assertFalse((ROOT / "themes" / "faithful.css").exists())
        self.assertFalse((QSITE / "themes" / "faithful.css").exists())

    def test_old_method_address_redirects(self):
        # D-0072: /how-this-was-made/ became /how-this-site-works/.
        text = (QSITE / "how-this-was-made" / "index.html").read_text(encoding="utf-8")
        self.assertTrue(is_redirect(text))
        self.assertIn("url=../how-this-site-works/", text)
        self.assertIn(">Continue to How this site works</a>", text)

    def test_method_page_from_its_own_source(self):
        # D-0072: the page is site/how-this-site-works.md, not a VISION.md lift.
        main = re.search(r"<main id=\"content\">(.*?)</main>",
                         (QSITE / "how-this-site-works" / "index.html").read_text(encoding="utf-8"),
                         re.S).group(1)
        source = (ROOT / "site" / "how-this-site-works.md").read_text(encoding="utf-8")
        for heading in re.findall(r"^##? (.+)$", source, re.M):
            with self.subTest(heading=heading):
                self.assertIn(heading, " ".join(html.unescape(main).split()))
        self.assertIn("Claude, an AI model from Anthropic", " ".join(words(main)))
        self.assertNotIn("Wispr", main)

    def test_trimmed_lab_url_redirects_to_modern(self):
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                text = (QSITE / "labs" / doc_id / "index.html").read_text(encoding="utf-8")
                self.assertTrue(is_redirect(text))
                self.assertIn('url=modern/', text)


if __name__ == "__main__":
    unittest.main()
