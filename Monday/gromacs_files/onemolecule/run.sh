#!/bin/sh
#export GROMACSHOME="/Users/mrshirts/work/gromacs_allv/gromacs_2025/install/bin"
module load gromacs
export MDRUN="gmx mdrun -nt 1"
export GROMPP="gmx grompp"
export GENERGY="gmx energy"
export NAME="benzene"
$GROMPP -f onemolecule.mdp -c justonebenzene.gro -p onebenzene.top -o ${NAME}.tpr -maxwarn 100
$MDRUN -deffnm ${NAME}
