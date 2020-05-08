import collections
import itertools
import random
import re
import numpy as np
from scipy import special
import os
import csv
import json

match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')

# all possible undercoordinate bond codes when considering first neighbors
UCCodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30,
           31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 81, 84, 87, 90,
           93, 96, 99, 102, 105, 108, 111, 114, 117, 120, 123, 126, 129]


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


def read_struct_list(filename):
    with open(filename, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Pass reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)
        list_int = [list(map(int, x)) for x in list_of_rows]
    return list_int


def write_struct_list(filename, code):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(code)


def write_to_csv(filename, code):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(code)


def write_to_json(filename, code):
    with open(filename, "w") as f:
        f.write(json.dumps(code))


def read_oszicar(filename):
    with open(filename) as f:
        for line in f:
            pass
    temp = line.split(" ")
    eng = float(temp[5])
    return eng


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
                atoms.append([counter - 8, temp_xyz, tempb, 0, [], []])
    cell = np.asarray([a, b, c])

    return atoms, cell


def write_poscar_v2(address, atoms, cell, constraint):
    """function to write VASP POSCAR file for a configuration"""
    atoms.sort(key=lambda x: x[2][0])  # Sort to write Ni atoms first
    file = address / 'POSCAR'
    with open(file, "w") as f:
        f.write("Structure made with write_poscar_v2\n")
        f.write("1.0\n")
        f.write("%20.10f%20.10f%20.10f\n" % (cell[0][0], cell[0][1], cell[0][2]))
        f.write("%20.10f%20.10f%20.10f\n" % (cell[1][0], cell[1][1], cell[1][2]))
        f.write("%20.10f%20.10f%20.10f\n" % (cell[2][0], cell[2][1], cell[2][2]))
        Ni_num = sum(x[2][0] == 0 for x in atoms)
        S_num = len(atoms) - Ni_num
        f.write("   Ni    S\n")
        f.write("%5i%5i\n" % (Ni_num, S_num))
        if constraint:
            f.write("Selective Dynamics\n")
        f.write("Direct\n")
        for a in atoms:
            if constraint:
                if a[3] != 132 and a[3] != 53:
                    f.write("%16.9f%16.9f%16.9f T T T\n" % (a[1][0], a[1][1], a[1][2]))
                else:
                    f.write("%16.9f%16.9f%16.9f F F F\n" % (a[1][0], a[1][1], a[1][2]))
            else:
                f.write("%16.9f%16.9f%16.9f\n" % (a[1][0], a[1][1], a[1][2]))


def write_poscar(vasp_folder, filename, name, num, atoms, cell, struct_type):
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

    file = directory / struct_type
    with open(file, "w") as f:
        f.write(struct_type)


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
                    temp_xyz = [0.0, 0.0, 0.0]
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
                    atoms.append([temp_id, temp_xyz, tempb, 0, [], []])
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
    code = [0] * len(UCCodes)
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
            code[index] = bnums[j]
    # temp_b = [x for x in code if x]
    # gcd = np.gcd.reduce(temp_b)
    # code = [int(x/gcd) for x in code]
    return list(code)


def struc_one_code(struct_code):
    new_list = [x + 1 for x in struct_code]
    one_code = ''.join(map(str, new_list))
    return one_code


def duplicate(one_code):
    compare = False
    with open("temp", "r") as f:
        for line in f:
            if line == one_code:
                compare = True
    return compare


def CN(atoms, h):
    """calculates b = [type, b1, b2, b3, b4] for each atom in atoms"""
    # image_vector = np.array([p for p in itertools.product([-1, 0, 1], repeat=3)])
    # lower and higher limit of bond length in Millerite unitcell to find bond types of ions
    MilBonds = [2.255, 2.3, 2.55]

    for i in range(len(atoms)):
        atoms[i][2][1] = 0
        atoms[i][2][2] = 0
        atoms[i][2][3] = 0
        atoms[i][2][4] = 0

    for i in range(len(atoms)):
        si = np.asarray(atoms[i][1])
        for j in range(i + 1, len(atoms)):
            sj = np.asarray(atoms[j][1])
            # xsd files contain fractional coordinates. This will calculate shortest distance considering PBC
            sij = si - sj - np.rint(si - sj)
            rij = np.matmul(sij, h)  # converting to cartesian coordinates
            rij_norm = np.linalg.norm(rij)  # length of distance vector
            if rij_norm < MilBonds[2]:  # if bonded atoms are same type, it is b4!
                set1 = set(atoms[i][4])
                set2 = set(atoms[j][4])
                set1.add(j)
                set2.add(i)
                atoms[i][4] = list(set1)
                atoms[j][4] = list(set2)
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


def neutralizer(vasp_folder, atoms, cell, struct_list, file, struct_type, wrongs, bcodes):
    struct_num = 0
    max_trials = 1000  # number of trials
    max_structures = 50  # number of trials
    Num = [0, 0]  # number of Ni and S in structure
    remove_ids = []  # id of all undercoordinated atoms of type_to_remove
    remove_bcodes = []  # bcodes of all uandercoordinated atoms of type_to_remove
    Num[1] = sum(at[2][0] for at in atoms)  # S ids are 1
    Num[0] = len(atoms) - Num[1]
    remove_num = np.abs(Num[1] - Num[0])  # number of atoms to be remove to retain charge neutrality

    if remove_num != 0:
        if Num[1] > Num[0]:
            type_to_remove = 1  # S should be removed
            print(remove_num, "S atoms will be removed from", end=" ")
        else:
            type_to_remove = 0  # Ni should be removed
            print(remove_num, "Ni atoms will be removed from", end=" ")
        i = 0
        for at in atoms:
            if at[2][0] == type_to_remove and at[3] != 132 and at[3] != 53:
                remove_ids.append([at[0], at[3]])  # all undercoordinate atom of type_to_remove are candidates
                remove_bcodes.append(at[3])  # store their bcodes
                i += 1
        print(i, "undercoordinated atoms")
        remove_bcodes_set = list(set(remove_bcodes))  # unique bcodes in removal candidates
        remove_ids_sorted = sorted(remove_ids, key=lambda x: x[1])
        # removed ids are grouped according to their bcodes
        remove_ids_grouped = [[key, [g[0] for g in group]] for key, group in itertools.groupby(remove_ids_sorted,
                                                                                               lambda x: x[1])]
        structures = 1
        trial = 0
        while trial <= max_trials and structures <= max_structures:
            trial += 1
            rm_ids = []
            i = [''] * remove_num
            # """select remove_num elements from remove_bcodes_set randomly. There are bcodes removed atoms will be
            # selected from. If we select atoms to remove directly, the choice will be biased towards bcodes with large
            # numbers"""
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
            neut_atoms = CN(neut_atoms, cell)
            zero_bond = any((x[3] == 0 or x[3] == 81) for x in neut_atoms)
            neut_code = struc_code(neut_atoms)
            if any(elem == neut_code for elem in struct_list) or zero_bond:
                pass
            else:
                flag = 0
                for id, atom in enumerate(neut_atoms):
                    bcodes.add(atom[3])
                    if (any(x > 2 for x in atom[2]) or atom[2][1] > 1) and flag == 0:
                        wrongs.append([file, len(struct_list), struct_type])
                        flag = 1
                        break
                struct_list.append(neut_code)
                struct_num += 1
                write_poscar(vasp_folder, file, len(struct_list), struct_num, neut_atoms, cell, struct_type)
                structures += 1
                path = vasp_folder / str(len(struct_list)) / 'atoms.json'
                write_to_json(path, neut_atoms)
    else:
        neut_code = struc_code(atoms)
        neut_atoms = atoms
        flag = 0
        for id, atom in enumerate(neut_atoms):
            bcodes.add(atom[3])
            if (any(x > 2 for x in atom[2]) or atom[2][1] > 1) and flag == 0:
                wrongs.append([file, len(struct_list), struct_type])
                flag = 1
                break
        if any(elem == neut_code for elem in struct_list):
            pass
        else:
            struct_list.append(neut_code)
            struct_num += 1
            # print(struct_num, ": ", neut_code)
            write_poscar(vasp_folder, file, len(struct_list), struct_num, neut_atoms, cell, struct_type)
            path = vasp_folder / str(len(struct_list)) / 'atoms.json'
            write_to_json(path, neut_atoms)

    return struct_list, neut_atoms, wrongs, bcodes


def steinhardt(atoms, h, rmax, orders):
    max_order = max(orders)
    for i in range(len(atoms)):
        ybar = np.zeros((2 * max_order + 1, len(orders)), dtype=np.cdouble)
        nnn = 0
        si = np.asarray(atoms[i][1])
        for j in range(len(atoms)):
            sj = np.asarray(atoms[j][1])
            # xsd files contain fractional coordinates. This will calculate shortest distance considering PBC
            sij = sj - si - np.rint(sj - si)
            rij = np.matmul(sij, h)  # converting to cartesian coordinates
            rij_norm = np.linalg.norm(rij)  # length of distance vector
            if rij_norm < rmax and i != j:
                nnn += 1
                theta = np.arctan2(rij[1], rij[0])
                theta = np.mod(theta, 2 * np.pi)
                phi = np.arctan2(np.sqrt(rij[0] * rij[0] + rij[1] * rij[1]), rij[2])
                # print(theta, phi)
                counter = 0
                for order in orders:
                    for k in range(2 * order + 1):
                        l = order
                        m = k - order
                        ybar[k, counter] += special.sph_harm(m, l, theta, phi)
                    counter += 1
        ybar = np.divide(ybar, nnn, out=np.zeros_like(ybar), where=nnn != 0)
        for k in range(len(orders)):
            ybar_square = np.square(np.absolute(ybar[:, k]))
            q = np.sqrt((4 * np.pi / (2 * orders[k] + 1)) * np.sum(ybar_square))
            atoms[i][5].append(np.around(q, decimals=3))
    return atoms


def frac2cart(cellParam, i):
    x = i[0] * cellParam[0][0] + i[1] * cellParam[1][0] + i[2] * cellParam[2][0]
    y = i[0] * cellParam[0][1] + i[1] * cellParam[1][1] + i[2] * cellParam[2][1]
    z = i[0] * cellParam[0][2] + i[1] * cellParam[1][2] + i[2] * cellParam[2][2]
    return x, y, z


def write_lammps(address, atoms, h):
    lmp_file = address / 'lmp.data'
    print(h)
    # converting cell vectors
    a = h[0]
    b = h[1]
    c = h[2]
    ax = np.linalg.norm(a)
    bx = np.dot(b, a) / ax
    by = np.sqrt(np.linalg.norm(b) * np.linalg.norm(b) - bx * bx)
    cx = np.dot(c, a) / ax
    cy = np.divide(np.dot(b, c) - bx * cx, by)
    cz = np.sqrt(np.square(np.linalg.norm(c)) - np.square(np.linalg.norm(cx)) - np.square(np.linalg.norm(cy)))

    lmp_h = np.array([[ax, 0, 0], [bx, by, 0], [cx, cy, cz]])

    with open(lmp_file, 'w') as f:
        f.write('lammps data file made by write_lammps function in millerite project\n')
        f.write('\n')
        f.write('  %d atoms\n' % (len(atoms)))
        f.write('\n')
        f.write('  2 atom types\n')
        f.write('\n')
        f.write('%10.8f %10.8f  xlo xhi\n' % (0.0, ax))
        f.write('%10.8f %10.8f  ylo yhi\n' % (0.0, by))
        f.write('%10.8f %10.8f  zlo zhi\n' % (0.0, cz))
        if np.around(bx, decimals=6) != 0.0 or np.around(cx, decimals=6) != 0.0 or np.around(cy, decimals=6) != 0.0:
            f.write('%10.8f %10.8f %10.8f xy xz yz\n' % (bx, cx, cy))
        f.write('\n')
        f.write('  Masses\n')
        f.write('\n')
        f.write('  1  58.6934\n')
        f.write('  2  32.0650\n')
        f.write('\n')
        f.write('Atoms # full\n')
        f.write('\n')
        for i, atom in enumerate(atoms):
            [x, y, z] = np.dot(lmp_h.T, atom[1])
            f.write('%7d %5d %5d %10.6f %10.6f %10.6f %10.6f\n' % (i+1, 1, atom[2][0]+1, 0.0, x, y, z))