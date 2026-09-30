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
