import os
from pathlib import Path
from Phase2.Bond_code import utils
import dpdata

address = Path('/home/khalkhal/Simulations/VASP/Millerite/Machine_Learning/new-training-builder/VASP_folder')

def run_lammps(address, counter):
    '''
    This function runs lammps to relax the Millerite structures
    '''
    input = str(address) + '/in.temp'
    with open(input, 'w') as f:
        f.write('\n')
        f.write('units		    metal\n')
        f.write('atom_style     atomic\n')
        f.write('boundary	    p p p\n')
        f.write('read_data 	    %s/conf.lmp\n' % (str(address)))
        if counter:
            f.write('include	    %s/system.freeze\n' % (str(address)))
        f.write('pair_style     eam/alloy\n')
        f.write('pair_coeff     * * /home/khalkhal/Simulations/VASP/Millerite/NiS.eam.alloy Ni S \n')
        if counter:
            f.write('fix            1 bulk setforce 0.0 0.0 0.0\n')
        f.write('min_style	    cg\n')
        f.write('minimize	    1.0e-5 1.0e-7 10000 10000\n')
        f.write('write_data 	%s/rlx.lmp\n' % (str(address)))
    command = 'source /opt/LAMMPS/lammps-intel.sh; lmp_intel < ' + str(address) + '/in.temp > ' + str(address) + '/out.lmp'
    os.system(command)
    # os.system('lmp_intel < in.temp')

for dir in os.listdir(address):
    print(dir)
    #
    poscar = address / dir / "POSCAR"
    # potcar = address / dir / "POTCAR"
    # incar = address / dir / "INCAR"
    # kpoints = address / dir / "KPOINTS"
    # # read atoms from the original POSCAR file
    atoms, cell = utils.read_poscar(poscar)
    atoms = utils.CN(atoms, cell)
    #
    # # Make GEOM_OPT directory to geometry optimize the structure with lammps
    geom_opt_dir = address / dir / "GEOM_OPT"
    # if os.path.isdir(geom_opt_dir):
    #     command = 'rm -rf ' + str(geom_opt_dir)
    #     os.system(command)
    #
    # os.mkdir(geom_opt_dir)
    # # copy VASP files to the GEOM_OPT directory
    # cp_command = 'cp ' + str(incar) + ' ' + str(geom_opt_dir)
    # os.system(cp_command)
    # cp_command = 'cp ' + str(poscar) + ' ' + str(geom_opt_dir)
    # os.system(cp_command)
    # cp_command = 'cp ' + str(potcar) + ' ' + str(geom_opt_dir)
    # os.system(cp_command)
    # cp_command = 'cp ' + str(kpoints) + ' ' + str(geom_opt_dir)
    # os.system(cp_command)
    # # make lammps data file from POSCAR using dpdata
    poscar_old = geom_opt_dir / "POSCAR"
    # poscar_new = geom_opt_dir / "p"
    # cp_command = 'mv ' + str(poscar_old) + ' ' + str(poscar_new)
    # os.system(cp_command)
    # d_poscar = dpdata.System(str(geom_opt_dir) + '/p', fmt='vasp/poscar')
    # d_poscar.to('lammps/lmp', str(geom_opt_dir) + '/conf.lmp', frame_idx=0)
    # # finding atoms in bulk to freeze them during geometry optimization (bcodes for Ni and S atoms in bulk are 53 and
    # # 132, respectively)
    # counter = 0
    # with open(str(geom_opt_dir) + '/system.freeze', 'w') as f:
    #     f.write('group bulk id ')
    #     for i, atom in enumerate(atoms):
    #         # print(atom)
    #         if atom[3] == 132 or atom[3] == 53:
    #             counter += 1
    #             f.write('%d ' % (i+1))
    # # run lammps
    # run_lammps(geom_opt_dir, counter)
    # # convert the structure relazex bu lammps back to POSCAR
    # d_lmp = dpdata.System(str(geom_opt_dir) + '/rlx.lmp', fmt='lammps/lmp')
    # d_lmp.to('vasp/poscar', str(geom_opt_dir) + '/POSCAR', frame_idx=0)
    # # read new atomic positions from the relaxed structure
    atoms_new, cell = utils.read_poscar(poscar_old)
    #calculate properties of the new atoms
    atoms_new = utils.CN(atoms_new, cell)
    atoms_new = utils.steinhardt(atoms_new, cell, 2.55, [4, 6, 8, 10])
    # write new atomic configuration to the atoms.json file
    atom_file = geom_opt_dir / "atoms.json"
    utils.write_to_json(atom_file, atoms_new)





