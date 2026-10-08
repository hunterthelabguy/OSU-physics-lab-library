"""The strip tool (D-0086): identity parts go, every other part stays byte for byte."""

import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

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

    def test_revision_author_stops_it(self):
        doc = self.parts["word/document.xml"].replace(
            b"<w:body>", b'<w:body><w:p><w:ins w:id="1" w:author="Someone"/></w:p>', 1)
        path = self.write("tracked.docx", {**self.parts, "word/document.xml": doc})
        with self.assertRaises(SystemExit):
            strip_identity.strip(path, self.dir / "out.docx")


if __name__ == "__main__":
    unittest.main()
