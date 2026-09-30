"""The Quarto build's warning gate, tools/quarto_build.py (D-0033, phase 1).

Any Quarto warning line fails the build. Quarto prints its own warnings as
`WARN: ...` and Pandoc's as `[WARNING] ...`; the gate must catch both and
must not trip on the ordinary progress lines.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from quarto_build import WARNING            # noqa: E402


class WarningGate(unittest.TestCase):

    def test_quarto_warn_line(self):
        self.assertIsNotNone(WARNING.search("WARN: Unable to resolve link target: x.qmd"))

    def test_plain_warning_line(self):
        self.assertIsNotNone(WARNING.search("WARNING: something"))

    def test_pandoc_bracketed_warning_line(self):
        line = "[WARNING] Note with key '1' defined at line 11 column 1 but not used."
        self.assertIsNotNone(WARNING.search(line))

    def test_progress_line_is_not_a_warning(self):
        self.assertIsNone(WARNING.search("[1/6] index.qmd"))

    def test_found_inside_a_whole_log(self):
        clean = "[1/2] index.qmd\n\n[2/2] courses\\index.qmd\n\nOutput created: build\\quarto-site\\index.html\n"
        self.assertIsNone(WARNING.search(clean))
        self.assertIsNotNone(WARNING.search(clean + "[WARNING] a Pandoc note\n"))
        self.assertIsNotNone(WARNING.search(clean + "WARN: a Quarto note\n"))


if __name__ == "__main__":
    unittest.main()
