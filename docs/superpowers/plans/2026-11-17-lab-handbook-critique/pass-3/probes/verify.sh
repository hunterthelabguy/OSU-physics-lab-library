# The plan's full Verify, verbatim (plan lines 15 to 20), with timings.
. "$(dirname "$0")/env.sh"
start=$(date +%s)
files=$(for f in $(git ls-files '*.md'); do [ "$(head -1 "$f")" = "---" ] && sed -n '2,/^---$/p' "$f" | grep -q '^source_file:' && echo "$f"; done)
python tools/check_em_dash.py && python tools/check_unchanged.py $files && python tools/check_numbers.py $files && python tools/quarto_build.py && python -m unittest discover -s tests -v
code=$?
echo "VERIFY EXIT $code after $(( $(date +%s) - start )) s"
