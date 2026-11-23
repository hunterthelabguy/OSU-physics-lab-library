"""Fenced code blocks of the plan at 21d2f59, by index: python -X utf8 extract.py [N]."""
import subprocess
import sys

text = subprocess.run(["git", "show", "21d2f59:docs/superpowers/plans/2026-11-17-lab-handbook.md"],
                      capture_output=True, encoding="utf-8", check=True).stdout


def blocks():
    out, cur, lang = [], None, None
    for line in text.split("\n"):
        if line.startswith("```"):
            if cur is None:
                cur, lang = [], line[3:]
            else:
                out.append((lang, "\n".join(cur) + "\n"))
                cur = None
        elif cur is not None:
            cur.append(line)
    return out


if __name__ == "__main__":
    b = blocks()
    if len(sys.argv) > 1:
        sys.stdout.write(b[int(sys.argv[1])][1])
    else:
        for i, (lang, body) in enumerate(b):
            print(i, lang, repr(body.split("\n")[0][:70]), len(body.split("\n")))
