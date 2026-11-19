"""T2, step 1: tests/test_lab_handbook.py as written. Run from the tree root."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

Path("tests/test_lab_handbook.py").write_text(extract.blocks()[11][1], encoding="utf-8", newline="\n")
print("written")
