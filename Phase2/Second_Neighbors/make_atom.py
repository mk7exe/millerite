'''
This code makes atoms.json file for all structures in the vasp_folder. atoms.json contains a list of list of atoms in
the POSCAR file. Each element, atom, is a list as:
atom = [id, [x, y, z], [type, b1, b2, b3, b4], bcode, [q4, q6]]
'''

import os
import json
from pathlib import Path
from Phase2.First_Neighbors import utils

