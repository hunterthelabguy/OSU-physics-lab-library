"""Strip the identity-bearing parts of an Office original before it is committed.

Usage: python tools/strip_identity.py ORIGINAL STRIPPED

D-0086: every original is committed with its identity-bearing parts
stripped, in both repos; `source_sha256` names the stripped file, and an
entry records both hashes. This removes `dc:creator` and `cp:lastModifiedBy`
from docProps/core.xml and `Company`, `Manager` and `Template` from
docProps/app.xml (survey section 8). Every other part is copied byte for
byte, so no `w:t` changes and the parts docs/word-labels.json is keyed to
stay as they were (D-0112).

The rest of D-0086's list (comments and their authors, revision authors,
people.xml, custom properties, photo EXIF) is in none of the 19 handouts, so
this tool removes none of it: it stops, naming the part, so a new original
that has one is looked at before anything is committed. Custom properties
that only repeat app.xml's fields pass (`APP_FIELDS`). Prints both hashes.
"""

import hashlib
import re
import sys
import zipfile

REMOVE = {
    "docProps/core.xml": ("dc:creator", "cp:lastModifiedBy"),
    "docProps/app.xml": ("Company", "Manager", "Template"),
}
# A part D-0086 lists, and what in it would carry a person: Pandoc writes an
# empty comments.xml and custom.xml into every docx, which hold nobody.
STOP_PART = (
    (re.compile(r"(^|/)comments\w*\.xml$", re.I), re.compile(rb"<w:comment\b")),
    (re.compile(r"(^|/)(people|persons)\.xml$", re.I), re.compile(rb"<\w*:?person\b", re.I)),
    (re.compile(r"(^|/)threadedComments\d*\.xml$", re.I), re.compile(rb"<\w*:?threadedComment\b")),
)
# Custom properties that only repeat app.xml's own fields, as the PH 211
# rubric workbook's do; any other custom property stops the strip.
CUSTOM = "docProps/custom.xml"
APP_FIELDS = {"AppVersion", "DocSecurity", "HyperlinksChanged", "LinksUpToDate",
              "ScaleCrop", "ShareDoc"}
PROPERTY_NAME = re.compile(rb'<property\b[^>]*\bname="([^"]*)"')
AUTHOR = re.compile(rb'\sw:author="')
EXIF = b"Exif\x00\x00"


def element(tag):
    t = re.escape(tag)
    return re.compile(r"<{0}(\s[^>]*)?/>|<{0}(\s[^>]*)?>.*?</{0}>".format(t), re.S)


def refusals(z):
    found = []
    for name in z.namelist():
        if any(part.search(name) and body.search(z.read(name)) for part, body in STOP_PART):
            found.append(f"{name}: a part D-0086 lists, which this tool does not strip")
        elif name == CUSTOM:
            other = sorted({n.decode("utf-8") for n in PROPERTY_NAME.findall(z.read(name))}
                           - APP_FIELDS)
            if other:
                found.append(f"{name}: custom properties {', '.join(other)}")
        elif name.startswith("word/") and name.endswith(".xml") and AUTHOR.search(z.read(name)):
            found.append(f"{name}: a revision or comment author (w:author)")
        elif name.lower().endswith((".jpg", ".jpeg")) and EXIF in z.read(name)[:65536]:
            found.append(f"{name}: EXIF data in a photo")
    return found


def strip(src, dst):
    with zipfile.ZipFile(src) as z:
        stop = refusals(z)
        if stop:
            raise SystemExit(f"{src}: not stripped:\n  " + "\n  ".join(stop))
        removed = []
        with zipfile.ZipFile(dst, "w") as out:
            for info in z.infolist():
                data = z.read(info)
                for tag in REMOVE.get(info.filename, ()):
                    text, n = element(tag).subn("", data.decode("utf-8"))
                    if n:
                        removed.append(f"{info.filename} {tag}")
                        data = text.encode("utf-8")
                out.writestr(info, data, compress_type=info.compress_type)
    return removed


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main(argv):
    if len(argv) != 2:
        raise SystemExit(__doc__.split("\n\n")[1])
    src, dst = argv
    removed = strip(src, dst)
    print("removed: " + (", ".join(removed) or "nothing"))
    print(f"original sha256: {sha256(src)}")
    print(f"stripped sha256: {sha256(dst)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
