import os
from pathlib import Path
import utils

vasp_folder = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/VASP_folder')
counter = 0
for folder in os.listdir(vasp_folder):
    counter += 1
    if counter % 10 == 0:
        print("number of structures read: %d" % counter, end="\n")
    poscar = vasp_folder / folder / "POSCAR"
    atoms, cell = utils.read_poscar(poscar)
    atoms = utils.CN(atoms, cell)
    atom_file = vasp_folder / folder / "atoms.json"
    utils.write_to_json(atom_file, atoms)