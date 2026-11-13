# run_mutants.sh WORKTREE SCRATCH: pass 2's four mutants of the built .docx
# files (mutate_pass2.py), each against tests.test_downloads.MarkdownAndWord;
# backs up the build first and restores it after, checking the hashes.
W="$1"; S="$2"
ROOT="$W/build/quarto-site"
BAK="$S/mutant-bak"
cd "$W" || exit 1
"$PY" -X utf8 "$S/probes/mutate_pass2.py" backup "$ROOT" "$BAK"
before=$(cat "$ROOT"/labs/*/*.docx | sha256sum)
for m in space_after no_spacing indent bdr_space; do
  "$PY" -X utf8 "$S/probes/mutate_pass2.py" "$m" "$ROOT" "$BAK"
  echo "== $m: $("$PY" -m unittest tests.test_downloads.MarkdownAndWord 2>&1 | tail -1)"
  "$PY" -m unittest tests.test_downloads.MarkdownAndWord 2>&1 | grep -E "^(FAIL|ERROR):" | sed 's/ (tests[^)]*)//' | sort | uniq -c
done
"$PY" -X utf8 "$S/probes/mutate_pass2.py" restore "$ROOT" "$BAK"
after=$(cat "$ROOT"/labs/*/*.docx | sha256sum)
[ "$before" = "$after" ] && echo "restored: hashes equal" || echo "RESTORE MISMATCH"
