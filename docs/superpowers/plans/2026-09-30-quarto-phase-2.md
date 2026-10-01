# Quarto Migration Phase 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Quarto build carry the old build's chrome (draft banner, OSU header and footer, document nav and footer, fonts, landing hero) so that the whole chrome suite, `tests/test_site_chrome.py`, passes against `build/quarto-site/` and gates `verify`.

**Architecture:** Quarto renders a flat body (`section-divs: false`, `anchor-sections: false`, `wrap: auto`), which makes the content inside `<main>` byte-identical to the old build. A post-render step in `tools/quarto_build.py` then dresses each page: a bare `<main>`, the old chrome inserted after `<body ...>` and after Quarto's content div, and the old body class added. The chrome is never copied. A new module, `tools/quarto_chrome.py`, renders the old templates through Pandoc with an empty body and the metadata `tools/render.py` already passes, then cuts at `<main>`. `site/site.css` gets a small block of Quarto-only rules, closed by measured parity with the old build.

**Tech Stack:** Quarto 1.10.18 (pinned, checked by the driver), Pandoc 3.11 (old build, front matter reads, chrome lift), Python 3.12 stdlib only, GitHub Actions, the desktop app's browser pane for measurement.

**Spec:** `docs/quarto-migration-plan.md` (phase 2), with the rulings in `DECISIONS.md` D-0036 to D-0042 and the evidence in `docs/quarto-spike-2026-09-30.md`. Phase 1's plan, `docs/superpowers/plans/2026-09-30-quarto-phase-1.md`, shows the shape of the driver this extends.

Ledger: D-0029, D-0030, D-0031, D-0032, D-0033, D-0036, D-0037, D-0038, D-0039, D-0040, D-0041, D-0042
binds LEDGER 28, 37, 39, 51, 53

## Gates (owner rulings before work starts)

The owner ruled the eleven critique questions in chat on 2026-09-30 ("Rule your way on all eleven and write the plan"). The ledger entries recording them were appended as `proposed`, because an agent never changes a status. Before Task 1:

- D-0029, D-0030, D-0031 and D-0032 promoted. Task 4's parity target is the old build's look, which is those four entries.
- D-0036, D-0037, D-0038, D-0039, D-0040 and D-0042 promoted.

Before Task 6, Step 1: D-0041 ruled. If it is declined, stop after Task 5 and bring the owner the alternatives listed in D-0041. The PR does not merge with the chrome suite outside `verify`.

## Global Constraints

- No brand test is edited, weakened, skipped or dropped. The only test edit in this phase is D-0041's, made only after its ruling, in Task 6. Every other test change is a new test in a new file.
- The old build keeps feeding production unchanged in behavior. `tools/render.py --site` output stays byte-identical through Task 2's refactor (proved by a tree hash). `site/site.css` gains only rules whose selectors exist only on Quarto pages (Task 4, asserted by a test).
- One source per document (LEDGER 28) and one source for the chrome: the chrome is lifted from `tools/template.html`, `tools/template-site.html` and the brand partials at build time, never copied into a new file.
- Every page unlisted (LEDGER 37): noindex meta and our `robots.txt`, as phase 1.
- Plain static output any host serves (LEDGER 39). No setting that loads a third-party resource: theme `default`, never Cosmo; never `algolia:`; math as MathML (D-0040).
- Sims ship byte for byte plus the bar only (LEDGER 51), through `render.render_sim` unchanged. Sims are not dressed.
- A missing build is an error, never a skip (LEDGER 53). The new built-output tests need both `build/site/` and `build/quarto-site/`.
- Markdown is read as `markdown-smart`. No curly quotes anywhere.
- No invented copy: every string on a page comes from `tools/render.py`, the templates, the partials or the curriculum and site sources. Banner wording stays in `BANNER_MAIN` and `BANNER_DETAIL`.
- Quarto 1.10.18 exactly; the driver refuses any other version. Any Quarto warning line fails the build.
- No em dashes. Roles, not names. FERPA gate.
- Locally on Windows set both `QUARTO="C:\Program Files\Quarto\bin\quarto.exe"` and `PANDOC="%LOCALAPPDATA%\Pandoc\pandoc.exe"`. In Git Bash: `export QUARTO="/c/Program Files/Quarto/bin/quarto.exe" PANDOC="$LOCALAPPDATA/Pandoc/pandoc.exe"`. Long Python with backslash paths goes in a scratchpad file, not a bash heredoc.
- Branch `quarto-phase-2`. Every commit is green under the full verify sequence below, so each task may push. Lands as one PR through `verify`, squash merge, then `git branch -D quarto-phase-2` (the PR keeps the commits at `refs/pull/<n>/head`). Identity hunterthelabguy with the noreply email, no trailer.

**Verify sequence** (named in steps as "the verify sequence"):

```bash
python tools/check_unchanged.py curriculum/ph211/ph211-team-building-handout.md
grep -rIl $'\xe2\x80\x94' --exclude-dir=.git --exclude-dir=originals --exclude-dir=build . && echo "EM DASH" || echo "no em dash"
python tools/render.py --site
python tools/quarto_build.py
python -m unittest discover -s tests
SITE_DIR=build/quarto-site python -m unittest discover -s tests -p test_site_chrome.py
```

The converted file list for `check_unchanged.py` is whatever CI's "Content unchanged" step finds (on 2026-09-30, that one file); rerun that step's loop locally if curriculum files were added. The last command is the chrome contract on Quarto. It is expected to fail until Task 3 (all but the footer test) and Task 6 (the footer test).

## File Structure

- Modify `_quarto.yml`: no navbar, search off, flat body, MathML, exact resources (Task 1).
- Modify `tools/quarto_build.py`: the version check (Task 1); a page manifest from `generate()` and a dressing pass (Task 3).
- Create `tests/test_quarto_config.py`: pins on `_quarto.yml` and the Quarto version (Task 1).
- Create `tests/test_quarto_chrome.py`: built-output checks of navigation, published files (Task 1), chrome parity and the bare `<main>` (Task 3), and the Quarto-only CSS block (Task 4).
- Modify `tools/render.py`: hoist the two footnotes and the document-nav metadata into named values; behavior unchanged (Task 2).
- Create `tools/quarto_chrome.py`: lift the old chrome, dress a Quarto page (Task 2).
- Create `tests/test_quarto_dress.py`: unit tests for `tools/quarto_chrome.py` (Task 2).
- Modify `site/site.css`: one delimited block of Quarto-only rules (Task 4).
- Create `tools/measure_chrome.js`: the manual parity and layout measurement, run in the browser pane (Task 4, Task 5).
- Modify `tests/test_site_chrome.py`: D-0041's one-line edit, only if ruled (Task 6).
- Modify `.github/workflows/verify.yml`: the chrome contract moves into `verify`; `chrome-on-quarto` goes (Task 6).
- Modify `CLAUDE.md`, `STATE.md`, `docs/quarto-migration-plan.md`: the new state and the measured numbers (Task 5, Task 6).

---

### Task 1: Config pins, the version check, one nav, published files

D-0037 (no navbar, no search), D-0039 (exact resources), D-0040 (MathML), D-0036's three body settings, and the version check. The body settings change nothing visible yet. They are pinned here so that later tasks build on them.

**Files:**
- Modify: `_quarto.yml`
- Modify: `tools/quarto_build.py` (new `QUARTO_VERSION`, `check_version`, `quarto_version`; `build()` calls the check first)
- Create: `tests/test_quarto_config.py`
- Create: `tests/test_quarto_chrome.py` (module setup, `chrome_pages()`, classes `Navigation` and `Published`)

**Interfaces:**
- Produces: `quarto_build.QUARTO_VERSION: str = "1.10.18"`; `quarto_build.check_version(reported: str) -> None` (raises `SystemExit` unless `reported.strip() == QUARTO_VERSION`); `quarto_build.quarto_version() -> str` (stdout of `QUARTO --version`).
- Produces in `tests/test_quarto_chrome.py`: `QSITE`, `OLD` (paths), `chrome_pages() -> iterator of (rel: str, text: str)` over Quarto `index.html` pages that are neither redirect stubs nor `sims/<id>/index.html`. Task 3 and Task 4 add classes to this file.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_quarto_config.py`:

```python
"""Pins on _quarto.yml and the Quarto version (D-0033, D-0036, D-0037,
D-0039, D-0040).

Settings that change no page today, such as the math method, can only be
guarded here. Reads the YAML with the standard library: comment lines
dropped, then "key: value" per line.
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import quarto_build                       # noqa: E402

RESOURCES = [
    "site/fonts/OpenSans-Regular.woff2",
    "site/fonts/OpenSans-Bold.woff2",
    "site/fonts/OpenSans-Italic.woff2",
    "site/fonts/OpenSans-BoldItalic.woff2",
    "site/fonts/OFL.txt",
]


def config():
    lines = (ROOT / "_quarto.yml").read_text(encoding="utf-8").splitlines()
    return "\n".join(l.rstrip() for l in lines if not l.lstrip().startswith("#")) + "\n"


def values(key):
    found = re.findall(r"^[ ]*" + re.escape(key) + r":[ ]*(.*)$", config(), re.M)
    return [v.strip().strip("'\"") for v in found]


def items(key):
    """The '- item' lines directly under a key."""
    m = re.search(r"^([ ]*)" + re.escape(key) + r":[ ]*\n((?:\1[ ]+- .*\n)+)", config(), re.M)
    return [] if m is None else [l.strip()[2:].strip() for l in m.group(2).splitlines()]


class Pins(unittest.TestCase):

    def test_theme_default_never_cosmo(self):
        self.assertEqual(values("theme"), ["default"])
        self.assertNotIn("cosmo", config().lower())

    def test_math_is_mathml(self):
        # D-0040: Quarto's default fetches MathJax from a CDN.
        self.assertEqual(values("html-math-method"), ["mathml"])

    def test_no_algolia(self):
        self.assertNotIn("algolia", config().lower())

    def test_one_nav_and_no_search(self):
        # D-0037: the OSU header's nav is the only one.
        self.assertEqual(values("navbar"), [])
        self.assertEqual(values("search"), ["false"])

    def test_flat_body(self):
        # D-0036: with these, <main> holds the old build's bytes.
        self.assertEqual(values("section-divs"), ["false"])
        self.assertEqual(values("anchor-sections"), ["false"])
        self.assertEqual(values("wrap"), ["auto"])

    def test_straight_quotes(self):
        self.assertEqual(values("from"), ["markdown-smart"])

    def test_title_partial_wired(self):
        self.assertIn("title-block.html", items("template-partials"))

    def test_output_dir(self):
        self.assertEqual(values("output-dir"), ["build/quarto-site"])

    def test_resources_exact(self):
        # D-0039: fonts and their license only; no READMEs, no logo files.
        self.assertEqual(sorted(items("resources")), sorted(RESOURCES))

    def test_noindex_in_head(self):
        self.assertIn('content="noindex, nofollow"', config())


class Version(unittest.TestCase):

    def test_pin(self):
        # Upgrade on purpose, in its own PR (docs/quarto-migration-plan.md).
        self.assertEqual(quarto_build.QUARTO_VERSION, "1.10.18")

    def test_accepts_the_pin(self):
        quarto_build.check_version("1.10.18\n")

    def test_rejects_anything_else(self):
        for reported in ("1.10.17", "1.11.0", "", "quarto 1.10.18"):
            with self.subTest(reported=reported):
                with self.assertRaises(SystemExit):
                    quarto_build.check_version(reported)

    def test_ci_installs_the_pin(self):
        ci = (ROOT / ".github" / "workflows" / "verify.yml").read_text(encoding="utf-8")
        installs = re.findall(r"quarto-cli/releases/download/v([\d.]+)/quarto-([\d.]+)-", ci)
        self.assertTrue(installs)
        v = quarto_build.QUARTO_VERSION
        for tag, name in installs:
            self.assertEqual((tag, name), (v, v))


if __name__ == "__main__":
    unittest.main()
```

Create `tests/test_quarto_chrome.py`:

```python
"""Phase 2 chrome on the Quarto build (D-0036 to D-0039, D-0042).

Needs both builds: build/site/ (the old build, the chrome's source) and
build/quarto-site/. A missing build is an error, never a skip (LEDGER 53).
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QSITE = ROOT / "build" / "quarto-site"
OLD = ROOT / "build" / "site"


def setUpModule():
    for d, how in ((OLD, "tools/render.py --site"), (QSITE, "tools/quarto_build.py")):
        if not d.is_dir():
            raise RuntimeError("{} is missing: run {} first".format(d, how))


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


class Published(unittest.TestCase):
    """D-0039: only the fonts and their license go out."""

    def test_fonts_and_license_only(self):
        names = sorted(p.name for p in (QSITE / "site" / "fonts").iterdir())
        self.assertEqual(names, ["OFL.txt", "OpenSans-Bold.woff2", "OpenSans-BoldItalic.woff2",
                                 "OpenSans-Italic.woff2", "OpenSans-Regular.woff2"])
        self.assertFalse((QSITE / "site" / "brand").exists())

    def test_no_markdown_published(self):
        self.assertEqual([p.relative_to(QSITE).as_posix() for p in QSITE.rglob("*.md")], [])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run them to verify they fail**

Run the builds, then `python -m unittest tests.test_quarto_config tests.test_quarto_chrome -v`.
Expected: `Version` errors with `AttributeError: module 'quarto_build' has no attribute 'QUARTO_VERSION'`. `test_math_is_mathml`, `test_one_nav_and_no_search`, `test_flat_body` and `test_resources_exact` fail. `Navigation` fails because `id="quarto-header"` is present. `Published` fails on `README.md` and `site/brand`. The other `Pins` tests pass already.

- [ ] **Step 3: Implement**

Replace `_quarto.yml` with:

```yaml
# Quarto build (D-0033). Run it only through tools/quarto_build.py, which
# checks the Quarto version, generates the pages listed under render, and
# dresses them with the old build's chrome (D-0036).
# The render list is explicit: without it Quarto would render every
# Markdown file in the repo, including the ledgers and the curriculum
# sources themselves.
project:
  type: website
  output-dir: build/quarto-site
  render:
    - index.qmd
    - courses/index.qmd
    - how-this-was-made/index.qmd
    - sims/index.qmd
    - labs/**/*.qmd
  # Fonts and their license only (D-0039). The logo travels embedded in
  # each page, so no logo file is published; READMEs stay in the repo.
  resources:
    - site/fonts/OpenSans-Regular.woff2
    - site/fonts/OpenSans-Bold.woff2
    - site/fonts/OpenSans-Italic.woff2
    - site/fonts/OpenSans-BoldItalic.woff2
    - site/fonts/OFL.txt

website:
  title: "Physics Lab Library"
  # One nav, the OSU header's (D-0037). Search stays off until ruled.
  search: false

format:
  html:
    # Never Cosmo or another theme that imports a remote font (D-0033).
    theme: default
    css: site/site.css
    lang: en
    # As the Pandoc build: no smart quotes, so words match the originals.
    from: markdown-smart
    # Flat body (D-0036): no section wrappers, no anchor markup, lines
    # wrapped as Pandoc wraps them. With these, <main> holds the old
    # build's bytes.
    section-divs: false
    anchor-sections: false
    wrap: auto
    # MathML needs no script; Quarto's default fetches MathJax from a CDN
    # (D-0040).
    html-math-method: mathml
    # Every page carries its own <h1>, the "#" heading of its Markdown.
    # Quarto would draw a second one from the title metadata: this style only
    # strips the block's styling, so the empty partial below is what removes
    # the drawn title. The title still sets the <title> element.
    title-block-style: none
    template-partials:
      - title-block.html
    include-in-header:
      text: '<meta name="robots" content="noindex, nofollow">'
```

In `tools/quarto_build.py`, after the `WARNING` line, add:

```python
QUARTO_VERSION = "1.10.18"


def check_version(reported):
    """Fail unless Quarto reports exactly the pinned version (D-0033)."""
    if reported.strip() != QUARTO_VERSION:
        raise SystemExit(
            "Quarto {} is pinned; this Quarto reports {!r}. Upgrade the pin on "
            "purpose, in its own PR.".format(QUARTO_VERSION, reported.strip()))


def quarto_version():
    return subprocess.run([QUARTO, "--version"], capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout
```

Make `build()` call it first:

```python
def build():
    check_version(quarto_version())
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    generate()
    run_quarto()
    post()
```

Update the module docstring's "Requires Quarto 1.10.18" sentence to say the driver checks it.

- [ ] **Step 4: Run them to verify they pass**

Run the verify sequence. Expected: the full suite passes (45 existing plus the new ones), and the Quarto build prints no warning line. The chrome contract on Quarto still fails as before: 5 of 9 not passing. If `quarto-search` still appears in pages with `search: false`, stop and report it; do not loosen the test.

- [ ] **Step 5: Commit**

```bash
git add _quarto.yml tools/quarto_build.py tests/test_quarto_config.py tests/test_quarto_chrome.py
git commit -m "Pin the Quarto config and version; one nav, fonts only" -m "D-0036 body settings, D-0037 no navbar or search, D-0039 exact resources, D-0040 MathML. The driver refuses any Quarto but 1.10.18, and a test holds CI's install to the same pin."
```

---

### Task 2: Lift the old chrome; dress a Quarto page

A pure module plus one behavior-preserving refactor in `render.py`. Nothing in the build calls the module yet.

Evidence (probe, 2026-09-30, Pandoc 3.11): `old_chrome`'s exact arguments, run on an empty body, gave a body class, top and bottom byte-identical to the old build's on both lab pages, the course index, the method page and the landing page. Each top is about 235 KB, almost all of it the embedded logo.

**Files:**
- Modify: `tools/render.py` (add `LANDING_FOOTNOTE`, `METHOD_FOOTNOTE`, `document_extras`; `build_site` uses them)
- Create: `tools/quarto_chrome.py`
- Create: `tests/test_quarto_dress.py`

**Interfaces:**
- Produces in `render.py`: `LANDING_FOOTNOTE: str`, `METHOD_FOOTNOTE: str` (the exact strings `build_site` passes today), `document_extras(theme: str, depth: int = 3) -> list[str]` (the four `-M` pairs `build_site` passes today for `uphref`, `uplabel`, `switchhref`, `switchlabel`).
- Produces in `quarto_chrome.py`:
  - `Page`: a dict `{"html": str, "kind": "site" | "doc", "depth": int, "theme": str | None, "footnote": str}`. `html` is the page's path under the output folder, with forward slashes.
  - `old_chrome(page) -> (body_class: str, top: str, bottom: str)`. `top` is the old template's output between `<body class="...">\n` and `<main>`; `bottom` is what lies between `</main>\n` and `</body>`.
  - `dress(quarto_html: str, body_class: str, top: str, bottom: str) -> str`.
  - Constants `QMAIN`, `QBODY` (compiled regexes) and `QCONTENT_END: str`.
  - `dress` raises `ValueError` if Quarto's `<main>` shape, the `<body class=...>` tag or the content-div end is not found exactly once.

- [ ] **Step 1: Prove the refactor's baseline**

Write `<scratchpad>/tree_hash.py`:

```python
import hashlib, os, sys
root = sys.argv[1]
h = hashlib.sha256()
for d, dirs, files in os.walk(root):
    dirs.sort()
    for f in sorted(files):
        p = os.path.join(d, f)
        h.update(os.path.relpath(p, root).replace(os.sep, "/").encode())
        h.update(open(p, "rb").read())
print(h.hexdigest())
```

Run `python tools/render.py --site` then `python <scratchpad>/tree_hash.py build/site` and keep the hash.

- [ ] **Step 2: Write the failing tests**

Create `tests/test_quarto_dress.py`:

```python
"""tools/quarto_chrome.py: the old chrome lifted, and a Quarto page dressed
(D-0036, D-0038). Needs Pandoc (PANDOC), not a build.
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import quarto_chrome                      # noqa: E402
import render                             # noqa: E402

# The shape Quarto 1.10.18 writes, cut down (real lines from build/quarto-site).
SKELETON = (
    '<!DOCTYPE html>\n<html><head><title>t</title></head>\n'
    '<body class="fullcontent quarto-light">\n\n'
    '<div id="quarto-content" class="quarto-container page-columns">\n'
    '<main class="content" id="quarto-document-content">'
    '<header id="title-block-header" class="quarto-title-block"></header>\n\n\n'
    '<h1 id="x">X</h1>\n<p>Body.</p>\n\n'
    '</main> <!-- /main -->\n<script>var mailtoRegex;</script>\n'
    '</div> <!-- /content -->\n\n</body></html>\n')
TOP = '<div class="top">T</div>\n'
BOTTOM = '<footer class="b">B</footer>\n'


def dressed(page=SKELETON):
    return quarto_chrome.dress(page, "site-page", TOP, BOTTOM)


class Dress(unittest.TestCase):

    def test_main_made_bare(self):
        out = dressed()
        self.assertIn('<main>\n<h1 id="x">X</h1>\n<p>Body.</p>\n</main>', out)
        self.assertNotIn("title-block-header", out)
        self.assertNotIn("quarto-document-content", out)

    def test_top_right_after_body(self):
        self.assertIn('<body class="site-page fullcontent quarto-light">\n<div class="top">T</div>\n',
                      dressed())

    def test_bottom_right_after_content_div(self):
        out = dressed()
        self.assertIn('</div> <!-- /content -->\n<footer class="b">B</footer>\n', out)
        self.assertGreater(out.index("<footer"), out.index("</main>"))

    def test_anchor_missing_or_doubled_fails(self):
        broken = {
            "no main shape": SKELETON.replace('<main class="content"', "<main"),
            "no body class": SKELETON.replace('<body class="fullcontent quarto-light">', "<body>"),
            "two content ends": SKELETON.replace(quarto_chrome.QCONTENT_END,
                                                 quarto_chrome.QCONTENT_END * 2),
        }
        for what, page in broken.items():
            with self.subTest(case=what):
                with self.assertRaises(ValueError):
                    dressed(page)


class OldChrome(unittest.TestCase):

    def test_document_page(self):
        body_class, top, bottom = quarto_chrome.old_chrome(
            {"html": "labs/x/modern/index.html", "kind": "doc", "depth": 3,
             "theme": "modern", "footnote": ""})
        self.assertEqual(body_class, "theme-modern")
        for piece in ('<div class="draft-banner">', '<header class="osu-header">',
                      '<nav class="site-nav">', '<a class="switch" href="../faithful/">',
                      'src="data:image/png;base64,'):
            self.assertIn(piece, top)
        self.assertIn(render.BANNER_MAIN, " ".join(top.split()))
        self.assertIn('<footer class="doc-footer">', bottom)
        self.assertIn('<footer class="osu-foot">', bottom)

    def test_site_page_with_footnote(self):
        body_class, top, bottom = quarto_chrome.old_chrome(
            {"html": "how-this-was-made/index.html", "kind": "site", "depth": 1,
             "theme": None, "footnote": render.METHOD_FOOTNOTE})
        self.assertEqual(body_class, "site-page")
        self.assertNotIn("site-nav", top)
        self.assertIn('<div class="site-foot">', bottom)
        self.assertIn("VISION.md", bottom)

    def test_site_page_without_footnote(self):
        _, _, bottom = quarto_chrome.old_chrome(
            {"html": "index.html", "kind": "site", "depth": 0, "theme": None, "footnote": ""})
        self.assertNotIn("site-foot", bottom)
        self.assertIn('<footer class="osu-foot">', bottom)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run them to verify they fail**

Run `python -m unittest tests.test_quarto_dress -v`.
Expected: an import error, `ModuleNotFoundError: No module named 'quarto_chrome'`.

- [ ] **Step 4: Refactor `render.py` without changing behavior**

After `THEME_NOTE`, add:

```python
# Footnotes on two site pages. The landing one names the old build, so the
# Quarto build does not carry it (D-0038).
LANDING_FOOTNOTE = ("This site is built from the repository "
                    "OSU-physics-lab-library with Pandoc and one build script.")
METHOD_FOOTNOTE = ("This page is built from VISION.md in the project's "
                   "repository; ledger numbers refer to the dated decision "
                   "ledger kept there.")
```

After `up()`, add:

```python
def document_extras(theme, depth=3):
    """The document nav's metadata: the course index link and the switch."""
    other = THEMES[0] if theme == THEMES[1] else THEMES[1]
    return [
        "-M", "uphref=" + up(depth) + "courses/",
        "-M", "uplabel=Course index",
        "-M", "switchhref=" + up(1) + other + "/",
        "-M", "switchlabel=Read it " + THEME_LABEL[other].lower(),
    ]
```

In `build_site`, delete the `other = ...` line, pass `extra=document_extras(theme)` to `render(...)`, and replace the two inline footnote strings with `LANDING_FOOTNOTE` and `METHOD_FOOTNOTE`.

Run `python tools/render.py --site` and the tree hash again. Expected: the same hash as Step 1. If it differs, undo and find out why before going on.

- [ ] **Step 5: Write `tools/quarto_chrome.py`**

```python
"""The old build's chrome, lifted for the Quarto pages (D-0036, D-0038).

The chrome is not copied. Each piece is rendered from the old templates,
tools/template.html and tools/template-site.html (with the brand partials
beside them), by Pandoc with an empty body and the metadata tools/render.py
passes, then cut at <main>. Phase 4 moves the templates when it retires the
old build. The Quarto shapes below are Quarto 1.10.18's; the driver pins
that version, and dress() fails loudly if a shape is not found exactly once.
"""

import os
import re

import render

OLD = re.compile(r'<body class="([^"]*)">\n(.*?)<main>.*?</main>\n(.*?)</body>', re.S)
QMAIN = re.compile(
    r'<main class="content" id="quarto-document-content">'
    r'<header id="title-block-header" class="quarto-title-block"></header>'
    r'(.*?)</main> <!-- /main -->', re.S)
QBODY = re.compile(r'<body class="([^"]*)">')
QCONTENT_END = "</div> <!-- /content -->"


def css_path(*parts):
    """Absolute, so --embed-resources finds it, as render.py does."""
    return os.path.join(render.ROOT, *parts).replace(os.sep, "/")


def old_chrome(page):
    """(body_class, top, bottom) for one page, from the old template.

    The arguments mirror render.render() and render.render_page(), including
    --embed-resources: that is what turns the logo path in render.site_vars
    into the data: URI the logo test checks. Passing the data URI itself
    would not work: at about 234 KB it exceeds the Windows command-line
    limit of 32767 characters.
    """
    cmd = [render.PANDOC, "-f", "markdown-smart", "-t", "html5", "--standalone",
           "--embed-resources", "-M", "pagetitle=chrome",
           "-M", "chromecss=" + css_path("site", "site.css")]
    if page["kind"] == "doc":
        theme = page["theme"]
        cmd += ["--template", os.path.join(render.ROOT, "tools", "template.html"),
                "-M", "theme=" + theme,
                "-M", "css=" + css_path("themes", theme + ".css"),
                "-M", "presentationnote=" + render.THEME_NOTE[theme]]
        cmd += render.site_vars(page["depth"]) + render.document_extras(theme, page["depth"])
    else:
        cmd += ["--template", os.path.join(render.ROOT, "tools", "template-site.html"),
                "-M", "footnote=" + page["footnote"]]
        cmd += render.site_vars(page["depth"])
    out = render.run(cmd, input="", capture_output=True, text=True, encoding="utf-8").stdout
    m = OLD.search(out)
    if m is None:
        raise ValueError("old template gave no <body>...<main> shape for " + page["html"])
    return m.group(1), m.group(2), m.group(3)


def once(pattern, text, what):
    found = list(pattern.finditer(text))
    if len(found) != 1:
        raise ValueError("{}: expected exactly one, found {}".format(what, len(found)))
    return found[0]


def dress(quarto_html, body_class, top, bottom):
    """A Quarto page with the old chrome: bare <main>, top chrome right after
    <body>, bottom chrome right after Quarto's content div."""
    m = once(QMAIN, quarto_html, "Quarto <main>")
    text = (quarto_html[:m.start()] + "<main>\n" + m.group(1).strip() + "\n</main>"
            + quarto_html[m.end():])
    b = once(QBODY, text, "<body class=...>")
    text = (text[:b.start()] + '<body class="{} {}">\n'.format(body_class, b.group(1))
            + top.rstrip("\n") + text[b.end():])
    e = once(re.compile(re.escape(QCONTENT_END)), text, "Quarto content div end")
    return text[:e.end()] + "\n" + bottom + text[e.end():]
```

- [ ] **Step 6: Run the tests to verify they pass**

Run the verify sequence. Expected: everything passes as at the end of Task 1, plus `test_quarto_dress` (7 tests). The chrome contract on Quarto is unchanged (5 of 9 not passing).

- [ ] **Step 7: Commit**

```bash
git add tools/render.py tools/quarto_chrome.py tests/test_quarto_dress.py
git commit -m "Lift the old chrome from its templates for the Quarto pages" -m "D-0036, D-0038. quarto_chrome renders template.html and template-site.html with an empty body and render.py's own metadata, then cuts at <main>, so the chrome has one source until phase 4. render.py gains named footnotes and document_extras; build/site is byte-identical before and after (tree hash)."
```

---

### Task 3: The driver dresses every page

**Files:**
- Modify: `tools/quarto_build.py` (`generate()` returns the page manifest; new `dress_pages(pages)`; `build()` calls it after `run_quarto()`)
- Modify: `tests/test_quarto_chrome.py` (add `ChromeParity` and `MainBare`; add `test_one_osu_nav` to `Navigation`)

**Interfaces:**
- Consumes: `quarto_chrome.old_chrome(page)`, `quarto_chrome.dress(...)`, `render.METHOD_FOOTNOTE` (Task 2).
- Produces: `quarto_build.generate() -> list[Page]` (Task 2's `Page` dict); `quarto_build.dress_pages(pages: list[Page]) -> None`.

- [ ] **Step 1: Write the failing tests**

Add to the imports of `tests/test_quarto_chrome.py`:

```python
import base64
import hashlib
```

Add to class `Navigation`:

```python
    def test_one_osu_nav(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                self.assertEqual(text.count('<nav class="osu-nav"'), 1)
```

Add these helpers after `chrome_pages()`:

```python
LOGO = re.compile(r'src="data:image/png;base64,([^"]+)"')


def logo_by_digest(fragment):
    """Compare embedded images by their decoded bytes, not their encoding."""
    return LOGO.sub(lambda m: 'src="sha256:{}"'.format(
        hashlib.sha256(base64.b64decode(m.group(1))).hexdigest()), fragment)


def old_parts(text):
    m = re.search(r'<body class="([^"]*)">\n(.*?)<main>.*?</main>\n(.*?)</body>', text, re.S)
    return m.group(1), m.group(2), m.group(3)


def new_parts(text):
    body = re.search(r'<body class="([^"]*)">\n', text)
    end = "</div> <!-- /content -->\n"
    after = text.index(end) + len(end)
    return body.group(1), text[body.end():text.index("<main>")], text[after:text.index("</body>")]
```

Add these classes:

```python
class ChromeParity(unittest.TestCase):
    """D-0036, D-0038: every Quarto page carries the old page's chrome."""

    def test_every_page_has_an_old_twin(self):
        rels = [rel for rel, _ in chrome_pages()]
        self.assertGreaterEqual(len(rels), 6)
        for rel in rels:
            with self.subTest(page=rel):
                self.assertTrue((OLD / rel).is_file())

    def test_body_class_carried(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                want = old_parts((OLD / rel).read_text(encoding="utf-8"))[0]
                self.assertTrue(new_parts(text)[0].startswith(want + " "))

    def test_top_chrome_matches_old_build(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                want = old_parts((OLD / rel).read_text(encoding="utf-8"))[1].rstrip("\n")
                got = new_parts(text)[1]
                self.assertTrue(logo_by_digest(got).startswith(logo_by_digest(want)))

    def test_bottom_chrome_matches_old_build(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                want = old_parts((OLD / rel).read_text(encoding="utf-8"))[2]
                if rel == "index.html":
                    # D-0038: the landing footnote names the old build.
                    want = re.sub(r'<div class="site-foot">.*?</div>\n', "", want, flags=re.S)
                self.assertEqual(new_parts(text)[2].strip(), want.strip())

    def test_landing_footnote_not_carried(self):
        self.assertNotIn("one build script", (QSITE / "index.html").read_text(encoding="utf-8"))


class MainBare(unittest.TestCase):
    """D-0036: one bare <main>, no empty title block."""

    def test_main_is_bare(self):
        for rel, text in chrome_pages():
            with self.subTest(page=rel):
                self.assertEqual(text.count("<main>"), 1)
                self.assertNotIn("<main ", text)
                self.assertNotIn("title-block-header", text)
```

- [ ] **Step 2: Run them to verify they fail**

Rebuild both, then `python -m unittest tests.test_quarto_chrome -v`.
Expected: `test_every_page_has_an_old_twin` passes. The other parity tests and `MainBare` fail (`new_parts` errors on `.index("<main>")` with `ValueError`). `test_one_osu_nav` fails with count 0.

- [ ] **Step 3: Implement**

In `tools/quarto_build.py`, add `import quarto_chrome` after `import render`. Make `generate()` build and return the manifest. Keep its existing body, and add:

```python
    pages = [
        {"html": "index.html", "kind": "site", "depth": 0, "theme": None, "footnote": ""},
        {"html": "courses/index.html", "kind": "site", "depth": 1, "theme": None, "footnote": ""},
        {"html": "how-this-was-made/index.html", "kind": "site", "depth": 1, "theme": None,
         "footnote": render.METHOD_FOOTNOTE},
        {"html": "sims/index.html", "kind": "site", "depth": 1, "theme": None, "footnote": ""},
    ]
```

Inside the existing per-document loop, after `write(page, ...)`:

```python
            pages.append({"html": "labs/{}/{}/index.html".format(doc_id, theme),
                          "kind": "doc", "depth": 3, "theme": theme, "footnote": ""})
```

At the end of `generate()`, add `return pages`. Then add:

```python
def dress_pages(pages):
    """Put the old build's chrome on every rendered page (D-0036)."""
    for page in pages:
        path = os.path.join(OUT, *page["html"].split("/"))
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        body_class, top, bottom = quarto_chrome.old_chrome(page)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(quarto_chrome.dress(text, body_class, top, bottom))
```

and change `build()` to:

```python
def build():
    check_version(quarto_version())
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    pages = generate()
    run_quarto()
    dress_pages(pages)
    post()
```

- [ ] **Step 4: Run the tests to verify they pass**

Run the verify sequence. Expected: the full suite passes. The chrome contract on Quarto now passes 8 of 9: `test_logo_unaltered_and_linked`, `test_top_strip_links_department`, `test_draft_banner_and_noindex` and `test_bodies_unchanged` pass with no edit. `test_footer_as_ruled` fails only on `mailto:` (D-0041), on all six pages.

If a parity test fails, compare the two fragments; do not loosen the test. A likely cause is Pandoc writing an attribute differently under `--embed-resources`. If that happens, fix `old_chrome` and report it in the task notes.

- [ ] **Step 5: Commit**

```bash
git add tools/quarto_build.py tests/test_quarto_chrome.py
git commit -m "Dress every Quarto page with the old build's chrome" -m "D-0036, D-0038. The driver lifts each page's chrome from the old template and inserts it around a bare <main>. Chrome suite on Quarto: 8 of 9 pass with no test edited, including test_bodies_unchanged against its original fixture; test_footer_as_ruled fails only on Quarto's inline mailto: regex (D-0041)."
```

---

### Task 4: Layout parity in `site/site.css`

The pages now carry the right markup. Bootstrap and Quarto's page grid still style it differently from the old build. Close the gap with rules that only Quarto pages can match, measured against the old build.

**Files:**
- Modify: `site/site.css` (one delimited block at the end of the screen rules, before the `@page` print section)
- Create: `tools/measure_chrome.js`
- Modify: `tests/test_quarto_chrome.py` (add `QuartoOnlyCss`)

**Interfaces:**
- Produces: a block in `site/site.css` between the lines `/* quarto-only: start (D-0036) */` and `/* quarto-only: end */`. Every selector in it contains `#quarto-content` or `.quarto-light`, which exist only on Quarto pages.
- Produces: `tools/measure_chrome.js`, a manual measurement that returns JSON with keys `diffs`, `scroll375`, `banner1440`, `landing1440`, `contrast` and `sim`.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_quarto_chrome.py`:

```python
class QuartoOnlyCss(unittest.TestCase):
    """Rules added for Quarto must not reach the old build, which shares
    site/site.css and is still production."""

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
```

- [ ] **Step 2: Run it to verify it fails**

Run `python -m unittest tests.test_quarto_chrome.QuartoOnlyCss -v`. Expected: FAIL, "no quarto-only block".

- [ ] **Step 3: Add the block's first rule**

Before the `@page` section of `site/site.css`, add:

```css
/* quarto-only: start (D-0036) */
/* Quarto pages put the old chrome and a bare <main> inside Quarto's page
   grid, which the old layout never had. Selectors here name markup only
   Quarto writes, so the old build is not affected. */
#quarto-content { display: block; }
/* quarto-only: end */
```

Run the verify sequence. Expected: everything green, including `QuartoOnlyCss` and `test_brand.py`'s palette check.

- [ ] **Step 4: Create the measurement**

Create `tools/measure_chrome.js`:

```js
// Manual layout check for the Quarto migration (phase 2). CI does not run it.
// Serve both builds from one origin, on a port not used before in the session
// (the pane caches per origin):
//   python -m http.server <port> --directory <absolute path to build>
// Open http://127.0.0.1:<port>/quarto-site/ in the browser pane and run this
// file's text with the pane's JavaScript tool. It loads every page of both
// builds in same-origin iframes at fixed sizes and returns JSON:
//   diffs        computed-style and box differences, old build versus Quarto
//   scroll375    each Quarto page's scrollWidth at 375 px (want <= 375)
//   banner1440   draft banner height, closed and open, at 1440 px
//   landing1440  the landing prose column's left and right gaps at 1440 px
//   contrast     WCAG ratios of the chrome text on its background
//   sim          the sim bar and page height at 1280x720
await (async () => {
  const LAB = "labs/ph211-team-building-handout/";
  const PAGES = ["index.html", "courses/index.html", "how-this-was-made/index.html",
    "sims/index.html", LAB + "modern/index.html", LAB + "faithful/index.html"];
  const SIM = "sims/modified-electric-force/index.html";
  const SEL = [".draft-banner", ".draft-banner summary", ".osu-strip", ".osu-strip a",
    ".osu-banner", ".osu-logo img", ".osu-sitename", ".osu-nav", ".osu-nav a", "main",
    "main h1", "main h2", "main p", "main li", ".hero", ".hero .lead", ".hero .button",
    ".link-cards li", ".lab-list > li", ".site-nav", ".site-nav a", ".doc-footer",
    ".site-foot", ".osu-foot", ".osu-foot a"];
  const PROPS = ["font-family", "font-size", "font-weight", "line-height", "color",
    "background-color", "margin-top", "margin-bottom", "padding-top", "padding-bottom"];
  const frame = (src, w, h) => new Promise(done => {
    const f = document.createElement("iframe");
    f.style.cssText = `position:absolute;left:-20000px;top:0;border:0;width:${w}px;height:${h}px`;
    f.onload = async () => { await f.contentDocument.fonts.ready; done(f); };
    f.src = src + "?m=" + Date.now();
    document.body.appendChild(f);
  });
  const css = el => el.ownerDocument.defaultView.getComputedStyle(el);
  const snap = doc => Object.fromEntries(SEL.map(s => {
    const el = doc.querySelector(s);
    if (!el) return [s, null];
    const r = el.getBoundingClientRect(), cs = css(el);
    return [s, Object.assign(Object.fromEntries(PROPS.map(p => [p, cs.getPropertyValue(p)])),
      {left: Math.round(r.left), width: Math.round(r.width), height: Math.round(r.height)})];
  }));
  const lum = c => {
    const [r, g, b] = c.match(/[\d.]+/g).slice(0, 3).map(Number).map(v => {
      v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const back = el => {
    for (; el; el = el.parentElement) {
      const c = css(el).backgroundColor;
      if (!/^rgba\(.*,\s*0\)$|^transparent$/.test(c)) return c;
    }
    return "rgb(255, 255, 255)";
  };
  const ratio = el => {
    if (!el) return null;
    const [a, b] = [lum(css(el).color), lum(back(el))].sort((x, y) => y - x);
    return Math.round((a + 0.05) / (b + 0.05) * 100) / 100;
  };
  const out = {diffs: {}, scroll375: {}, banner1440: {}, landing1440: null, contrast: {}, sim: null};
  for (const page of PAGES) {
    for (const [w, h] of [[1440, 900], [375, 812]]) {
      const a = await frame("/site/" + page, w, h), b = await frame("/quarto-site/" + page, w, h);
      const sa = snap(a.contentDocument), sb = snap(b.contentDocument), d = [];
      for (const s of SEL) {
        if (JSON.stringify(sa[s]) === JSON.stringify(sb[s])) continue;
        if (!sa[s] || !sb[s]) { d.push([s, sa[s] ? "missing in quarto" : "only in quarto"]); continue; }
        for (const k of Object.keys(sa[s])) if (sa[s][k] !== sb[s][k]) d.push([s, k, sa[s][k], sb[s][k]]);
      }
      if (d.length) out.diffs[page + " @" + w] = d;
      const q = b.contentDocument;
      if (w === 375) out.scroll375[page] = q.documentElement.scrollWidth;
      if (w === 1440) {
        const banner = q.querySelector(".draft-banner"), det = banner.querySelector("details");
        const closed = Math.round(banner.getBoundingClientRect().height);
        det.open = true;
        const opened = Math.round(banner.getBoundingClientRect().height);
        det.open = false;
        out.banner1440[page] = {closed, opened};
        out.contrast[page] = {
          banner: ratio(q.querySelector(".draft-banner strong")),
          sitename: ratio(q.querySelector(".osu-sitename")),
          heroTitle: ratio(q.querySelector(".hero h1")),
          heroLead: ratio(q.querySelector(".hero .lead p")),
          heroButton: ratio(q.querySelector(".hero .button.primary")),
        };
        if (page === "index.html") {
          const r = q.querySelector("main > p").getBoundingClientRect();
          out.landing1440 = {selector: "main > p", left: Math.round(r.left), right: Math.round(w - r.right)};
        }
      }
      a.remove(); b.remove();
    }
  }
  const s = await frame("/quarto-site/" + SIM, 1280, 720), sd = s.contentDocument.documentElement;
  out.sim = {bar: Math.round(s.contentDocument.querySelector(".lib-bar").getBoundingClientRect().height),
             page: sd.scrollHeight, fits: sd.scrollHeight <= 720};
  s.remove();
  return JSON.stringify(out, null, 1);
})();
```

- [ ] **Step 5: Measure, fix, repeat until `diffs` is empty**

Each round:

1. Run `python tools/render.py --site` and `python tools/quarto_build.py`.
2. Start `python -m http.server <new port> --directory <absolute path to build>` in the background, from the repo root. Use a new port every round.
3. Open `http://127.0.0.1:<port>/quarto-site/` in the browser pane. Confirm the page's stylesheet holds the newest rule: fetch `/quarto-site/site/site.css` in the pane and look for it.
4. Run `tools/measure_chrome.js`. Read `diffs`.
5. For each difference, add one rule inside the quarto-only block whose selector carries `.quarto-light` or `#quarto-content`. For example, if `main p` differs in `font-size` because Bootstrap sets the body size, write `body.quarto-light.site-page main p { ... }` with the old build's computed value expressed through the existing tokens (`var(--...)`). Never a new color literal: `test_brand.py`'s palette check must stay green.
6. Stop the server.

Done when `diffs` is `{}` at both widths on all six pages. Then open each Quarto page directly in the pane and read its console with `read_console_messages` (`onlyErrors: true`): there must be no error. A Quarto script that breaks because `<main>` lost its id is a finding. Report it; do not restore the id.

If a difference cannot be closed by a scoped rule, stop and report it with both values. Do not widen the selector scope.

- [ ] **Step 6: Commit**

```bash
git add site/site.css tools/measure_chrome.js tests/test_quarto_chrome.py
git commit -m "Match the Quarto pages' layout to the old build" -m "D-0036. A delimited quarto-only block in site.css, every selector naming markup only Quarto writes (tested), closes the computed-style differences tools/measure_chrome.js found at 1440 and 375 px to zero. No console errors on any Quarto page."
```

---

### Task 5: Re-measure what STATE.md records

**Files:**
- Modify: `STATE.md` (a new "Measurements (Quarto build, <date>)" block above the 2026-09-22 one)

**Interfaces:**
- Consumes: `tools/measure_chrome.js` (Task 4).

- [ ] **Step 1: Run the measurement on a fresh build and a new port**

Follow Task 4 Step 5, items 1 to 4. Keep the full JSON in the session notes.

- [ ] **Step 2: Page weights**

Write `<scratchpad>/page_weight.py`:

```python
import os, re
OLD, NEW = "build/site", "build/quarto-site"
PAGES = ["index.html", "courses/index.html", "how-this-was-made/index.html", "sims/index.html",
         "labs/ph211-team-building-handout/modern/index.html",
         "labs/ph211-team-building-handout/faithful/index.html"]
for rel in PAGES:
    page = os.path.join(NEW, rel)
    text = open(page, encoding="utf-8").read()
    refs = set(re.findall(r'<(?:link|script)\b[^>]*(?:href|src)="([^"#?:]+)"', text))
    files = {os.path.normpath(os.path.join(os.path.dirname(page), r)) for r in refs}
    files = {f for f in files if os.path.isfile(f)}
    fonts = [os.path.join(NEW, "site", "fonts", f) for f in os.listdir(os.path.join(NEW, "site", "fonts"))
             if f.endswith(".woff2")]
    first = os.path.getsize(page) + sum(os.path.getsize(f) for f in files | set(fonts))
    print("{}: old {} B; quarto page {} B, first visit with every linked file and all four fonts {} B".format(
        rel, os.path.getsize(os.path.join(OLD, rel)), os.path.getsize(page), first))
```

Run it from the repo root. The "first visit" figure is an upper bound: a browser fetches only the font faces a page uses.

- [ ] **Step 3: Record**

In `STATE.md`, add a block with the date and, from the JSON and the script, word for word:

- Sim bar at 1280x720: bar px, page px, fits.
- Phone width 375 px: scrollWidth for each of the six pages.
- Draft banner at 1440 px: closed and open px.
- Landing prose column at 1440 px: left and right px (selector `main > p`).
- Contrast (computed from the rendered page with the WCAG formula): banner, site name, hero title, hero lead, hero button.
- Page weights per page: old, Quarto page, Quarto first visit.

Compare each with the 2026-09-21 and 2026-09-22 numbers. Do not tune anything to match them. Any value that differs goes in the PR description with both numbers, for the owner. An empty `diffs` in Task 4 means the two builds agree today. The older numbers may themselves have moved since they were taken.

- [ ] **Step 4: Commit**

```bash
git add STATE.md
git commit -m "Record the Quarto build's measurements" -m "Sim bar at 1280x720, 375 px scroll width on six pages, banner and landing column at 1440 px, chrome contrast from the rendered page, and page weights old versus Quarto (tools/measure_chrome.js plus a weight script; method in STATE.md)."
```

---

### Task 6: The chrome contract gates `verify`

Starts only after D-0041 is ruled (see Gates).

**Files:**
- Modify: `tests/test_site_chrome.py` (D-0041's one line)
- Modify: `.github/workflows/verify.yml`
- Modify: `CLAUDE.md`, `docs/quarto-migration-plan.md`, `STATE.md`

- [ ] **Step 1: Confirm the failure D-0041 addresses**

Run `SITE_DIR=build/quarto-site python -m unittest tests.test_site_chrome -v`.
Expected: 8 pass; `test_footer_as_ruled` fails on all six pages, each with `'mailto:' unexpectedly found`. Any other failure means stop.

- [ ] **Step 2: Apply D-0041 exactly as ruled**

In `test_footer_as_ruled`, change only the banned-string loop:

```python
                for banned in ("mailto:", "tel:", "&copy;", "©", "Copyright"):
                    self.assertNotIn(banned, re.sub(r"<script\b.*?</script>", "", text, flags=re.S))
```

If the owner ruled a different wording, apply that instead. Run the verify sequence. Expected: the chrome contract on Quarto passes 9 of 9, and on the old build it still passes 9 of 9.

- [ ] **Step 3: Move the contract into `verify`**

In `.github/workflows/verify.yml`, add after the `Tests` step of the `verify` job:

```yaml
      - name: Chrome contract against the Quarto build
        # Phase 2 exit (D-0042): the brand contract gates the Quarto build.
        env:
          SITE_DIR: build/quarto-site
        run: python3 -m unittest discover -s tests -p test_site_chrome.py -v
```

Delete the whole `chrome-on-quarto` job.

- [ ] **Step 4: Docs**

- `CLAUDE.md`, the Quarto bullet in Build:
  - The driver checks the version and dresses pages from the old templates (D-0036); never hand-edit the chrome in a Quarto page, and never copy the templates.
  - The three body settings, the bare `<main>`, and the quarto-only CSS block with its test.
  - No navbar or search (D-0037); MathML (D-0040).
  - `tools/measure_chrome.js` and how to run it.
  - Delete the sentence calling MathJax "a phase 2 item".
- `docs/quarto-migration-plan.md`: mark phase 2 done with the PR number, and point to this plan.
- `STATE.md`: focus is phase 2 merged, the test count, and the next phase.

- [ ] **Step 5: Commit, push, PR**

```bash
git add tests/test_site_chrome.py .github/workflows/verify.yml CLAUDE.md docs/quarto-migration-plan.md STATE.md
git commit -m "Gate verify on the chrome contract against Quarto" -m "D-0041 as ruled: the footer test looks for contact links outside script blocks, since Quarto writes a mailto: regex in its own link handler. D-0042: the chrome suite runs in verify against build/quarto-site; the non-blocking job goes. No brand test dropped."
git push -u origin quarto-phase-2
```

Open the PR with the test counts, the Task 5 numbers and any differences from the earlier numbers. Squash merge on green `verify`, then `git branch -D quarto-phase-2`.

---

## Declined

- **`minimal: true`.** Probed 2026-09-30: it drops Bootstrap, and with it `<main>` and Quarto's content div. It also drops the site features (search, sidebar, listings) that D-0033 moved for.
- **Quarto's `website.announcement` as the draft banner.** The wording would need a second home in `_quarto.yml`, it is dismissable by script, and it changes the D-0030 markup the tests pin.
- **`include-before-body` for the header.** It lands inside `<main>` (probe).
- **Copying the chrome markup into a new file.** Two copies that drift until phase 4. Lifting it from the templates costs one Pandoc call per page.
- **Re-pinning `main-bodies.json` to Quarto's output.** That would weaken the evidence; the original fixture passes.
- **The logo as a file reference.** That is a test edit for page weight; D-0039 keeps the test.
- **Hosting MathJax in the repo, or `plain` math.** Size and upkeep, or unreadable math.
- **Stripping Quarto's `mailto:` script.** It breaks Quarto's link handling; D-0041 is proposed instead.
- **Quarto's navbar, or both navs; search now.** D-0037.
- **Carrying the landing footnote.** It is false under Quarto (D-0038).
- **Publishing the READMEs.** These are maintainer notes (D-0039).
- **Automating the layout measurement in CI.** It would need a browser toolchain in CI for a check that runs once per chrome change. The script is committed so a successor can rerun it.

## Not in this plan

- The owner's print check of Lab 1 and the first look at the live banner and landing (STATE.md, awaiting owner).
- The two unruled design items: nav into the orange bar, and a new hero headline.
- Sims stay without a noindex meta (source plus bar only, LEDGER 51); `robots.txt` covers them.
- Quarto's `<title>` gains the site title as a suffix ("Course index", followed by a separator and "Physics Lab Library"). It is untested and was not raised; a question for the owner, not a fix here.
- One Pandoc (phase 3), retiring the old build and moving the templates (phase 4), and the Cloudflare deploy and its owner-created token (phase 5, D-0034). Search, listings and downloads come later.
