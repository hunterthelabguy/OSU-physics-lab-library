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
    # The header logo, one cached file for every page (D-0039 amended).
    "site/brand/OSU_horizontal_2C_W_over_B.png",
    # The course index's Download all script (D-0067).
    "site/download-all.js",
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


def ci_steps():
    """(name, text) of each step of verify.yml, in order."""
    ci = (ROOT / ".github" / "workflows" / "verify.yml").read_text(encoding="utf-8")
    steps = []
    for text in re.split(r"^      - (?=name:|uses:)", ci, flags=re.M)[1:]:
        m = re.match(r"name:[ ]*(.*)", text)
        steps.append((m.group(1).strip() if m else text.splitlines()[0], text))
    return steps


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
        # D-0039 amended: fonts, their license and the one header logo.
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

    def test_ci_uses_quartos_pandoc(self):
        # D-0044, D-0061. CI's PANDOC is Quarto's bundled binary, and no step
        # names a standalone Pandoc: phase 4 retired the old build that kept
        # one. No version literal: test_one_pandoc.py compares the binary
        # with `quarto pandoc` itself.
        steps = ci_steps()
        names = [name for name, _ in steps]
        quarto = [i for i, (_, body) in enumerate(steps) if "quarto-cli/releases" in body]
        export = [i for i, (_, body) in enumerate(steps)
                  if "GITHUB_ENV" in body and re.search(r"\bPANDOC=", body)]
        self.assertEqual(len(quarto), 1)
        self.assertEqual(len(export), 1, "exactly one step exports PANDOC")
        self.assertIn("Content unchanged", names)
        self.assertLess(quarto[0], export[0])
        self.assertLess(export[0], names.index("Content unchanged"))
        body = steps[export[0]][1]
        self.assertIn("--version", body, "the step prints the version it found")
        self.assertIn("exit 1", body, "the step fails when the binary is missing")

        for name, body in steps:
            with self.subTest(step=name):
                self.assertNotRegex(body, r"(?m)^\s+PANDOC(_OLD_BUILD)?:", "a step sets its own Pandoc")
                self.assertNotIn("jgm/pandoc/releases", body, "a step installs a standalone Pandoc")
                self.assertNotIn("/usr/bin/pandoc", body)


if __name__ == "__main__":
    unittest.main()
