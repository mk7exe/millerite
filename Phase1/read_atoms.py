########################################################################################################################
# This code builds the initial data set for machine learning method for calculating the excess energy of Millerite
# structures with free surfaces. Each S atom in Millerite bonded to 5 Ni atoms through 3 different bond types. Bond 1
# , bond 2, and bond 3 are 2.263, 2.264, 2.369 angstroms, respectively. Ni atoms are also bonded to two adjacent Ni
# neighbors with two 2.529 angstrom bonds. The number of these four bonds are identified by b1, b2, b3, b4 in this
# code. Accordingly, each ion in Millerite can be identified by a code as
# b = [type, b1, b2, b3, b4].
# type = 0 (Ni) or 1 (S)
# b1 = 0 or 1
# b2 and b3 = 0, 1 or 2
# b4 = 0 for S and 0, 1, or 2 for Ni
# A single unique code, bcode, which is the representation of b in base 3 is sufficient to identify each atom type.
# There are 68 unique possibilities for bcode of a uncoordinated atom. The structure code is defined as a 68 element
# list contaning the count of each bcode in the structure.
# This code reads xsd files containg configurations with periodic boundary condition is 0, 1, 2 directions that include
# some undercoordinate atoms. These structures are not necessarily charge neutral. The code finds undercoordinated (UC)
# ions and removes excess ions to regain charge neutrality.
# This will be done on all xsd files and since there is not a unique way of making charge neutral cluster, the code will
# make more structures for VASP energy calculations compared to the initial xsd files numbers. After building each
# structure, its structure code is compared with previous structures to make sure it is not a duplicate.
# The code also can read a list of list of structure codes from a csv file. This list of list gives the structure codes
# of previously built structures that we do not want to duplicate.

import os
from pathlib import Path
import shutil
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

import utils

# the folder in which VASp files should be saved.
vasp_folder = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/VASP_folder')
if vasp_folder.exists():
    shutil.rmtree(vasp_folder)
os.mkdir(vasp_folder)

structure_nums = []
bcodes = set([])
wrongs = []

for file in os.listdir(vasp_folder):

    if file.endswith(".xsd"):
        print("Processing ", file, "...")
        atoms = None
        cell = None
        filename = xsd_folder / xsd_dir / file
        atoms, cell = utils.read_xsd(filename)
        atoms = utils.CN(atoms, cell)
        old_struct_num = len(struct_list)
        struct_list, atoms, wrongs, bcodes = utils.neutralizer(vasp_folder, atoms, cell, struct_list, file,
                                                               folder, wrongs, bcodes)
        new_struct_num = len(struct_list)
        if old_struct_num != new_struct_num:
            path = vasp_folder / str(new_struct_num) / 'atoms.json'
            utils.write_to_json(path, atoms)
        print(new_struct_num - old_struct_num, "new structures were made...")
        print("Current total number of structures: ", new_struct_num)

new_struct_file = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/struct_list.csv')
utils.write_struct_list(new_struct_file, struct_list)

print(wrongs)
codes = sorted(bcodes)

for i in range(len(codes)):
    if codes[i] == 0:
        print(bcodes[i])

# codes = list(Counter(bcodes).keys()) # equals to list(set(words))
# freqs = list(Counter(bcodes).values()) # counts the elements' frequency

print(len(codes))

with open('/home/khalkhal/codes.txt', 'w') as f:
    for item in codes:
        f.write("%5s %15s\n" % (item, str(utils.todigits(item, 3))))
# plt.bar(codes, freqs)
# plt.show()

struct_list = utils.read_struct_list(new_struct_file)
s1 = [sum(x) for x in zip(*struct_list)]
s2 = sum(s1)
s3 = [i*100 / s2 for i in s1]
x = np.arange(len(s3))
plt.bar(x, s3)
plt.show()



