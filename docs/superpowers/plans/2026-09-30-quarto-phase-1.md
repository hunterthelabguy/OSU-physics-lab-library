# Quarto Migration Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the whole site with Quarto into `build/quarto-site/`, beside the untouched old build, with a blocking test suite that proves the Quarto output keeps every content and safety guarantee the old build has.

**Architecture:** One driver, `tools/quarto_build.py`, generates gitignored wrapper pages from the same sources and the same functions `tools/render.py` already has (imported, not copied), runs `quarto render` against a committed `_quarto.yml`, then adds what Quarto does not make: the sim copies with the draft bar, our own `robots.txt`, and the redirect stubs. The old build keeps feeding production and its full suite stays green. The chrome is not rebuilt here; that is phase 2.

**Tech Stack:** Quarto 1.10.18 (bundles its own Pandoc), Python 3.12 stdlib only, Pandoc 3.11 (old build and front matter reads, unchanged), GitHub Actions.

**Spec:** `docs/quarto-migration-plan.md` (phase 1 section and its exit criterion), with evidence in `docs/quarto-spike-2026-09-30.md`.

Ledger: D-0033, D-0034
binds D-0033
binds LEDGER 28, 37, 39, 51, 53

## Global Constraints

- Nothing in the old build changes behavior: `tools/render.py --site` output and the existing 24 tests stay exactly as they are. The only edits to existing files are the `questions.lua` fallback (Task 1), the `SITE_DIR` override in `tests/test_site_chrome.py` (Task 4), CI, `.gitignore`, and docs.
- No existing test is edited to make it pass, weakened, skipped or deleted. A brand test that fails against the Quarto output is phase 2's to-do list, reported, not fixed here.
- One source per document (LEDGER 28): wrappers `include` the curriculum file; no content is copied into a committed file. Generated files are gitignored and never hand-edited.
- Every page unlisted (LEDGER 37): `<meta name="robots" content="noindex, nofollow">` on every page and a `robots.txt` of `User-agent: *` / `Disallow: /`.
- Plain static output any host serves (LEDGER 39). No theme or setting that loads a third-party resource: Quarto theme `default`, never Cosmo.
- Sims ship byte for byte plus the bar only (LEDGER 51), using `render.render_sim` unchanged.
- A missing build is an error, never a skip (LEDGER 53).
- Markdown is read as `markdown-smart`, as the old build does, so straight quotes are never turned into curly ones.
- Quarto 1.10.18 exactly. Any Quarto warning line fails the build.
- No em dashes anywhere. No invented copy: page titles and text come from the existing sources and `render.py` functions only.
- Locally on Windows, Quarto is `C:\Program Files\Quarto\bin\quarto.exe` (not on PATH): set `QUARTO` to it and `PANDOC=%LOCALAPPDATA%\Pandoc\pandoc.exe`.
- Tasks 1 to 3 commit locally without pushing: until Task 4 adds Quarto to CI, `test_quarto_site.py` would error in `verify`. Push first at Task 4.
- Lands as one PR through `verify`, squash merge, identity hunterthelabguy with the noreply email, no trailer.

## File Structure

- Modify `tools/filters/questions.lua`: read `theme-name`, fall back to `theme`.
- Create `tests/test_questions_filter.py`: the filter's presentation switch, both keys.
- Create `_quarto.yml`: the Quarto project, with an explicit render list.
- Create `tools/quarto_build.py`: generate wrappers, run Quarto, post-process.
- Modify `.gitignore`: the generated wrapper paths and `.quarto/`.
- Create `tests/test_quarto_site.py`: the blocking phase 1 suite.
- Modify `tests/test_site_chrome.py`: read the site folder from `SITE_DIR` when set.
- Modify `.github/workflows/verify.yml`: install Quarto, build, and a non-blocking chrome job.
- Modify `CLAUDE.md`, `STATE.md`: the new command and the phase state.

---

### Task 1: The question filter reads `theme-name`

Quarto reserves the `theme` metadata key for its page theme, so under Quarto the presentation name travels as `theme-name`. The old build keeps passing `theme`.

**Files:**
- Modify: `tools/filters/questions.lua` (the `Meta` function)
- Test: `tests/test_questions_filter.py`

**Interfaces:**
- Produces: `questions.lua` honors `-M theme-name=faithful|modern`, then `-M theme=...`; `theme-name` wins when both are set.

- [ ] **Step 1: Write the failing test**

```python
"""questions.lua picks the presentation from theme-name, then theme (D-0033)."""

import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PANDOC = os.environ.get("PANDOC", "pandoc")
FILTER = ROOT / "tools" / "filters" / "questions.lua"
SOURCE = ROOT / "curriculum" / "ph211" / "ph211-team-building-handout.md"


def render(*meta):
    args = [PANDOC, str(SOURCE), "-f", "markdown-smart", "-t", "html",
            "--lua-filter", str(FILTER)]
    for m in meta:
        args += ["-M", m]
    return subprocess.run(args, check=True, capture_output=True,
                          text=True, encoding="utf-8").stdout


class Presentation(unittest.TestCase):

    def test_theme_name_faithful(self):
        self.assertIn("<strong>1)", render("theme-name=faithful"))

    def test_theme_still_works(self):
        self.assertIn("<strong>1)", render("theme=faithful"))

    def test_theme_name_wins_over_quarto_theme(self):
        # Under Quarto, theme is the page theme ("default"), never a presentation.
        out = render("theme=default", "theme-name=faithful")
        self.assertIn("<strong>1)", out)
        self.assertNotIn("Question 1", out)

    def test_default_is_modern(self):
        self.assertIn("Question 1", render())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python -m unittest tests.test_questions_filter -v`
Expected: `test_theme_name_faithful` and `test_theme_name_wins_over_quarto_theme` FAIL (no `<strong>1)`); the other two PASS.

- [ ] **Step 3: Implement**

In `tools/filters/questions.lua`, replace the `Meta` function body:

```lua
    Meta = function(meta)
      -- Quarto reserves `theme` for its page theme, so the presentation
      -- travels as `theme-name` there; the Pandoc build still sends `theme`.
      local v = meta["theme-name"] or meta.theme
      if v then theme = pandoc.utils.stringify(v) end
    end,
```

- [ ] **Step 4: Run the new test and the whole suite**

Run: `python -m unittest tests.test_questions_filter -v` then `python tools/render.py --site` then `python -m unittest discover -s tests`
Expected: 4 new tests PASS; the full suite is 28 tests, all PASS (the old build is unaffected).

- [ ] **Step 5: Commit**

```bash
git add tools/filters/questions.lua tests/test_questions_filter.py
git commit -m "Let the question filter read theme-name under Quarto"
```
(with a body saying why: Quarto reserves `theme`.)

---

### Task 2: Quarto renders every page into build/quarto-site

**Files:**
- Create: `_quarto.yml`
- Create: `tools/quarto_build.py`
- Modify: `.gitignore`
- Test: `tests/test_quarto_site.py` (the page, noindex, h1, question, front matter, stylesheet, third-party and words tests)

**Interfaces:**
- Consumes from `tools/render.py` (unchanged): `ROOT`, `converted_documents() -> {id: {"path", "meta"}}`, `body_after_front_matter(path) -> str`, `course_index_markdown(docs, depth) -> str`, `how_this_was_made() -> str`, `sims() -> {id: {"path", "title", "text"}}`, `sims_index_markdown(found) -> str`.
- Produces: `python tools/quarto_build.py` exits 0 and fills `build/quarto-site/`; module constants `OUT` (output folder) and function `build() -> None`. Task 3 extends `build()`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_quarto_site.py`:

```python
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
import test_site_chrome as chrome         # noqa: E402  (for SimBar.BAR only)


def setUpModule():
    if not QSITE.is_dir():
        raise RuntimeError("build/quarto-site is missing: run tools/quarto_build.py first")


def converted():
    """(id, path) of every converted curriculum document."""
    for p in sorted((ROOT / "curriculum").rglob("*.md")):
        text = p.read_text(encoding="utf-8")
        if text.startswith("---") and re.search(r"^source_file:", text, re.M):
            yield re.search(r"^id:\s*(\S+)", text, re.M).group(1), p


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
        want = ["index.html", "courses/index.html",
                "how-this-was-made/index.html", "sims/index.html"]
        for doc_id, _ in converted():
            want += [f"labs/{doc_id}/modern/index.html",
                     f"labs/{doc_id}/faithful/index.html"]
        for rel in want:
            with self.subTest(page=rel):
                self.assertTrue((QSITE / rel).is_file())

    def test_noindex_on_every_page(self):
        for rel, _, text in html_pages():
            if is_sim(rel):
                continue
            with self.subTest(page=rel):
                self.assertIn('<meta name="robots" content="noindex', text)

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
            for href in re.findall(r'<link[^>]*rel="stylesheet"[^>]*href="([^"]+)"', text):
                if href.startswith("data:"):
                    continue
                with self.subTest(page=rel, href=href):
                    self.assertTrue((path.parent / href.split("?")[0]).resolve().is_file())


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
        out = subprocess.run(
            [PANDOC, str(source), "-f", "markdown-smart", "-t", "html",
             "--lua-filter", str(FILTER), "-M", "theme-name=" + theme],
            check=True, capture_output=True, text=True, encoding="utf-8").stdout
        return words(out)

    def test_words_match_a_plain_pandoc_render(self):
        # The document's words, in order, appear unbroken inside Quarto's <main>.
        for doc_id, source in converted():
            for theme in ("modern", "faithful"):
                with self.subTest(doc=doc_id, theme=theme):
                    page = (QSITE / "labs" / doc_id / theme / "index.html").read_text(encoding="utf-8")
                    main = re.search(r"<main\b.*?</main>", page, re.S).group(0)
                    want = "\x00".join(self.reference_words(source, theme))
                    self.assertIn(want, "\x00".join(words(main)))

    def test_questions_numbered(self):
        for doc_id, source in converted():
            n = len(re.findall(r"\{\.question\b", source.read_text(encoding="utf-8")))
            self.assertGreater(n, 0)
            base = QSITE / "labs" / doc_id
            modern = (base / "modern" / "index.html").read_text(encoding="utf-8")
            faithful = (base / "faithful" / "index.html").read_text(encoding="utf-8")
            with self.subTest(doc=doc_id):
                for k in range(1, n + 1):
                    self.assertIn(f"Question {k}<", modern)
                    self.assertIn(f"<strong>{k})", faithful)
                self.assertNotIn(f"Question {n + 1}<", modern)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python -m unittest tests.test_quarto_site -v`
Expected: ERROR in `setUpModule`: "build/quarto-site is missing".

- [ ] **Step 3: Write `_quarto.yml`**

```yaml
# Quarto build (D-0033, migration phase 1). Run it only through
# tools/quarto_build.py, which generates the pages listed under render.
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
  resources:
    - site/fonts/
    - site/brand/

website:
  title: "Physics Lab Library"
  search: true
  navbar:
    left:
      - href: index.qmd
        text: Library home
      - href: courses/index.qmd
        text: Course index
      - href: sims/index.qmd
        text: Sims
      - href: how-this-was-made/index.qmd
        text: How this was made

format:
  html:
    # Never Cosmo or another theme that imports a remote font (D-0033).
    theme: default
    css: site/site.css
    lang: en
    # As the Pandoc build: no smart quotes, so words match the originals.
    from: markdown-smart
    # Every page carries its own <h1>; Quarto's title block would repeat it.
    title-block-style: none
    include-in-header:
      text: '<meta name="robots" content="noindex, nofollow">'
```

- [ ] **Step 4: Add the generated paths to `.gitignore`**

Append:

```
# Generated by tools/quarto_build.py; never edit (D-0033)
/index.qmd
/courses/
/how-this-was-made/
/labs/
/sims/index.qmd
/.quarto/
```

- [ ] **Step 5: Write `tools/quarto_build.py`**

```python
"""Build the site with Quarto into build/quarto-site/ (D-0033, phase 1).

Usage: python tools/quarto_build.py

Generates the pages Quarto renders (gitignored, never hand-edited) from the
same sources and functions tools/render.py uses, runs Quarto, then adds what
Quarto does not make. Any Quarto warning line fails the build. Requires
Quarto 1.10.18 (QUARTO, or quarto on PATH) and Pandoc for front matter
(PANDOC, as render.py).
"""

import json
import os
import re
import shutil
import subprocess
import sys

import render

ROOT = render.ROOT
QUARTO = os.environ.get("QUARTO", "quarto")
OUT = os.path.join(ROOT, "build", "quarto-site")
GENERATED = ["index.qmd", "courses", "how-this-was-made", "labs",
             os.path.join("sims", "index.qmd")]
WARNING = re.compile(r"^\s*(WARN|WARNING)\b", re.I | re.M)


def rel_to_root(page):
    """Relative path from a generated page's folder back to the repo root."""
    up = os.path.relpath(ROOT, os.path.dirname(os.path.join(ROOT, page)))
    return up.replace(os.sep, "/")


def write(page, front, body):
    path = os.path.join(ROOT, page)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lines = ["---"] + ["{}: {}".format(k, json.dumps(v, ensure_ascii=False)) for k, v in front.items()]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n---\n\n" + body.rstrip("\n") + "\n")


def include(page, target):
    return "{{< include " + rel_to_root(page) + "/" + target + " >}}"


def generate():
    for rel in GENERATED:
        path = os.path.join(ROOT, rel)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    write("index.qmd", {"title": "OSU physics lab library"},
          include("index.qmd", "site/landing.md"))

    docs = render.converted_documents()
    write("courses/index.qmd", {"title": "Course index"},
          render.course_index_markdown(docs, 1))
    write("how-this-was-made/index.qmd", {"title": "How this was made"},
          render.how_this_was_made())
    write("sims/index.qmd", {"title": "Sims"},
          render.sims_index_markdown(render.sims()))

    for doc_id, doc in docs.items():
        source = os.path.relpath(doc["path"], ROOT).replace(os.sep, "/")
        for theme in render.THEMES:
            page = "labs/{}/{}/index.qmd".format(doc_id, theme)
            up = rel_to_root(page)
            write(page, {
                "title": doc["meta"]["title"],
                "theme-name": theme,
                "filters": [up + "/tools/filters/questions.lua"],
                "css": [up + "/themes/" + theme + ".css"],
            }, include(page, source))


def run_quarto():
    proc = subprocess.run([QUARTO, "render"], cwd=ROOT, capture_output=True,
                          text=True, encoding="utf-8")
    log = proc.stdout + proc.stderr
    print(log)
    if proc.returncode != 0:
        raise SystemExit("quarto render failed")
    if WARNING.search(log):
        raise SystemExit("quarto printed a warning; the build fails on any warning")


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    generate()
    run_quarto()


if __name__ == "__main__":
    build()
    sys.exit(0)
```

Note on `write`: `json.dumps` output is valid YAML, including the `filters` and `css` lists, so no YAML library is needed.

- [ ] **Step 6: Build and run the tests**

Run (Windows, from the repo root in Git Bash):
```bash
export QUARTO="/c/Program Files/Quarto/bin/quarto.exe" PANDOC="$LOCALAPPDATA/Pandoc/pandoc.exe"
python tools/quarto_build.py
python -m unittest tests.test_quarto_site -v
```
Expected: the build exits 0 with no warning line, and every test in `test_quarto_site` PASSES.

If a test fails, fix the build, never the test. Known risks from the spikes, in the order to check them:
- `test_one_h1_per_page` fails with 2: `title-block-style: none` did not take. Check the key against quarto.org's HTML options reference for 1.10 and correct `_quarto.yml`.
- `test_words_match_a_plain_pandoc_render` fails on quotes: `from: markdown-smart` did not take. Confirm the option name and placement in the same reference.
- `test_stylesheets_resolve` fails for `site.css`: the project-level `css` path resolved per page. Confirm how Quarto 1.10 resolves project-level `css` and adjust the path, not the test.
- `test_no_third_party` fails: find the file in the failure message; a theme or library pulled a remote resource. Do not allowlist it; report it.

Stop and report instead of improvising if a fix would change what a test asserts.

- [ ] **Step 7: Confirm the old build is untouched**

Run: `python tools/render.py --site` then `python -m unittest discover -s tests`
Expected: every test PASSES, including all of `test_site_chrome` against `build/site/`. `git status` shows no generated file as untracked.

- [ ] **Step 8: Commit**

```bash
git add _quarto.yml tools/quarto_build.py .gitignore tests/test_quarto_site.py
git commit -m "Build the site with Quarto beside the old build"
```
(Body: the explicit render list and why; `markdown-smart`; generated wrappers are gitignored; the old build still feeds production.)

---

### Task 3: Sims, robots.txt and redirect stubs

**Files:**
- Modify: `tools/quarto_build.py` (a `post()` step called at the end of `build()`)
- Test: `tests/test_quarto_site.py` (add `SimsAndStubs`)

**Interfaces:**
- Consumes from `tools/render.py` (unchanged): `sims()`, `render_sim(sim_id, sim, site) -> path`, `redirect_page(out, target) -> path`, `converted_documents()`.
- Consumes from Task 2: `OUT`, `build()`.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_quarto_site.py`, above `if __name__`:

```python
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
        self.assertNotIn("Sitemap", text)

    def test_trimmed_lab_url_redirects_to_modern(self):
        for doc_id, _ in converted():
            with self.subTest(doc=doc_id):
                text = (QSITE / "labs" / doc_id / "index.html").read_text(encoding="utf-8")
                self.assertTrue(is_redirect(text))
                self.assertIn('url=modern/', text)
```

- [ ] **Step 2: Run to verify they fail**

Run: `python tools/quarto_build.py && python -m unittest tests.test_quarto_site.SimsAndStubs -v`
Expected: all three FAIL (files missing).

- [ ] **Step 3: Implement**

In `tools/quarto_build.py`, add above `build()`:

```python
def post():
    """What Quarto does not make, written with render.py's own functions."""
    for sim_id, sim in render.sims().items():
        render.render_sim(sim_id, sim, OUT)
    for doc_id in render.converted_documents():
        render.redirect_page(os.path.join(OUT, "labs", doc_id, "index.html"),
                             "modern/")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write("# Unlisted draft while the license is open (ledger 37).\n"
                 "User-agent: *\nDisallow: /\n")
```

and make `build()` end with `post()` after `run_quarto()`.

- [ ] **Step 4: Run the whole Quarto suite**

Run: `python tools/quarto_build.py && python -m unittest tests.test_quarto_site -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/quarto_build.py tests/test_quarto_site.py
git commit -m "Add sims, robots.txt and lab redirects to the Quarto build"
```

---

### Task 4: CI builds both, and reports the chrome gap

**Files:**
- Modify: `tests/test_site_chrome.py` (the `SITE` line only)
- Modify: `.github/workflows/verify.yml`

- [ ] **Step 1: Let the chrome suite point at another folder**

In `tests/test_site_chrome.py`, add `import os` to the imports and replace the `SITE = ...` line with:

```python
# SITE_DIR lets CI run this contract against the Quarto build (D-0033,
# migration phase 1, non-blocking). Unset, it reads the old build as always.
SITE = Path(os.environ["SITE_DIR"]) if os.environ.get("SITE_DIR") else ROOT / "build" / "site"
```

Run: `python -m unittest discover -s tests` with `SITE_DIR` unset.
Expected: all PASS, same count as before this step.

- [ ] **Step 2: Add Quarto to the `verify` job**

In `.github/workflows/verify.yml`, after the "Install Pandoc 3.11" step:

```yaml
      - name: Install Quarto 1.10.18
        run: |
          curl -sSLo quarto.deb https://github.com/quarto-dev/quarto-cli/releases/download/v1.10.18/quarto-1.10.18-linux-amd64.deb
          sudo dpkg -i quarto.deb
          quarto --version
```

and after the "Site builds" step:

```yaml
      - name: Quarto site builds
        # Fails on any Quarto warning line (docs/quarto-migration-plan.md).
        run: python3 tools/quarto_build.py
```

The existing "Tests" step then runs `test_quarto_site.py` and `test_questions_filter.py` too, blocking.

- [ ] **Step 3: Add the non-blocking chrome job**

Append to `jobs:` in the same file:

```yaml
  chrome-on-quarto:
    # Phase 2's to-do list: the brand contract run against the Quarto build.
    # Expected to fail until phase 2; never gates a merge.
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - uses: actions/checkout@v4
      - name: Install Pandoc 3.11
        run: |
          curl -sSLo pandoc.deb https://github.com/jgm/pandoc/releases/download/3.11/pandoc-3.11-1-amd64.deb
          sudo dpkg -i pandoc.deb
      - name: Install Quarto 1.10.18
        run: |
          curl -sSLo quarto.deb https://github.com/quarto-dev/quarto-cli/releases/download/v1.10.18/quarto-1.10.18-linux-amd64.deb
          sudo dpkg -i quarto.deb
      - name: Quarto site builds
        run: python3 tools/quarto_build.py
      - name: Chrome contract against the Quarto build
        env:
          SITE_DIR: build/quarto-site
        run: python3 -m unittest discover -s tests -p test_site_chrome.py -v
```

- [ ] **Step 4: Commit, push the branch, open the PR**

```bash
git add tests/test_site_chrome.py .github/workflows/verify.yml
git commit -m "Run the Quarto build in CI; report the chrome gap"
```

Push over the SSH remote and open the PR. Wait for `verify` to report. Expected: `verify` green; `chrome-on-quarto` red with a list of failing chrome tests. Copy that list of failing test names into the PR description under "Phase 2 to-do". Confirm the Quarto .deb URL downloaded; if it 404s, find the correct asset name on the v1.10.18 release page and fix the URL, nothing else.

---

### Task 5: Docs and state

**Files:**
- Modify: `CLAUDE.md` (Build section, the Quarto bullet)
- Modify: `STATE.md` (Focus)

- [ ] **Step 1: CLAUDE.md**

Extend the existing Quarto bullet in the Build section with: "Build it with `python tools/quarto_build.py` (set `QUARTO` locally); output `build/quarto-site/`, checked by `tests/test_quarto_site.py`. Generated pages (`/index.qmd`, `/courses/`, `/how-this-was-made/`, `/labs/`, `/sims/index.qmd`) are gitignored and rebuilt every run; never edit them. Production still serves the old build."

- [ ] **Step 2: STATE.md**

Replace the 2026-09-30 Focus paragraph with the phase 1 result: the PR, the test count, and the `chrome-on-quarto` failure count from Task 4. Next is phase 2.

- [ ] **Step 3: Verify and commit**

Run the full verify recipe from CLAUDE.md (content check, em-dash scan, both builds, all tests). Then:

```bash
git add CLAUDE.md STATE.md
git commit -m "Record the Quarto build command and phase 1 state"
```

Push to the PR branch, wait for `verify`, squash merge, sync `main`, delete the branch.

---

## Not in this plan

Chrome, the draft banner, fonts and the landing hero (phase 2); `check_unchanged.py` on Quarto's Pandoc (phase 3); retiring `render.py` (phase 4, after phase 5's cutover); the Cloudflare deploy (phase 5, D-0034); search tuning, listings, downloads.
