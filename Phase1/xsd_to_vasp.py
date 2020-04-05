import os
from pathlib import Path
import numpy as np
import re
import shutil


match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
pwd = Path.cwd()
xsd_folder = pwd / "surface_xsds"  # the folder that contains xsd files
vasp_folder = pwd / "VASP_files"  # the folder in which VASp files should be saved.
if vasp_folder.exists():
    shutil.rmtree(vasp_folder)
os.mkdir(vasp_folder)

def read_xsd(filename):
    atoms = []
    cell = []
    process = False
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith('<IdentityMapping'):
                process = True
            elif line.startswith('</IdentityMapping>'):
                process = False
            if process:
                temp = line.split(" ")
                if line.startswith('<Atom3d'):
                    for item in temp:
                        if item.startswith('ID'):
                            temp_id = [int(s) for s in re.findall(r'\d+', item)]
                        if item.startswith('XYZ'):
                            temp_xyz = [float(s) for s in re.findall(match_number, item)]
                        if item.startswith('Components'):
                            temp_name = re.findall(r'"([^"]*)"', item)
                            if temp_name[0] == 'Ni':
                                temp_type = 0
                            else:
                                temp_type = 1
                            tempb = [temp_type, 0, 0, 0, 0]
                    atoms.append([temp_id, temp_xyz, tempb, 0])
                elif line.startswith('<SpaceGroup'):
                    for item in temp:
                        if item.startswith('AVector'):
                            a = [float(s) for s in re.findall(match_number, item)]
                        elif item.startswith('BVector'):
                            b = [float(s) for s in re.findall(match_number, item)]
                        if item.startswith('CVector'):
                            c = [float(s) for s in re.findall(match_number, item)]
                    cell = np.asarray([a, b, c])
    return [atoms, cell]

def write_vasp(filename, num, atoms, cell):
    """function to write VASP POSCAR file for a configuration"""
    atoms.sort(key=lambda x: x[2][0])  # Sort to write Ni atoms first
    directory = vasp_folder / str(num)
    os.mkdir(directory)
    file = directory / 'POSCAR'
    with open(file, "w") as f:
        f.write("VASP POSCAR made from %s file\n" % (filename))
        f.write("1.0\n")
        f.write("%20.10f%20.10f%20.10f\n" % (cell[0][0], cell[0][1], cell[0][2]))
        f.write("%20.10f%20.10f%20.10f\n" % (cell[1][0], cell[1][1], cell[1][2]))
        f.write("%20.10f%20.10f%20.10f\n" % (cell[2][0], cell[2][1], cell[2][2]))
        Ni_num = sum(x[2][0] == 0 for x in atoms)
        S_num = len(atoms) - Ni_num
        f.write("   Ni    S\n")
        f.write("%5i%5i\n" % (Ni_num, S_num))
        f.write("Direct\n")
        for a in atoms:
            f.write("%16.9f%16.9f%16.9f\n" % (a[1][0], a[1][1], a[1][2]))

num = 0
for file in os.listdir(xsd_folder):
    if file.endswith(".xsd"):
        print("Processing ", file, "...")
        atoms = None
        h = None
        num += 1
        filename = xsd_folder / file
        [atoms, cell] = read_xsd(filename)
        write_vasp(file, num, atoms, cell)

