#!/bin/bash
# The Quarto build with the Verify's exports, from the tree root.
export QUARTO="/c/Program Files/Quarto/bin/quarto.exe"
export PANDOC="/c/Program Files/Quarto/bin/tools/pandoc.exe"
export CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
start=$(date +%s)
python tools/quarto_build.py
echo "BUILD EXIT=$? seconds=$(( $(date +%s) - start ))"
