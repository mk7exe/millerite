import os
from pathlib import Path
import numpy as np
import re
import shutil
from Phase2.Bond_code.utils import *

pwd = Path.cwd()
xsd_folder = pwd / "surface_xsds" # the folder that contains xsd files
vasp_folder = pwd / "VASP_files"  # the folder in which VASp files should be saved.
if vasp_folder.exists():
    shutil.rmtree(vasp_folder)
os.mkdir(vasp_folder)

num = 0
for file in os.listdir(xsd_folder):
    if file.endswith(".xsd"):
        print("Processing ", file, "...")
        atoms = None
        h = None
        num += 1
        filename = xsd_folder / file
        [atoms, cell] = read_xsd(filename)
        temp = vasp_folder / str(file)
        os.mkdir(temp)
        write_poscar_v2(temp, file, atoms, cell, False)

