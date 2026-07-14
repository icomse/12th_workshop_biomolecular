#!/bin/sh
export GROMACSHOME="/Users/mrshirts/work/gromacs_allv/gromacs_2025/install/bin"
export MDRUN="${GROMACSHOME}/gmx mdrun -nt 4"
export GROMPP="${GROMACSHOME}/gmx grompp"
export GENERGY="${GROMACSHOME}/gmx energy"
export NAME="water"
$GROMPP -f nvt.mdp -c startwater.gro -p justwater.top -o ${NAME}.tpr -maxwarn 5
$MDRUN -deffnm ${NAME}
