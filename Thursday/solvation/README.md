### Prerequisites

This calculation requires `conda -c conda-forge install pandas matplotlib numpy pymbar alchemlyb`


### Calculations

There are 12 intermediate states defined to perform the
calculation of the solvation of ethanol.  You will need to run 12
different simulations.  The will use the SAME .gro file, the SAME
.top file, and nine different .mdp files.  But the .mdp files will
only be different by one line,

init_fep state = X

Where X is 0 through 11, inclusive, because there are 12 states.

Run grompp and mdrun as normal.  Specifically:

There may be some warnings, and you'll need to override, hence -maxwarn.  X runs from 0 to 8.

grompp -f outputs/ethanol.X.mdp -c ethanol.gro -p ethanol.top -o outputs/ethanol.X.tpr -p $top -o $tpr -maxwarn 10 

The number of threads can be anything you want (less than the number
run on the cluster) If running on the cluster, you will also want to
set the -nopin flag.  If you don't set the dhdl file independently,
it will be saved to ethanol.X.xvg, and might get written over
accidentally if you run g_energy.  X again runs 0-8

mdrun -nt 1 -deffnm outputs/ethanol.X -dhdl outputs/ethanol.X.dhdl.xvg

Strictly, you will only need the dhdl files, but looking at the others output files can be useful to identify problems.

After you have generated the dhdl files, you can then analyze them using analyze.py

python analyze.py

It will use all files it finds with the given prefix, and it will assume they are numbered in order.  Equilibration detection is performed.

