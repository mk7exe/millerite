import numpy as np
import os
import h5py
from pathlib import Path
from First_Neighbors import make_examples_utils as utils

#Energy per NiS in Millerite unitcell
eng_NiS = float(-93.110682/9)

def read_data(address, struct_num):
    xlist = []
    ylist = []
    counter = 0
    for dir in os.listdir(address):
        counter += 1
        if counter % 10 == 0:
            print("number of structures read: %d" % counter, end="\n")
        if counter > struct_num and struct_num > 0:
            break
        print("Structure ", counter, " is ", dir)
        poscar = address / dir / "POSCAR"
        oszicar = address / dir / "OSZICAR"

        atoms, cell = utils.read_poscar(poscar)
        atoms = utils.CN(atoms, cell)
        nis_num = len(atoms)/2
        code = utils.struc_code(atoms)
        xlist.append(code)

        eng = utils.read_oszicar(oszicar)
        eng_bar = eng - eng_NiS * nis_num
        ylist.append(eng_bar)
    x = np.array(xlist).T
    y = np.array(ylist)

    return x, y

# train_folder = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/DataSet/Big_Training/VASP_files')
# print("reading vasp files to build the training set ...")
# x_train, y_train = read_data(train_folder, 733)
# print(x_train.shape, y_train.shape)

print("reading vasp files to build the test set ...")
# test_folder = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/DataSet/Test/VASP_files'
# )
test_folder = Path('/home/khalkhal/Simulations/VASP/Millerite/Surfaces/Initial_Energy')
x_test, y_test = read_data(test_folder, -1)
print(x_test.shape, y_test.shape)

# h5f = h5py.File('datasets/training_dataset.h5', 'w')
# h5f.create_dataset('train_set_x', data=x_train)
# h5f.create_dataset('train_set_y', data=y_train)
# h5f.close()

h5f = h5py.File('datasets/test_dataset.h5', 'w')
h5f.create_dataset('test_set_x', data=x_test)
h5f.create_dataset('test_set_y', data=y_test)
h5f.close()