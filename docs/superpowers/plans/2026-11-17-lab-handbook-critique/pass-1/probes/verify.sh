#!/bin/bash
# The plan's full Verify, verbatim, run from the scratch tree's root.
cd "$1" || exit 2
export QUARTO="/c/Program Files/Quarto/bin/quarto.exe"
export PANDOC="/c/Program Files/Quarto/bin/tools/pandoc.exe"
export CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
export PDFTOTEXT="$LOCALAPPDATA/Microsoft/WinGet/Packages/oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe/poppler-25.07.0/Library/bin/pdftotext.exe"
export PYTHONWARNINGS=ignore::ResourceWarning PYTHONUTF8=1
files=$(for f in $(git ls-files '*.md'); do [ "$(head -1 "$f")" = "---" ] && sed -n '2,/^---$/p' "$f" | grep -q '^source_file:' && echo "$f"; done)
date
python tools/check_em_dash.py && echo EMDASH_OK && python tools/check_unchanged.py $files && echo WORDS_OK && python tools/check_numbers.py $files && echo NUMBERS_OK && python tools/quarto_build.py > "$2.build.log" 2>&1 && echo BUILD_OK && python -m unittest discover -s tests -v > "$2.tests.log" 2>&1 && echo TESTS_OK
echo "exit $?"
date
