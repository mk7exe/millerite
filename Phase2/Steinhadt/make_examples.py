'''
This code make the dataset for the NN training. In each example, x is a structure identifier and y in the energy
difference between the structure and bulk with teh same number of atoms. The excess energy is due to undercoordinated
atoms, so it is normalized by the number of the undercoordinated atoms. The structure identifier (x) is a 100x100
matrix. x and y axes of the matrix represent 100-bin histograms of q4 and q6 parameters restricted between 0.1 and 0.8.
Each cell represents the number of atoms having steinhardt parameters in the corresponding range.
'''

import numpy as np
import os
import json
import h5py
from pathlib import Path
import matplotlib.pyplot as plt
from Phase2.Bond_code import utils

database_folder = Path("/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/datasets")
#Energy per NiS in Millerite unitcell
eng_NiS = float(-93.110682/9)

sim_folder_old = Path("/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/DataSet/Big_Training")
eng_file = sim_folder_old / "energies.dat"
struct_num = -1

print("reading vasp files to build the training set ...")
counter = 0
xlist = []
ylist = []
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
        if counter > struct_num > 0:
            break
        atom_file = sim_folder_old / "VASP_files" / str(id) / "atoms.json"
        with open(atom_file) as f:
            atoms = json.load(f)  # atoms have already saved in atoms.json
        atom_num = len(atoms)
        # ids = [i for i in range(len(atoms)) if atoms[i][3] != 53 and atoms[i][3] != 132]  # find surface atoms
        # uc_num = len(ids)
        # we are only interested in order parameters of atoms on (or near) surface
        # q4 = [atoms[i][5][0] for i in ids]
        # q6 = [atoms[i][5][1] for i in ids]
        q4 = [x[5][0] for x in atoms]
        q6 = [x[5][1] for x in atoms]
        # calculate the 2D histogram
        H, xedges, yedges = np.histogram2d(q4, q6, bins=(100, 100), range=[[0.1, 0.8], [0.1, 0.8]])
        H = H.T  # normalizing the mesh to the total number of atoms
        # plt.imshow(H, interpolation='nearest', origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
        # plt.show()

        # this is the energy difference between our structure and bulk.
        eng = float(temp[5])
        eng_bar = 2 * eng / atom_num - eng_NiS

        xlist.append(H)
        ylist.append(eng_bar)

# reading new simulations. These simulations also have geometry optimized version saved in GEOM_OPT folder.
address = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/VASP_folder')
for dir_path in os.listdir(address):
    counter += 1
    if counter % 10 == 0:
        print("Structure %s" % dir_path, end="\n")
    if counter > struct_num > 0:
        break

    # first read the unrelaxed structure
    oszicar = address / dir_path / "OSZICAR"
    if os.path.isfile(oszicar):
        eng = utils.read_oszicar(oszicar) # red energy from oszicar. eng = 0.0 if simulation is not finished
        if eng != 0.0: # deal with the simulation onle if it is finished
            atom_file = address / dir_path / "atoms.json"
            with open(atom_file) as f:
                atoms = json.load(f) # atoms have already saved in atoms.json
            atom_num = len(atoms)
            # ids = [i for i in range(len(atoms)) if atoms[i][3] != 53 and atoms[i][3] != 132]  # find surface atoms
            # uc_num = len(ids)
            # we are only interested in order parameters of atoms on (or near) surface
            # q4 = [atoms[i][5][0] for i in ids]
            # q6 = [atoms[i][5][1] for i in ids]
            q4 = [x[5][0] for x in atoms]
            q6 = [x[5][1] for x in atoms]
            # calculate the 2D histogram
            H, xedges, yedges = np.histogram2d(q4, q6, bins=(100, 100), range=[[0.1, 0.8], [0.1, 0.8]])
            H = H.T # normalizing the mesh to the total number of atoms
            # plt.imshow(H, interpolation='nearest', origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
            # plt.show()

            # this is the energy difference between our structure and bulk.
            eng_bar = 2*eng/atom_num - eng_NiS

            xlist.append(H)
            ylist.append(eng_bar)

            slabs = address / dir_path / "slabs"
            if os.path.isfile(slabs):
                xlist_slab.append(H)
                ylist_slab.append(eng_bar)

    # now read the optimzed structure
    oszicar = address / dir_path / "GEOM_OPT" / "OSZICAR"
    if os.path.isfile(oszicar):
        eng = utils.read_oszicar(oszicar)
        if eng != 0.0:
            atom_file = address / dir_path / "GEOM_OPT" / "atoms.json"
            with open(atom_file) as f:
                atoms = json.load(f)
            atom_num = len(atoms)
            # ids = [i for i in range(len(atoms)) if atoms[i][3] != 53 and atoms[i][3] != 132]  # find surface atoms
            # uc_num = len(ids)
            # we are only interested in order parameters of atoms on (or near) surface
            # q4 = [atoms[i][5][0] for i in ids]
            # q6 = [atoms[i][5][1] for i in ids]
            q4 = [x[5][0] for x in atoms]
            q6 = [x[5][1] for x in atoms]
            H, xedges, yedges = np.histogram2d(q4, q6, bins=(100, 100), range=[[0.1, 0.8], [0.1, 0.8]])
            H = H.T
            # plt.imshow(H, interpolation='nearest', origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
            # plt.show()

            eng_bar = 2*eng/atom_num - eng_NiS

            xlist.append(H)
            ylist.append(eng_bar)

            slabs = address / dir_path / "slabs"
            if os.path.isfile(slabs):
                xlist_slab.append(H)
                ylist_slab.append(eng_bar)

x = np.array(xlist)
y = np.array(ylist)
xslab = np.array(xlist_slab)
yslab = np.array(ylist_slab)
print(y.shape)
print(np.max(x))

# x = np.divide(x, np.max(x))
# xslab = np.divide(xslab, np.max(x))
# # print(x.shape)
# print(np.max(x))

h5f = h5py.File('datasets/training_2D.h5', 'w')
h5f.create_dataset('x', data=x)
h5f.create_dataset('y', data=y)
h5f.close()

h5f = h5py.File('datasets/slab_2D.h5', 'w')
h5f.create_dataset('x', data=xslab)
h5f.create_dataset('y', data=yslab)
h5f.close()

os.system(' zip -r datasets/data.zip datasets')
os.system('rm datasets/training_2D.h5')
os.system('rm datasets/slab_2D.h5')

# dataset_num = int(y.shape[0]/1000)
# for i in range(dataset_num):
#     h5f = h5py.File(database_folder+'/training_2D_'+str(i+1)+'.h5', 'w')
#     h5f.create_dataset('x', data=x[i*1000:(i+1)*1000-1])
#     h5f.create_dataset('y', data=y[i*1000:(i+1)*1000-1])
#     h5f.close()
# h5f = h5py.File(database_folder+'/training_2D_'+str(i+2)+'.h5', 'w')
# h5f.create_dataset('x', data=x[(i+1)*1000:])
# h5f.create_dataset('y', data=y[(i+1)*1000:])
# h5f.close()
#
# dataset_num = int(yslab.shape[0]/1000)
# for i in range(dataset_num):
#     h5f = h5py.File(database_folder+'/slab_2D_'+str(i+1)+'.h5', 'w')
#     h5f.create_dataset('x', data=xslab[i*1000:(i+1)*1000-1])
#     h5f.create_dataset('y', data=yslab[i*1000:(i+1)*1000-1])
#     h5f.close()
# h5f = h5py.File(database_folder+'/slab_2D_'+str(i+2)+'.h5', 'w')
# h5f.create_dataset('x', data=xslab[(i+1)*1000:])
# h5f.create_dataset('y', data=yslab[(i+1)*1000:])
# h5f.close()


    # plt.hist2d(q4, q6, bins=(100, 100), range=[[0.1, 0.8], [0.1, 0.8]], cmap=plt.cm.Greys)
    # cb = plt.colorbar()
    # plt.title(str(dir_path) + ' opt')
    # plt.show()


