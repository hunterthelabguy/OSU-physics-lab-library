"""questions.lua has one presentation, modern (D-0108, retiring the faithful one)."""

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

    def test_a_faithful_request_renders_modern(self):
        # D-0108: no "N)" prefix and no kept bold, whatever theme is asked for.
        for meta in ("theme-name=faithful", "theme=faithful"):
            with self.subTest(meta=meta):
                out = render(meta)
                self.assertIn("Question 1", out)
                self.assertNotIn("<strong>1)", out)

    def test_default_is_modern(self):
        self.assertIn("Question 1", render())


if __name__ == "__main__":
    unittest.main()
