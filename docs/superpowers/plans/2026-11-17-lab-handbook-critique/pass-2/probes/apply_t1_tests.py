"""T1, step 1: the plan's three test blocks, as written. Run from the tree root."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

B = extract.blocks()
GUARD = '\n\nif __name__ == "__main__":\n    unittest.main()\n'


def add_imports(text):
    # "add `import contextlib` and `import io` to its imports", alphabetical
    lines = text.split("\n")
    first = next(i for i, l in enumerate(lines) if l.startswith("import "))
    lines.insert(first, "import contextlib")
    io_at = next(i for i, l in enumerate(lines) if l.startswith("import ") and l > "import io")
    lines.insert(io_at, "import io")
    return "\n".join(lines)


for name, block in (("tests/test_check_unchanged.py", 1), ("tests/test_check_numbers.py", 2)):
    p = Path(name)
    text = add_imports(p.read_text(encoding="utf-8"))
    assert text.endswith(GUARD), name
    # "At the end": before the main guard, so the class also runs as a script.
    text = text[:-len(GUARD)] + "\n\n" + B[block][1].rstrip("\n") + "\n" + GUARD
    p.write_text(text, encoding="utf-8", newline="\n")

Path("tests/test_check_em_dash.py").write_text(B[3][1], encoding="utf-8", newline="\n")
print("tests written")
