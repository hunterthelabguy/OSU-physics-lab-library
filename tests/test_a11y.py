"""Accessibility gate over everything the build publishes (showcase, 2026-11-24).

Three parts, each against build/quarto-site:

- AuditRules: tools/a11y_audit.mjs on two made-up pages. The broken one
  must raise every rule at the element built to break it, and the clean one
  none, so a rule that stops firing or starts misfiring fails here first.
- SiteRatchet: the audit over every published HTML page, in light and dark,
  at 1280 and 320 px, against tests/a11y-known.json. A finding not in the
  file fails; a count that drops fails too, until the file is lowered, so
  the file only shrinks (the KNOWN_SKIPS ratchet of tests/test_headings.py).
  `python tests/test_a11y.py --write-known` rewrites the file from a fresh
  audit; review its diff like any ruling.
- Downloads: the PDF's tags (Chrome 158 tags its print: one H1, a language,
  the title shown, a /Alt for every Figure, a Table for every table in the
  HTML download) and the Word file's alt text and language. KNOWN_UNTITLED
  is the Word ratchet: files whose dc:title is empty.

Needs node (22 or later), CHROME and PDFTOTEXT, as the other download
tests do; pdfinfo is found beside pdftotext. A missing tool fails.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import unittest
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "build" / "quarto-site"
AUDIT = ROOT / "tools" / "a11y_audit.mjs"
FIXTURES = ROOT / "tests" / "fixtures" / "a11y"
KNOWN = ROOT / "tests" / "a11y-known.json"

# The element in broken.html each rule must name (a class on the target,
# or "document" for a page-level rule).
BROKEN = {
    "contrast": "p.low-contrast",
    "contrast-unmeasured": "p.on-image",
    "html-lang": "document",
    "page-title": "document",
    "one-h1": "h1.second-h1",
    "heading-skip": "h4.skip",
    "main-landmark": "document",
    "img-alt": "img.no-alt",
    "name": "a.empty-link",
    "aria-ref": "span.dangling",
    "table-headers": "table.no-th",
    "zoom-blocked": "document",
    "reflow": "div.wide",
    "target-size": "div.tiny > a",
    "focus-visible": "a.no-ring",
    "text-spacing": "div.clip",
}

# Word downloads with an empty dc:title (all of them on 2026-11-24): the
# title a screen reader announces and Word shows is then the file name.
KNOWN_UNTITLED = {
    "ph211-capstone-handout", "ph211-data-analysis-handout",
    "ph211-describing-an-experiment-handout", "ph211-designing-an-experiment-handout",
    "ph211-hypothesis-testing-handout", "ph211-team-building-handout",
    "ph211-uncertainty-handout", "ph212-capstone-handout",
    "ph212-data-analysis-handout", "ph212-designing-experiments-handout",
    "ph212-extending-a-model-handout", "ph212-hypothesis-testing-handout",
    "ph212-sharing-and-comparing-handout", "ph213-analysis-and-testing-handout",
    "ph213-data-analysis-handout", "ph213-data-taking-handout",
    "ph213-hypothesis-testing-handout", "ph213-model-building-handout",
    "ph21x-lab-handbook", "ph21x-problem-solving-strategy",
}


# Word pictures with empty alt text, as the originals have them (D-0132
# call 6; docs/owner-tasks.md, "Pictures that need alt text"). The page
# writes alt="" (decorative); Word gets descr="" with no decorative mark.
KNOWN_EMPTY_ALT = {
    "ph212-extending-a-model-handout": 1,
    "ph212-hypothesis-testing-handout": 1,
}


def node():
    found = shutil.which("node")
    if not found:
        raise AssertionError("node is not on PATH; the accessibility audit needs it")
    return found


def audit(folder, pages=()):
    args = [node(), str(AUDIT), str(folder)]
    for p in pages:
        args += ["--page", p]
    run = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", timeout=1800)
    if run.returncode:
        raise AssertionError("audit failed:\n" + run.stderr[-3000:])
    return json.loads(run.stdout)


def key(f):
    return f"{f['rule']}|{f['page']}|{f['theme']}|{f['width']}|{f['target']}"


def counts(findings):
    return dict(sorted(Counter(key(f) for f in findings).items()))


class AuditRules(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = audit(FIXTURES, ["clean.html", "broken.html"])

    def rules(self):
        run = subprocess.run([node(), "--input-type=module", "-e",
                              f"import('{AUDIT.as_uri()}').then(m => console.log(JSON.stringify(m.RULES)))"],
                             capture_output=True, text=True, check=True)
        return json.loads(run.stdout)

    def test_every_rule_has_a_broken_case(self):
        self.assertEqual(set(self.rules()), set(BROKEN))

    def test_broken_page_raises_every_rule_at_its_element(self):
        broken = [f for f in self.result["findings"] if f["page"] == "broken.html"]
        for rule, target in BROKEN.items():
            with self.subTest(rule=rule):
                hits = [f["target"] for f in broken if f["rule"] == rule]
                self.assertTrue(any(t == target or t.endswith(target) for t in hits),
                                f"{rule} did not name {target}; it named {sorted(set(hits))}")

    def test_clean_page_raises_nothing(self):
        clean = [f"{f['rule']} {f['theme']}{f['width']} {f['target']}: {f['detail']}"
                 for f in self.result["findings"] if f["page"] == "clean.html"]
        self.assertFalse(clean, "\n".join(clean))


class SiteRatchet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not SITE.is_dir():
            raise AssertionError("build/quarto-site is missing: run tools/quarto_build.py")
        cls.result = audit(SITE)
        cls.known = json.loads(KNOWN.read_text(encoding="utf-8"))

    def test_audits_every_page(self):
        # Redirect stubs aside, every published HTML page, the downloads too.
        self.assertGreater(len(self.result["pages"]), 40)
        self.assertTrue(any(p.endswith("/modern/index.html") for p in self.result["pages"]))
        self.assertTrue(any(re.match(r"labs/([^/]+)/\1\.html$", p) for p in self.result["pages"]))

    def test_no_new_finding(self):
        now = counts(self.result["findings"])
        detail = {key(f): f"{f['wcag']} {f['detail']}" for f in self.result["findings"]}
        new = [f"{k} ({n} > {self.known.get(k, 0)}): {detail[k]}"
               for k, n in now.items() if n > self.known.get(k, 0)]
        self.assertFalse(new, "new accessibility findings:\n" + "\n".join(new))

    def test_known_findings_still_hold(self):
        now = counts(self.result["findings"])
        fixed = [f"{k} ({self.known[k]} -> {now.get(k, 0)})" for k in self.known if now.get(k, 0) < self.known[k]]
        self.assertFalse(fixed, "fixed, so lower tests/a11y-known.json (--write-known):\n" + "\n".join(fixed))


def pdfinfo():
    pdftotext = os.environ.get("PDFTOTEXT") or shutil.which("pdftotext")
    if not pdftotext:
        raise AssertionError("PDFTOTEXT is not set and pdftotext is not on PATH")
    beside = Path(pdftotext).with_name("pdfinfo" + Path(pdftotext).suffix)
    found = str(beside) if beside.exists() else shutil.which("pdfinfo")
    if not found:
        raise AssertionError("pdfinfo is not beside pdftotext nor on PATH")
    return found


def labs():
    return sorted(p for p in (SITE / "labs").iterdir() if (p / f"{p.name}.pdf").exists())


class PdfTags(unittest.TestCase):

    def test_each_pdf_is_tagged_to_match_its_page(self):
        tool = pdfinfo()
        for lab in labs():
            with self.subTest(lab=lab.name):
                pdf = lab / f"{lab.name}.pdf"
                info = subprocess.run([tool, str(pdf)], capture_output=True, text=True).stdout
                self.assertRegex(info, r"(?m)^Tagged:\s+yes$")
                tree = subprocess.run([tool, "-struct", str(pdf)], capture_output=True, text=True).stdout
                tags = Counter(line.split()[0] for line in tree.splitlines() if line.strip())
                raw = pdf.read_bytes()
                self.assertEqual(tags["H1"], 1, "one H1")
                self.assertRegex(raw, rb"/Lang\s*\(en", "document language")
                self.assertIn(b"/DisplayDocTitle true", raw, "title shown, not the file name")
                alts = re.findall(rb"/Alt\s*\(([^)]*)\)", raw)
                self.assertEqual(len(alts), tags["Figure"], "a /Alt for every Figure")
                html = (lab / f"{lab.name}.html").read_text(encoding="utf-8")
                self.assertEqual(tags["Table"], html.count("<table"), "a Table for every table")


class DocxA11y(unittest.TestCase):

    def test_pictures_language_title(self):
        for lab in labs():
            with self.subTest(lab=lab.name):
                z = zipfile.ZipFile(lab / f"{lab.name}.docx")
                doc = z.read("word/document.xml").decode("utf-8")
                core = z.read("docProps/core.xml").decode("utf-8")
                empty = [pr for pr in re.findall(r"<wp:docPr [^>]*>", doc) if not re.search(r'descr="[^"]+"', pr)]
                self.assertEqual(len(empty), KNOWN_EMPTY_ALT.get(lab.name, 0),
                                 "pictures with no alt text (fixed: lower KNOWN_EMPTY_ALT)")
                self.assertRegex(core, r"<dc:language>en", "document language")
                self.assertRegex(doc, r'w:pStyle w:val="Heading\d', "real headings")
                titled = bool(re.search(r"<dc:title>[^<]+</dc:title>", core))
                if lab.name in KNOWN_UNTITLED:
                    self.assertFalse(titled, "titled: remove it from KNOWN_UNTITLED")
                else:
                    self.assertTrue(titled, "dc:title")


if __name__ == "__main__":
    if "--write-known" in sys.argv:
        KNOWN.write_text(json.dumps(counts(audit(SITE)["findings"]), indent=1) + "\n", encoding="utf-8")
        print("wrote", KNOWN)
    else:
        unittest.main()
