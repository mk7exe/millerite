'''
This code makes atoms.json file for all structures in the vasp_folder. atoms.json contains a list of list of atoms in
the POSCAR file. Each element, atom, is a list as:
atom = [id, [x, y, z], [type, b1, b2, b3, b4], bcode, [q4, q6]]
'''

import os
from pathlib import Path
from Phase2.Bond_code import utils

address = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/VASP_folder')

for dir in os.listdir(address):
    print(dir)
    poscar = address / dir / "POSCAR"
    atom_file = address / dir / "atoms.json"
    atoms, cell = utils.read_poscar(poscar)
    atoms = utils.CN(atoms, cell)
    atoms = utils.steinhardt(atoms, cell, 2.55, [4, 6, 8, 10])
    utils.write_to_json(atom_file, atoms)
