from First_Neighbors import utils

atoms, cell = utils.read_xsd('FCC.xsd')
atoms = utils.steinhardt(atoms, cell, 2.6, 4)

print(atoms)