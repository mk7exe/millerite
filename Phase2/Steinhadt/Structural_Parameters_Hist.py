'''
This code make the dataset for the NN training. In each example, x is a structure identifier and y in the energy
difference between the structure and bulk with teh same number of atoms. The excess energy is due to undercoordinated
atoms, so only undercoordinated atoms are considered in old_datasets. The structure identifier (x) is a 100x100
matrix. x and y axes of the matrix represent 100-bin histograms of q4 and q6 parameters restricted between 0.1 and 0.8.
Each cell represents the number of atoms having steinhardt parameters in the corresponding range.

In this version, training set is made of all non slab configurations and some slab configurations to make the
total size of the training set 70% of the total number of examples. Dev and test sets are entirely made of
slab configurations.
'''

import numpy as np
import os
import json
import h5py
from pathlib import Path
import matplotlib.pyplot as plt
from Phase2.Bond_code import utils

bin_num = 100
hisLow = 0.0
hisHigh = 1.0
#Energy per NiS in Millerite unitcell
eng_NiS = float(-93.110682/9)

q4_his_slabs = np.zeros(bin_num)
q6_his_slabs = np.zeros(bin_num)
q4_his_clusters = np.zeros(bin_num)
q6_his_clusters = np.zeros(bin_num)
q4_his_surfaces = np.zeros(bin_num)
q6_his_surfaces = np.zeros(bin_num)

def sinle_example(atoms, temp):
    f_atom_num = len(atoms)
    ids = [i for i in range(len(atoms)) if atoms[i][3] != 53 and atoms[i][3] != 132]  # find surface atoms
    uc_num = len(ids)
    # we are only interested in order parameters of atoms on (or near) surface
    q4 = [atoms[i][5][0] for i in ids]
    q6 = [atoms[i][5][1] for i in ids]
    # q4 = [x[5][0] for x in atoms]
    # q6 = [x[5][1] for x in atoms]
    # calculate the 2D histogram
    hQ4, bin_edges = np.histogram(q4, bins=bin_num, range=[hisLow, hisHigh])
    hQ6, bin_edges = np.histogram(q6, bins=bin_num, range=[hisLow, hisHigh])
    return hQ4, hQ6


os.system('rm structural_parameters/*')

address = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/surfaces')
struct_num = -1
print("reading vasp files to build the training set ...")
counter = 0
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
            atoms = utils.steinhardt(atoms, cell, 2.55, [4, 6, 8, 10])
            hQ4, hQ6 = sinle_example(atoms, eng)
            q4_his_surfaces += hQ4
            q6_his_surfaces += hQ6
    oszicar = address / dir_path / "GEOM_OPT" / "OSZICAR"
    if os.path.isfile(oszicar):
        eng = utils.read_oszicar(oszicar)  # red energy from oszicar. eng = 0.0 if simulation is not finished
        if eng != 0.0:  # deal with the simulation only if it is finished
            counter += 1
            poscar = address / dir_path / "POSCAR"
            atoms, cell = utils.read_poscar(poscar)
            atom_num = len(atoms)
            atoms = utils.CN(atoms, cell)
            atoms = utils.steinhardt(atoms, cell, 2.55, [4, 6, 8, 10])
            hQ4, hQ6 = sinle_example(atoms, eng)
            q4_his_surfaces += hQ4
            q6_his_surfaces += hQ6

h5f = h5py.File('structural_parameters/surface_Q.h5', 'w')
h5f.create_dataset('q4', data=q4_his_surfaces)
h5f.create_dataset('q6', data=q6_his_surfaces)
h5f.close()


sim_folder_old = Path("/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/DataSet/Big_Training")
eng_file = sim_folder_old / "energies.dat"
struct_num = -1

print("reading vasp files to build the training set ...")
counter = 0

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
        hQ4, hQ6 = sinle_example(atoms, eng)
        q4_his_clusters += hQ4
        q6_his_clusters += hQ6

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
            # print("Initial %s" % dir_path, end="\n")
            atom_file = address / dir_path / "atoms.json"
            with open(atom_file) as f:
                atoms = json.load(f) # atoms have already saved in atoms.json
            hQ4, hQ6 = sinle_example(atoms, eng)

            slabs = address / dir_path / "slabs"
            if os.path.isfile(slabs):
                q4_his_slabs += hQ4
                q6_his_slabs += hQ6
            else:
                q4_his_clusters += hQ4
                q6_his_clusters += hQ6

    # now read the optimzed structure
    oszicar = address / dir_path / "GEOM_OPT" / "OSZICAR"
    if os.path.isfile(oszicar):
        eng = utils.read_oszicar(oszicar)
        if eng != 0.0:
            counter += 1
            # print("Relax %s" % dir_path, end="\n")
            atom_file = address / dir_path / "GEOM_OPT" / "atoms.json"
            with open(atom_file) as f:
                atoms = json.load(f)
            hQ4, hQ6 = sinle_example(atoms, eng)

            slabs = address / dir_path / "slabs"
            if os.path.isfile(slabs):
                q4_his_slabs += hQ4
                q6_his_slabs += hQ6
            else:
                q4_his_clusters += hQ4
                q6_his_clusters += hQ6

h5f = h5py.File('structural_parameters/cluster_Q.h5', 'w')
h5f.create_dataset('q4', data=q4_his_clusters)
h5f.create_dataset('q6', data=q6_his_clusters)
h5f.close()

h5f = h5py.File('structural_parameters/slab_Q.h5', 'w')
h5f.create_dataset('q4', data=q4_his_slabs)
h5f.create_dataset('q6', data=q6_his_slabs)
h5f.close()

os.system('zip -r q' + str(bin_num) + '.zip structural_parameters')
os.system('rm structural_parameters/*')
os.system('mv q' + str(bin_num) + '.zip structural_parameters')



