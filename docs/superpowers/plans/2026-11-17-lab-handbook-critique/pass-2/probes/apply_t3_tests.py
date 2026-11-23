"""T3, step 1: the Addresses test appended to tests/test_lab_handbook.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

p = Path("tests/test_lab_handbook.py")
p.write_text(p.read_text(encoding="utf-8") + "\n\n" + extract.blocks()[14][1], encoding="utf-8", newline="\n")
print("appended")
