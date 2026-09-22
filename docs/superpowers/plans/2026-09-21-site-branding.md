# Site Branding Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the library's site chrome the Oregon State University department look (official logo, Physics-style header and footer, palette-only color, Open Sans) without touching any document body.

**Architecture:** The build (`tools/render.py`, Pandoc templates) already wraps every page in chrome; this plan replaces that chrome. A shared header and footer become two Pandoc template partials used by both templates, the logo files are committed and embedded by Pandoc's `--embed-resources`, and the sim bar stays a string injected into the published copy only. Tests are standard-library `unittest` files that read `site/site.css` and the built `build/site/`.

**Tech Stack:** Python 3.12 (stdlib only in tests), Pandoc 3.11 templates and partials, plain CSS, Node 24 for the sim's own test, fontTools and brotli for subsetting (Task 6 only, pending D-0027).

**Spec:** `docs/superpowers/specs/2026-09-21-site-branding-design.md`

Ledger: D-0001, D-0002, D-0004, D-0005, D-0006, D-0007, D-0008, D-0009, D-0010, D-0011, D-0014, D-0015, D-0020, D-0022, D-0023, D-0024, D-0025, D-0026, D-0027, D-0028
binds D-0001
binds D-0002
binds D-0004
binds D-0005
binds D-0006
binds D-0007
binds D-0008
binds D-0009
binds D-0010
binds D-0011
binds D-0014
binds D-0015
binds D-0020
binds D-0022
binds D-0023
binds D-0024
binds D-0025
binds D-0026

D-0027 and D-0028 are `proposed`. Tasks 6 and 7 depend on them and STOP
until the owner rules them; Task 6 also needs the owner's approval of the
download (files and sizes listed in D-0027).

## Global Constraints

- No em dashes anywhere (CI scans raw bytes outside `originals/`).
- Palette values only in `site/site.css`, from `OSU-branding/OSU-style-guide.md`; no tints or shades (D-0008).
- Beaver Orange text only at 24 px regular or 18 px at weight 700 and up (D-0008).
- The logo is never altered, recolored, retyped or redrawn; files are committed byte for byte (D-0002, D-0014).
- Logo alt text is exactly `Oregon State University`; the logo links to `https://oregonstate.edu`.
- Footer: no address, email, phone or copyright line (D-0009, D-0023).
- Document bodies (`<main>` of converted documents) are not changed (D-0010).
- Sims: the published copy equals the source plus the injected bar, nothing else (LEDGER 51).
- Every page keeps the draft banner wording and `noindex` (LEDGER 37).
- Output stays plain static files, relative links, no host-specific config (LEDGER 39).
- Commits: identity `hunterthelabguy` with the noreply email (check `git config user.name` and `user.email`), no trailer, subject 72 characters or fewer, narrative body. Land via PR with green `verify`.
- Run commands from the repo root. On this machine: `PY="$LOCALAPPDATA/Programs/Python/Python312/python.exe"` and `PANDOC="$LOCALAPPDATA/Pandoc/pandoc.exe"`.

## Branch

PR #7 (ledger, spec, this plan) lands first. Then, in the worktree
`src/OSU-physics-lab-library-ledger`:

```bash
git fetch origin && git switch -c branding-refresh origin/main
```

---

### Task 1: Palette-only chrome colors

**Files:**
- Modify: `site/site.css:1-47` (header comment, `:root`, dark block, faithful block), `site/site.css:106` (`.switch` hover)
- Test: `tests/test_brand.py`

**Interfaces:**
- Consumes: `css_text()`, `norm_hex()` in `tests/test_brand.py`.
- Produces: `PALETTE` (set of 19 uppercase hex strings) in `tests/test_brand.py`; tokens `--chrome-rule` light `#a7aca2`, dark `#8e9089`; `--chrome-tint` no longer exists.

- [ ] **Step 1: Write the failing test.** Add to `tests/test_brand.py`, after the constants:

```python
# The style guide's primary and secondary colors (Electric Beav has no
# values and is print only). D-0008: the chrome uses nothing else.
PALETTE = {
    "D73F09", "000000", "FFFFFF",                      # primary
    "4A773C", "00859B", "FFB500", "006A8E", "C4D6A4",  # Pine Stand .. Reindeer Moss
    "B8DDE1", "FDD26E", "C6DAE7", "AA9D2E", "0D5257",  # Seafoam .. Rogue Wave
    "D3832B", "003B5C", "B7A99A", "A7ACA2", "7A6855",  # Solar Flare .. High Desert
    "8E9089",                                          # Crater
}
```

and this class, before `if __name__ == "__main__":`:

```python
class PaletteOnly(unittest.TestCase):
    """D-0008 and D-0015: every color in the chrome is a palette value."""

    def test_site_css_palette_only(self):
        found = {norm_hex(h) for h in re.findall(r"#[0-9a-fA-F]{3,6}\b", css_text())}
        self.assertEqual(sorted(found - PALETTE), [])
```

- [ ] **Step 2: Run it and watch it fail.**

Run: `"$PY" -m unittest tests.test_brand.PaletteOnly -v`
Expected: FAIL listing `['14181B', '1C2227', '33393F', 'D6DBE0', 'F2F4F6', 'F4F7F9']`.

- [ ] **Step 3: Implement.** In `site/site.css`:
  - In the header comment, replace `(../../OSU-style-guide.md in the sandbox, not in this repo)` with `(OSU-branding/OSU-style-guide.md in the sandbox, not in this repo)`.
  - `:root`: `--chrome-rule: #a7aca2;   /* Coastline */`; delete the `--chrome-tint` line.
  - Dark block: `--chrome-ink: #fff;`, `--chrome-paper: #000;` (D-0015), `--chrome-rule: #8e9089; /* Crater */`; delete its `--chrome-tint` line.
  - `body.theme-faithful` block: `--chrome-rule: #a7aca2;`; delete its `--chrome-tint` line.
  - Replace line 106 with:

```css
.switch:hover, .switch:focus { text-decoration: underline; }
```

- [ ] **Step 4: Run all tests.**

Run: `"$PY" -m unittest discover -s tests -v`
Expected: all pass, `expected failures=1` (the D-0022 banner test, fixed in Task 2). `grep -n "chrome-tint" site/site.css` prints nothing.

- [ ] **Step 5: Commit.**

```bash
git add site/site.css tests/test_brand.py
git commit -m "Hold the site chrome to palette colors only" -m "D-0008 and D-0015. Six off-palette values go: light rules become Coastline, dark paper and ink become Paddletail Black and Bucktooth White, dark rules become Crater, and the hover tint gives way to an underline. A test now rejects any hex in site.css outside the style guide's palette."
```

---

### Task 2: Luminance draft banner

**Files:**
- Modify: `site/site.css` (`:root`, `.draft-banner`)
- Test: `tests/test_brand.py` (`DraftBanner.test_banner_colors`)

**Interfaces:**
- Consumes: `light_root_tokens()`, `rules()`.
- Produces: token `--chrome-warn: #ffb500`.

- [ ] **Step 1: Make the test strict.** In `tests/test_brand.py`, delete the four comment lines and the `@unittest.expectedFailure` line above `def test_banner_colors`.

- [ ] **Step 2: Run it and watch it fail.**

Run: `"$PY" -m unittest tests.test_brand.DraftBanner -v`
Expected: FAIL, `AssertionError: 'D73F09' != 'FFB500'`.

- [ ] **Step 3: Implement.** In `site/site.css` `:root` add `--chrome-warn: #ffb500;     /* Luminance, black text 11.86:1 (D-0022) */`, and in `.draft-banner` set:

```css
  background: var(--chrome-warn);
  color: #000;
```

- [ ] **Step 4: Run all tests.** Run: `"$PY" -m unittest discover -s tests -v`. Expected: all pass, no expected failures.

- [ ] **Step 5: Commit.**

```bash
git add site/site.css tests/test_brand.py
git commit -m "Set the draft banner in Luminance with black text" -m "D-0022: the warning must not merge into the orange brand banner that Task 4 adds beneath it. The banner test drops its expected-failure marker and now gates the colors."
```

---

### Task 3: Commit the logo files

**Files:**
- Create: `site/brand/OSU_horizontal_2C_W_over_B.png`, `site/brand/OSU_horizontal_2C_O_over_W.png`, `site/brand/OSU_horizontal_2C_O_over_B.png`, `site/brand/README.md`
- Test: `tests/test_assets.py`

**Interfaces:**
- Produces: `LOGOS` dict (file name to SHA-256) in `tests/test_assets.py`; paths under `site/brand/` used by Tasks 4 and 5.

- [ ] **Step 1: Write the failing test.** Create `tests/test_assets.py`:

```python
"""Committed brand assets are the official files, byte for byte (D-0014, D-0020)."""

import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "site" / "brand"

# SHA-256 of the files in OSU-branding/, hashed 2026-09-21.
LOGOS = {
    "OSU_horizontal_2C_W_over_B.png": "29b50744b39b1dadfbe55a5517c0b55da3d9d2e7ef2be7ad25a0b68cb12e50f1",
    "OSU_horizontal_2C_O_over_W.png": "8721817d9c9ca785fd3611b2f498b43f3ea21c762de95e45ea77efacb0a73c06",
    "OSU_horizontal_2C_O_over_B.png": "b6e0ba835619a2023b1403e40c7e7dda52c0ef7019411c31eddd23d421297fc8",
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


class LogoFiles(unittest.TestCase):

    def test_logos_are_byte_for_byte(self):
        for name, digest in LOGOS.items():
            with self.subTest(name=name):
                self.assertEqual(sha256((BRAND / name).read_bytes()), digest)

    def test_trademark_notice(self):
        text = (BRAND / "README.md").read_text(encoding="utf-8")
        self.assertIn("registered trademark", text)
        self.assertIn("excluded from any license", text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run it and watch it fail.** Run: `"$PY" -m unittest tests.test_assets -v`. Expected: ERROR, `FileNotFoundError` for `site/brand/...`.

- [ ] **Step 3: Copy the files and write the notice.**

```bash
SRC="../OSU-branding/PNG RGB for digital and Microsoft Office/PNG RGB for digital and Microsoft Office"
mkdir -p site/brand
cp "$SRC/OSU_horizontal_2C_W_over_B.png" "$SRC/OSU_horizontal_2C_O_over_W.png" "$SRC/OSU_horizontal_2C_O_over_B.png" site/brand/
```

Create `site/brand/README.md`:

```markdown
# Brand files

The Oregon State University logo files here are OSU registered trademarks,
committed byte for byte from the official PNG set the owner supplied on
2026-09-21 (DECISIONS D-0014, D-0020). They are excluded from any license
this repository adopts (D-0007). Do not edit, recolor, crop or re-export
them; `tests/test_assets.py` checks each file's SHA-256.

| File | Used on |
|---|---|
| `OSU_horizontal_2C_W_over_B.png` | the Beaver Orange header banner |
| `OSU_horizontal_2C_O_over_W.png` | the black sim bar |
| `OSU_horizontal_2C_O_over_B.png` | white backgrounds |
```

Also add `*.png binary` to `.gitattributes` if a `png` rule is not already there (`grep -n png .gitattributes`).

- [ ] **Step 4: Run all tests.** Run: `"$PY" -m unittest discover -s tests -v`. Expected: all pass.

- [ ] **Step 5: Commit.**

```bash
git add site/brand tests/test_assets.py .gitattributes
git commit -m "Commit the three official logo files, byte for byte" -m "D-0007, D-0014, D-0020: W over B for the orange banner, O over W for the black sim bar, O over B for white. A README marks them as trademarks outside any license, and a test pins each file's SHA-256."
```

---

### Task 4: Header and footer on every site and document page

**Files:**
- Create: `tools/brandheader.html`, `tools/brandfooter.html` (Pandoc partials), `tests/test_site_chrome.py`, `tests/fixtures/main-bodies.json`
- Modify: `tools/template-site.html`, `tools/template.html`, `tools/render.py` (`site_vars`), `site/site.css` (new header, nav, footer rules), `.github/workflows/verify.yml` (move tests after the build)

**Interfaces:**
- Consumes: `LOGOS` from `tests/test_assets.py`; `BANNER_MAIN` from `tools/render.py`.
- Produces: `SITE_LOGO` constant in `tools/render.py`; template variable `logo`; CSS classes `osu-header`, `osu-strip`, `osu-banner`, `osu-logo`, `osu-sitename`, `osu-nav`, `osu-foot`, `osu-inner`; helper `pages()` in `tests/test_site_chrome.py`.

- [ ] **Step 1: Capture the document bodies before any template change.** This fixture is what the "bodies unchanged" check compares against (spec 7.6).

```bash
PANDOC="$PANDOC" "$PY" tools/render.py --site
"$PY" - <<'EOF'
import hashlib, json, re
from pathlib import Path
out = {}
for p in sorted(Path("build/site/labs").glob("*/*/index.html")):
    m = re.search(r"<main>.*?</main>", p.read_text(encoding="utf-8"), re.S)
    out[p.relative_to("build/site").as_posix()] = hashlib.sha256(m.group(0).encode()).hexdigest()
Path("tests/fixtures").mkdir(exist_ok=True)
Path("tests/fixtures/main-bodies.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(len(out), "document bodies captured")
EOF
```

Expected: `2 document bodies captured` (Team Building, two presentations).

- [ ] **Step 2: Write the failing test.** Create `tests/test_site_chrome.py`:

```python
"""Checks on the built site (build/site/). CI runs this after "Site builds".

A missing build is an error, never a skip (LEDGER 53).
"""

import base64
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "build" / "site"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))
from render import BANNER_MAIN            # noqa: E402
from test_assets import LOGOS, sha256     # noqa: E402

POLICY_LINKS = [
    "https://oregonstate.edu/accessibility-statement",
    "https://oregonstate.edu/official-web-disclaimer",
    "https://eoa.oregonstate.edu/about-us/policies-guidance-and-memos",
]


def setUpModule():
    if not SITE.is_dir():
        raise RuntimeError("build/site is missing: run tools/render.py --site first")


def pages():
    """Built pages that carry the full chrome: not redirect stubs, not sims."""
    for p in sorted(SITE.rglob("index.html")):
        rel = p.relative_to(SITE).as_posix()
        text = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text:
            continue
        if re.fullmatch(r"sims/[^/]+/index\.html", rel):
            continue
        yield rel, text


def img_attrs(tag):
    return dict(re.findall(r'(\w+)="([^"]*)"', tag))


def embedded_png_sha(src):
    prefix = "data:image/png;base64,"
    assert src.startswith(prefix), src[:40]
    return sha256(base64.b64decode(src[len(prefix):]))


class FullChrome(unittest.TestCase):

    def test_enough_pages(self):
        self.assertGreaterEqual(len(list(pages())), 6)

    def test_logo_unaltered_and_linked(self):
        for rel, text in pages():
            with self.subTest(page=rel):
                m = re.search(r'<a class="osu-logo" href="https://oregonstate.edu">\s*(<img[^>]*>)', text)
                self.assertIsNotNone(m, "no linked logo")
                attrs = img_attrs(m.group(1))
                self.assertEqual(attrs.get("alt"), "Oregon State University")
                self.assertEqual(embedded_png_sha(attrs["src"]), LOGOS["OSU_horizontal_2C_W_over_B.png"])

    def test_top_strip_links_department(self):
        for rel, text in pages():
            with self.subTest(page=rel):
                self.assertIn('<a href="https://physics.oregonstate.edu">Department of Physics</a>', text)

    def test_draft_banner_and_noindex(self):
        for rel, text in pages():
            with self.subTest(page=rel):
                self.assertIn(BANNER_MAIN, text)
                self.assertIn('<meta name="robots" content="noindex', text)

    def test_footer_as_ruled(self):
        for rel, text in pages():
            with self.subTest(page=rel):
                foot = re.search(r'<footer class="osu-foot">.*?</footer>', text, re.S)
                self.assertIsNotNone(foot)
                for url in POLICY_LINKS:
                    self.assertIn(url, foot.group(0))
                for banned in ("mailto:", "tel:", "&copy;", "©", "Copyright"):
                    self.assertNotIn(banned, text)


class DocumentBodies(unittest.TestCase):
    """D-0010: branding never changes a document's <main>."""

    def test_bodies_unchanged(self):
        want = json.loads((ROOT / "tests" / "fixtures" / "main-bodies.json").read_text(encoding="utf-8"))
        for rel, digest in want.items():
            with self.subTest(page=rel):
                text = (SITE / rel).read_text(encoding="utf-8")
                main = re.search(r"<main>.*?</main>", text, re.S).group(0)
                self.assertEqual(hashlib.sha256(main.encode()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run it and watch it fail.** Run: `"$PY" -m unittest tests.test_site_chrome -v`. Expected: `test_logo_unaltered_and_linked`, `test_top_strip_links_department`, `test_footer_as_ruled` FAIL; `test_bodies_unchanged` and `test_draft_banner_and_noindex` PASS.

- [ ] **Step 4: Write the partials.** Create `tools/brandheader.html`:

```html
<header class="osu-header">
<div class="osu-strip"><div class="osu-inner"><a href="https://physics.oregonstate.edu">Department of Physics</a></div></div>
<div class="osu-banner"><div class="osu-inner">
<a class="osu-logo" href="https://oregonstate.edu"><img src="$logo$" alt="Oregon State University"></a>
<a class="osu-sitename" href="$homehref$">Physics Lab Library</a>
</div></div>
<nav class="osu-nav" aria-label="Library"><div class="osu-inner">
<a href="$homehref$">Library home</a>
<a href="$indexhref$">Course index</a>
<a href="$simshref$">Sims</a>
<a href="$methodhref$">How this was made</a>
</div></nav>
</header>
```

Create `tools/brandfooter.html`:

```html
<footer class="osu-foot"><div class="osu-inner">
<p class="osu-foot-unit">Department of Physics</p>
<p><a href="https://oregonstate.edu/accessibility-statement">Accessibility Statement</a> &middot; <a href="https://oregonstate.edu/official-web-disclaimer">Privacy Disclaimer</a> &middot; <a href="https://eoa.oregonstate.edu/about-us/policies-guidance-and-memos">Non-Discrimination Statement</a></p>
<p>License and credits: see <a href="$methodhref$">How this was made</a>.</p>
</div></footer>
```

- [ ] **Step 5: Use them in the templates.** In `tools/template-site.html`, replace everything from the `<p class="draft-banner">` line through `</body>` with:

```html
<p class="draft-banner">$bannermain$<span class="draft-detail">$bannerdetail$</span></p>
$brandheader()$
<main>
$body$
</main>
$if(footnote)$
<div class="site-foot">
<p class="print-hide">$footnote$</p>
</div>
$endif$
$brandfooter()$
</body>
```

In `tools/template.html`, directly after the `$if(bannermain)$ ... $endif$` block add:

```html
$if(homehref)$
$brandheader()$
$endif$
```

keep the existing `<nav class="site-nav">` block (up-link and switch) as is, and replace the final `$if(homehref)$ <div class="site-foot"> ... </div> $endif$` block with:

```html
$if(homehref)$
$brandfooter()$
$endif$
```

- [ ] **Step 6: Pass the logo path.** In `tools/render.py`, after `THEMES = ...` add:

```python
# Official logo files, committed byte for byte (DECISIONS D-0014, D-0020).
# Absolute, so --embed-resources finds them wherever the output lands.
BRAND = os.path.join(ROOT, "site", "brand")
SITE_LOGO = os.path.join(BRAND, "OSU_horizontal_2C_W_over_B.png").replace(os.sep, "/")
```

and add `"-M", "logo=" + SITE_LOGO,` to the list `site_vars` returns.

- [ ] **Step 7: Style it.** Append to `site/site.css`, before the `@media print` block:

```css
/* OSU header and footer (DECISIONS D-0004, D-0009, D-0024): the structure
   of the Physics department site. The logo's clear space is at least the
   width of the "O" in "Oregon State", measured from the file at about a
   quarter of the logo's height, so the padding scales with --logo-h. */
:root { --logo-h: 48px; }

.osu-inner { max-width: var(--chrome-shell); margin: 0 auto; padding: 0 1rem; }

.osu-header, .osu-foot {
  font-family: ui-sans-serif, system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.osu-strip { background: #000; font-size: .85rem; line-height: 1.5; padding: .35rem 0; }
.osu-strip a { color: #fff; }

.osu-banner { background: var(--chrome-accent); }
.osu-banner .osu-inner {
  display: flex; flex-wrap: wrap; align-items: center; gap: .25rem 1.25rem;
}
.osu-logo { display: block; line-height: 0; padding: calc(var(--logo-h) * .25) calc(var(--logo-h) * .25) calc(var(--logo-h) * .25) 0; }
.osu-logo img { display: block; height: var(--logo-h); width: auto; }
.osu-sitename {
  color: #fff; font-size: 1.75rem; font-weight: 700; line-height: 1.2;
  text-decoration: none; padding: .25rem 0;
}
.osu-sitename:hover, .osu-sitename:focus { text-decoration: underline; }

.osu-nav { background: #fff; border-bottom: 1px solid var(--chrome-rule); }
.osu-nav .osu-inner { display: flex; flex-wrap: wrap; gap: .25rem 1.5rem; padding-top: .6rem; padding-bottom: .6rem; }
.osu-nav a { color: #000; font-weight: 700; text-decoration: none; font-size: .95rem; }
.osu-nav a:hover, .osu-nav a:focus { text-decoration: underline; }

.osu-foot { background: #000; color: #fff; margin-top: 3rem; padding: 1.5rem 0 2.5rem; font-size: .9rem; line-height: 1.5; }
.osu-foot a { color: #fff; }
.osu-foot p { margin: 0 0 .5rem; }
.osu-foot-unit { font-weight: 700; font-size: 1.1rem; }

@media (max-width: 40rem) {
  :root { --logo-h: 36px; }
  .osu-sitename { font-size: 1.5rem; }
}
```

and inside the existing `@media print` block add `.osu-header, .osu-foot { display: none; }`. Then, since `.site-foot` now holds only the footnote, change its `border-top` line to nothing (delete it) and its `margin-top: 3rem` to `margin-top: 2rem`.

- [ ] **Step 8: Move the tests after the build in CI.** In `.github/workflows/verify.yml`, cut the `Brand tests` step and paste it after `Site builds`, renamed:

```yaml
      - name: Tests
        # Each asserts a ruled DECISIONS.md quantity or reads build/site.
        run: python3 -m unittest discover -s tests -v
```

- [ ] **Step 9: Build and run everything.**

```bash
PANDOC="$PANDOC" "$PY" tools/render.py --site && "$PY" -m unittest discover -s tests -v
```

Expected: all pass. If `$brandheader()$` renders literally, Pandoc did not find the partial: it must sit beside the template with the same `.html` extension.

- [ ] **Step 10: Commit.**

```bash
git add tools/brandheader.html tools/brandfooter.html tools/template-site.html tools/template.html tools/render.py site/site.css tests/test_site_chrome.py tests/fixtures/main-bodies.json .github/workflows/verify.yml
git commit -m "Frame every page in the Physics department's header and footer" -m "D-0002, D-0004, D-0009, D-0020, D-0023, D-0024: black strip linking the department, orange banner with the official logo (W over B, embedded unaltered, linked to oregonstate.edu) and the site name as text, white navigation bar, black footer with the three OSU policy links and no contact or copyright line. Both templates share two Pandoc partials. Document bodies are pinned by hash to their pre-change build (D-0010), and CI now runs the tests after the site build."
```

---

### Task 5: The sim bar

**Files:**
- Modify: `tools/render.py` (`SIM_CHROME`, `render_sim`, imports)
- Test: `tests/test_site_chrome.py`

**Interfaces:**
- Consumes: `BRAND`, `BANNER_MAIN` in `tools/render.py`; `LOGOS`, `embedded_png_sha`, `img_attrs` in tests.
- Produces: `SIM_LOGO` constant and `png_data_uri(path) -> str` in `tools/render.py`.

- [ ] **Step 1: Write the failing test.** Add to `tests/test_site_chrome.py`:

```python
class SimBar(unittest.TestCase):
    """D-0005, D-0020, D-0022; LEDGER 51: source plus the bar, nothing else."""

    BAR = re.compile(r"<body[^>]*>(\n<style>\n\.lib-bar.*?</div>\n)", re.S)

    def sims(self):
        for src in sorted((ROOT / "sims").glob("*/index.html")):
            yield src, SITE / "sims" / src.parent.name / "index.html"

    def test_source_plus_bar_only(self):
        for src, pub in self.sims():
            with self.subTest(sim=src.parent.name):
                p = pub.read_text(encoding="utf-8")
                m = self.BAR.search(p)
                self.assertIsNotNone(m, "no bar after <body>")
                self.assertEqual(p.replace(m.group(1), "", 1), src.read_text(encoding="utf-8"))

    def test_bar_logo_and_banner(self):
        for src, pub in self.sims():
            with self.subTest(sim=src.parent.name):
                bar = self.BAR.search(pub.read_text(encoding="utf-8")).group(1)
                self.assertIn("background: #000", bar)
                self.assertIn('<span class="lib-draft">' + BANNER_MAIN + "</span>", bar)
                img = re.search(r'<a href="https://oregonstate.edu">(<img[^>]*>)</a>', bar)
                self.assertIsNotNone(img)
                attrs = img_attrs(img.group(1))
                self.assertEqual(attrs.get("alt"), "Oregon State University")
                self.assertEqual(embedded_png_sha(attrs["src"]), LOGOS["OSU_horizontal_2C_O_over_W.png"])
```

- [ ] **Step 2: Run it and watch it fail.** Run: `PANDOC="$PANDOC" "$PY" tools/render.py --site && "$PY" -m unittest tests.test_site_chrome.SimBar -v`. Expected: `test_bar_logo_and_banner` FAILS (orange bar, no logo); `test_source_plus_bar_only` PASSES.

- [ ] **Step 3: Implement.** In `tools/render.py` add `import base64` to the imports, add after `SITE_LOGO`:

```python
SIM_LOGO = os.path.join(BRAND, "OSU_horizontal_2C_O_over_W.png")


def png_data_uri(path):
    """The sim's policy allows images only as data: URIs (img-src data:)."""
    with open(path, "rb") as fh:
        return "data:image/png;base64," + base64.b64encode(fh.read()).decode("ascii")
```

replace `SIM_CHROME` with:

```python
SIM_CHROME = """<style>
.lib-bar {{
  flex: 0 0 auto;
  display: flex; flex-wrap: wrap; gap: .1rem .9rem; align-items: center;
  background: #000; color: #fff;
  padding: 0 .75rem;
  font: 400 .85rem/1.4 ui-sans-serif, system-ui, "Segoe UI", Roboto, Arial, sans-serif;
}}
.lib-bar img {{ display: block; height: 22px; width: auto; padding: 6px 6px 6px 0; }}
.lib-bar .lib-draft {{ background: #ffb500; color: #000; font-weight: 700; padding: 0 .4rem; }}
.lib-bar a {{ color: #fff; }}
.lib-bar .lib-links {{ display: flex; gap: 1rem; margin-left: auto; }}
@media print {{ .lib-bar {{ display: none; }} }}
</style>
<div class="lib-bar">
<a href="https://oregonstate.edu"><img src="{logo}" alt="Oregon State University"></a>
<span class="lib-draft">{banner}</span>
<span class="lib-links"><a href="{home}">Library home</a><a href="{sims}">Sims</a></span>
</div>
"""
```

update the comment above it to say the bar is Paddletail Black with the O over W logo (D-0005, D-0020) and the draft sentence in Luminance (D-0022), and in `render_sim` pass the logo:

```python
    chrome = SIM_CHROME.format(banner=html.escape(BANNER_MAIN),
                               logo=png_data_uri(SIM_LOGO),
                               home=up(2), sims=up(1))
```

- [ ] **Step 4: Build and run everything.** Run: `PANDOC="$PANDOC" "$PY" tools/render.py --site && "$PY" -m unittest discover -s tests -v`. Expected: all pass.

- [ ] **Step 5: Measure the height budget (LEDGER 51, D-0005).** Serve the build from the repo root: `"$PY" -m http.server 8733 --directory build/site` (background). In the browser pane, set the viewport to 1280 by 720, load `http://127.0.0.1:8733/sims/modified-electric-force/`, and run:

```js
({bar: document.querySelector('.lib-bar').getBoundingClientRect().height,
  page: document.documentElement.scrollHeight, fits: document.documentElement.scrollHeight <= 720})
```

Expected: `fits: true`. Record the three numbers in `STATE.md`. If it does not fit, stop and report; do not shrink the logo below 22 px without a ruling.

- [ ] **Step 6: Commit.**

```bash
git add tools/render.py tests/test_site_chrome.py STATE.md
git commit -m "Give sims a slim black bar with the logo" -m "D-0005, D-0020, D-0022: the injected bar is Paddletail Black with the O over W logo as a data: URI (the sim's policy allows img-src data:) and the draft sentence in Luminance. The published sim is still exactly its source plus the bar (LEDGER 51), now asserted, and the 1280 by 720 budget is measured and recorded."
```

---

### Task 6: Open Sans on site pages (STOP: needs D-0027 ruled and download approved)

Before any step: confirm in chat that the owner has ruled D-0027 and approved
the download (four TTFs, 147528 + 147264 + 153256 + 153308 bytes, and
`OFL.txt`, 4216 bytes, from `github.com/googlefonts/opensans`; plus
`fonttools` and `brotli` from PyPI). If not, stop and surface it.

**Files:**
- Create: `tools/subset_fonts.py`, `site/fonts/OpenSans-Regular.woff2`, `-Bold.woff2`, `-Italic.woff2`, `-BoldItalic.woff2`, `site/fonts/OFL.txt`, `site/fonts/README.md`, `tests/test_fonts.py`
- Modify: `site/site.css` (`@font-face`, font stacks, weights), `themes/modern.css` (font stack, weights)

**Interfaces:**
- Produces: `UNICODES` (list of `(first, last)` int pairs) and `covers(ch) -> bool` in `tools/subset_fonts.py`; `@font-face` family name `"Open Sans"`.

- [ ] **Step 1: Write the failing tests.** Create `tests/test_fonts.py`:

```python
"""Open Sans, subset to Latin and Greek (D-0006, D-0025, D-0027)."""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "site" / "fonts"
sys.path.insert(0, str(ROOT / "tools"))
from subset_fonts import STYLES, covers   # noqa: E402

STRIP = re.compile(r"/\*.*?\*/", re.S)


class FontFiles(unittest.TestCase):

    def test_files_and_license_present(self):
        for style in STYLES:
            self.assertTrue((FONTS / f"OpenSans-{style}.woff2").is_file(), style)
        self.assertIn("SIL OPEN FONT LICENSE", (FONTS / "OFL.txt").read_text(encoding="utf-8").upper())

    def test_subset_covers_our_text(self):
        # Every character in the converted documents and site copy must be in
        # the subset, or a reader sees a fallback glyph mid-word.
        chars = set()
        for md in list(ROOT.glob("curriculum/**/*.md")) + list(ROOT.glob("site/*.md")):
            chars |= set(md.read_text(encoding="utf-8"))
        missing = sorted(c for c in chars if not c.isspace() and not covers(c))
        self.assertEqual([f"U+{ord(c):04X}" for c in missing], [])


class Weights(unittest.TestCase):
    """D-0027: two weights only, 400 and 700."""

    def test_only_two_weights(self):
        for css in ("site/site.css", "themes/modern.css"):
            text = STRIP.sub("", (ROOT / css).read_text(encoding="utf-8"))
            found = set(re.findall(r"font-weight\s*:\s*(\d+)", text))
            found |= set(re.findall(r"font\s*:\s*(\d{3})\s", text))
            with self.subTest(css=css):
                self.assertTrue(found <= {"400", "700"}, found)


class Embedded(unittest.TestCase):

    def test_pages_embed_the_font(self):
        page = ROOT / "build" / "site" / "index.html"
        text = page.read_text(encoding="utf-8")
        self.assertEqual(text.count("@font-face"), len(STYLES))
        self.assertNotIn('url("fonts/', text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Write the subsetting script.** Create `tools/subset_fonts.py`:

```python
"""Subset Open Sans to Latin and Greek as WOFF2 (DECISIONS D-0025, D-0027).

One-time tool, run by hand; CI imports only UNICODES and covers().
Needs fontTools and brotli: python -m pip install --user fonttools brotli

Usage: python tools/subset_fonts.py SRC_DIR
SRC_DIR holds OpenSans-{Regular,Bold,Italic,BoldItalic}.ttf from
github.com/googlefonts/opensans (fonts/ttf/). Output: site/fonts/*.woff2.
"""

import os
import subprocess
import sys

STYLES = ("Regular", "Bold", "Italic", "BoldItalic")

# Latin: Basic Latin and Latin-1 (includes the degree, plus-minus, micro and
# multiplication signs), the OE ligatures, spacing modifiers for quotes,
# General Punctuation (dashes, quotes, primes, bullets), the euro and trade
# marks, arrows used as hint glyphs, and the true minus sign. Greek: the
# Greek and Coptic block, for symbols in physics text.
UNICODES = [
    (0x0000, 0x00FF), (0x0131, 0x0131), (0x0152, 0x0153),
    (0x02BB, 0x02BC), (0x02C6, 0x02C6), (0x02DA, 0x02DA), (0x02DC, 0x02DC),
    (0x2000, 0x206F), (0x20AC, 0x20AC), (0x2122, 0x2122),
    (0x2190, 0x2193), (0x2212, 0x2212), (0x2215, 0x2215),
    (0xFEFF, 0xFEFF), (0xFFFD, 0xFFFD),
    (0x0370, 0x03FF),
]


def covers(ch):
    cp = ord(ch)
    return any(a <= cp <= b for a, b in UNICODES)


def unicodes_arg():
    return ",".join(f"U+{a:04X}-{b:04X}" if a != b else f"U+{a:04X}" for a, b in UNICODES)


def main(src):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "site", "fonts")
    os.makedirs(out, exist_ok=True)
    for style in STYLES:
        subprocess.run([
            sys.executable, "-m", "fontTools.subset",
            os.path.join(src, f"OpenSans-{style}.ttf"),
            "--unicodes=" + unicodes_arg(),
            "--layout-features=*",
            "--flavor=woff2",
            "--output-file=" + os.path.join(out, f"OpenSans-{style}.woff2"),
        ], check=True)
        print(style, os.path.getsize(os.path.join(out, f"OpenSans-{style}.woff2")), "bytes")


if __name__ == "__main__":
    main(sys.argv[1])
```

- [ ] **Step 3: Run the coverage test before any download.** Run: `"$PY" -m unittest tests.test_fonts.FontFiles.test_subset_covers_our_text -v`. Expected: PASS. If it lists code points, add them to `UNICODES` (and say so in the commit body) before subsetting.

- [ ] **Step 4: Fetch, verify, subset (approved download only).**

```bash
GH="/c/Program Files/GitHub CLI/gh.exe"
mkdir -p build/font-src
SHA=$("$GH" api repos/googlefonts/opensans/commits/main --jq .sha); echo "$SHA"
for s in Regular Bold Italic BoldItalic; do
  "$GH" api "repos/googlefonts/opensans/contents/fonts/ttf/OpenSans-$s.ttf?ref=$SHA" -H "Accept: application/vnd.github.raw" > "build/font-src/OpenSans-$s.ttf"
done
"$GH" api "repos/googlefonts/opensans/contents/OFL.txt?ref=$SHA" -H "Accept: application/vnd.github.raw" > site/fonts/OFL.txt
wc -c build/font-src/*.ttf site/fonts/OFL.txt
"$PY" -m pip install --user fonttools brotli
"$PY" -m pip show fonttools brotli | grep -E "^(Name|Version)"
"$PY" tools/subset_fonts.py build/font-src
```

Expected: sizes 147528, 147264, 153256, 153308 and 4216; if any differs, stop and report. Note the commit SHA, the two package versions and the four output sizes.

- [ ] **Step 5: Write `site/fonts/README.md`** with: source repository and the commit SHA from Step 4; the SIL Open Font License 1.1 (text in `OFL.txt`, which must travel with the fonts); the subset (Latin and Greek, `tools/subset_fonts.py`); fontTools and brotli versions; each file's size; and the rulings (D-0006, D-0025, D-0027).

- [ ] **Step 6: Use the font.** In `site/site.css`, at the top after the header comment:

```css
@font-face { font-family: "Open Sans"; font-style: normal; font-weight: 400; src: url("fonts/OpenSans-Regular.woff2") format("woff2"); }
@font-face { font-family: "Open Sans"; font-style: normal; font-weight: 700; src: url("fonts/OpenSans-Bold.woff2") format("woff2"); }
@font-face { font-family: "Open Sans"; font-style: italic; font-weight: 400; src: url("fonts/OpenSans-Italic.woff2") format("woff2"); }
@font-face { font-family: "Open Sans"; font-style: italic; font-weight: 700; src: url("fonts/OpenSans-BoldItalic.woff2") format("woff2"); }
```

Replace every `ui-sans-serif, system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif` in `site/site.css` and `themes/modern.css` with `"Open Sans", ui-sans-serif, system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`. The `@font-face` rules live only in `site/site.css`, which every site-built page loads, so the font is embedded once per page; a single-file render without chrome falls back to the system stack. Weights (D-0027): `site/site.css` 600 and 650 to 700; `themes/modern.css` 650 to 700 and 500 to 400. `themes/faithful.css` is not touched (D-0010).

- [ ] **Step 7: Build and run everything.** Run: `PANDOC="$PANDOC" "$PY" tools/render.py --site && "$PY" -m unittest discover -s tests -v`. Expected: all pass, including `test_pages_embed_the_font` (Pandoc embeds CSS `url()` references relative to the stylesheet). Report the largest built page: `find build/site -name index.html -printf "%s %p\n" | sort -n | tail -3`.

- [ ] **Step 8: Commit.**

```bash
git add tools/subset_fonts.py site/fonts tests/test_fonts.py site/site.css themes/modern.css
git commit -m "Self-host Open Sans, subset to Latin and Greek" -m "D-0006, D-0025, D-0027: four static styles from googlefonts/opensans at the recorded commit, subset to WOFF2 with fontTools, OFL text alongside. The chrome and the modern presentation use it; weights collapse to 400 and 700. A test checks every character of our text is in the subset."
```

---

### Task 7: Open Sans inside the sim (STOP: needs D-0027 and D-0028 ruled, Task 6 done)

**Files:**
- Modify: `sims/modified-electric-force/index.html` (CSP, `@font-face`, font stack, weight), `sims/modified-electric-force/test-law.mjs` (data-URI stripping), `tools/render.py` (`SIM_CHROME` font stack)

**Interfaces:**
- Consumes: `site/fonts/OpenSans-Regular.woff2`, `-Bold.woff2` from Task 6.

- [ ] **Step 1: Write the failing check.** In `test-law.mjs`, after `const html = read("index.html");` add:

```js
// DECISIONS D-0028: page-text checks skip embedded data (base64 fonts can
// contain any letters by chance); network, policy and hash checks still
// read the whole file.
const pageText = html.replace(/data:[^"')\s]+/g, "data:");
```

change the "identity fields" and "law's form" checks to test `pageText` instead of `html` (the name `text` is already used in two inner blocks of this file), and add:

```js
check("index.html embeds Open Sans", /@font-face\s*\{[^}]*font-family:\s*"Open Sans"/.test(html) && /font-src data:/.test(html));
```

- [ ] **Step 2: Run it and watch it fail.** Run: `cd sims/modified-electric-force && node test-law.mjs; cd ../..`. Expected: exactly one failure, "index.html embeds Open Sans".

- [ ] **Step 3: Implement.** Confirm the sim uses no italics (`grep -n "italic\|<em>\|<i>" sims/modified-electric-force/index.html`; if any appear, stop and report, since only Regular and Bold are embedded). Then:

```bash
"$PY" - <<'EOF'
import base64
from pathlib import Path
p = Path("sims/modified-electric-force/index.html")
s = p.read_text(encoding="utf-8")
csp = "img-src data:;"
assert s.count(csp) == 1
s = s.replace(csp, "img-src data:; font-src data:;")
faces = "".join(
    '  @font-face { font-family: "Open Sans"; font-style: normal; font-weight: %d; '
    'src: url(data:font/woff2;base64,%s) format("woff2"); }\n'
    % (w, base64.b64encode(Path(f"site/fonts/OpenSans-{n}.woff2").read_bytes()).decode("ascii"))
    for n, w in (("Regular", 400), ("Bold", 700)))
assert s.count("<style>\n") >= 1
s = s.replace("<style>\n", "<style>\n" + faces, 1)
stack = 'font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;'
assert s.count(stack) == 1
s = s.replace(stack, 'font-family: "Open Sans", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;')
p.write_text(s, encoding="utf-8", newline="\n")
EOF
grep -n "font-weight: 600\|font-weight:600" sims/modified-electric-force/index.html
```

Change each weight 600 printed by the grep to 700 (D-0027). In `tools/render.py` `SIM_CHROME`, put `"Open Sans", ` first in the `.lib-bar` font stack.

- [ ] **Step 4: Run every check.**

```bash
(cd sims/modified-electric-force && node test-law.mjs)
PANDOC="$PANDOC" "$PY" tools/render.py --site && "$PY" -m unittest discover -s tests -v
```

Expected: the sim test reports all passes (the legacy hash is unchanged, since `index.legacy.html` is not touched) and the Python suite passes (`SimBar.test_source_plus_bar_only` compares against the new source). Re-run the Task 5 Step 5 height measurement and record it in `STATE.md`.

- [ ] **Step 5: Commit.**

```bash
git add sims/modified-electric-force/index.html sims/modified-electric-force/test-law.mjs tools/render.py STATE.md
git commit -m "Embed Open Sans in the Electric Force sim" -m "D-0026, D-0027, D-0028: the sim's own file gains font-src data: and Regular and Bold as data: URIs, so it stays one offline file and the published copy still differs only by the bar. The sim's page-text checks now skip embedded data, which could spell a banned word by chance; the network, policy and legacy-hash checks still read everything."
```

---

### Task 8: Measure, record, hand off

**Files:**
- Modify: `STATE.md`, `CLAUDE.md`

- [ ] **Step 1: Phone width.** With the server from Task 5 running, set the pane to 375 by 812 and, on `/`, `/courses/`, `/how-this-was-made/`, `/sims/` and `/labs/ph211-team-building-handout/modern/`, run `document.documentElement.scrollWidth <= 375`. Expected: `true` on each. Record the results.

- [ ] **Step 2: Page weight.** Run `find build/site -name index.html -printf "%s %p\n" | sort -n | tail -5` and record the largest pages for the owner's judgment (spec 6; no threshold is ruled).

- [ ] **Step 3: Screenshots.** Take a 1280-wide screenshot of `/` and of the sim for the D-0012 heads-up the owner sends to University Marketing. The owner sends it; nothing is sent from here.

- [ ] **Step 4: Update `CLAUDE.md`** under "Build": the header and footer are the partials `tools/brandheader.html` and `tools/brandfooter.html`; logo files live in `site/brand/` and must never be edited; fonts live in `site/fonts/` and are rebuilt only with `tools/subset_fonts.py`; the tests run after the site build and need `build/site/`.

- [ ] **Step 5: Update `STATE.md`** (one screen): focus done, the measurements, pilot measures (spec gaps, owner corrections, promotions without edits), and what awaits the owner (Marketing heads-up per D-0012, the pilot comparison feature and verdict date).

- [ ] **Step 6: Verify and open the PR.**

```bash
grep -rIl $'\xe2\x80\x94' --exclude-dir=.git --exclude-dir=originals --exclude-dir=build . ; echo "em-dash scan exit $? (1 means none)"
git config user.name; git config user.email
git add STATE.md CLAUDE.md
git commit -m "Record the branding refresh's measurements and runbook notes" -m "Phone-width, sim-height and page-weight measurements from the built site; CLAUDE.md learns where the header partials, logo files and fonts live."
git push -u origin branding-refresh
"/c/Program Files/GitHub CLI/gh.exe" pr create --title "Brand the site chrome to OSU department style" --body "Implements docs/superpowers/specs/2026-09-21-site-branding-design.md per the plan of the same date. Ledger: see the plan header. Measurements in STATE.md."
```

Expected: `verify` green on the PR before anyone merges it.
