"""Download all on the course index (D-0067).

Runs the node test beside site/download-all.js, has that script's own code
write a zip of a course's published files, reads the zip back with Python's
zipfile, and checks the course index Quarto built: one control per course
with a converted lab, its file list, its words, its CSS and its script.
Needs build/quarto-site/ and node; either missing is an error, never a skip
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
import render                             # noqa: E402

QSITE = ROOT / "build" / "quarto-site"
INDEX = QSITE / "courses" / "index.html"
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


def setUpModule():
    if not QSITE.is_dir():
        raise RuntimeError("{} is missing: run tools/quarto_build.py first".format(QSITE))
    if NODE is None:
        raise RuntimeError("node is not on PATH; the Download all tests need it")


@functools.lru_cache(maxsize=None)
def courses():
    """[(course, [converted lab ids])] in the order of site/courses.md."""
    docs = render.converted_documents()
    meta = render.pandoc_meta(str(ROOT / "site" / "courses.md"))
    return tuple((c, [lab["document"] for lab in c.get("labs") or [] if lab.get("document") in docs])
            for c in meta["courses"])


def sections():
    """{course code: the course index's HTML from its h2 to the next}."""
    text = INDEX.read_text(encoding="utf-8")
    parts = re.split(r"(?=<h2\b)", text)
    out = {}
    for course, _ in courses():
        found = [p for p in parts[1:] if re.match(r"<h2[^>]*>" + re.escape(course["code"]) + r"\b", p)]
        assert len(found) == 1, (course["code"], len(found))
        out[course["code"]] = found[0]
    return out


OPENER = re.compile(r'<button type="button" class="download-all-open"[^>]*>([^<]*)</button>')


def controls(section):
    """Each Download all dialog in a course's section."""
    return re.findall(r'<dialog class="download-all"[^>]*>.*?</dialog>', section, re.S)


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
    """A zip the page's code writes, read by Python's zipfile."""

    def course_files(self, code):
        control = controls(sections()[code])[0]
        return [(value, files) for value, files, _, _ in boxes(control)]

    def check_zip(self, paths):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d, "course.zip")
            write_zip(paths, INDEX.parent, out)
            with zipfile.ZipFile(out) as z:
                self.assertIsNone(z.testzip(), "a CRC-32 does not match")
                infos = z.infolist()
                self.assertEqual([i.filename for i in infos],
                                 ["/".join(p.split("/")[-2:]) for p in paths])
                for info, path in zip(infos, paths):
                    want = (INDEX.parent / path).resolve().read_bytes()
                    with self.subTest(entry=info.filename):
                        self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
                        self.assertEqual(info.CRC, zlib.crc32(want))
                        self.assertEqual(z.read(info), want)

    def test_every_format_of_ph211(self):
        paths = [p for _, files in self.course_files("PH 211") for p in files]
        ids = dict((c["code"], i) for c, i in courses())["PH 211"]
        self.assertEqual(len(paths), len(downloads.EXTENSIONS) * len(ids))
        self.check_zip(paths)

    def test_one_format_only(self):
        paths = dict(self.course_files("PH 211"))["md"]
        self.check_zip(paths)

    def test_no_format_writes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d, "course.zip")
            write_zip([], INDEX.parent, out)
            self.assertFalse(out.exists())


class Control(unittest.TestCase):
    """The course index as built."""

    def test_one_control_per_course_with_a_converted_lab(self):
        found = sections()
        for course, ids in courses():
            with self.subTest(course=course["code"]):
                self.assertEqual(len(controls(found[course["code"]])), 1 if ids else 0)
        self.assertTrue(any(ids for _, ids in courses()), "no course has a converted lab")

    def test_opener_then_dialog_after_the_lab_list(self):
        # D-0067 as amended 2026-10-03: out of students' path, after the list.
        for code, section in sections().items():
            if controls(section):
                with self.subTest(course=code):
                    after_list = section.split("</ul>", 1)[1].lstrip()
                    self.assertRegex(after_list, r'^<button type="button" class="download-all-open"'
                                                 r'[^>]*>[^<]*</button>\s*<dialog class="download-all"')
                    self.assertEqual(len(OPENER.findall(section)), 1)

    def test_files_are_exactly_the_converted_labs_published_files(self):
        found = sections()
        for course, ids in courses():
            if not ids:
                continue
            with self.subTest(course=course["code"]):
                listed = boxes(controls(found[course["code"]])[0])
                self.assertEqual(sorted(v for v, _, _, _ in listed), sorted(downloads.EXTENSIONS))
                for value, files, _, _ in listed:
                    self.assertEqual(files, ["../labs/{0}/{0}.{1}".format(i, value) for i in ids])
                    for f in files:
                        self.assertTrue((INDEX.parent / f).resolve().is_file(), f)

    def test_zip_named_by_course_code(self):
        found = sections()
        for course, ids in courses():
            if ids:
                with self.subTest(course=course["code"]):
                    control = controls(found[course["code"]])[0]
                    want = "".join(course["code"].split()).lower() + ".zip"
                    self.assertIn('data-zip="{}"'.format(want), control)
        self.assertIn('data-zip="ph211.zip"', controls(found["PH 211"])[0])

    def test_words(self):
        # "Download all" and "Download selected" as approved (D-0067); the four
        # names are the lab page's download row's, read from the template.
        row = re.findall(r'<a class="download-button"[^>]*>([^<]+)</a>',
                         (ROOT / "tools" / "template.html").read_text(encoding="utf-8"))
        self.assertEqual(len(row), 4)
        for code, section in sections().items():
            for control in controls(section):
                with self.subTest(course=code):
                    self.assertEqual(OPENER.findall(section), ["Download all"])
                    self.assertIn('aria-label="Download all"', control)
                    self.assertEqual(re.findall(r'<button [^>]*>([^<]*)</button>', control),
                                     ["Download selected"])
                    self.assertEqual([label for _, _, label, _ in boxes(control)], row)
                    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", control)).strip()
                    self.assertEqual(text, " ".join(row + ["Download selected"]))

    def test_opt_in_and_hidden_until_the_script_runs(self):
        # Nothing ticked, so "Download selected" starts disabled; the opener
        # is hidden as built and shown by the script, never a dead button.
        for code, section in sections().items():
            for control in controls(section):
                with self.subTest(course=code):
                    for _, _, _, tag in boxes(control):
                        self.assertNotRegex(tag, r"\bchecked\b")
                    self.assertRegex(re.search(r"<button [^>]*>", control).group(0), r"\bdisabled\b")
                    opener = re.search(r'<button type="button" class="download-all-open"[^>]*>', section).group(0)
                    self.assertRegex(opener, r"\bhidden\b")
                    self.assertIn('aria-haspopup="dialog"', opener)

    def test_opener_is_quiet(self):
        # Less prominent than the lab pages' orange buttons, still one tap.
        opener = rules(".quarto-light .download-all-open")
        for decl in ("min-height: 44px", "background: transparent", "color: var(--chrome-quiet)",
                     "border: 1px solid var(--chrome-quiet)"):
            with self.subTest(decl=decl):
                self.assertIn(decl, opener)
        self.assertNotIn("--chrome-accent", opener)
        self.assertIn("display: none", rules(".quarto-light .download-all-open[hidden]"))

    def test_download_selected_is_the_download_button(self):
        # D-0059's button: test_quarto_chrome.QuartoOnlyCss.test_download_buttons.
        decls = rules(".quarto-light .download-all button.download-selected")
        for decl in ("min-height: 44px", "background: var(--chrome-accent)", "color: #fff",
                     "font-weight: 700", "font-size: 1rem", "border-radius: 6px"):
            with self.subTest(decl=decl):
                self.assertIn(decl, decls)


class Script(unittest.TestCase):

    def test_names_no_url_outside_the_site(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"[a-z][a-z0-9+.-]*://", text, re.I))
        self.assertIsNone(re.search(r"[\"'`]//", text))
        self.assertNotRegex(text, r"\bimport\b|\brequire\s*\(")

    def test_linked_once_from_the_course_index_only(self):
        tag = '<script src="../site/download-all.js" defer'
        self.assertEqual(INDEX.read_text(encoding="utf-8").count(tag), 1)
        self.assertEqual((QSITE / "site" / "download-all.js").read_bytes(), SCRIPT.read_bytes())
        for page in QSITE.rglob("*.html"):
            if page != INDEX:
                with self.subTest(page=page.relative_to(QSITE).as_posix()):
                    self.assertNotIn("download-all.js", page.read_text(encoding="utf-8"))

    def test_no_zip_published(self):
        self.assertEqual([p.relative_to(QSITE).as_posix() for p in QSITE.rglob("*.zip")], [])

    def test_node_test_not_published(self):
        self.assertFalse((QSITE / "site" / "download-all.test.mjs").exists())


if __name__ == "__main__":
    unittest.main()
