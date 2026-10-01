"""One Pandoc (D-0044, D-0045, D-0046): Quarto migration phase 3.

PANDOC is the Pandoc bundled with the pinned Quarto, so the word check, the
chrome lift and the tests read with the Pandoc the Quarto pages render with.
PANDOC_OLD_BUILD is the standalone Pandoc the old build keeps until phase 4,
because production is built with it. A tool that is missing or will not run
fails a test, never skips it (LEDGER 53 by analogy).
"""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))
import quarto_build                       # noqa: E402
from test_quarto_site import converted    # noqa: E402  (the CI rule for converted files)

PANDOC = os.environ.get("PANDOC", "pandoc")
PANDOC_OLD_BUILD = os.environ.get("PANDOC_OLD_BUILD")
QUARTO = quarto_build.QUARTO


def run(case, cmd):
    """stdout of cmd; a tool that is missing or exits non-zero fails the test."""
    try:
        return subprocess.run(cmd, capture_output=True, check=True,
                              encoding="utf-8").stdout
    except OSError as e:
        case.fail("cannot run {!r}: {}".format(cmd[0], e))
    except subprocess.CalledProcessError as e:
        case.fail("{!r} exited {}: {}".format(cmd[0], e.returncode, e.stderr.strip()))


def tree(case, pandoc, path):
    """The syntax tree the word check reads: blocks and metadata."""
    doc = json.loads(run(case, [pandoc, "-f", "markdown-smart", "-t", "json", str(path)]))
    return doc["blocks"], doc["meta"]


class OnePandoc(unittest.TestCase):

    def test_pandoc_is_quartos(self):
        # D-0044. Compared with `quarto pandoc`, not a literal, so a Quarto
        # upgrade moves Pandoc with no second pin. `quarto pandoc` is for this
        # one-line output only; the tools never call Pandoc that way (D-0045).
        ours = run(self, [PANDOC, "--version"]).splitlines()[0]
        quartos = run(self, [QUARTO, "pandoc", "--version"]).splitlines()[0]
        self.assertEqual(ours, quartos,
                         "PANDOC is not the Pandoc bundled with Quarto: point it "
                         "at the binary in Quarto's install (CLAUDE.md, Build)")

    def test_old_build_pandoc_reads_the_same_tree(self):
        # D-0046: production builds with the standalone Pandoc while the word
        # check reads with Quarto's. This keeps "the check covers what
        # production shows" true until phase 4 deletes the old build.
        if not PANDOC_OLD_BUILD:
            self.fail("PANDOC_OLD_BUILD is not set: point it at the standalone "
                      "Pandoc production uses (CLAUDE.md, Build)")
        files = [path for _, path in converted()]
        self.assertTrue(files, "no converted files found")
        for path in files:
            rel = path.relative_to(ROOT).as_posix()
            with self.subTest(file=rel):
                same = tree(self, PANDOC, path) == tree(self, PANDOC_OLD_BUILD, path)
                self.assertTrue(same, "the two Pandocs read " + rel + " to different trees")


if __name__ == "__main__":
    unittest.main()
