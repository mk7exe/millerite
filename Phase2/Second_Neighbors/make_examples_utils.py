import collections
import re
import shutil
import numpy as np

match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')

# all possible undercoordinate bond codes when considering first neighbors
UCCodes = [7, 8, 14, 20, 26, 27, 33, 34, 35, 39, 40, 41, 44, 45, 46, 47, 50, 51, 52, 87, 93, 99, 105, 108, 114, 120,
           123, 126, 129]

# lower and higher limit of bond length in Millerite unitcell to find bond types of ions
MilBonds = [2.255, 2.3]


def todigits(n, b):
    """Convert a positive number n to its digit representation in base b."""
    digits = []
    for i in range(5):
        digits.insert(0, n % b)
        n = n // b
    return digits


def fromdigits(digits, b):
    """Compute the number given by digits in base b."""
    n = 0
    for d in digits:
        n = b * n + d
    return n


def read_poscar(filename):
    atoms = []
    counter = 0
    with open(filename) as f:
        for line in f:
            counter += 1
            if counter == 3:
                a = [float(number) for number in line.split()]
            if counter == 4:
                b = [float(number) for number in line.split()]
            if counter == 5:
                c = [float(number) for number in line.split()]
            if counter == 7:
                num = [int(number) for number in line.split()]
            if counter > 8:
                temp_xyz = [float(number) for number in line.split()]
                if counter <= num[0] + 8:
                    tempb = [0, 0, 0, 0, 0]
                else:
                    tempb = [1, 0, 0, 0, 0]
                atoms.append([counter - 8, temp_xyz, tempb, 0])
    cell = np.asarray([a, b, c])

    return atoms, cell

def read_oszicar(filename):
    with open(filename) as f:
        for line in f:
            pass
    temp = line.split(" ")
    eng = float(temp[5])
    return eng

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
        return atoms, cell


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
        atoms[i][3] = fromdigits(atoms[i][2], 3)  # get bcode from b
    return atoms
