import numpy as np
import os
import h5py
from pathlib import Path
from Phase2.Bond_code import utils

#Energy per NiS in Millerite unitcell
eng_NiS = float(-93.110682/9)

def sinle_example(atoms, temp):
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
    x = np.divide(H.T, atom_num)  # normalizing the mesh to the total number of atoms
    # plt.imshow(H, interpolation='nearest', origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
    # plt.show()
    # this is the energy difference between our structure and bulk.
    eng = float(temp)
    y = 2 * eng / atom_num - eng_NiS

    return x, y

address = Path('/home/khalkhal/Simulations/VASP/Millerite/Surfaces/Initial_Energy')
struct_num = -1
print("reading vasp files to build the training set ...")
counter = 0
xlist = []
ylist = []
for dir_path in os.listdir(address):
    counter += 1
    print("Structure %s" % dir_path, end="\n")
    # first read the unrelaxed structure
    oszicar = address / dir_path / "OSZICAR"
    if os.path.isfile(oszicar):
        eng = utils.read_oszicar(oszicar) # red energy from oszicar. eng = 0.0 if simulation is not finished
        if eng != 0.0: # deal with the simulation onle if it is finished
            poscar = address / dir_path / "POSCAR"
            atoms, cell = utils.read_poscar(poscar)
            atom_num = len(atoms)
            atoms = utils.CN(atoms, cell)
            atoms = utils.steinhardt(atoms, cell, 2.55, [4, 6, 8, 10])
            x, y = sinle_example(atoms, eng)
            xlist.append(x)
            ylist.append(y)
x = np.array(xlist)
y = np.array(ylist)

print(x.shape)
print(y.shape)
print(np.max(x))

h5f = h5py.File('old_datasets/surface_2D.h5', 'w')
h5f.create_dataset('x', data=x)
h5f.create_dataset('y', data=y)
h5f.close()