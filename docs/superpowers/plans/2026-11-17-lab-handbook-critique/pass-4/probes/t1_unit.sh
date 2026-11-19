# T1's own verify (plan line 82), with the full Verify's exports.
. "$(dirname "$0")/env.sh"
start=$(date +%s)
python -m unittest tests.test_check_unchanged tests.test_check_numbers tests.test_question_ids tests.test_downloads.MediaDownloads -v
echo "UNIT EXIT $? after $(( $(date +%s) - start )) s"
