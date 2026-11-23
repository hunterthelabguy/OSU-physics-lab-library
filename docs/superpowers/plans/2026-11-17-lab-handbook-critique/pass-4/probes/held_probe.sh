# HeldToLab7 must fail on a one-word change to the handbook, and on the same
# change made to Lab 7 alone; it passes when both change together.
. "$(dirname "$0")/env.sh"
h=curriculum/ph21x/ph21x-lab-handbook.md; c=curriculum/ph211/ph211-capstone-handout.md
run() { python -m unittest tests.test_lab_handbook.HeldToLab7 2>&1 | grep -E "^(OK|FAILED)"; }
cp $h $h.bak; cp $c $c.bak
sed -i 's/Do not connect the data points/Never connect the data points/' $h; echo -n "handbook only: "; run
cp $h.bak $h; sed -i 's/Do not connect the data points/Never connect the data points/' $c; echo -n "Lab 7 only: "; run
sed -i 's/Do not connect the data points/Never connect the data points/' $h; echo -n "both: "; run
mv $h.bak $h; mv $c.bak $c; git status --short
