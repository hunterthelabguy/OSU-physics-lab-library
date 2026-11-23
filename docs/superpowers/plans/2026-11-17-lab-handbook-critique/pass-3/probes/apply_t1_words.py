"""Apply T1's "Amend the words" step (plan lines 286 to 317), as written.

Run from the scratch tree's root: python -X utf8 apply_t1_words.py BLOCKS
"""
import sys
import textwrap
from pathlib import Path

B = Path(sys.argv[1])


def block(n, ext):
    return (B / "{:02d}.{}".format(n, ext)).read_text(encoding="utf-8")


def norm(s):
    return " ".join(s.split())


def once(text, old, new, what):
    assert text.count(old) == 1, (what, text.count(old))
    return text.replace(old, new, 1)


# site/landing.md: the two lines (block 13) become one.
p = Path("site/landing.md")
t = p.read_text(encoding="utf-8")
t = once(t, block(13, "markdown"), "  How a page is built and who did the work.\n", "landing")
p.write_text(t, encoding="utf-8", newline="\n")

# CLAUDE.md: bullets matched with whitespace normalised.
p = Path("CLAUDE.md")
lines = p.read_text(encoding="utf-8").split("\n")


def bullets(lines):
    """(start, end) of each top-level "- " bullet, end exclusive."""
    out, i = [], 0
    while i < len(lines):
        if lines[i].startswith("- "):
            j = i + 1
            while j < len(lines) and lines[j].startswith("  ") and lines[j].strip():
                j += 1
            out.append((i, j))
            i = j
        else:
            i += 1
    return out


hits = [(a, b) for a, b in bullets(lines)
        if norm(" ".join(lines[a:b])).startswith("- Conversion first, then ruled changes (D-0168).")
        and norm(" ".join(lines[a:b])).endswith("Never loosen the check for a change.")]
assert len(hits) == 1, hits
a, b = hits[0]
lines[a:b] = block(14, "markdown").rstrip("\n").split("\n")

hits = [(a, b) for a, b in bullets(lines)
        if norm(" ".join(lines[a:b])).startswith("- One Markdown source feeds one presentation")]
assert len(hits) == 1, hits
a, b = hits[0]
text = norm(" ".join(lines[a:b]))
anchor = "never copy content into a second file"
assert text.count(anchor) == 1
text = text.replace(anchor, anchor + " (one exception, until PH 211's appendix copies are cut: the Lab "
                    "Handbook's sections, D-0191, held to Lab 7's by a test, D-0198; a change reaches "
                    "every copy in one PR)")
lines[a:b] = textwrap.wrap(text, 76, subsequent_indent="  ", break_long_words=False,
                           break_on_hyphens=False)
p.write_text("\n".join(lines), encoding="utf-8", newline="\n")

# docs/conversion-spec.md: line 21's comment; a paragraph after the check's first.
p = Path("docs/conversion-spec.md")
t = p.read_text(encoding="utf-8")
t = once(t, "status: converted                 # converted | checked | ruled-change\n",
         "status: converted                 # converted | checked | ruled-change (the Word checks skip ruled-change, D-0195)\n",
         "spec line 21")
t = once(t, "every file with a `source_file` (ledger 20).\n",
         "every file with a `source_file` (ledger 20).\n\n" + block(15, "markdown").rstrip("\n") + "\n",
         "spec paragraph")
p.write_text(t, encoding="utf-8", newline="\n")
print("T1 words applied")
