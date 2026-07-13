#!/bin/sh
export GROMACSHOME="/Users/mrshirts/work/gromacs_allv/gromacs_2025/install/bin"
export MDRUN="${GROMACSHOME}/gmx mdrun -nt 1"
export GROMPP="${GROMACSHOME}/gmx grompp"
export GENERGY="${GROMACSHOME}/gmx energy"
export NAME="benzene"
$GROMPP -f onemolecule.mdp -c justonebenzene.gro -p onebenzene.top -o ${NAME}.tpr -maxwarn 100
$MDRUN -deffnm ${NAME}
