"""Apply T1's "Amend the words" step (plan lines 288 to 319), as written in
revision 2.3: "rewrap each changed paragraph or bullet to its own widest
line before the edit, never breaking "PH 211" or "D-0198" across lines",
and the conversion-spec paragraph "to that section's widest line".

Run from the scratch tree's root: python -X utf8 apply_t1_words.py BLOCKS
Prints each width it used.
"""
import sys
import textwrap
from pathlib import Path

B = Path(sys.argv[1])
NBSP = " "


def block(n, ext):
    return (B / "{:02d}.{}".format(n, ext)).read_text(encoding="utf-8")


def norm(s):
    return " ".join(s.split())


def once(text, old, new, what):
    assert text.count(old) == 1, (what, text.count(old))
    return text.replace(old, new, 1)


def wrap(words, width, first="", rest=""):
    words = words.replace("PH 211", "PH" + NBSP + "211")
    out = textwrap.wrap(words, width=width, initial_indent=first, subsequent_indent=rest,
                        break_long_words=False, break_on_hyphens=False)
    return [ln.replace(NBSP, " ") for ln in out]


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
w = max(len(x) for x in lines[a:b])
print("CLAUDE.md 'Conversion first' widest before the edit:", w)
lines[a:b] = wrap(norm(block(14, "markdown"))[2:], w, "- ", "  ")

hits = [(a, b) for a, b in bullets(lines)
        if norm(" ".join(lines[a:b])).startswith("- One Markdown source feeds one presentation")]
assert len(hits) == 1, hits
a, b = hits[0]
w = max(len(x) for x in lines[a:b])
print("CLAUDE.md 'One Markdown source' widest before the edit:", w)
text = norm(" ".join(lines[a:b]))
anchor = "never copy content into a second file"
assert text.count(anchor) == 1
text = text.replace(anchor, anchor + " (one exception, until PH 211's appendix copies are cut: the Lab "
                    "Handbook's sections, D-0191, held to Lab 7's by a test, D-0198; a change reaches "
                    "every copy in one PR)")
lines[a:b] = wrap(text[2:], w, "- ", "  ")
p.write_text("\n".join(lines), encoding="utf-8", newline="\n")

# docs/conversion-spec.md: line 21's comment; a paragraph after the check's first.
p = Path("docs/conversion-spec.md")
lines = p.read_text(encoding="utf-8").split("\n")
assert lines[20] == "status: converted                 # converted | checked | ruled-change", lines[20]
lines[20] = "status: converted                 # converted | checked | ruled-change (the Word checks skip ruled-change, D-0195)"
s = lines.index("## Content-unchanged check")
e = next(i for i in range(s + 1, len(lines)) if lines[i].startswith("## "))
w = max(len(x) for x in lines[s:e])
print("conversion-spec 'Content-unchanged check' section widest:", w)
end_first = next(i for i in range(s, e) if lines[i].endswith("(ledger 20)."))
lines[end_first + 1:end_first + 1] = [""] + wrap(norm(block(15, "markdown")), w)
p.write_text("\n".join(lines), encoding="utf-8", newline="\n")
print("T1 words applied")
