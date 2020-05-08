from Phase2.Bond_code import utils
from pathlib import Path
import dpdata

# atoms, cell = utils.read_xsd('Millerite-Rlx.xsd')
# atoms = utils.CN(atoms, cell)
# atoms = utils.steinhardt(atoms, cell, 2.55, [4, 6, 8, 10])
# utils.write_lammps(Path('./'), atoms, cell)

d_poscar = dpdata.System('POSCAR', fmt = 'vasp/poscar')
d_poscar.to('lammps/lmp', 'conf.lmp', frame_idx=0)

d_lmp = dpdata.System('conf.lmp', fmt = 'lammps/lmp')
d_lmp.to('vasp/poscar', 'poscar1', frame_idx=0)
# print(atoms)

