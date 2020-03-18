# Millerite
Deer Neural Networks for Millerite surface energy calculation

[Millerite](https://en.wikipedia.org/wiki/Millerite), the trigonal NiS crystal, has a complicated crystal structure that makes calculating its surface properties through classical computational materials science methods troublesome. The goal of this project is to implement the high-dimentional neural networks (HDNN) to calculate surface energy of different possible facets of Millerite. This project is divided into three phases as follows:

* __Phase 1__: Making the initial structures for VASP single point energy calculations. This structures are made from 3D nanocluster configurations made in Materials Studio (input files are XSD files). The code reads XSD fils and makes charge neutral nanocluster configurations by removing cations (Ni) or anaions (S) from the surface of the nanocluster randomley. The VASP POSCAR file is then made from this atomic configuration. 

  Each structure is given a structure code and once a random stucture is built, its structure code is compared with the existing structures. The new structure is accepted if its not a duplicate. The structure code is built according to the number of each type of undercoordinated atoms on its surface. For a simple crystl structure, coordination number (number of the close neighbors) along with the atom type (Ni or S) may be enough to build an adequate structural code for an undercoordinated atom. For millerite how ever, it is not possible. 

* __Phase 2__: Building the training set. After calculating the energies of all nanoclusters built in Phase 1, this code is making a training set for training the neural network. 
