import numpy as np
import os
import h5py
import json
from pathlib import Path

from collections import Counter
import matplotlib.pyplot as plt

def read_data(address, struct_num, wrongs):
    b1stNN = []
    b2ndNN = []
    counter = 0
    for dir_path in os.listdir(address):
        counter += 1
        if counter % 10 == 0:
            print("number of structures read: %d" % counter, end="\n")
        if counter > struct_num and struct_num > 0:
            break
        # poscar = address / dir_path / "POSCAR"
        # oszicar = address / dir_path / "OSZICAR"
        atom_file = address / dir_path / "atoms.json"

        with open(atom_file) as f:
            atoms = json.load(f)
        # atoms, cell = utils.read_poscar(poscar)
        # atoms = utils.CN(atoms, cell)
        # utils.write_to_json(atom_file, atoms)
        # atoms = utils.steinhardt(atoms, cell, 2.55, [4, 6])

        flag = 0
        for id, atom in enumerate(atoms):
            # if atom[3] != 132 and atom[3] != 53:
            b1stNN.append(atom[3])
            temp = [atom[3]]
            for nn in atom[4]:
                temp.append(atoms[nn][3])
            b2ndNN.append(temp)
            if (any(x > 2 for x in atom[2]) or atom[2][1] > 1) and flag == 0:
                wrongs.append(dir_path)
                flag = 1
            # q4s.append(atom[4])
            # q6s.append(atom[5])
            # if (atom[3] == 0):
            #     f.write('{} {}\n'.format(id, counter))

        # nis_num = len(atoms)/2
        # code = utils.struc_code(atoms)
        # xlist.append(code)

    #     eng = utils.read_oszicar(oszicar)
    #     eng_bar = eng/nis_num - eng_NiS
    #     ylist.append(eng_bar)
    # x = np.array(xlist).T
    # y = np.array(ylist)
    # f.close()

    return b1stNN, b2ndNN, wrongs

train_folder = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/VASP_folder/')
# train_folder = Path('C:\GitHub_Projects\millerite\Phase1\VASP_files\9')
print("reading vasp files to build the training set ...")
wrongs = []
b1stNN, b2ndNN, wrongs = read_data(train_folder, -1, wrongs)

print(wrongs)
b1stNN.sort()

# for i in range(len(bcodes)):
#     if bcodes[i] == 0:
#         print(bcodes[i], bonds[i])

unique_b1ndNN = list(Counter(b1stNN).keys()) # equals to list(set(words))
freqs = list(Counter(b1stNN).values()) # counts the elements' frequency

unique_b2ndNN = [list(x) for x in set(tuple(x) for x in b2ndNN)]

# Output list initialization
Output = {}

# Using Iteration
for lis in b2ndNN:
    Output.setdefault(tuple(lis), list()).append(1)
for a, b in Output.items():
    Output[a] = sum(b)

# q4_codes = list(Counter(q4s).keys()) # equals to list(set(words))
# q4_freqs = list(Counter(q4s).values()) # counts the elements' frequency
#
# q6_codes = list(Counter(q6s).keys()) # equals to list(set(words))
# q6_freqs = list(Counter(q6s).values()) # counts the elements' frequency

# codes = [int(i) for i in codes]
# freqs = [int(i) for i in freqs]

print(len(unique_b1ndNN))
print(len(unique_b2ndNN))
#print(codes)
# print(len(q4_codes))
#print(q4_codes)
# print(len(q6_codes))
#print(q6_codes)
plt.bar(unique_b1ndNN, freqs)
plt.show()