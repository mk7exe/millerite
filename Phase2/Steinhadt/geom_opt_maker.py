import os
from pathlib import Path
from Phase2.Bond_code import utils

address = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/VASP_folder')

for dir in os.listdir(address):
    print(dir)
    poscar = address / dir / "POSCAR"
    potcar = address / dir / "POTCAR"
    incar = address / dir / "INCAR"
    kpoints = address / dir / "KPOINTS"

    atoms, cell = utils.read_poscar(poscar)
    atoms = utils.CN(atoms, cell)

    geom_opt_dir = address / dir / "GEOM_OPT"
    if not os.path.isdir(geom_opt_dir):
        os.mkdir(geom_opt_dir)

    cp_command = 'cp ' +  str(incar) + ' ' + str(geom_opt_dir)
    os.system(cp_command)
    cp_command = 'cp ' + str(potcar) + ' ' + str(geom_opt_dir)
    os.system(cp_command)
    cp_command = 'cp ' + str(kpoints) + ' ' + str(geom_opt_dir)
    os.system(cp_command)

    utils.write_poscar_v2(geom_opt_dir, atoms, cell, True)
    incar = geom_opt_dir / "INCAR"
    with open(incar, 'a') as f:
        f.write('# Relaxation\n')
        f.write('NSW = 10\n')
        f.write('IBRION = 2\n')
        f.write('ISIF = 2\n')



