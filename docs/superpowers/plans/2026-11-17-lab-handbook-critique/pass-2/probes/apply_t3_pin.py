"""T3: the handbook's empty pin, as written."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

p = Path("tests/question-ids.json")
text = p.read_text(encoding="utf-8")
OLD = '  "ph21x-problem-solving-strategy": []\n'
assert text.count(OLD) == 1 and text.endswith(OLD + " }\n}\n")
text = text.replace(OLD, extract.blocks()[17][1])
p.write_text(text, encoding="utf-8", newline="\n")
print("pinned")
