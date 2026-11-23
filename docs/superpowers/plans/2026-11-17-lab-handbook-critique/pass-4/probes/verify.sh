# The plan's full Verify, verbatim (plan block 01, lines 16 to 21), timed.
# Run from the scratch tree's root: bash verify.sh BLOCKS
start=$(date +%s)
. "$1/01.bash"
code=$?
echo "VERIFY EXIT $code after $(( $(date +%s) - start )) s"
