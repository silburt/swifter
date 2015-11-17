#A.S. Program to call tool_follow and output all the planet/particle data and put it into follow/
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
    m0 = float(split[2])   #get suns mass
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
    return m, m0

def get_com(cube, m, m0, iteration, N_bods):
    com = np.zeros(7) #m,x,y,z,vx,vy,vz
    com[0] += m0
    for i in xrange(0,N_bods):
        if m[i] > m[-1]:
            com[1] += m[i]*cube[i][iteration][2] #x
            com[2] += m[i]*cube[i][iteration][3] #y
            com[3] += m[i]*cube[i][iteration][4] #z
            com[4] += m[i]*cube[i][iteration][5] #vx
            com[5] += m[i]*cube[i][iteration][6] #vy
            com[6] += m[i]*cube[i][iteration][7] #vz
            com[0] += m[i]
    if com[0] > 0:
        com[1] /= com[0]
        com[2] /= com[0]
        com[3] /= com[0]
        com[4] /= com[0]
        com[5] /= com[0]
        com[6] /= com[0]
    return com

def get_energy(cube, m, m0, com, iteration, N_bods):
    K = 0
    U = 0
    G = 1   #G=1 units
    K += 0.5*m0*(com[4]*com[4] + com[5]*com[5] + com[6]*com[6])   #sun non-zero in COM frame
    for i in xrange(0,N_bods):
        dx = cube[i][iteration][2]
        dy = cube[i][iteration][3]
        dz = cube[i][iteration][4]
        dvx = cube[i][iteration][5] - com[4]
        dvy = cube[i][iteration][6] - com[5]
        dvz = cube[i][iteration][7] - com[6]
        r = (dx*dx + dy*dy + dz*dz)**0.5
        U -= G*m0*m[i]/r                                        #U_sun/massive body
        K += 0.5*m[i]*(dvx*dvx + dvy*dvy + dvz*dvz)               #KE body
        if m[i] > m[-1]:    #ignore forces between planetesimals
            for j in xrange(i+1,N_bods):
                ddx = dx - cube[j][iteration][2]
                ddy = dy - cube[j][iteration][3]
                ddz = dz - cube[j][iteration][4]
                r = (ddx*ddx + ddy*ddy + ddz*ddz)**0.5
                U -= G*m[i]*m[j]/r  #U between bodies
    return U + K

def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

dir = sys.argv[1]
massdir = sys.argv[2]    #location of where masses are stored
files = glob.glob(dir+'follow*.txt')
files = sorted(files, key=natural_key)
N_bodies = len(files)

#read in data for each body
print 'get data cube'
cube=np.genfromtxt(files[1],delimiter='  ',dtype=float) #file 0 is the sun which is empty
nr, nc = cube.shape
cube = np.reshape(cube, (1,nr,nc))
for i in xrange(2,N_bodies):
    data=np.genfromtxt(files[i],delimiter=None,dtype=float)
    data = np.reshape(data, (1,nr,nc))
    cube = np.concatenate((cube,data),axis=0)

N_bods,N_output,N_cols = cube.shape

#get masses of each body
print 'get masses'
m, m0 = get_mass(massdir,0)
#mtp = get_mass("tp.in",1)
#m = np.concatenate([mp,mtp])    #0th slot is sun's mass!!

#calc E of system at time 0
dE = np.zeros(N_output)
time = np.zeros(N_output)
com = get_com(cube,m,m0,0,N_bods)
E0 = get_energy(cube,m,m0,com,0,N_bods)
print 'calculating energy'
increment = 0.1*N_output
for i in xrange(0,N_output):
    com = get_com(cube,m,m0,i,N_bods)
    E = get_energy(cube,m,m0,com,i,N_bods)
    dE[i] = np.fabs((E - E0)/E0)
    time[i] = cube[0][i][0]
    if i > increment:
        print '% done =',round(100*float(i)/float(N_output))
        increment += 0.1*N_output

plt.plot(time, dE, 'o')
plt.yscale('log')
plt.xscale('log')
plt.savefig(dir+'Energy.png')
plt.show()

