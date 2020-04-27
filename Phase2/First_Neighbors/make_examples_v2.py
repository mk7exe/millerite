'''
In this version datasets are built from csv and dat files containing struc_lists and energies, respectively. In v1,
datasets are built by reading POSCAR and OZICARS directly.
'''

import h5py
from pathlib import Path
from Phase2.First_Neighbors.utils_v2 import *

strust_type_file = Path("Z:/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/struct_type.dat")
struct_types = read_struct_type(strust_type_file)

struct_list_files_1 = Path("Z:/Simulations/VASP/Millerite/Machine_Learning/DataSet/Big_Training/struct_list.csv")
struct_list_files_2 = Path("Z:/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/struct_list.csv")
struct_list = read_csv(struct_list_files_1) + read_csv(struct_list_files_2)

eng_file_1 = Path("Z:/Simulations/VASP/Millerite/Machine_Learning/DataSet/Big_Training/energies.dat")
eng_file_2 = Path("Z:/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/energies.dat")

x = []
y = []
x_slab = []
y_slab = []

with open(eng_file_1, 'r') as f:
    for line in f:
        temp = line.split()
        id = int(temp[0])
        eng = float(temp[5])
        x.append(struct_list[id-1])
        y.append(eng)
        if struct_types[id-1] == 2:
            x_slab.append(struct_list[id - 1])
            y_slab.append(eng)

with open(eng_file_2, 'r') as f:
    for line in f:
        temp = line.split()
        id = int(temp[0])
        eng = float(temp[5])
        x.append(struct_list[id-1])
        y.append(eng)
        if struct_types[id-1] == 2:
            x_slab.append(struct_list[id - 1])
            y_slab.append(eng)

print(len(y))
print(len(y_slab))

dataset_file = Path("C:\GitHub_Projects\millerite\Phase2\datasets")
train_file = dataset_file / "train.h5"
slab_file = dataset_file / "slab.h5"

print(train_file)
h5f = h5py.File(train_file, 'w')
h5f.create_dataset('train_set_x', data=x)
h5f.create_dataset('train_set_y', data=y)
h5f.close()

print(slab_file)
h5f = h5py.File(slab_file, 'w')
h5f.create_dataset('slab_x', data=x_slab)
h5f.create_dataset('slab_y', data=y_slab)
h5f.close()
