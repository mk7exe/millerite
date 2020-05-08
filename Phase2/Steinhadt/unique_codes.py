import os
import json
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt

# Bcodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30,
#            31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 81, 84, 87, 90,
#            93, 96, 99, 102, 105, 108, 111, 114, 117, 120, 123, 126, 129, 132]
#
# def read_data(address, struct_num):
#     b1stNN = []
#     b2ndNN = []
#     wrongs = []
#     # bcode_q4 = [[] for i in range(len(Bcodes))]
#     bcode_q6 = [[] for i in range(len(Bcodes))]
#     bcode_q8 = [[] for i in range(len(Bcodes))]
#     bcode_q10 = [[] for i in range(len(Bcodes))]
#
#     counter = 0
#     for dir_path in os.listdir(address):
#         counter += 1
#         if counter % 10 == 0:
#             print("number of structures read: %d" % counter, end="\n")
#         if counter > struct_num and struct_num > 0:
#             break
#         # poscar = address / dir_path / "POSCAR"
#         # oszicar = address / dir_path / "OSZICAR"
#         atom_file = address / dir_path / "atoms.json"
#
#         with open(atom_file) as f:
#             atoms = json.load(f)
#         # atoms, cell = utils.read_poscar(poscar)
#         # atoms = utils.CN(atoms, cell)
#         # utils.write_to_json(atom_file, atoms)
#         # atoms = utils.steinhardt(atoms, cell, 2.55, [4, 6])
#
#         flag = 0
#         for id, atom in enumerate(atoms):
#             # if atom[3] != 132 and atom[3] != 53:
#             b1stNN.append(atom[3])
#             index = Bcodes.index(atom[3])
#             temp = []
#             for nn in atom[5]:
#                 temp.append(nn)
#             # bcode qs #######################
#             # bcode_q4[index].append(atom[5][0])
#             # bcode_q6[index].append(atom[5][1])
#             # bcode_q8[index].append(atom[5][2])
#             # bcode_q10[index].append(atom[5][3])
#             ###################################
#
#             b2ndNN.append(temp)
#             if (any(x > 2 for x in atom[2]) or atom[2][1] > 1) and flag == 0:
#                 wrongs.append(dir_path)
#                 flag = 1
#
#
#     return b1stNN, b2ndNN, wrongs, bcode_q4
#
# train_folder = Path('Z:/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/VASP_folder')
# # train_folder = Path('C:\GitHub_Projects\millerite\Phase1\VASP_files\9')
# print("reading vasp files to build the training set ...")
# b1stNN, b2ndNN, wrongs, bcode_q4 = read_data(train_folder, 50)
#
# q0 = b1stNN
# q4 = [x[0] for x in b2ndNN]
# q6 = [x[1] for x in b2ndNN]
# q8 = [x[2] for x in b2ndNN]
# q10 = [x[3] for x in b2ndNN]

with open("bcodes.txt", "r") as f:
    q0 = json.load(f)
with open("q4.txt", "r") as f:
    q4 = json.load(f)
    q4 = [x for x in q4 if x < 1]
with open("q6.txt", "r") as f:
    q6 = json.load(f)
    q6 = [x for x in q6 if x < 1]
with open("q8.txt", "r") as f:
    q8 = json.load(f)
    q8 = [x for x in q8 if x < 1]
with open("q10.txt", "r") as f:
    q10 = json.load(f)
    q10 = [x for x in q10 if x < 1]


q0.sort()
q4.sort()
q6.sort()
q8.sort()
q10.sort()

unique_q0 = list(Counter(q0).keys()) # equals to list(set(words))
freqs_q0 = list(Counter(q0).values()) # counts the elements' frequency

unique_q4 = list(Counter(q4).keys()) # equals to list(set(words))
freqs_q4 = list(Counter(q4).values()) # counts the elements' frequency

unique_q6 = list(Counter(q6).keys()) # equals to list(set(words))
freqs_q6 = list(Counter(q6).values()) # counts the elements' frequency

unique_q8 = list(Counter(q8).keys()) # equals to list(set(words))
freqs_q8 = list(Counter(q8).values()) # counts the elements' frequency

unique_q10 = list(Counter(q10).keys()) # equals to list(set(words))
freqs_q10 = list(Counter(q10).values()) # counts the elements' frequency

# print(len(unique_q0), len(unique_q4), len(unique_q6), len(unique_q8), len(unique_q10))
#
# print(unique_q0)
# print(unique_q4)
# print(unique_q6)
# print(unique_q8)
# print(unique_q10)

# with open("bcodes.txt", "w") as f:
#     f.write(json.dumps(q0))
# with open("q4.txt", "w") as f:
#     f.write(json.dumps(q4))
# with open("q6.txt", "w") as f:
#     f.write(json.dumps(q6))
# with open("q8.txt", "w") as f:
#     f.write(json.dumps(q8))
# with open("q10.txt", "w") as f:
#     f.write(json.dumps(q10))

# plt.bar(unique_q0, freqs_q0)
# plt.xlabel('bcodes')
# plt.ylabel('count')
# plt.show()
#
# plt.bar(unique_q4, freqs_q4)
# plt.xlabel('q4')
# plt.ylabel('count')
# plt.show()
#
# plt.bar(unique_q6, freqs_q6)
# plt.xlabel('q6')
# plt.ylabel('count')
# plt.show()
#
# plt.bar(unique_q8, freqs_q8)
# plt.xlabel('q10')
# plt.ylabel('count')
# plt.show()
#
# plt.bar(unique_q10, freqs_q10)
# plt.xlabel('bcodes')
# plt.ylabel('count')
# plt.show()