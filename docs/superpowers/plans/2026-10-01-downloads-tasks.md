# Lab Downloads Implementation Plan

> **Executed 2026-10-01, attended, with amendments; do not rerun.** The
> unattended run stopped at Task 2 (stop rule 2). The owner then ruled
> D-0054 to D-0056 in chat: the HTML download is a plain render with no
> chrome (`standalone()` deleted), the department line in every download,
> the top parity test retired, the Markdown guard narrowed, and the header
> logo published once. Task 2 Step 6 also lacked `render.py --site`. The
> record is PR #19 and those entries; where this plan differs, they win.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans
> to implement this plan task-by-task, in order. Steps use checkbox (`- [ ]`)
> syntax for tracking. You run unattended: the stop rules below override
> every other instinct.

**Goal:** Every converted lab offers four downloads (Markdown, Word, HTML,
PDF), all from the modern presentation, each carrying the draft banner,
linked from the modern lab page, built and tested in the Quarto build.

**Architecture:** A new `tools/downloads.py` runs at the end of
`tools/quarto_build.py`, after the site is built and dressed. Markdown is the
source file copied; Word is Pandoc from the source with the banner prepended;
HTML is the built modern page made self-contained by inlining its
stylesheets and fonts with the standard library; PDF is that built page
printed by headless Chrome. The links are a new `$if(downloadid)$` block in
`tools/template.html`, which the Quarto build already lifts into its pages
(D-0036), set only for modern lab pages.

**Tech Stack:** Python 3.12 standard library, Pandoc bundled with Quarto
(`$PANDOC`, D-0044), Quarto 1.10.18, Google Chrome (headless), poppler's
`pdftotext` (tests only), GitHub Actions.

**Spec:** `docs/superpowers/plans/2026-10-01-downloads.md` (its "Rulings"
section wins over its leans), `DECISIONS.md` D-0052 and D-0053 (both
proposed; the owner approved their content in chat on 2026-10-01).
`DECISIONS.md` wins over any plan where they differ.

## Global Constraints

- Every download comes from the modern presentation. No download for faithful, and no link on faithful pages (D-0053).
- Files: `build/quarto-site/labs/<id>/<id>.md`, `<id>.docx`, `<id>.html`, `<id>.pdf` (call 6).
- Link text, approved verbatim (D-0053): `Download: Word · HTML · PDF · Markdown`, in the lab page's `site-nav` bar. Write the separator as `&middot;`, as `tools/brandfooter.html` does.
- Footer sentence, approved verbatim (D-0053): `Downloads carry the same draft notice as these pages.` It replaces `Downloads (Markdown, Word, PDF) are not wired up in this draft.` in `tools/template.html`.
- Banner words come only from `render.BANNER_MAIN` and `render.BANNER_DETAIL`. Never write new copy anywhere.
- D-0010: a lab page's `<main>` never changes; `tests/fixtures/main-bodies.json` must stay green untouched.
- LEDGER 53: a missing tool or build is an error, never a skip.
- LEDGER 28: one source per document; the Markdown download is that file, byte for byte.
- `site/site.css` is shared with the old build: this plan adds no CSS. If a rule seems needed, stop (rule 3).
- No em dashes anywhere (grep for the bytes `\xe2\x80\x94`). Straight quotes in prose you write.
- Never route `PANDOC` through `quarto pandoc` (D-0045).
- Commits: identity `hunterthelabguy` with `301055645+hunterthelabguy@users.noreply.github.com`; no Co-Authored-By trailer; subject 72 characters or fewer, a narrative body.

## Stop rules (unattended run)

Stop means: commit what is green, push the branch, write the question as a
PR comment (or in the PR body if no PR yet), and end. Do not guess past these.

1. A test you wrote does not fail first, or fails for a reason other than the one its step names.
2. Any Quarto `WARN`/`WARNING` line, any Pandoc `[WARNING]`, or an existing test going red.
3. Anything that needs new page copy, new CSS, a change inside `<main>`, or a change to a ledger entry's status.
4. Chrome or `pdftotext` missing or failing, except the one documented case in Task 5, Step 4.
5. The PR's CI red after one honest fix attempt.
6. Never merge the PR, never push to `main`, never touch the Cloudflare or Vercel projects, never read or print a secret.

## Environment (local, Windows, Git Bash)

```bash
export QUARTO="/c/Program Files/Quarto/bin/quarto.exe"
export PANDOC="/c/Program Files/Quarto/bin/tools/pandoc.exe"
export PANDOC_OLD_BUILD="$LOCALAPPDATA/Pandoc/pandoc.exe"
export CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
export PDFTOTEXT="$LOCALAPPDATA/Microsoft/WinGet/Packages/oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe/poppler-25.07.0/Library/bin/pdftotext.exe"
```

Python is `python` (3.12). Rebuild the Quarto site with
`python tools/quarto_build.py` before any test that reads `build/quarto-site/`.
Long inline Python heredocs fail in the Bash tool: write scripts to a file.
Edit files with the Edit tool, not `sed` or heredoc `\n` escapes (an escaped
`\n` in a heredoc lands as a real newline and breaks string literals).

## File map

- Create `tools/downloads.py`: the four builders and `standalone()`. One responsibility: turn a built lab into its downloads.
- Create `tests/test_downloads_unit.py`: `standalone()` on small fixtures; needs no build.
- Create `tests/test_downloads.py`: the built downloads and the links; needs `build/quarto-site/`.
- Modify `tools/template.html`: the links block and the footer sentence.
- Modify `tools/quarto_chrome.py` (`old_chrome`): pass `downloadid` when the page has one.
- Modify `tools/quarto_build.py`: `download_id` on modern lab pages in `generate()`; call `downloads.build()` at the end of `build()`.
- Modify `.github/workflows/verify.yml`: Chrome and `pdftotext` steps.
- Modify `CLAUDE.md` (Build) and `STATE.md`: what exists now and how to run it.

---

### Task 1: `standalone()`, the self-contained HTML maker

**Files:**
- Create: `tools/downloads.py`
- Test: `tests/test_downloads_unit.py`

**Interfaces:**
- Produces: `downloads.standalone(page_html: str, page_dir: str) -> str`; `downloads.is_relative(url: str) -> bool`; constants `downloads.THEME = "modern"`, `downloads.EXTENSIONS = ("md", "docx", "html", "pdf")`.

- [ ] **Step 1: Create the branch**

```bash
git switch main && git pull && git switch -c lab-downloads
git config user.name && git config user.email
```
Expected: `hunterthelabguy` and `301055645+hunterthelabguy@users.noreply.github.com`. Anything else: stop.

- [ ] **Step 2: Write the failing unit tests**

Create `tests/test_downloads_unit.py`:

```python
"""tools/downloads.py: standalone() on small fixtures (D-0052, D-0053).

The HTML download is the built modern page made to open from disk:
stylesheets inlined with their fonts, scripts and both navs removed,
relative links reduced to their words. Anything it cannot place is an
error, never a silent drop (LEDGER 53). Needs no build.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import downloads                          # noqa: E402

PAGE = """<!DOCTYPE html>
<html><head>
<meta name="robots" content="noindex, nofollow">
<link href="lib/bootstrap.min.css" rel="stylesheet" id="quarto-bootstrap">
<link href="lib/bootstrap-icons.css" rel="stylesheet">
<link rel="stylesheet" href="site/site.css">
<script src="lib/quarto.js"></script>
</head>
<body class="theme-modern">
<div class="draft-banner">Draft</div>
<header class="osu-header">
<a class="osu-logo" href="https://oregonstate.edu"><img src="data:image/png;base64,AAAA" alt="Oregon State University"></a>
<a class="osu-sitename" href="../../../">Physics Lab Library</a>
<nav class="osu-nav" aria-label="Library"><div class="osu-inner">
<a href="../../../">Library home</a>
</div></nav>
</header><nav class="site-nav">
<a href="../../../courses/">Course index</a>
</nav>
<main>
<h1>Lab</h1>
<p>See <a href="#part-1">part 1</a>.</p>
</main>
<script>window.x = 1;</script>
<footer class="osu-foot"><p>License: see <a href="../../../how-this-was-made/">How this was made</a>.</p>
<p><a href="https://oregonstate.edu/accessibility-statement">Accessibility Statement</a></p></footer>
</body></html>
"""


class Standalone(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "lib").mkdir()
        (root / "site" / "fonts").mkdir(parents=True)
        (root / "lib" / "bootstrap.min.css").write_text("body{margin:0}\n", encoding="utf-8")
        (root / "lib" / "bootstrap-icons.css").write_text(".bi{x:1}\n", encoding="utf-8")
        (root / "site" / "site.css").write_text(
            '@font-face { src: url("fonts/Sans.woff2") format("woff2"); }\n', encoding="utf-8")
        (root / "site" / "fonts" / "Sans.woff2").write_bytes(b"\x00\x01font")
        self.page_dir = str(root)

    def tearDown(self):
        self.tmp.cleanup()

    def out(self, page=PAGE):
        return downloads.standalone(page, self.page_dir)

    def test_both_navs_removed(self):
        text = self.out()
        self.assertNotIn('class="osu-nav"', text)
        self.assertNotIn('class="site-nav"', text)
        self.assertNotIn("Course index", text)

    def test_missing_nav_is_an_error(self):
        with self.assertRaises(ValueError):
            self.out(PAGE.replace('<nav class="site-nav">', '<nav class="other">'))

    def test_scripts_removed(self):
        self.assertNotIn("<script", self.out())

    def test_stylesheets_inlined_with_fonts(self):
        text = self.out()
        self.assertNotIn("<link", text)
        self.assertIn("body{margin:0}", text)
        self.assertIn('url("data:font/woff2;base64,AAFmb250")', text)

    def test_icon_stylesheet_dropped(self):
        self.assertNotIn(".bi{x:1}", self.out())

    def test_icons_in_use_is_an_error(self):
        with self.assertRaises(ValueError):
            self.out(PAGE.replace("<h1>Lab</h1>", '<h1 class="bi-star">Lab</h1>'))

    def test_relative_links_become_words(self):
        text = self.out()
        self.assertIn('<a href="#part-1">part 1</a>', text)
        self.assertIn("Physics Lab Library", text)
        self.assertNotIn('href="../../../"', text)
        self.assertIn("see How this was made.", text)

    def test_absolute_links_kept(self):
        text = self.out()
        self.assertIn('<a href="https://oregonstate.edu/accessibility-statement">', text)
        self.assertIn('<a class="osu-logo" href="https://oregonstate.edu">', text)

    def test_missing_font_is_an_error(self):
        (Path(self.page_dir) / "site" / "fonts" / "Sans.woff2").unlink()
        with self.assertRaises(FileNotFoundError):
            self.out()

    def test_relative_reference_left_is_an_error(self):
        with self.assertRaises(ValueError):
            self.out(PAGE.replace('src="data:image/png;base64,AAAA"', 'src="logo.png"'))

    def test_nothing_relative_left(self):
        import re
        for url in re.findall(r'\b(?:src|href)="([^"]*)"', self.out()):
            with self.subTest(url=url):
                self.assertFalse(downloads.is_relative(url), url)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run it to verify it fails**

Run: `python -m unittest tests.test_downloads_unit -v`
Expected: ERROR, `ModuleNotFoundError: No module named 'downloads'`.

- [ ] **Step 4: Write `tools/downloads.py` with `standalone()`**

```python
"""Lab downloads: Markdown, Word, HTML and PDF (D-0052, D-0053).

Run by tools/quarto_build.py after the site is built and dressed; never on
its own. Every file comes from the modern presentation and carries the
draft banner (ledger 37), and is written beside the presentations as
labs/<id>/<id>.<ext>, so a saved file is named after the lab. Markdown is
the source, byte for byte (LEDGER 28). Word is Pandoc's, from the source,
with the banner as its first two paragraphs. HTML is the built modern page
made self-contained: stylesheets and fonts inlined, scripts and both navs
removed, relative links reduced to their words, so it opens from disk. PDF
is the built modern page printed by headless Chrome with the site's print
rules. A missing tool is an error, never a skip (LEDGER 53).
"""

import base64
import os
import re

THEME = "modern"
EXTENSIONS = ("md", "docx", "html", "pdf")
FONT_TYPES = {".woff2": "font/woff2", ".woff": "font/woff"}
# Lab pages use no Bootstrap icon; standalone() refuses a page that does.
UNUSED_STYLESHEETS = ("bootstrap-icons.css",)

NAV = re.compile(r'<nav class="(osu-nav|site-nav)"[^>]*>.*?</nav>\n?', re.S)
SCRIPT = re.compile(r"<script\b[^>]*>.*?</script>\n?", re.S)
STYLESHEET = re.compile(r'<link\b[^>]*\brel="stylesheet"[^>]*>\n?')
HREF = re.compile(r'\bhref="([^"]*)"')
ANCHOR = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.S)
ATTR_URL = re.compile(r'\b(?:src|href)="([^"]*)"')
CSS_URL = re.compile(r"""url\(\s*(["']?)([^)"']+)\1\s*\)""")


def is_relative(url):
    """True for a path inside the site; false for a scheme, //host, or #."""
    return not re.match(r"(?:[a-z][a-z0-9+.-]*:|#|//)", url, re.I)


def inline_css(css_text, css_dir):
    """Embed each relative url() (fonts only) as a data: URI."""
    def embed(m):
        url = m.group(2)
        if not is_relative(url):
            return m.group(0)
        path = os.path.normpath(os.path.join(css_dir, url.split("?")[0].split("#")[0]))
        ext = os.path.splitext(path)[1].lower()
        if ext not in FONT_TYPES:
            raise ValueError("unexpected resource in a stylesheet: " + url)
        with open(path, "rb") as fh:
            data = base64.b64encode(fh.read()).decode("ascii")
        return 'url("data:{};base64,{}")'.format(FONT_TYPES[ext], data)
    return CSS_URL.sub(embed, css_text)


def standalone(page_html, page_dir):
    """The built modern page, made to open from disk (D-0053, call 5)."""
    navs = NAV.findall(page_html)
    if sorted(navs) != ["osu-nav", "site-nav"]:
        raise ValueError("expected one osu-nav and one site-nav, found {}".format(navs))
    text = NAV.sub("", page_html)
    text = SCRIPT.sub("", text)
    if re.search(r'class="[^"]*\bbi-', text):
        raise ValueError("the page uses Bootstrap icons; their stylesheet cannot be dropped")

    def link(m):
        href = HREF.search(m.group(0)).group(1)
        if not is_relative(href):
            raise ValueError("external stylesheet: " + href)
        if os.path.basename(href) in UNUSED_STYLESHEETS:
            return ""
        path = os.path.normpath(os.path.join(page_dir, href))
        with open(path, encoding="utf-8") as fh:
            css = inline_css(fh.read(), os.path.dirname(path))
        return "<style>\n" + css + "\n</style>\n"
    text = STYLESHEET.sub(link, text)

    def unwrap(m):
        found = HREF.search(m.group(1))
        return m.group(2) if found and is_relative(found.group(1)) else m.group(0)
    text = ANCHOR.sub(unwrap, text)

    left = sorted({u for u in ATTR_URL.findall(text) if is_relative(u)})
    if left:
        raise ValueError("relative references left: {}".format(left[:5]))
    return text
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python -m unittest tests.test_downloads_unit -v`
Expected: 11 tests, OK.

- [ ] **Step 6: Commit**

```bash
grep -c $'\xe2\x80\x94' tools/downloads.py tests/test_downloads_unit.py
git add tools/downloads.py tests/test_downloads_unit.py
git commit -m "Add standalone(): the built modern page made to open from disk" -m "D-0052, D-0053 call 5: stylesheets and fonts inlined, scripts and both
navs removed, relative links reduced to their words; a page it cannot
place raises. Tests first (11), watched failing on the missing module."
```
Expected grep counts: 0 and 0.

---

### Task 2: the links and the footer sentence on modern lab pages

**Files:**
- Modify: `tools/template.html` (the `site-nav` block and the footer paragraph)
- Modify: `tools/quarto_chrome.py` (`old_chrome`, the `doc` branch)
- Modify: `tools/quarto_build.py` (`generate()`, the lab page dicts)
- Test: `tests/test_downloads.py` (new; its first class)

**Interfaces:**
- Consumes: `downloads.THEME`, `downloads.EXTENSIONS` (Task 1).
- Produces: page dicts from `quarto_build.generate()` carry `"download_id"`: the doc id on modern lab pages, `""` elsewhere; `old_chrome(page)` passes `-M downloadid=<id>` when it is set.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_downloads.py`:

```python
"""The lab downloads in the built Quarto site (D-0052, D-0053).

A missing build or tool is an error, never a skip (LEDGER 53). Reads
build/quarto-site/; run tools/quarto_build.py first.
"""

import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QSITE = ROOT / "build" / "quarto-site"
PANDOC = os.environ.get("PANDOC", "pandoc")
PDFTOTEXT = os.environ.get("PDFTOTEXT", "pdftotext")
FILTER = ROOT / "tools" / "filters" / "questions.lua"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))
import downloads                          # noqa: E402
from render import BANNER_MAIN, BANNER_DETAIL  # noqa: E402
from test_quarto_site import converted    # noqa: E402

LABELS = {"docx": "Word", "html": "HTML", "pdf": "PDF", "md": "Markdown"}
FOOTER_NEW = "Downloads carry the same draft notice as these pages."
FOOTER_OLD = "are not wired up in this draft"


def setUpModule():
    if not QSITE.is_dir():
        raise RuntimeError("build/quarto-site is missing: run tools/quarto_build.py first")


def page(doc_id, theme):
    return (QSITE / "labs" / doc_id / theme / "index.html").read_text(encoding="utf-8")


def flat(text):
    return " ".join(text.split())


class Links(unittest.TestCase):
    """D-0053: the approved links on modern pages only, outside <main>."""

    def site_nav(self, text):
        m = re.search(r'<nav class="site-nav">.*?</nav>', text, re.S)
        self.assertIsNotNone(m, "no site-nav")
        return m.group(0)

    def test_modern_page_links_every_download(self):
        for doc_id, _ in converted():
            nav = self.site_nav(page(doc_id, "modern"))
            for ext in downloads.EXTENSIONS:
                with self.subTest(doc=doc_id, ext=ext):
                    self.assertIn('<a href="../{0}.{1}" download="{0}.{1}">{2}</a>'.format(
                        doc_id, ext, LABELS[ext]), nav)

    def test_approved_wording(self):
        for doc_id, _ in converted():
            nav = flat(re.sub(r"<[^>]+>", "", self.site_nav(page(doc_id, "modern"))))
            with self.subTest(doc=doc_id):
                self.assertIn("Download: Word · HTML · PDF · Markdown", nav.replace("&middot;", "·"))

    def test_faithful_page_offers_none(self):
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                self.assertNotIn(" download=", page(doc_id, "faithful"))

    def test_links_outside_main(self):
        for doc_id, _ in converted():
            main = re.search(r"<main>.*?</main>", page(doc_id, "modern"), re.S).group(0)
            with self.subTest(doc=doc_id):
                self.assertNotIn(" download=", main)

    def test_footer_sentence(self):
        for doc_id, _ in converted():
            for theme in ("modern", "faithful"):
                text = flat(page(doc_id, theme))
                with self.subTest(doc=doc_id, theme=theme):
                    self.assertIn(FOOTER_NEW, text)
                    self.assertNotIn(FOOTER_OLD, text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Rebuild and run to verify they fail**

```bash
python tools/quarto_build.py > /dev/null && python -m unittest tests.test_downloads -v
```
Expected: `test_modern_page_links_every_download`, `test_approved_wording` and `test_footer_sentence` FAIL (no links, old sentence); `test_faithful_page_offers_none` and `test_links_outside_main` pass (they guard what must stay true).

- [ ] **Step 3: Edit `tools/template.html`**

Replace:
```
$if(switchhref)$<a class="switch" href="$switchhref$">$switchlabel$</a>$endif$
```
with:
```
$if(downloadid)$<span class="downloads">Download: <a href="../$downloadid$.docx" download="$downloadid$.docx">Word</a> &middot; <a href="../$downloadid$.html" download="$downloadid$.html">HTML</a> &middot; <a href="../$downloadid$.pdf" download="$downloadid$.pdf">PDF</a> &middot; <a href="../$downloadid$.md" download="$downloadid$.md">Markdown</a></span>$endif$
$if(switchhref)$<a class="switch" href="$switchhref$">$switchlabel$</a>$endif$
```
And replace:
```
apart. Downloads (Markdown, Word, PDF) are not wired up in this draft.</p>
```
with:
```
apart. Downloads carry the same draft notice as these pages.</p>
```

- [ ] **Step 4: Edit `tools/quarto_chrome.py`, `old_chrome`, the `doc` branch**

After the line `cmd += render.site_vars(page["depth"]) + render.document_extras(theme, page["depth"])`, add:
```python
        if page.get("download_id"):
            cmd += ["-M", "downloadid=" + page["download_id"]]
```

- [ ] **Step 5: Edit `tools/quarto_build.py`**

Add `import downloads` after `import quarto_chrome`. In `generate()`, replace:
```python
            pages.append({"html": "labs/{}/{}/index.html".format(doc_id, theme),
                          "kind": "doc", "depth": 3, "theme": theme, "footnote": ""})
```
with:
```python
            pages.append({"html": "labs/{}/{}/index.html".format(doc_id, theme),
                          "kind": "doc", "depth": 3, "theme": theme, "footnote": "",
                          # D-0053: downloads come from modern only.
                          "download_id": doc_id if theme == downloads.THEME else ""})
```

- [ ] **Step 6: Rebuild and run everything**

```bash
python tools/quarto_build.py > /dev/null && python -m unittest tests.test_downloads -v
python -m unittest discover -s tests
SITE_DIR=build/quarto-site python -m unittest discover -s tests -p test_site_chrome.py
```
Expected: `tests.test_downloads` 5 OK; the full suite OK (the body hashes in `tests/fixtures/main-bodies.json` unchanged, D-0010); chrome contract 9 OK. Any red: stop rule 2.

- [ ] **Step 7: Commit**

```bash
grep -c $'\xe2\x80\x94' tools/template.html tools/quarto_chrome.py tools/quarto_build.py tests/test_downloads.py
git add tools/template.html tools/quarto_chrome.py tools/quarto_build.py tests/test_downloads.py
git commit -m "Link the four downloads from modern lab pages; new footer line" -m "D-0053: 'Download: Word · HTML · PDF · Markdown' in the site-nav bar of
modern lab pages only, each link with a download filename (Pages serves
.html without its extension, so the attribute names the saved file); the
footer's 'not wired up' sentence becomes the approved one. Outside <main>
(D-0010). Tests first; the three new-behavior tests watched failing."
```

---

### Task 3: Markdown and Word downloads

**Files:**
- Modify: `tools/downloads.py` (add `markdown()`, `word()`, `banner_markdown()`, `build()`)
- Modify: `tools/quarto_build.py` (`build()` calls `downloads.build`)
- Test: `tests/test_downloads.py` (add class `MarkdownAndWord`)

**Interfaces:**
- Consumes: `render.ROOT`, `render.PANDOC`, `render.BANNER_MAIN`, `render.BANNER_DETAIL`, `render.body_after_front_matter(path) -> str`, `render.converted_documents() -> {id: {"path", "meta"}}`.
- Produces: `downloads.build(out: str, docs: dict) -> None`, which writes every extension in `EXTENSIONS` per lab (the HTML and PDF builders arrive in Tasks 4 and 5; until then `build()` writes only `md` and `docx`).

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_downloads.py`, above `if __name__`:

```python
def words(text):
    """Letters and digits only, so bullets and list marks cannot differ."""
    return re.findall(r"[\w’']+", text)


def plain(*args, input=None):
    return subprocess.run([PANDOC, *args, "-t", "plain"], input=input, check=True,
                          capture_output=True, text=True, encoding="utf-8").stdout


class MarkdownAndWord(unittest.TestCase):

    def test_markdown_is_the_source_byte_for_byte(self):
        for doc_id, source in converted():
            with self.subTest(doc=doc_id):
                got = (QSITE / "labs" / doc_id / (doc_id + ".md")).read_bytes()
                self.assertEqual(got, source.read_bytes())

    def test_word_is_banner_then_the_modern_words(self):
        banner = words(BANNER_MAIN + " " + BANNER_DETAIL)
        for doc_id, source in converted():
            with self.subTest(doc=doc_id):
                docx = QSITE / "labs" / doc_id / (doc_id + ".docx")
                got = words(plain(str(docx)))
                want = words(plain(str(source), "-f", "markdown-smart",
                                   "--lua-filter", str(FILTER), "-M", "theme=modern"))
                self.assertEqual(got[:len(banner)], banner)
                self.assertEqual(got[len(banner):], want)
                self.assertIn("Question", got)
```

- [ ] **Step 2: Rebuild and run to verify they fail**

```bash
python tools/quarto_build.py > /dev/null && python -m unittest tests.test_downloads.MarkdownAndWord -v
```
Expected: both ERROR with `FileNotFoundError` naming `<id>.md` and `<id>.docx`.

- [ ] **Step 3: Add the builders to `tools/downloads.py`**

Add `import shutil` and `import subprocess` to the imports, and `import render` after them. Then append:

```python
def banner_markdown():
    """The approved banner as the Word file's first two paragraphs."""
    return "**{}**\n\n{}\n\n".format(render.BANNER_MAIN, render.BANNER_DETAIL)


def markdown(doc, dest):
    shutil.copyfile(doc["path"], dest)


def word(doc, dest):
    """Pandoc's Word file from the source, modern question labels (D-0053)."""
    text = banner_markdown() + render.body_after_front_matter(doc["path"])
    proc = subprocess.run(
        [render.PANDOC, "-f", "markdown-smart", "-t", "docx",
         "--lua-filter", os.path.join(render.ROOT, "tools", "filters", "questions.lua"),
         "-M", "theme=" + THEME, "-M", "lang=en", "-o", dest],
        input=text, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0 or "[WARNING]" in proc.stderr:
        raise SystemExit("Pandoc failed on {}:\n{}".format(doc["path"], proc.stderr))


def build(out, docs):
    """Write every lab's downloads into out/labs/<id>/."""
    for doc_id, doc in docs.items():
        folder = os.path.join(out, "labs", doc_id)
        markdown(doc, os.path.join(folder, doc_id + ".md"))
        word(doc, os.path.join(folder, doc_id + ".docx"))
```

- [ ] **Step 4: Call it from `tools/quarto_build.py`**

In `build()`, after the line `    post()`, add:
```python
    downloads.build(OUT, render.converted_documents())
```

- [ ] **Step 5: Rebuild and run**

```bash
python tools/quarto_build.py > /dev/null && python -m unittest tests.test_downloads -v
python -m unittest tests.test_downloads_unit
```
Expected: `tests.test_downloads` 7 OK; unit 11 OK. If the Word words differ from the source words, do not loosen the test: stop rule 1, with the first differing words in the PR comment.

- [ ] **Step 6: Commit**

```bash
grep -c $'\xe2\x80\x94' tools/downloads.py tools/quarto_build.py tests/test_downloads.py
git add tools/downloads.py tools/quarto_build.py tests/test_downloads.py
git commit -m "Build the Markdown and Word downloads" -m "Markdown is the source byte for byte (LEDGER 28). Word is Pandoc's from
the source with modern question labels and the approved banner as its
first two paragraphs (D-0052, D-0053); a Pandoc warning fails the build.
Tests first: byte equality, and the Word file's words equal the banner's
then the modern render's."
```

---

### Task 4: HTML download

**Files:**
- Modify: `tools/downloads.py` (`html()`, and `build()` calls it)
- Test: `tests/test_downloads.py` (add class `Html`)

**Interfaces:**
- Consumes: `standalone()` (Task 1); the built page `out/labs/<id>/modern/index.html`.
- Produces: `downloads.html(page_path: str, dest: str) -> None`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_downloads.py`, above `if __name__`:

```python
# Measured in Task 4, Step 5; never a guess. See the commit that sets it.
HTML_CAP_BYTES = None


class Html(unittest.TestCase):

    def download(self, doc_id):
        return (QSITE / "labs" / doc_id / (doc_id + ".html")).read_text(encoding="utf-8")

    def test_self_contained(self):
        for doc_id, _ in converted():
            text = self.download(doc_id)
            with self.subTest(doc=doc_id):
                self.assertNotIn("<script", text)
                self.assertNotIn("<link", text)
                for url in re.findall(r'\b(?:src|href)="([^"]*)"', text):
                    self.assertFalse(downloads.is_relative(url), url)
                self.assertIn("data:font/woff2;base64,", text)

    def test_banner_and_noindex(self):
        for doc_id, _ in converted():
            text = self.download(doc_id)
            with self.subTest(doc=doc_id):
                self.assertIn(BANNER_MAIN, flat(text))
                self.assertIn('<meta name="robots" content="noindex', text)

    def test_main_is_the_modern_pages(self):
        for doc_id, _ in converted():
            want = re.search(r"<main>.*?</main>", page(doc_id, "modern"), re.S).group(0)
            got = re.search(r"<main>.*?</main>", self.download(doc_id), re.S).group(0)
            with self.subTest(doc=doc_id):
                self.assertEqual(re.sub(r"<a\b[^>]*>|</a>", "", got),
                                 re.sub(r"<a\b[^>]*>|</a>", "", want))

    def test_size_capped(self):
        self.assertIsNotNone(HTML_CAP_BYTES, "set HTML_CAP_BYTES from the measurement")
        for doc_id, _ in converted():
            size = (QSITE / "labs" / doc_id / (doc_id + ".html")).stat().st_size
            with self.subTest(doc=doc_id, size=size):
                self.assertLessEqual(size, HTML_CAP_BYTES)
```

- [ ] **Step 2: Rebuild and run to verify they fail**

```bash
python tools/quarto_build.py > /dev/null && python -m unittest tests.test_downloads.Html -v
```
Expected: three ERROR with `FileNotFoundError` naming `<id>.html`; `test_size_capped` FAIL on "set HTML_CAP_BYTES".

- [ ] **Step 3: Add `html()` to `tools/downloads.py` and call it**

Append:
```python
def html(page_path, dest):
    with open(page_path, encoding="utf-8", newline="") as fh:
        text = standalone(fh.read(), os.path.dirname(page_path))
    with open(dest, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
```
In `build()`, after the `word(...)` line, add:
```python
        page = os.path.join(folder, THEME, "index.html")
        html(page, os.path.join(folder, doc_id + ".html"))
```

- [ ] **Step 4: Rebuild and run**

```bash
python tools/quarto_build.py > /dev/null && python -m unittest tests.test_downloads.Html -v
```
Expected: three OK; `test_size_capped` still FAIL (cap unset).

- [ ] **Step 5: Measure and set the cap (call 7)**

```bash
ls -l build/quarto-site/labs/*/*.html | grep -v index.html
```
Take the largest size in bytes, multiply by 1.10, round up to the next 10,000, and set `HTML_CAP_BYTES` to that integer. The planning probe expects about 0.9 MB (page 261,916 bytes; Bootstrap CSS 504,152; Open Sans 4 files 102,356 raw, about 136 KB encoded); if the measured size is above 1,000,000 bytes, stop rule 3 (cutting more means dropping Bootstrap, a design change).

- [ ] **Step 6: Run the whole module and suite**

```bash
python -m unittest tests.test_downloads -v && python -m unittest discover -s tests
```
Expected: all OK. `tests/test_quarto_site.py` walks every `.html` in the build, so it now reads the download too (noindex, one `<h1>`, no third party): if it goes red, stop rule 2.

- [ ] **Step 7: Open the file from disk, network off, and look**

Open `build/quarto-site/labs/<id>/<id>.html` in Chrome by its `file://` path with Wi-Fi off (or with DevTools' network set to Offline). Expected: Open Sans, the banner, the logo, the modern layout, no console error about a missing file. Note what you saw in the commit body. If it looks wrong, stop rule 3.

- [ ] **Step 8: Commit**

```bash
grep -c $'\xe2\x80\x94' tools/downloads.py tests/test_downloads.py
git add tools/downloads.py tests/test_downloads.py
git commit -m "Build the HTML download: the modern page, self-contained" -m "<Measured: N bytes for <id>.html; cap set to M (N x 1.10, rounded up to
10,000). What the page looked like opened from disk offline.> D-0053 call
5 and 7. Tests first; three watched failing on the missing file."
```
Replace the angle-bracket text with the real numbers and observation before committing.

---

### Task 5: PDF download, and CI

**Files:**
- Modify: `tools/downloads.py` (`pdf()`, and `build()` calls it)
- Modify: `.github/workflows/verify.yml` (two steps)
- Test: `tests/test_downloads.py` (add class `Pdf`)

**Interfaces:**
- Consumes: the built page `out/labs/<id>/modern/index.html`; `CHROME` from the environment.
- Produces: `downloads.pdf(page_path: str, dest: str) -> None`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_downloads.py`, above `if __name__`:

```python
class Pdf(unittest.TestCase):

    def path(self, doc_id):
        return QSITE / "labs" / doc_id / (doc_id + ".pdf")

    def text(self, doc_id):
        return subprocess.run([PDFTOTEXT, "-layout", str(self.path(doc_id)), "-"],
                              check=True, capture_output=True, text=True,
                              encoding="utf-8").stdout

    def test_is_a_pdf(self):
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                self.assertEqual(self.path(doc_id).read_bytes()[:5], b"%PDF-")

    def test_banner_running_header_and_title(self):
        for doc_id, source in converted():
            title = re.search(r"^# (.+)$", source.read_text(encoding="utf-8"), re.M).group(1)
            text = flat(self.text(doc_id))
            with self.subTest(doc=doc_id):
                self.assertIn(BANNER_MAIN, text)
                self.assertIn("DRAFT: license pending", text)
                self.assertIn(flat(title), text)
                self.assertRegex(text, r"Page 1 of \d+")
```

- [ ] **Step 2: Rebuild and run to verify they fail**

```bash
python tools/quarto_build.py > /dev/null && python -m unittest tests.test_downloads.Pdf -v
```
Expected: `test_is_a_pdf` ERROR `FileNotFoundError`; `test_banner_running_header_and_title` ERROR from `pdftotext` (the file is missing). If instead `pdftotext` itself is not found, `PDFTOTEXT` is not exported: fix the environment, not the test.

- [ ] **Step 3: Add `pdf()` to `tools/downloads.py` and call it**

Add `import pathlib` to the imports and `CHROME = os.environ.get("CHROME", "google-chrome")` after `THEME`. Append:
```python
def pdf(page_path, dest):
    """Headless Chrome prints the built page with the site's print rules.

    --no-pdf-header-footer: the running header and page numbers come from
    the @page rules in site/site.css, not from Chrome.
    """
    if shutil.which(CHROME) is None and not os.path.isfile(CHROME):
        raise SystemExit("Chrome not found; set CHROME to the browser (LEDGER 53)")
    proc = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
         "--print-to-pdf=" + os.path.abspath(dest),
         pathlib.Path(os.path.abspath(page_path)).as_uri()],
        capture_output=True, text=True)
    if proc.returncode != 0 or not os.path.isfile(dest) or os.path.getsize(dest) == 0:
        raise SystemExit("Chrome did not print {}:\n{}".format(page_path, proc.stderr[-2000:]))
```
In `build()`, after the `html(...)` line, add:
```python
        pdf(page, os.path.join(folder, doc_id + ".pdf"))
```

- [ ] **Step 4: Rebuild and run**

```bash
python tools/quarto_build.py > /dev/null && python -m unittest tests.test_downloads -v
```
Expected: all OK. The planning probe (2026-10-01, Chrome on Windows) printed Lab 1's modern page as 4 letter pages, 86,416 bytes, with the running header and "Page N of 4". Open the PDF and compare it by eye with that description.

- [ ] **Step 5: Add the CI steps to `.github/workflows/verify.yml`**

Insert these two steps immediately before the step named `Quarto site builds`:
```yaml
      - name: Use the runner's Chrome for the PDF downloads
        # D-0052: GitHub's Ubuntu images ship Google Chrome (runner-images
        # readmes, checked 2026-10-01); a missing one fails, never skips.
        run: |
          c=$(command -v google-chrome || true)
          if [ -z "$c" ]; then echo "google-chrome not found on the runner"; exit 1; fi
          "$c" --version
          echo "CHROME=$c" >> "$GITHUB_ENV"
      - name: Install pdftotext (PDF download tests)
        # Not on the runner images; tests/test_downloads.py reads PDFs with it.
        run: |
          sudo apt-get update
          sudo apt-get install -y poppler-utils
          pdftotext -v 2>&1 | head -1
```
The documented exception to stop rule 4: if CI's build fails and Chrome's stderr names the sandbox (for example "No usable sandbox"), add `--no-sandbox` to the Chrome command in `pdf()` only when the environment variable `CI` is `true`, with a comment citing the CI log line; any other Chrome failure is a stop.

- [ ] **Step 6: Run the full local verify**

```bash
python tools/check_unchanged.py curriculum/ph211/ph211-team-building-handout.md
grep -rIl $'\xe2\x80\x94' --exclude-dir=.git --exclude-dir=originals --exclude-dir=build --exclude-dir=.superpowers .
PANDOC="$PANDOC_OLD_BUILD" python tools/render.py --site
python tools/quarto_build.py
python -m unittest discover -s tests
SITE_DIR=build/quarto-site python -m unittest discover -s tests -p test_site_chrome.py
```
Expected: `ok ... (989 words identical; bold identical on 943 words outside headings)`; no em-dash file listed; both builds exit 0; the suite OK with 134 + 11 + 13 = 158 tests (134 before this plan; 11 unit; 13 in `tests/test_downloads.py`); chrome contract 9 OK. Use the real counts from the run in the commit and PR.

- [ ] **Step 7: Commit**

```bash
grep -c $'\xe2\x80\x94' tools/downloads.py tests/test_downloads.py .github/workflows/verify.yml
git add tools/downloads.py tests/test_downloads.py .github/workflows/verify.yml
git commit -m "Build the PDF download with headless Chrome; CI gets pdftotext" -m "D-0052, D-0053: the modern page printed by headless Chrome with the
site's @page rules (running header, page numbers); Chrome's own header
and footer off. CI uses the runner's google-chrome and installs
poppler-utils for the tests. Tests first, watched failing on the missing
file. <real test counts>."
```

---

### Task 6: docs, PR, and the preview

**Files:**
- Modify: `CLAUDE.md` (Build section: a "Downloads" bullet; the verify exports)
- Modify: `STATE.md` (Focus and Awaiting owner)

- [ ] **Step 1: `CLAUDE.md`, Build section**

Add a bullet after the Quarto bullet's "Build with `python tools/quarto_build.py`" sub-bullet:
```markdown
  - Downloads (D-0052, D-0053): `tools/downloads.py`, run at the end of
    `tools/quarto_build.py`, writes `labs/<id>/<id>.md`, `.docx`, `.html`
    and `.pdf`, all from modern, each with the draft banner. The PDF needs
    Chrome (`CHROME`; locally
    `/c/Program Files/Google/Chrome/Application/chrome.exe`, in CI the
    runner's `google-chrome`); the tests need `pdftotext` (`PDFTOTEXT`;
    locally poppler from winget, in CI `poppler-utils`). Missing either is
    an error. The HTML download is the built modern page made
    self-contained by `standalone()`; it refuses a page using Bootstrap
    icons, because it drops their stylesheet.
```
And in "Which Pandoc", where the three exports are listed, add that `CHROME` and `PDFTOTEXT` are exported too for the downloads.

- [ ] **Step 2: `STATE.md`**

In Focus, add one sentence: downloads built on branch `lab-downloads`, PR number, test count, awaiting the owner's review of the preview. Under Awaiting owner, replace the downloads line with: review PR <n> and its preview on a phone; merge is the owner's.

- [ ] **Step 3: Commit, push, open the PR**

```bash
grep -c $'\xe2\x80\x94' CLAUDE.md STATE.md
git add CLAUDE.md STATE.md
git commit -m "Document the downloads build and its two tools" -m "CLAUDE.md: what tools/downloads.py writes, CHROME and PDFTOTEXT, and the
icon-stylesheet guard. STATE.md: the PR awaits the owner's review."
git push -u origin lab-downloads
"/c/Program Files/GitHub CLI/gh.exe" pr create --base main --head lab-downloads \
  --title "Lab downloads: Word, HTML, PDF and Markdown, from modern" \
  --body "Implements docs/superpowers/plans/2026-10-01-downloads-tasks.md (D-0052, D-0053). Do not merge without the owner. Tests: <counts>. HTML download: <bytes>, cap <bytes>. PDF: <pages> pages. Preview: see this PR's deploy job log for the URL; open a modern lab page on a phone, check the Download row fits at phone width, and try each link."
```

- [ ] **Step 4: Read CI once it reports, through the PR tools; do not poll**

Expected: `verify` green and `deploy` green (the preview's byte check covers the four new files per lab, since `check_deployed.py` walks every file). Red: one honest fix, then stop rule 5. Then end the run with the PR open. Never merge (stop rule 6).

## Self-review (done at planning time)

- Spec coverage: one set per lab, all from modern (Tasks 3 to 5); Markdown byte for byte (Task 3); approved wording and footer (Task 2); banner in every file (Tasks 3, 4, 5 tests); HTML without nav, relative links reduced (Tasks 1, 4); file names (Task 2 links, Tasks 3 to 5 writes); size measured and capped (Task 4); tests per file (all); CI tools (Task 5); docs (Task 6).
- Deviations from the planning doc, both for cause: Word is made by Pandoc directly instead of Quarto's `format-links` (the owner's ruling is "Word by Pandoc"; `format-links` would add Quarto's own link UI to the page and cannot put the banner first). The HTML is the built page inlined, not a second Quarto render: probed 2026-10-01, a standalone Quarto render was 1,333,949 bytes, and its `<main>` lacks the end marker `quarto_chrome.dress()` anchors on, so it could not carry the approved chrome.
- Names used across tasks: `downloads.THEME`, `downloads.EXTENSIONS`, `downloads.standalone`, `downloads.is_relative`, `downloads.build`, `downloads.markdown`, `downloads.word`, `downloads.html`, `downloads.pdf`, page key `download_id`, template variable `downloadid`.
