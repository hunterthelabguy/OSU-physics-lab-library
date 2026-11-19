"""Writes the plan's T4 script (block 21) to the path given."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

Path(sys.argv[1]).write_text(extract.blocks()[21][1], encoding="utf-8", newline="\n")
