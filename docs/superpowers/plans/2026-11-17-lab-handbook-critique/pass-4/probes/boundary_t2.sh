# The full Verify at T2's boundary, the build skipped because it was made
# from this exact tree a moment before (the plan runs only T2's narrower
# verify here). Run from the scratch tree's root: bash boundary_t2.sh
. "$(dirname "$0")/env.sh"
start=$(date +%s)
files=$(for f in $(git ls-files '*.md'); do [ "$(head -1 "$f")" = "---" ] && sed -n '2,/^---$/p' "$f" | grep -q '^source_file:' && echo "$f"; done)
python tools/check_em_dash.py && python tools/check_unchanged.py $files && python tools/check_numbers.py $files && python -m unittest discover -s tests -v
echo "BOUNDARY EXIT $? after $(( $(date +%s) - start )) s"
