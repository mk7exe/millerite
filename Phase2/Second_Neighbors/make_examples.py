import numpy as np
import os
import h5py
from pathlib import Path
from Second_Neighbors import make_examples_utils as utils

from collections import Counter
import matplotlib.pyplot as plt

#Energy per NiS in Millerite unitcell
eng_NiS = float(-93.110682/9)

def read_data(address, struct_num):
    # xlist = []
    # ylist = []
    bcodes = []
    bs = []
    counter = 0
    f=open('/home/khalkhal/bond_codes.txt','w')

    for dir in os.listdir(address):
        counter += 1
        if counter % 10 == 0:
            print("number of structures read: %d" % counter, end="\n")
        if counter > struct_num and struct_num > 0:
            break
        poscar = address / dir / "POSCAR"
        oszicar = address / dir / "OSZICAR"

        atoms, cell = utils.read_poscar(poscar)
        atoms = utils.CN(atoms, cell)
        ni = 0

        for id, atom in enumerate(atoms):
            bs.append(atom[2])
            bcodes.append(atom[3])
            if (atom[3] == 0):
                f.write('{} {}\n'.format(id, counter))

        # nis_num = len(atoms)/2
        # code = utils.struc_code(atoms)
        # xlist.append(code)

    #     eng = utils.read_oszicar(oszicar)
    #     eng_bar = eng/nis_num - eng_NiS
    #     ylist.append(eng_bar)
    # x = np.array(xlist).T
    # y = np.array(ylist)
    f.close()

    return bs, bcodes

train_folder = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/DataSet/Big_Training/VASP_files')
print("reading vasp files to build the training set ...")
bonds, bcodes = read_data(train_folder, 733)

bcodes.sort()

for i in range(len(bcodes)):
    if bcodes[i] == 0:
        print(bcodes[i], bonds[i])

unique_bcodes = [list(x) for x in set(tuple(x) for x in bonds)]

codes = list(Counter(bcodes).keys()) # equals to list(set(words))
freqs = list(Counter(bcodes).values()) # counts the elements' frequency

# codes = [int(i) for i in codes]
# freqs = [int(i) for i in freqs]

print(len(unique_bcodes))
print(codes)

plt.bar(codes, freqs)
plt.show()