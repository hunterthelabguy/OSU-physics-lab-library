"""Strip the identity-bearing parts of an Office original before it is committed.

Usage: python tools/strip_identity.py ORIGINAL STRIPPED [--redact LIST]

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

D-0185: the custom property `ContentTypeId` passes too. SharePoint writes it
into a file kept in a document library; its value names the library's
content type, not a person. Such a file also carries `customXml` parts: a
form template, the content type's schema, and a properties record. The
schema declares person fields (`SharedWithUsers`, `DisplayName`) without
holding anyone; a properties record that fills one in stops the strip
(`PERSON_VALUE`).

D-0133: `--redact LIST` names a UTF-8 file, kept outside the repo, of
passages that must never be committed (one per line). In every XML part
each passage, raw or XML-escaped, becomes `MARKER`; in a .rels part, an
external target holding one becomes `REMOVED_TARGET`. The tool then stops if
any passage is left in any part, and never prints one: only counts. An
external target on a personal file store (`PERSONAL_STORE`) stops the strip
unless it is redacted, since no original may carry one (D-0104).
"""

import hashlib
import re
from xml.sax.saxutils import escape
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
# What SharePoint adds that names no one (D-0185).
SHAREPOINT_FIELDS = {"ContentTypeId"}
CUSTOM_XML = re.compile(r"^customXml/item\d+\.xml$")
SCHEMA = b"contentTypeSchema"
PERSON_VALUE = re.compile(rb"<(\w+:)?(DisplayName|AccountId|UserInfo)\b")
PROPERTY_NAME = re.compile(rb'<property\b[^>]*\bname="([^"]*)"')
AUTHOR = re.compile(rb'\sw:author="')
EXIF = b"Exif\x00\x00"
MARKER = "[removed under D-0104]"
REMOVED_TARGET = "https://removed.invalid/"
PERSONAL_STORE = re.compile(rb'Target="[^"]*(sharepoint\.com|onedrive\.|1drv\.ms)[^"]*"', re.I)
EXTERNAL = re.compile(r'<Relationship\b[^>]*TargetMode="External"[^>]*>')
TARGET = re.compile(r'Target="([^"]*)"')


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
                           - APP_FIELDS - SHAREPOINT_FIELDS)
            if other:
                found.append(f"{name}: custom properties {', '.join(other)}")
        elif (CUSTOM_XML.match(name) and SCHEMA not in z.read(name)
              and PERSON_VALUE.search(z.read(name))):
            found.append(f"{name}: a SharePoint properties record that names a person")
        elif name.startswith("word/") and name.endswith(".xml") and AUTHOR.search(z.read(name)):
            found.append(f"{name}: a revision or comment author (w:author)")
        elif name.lower().endswith((".jpg", ".jpeg")) and EXIF in z.read(name)[:65536]:
            found.append(f"{name}: EXIF data in a photo")
        elif name.endswith(".rels") and PERSONAL_STORE.search(z.read(name)):
            found.append(f"{name}: a link target on a personal file store (D-0104);"
                         " redact it with --redact")
    return found


def redact(name, text, passages):
    """Return the part's text with every passage removed, and the count."""
    count = 0
    if name.endswith(".rels"):
        def target(m):
            nonlocal count
            rel = m.group(0)
            if any(p in rel or escape(p) in rel for p in passages):
                count += 1
                return TARGET.sub('Target="' + REMOVED_TARGET + '"', rel)
            return rel
        return EXTERNAL.sub(target, text), count
    for p in passages:  # longest first, so a passage inside another goes with it
        for form in dict.fromkeys((escape(p), p)):
            count += text.count(form)
            text = text.replace(form, MARKER)
    return text, count


def strip(src, dst, passages=()):
    passages = sorted(set(passages), key=len, reverse=True)
    with zipfile.ZipFile(src) as z:
        stop = refusals(redacted_view(z, passages)) if passages else refusals(z)
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
                if passages and xml_part(info.filename):
                    text, n = redact(info.filename, data.decode("utf-8"), passages)
                    if n:
                        removed.append(f"{info.filename} redacted x{n}")
                        data = text.encode("utf-8")
                if any(p.encode("utf-8") in data or escape(p).encode("utf-8") in data
                       for p in passages):
                    raise SystemExit(f"{src}: a redacted passage is left in {info.filename}")
                out.writestr(info, data, compress_type=info.compress_type)
    return removed


def xml_part(name):
    return name.endswith((".xml", ".rels"))


class redacted_view:
    """The archive as `refusals` sees it once the passages are redacted."""

    def __init__(self, z, passages):
        self.z, self.passages = z, passages

    def namelist(self):
        return self.z.namelist()

    def read(self, name):
        data = self.z.read(name)
        if xml_part(name):
            data = redact(name, data.decode("utf-8"), self.passages)[0].encode("utf-8")
        return data


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main(argv):
    passages = []
    if len(argv) == 4 and argv[2] == "--redact":
        with open(argv[3], encoding="utf-8") as fh:
            passages = [line.strip() for line in fh if line.strip()]
        if not passages:
            raise SystemExit(f"{argv[3]}: no passages")
        argv = argv[:2]
    if len(argv) != 2:
        raise SystemExit(__doc__.split("\n\n")[1])
    src, dst = argv
    removed = strip(src, dst, passages)
    print("removed: " + (", ".join(removed) or "nothing"))
    print(f"original sha256: {sha256(src)}")
    print(f"stripped sha256: {sha256(dst)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
