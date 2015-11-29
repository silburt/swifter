#A.S. This actually calculates the energy based on the outputted xyz and vx,vy,vz positions/velocities
#Symba only uses massless particles, and so there is no particle-particle interactions!!
#Python note: genfromtxt only makes a 2D array if all the elements are of the same type. Otherwise what I get is called a "structured ndarray". Makes it hard to concatenate and stuff, though it can still work with np.dstack.

import glob
import numpy as np
import re
import matplotlib.pyplot as plt
import sys

def get_mass(mass_file, tp):
    fos = open(mass_file,'r')
    lines = fos.readlines()
    n_lines = len(lines)
    m=np.zeros(0)
    temp = lines[1]     #get suns mass
    split = temp.split(" ") #get suns mass
    m = np.append(m,float(split[2]))   #get suns mass
    junk = "\n"
    n_skip = 4
    i=4
    while i < n_lines:
        temp = lines[i]
        split = temp.split(" ")
        if tp == 1:
            val = 0
            m=np.append(m,val)
        else:
            m=np.append(m,float(split[2]))
        i += n_skip
    return m

def h2b(cube, m, iteration, N_bodies, mtiny):  #heliocentric to barycentric
    com = np.zeros(7) #m,x,y,z,vx,vy,vz
    com[0] = m[0]
    for i in xrange(1,N_bodies):
        if m[i] > mtiny:
            com[1] += m[i]*cube[i-1][iteration][2] #x
            com[2] += m[i]*cube[i-1][iteration][3] #y
            com[3] += m[i]*cube[i-1][iteration][4] #z
            com[4] += m[i]*cube[i-1][iteration][5] #vx
            com[5] += m[i]*cube[i-1][iteration][6] #vy
            com[6] += m[i]*cube[i-1][iteration][7] #vz
            com[0] += m[i]
    x = np.zeros(N_bodies)
    y = np.zeros(N_bodies)
    z = np.zeros(N_bodies)
    vx = np.zeros(N_bodies)
    vy = np.zeros(N_bodies)
    vz = np.zeros(N_bodies)
    x[0] = -com[1]/com[0]
    y[0] = -com[2]/com[0]
    z[0] = -com[3]/com[0]
    vx[0] = -com[4]/com[0]
    vy[0] = -com[5]/com[0]
    vz[0] = -com[6]/com[0]
    for i in xrange(1,N_bodies):
        x[i] = cube[i-1][iteration][2] + x[0]
        y[i] = cube[i-1][iteration][3] + y[0]
        z[i] = cube[i-1][iteration][4] + z[0]
        vx[i] = cube[i-1][iteration][5] + vx[0]
        vy[i] = cube[i-1][iteration][6] + vy[0]
        vz[i] = cube[i-1][iteration][7] + vz[0]
    return x, y, z, vx, vy, vz

def cal_energy(m,x,y,z,vx,vy,vz,N_bodies,mtiny):
    K = 0
    U = 0
    G = 1   #G=1 units
    for i in xrange(0,N_bodies):
        K += 0.5*m[i]*(vx[i]*vx[i] + vy[i]*vy[i] + vz[i]*vz[i])     #KE body
        if m[i] > mtiny:                    #ignore forces between planetesimals
            for j in xrange(i+1,N_bodies):
                dx = x[i] - x[j]
                dy = y[i] - y[j]
                dz = z[i] - z[j]
                r = (dx*dx + dy*dy + dz*dz)**0.5
                U -= G*m[i]*m[j]/r          #U between bodies
    return U + K

def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

dir = sys.argv[1]
massdir = 'swifter_pl.in'    #location of where masses are stored
files = glob.glob(dir+'follow*.txt')
files = sorted(files, key=natural_key)
N_bodies = len(files)

default_mtiny = '1e-07'
input = raw_input('Enter Mtiny value (default, Msun=1, mtiny=1e-07): ')
if not input:
    mtiny = float(default_mtiny)
else:
    mtiny = float(input)

try:
    energy_prototype = int(sys.argv[3]) #default array to make cube framework
except:
    energy_prototype = 1

#read in data for each body
print 'get data cube'
cube=np.genfromtxt(files[energy_prototype],delimiter='  ',dtype=float) #file 0 is the sun which is empty
nr, nc = cube.shape
cube = np.reshape(cube, (1,nr,nc))
for i in xrange(1,N_bodies):
    if i==energy_prototype:
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

N_bods,N_output,N_cols = cube.shape

#get masses of each body
print 'get masses'
m = get_mass(massdir,0)

#calc E of system at time 0
dE = np.zeros(N_output)
time = np.zeros(N_output)
x,y,z,vx,vy,vz = h2b(cube,m,0,N_bodies,mtiny)
E0 = cal_energy(m,x,y,z,vx,vy,vz,N_bodies,mtiny)
print 'calculating energy'
increment = 0.1*N_output
for i in xrange(1,N_output):
    x,y,z,vx,vy,vz = h2b(cube,m,i,N_bodies,mtiny)
    E = cal_energy(m,x,y,z,vx,vy,vz,N_bodies,mtiny)
    dE[i] = np.fabs((E - E0)/E0)
    time[i] = cube[0][i][0]
    if i > increment:
        print '% done =',round(100*float(i)/float(N_output))
        increment += 0.1*N_output

plt.plot(time, dE, 'o')
plt.yscale('log')
plt.xscale('log')
plt.savefig(dir+'Energy_fromoutput.png')
plt.show()