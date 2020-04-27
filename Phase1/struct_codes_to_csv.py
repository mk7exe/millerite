import os
from pathlib import Path
import csv
from Phase1 import utils

def read_data(address, struct_num):
    xlist = []
    ylist = []
    counter = 0
    for dir in os.listdir(address):
        counter += 1
        if counter % 10 == 0:
            print("number of structures read: %d" % counter, end="\n")
        if counter > struct_num and struct_num > 0:
            break
        print("Structure ", counter, " is ", dir)
        poscar = address / dir / "POSCAR"
        oszicar = address / dir / "OSZICAR"

        atoms, cell = utils.read_poscar(poscar)
        atoms = utils.CN(atoms, cell)
        code = utils.struc_code(atoms)
        xlist.append(code)

    return xlist

print("reading vasp files to build the struct code file ...")
folder = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/VASP_folder')
struct_list = read_data(folder, -1)
struct_file = '/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/struct_list.csv'

with open(struct_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(struct_list)