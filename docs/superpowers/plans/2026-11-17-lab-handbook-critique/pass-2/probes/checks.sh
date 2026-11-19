#!/bin/bash
# The two Word checks on every file the plan's Verify selects; run from the
# tree root: bash checks.sh OUTDIR
set -u
out="$1"
mkdir -p "$out"
export PANDOC="/c/Program Files/Quarto/bin/tools/pandoc.exe"
files=$(for f in $(git ls-files '*.md'); do [ "$(head -1 "$f")" = "---" ] && sed -n '2,/^---$/p' "$f" | grep -q '^source_file:' && echo "$f"; done)
echo "$files" > "$out/files.txt"
python -X utf8 tools/check_unchanged.py $files > "$out/unchanged.txt" 2>&1; echo "exit=$?" >> "$out/unchanged.txt"
python -X utf8 tools/check_numbers.py $files > "$out/numbers.txt" 2>&1; echo "exit=$?" >> "$out/numbers.txt"
