#A.S. This macro takes two bodies as inputs and calculates/plots their distance over time. Other things could be done too...

import glob
import numpy as np
import matplotlib.pyplot as plt
import re
import sys

def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

dir = sys.argv[1]
files = glob.glob(dir+'follow*.txt')
files = sorted(files, key=natural_key)
N_bodies = len(files)

input = raw_input('Enter body 1 to track: ')
body1 = int(input)
input = raw_input('Enter body 2 to track: ')
body2 = int(input)

#read in data for each body
data1=np.genfromtxt(files[body1-1],delimiter='  ',dtype=float)
data2=np.genfromtxt(files[body2-1],delimiter='  ',dtype=float)

nr,nc = data2.shape
time = np.zeros(nr)
r = np.zeros(nr)
min_r = 100
time_min_r = 0
for i in xrange(0,nr):
    dx = data1[i][2] - data2[i][2]
    dy = data1[i][3] - data2[i][3]
    dz = data1[i][4] - data2[i][4]
    r[i] = (dx*dx + dy*dy + dz*dz)**0.5
    time[i] = data1[i][0]
    if r[i] < min_r:
        min_r = r[i]
        time_min_r = time[i]

plt.plot(time, r, 'o', ms=2)
plt.xlabel('time (years)')
plt.ylabel('r (AU)')
plt.yscale('log')
plt.xscale('log')
plt.savefig(dir+'p'+str(body1)+'-p'+str(body2)+'_distance.png')
print 'min distance (AU) between bodies',body1,'and',body2,'is',min_r,'at time',time_min_r
plt.show()