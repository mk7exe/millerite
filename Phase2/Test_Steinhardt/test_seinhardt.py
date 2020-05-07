from Phase2.First_Neighbors import utils

atoms, cell = utils.read_xsd('FCC.xsd')
atoms = utils.steinhardt(atoms, cell, 2.13, [4, 6])

print(atoms)

