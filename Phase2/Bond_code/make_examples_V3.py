'''
This code make the dataset for the NN training. In each example, x is a structure identifier and y in the energy
difference between the structure and bulk with teh same number of atoms. The excess energy is due to undercoordinated
atoms, so only undercoordinated atoms are considered in old_datasets. The structure identifier (x) is an array with 68
elements called Struct_Code. The ith element in Struct_Code represents the number of undercoordinated atoms in the
structure having bcode equal to UCCode[i].

In this version, training set is made of all non slab configurations and some slab configurations to make the
total size of the training set 85% of the total number of examples. Dev and test sets are entirely made of
slab configurations.
'''

import numpy as np
import os
import json
import h5py
from pathlib import Path
import matplotlib.pyplot as plt
from Phase2.Bond_code import utils

hisLow = 0.0
hisHigh = 1.0
#Energy per NiS in Millerite unitcell
eng_NiS = float(-93.110682/9)


def sinle_example(atoms, temp):
    f_atom_num = len(atoms)
    ids = [i for i in range(len(atoms)) if atoms[i][3] != 53 and atoms[i][3] != 132]  # find surface atoms
    uc_num = len(ids)
    # we are only interested in order parameters of atoms on (or near) surface
    code = utils.struc_code(atoms)
    x = np.divide(code, uc_num)  # normalizing the mesh to the total number of atoms

    # this is the energy difference between our structure and bulk.
    eng = float(temp)
    y = eng - eng_NiS * f_atom_num / 2
    y /= uc_num

    return x, y


os.system('rm datasets/*')

address = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/surfaces')
struct_num = -1
print("reading vasp files to build the training set ...")
counter = 0
xlist = []
ylist = []
for dir_path in os.listdir(address):
    print("Structure %s" % dir_path, end="\n")
    # first read the unrelaxed structure
    oszicar = address / dir_path / "OSZICAR"
    if os.path.isfile(oszicar):
        eng = utils.read_oszicar(oszicar) # red energy from oszicar. eng = 0.0 if simulation is not finished
        if eng != 0.0: # deal with the simulation only if it is finished
            counter += 1
            poscar = address / dir_path / "POSCAR"
            atoms, cell = utils.read_poscar(poscar)
            atom_num = len(atoms)
            atoms = utils.CN(atoms, cell)
            x, y = sinle_example(atoms, eng)
            # print (x, y)
            xlist.append(x)
            ylist.append(y)

x = np.array(xlist)
y = np.array(ylist)

h5f = h5py.File('datasets/surface_2D.h5', 'w')
h5f.create_dataset('x', data=x)
h5f.create_dataset('y', data=y)
h5f.close()


sim_folder_old = Path("/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/DataSet/Big_Training")
eng_file = sim_folder_old / "energies.dat"
struct_num = -1

print("reading vasp files to build the training set ...")
counter = 0
xlist_cluster = []
ylist_cluster = []
xlist_slab = []
ylist_slab = []
# reading the old simulations. Vasp files were removed but energies can be written from energy.dat file. POSCAR files
# can be written normally.
with open(eng_file, 'r') as f:
    for line in f:
        counter += 1
        temp = line.split()
        id = int(temp[0])
        if counter % 10 == 0:
            print("Structure %s" % str(id), end="\n")
        atom_file = sim_folder_old / "VASP_files" / str(id) / "atoms.json"
        with open(atom_file) as f:
            atoms = json.load(f)  # atoms have already saved in atoms.json
        x, y = sinle_example(atoms, temp[5])
        xlist_cluster.append(x)
        ylist_cluster.append(y)

# reading new simulations. These simulations also have geometry optimized version saved in GEOM_OPT folder.
address = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/VASP_folder')
for dir_path in os.listdir(address):
    if counter % 10 == 0:
        print("Structure %s" % dir_path, end="\n")
    if counter > struct_num > 0:
        break
    # first read the unrelaxed structure
    oszicar = address / dir_path / "OSZICAR"
    if os.path.isfile(oszicar):
        eng = utils.read_oszicar(oszicar) # red energy from oszicar. eng = 0.0 if simulation is not finished
        if eng != 0.0: # deal with the simulation onle if it is finished
            counter += 1
            atom_file = address / dir_path / "atoms.json"
            with open(atom_file) as f:
                atoms = json.load(f) # atoms have already saved in atoms.json
            x, y = sinle_example(atoms, eng)

            slabs = address / dir_path / "slabs"
            if os.path.isfile(slabs):
                xlist_slab.append(x)
                ylist_slab.append(y)
            else:
                xlist_cluster.append(x)
                ylist_cluster.append(y)

xcluster = np.array(xlist_cluster)
ycluster = np.array(ylist_cluster)
xslab = np.array(xlist_slab)
yslab = np.array(ylist_slab)

print("ycluster and yslab sizes: ", ycluster.shape, yslab.shape)

# data divided to 70/15/15 for training/dev/test
train_size = int(0.85*counter)
dev_size = int(0.15*counter)
print("training, dev, and test set sizes: ", train_size, dev_size)

# shuffle data
perm = list(np.random.permutation(yslab.shape[0]))
xslab = xslab[perm, :]
yslab = yslab[perm]

# the amount of the slab examples going to training dataset
train_from_slab_size = max(0, train_size - int(ycluster.shape[0]))
xtrain = np.concatenate((xcluster, xslab[:train_from_slab_size, :]))
ytrain = np.concatenate((ycluster, yslab[:train_from_slab_size]))
xdev = xslab[train_from_slab_size+1:train_from_slab_size+dev_size+1, :]
ydev = yslab[train_from_slab_size+1:train_from_slab_size+dev_size+1:]

print("xtrain shape: ", xtrain.shape)
print("ytrain shape: ", ytrain.shape)
print("xdev shape: ", xdev.shape)
print("ydev shape: ", ydev.shape)

h5f = h5py.File('datasets/data_1D.h5', 'w')
h5f.create_dataset('xtrain', data=xtrain)
h5f.create_dataset('ytrain', data=ytrain)
h5f.create_dataset('xdev', data=xdev)
h5f.create_dataset('ydev', data=ydev)
h5f.create_dataset('xtest', data=xdev)
h5f.create_dataset('ytest', data=ydev)
h5f.close()

os.system('zip -r data.zip datasets')
os.system('rm datasets/*')
os.system('mv data.zip datasets')


