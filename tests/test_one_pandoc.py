"""One Pandoc (D-0044, D-0045, D-0061): Quarto migration phases 3 and 4.

PANDOC is the Pandoc bundled with the pinned Quarto, so the word check, the
chrome lift and the tests read with the Pandoc the Quarto pages render with.
Phase 4 retired the old build and the standalone Pandoc it kept (D-0046,
superseded by D-0061). A tool that is missing or will not run fails a test,
never skips it (LEDGER 53 by analogy).
"""

import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import quarto_build                       # noqa: E402

PANDOC = os.environ.get("PANDOC", "pandoc")
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


if __name__ == "__main__":
    unittest.main()
