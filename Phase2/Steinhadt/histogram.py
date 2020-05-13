import json
import numpy as np
import matplotlib.pyplot as plt

with open('q4.txt', 'r') as f:
    q4 = json.load(f)
    print(min(q4), max(q4))
with open('q6.txt', 'r') as f:
    q6 = json.load(f)
    print(min(q6), max(q6))
with open('q10.txt', 'r') as f:
    q10 = json.load(f)
with open('q8.txt', 'r') as f:
    q8 = json.load(f)

plt.hist2d(q4, q6, bins=(100, 100), range=[[0.1, 0.8], [0.1, 0.8]], cmap=plt.cm.jet)
cb = plt.colorbar()
plt.show()

plt.hist(q4, bins=50, range=[0.1, 0.8])
plt.title('q4')
plt.show()

plt.hist(q6, bins=50, range=[0.1, 0.8])
plt.title('q6')
plt.show()

plt.hist(q8, bins=50, range=[0, 1])
plt.title('q8')
plt.show()

plt.hist(q10, bins=50, range=[0, 1])
plt.title('q10')
plt.show()
# hist, bin_edges = np.histogram(q4, bin=100, density=True)
# print(hist)