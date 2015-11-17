import sys
import matplotlib.pyplot as plt
import numpy as np
import glob
import math
pi = math.pi
from mpl_toolkits.mplot3d import Axes3D
import re

def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

dir = sys.argv[1]
outputdir = 'movie_output/'
files = glob.glob(dir+'follow*.txt')
files = sorted(files, key=natural_key)
N_bodies = len(files)

try:
    movie_prototype = int(sys.argv[2])
except:
    movie_prototype = 1

#read in data for each body
print 'get data cube'
cube=np.genfromtxt(files[movie_prototype],delimiter='  ',dtype=float) #file 0 is the sun which is empty
nr, nc = cube.shape
cube = np.reshape(cube, (1,nr,nc))
for i in xrange(1,N_bodies):
    if i == movie_prototype:
        continue
    data=np.genfromtxt(files[i],delimiter=None,dtype=float)
    data=data[0:nr]
    try:
        data = np.reshape(data, (1,nr,nc))
    except:
        print 'Error, different array dimensions (probably from particle merging).'
        print 'Prototype dimenstions =',(nr,nc)
        print 'current data shape =',data.shape
        print 'Retry movie with movie_prototype =',i
        exit(0)
    cube = np.concatenate((cube,data),axis=0)

#colors - need to improve this later for any number of active/passive bodies
colors =  ["black" for x in range(N_bodies)]
colors[0] = 'orange'
colors[1] = 'red'

for i in xrange(0,nr):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(0,0,0,c='yellow', lw=0)  #sun
    for j in xrange(0,N_bodies-1):
        ax.scatter(cube[j][i][2],cube[j][i][3],cube[j][i][4],c=colors[j], lw=0)
    ax.set_xlim([-2,2])
    ax.set_ylim([-2,2])
    ax.set_zlim([-1,1])
    output = 't='+str(cube[0][i][0])
    ax.set_title(output)
    plt.savefig(dir+'movie_output'+str(i)+'.png')
    print 'completed iteration',i
