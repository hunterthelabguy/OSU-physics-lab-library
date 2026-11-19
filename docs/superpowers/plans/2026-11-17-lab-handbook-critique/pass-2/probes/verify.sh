#!/bin/bash
# The plan's full Verify, verbatim, from the tree root: bash verify.sh LOG
export QUARTO="/c/Program Files/Quarto/bin/quarto.exe"
export PANDOC="/c/Program Files/Quarto/bin/tools/pandoc.exe"
export CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
export PDFTOTEXT="$LOCALAPPDATA/Microsoft/WinGet/Packages/oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe/poppler-25.07.0/Library/bin/pdftotext.exe"
start=$(date +%s)
files=$(for f in $(git ls-files '*.md'); do [ "$(head -1 "$f")" = "---" ] && sed -n '2,/^---$/p' "$f" | grep -q '^source_file:' && echo "$f"; done)
python tools/check_em_dash.py && python tools/check_unchanged.py $files && python tools/check_numbers.py $files && python tools/quarto_build.py && python -m unittest discover -s tests -v
code=$?
echo "VERIFY EXIT=$code seconds=$(( $(date +%s) - start ))"
