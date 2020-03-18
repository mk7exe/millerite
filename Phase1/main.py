########################################################################################################################
# This code build the initial data set for machine learning method for calculating the excess energy of Millerite
# structures with free surfaces. Each S atom in Millerite bonded to 5 Ni atoms through 3 different bond types. Bond 1
# , bond 2, and bond 3 are 2.263, 2.264, 2.369 angstroms, respectively. Ni atoms are also bonded to two adjacent Ni
# neighbors with two 2.529 angstrom bonds. The number of these four bonds are identified by b1, b2, b3, b4 in this
# code. Accordingly, each ion in Millerite can be identified by a code as
# b = [type, b1, b2, b3, b4].
# type = 0 (Ni) or 1 (S)
# b1 = 0 or 1
# b2 and b3 = 0, 1 or 2
# b4 = 0 for S and 0, 1, or 2 for Ni
# A single unique code, bcode, which is the representation of b in base 3 is sufficient to identify each atom type
# This code reads a configuration of a nanocluster built in materials studio (xsd file). The nanocluster is not charge
# neutral necessarily. The code finds undercoordinated (UC) ions and removes excess ions to retain charge neutrality.
# This will be done on all xsd files and since there is not a unique way of making charge neutral cluster, the code will
# make more structures for VASP energy calculations compared to the initial sxd files numbers.

import os
from pathlib import Path
import collections
import itertools
import random
import re
import shutil
import numpy as np
import matplotlib.pyplot as plt

match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
pwd = Path.cwd()
xsd_folder = pwd / "xsd_files"  # the folder that contains xsd files
vasp_folder = pwd / "VASP_files"  # the folder in which VASp files should be saved.
if vasp_folder.exists():
    shutil.rmtree(vasp_folder)
os.mkdir(vasp_folder)

# all possible undercoordinate bond codes
UCCodes = [7, 8, 14, 20, 26, 27, 33, 34, 35, 39, 40, 41, 44, 45, 46, 47, 50, 51, 52, 87, 93, 99, 105, 108, 114, 120,
           123, 126, 129]

#lower and higher limit of bond length in Millerite unitcell to find bond types of ions
MilBonds = [2.255, 2.3]

def toDigits(n, b):
    """Convert a positive number n to its digit representation in base b."""
    digits = []
    for i in range(5):
        digits.insert(0, n % b)
        n = n // b
    return digits

def fromDigits(digits, b):
    """Compute the number given by digits in base b."""
    n = 0
    for d in digits:
        n = b * n + d
    return n

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

def struc_code(atoms):
    """function returns a list for an structure including number of each types in UCCodes"""
    all_bcodes = []
    struct_code = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for at in atoms:
        if at[3] != 132 and at[3] != 53:
            all_bcodes.append(at[3])
    bcodes = list(collections.Counter(all_bcodes).keys())
    bnums = list(collections.Counter(all_bcodes).values())
    for j in range(len(bcodes)):
        try:
            index = UCCodes.index(bcodes[j])
        except ValueError:
            index = -1
        if index >= 0:
            struct_code[index] = bnums[j]
    return list(struct_code)

def struc_one_code(struct_code):
    new_list = [x+1 for x in struct_code]
    one_code = ''.join(map(str,new_list))
    return one_code

def duplicate(one_code):
    compare = False
    with open("temp", "r") as f:
        for line in f:
            if line == one_code:
                compare = True
    return compare

def write_vasp(filename, name, num, atoms, cell, neut_code):
    """function to write VASP POSCAR file for a configuration"""
    atoms.sort(key=lambda x: x[2][0])  # Sort to write Ni atoms first
    directory = vasp_folder / str(name)
    os.mkdir(directory)
    file = directory / 'POSCAR'
    with open(file, "w") as f:
        f.write("Structure %d made from %s file\n" % (num, filename))
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
    file = directory / 'STRUCT_CODE'
    with open(file, "w") as f:
        for item in neut_code:
            f.write("%d\n" % item)

def CN(atoms, h):
    """calculates b = [type, b1, b2, b3, b4] for each atom in atoms"""
    for i in range(len(atoms)):
        si = np.asarray(atoms[i][1])
        for j in range(i + 1, len(atoms)):
            sj = np.asarray(atoms[j][1])
            # xsd files contain fractional coordinates. This will calculate shortest distance considering PBC
            sij = si - sj - np.rint(si - sj)
            rij = np.matmul(sij, h)  # converting to cartesian coordinates
            rij_norm = np.linalg.norm(rij)  # length of distance vector
            if rij_norm < 2.55:  # if bonded atoms are same type, it is b4!
                if atoms[i][2][0] == atoms[j][2][0]:
                    atoms[i][2][4] += 1
                    atoms[j][2][4] += 1
                else:
                    if rij_norm < MilBonds[0]:
                        atoms[i][2][1] += 1
                        atoms[j][2][1] += 1
                    elif rij_norm > MilBonds[1]:
                        atoms[i][2][3] += 1
                        atoms[j][2][3] += 1
                    else:
                        atoms[i][2][2] += 1
                        atoms[j][2][2] += 1
        atoms[i][3] = fromDigits(atoms[i][2], 3)  # get bcode from b
    return atoms

def neutralizer(atoms, cell, struct_list, file):
    struct_num = 0
    max_trials = 1000 # number of trials
    max_structuress = 10  # number of trials
    Num = [0, 0]  # number of Ni and S in structure
    remove_ids = []  # id of all undercoordinated atoms of type_to_remove
    remove_bcodes = [] # bcodes of all uandercoordinated atoms of type_to_remove
    Num[1] = sum(at[2][0] for at in atoms)  # S ids are 1
    Num[0] = len(atoms) - Num[1]
    remove_num = np.abs(Num[1] - Num[0])  # number of atoms to be remove to retain charge neutrality

    if remove_num != 0:
        if Num[1] > Num[0]:
            type_to_remove = 1 # S should be removed
            print(remove_num, "S atoms will be removed from", end=" ")
        else:
            type_to_remove = 0 # Ni should be removed
            print(remove_num, "Ni atoms will be removed from", end=" ")
        i = 0
        for at in atoms:
            if at[2][0] == type_to_remove and at[3] != 132 and at[3] != 53:
                remove_ids.append([at[0], at[3]]) # all undercoordinate atom of type_to_remove are candidates
                remove_bcodes.append(at[3]) # store their bcodes
                i += 1
        print(i, "undercoordinated atoms")
        remove_bcodes_set = list(set(remove_bcodes)) # unique bcodes in removal candidates
        remove_ids_sorted = sorted(remove_ids, key = lambda x: x[1])
        # removed ids are grouped according to their bcodes
        remove_ids_grouped = [[key, [g[0] for g in group]] for key, group in itertools.groupby(remove_ids_sorted,
                                                                                                lambda x: x[1])]
        structures = 1
        trial = 0
        while trial <= max_trials and structures <= max_structuress:
            trial += 1
            rm_ids = []
            i = ['']*remove_num
            """select remove_num elements from remove_bcodes_set randomly. There are bcodes removed atoms will be
            selected from. If we select atoms to remove directly, the choice will be biased towards bcodes with large
            numbers"""
            flag = 1
            while flag == 1:
                flag = 0
                for ii in range(remove_num):
                    i[ii] = random.choice(remove_bcodes_set)
                # the number of bcode in i should be smaller than remove_bcodes
                for elem in i:
                    if i.count(elem) > remove_bcodes.count(elem):
                        flag = 1
            for b in remove_bcodes_set:
                n = i.count(b)
                if n > 0:
                    for sub_list in remove_ids_grouped:
                        if b == sub_list[0]:
                            temp = random.sample(sub_list[1], n)
                            rm_ids.append(temp)
            flat_list = [item for sublist in rm_ids for item in sublist]
            neut_atoms = [x for x in atoms if x[0] not in flat_list]
            neut_code = struc_code(neut_atoms)
            one_code = struc_one_code(neut_code)
            if any(elem == neut_code for elem in struct_list):
                pass
            else:
                struct_list.append(neut_code)
                struct_num += 1
                #print(len(struct_list), "structure have been built...", end="\r")
                #print(struct_num, ": ", neut_code)
                write_vasp(file, len(struct_list), struct_num, neut_atoms, cell, neut_code)
                structures += 1
    else:
        neut_code = struc_code(atoms)
        if any(elem == neut_code for elem in struct_list):
            pass
        else:
            struct_list.append(neut_code)
            struct_num += 1
            #print(struct_num, ": ", neut_code)
            write_vasp(file, len(struct_list), struct_num, atoms, cell, neut_code)
    return struct_list

struct_list = []
for file in os.listdir(xsd_folder):
    if file.endswith(".xsd"):
        print("Processing ", file, "...")
        atoms = None
        h = None
        filename = xsd_folder / file
        [atoms, cell] = read_xsd(filename)
        atoms = CN(atoms, cell)
        old_struct_num = len(struct_list)
        struct_list = neutralizer(atoms, cell, struct_list, file)
        new_struct_num = len(struct_list)
        print(new_struct_num - old_struct_num, "new structures were made...")
        print("Current total number of structures: ", new_struct_num)
s1 = [sum(i) for i in zip(*struct_list)]
s2 = sum(s1)
s3 = [i*100 / s2 for i in s1]
print("Final bonds distribution: ")
x = np.arange(len(s3))
plt.bar(x, s3)
plt.show()



