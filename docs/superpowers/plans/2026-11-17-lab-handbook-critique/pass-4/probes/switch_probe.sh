# D-0198 (3): flip one converted file's status and see the pin fail; then
# a ruled-change file with an em dash in a front-matter comment.
. "$(dirname "$0")/env.sh"
f=curriculum/ph211/ph211-team-building-handout.md
sed -i 's/^status: converted$/status: ruled-change/' "$f"
python tools/check_unchanged.py "$f"
python -m unittest tests.test_check_unchanged.Rebaselined.test_rebaselined_files_are_pinned 2>&1 | grep -E "^(OK|FAILED)|Items in"
git checkout -q -- "$f"
