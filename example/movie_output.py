import sys
import matplotlib.pyplot as plt
import numpy as np
import glob
import math
pi = math.pi
from mpl_toolkits.mplot3d import Axes3D
import re

def get_color(id,N_massive):
    color = 'black'
    if id == 0:
        color = 'yellow'
    elif id <= N_massive:
        color = 'red'
    return color

def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

dir = sys.argv[1]
outputdir = 'output_movie/'
files = glob.glob(dir+'follow*.txt')
files = sorted(files, key=natural_key)
N_bodies = len(files)

N_massive = int(raw_input("Number of **massive** bodies (including sun): "))

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

#limits for plots = (x,y,z/2)
limit = 20

print 'deleting any existing .png images in output_movie folder'
call("rm output_movie/*.png",shell=True)

#output movie
for i in xrange(0,nr):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(0,0,0,c='yellow', lw=0)  #sun
    for j in xrange(0,N_bodies-1):
        color = get_color(cube[j][i][1],N_massive)
        ax.scatter(cube[j][i][2],cube[j][i][3],cube[j][i][4],c=color, lw=0)
    ax.set_xlim([-limit,limit])
    ax.set_ylim([-limit,limit])
    ax.set_zlim([-limit/4,limit/4])
    ax.view_init(elev = 90, azim=100)    #both are in degrees. elev = 0 or 90 is what you want
    output = 't='+str(cube[0][i][0])
    ax.set_title(output)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.savefig(outputdir+'movie_output'+str(i)+'.png')
    print 'completed iteration '+str(i)+' of '+str(nr)
