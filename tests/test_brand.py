"""Brand tests: each asserts a bracketed quantity in a ruled DECISIONS.md entry.

Standard library only, so CI needs no install step. Run from the repo root:
    python -m unittest discover -s tests -v

Palette values and contrast figures come from OSU-branding/OSU-style-guide.md in the
sandbox (supplied by the owner 2026-09-19), which is not in this repo; the
values are restated here as the ruled quantities.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_CSS = ROOT / "site" / "site.css"

BEAVER_ORANGE = "D73F09"
PADDLETAIL_BLACK = "000000"
BUCKTOOTH_WHITE = "FFFFFF"
STAR_CANVAS = "003B5C"
LUMINANCE = "FFB500"

AA_NORMAL = 4.5            # WCAG 2.x AA, normal text
LARGE_BOLD_PX = 18         # style guide: 18 px bold is large text
LARGE_REGULAR_PX = 24      # style guide: 24 px regular is large text
BOLD_WEIGHT = 700
ROOT_PX = 16               # rem base; the site sets no root font size


def norm_hex(value):
    """'#fff' or '#d73f09' to 'FFFFFF' or 'D73F09'."""
    h = value.strip().lstrip("#").upper()
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return h


def luminance(hex6):
    def chan(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex6[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def css_text():
    # Comments out, so prose inside them never reads as a declaration.
    return re.sub(r"/\*.*?\*/", "", SITE_CSS.read_text(encoding="utf-8"), flags=re.S)


def light_root_tokens():
    """Custom properties of the first :root block, the light theme."""
    block = re.search(r":root\s*\{(.*?)\}", css_text(), re.S).group(1)
    return dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", block))


def rules(text=None):
    """Innermost (selector, body) pairs; @media wrappers are skipped over."""
    return re.findall(r"([^{}]+)\{([^{}]*)\}", css_text() if text is None else text)


def to_px(size):
    size = size.strip()
    if size.endswith("rem"):
        return float(size[:-3]) * ROOT_PX
    if size.endswith("px"):
        return float(size[:-2])
    return None


class BrandPalette(unittest.TestCase):
    """D-0004 and D-0008: the chrome's brand tokens hold the palette values."""

    def test_palette_tokens(self):
        t = light_root_tokens()
        self.assertEqual(norm_hex(t["--chrome-accent"]), BEAVER_ORANGE)
        self.assertEqual(norm_hex(t["--chrome-ink"]), PADDLETAIL_BLACK)
        self.assertEqual(norm_hex(t["--chrome-paper"]), BUCKTOOTH_WHITE)
        self.assertEqual(norm_hex(t["--chrome-heading"]), STAR_CANVAS)


class BrandContrast(unittest.TestCase):
    """D-0008: the contrast figures the ruling rests on are computed, not copied."""

    def test_orange_on_white(self):
        self.assertEqual(round(contrast(BEAVER_ORANGE, BUCKTOOTH_WHITE), 2), 4.56)

    def test_orange_on_white_meets_aa(self):
        self.assertGreaterEqual(contrast(BEAVER_ORANGE, BUCKTOOTH_WHITE), AA_NORMAL)

    def test_star_canvas_on_white(self):
        self.assertEqual(round(contrast(STAR_CANVAS, BUCKTOOTH_WHITE), 2), 11.80)


class OrangeTextIsLarge(unittest.TestCase):
    """D-0008: any rule that colors text Beaver Orange sets large text:
    at least 24 px, or at least 18 px at weight 700 or more."""

    def small_orange(self, text=None):
        """Selectors that color text Beaver Orange below large-text size."""
        bad = []
        for selector, body in rules(text):
            decl = dict(re.findall(r"([\w-]+)\s*:\s*([^;]+);?", body))
            color = decl.get("color", "").strip()
            orange = color == "var(--chrome-accent)" or (
                color.startswith("#") and norm_hex(color) == BEAVER_ORANGE)
            if not orange:
                continue
            px = to_px(decl.get("font-size", ""))
            weight = int(decl.get("font-weight", "400").strip() or 400)
            if px is None or not (
                    px >= LARGE_REGULAR_PX or (px >= LARGE_BOLD_PX and weight >= BOLD_WEIGHT)):
                bad.append(selector.strip())
        return bad

    def test_orange_text_is_large(self):
        self.assertEqual(self.small_orange(), [])

    def test_checker_catches_small_orange(self):
        # The guard passes vacuously today (no orange text yet), so prove it
        # can fail, and that the thresholds sit where the ruling puts them.
        css = """
        .small { color: var(--chrome-accent); font-size: 1rem; }
        .bold18 { color: #d73f09; font-size: 18px; font-weight: 700; }
        .reg18 { color: #D73F09; font-size: 18px; }
        .reg24 { color: var(--chrome-accent); font-size: 1.5rem; }
        .nosize { color: var(--chrome-accent); }
        """
        self.assertEqual(self.small_orange(css), [".small", ".reg18", ".nosize"])


class DraftBanner(unittest.TestCase):
    """D-0022: the draft banner is Luminance with black text."""

    def test_black_on_luminance(self):
        self.assertEqual(round(contrast(LUMINANCE, PADDLETAIL_BLACK), 2), 11.86)

    # Not built yet. Strict by construction: when the refresh lands this
    # passes, unittest reports an unexpected success as a failure, and the
    # decorator has to come off. It is reported as an expected failure, never
    # counted as a pass.
    @unittest.expectedFailure
    def test_banner_colors(self):
        for selector, body in rules():
            if selector.strip() == ".draft-banner":
                decl = dict(re.findall(r"([\w-]+)\s*:\s*([^;]+);?", body))
                t = light_root_tokens()
                bg = decl.get("background", "").strip()
                fg = decl.get("color", "").strip()
                resolve = lambda v: norm_hex(t[v[4:-1]] if v.startswith("var(") else v)
                self.assertEqual(resolve(bg), LUMINANCE)
                self.assertEqual(resolve(fg), PADDLETAIL_BLACK)
                return
        self.fail("no .draft-banner rule")


if __name__ == "__main__":
    unittest.main()
