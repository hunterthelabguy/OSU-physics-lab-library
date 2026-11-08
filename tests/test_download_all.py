"""The course download on each course page (D-0067, amended by D-0071).

Runs the node test beside site/download-all.js, has that script's own code
write a zip of a course's published files, reads the zip back with Python's
zipfile, and checks the control: its words, its group, its file list, its
CSS and its script, as render.download_all() writes it for a course with two
converted labs, and on the course pages Quarto built, where it shows only
with two files or more, four to a converted handout (D-0071). Needs
build/quarto-site/ and node; either missing is an error, never a skip
(LEDGER 53).
"""

import functools
import html
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import downloads                          # noqa: E402
import media                              # noqa: E402
import render                             # noqa: E402

QSITE = ROOT / "build" / "quarto-site"
SCRIPT = ROOT / "site" / "download-all.js"
NODE = shutil.which("node")
CSS_BLOCK = re.compile(r"/\* quarto-only: start \(D-0036\) \*/(.*?)/\* quarto-only: end \*/", re.S)

# Has download-all.js's own CORE write a zip of the given paths, each read
# from a folder; the same code the page runs, loaded as the node test does.
WRITER = r"""
const fs = require("fs"), path = require("path");
const [src, base, out, ...paths] = process.argv.slice(2);
const block = fs.readFileSync(src, "utf8").match(/\/\/ BEGIN CORE\n([\s\S]*?)\/\/ END CORE/)[1];
const core = new Function(block + "\nreturn { buildZip };")();
core.buildZip(paths, async (p) => new Uint8Array(fs.readFileSync(path.join(base, p))), new Date())
  .then((zip) => { if (zip) fs.writeFileSync(out, zip); })
  .catch((err) => { console.error(err); process.exit(1); });
"""

# A course with two converted labs, for the control's markup with more than
# one lab: no course on the built site has two yet. The ids are the test's
# own; only render.download_all() reads them.
TWO = {"code": "PH 211", "labs": [{"number": "1", "title": "First", "document": "lab-one"},
                                 {"number": "2", "title": "Second", "document": "lab-two"}]}
TWO_DOCS = {"lab-one": {}, "lab-two": {}}


def setUpModule():
    if not QSITE.is_dir():
        raise RuntimeError("{} is missing: run tools/quarto_build.py first".format(QSITE))
    if NODE is None:
        raise RuntimeError("node is not on PATH; the Download all tests need it")


@functools.lru_cache(maxsize=None)
def courses():
    """[(course, [converted lab ids])] in the order of site/courses.md."""
    docs = render.converted_documents()
    return tuple((c, [lab["document"] for lab in render.converted_labs(c, docs)])
                 for c in render.courses_meta()["courses"])


def page(code):
    """A course page's built file (D-0069)."""
    return QSITE / "courses" / "".join(code.split()).lower() / "index.html"


def published(ids, ext):
    """A course page's relative paths to its labs' published files of one format."""
    return ["../../labs/{0}/{0}.{1}".format(i, ext) for i in ids]


OPENER = re.compile(r'<button type="button" class="download-all-open"[^>]*>([^<]*)</button>')


def controls(text):
    """Each course download dialog in a page or a fragment."""
    return re.findall(r'<dialog class="download-all"[^>]*>.*?</dialog>', text, re.S)


def rules(selector):
    """Declarations of every quarto-only rule whose selector list names selector."""
    css = (ROOT / "site" / "site.css").read_text(encoding="utf-8")
    block = re.sub(r"/\*.*?\*/", "", CSS_BLOCK.search(css).group(1), flags=re.S)
    return " ".join(body for sel, body in re.findall(r"([^{}]+)\{([^}]*)\}", block)
                    if selector in [x.strip() for x in sel.split(",")])


def boxes(control):
    """[(value, [files], label, tag)] of each checkbox, in order."""
    return [(re.search(r'value="([^"]*)"', tag).group(1),
             html.unescape(re.search(r'data-files="([^"]*)"', tag).group(1)).split(),
             html.unescape(label).strip(), tag)
            for tag, label in re.findall(r"<label>(<input [^>]*>)([^<]*)</label>", control)]


def write_zip(paths, base, out):
    with tempfile.TemporaryDirectory() as d:
        writer = Path(d, "write-zip.cjs")
        writer.write_text(WRITER, encoding="utf-8")
        proc = subprocess.run([NODE, str(writer), str(SCRIPT), str(base), str(out), *paths],
                              capture_output=True, text=True)
    if proc.returncode != 0:
        raise AssertionError(proc.stderr)


class NodeTest(unittest.TestCase):

    def test_zip_writer_node_test_passes(self):
        proc = subprocess.run([NODE, "download-all.test.mjs"], cwd=ROOT / "site",
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertRegex(proc.stdout, r"\b[1-9]\d* passed, 0 failed")


class ZipReadBack(unittest.TestCase):
    """A zip the page's code writes of the files PH 211's built control
    lists, read by Python's zipfile, from the folder of PH 211's page."""

    def ids(self):
        return dict((c["code"], i) for c, i in courses())["PH 211"]

    def course_files(self):
        found = controls(page("PH 211").read_text(encoding="utf-8"))
        self.assertEqual(len(found), 1, "PH 211's page has no course download")
        return [(value, files) for value, files, _, _ in boxes(found[0])]

    def check_zip(self, paths):
        base = page("PH 211").parent
        with tempfile.TemporaryDirectory() as d:
            out = Path(d, "course.zip")
            write_zip(paths, base, out)
            with zipfile.ZipFile(out) as z:
                self.assertIsNone(z.testzip(), "a CRC-32 does not match")
                infos = z.infolist()
                # A lab's folder, its media inside it (D-0118 call 6).
                self.assertEqual([i.filename for i in infos],
                                 [p.split("/labs/", 1)[1] for p in paths])
                for info, path in zip(infos, paths):
                    want = (base / path).resolve().read_bytes()
                    with self.subTest(entry=info.filename):
                        self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
                        self.assertEqual(info.CRC, zlib.crc32(want))
                        self.assertEqual(z.read(info), want)

    def test_every_format_of_ph211(self):
        self.assertTrue(self.ids(), "PH 211 has no converted lab")
        paths = [p for _, files in self.course_files() for p in files]
        docs = render.converted_documents()
        media_files = ["../../labs/{0}/{0}-media/{1}".format(i, f)
                       for i in self.ids() for f in media.published(docs[i])]
        want = [p for ext, _ in render.DOWNLOAD_FORMATS for p in published(self.ids(), ext)
                + (media_files if ext == "md" else [])]
        self.assertEqual(paths, want)
        self.assertEqual(len(paths), len(downloads.EXTENSIONS) * len(self.ids()) + len(media_files))
        self.check_zip(paths)

    def test_one_format_only(self):
        self.check_zip(dict(self.course_files())["md"])

    def test_no_format_writes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d, "course.zip")
            write_zip([], page("PH 211").parent, out)
            self.assertFalse(out.exists())


class Control(unittest.TestCase):
    """render.download_all() for a course with two converted labs."""

    def control(self):
        found = controls(render.download_all(TWO, TWO_DOCS, 2))
        self.assertEqual(len(found), 1)
        return found[0]

    def test_hidden_under_two_files_four_to_a_handout(self):
        # D-0071: hidden under [2] files (the owner's "6 hide"), each format
        # of a converted handout a file (the owner's "Four files"), so one
        # converted lab already shows the control.
        self.assertEqual(render.DOWNLOAD_MIN_FILES, 2)
        one = {"code": "PH 211", "labs": TWO["labs"][:1]}
        self.assertEqual(render.downloadable_files(one, TWO_DOCS), 4)
        self.assertNotEqual(render.download_all(one, TWO_DOCS, 2), "")
        self.assertEqual(render.downloadable_files(TWO, TWO_DOCS), 8)
        unconverted = {"code": "PH 212", "labs": [{"number": "1", "title": "Not yet"}]}
        self.assertEqual(render.downloadable_files(unconverted, TWO_DOCS), 0)
        self.assertEqual(render.download_all(unconverted, TWO_DOCS, 2), "")
        self.assertEqual(render.download_all({"code": "PH 213", "labs": []}, TWO_DOCS, 2), "")

    def test_words(self):
        # D-0071: the button and the dialog's title name the course and say
        # files; the note; the group; the four names are the lab page's
        # download row's, read from the template; "Download selected"
        # (D-0067) and "Close" (Q8's lean).
        row = re.findall(r'<a class="download-button"[^>]*>([^<]+)</a>',
                         (ROOT / "tools" / "template.html").read_text(encoding="utf-8"))
        self.assertEqual(len(row), 4)
        fragment = render.download_all(TWO, TWO_DOCS, 2)
        control = self.control()
        self.assertEqual(OPENER.findall(fragment), ["Download PH 211 files"])
        title = re.search(r'aria-labelledby="([^"]+)"', control).group(1)
        self.assertEqual(re.findall(r'<h2 id="{}">([^<]*)</h2>'.format(re.escape(title)), control),
                         ["Download PH 211 files"])
        self.assertEqual(re.findall(r"<legend>([^<]*)</legend>", control), ["Handouts"])
        self.assertEqual([label for _, _, label, _ in boxes(control)], row)
        self.assertEqual(re.findall(r"<button [^>]*>([^<]*)</button>", control),
                         ["Download selected", "Close"])
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", control)).strip()
        self.assertEqual(text, " ".join(["Download PH 211 files",
                                         "One zip, a folder per lab.",  # D-0170
                                         "Handouts"] + row + ["Download selected", "Close"]))

    def test_no_lab_files_group_without_lab_files(self):
        # D-0071's "Lab files" group lists data files and simulations only
        # where a course has them; none can be attached to a lab yet.
        self.assertNotIn("Lab files", self.control())
        self.assertEqual(self.control().count("<fieldset>"), 1)

    def test_files_are_exactly_the_converted_labs_published_files(self):
        listed = boxes(self.control())
        self.assertEqual(sorted(v for v, _, _, _ in listed), sorted(downloads.EXTENSIONS))
        for value, files, _, _ in listed:
            self.assertEqual(files, published(["lab-one", "lab-two"], value))

    def test_markdown_carries_its_labs_media(self):
        # Four-items call 4.3: a zipped .md opens with its pictures, each in
        # its lab's media folder.
        docs = {"lab-one": {"published": ["a.png", "panel.svg"]}, "lab-two": {}}
        listed = {v: files for v, files, _, _ in boxes(controls(render.download_all(TWO, docs, 2))[0])}
        self.assertEqual(listed["md"], published(["lab-one", "lab-two"], "md")
                         + ["../../labs/lab-one/lab-one-media/a.png", "../../labs/lab-one/lab-one-media/panel.svg"])
        self.assertEqual(listed["docx"], published(["lab-one", "lab-two"], "docx"))

    def test_zip_named_by_course_code(self):
        self.assertIn('data-zip="ph211.zip"', self.control())

    def test_opt_in_and_hidden_until_the_script_runs(self):
        # Nothing ticked, so "Download selected" starts disabled; the opener
        # is hidden as built and shown by the script, never a dead button.
        control = self.control()
        for _, _, _, tag in boxes(control):
            self.assertNotRegex(tag, r"\bchecked\b")
        self.assertRegex(re.search(r'<button type="button" class="download-selected"[^>]*>', control).group(0),
                         r"\bdisabled\b")
        opener = re.search(r'<button type="button" class="download-all-open"[^>]*>',
                           render.download_all(TWO, TWO_DOCS, 2)).group(0)
        self.assertRegex(opener, r"\bhidden\b")
        self.assertIn('aria-haspopup="dialog"', opener)

    def test_close_needs_no_script(self):
        # A dialog-method form closes its dialog natively (four-items call 3.1).
        self.assertIn('<form method="dialog"><button class="download-all-close">Close</button></form>',
                      self.control())

    def test_in_the_heading_row(self):
        # D-0071: beside the h1, before the intro and the table.
        text = render.course_page_markdown(TWO, TWO_DOCS)
        head = re.match(r"::: \{\.course-head\}\n# (.*?)\n\n```\{=html\}\n(.*?)\n```\n:::\n", text, re.S)
        self.assertIsNotNone(head, text[:300])
        self.assertEqual(head.group(1), "PH 211")
        self.assertRegex(head.group(2), r'^<button type="button" class="download-all-open"[^>]*>[^<]*</button>\n'
                                        r'<dialog class="download-all"')

    def test_opener_is_quiet(self):
        # Less prominent than the lab pages' orange buttons, still one tap;
        # "Close" shares the look.
        for selector in (".quarto-light .download-all-open", ".quarto-light .download-all button.download-all-close"):
            decls = rules(selector)
            for decl in ("min-height: 44px", "background: transparent", "color: var(--chrome-quiet)",
                         "border: 1px solid var(--chrome-quiet)"):
                with self.subTest(selector=selector, decl=decl):
                    self.assertIn(decl, decls)
            self.assertNotIn("--chrome-accent", decls)
        self.assertIn("display: none", rules(".quarto-light .download-all-open[hidden]"))

    def test_download_selected_is_the_download_button(self):
        # D-0059's button: test_quarto_chrome.QuartoOnlyCss.test_download_buttons.
        decls = rules(".quarto-light .download-all button.download-selected")
        for decl in ("min-height: 44px", "background: var(--chrome-accent)", "color: #fff",
                     "font-weight: 700", "font-size: 1rem", "border-radius: 6px"):
            with self.subTest(decl=decl):
                self.assertIn(decl, decls)

    def test_legend_not_floated(self):
        # Bootstrap floats a legend at a large size; undone in the dialog.
        decls = rules(".quarto-light .download-all legend")
        self.assertIn("float: none", decls)
        self.assertIn("font-size: .85rem", decls)


def files_of(ids):
    """D-0071's count, made here: every format of each converted handout."""
    return len(ids) * len(downloads.EXTENSIONS)


def visible(fragment):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragment)).strip()


class BuiltPages(unittest.TestCase):
    """The course pages as built: the control only where a course has two
    files, written as render.download_all() writes it, in the heading row
    beside the h1."""

    def test_control_only_with_two_files(self):
        shown = 0
        for course, ids in courses():
            text = page(course["code"]).read_text(encoding="utf-8")
            want = 1 if files_of(ids) >= 2 else 0
            shown += want
            with self.subTest(course=course["code"]):
                self.assertEqual(len(controls(text)), want)
                self.assertEqual(len(OPENER.findall(text)), want)
        self.assertTrue(shown, "no course page carries the course download")

    def test_built_as_rendered(self):
        # Quarto rewrites boolean attributes (hidden="") but must not change
        # the boxes, their files, or a word.
        docs = render.converted_documents()
        for doc in docs.values():
            # What the build published beside each lab (tools/media.py).
            doc["published"] = media.published(doc)
        for course, ids in courses():
            if files_of(ids) < 2:
                continue
            built = page(course["code"]).read_text(encoding="utf-8")
            rendered = render.download_all(course, docs, 2)
            with self.subTest(course=course["code"]):
                self.assertEqual([b[:3] for b in boxes(controls(built)[0])],
                                 [b[:3] for b in boxes(controls(rendered)[0])])
                self.assertEqual(visible(controls(built)[0]), visible(controls(rendered)[0]))
                self.assertEqual(OPENER.findall(built), OPENER.findall(rendered))
                self.assertRegex(re.search(r'<button type="button" class="download-all-open"[^>]*>',
                                           built).group(0), r"\bhidden\b")

    def test_heading_row_holds_the_h1(self):
        # Quarto writes the fenced div as a <section> that takes the h1's id.
        for course, _ in courses():
            main = re.search(r"<main id=\"content\">(.*?)</main>", page(course["code"]).read_text(encoding="utf-8"), re.S).group(1)
            with self.subTest(course=course["code"]):
                self.assertRegex(main.lstrip(), r'^<section id="[^"]+" class="course-head">\s*<h1>')


class Script(unittest.TestCase):

    def test_names_no_url_outside_the_site(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"[a-z][a-z0-9+.-]*://", text, re.I))
        self.assertIsNone(re.search(r"[\"'`]//", text))
        self.assertNotRegex(text, r"\bimport\b|\brequire\s*\(")

    def test_linked_once_from_each_course_page_with_a_control(self):
        # Published either way (_quarto.yml resources), linked only where a
        # control is written.
        tag = '<script src="../../site/download-all.js" defer'
        with_control = {page(course["code"]) for course, ids in courses() if files_of(ids) >= 2}
        self.assertEqual((QSITE / "site" / "download-all.js").read_bytes(), SCRIPT.read_bytes())
        for built in QSITE.rglob("*.html"):
            with self.subTest(page=built.relative_to(QSITE).as_posix()):
                text = built.read_text(encoding="utf-8")
                if built in with_control:
                    self.assertEqual(text.count(tag), 1)
                else:
                    self.assertNotIn("download-all.js", text)

    def test_no_zip_published(self):
        self.assertEqual([p.relative_to(QSITE).as_posix() for p in QSITE.rglob("*.zip")], [])

    def test_node_test_not_published(self):
        self.assertFalse((QSITE / "site" / "download-all.test.mjs").exists())


if __name__ == "__main__":
    unittest.main()
