"""Writes the plan's make_handbook.py (block 16) to the path given."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

Path(sys.argv[1]).write_text(extract.blocks()[16][1], encoding="utf-8", newline="\n")
