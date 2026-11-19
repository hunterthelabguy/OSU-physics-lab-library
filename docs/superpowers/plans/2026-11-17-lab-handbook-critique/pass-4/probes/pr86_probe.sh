# Open PR #86 (D-0184) makes PH 212 Lab 1 a second `ruled-change` file with
# ruled_omissions, ruled_additions and ruled_equations. Apply its handout
# change (only) on top of T1 as written, run what T1 built, then restore.
# Run from the scratch tree's root after T1: bash pr86_probe.sh
. "$(dirname "$0")/env.sh"
GH="/c/Program Files/GitHub CLI/gh.exe"
f=curriculum/ph212/ph212-data-analysis-handout.md
diff=$(mktemp)
"$GH" pr diff 86 > "$diff"
git apply --include="$f" "$diff" && echo "applied #86's change to $f"
sed -n '9,22p' "$f"
echo "--- check_unchanged:"; python tools/check_unchanged.py "$f"
echo "--- check_numbers:"; python tools/check_numbers.py "$f"
echo "--- check_em_dash:"; python tools/check_em_dash.py; echo "exit $?"
echo "--- the pinned set:"
python -m unittest tests.test_check_unchanged.Rebaselined.test_rebaselined_files_are_pinned 2>&1 | grep -E "^(OK|FAILED)|Items in|^\+|^-"
git checkout -q -- "$f"; rm -f "$diff"; git status --short -- curriculum
