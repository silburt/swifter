#A.S. This just reads in the symba calculated energies and plots it.

import numpy as np
import matplotlib.pyplot as plt
import sys

dir = sys.argv[1]

#energy offset
f = open(dir+'energyoutput.txt')
lines=list(f)
N = len(lines)
dE = np.zeros(N)
t = np.zeros(N)
temp = lines[0]
temp2 = temp.split()
E0 = float(temp2[1])
for i in xrange(1,N):
    temp = lines[i]
    temp2 = temp.split()
    t[i] = float(temp2[0])
    E = float(temp2[1])
    Eoffset = float(temp2[2])
    dE[i] = abs((E0 - E - Eoffset)/E0)

plt.plot(t,dE,'o')
plt.yscale('log')
plt.xscale('log')
plt.savefig(dir+'Energy.png')
plt.show()

