"""Extract fenced code blocks from the plan, numbered, to apply them verbatim."""
import re, sys
plan = open(sys.argv[1], encoding="utf-8").read()
blocks = re.findall(r"^```(\w*)\n(.*?)^```\s*$", plan, re.S | re.M)
for i, (lang, body) in enumerate(blocks):
    print("=== block", i, lang, len(body.splitlines()), "lines; first:", body.splitlines()[0][:70])
