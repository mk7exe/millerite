'''
This code makes representative struct codes for imaginary structures having only one to two bonds of a bond type
removed.
'''
import json
from pathlib import Path

dataset_folder = Path("C:\GitHub_Projects\millerite\Phase2\datasets")

UCCodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30,
           31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 81, 84, 87, 90,
           93, 96, 99, 102, 105, 108, 111, 114, 117, 120, 123, 126, 129]

bs = [26, 44, 35, 50, 45, 52, 51, 105, 123, 114, 129, 126]
names = ['Ni-1b1','Ni-1b2', 'Ni-2b2', 'Ni-1b3', 'Ni-2b3', 'Ni-1b4', 'Ni-2b4', 'S-1b1', 'S-1b2', 'S-2b2', 'S-1b3',
         'S-2b3']

bcodes = []
for b in bs:
    code = [0] * len(UCCodes)
    index = UCCodes.index(b)
    code[index] = 1
    bcodes.append(code)

dic = dict(zip(names, bcodes))
print(len(names), len(bs), len(bcodes), len(dic))

file = dataset_folder / "single_bonds.json"
with open(file, 'w') as fp:
    json.dump(dic, fp)

print(dic)