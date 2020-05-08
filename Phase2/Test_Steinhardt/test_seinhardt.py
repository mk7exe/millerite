from Phase2.Bond_code import utils
from pathlib import Path

atoms, cell = utils.read_xsd('Millerite-Rlx.xsd')
atoms = utils.CN(atoms, cell)
atoms = utils.steinhardt(atoms, cell, 2.55, [4, 6, 8, 10])
utils.write_lammps(Path('./'), atoms, cell)
print(atoms)

