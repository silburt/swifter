#A.S. This actually calculates the energy based on the outputted xyz and vx,vy,vz positions/velocities
#Symba only uses massless particles, and so there is no particle-particle interactions!!
#Python note: genfromtxt only makes a 2D array if all the elements are of the same type. Otherwise what I get is called a "structured ndarray". Makes it hard to concatenate and stuff, though it can still work with np.dstack.

#A.S. update - this "new" routine calculates it more elegantly, reading in line by line (instead of the whole thing at the beginning), and if one particle has a smaller array (due to it colliding and disappearing) this handles that and still calculates the energy, while the old algorithm would selfdestruct. And best of all, it works! Matches the straight up outputted values from swifter!

import glob
import numpy as np
import re
import matplotlib.pyplot as plt
import sys
import linecache

def get_data(files, iteration, eoffset_array):
    data = []
    eoffset = 0
    got_offset = 0
    N = 1   #sun exists
    for f in files:
        try:
            line = linecache.getline(f,iteration+1)
            split = line.split()
            if len(split) > 0:
                for i in xrange(0,len(split)):
                    split[i] = float(split[i])
                data.append(split)
                N += 1  #bodies still in simulation
            elif iteration > 0 and got_offset == 0:
                split = eoffset_array[iteration].split()
                eoffset = float(split[2])
                got_offset = 1
        except:
            print 'Error, file must not exist or something'
            exit(0)
    return data, eoffset, N

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

def h2b(data, m0, iteration, N_bodies, mtiny):  #heliocentric to barycentric
    com = np.zeros(7) #m,x,y,z,vx,vy,vz
    mass = np.zeros(N_bodies)
    mass[0] = m0
    com[0] = m0
    for i in xrange(0,N_bodies-1):
        m = data[i][8]
        mass[i+1] = m
        if m > mtiny:
            com[1] += m*data[i][2] #x
            com[2] += m*data[i][3] #y
            com[3] += m*data[i][4] #z
            com[4] += m*data[i][5] #vx
            com[5] += m*data[i][6] #vy
            com[6] += m*data[i][7] #vz
            com[0] += m
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
    for i in xrange(0,N_bodies-1):
        x[i+1] = data[i][2] + x[0]
        y[i+1] = data[i][3] + y[0]
        z[i+1] = data[i][4] + z[0]
        vx[i+1] = data[i][5] + vx[0]
        vy[i+1] = data[i][6] + vy[0]
        vz[i+1] = data[i][7] + vz[0]
    return mass, x, y, z, vx, vy, vz

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
files = files[1:]   #skip first file, it's empty (star)

default_mtiny = '1e-07'
input = raw_input('Enter Mtiny value (default, Msun=1, mtiny=1e-07): ')
if not input:
    mtiny = float(default_mtiny)
else:
    mtiny = float(input)

default_m0 = '1'
input = raw_input('Enter Suns mass (default Msun=1): ')
if not input:
    m0 = float(default_m0)
else:
    m0 = float(input)

#get masses of each body
#print 'get masses'
#m = get_mass(massdir,0)


#find number of outputs
f=open(dir+'energyoutput.txt')
eoffset_array = f.readlines()
N_output = len(eoffset_array)

#calc E of system at time 0
data, eoffset, N_bodies = get_data(files,0,eoffset_array)
dE = np.zeros(N_output)
time = np.zeros(N_output)
m,x,y,z,vx,vy,vz = h2b(data,m0,0,N_bodies,mtiny)
E0 = cal_energy(m,x,y,z,vx,vy,vz,N_bodies,mtiny)
print 'calculating energy'
increment = 0.1*N_output
for i in xrange(1,N_output):
    data, eoffset, N_bodies = get_data(files,i,eoffset_array)
    m,x,y,z,vx,vy,vz = h2b(data,m0,i,N_bodies,mtiny)
    E = cal_energy(m,x,y,z,vx,vy,vz,N_bodies,mtiny)
    dE[i] = np.fabs((E + eoffset - E0)/E0)
    time[i] = data[0][0]
    if i > increment:
        print '% done =',round(100*float(i)/float(N_output))
        increment += 0.1*N_output

plt.plot(time, dE, 'o')
plt.yscale('log')
plt.xscale('log')
plt.savefig(dir+'Energy_fromoutputnew.png')
plt.show()