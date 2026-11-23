#!/bin/bash
# T2's last verify step, from the tree root: bash t2_step.sh LOG
export QUARTO="/c/Program Files/Quarto/bin/quarto.exe"
export PANDOC="/c/Program Files/Quarto/bin/tools/pandoc.exe"
export CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
export PDFTOTEXT="$LOCALAPPDATA/Microsoft/WinGet/Packages/oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe/poppler-25.07.0/Library/bin/pdftotext.exe"
start=$(date +%s)
python tools/quarto_build.py && python -m unittest tests.test_downloads tests.test_quarto_site
echo "STEP EXIT=$? seconds=$(( $(date +%s) - start ))"
