"""The strip tool (D-0086): identity parts go, every other part stays byte for byte."""

import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import strip_identity  # noqa: E402

PANDOC = os.environ.get("PANDOC", "pandoc")
NAME = "Test Author Name"


class Strip(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        src = self.dir / "src.md"
        src.write_text("Some words.\n\n1.  A list.\n", encoding="utf-8")
        made = self.dir / "made.docx"
        subprocess.run([PANDOC, str(src), "-M", "author=" + NAME, "-o", str(made)], check=True)
        # Add what Word writes and Pandoc does not.
        with zipfile.ZipFile(made) as z:
            parts = {i.filename: z.read(i) for i in z.infolist()}
        core = parts["docProps/core.xml"].decode("utf-8")
        core = core.replace("</cp:coreProperties>",
                            "<cp:lastModifiedBy>" + NAME + "</cp:lastModifiedBy></cp:coreProperties>")
        parts["docProps/core.xml"] = core.encode("utf-8")
        app = parts["docProps/app.xml"].decode("utf-8")
        app = app.replace("</Properties>",
                          "<Template>C:\\Users\\someone\\Normal.dotm</Template>"
                          "<Manager>" + NAME + "</Manager>"
                          "<Company>" + NAME + "</Company></Properties>")
        parts["docProps/app.xml"] = app.encode("utf-8")
        self.parts = parts
        self.original = self.write("original.docx", parts)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, parts):
        path = self.dir / name
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            for n, data in parts.items():
                z.writestr(n, data)
        return path

    def test_identity_removed_and_other_parts_identical(self):
        out = self.dir / "stripped.docx"
        removed = strip_identity.strip(self.original, out)
        self.assertEqual(sorted(removed), sorted([
            "docProps/core.xml dc:creator", "docProps/core.xml cp:lastModifiedBy",
            "docProps/app.xml Company", "docProps/app.xml Manager",
            "docProps/app.xml Template"]))
        with zipfile.ZipFile(self.original) as a, zipfile.ZipFile(out) as b:
            self.assertEqual(a.namelist(), b.namelist())
            for name in a.namelist():
                if name.startswith("docProps/"):
                    self.assertNotIn(NAME.encode(), b.read(name))
                    self.assertNotIn(b"someone", b.read(name))
                else:
                    self.assertEqual(a.read(name), b.read(name), name)

    def test_parts_it_does_not_strip_stop_it(self):
        for name, data in (
                ("word/comments.xml", b'<w:comments><w:comment w:id="0"/></w:comments>'),
                ("word/people.xml", b'<w15:people><w15:person w15:author="A"/></w15:people>'),
                ("docProps/custom.xml", b'<Properties><property name="Owner"/></Properties>')):
            with self.subTest(part=name):
                path = self.write("extra.docx", {**self.parts, name: data})
                with self.assertRaises(SystemExit) as stop:
                    strip_identity.strip(path, self.dir / "out.docx")
                self.assertIn(name, str(stop.exception))

    def test_custom_properties_repeating_app_fields_pass(self):
        # The PH 211 rubric workbook's six, which name no one.
        custom = (b'<Properties><property name="AppVersion"/><property name="DocSecurity"/>'
                  b'<property name="ScaleCrop"/><property name="ShareDoc"/>'
                  b'<property name="LinksUpToDate"/><property name="HyperlinksChanged"/></Properties>')
        path = self.write("custom.docx", {**self.parts, "docProps/custom.xml": custom})
        strip_identity.strip(path, self.dir / "out.docx")
        with zipfile.ZipFile(self.dir / "out.docx") as z:
            self.assertEqual(z.read("docProps/custom.xml"), custom)

    def test_sharepoint_content_type_passes_when_it_names_no_one(self):
        # D-0185: the instructor notes kept in a SharePoint library. The
        # schema declares person fields; the properties record fills none.
        extra = {
            "docProps/custom.xml":
                b'<Properties><property name="ContentTypeId"/></Properties>',
            "customXml/item1.xml":
                b'<ct:contentTypeSchema><xsd:element name="UserInfo"/>'
                b'<xsd:element name="DisplayName"/></ct:contentTypeSchema>',
            "customXml/item2.xml":
                b'<p:properties><documentManagement/></p:properties>',
        }
        path = self.write("sharepoint.docx", {**self.parts, **extra})
        strip_identity.strip(path, self.dir / "out.docx")
        with zipfile.ZipFile(self.dir / "out.docx") as z:
            for name, data in extra.items():
                self.assertEqual(z.read(name), data)

    def test_sharepoint_properties_naming_a_person_stop_it(self):
        record = (b'<p:properties><documentManagement><SharedWithUsers><UserInfo>'
                  b'<DisplayName>A</DisplayName></UserInfo></SharedWithUsers>'
                  b'</documentManagement></p:properties>')
        path = self.write("shared.docx", {
            **self.parts,
            "docProps/custom.xml": b'<Properties><property name="ContentTypeId"/></Properties>',
            "customXml/item2.xml": record})
        with self.assertRaises(SystemExit) as stop:
            strip_identity.strip(path, self.dir / "out.docx")
        self.assertIn("customXml/item2.xml", str(stop.exception))

    def test_revision_author_stops_it(self):
        doc = self.parts["word/document.xml"].replace(
            b"<w:body>", b'<w:body><w:p><w:ins w:id="1" w:author="Someone"/></w:p>', 1)
        path = self.write("tracked.docx", {**self.parts, "word/document.xml": doc})
        with self.assertRaises(SystemExit):
            strip_identity.strip(path, self.dir / "out.docx")


# Made up for the test (D-0119 call 4): no real code or address.
CODE = "QZ7XK2PLM9"
URL = "https://vendor.example/app/?key=" + CODE + "&lang=en"
PERSONAL = "https://someone-my.sharepoint.com/personal/someone/doc.docx"


class Redact(unittest.TestCase):
    """D-0133: named passages and the link targets holding them never leave."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        src = self.dir / "src.md"
        src.write_text(
            "Install from <" + URL + ">.\n\n"
            "The activation code is **" + CODE + "**.\n\n"
            "Copy [your](" + PERSONAL + ") document and [the app page](" + URL + ").\n",
            encoding="utf-8")
        self.original = self.dir / "original.docx"
        subprocess.run([PANDOC, str(src), "-o", str(self.original)], check=True)
        with zipfile.ZipFile(self.original) as z:
            doc = z.read("word/document.xml").decode("utf-8")
        # The address is also the link's own text, as in PH 212 Lab 2.
        self.assertIn(escape(URL), doc)

    def tearDown(self):
        self.tmp.cleanup()

    def everything(self, path):
        with zipfile.ZipFile(path) as z:
            return {n: z.read(n) for n in z.namelist()}

    def test_passages_and_their_targets_are_removed(self):
        out = self.dir / "out.docx"
        removed = strip_identity.strip(self.original, out, [CODE, URL, PERSONAL])
        self.assertTrue(any("redacted" in r for r in removed))
        parts = self.everything(out)
        for name, data in parts.items():
            for p in (CODE, URL, PERSONAL, escape(URL)):
                self.assertNotIn(p.encode("utf-8"), data, name)
        doc = parts["word/document.xml"].decode("utf-8")
        self.assertIn("The activation code is<", doc)
        self.assertIn(strip_identity.MARKER, doc)
        rels = parts["word/_rels/document.xml.rels"].decode("utf-8")
        self.assertEqual(rels.count(strip_identity.REMOVED_TARGET), 2)  # one per address
        self.assertIn(">your<", doc)  # the linked word stays
        before = self.everything(self.original)
        for name in before:
            if not name.startswith(("docProps/", "word/document.xml", "word/_rels/")):
                self.assertEqual(before[name], parts[name], name)

    def test_redacted_file_reads_as_words_with_the_marker(self):
        out = self.dir / "out.docx"
        strip_identity.strip(self.original, out, [CODE, URL, PERSONAL])
        text = subprocess.run([PANDOC, str(out), "-t", "plain"], check=True,
                              capture_output=True, encoding="utf-8").stdout
        self.assertIn("The activation code is " + strip_identity.MARKER, text)
        self.assertNotIn(CODE, text)

    def test_personal_store_target_stops_an_unredacted_strip(self):
        with self.assertRaises(SystemExit) as stop:
            strip_identity.strip(self.original, self.dir / "out.docx")
        self.assertIn("personal file store", str(stop.exception))
        strip_identity.strip(self.original, self.dir / "out.docx", [PERSONAL])

    def test_a_passage_left_in_a_part_stops_it(self):
        parts = self.everything(self.original)
        parts["word/media/blob.bin"] = CODE.encode("utf-8")
        path = self.dir / "blob.docx"
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            for n, data in parts.items():
                z.writestr(n, data)
        with self.assertRaises(SystemExit) as stop:
            strip_identity.strip(path, self.dir / "out.docx", [CODE, URL, PERSONAL])
        self.assertIn("word/media/blob.bin", str(stop.exception))
        self.assertNotIn(CODE, str(stop.exception))

    def test_command_line_prints_no_passage(self):
        listing = self.dir / "passages.txt"
        listing.write_text(CODE + "\n" + URL + "\n" + PERSONAL + "\n", encoding="utf-8")
        run = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "strip_identity.py"), str(self.original),
             str(self.dir / "out.docx"), "--redact", str(listing)],
            check=True, capture_output=True, encoding="utf-8")
        for p in (CODE, URL, PERSONAL):
            self.assertNotIn(p, run.stdout + run.stderr)


class CommittedOriginals(unittest.TestCase):
    """No committed original links to a personal file store (D-0104, D-0133)."""

    def test_no_personal_store_targets(self):
        found = sorted(ROOT.glob("originals/**/*.docx"))
        self.assertTrue(found)
        for path in found:
            with zipfile.ZipFile(path) as z:
                for name in z.namelist():
                    if name.endswith(".rels"):
                        self.assertIsNone(strip_identity.PERSONAL_STORE.search(z.read(name)),
                                          f"{path.name} {name}")


if __name__ == "__main__":
    unittest.main()
