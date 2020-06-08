import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

# os.system('unzip -o structural_parameters/q100.zip')

dataset = h5py.File('structural_parameters/surface_Q.h5', "r")
surf_q4 = np.array(dataset["q4"][:])
surf_q6 = np.array(dataset["q6"][:])

dataset = h5py.File('structural_parameters/cluster_Q.h5', "r")
clus_q4 = np.array(dataset["q4"][:])
clus_q6 = np.array(dataset["q6"][:])

dataset = h5py.File('structural_parameters/slab_Q.h5', "r")
slab_q4 = np.array(dataset["q4"][:])
slab_q6 = np.array(dataset["q6"][:])

x = np.arange(100)
x_pos = np.arange(0, 110, step=10)
x_label = [str(np.round(i*0.01, 2)) for i in x_pos]

plt.figure()
plt.subplot(1, 2, 1)
plt.bar(x, surf_q4)
plt.ylabel('Q4')
plt.title('Surface')
plt.xticks(x_pos, x_label)
plt.xticks(rotation=90)

plt.subplot(1, 2, 2)
plt.bar(x, surf_q6)
plt.ylabel('Q6')
plt.title('Surface')
plt.xticks(x_pos, x_label)
plt.xticks(rotation=90)
plt.show()

plt.figure()
plt.subplot(1, 2, 1)
plt.bar(x, slab_q4)
plt.ylabel('Q4')
plt.title('Slab')
plt.xticks(x_pos, x_label)
plt.xticks(rotation=90)

plt.subplot(1, 2, 2)
plt.bar(x, slab_q6)
plt.ylabel('Q6')
plt.title('Slab')
plt.xticks(x_pos, x_label)
plt.xticks(rotation=90)
plt.show()

plt.figure()
plt.subplot(1, 2, 1)
plt.bar(x, clus_q4)
plt.ylabel('Q4')
plt.title('Cluster')
plt.xticks(x_pos, x_label)
plt.xticks(rotation=90)

plt.subplot(1, 2, 2)
plt.bar(x, clus_q6)
plt.ylabel('Q6')
plt.title('Cluster')
plt.xticks(x_pos, x_label)
plt.xticks(rotation=90)
plt.show()