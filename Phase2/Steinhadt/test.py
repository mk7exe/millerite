import json
import numpy as np
import matplotlib.pyplot as plt

with open('q4.txt', 'r') as f:
    q4 = json.load(f)
with open('q6.txt', 'r') as f:
    q6 = json.load(f)

plt.hist2d(q4, q6, bins=(50, 50), range=[[0, 1], [0, 1]], cmap=plt.cm.jet)
cb = plt.colorbar()
plt.show()

plt.hist(q4, bins=50, range=[0, 1])
plt.title('q4')
plt.show()

plt.hist(q6, bins=50, range=[0, 1])
plt.title('q6')
plt.show()
# hist, bin_edges = np.histogram(q4, bin=100, density=True)
# print(hist)