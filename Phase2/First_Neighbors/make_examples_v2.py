'''
In this version datasets are built from csv and dat files containing struc_lists and energies, respectively. In v1,
datasets are built by reading POSCAR and OZICARS directly.
'''

import h5py
from pathlib import Path
from Phase2.First_Neighbors.utils_v2 import *

#Energy per NiS in Millerite unitcell
eng_NiS = float(-93.110682/9)

sim_folder_old = Path("Z:/Simulations/VASP/Millerite/Machine_Learning/DataSet/Big_Training")
sim_folder_new = Path("Z:/Simulations/VASP/Millerite/Machine_Learning/new-training-builder")

strust_type_file =  sim_folder_new / "struct_type.dat"
struct_types = read_struct_type(strust_type_file)

struct_list_files_1 = sim_folder_old / "struct_list.csv"
struct_list_files_2 = sim_folder_new / "struct_list.csv"
struct_list = read_csv(struct_list_files_1) + read_csv(struct_list_files_2)

eng_file_1 = sim_folder_old / "energies.dat"
eng_file_2 = sim_folder_new / "energies.dat"

dataset_folder = Path("C:\GitHub_Projects\millerite\Phase2\datasets")

x = []
y = []
x_slab = []
y_slab = []

old_dataset_file = dataset_folder / "training_dataset.h5"
old_dataset = h5py.File(old_dataset_file, "r")
x_temp = list(old_dataset["train_set_x"][:].T)
x = [list(elm) for elm in x_temp]
y = list(old_dataset["train_set_y"][:])

# print(len(y))
# print(len(y_slab))

with open(eng_file_2, 'r') as f:
    for line in f:
        temp = line.split()
        id = int(temp[0])
        print(id)
        # print(temp[0], id)
        eng = float(temp[5])
        poscar = sim_folder_new / "VASP_folder" / str(id) / "POSCAR"
        num = read_atom_num(poscar)
        # atom_num = sim_folder_new / "atom_nums.dat"
        # with open(atom_num, 'a') as f1:
        #     f1.write(str(num))
        #     f1.write("\n")
        eng_bar = eng - eng_NiS * num

        x.append(struct_list[id-1])
        y.append(eng_bar)
        if struct_types[id-1] == 2:
            x_slab.append(struct_list[id - 1])
            y_slab.append(eng_bar)

print(len(y))
print(len(y_slab))

train_file = dataset_folder / "train.h5"
slab_file = dataset_folder / "slab.h5"

h5f = h5py.File(train_file, 'w')
h5f.create_dataset('train_set_x', data=x)
h5f.create_dataset('train_set_y', data=y)
h5f.close()

h5f = h5py.File(slab_file, 'w')
h5f.create_dataset('slab_x', data=x_slab)
h5f.create_dataset('slab_y', data=y_slab)
h5f.close()
