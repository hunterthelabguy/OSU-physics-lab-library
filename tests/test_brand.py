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

# The style guide's primary and secondary colors (Electric Beav has no
# values and is print only). D-0008: the chrome uses nothing else.
PALETTE = {
    "D73F09", "000000", "FFFFFF",                      # primary
    "4A773C", "00859B", "FFB500", "006A8E", "C4D6A4",  # Pine Stand .. Reindeer Moss
    "B8DDE1", "FDD26E", "C6DAE7", "AA9D2E", "0D5257",  # Seafoam .. Rogue Wave
    "D3832B", "003B5C", "B7A99A", "A7ACA2", "7A6855",  # Solar Flare .. High Desert
    "8E9089",                                          # Crater
}


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


class NoDraftBanner(unittest.TestCase):
    """D-0156 (amending D-0022): the draft banner is gone from the chrome
    CSS, its Luminance token with it. Luminance itself stays, as the
    checkpoint's rule (D-0115, tested below)."""

    def test_no_banner_rules_or_words_in_site_css(self):
        text = SITE_CSS.read_text(encoding="utf-8")
        for gone in ("draft-banner", "draft-more", "draft-detail", "--chrome-warn",
                     "license pending"):
            self.assertNotIn(gone, text.lower())
        self.assertEqual([s for s, _ in rules() if "draft" in s], [])


class Widths(unittest.TestCase):
    """LEDGER 56 to 58 and D-0070 (proposed): two widths. Prose keeps the
    [68ch] measure everywhere; the shell is [72rem] for document pages and
    [96rem] (1,536 px) on site pages."""

    def site_page_tokens(self):
        found = {}
        for selector, body in rules():
            if selector.strip() == "body.site-page":
                found.update(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", body))
        return found

    def test_measure_68ch(self):
        self.assertEqual(light_root_tokens()["--chrome-measure"].strip(), "68ch")
        self.assertNotIn("--chrome-measure", self.site_page_tokens())

    def test_document_shell_72rem(self):
        self.assertEqual(light_root_tokens()["--chrome-shell"].strip(), "72rem")

    def test_site_page_shell_96rem(self):
        shell = self.site_page_tokens()["--chrome-shell"].strip()
        self.assertEqual(shell, "96rem")
        self.assertEqual(to_px(shell), 1536)


class PaletteOnly(unittest.TestCase):
    """D-0008 and D-0015: every color in the chrome is a palette value."""

    def test_site_css_palette_only(self):
        found = {norm_hex(h) for h in re.findall(r"#[0-9a-fA-F]{3,6}\b", css_text())}
        self.assertEqual(sorted(found - PALETTE), [])


class CheckpointColours(unittest.TestCase):
    """D-0115: the checkpoint block is Candela with a Luminance rule on the
    light page, the dark tint with a Luminance rule on the dark page."""

    MODERN = re.sub(r"/\*.*?\*/", "", (ROOT / "themes" / "modern.css").read_text(encoding="utf-8"), flags=re.S)

    def tokens(self, pattern):
        block = re.search(pattern, self.MODERN, re.S).group(1)
        return {k: norm_hex(v) for k, v in re.findall(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,6})\s*;", block)}

    def test_light_is_candela_and_luminance(self):
        light = self.tokens(r":root\s*\{(.*?)\}")
        self.assertEqual(light["--checkpoint-rule"], LUMINANCE)
        self.assertEqual(light["--checkpoint-fill"], "FDD26E")    # Candela
        self.assertLessEqual({light["--checkpoint-rule"], light["--checkpoint-fill"]}, PALETTE)
        # Text on the fill: the body's ink and the label's --quiet.
        self.assertGreaterEqual(contrast(light["--ink"], light["--checkpoint-fill"]), AA_NORMAL)
        self.assertGreaterEqual(contrast(light["--quiet"], light["--checkpoint-fill"]), AA_NORMAL)

    def test_dark_rule_shows_on_the_dark_tint(self):
        dark = self.tokens(r":root:not\(\[data-theme=\"light\"\]\)\s*\{(.*?)\}")
        light = self.tokens(r":root\s*\{(.*?)\}")
        self.assertEqual(dark["--checkpoint-fill"], dark["--tint"])
        self.assertNotIn("--checkpoint-rule", dark, "the rule stays Luminance")
        self.assertGreaterEqual(contrast(light["--checkpoint-rule"], dark["--checkpoint-fill"]), 3)


class DrawnFigurePaper(unittest.TestCase):
    """A drawn figure sits on Word's white page in both themes: its lines and
    labels keep Word's colours, black in PH 213 Lab 4 (WCAG 1.4.3, 1.4.11)."""

    MODERN = CheckpointColours.MODERN
    tokens = CheckpointColours.tokens

    def test_white_in_light_and_dark(self):
        light = self.tokens(r":root\s*\{(.*?)\}")
        dark = self.tokens(r":root:not\(\[data-theme=\"light\"\]\)\s*\{(.*?)\}")
        self.assertEqual(light["--figure-paper"], "FFFFFF")
        self.assertNotIn("--figure-paper", dark, "the figure's paper is not themed")
        self.assertGreaterEqual(contrast("000000", light["--figure-paper"]), AA_NORMAL)

    def test_the_figure_takes_it(self):
        rules = re.findall(r"main svg\.drawn-figure\s*\{([^}]*)\}", self.MODERN)
        self.assertTrue(any("background: var(--figure-paper)" in r for r in rules))


if __name__ == "__main__":
    unittest.main()
