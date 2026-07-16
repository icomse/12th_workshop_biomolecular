import subprocess
gmx = "/Users/mrshirts/work/gromacs_allv/gromacs_2025/install/bin/gmx"
genergy = "energy"
grompp = "grompp"
nstates = 12

name = "ethanol"
gro = f"start_{name}.gro"
top = f"{name}.top"
template = f"{name}_template.mdp"

for i in range(nstates):
    namei = f"{name}.{i}" 
    
    try:
        with open(template, 'r') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading the file: {e}")
        
    new_content = content.replace("REPLACELAMBDA", str(i))
    mdp = f"outputs/{namei}.mdp"
    try:
        with open(mdp, 'w') as output_file:
            output_file.write(new_content)
    except Exception as e:
            print(f"Failed to write {mdp}: {e}")

for i in range(nstates):
    namei = f"{name}.{i}"
    mdp = f"outputs/{namei}.mdp"    
    gro = f"start_{name}.gro"
    top = f"{name}.top"
    dhdl = f"outputs/{namei}.dhdl.xvg"
    tpr = f"outputs/{namei}.tpr"
    mdrun = f"{gmx} grompp -f {mdp} -c {gro} -p {top} -o {tpr} -maxwarn 10";
    subprocess.run(mdrun,shell=True)
    grompp = f"{gmx} mdrun -nt 4 -deffnm outputs/{namei} -dhdl {dhdl}"
    subprocess.run(grompp,shell=True)
    subprocess.run("sleep 1",shell=True);
