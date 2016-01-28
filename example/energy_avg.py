#This macro calculates the average energy for a collection of runs in energy_avg/ to average out the noise.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cmx
import matplotlib.colors as colors
import os
import sys

def get_cmap(N):
    '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct
        RGB color.'''
    color_norm  = colors.Normalize(vmin=0, vmax=N-1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv')
    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    return map_index_to_rgb_color

N_planetesimals = raw_input("Enter # planetesimals for runs you wish to average: ")

files = [x[0] for x in os.walk('input_files/')]
files = files[1:]
N_files = 0

print 'reading in data'
data = []
for f in files:
    split = f.split("/")
    split2 = split[1].split("_")
    if split2[0] == 'Np'+N_planetesimals:
        try:
            ff = open(f+'/energyoutput.txt', 'r')
            lines = ff.readlines()
            data.append(lines)
            N_files += 1
            print 'iteration complete'
        except:
            print 'couldnt read in data file '+f+'/energyoutput.txt'

n_it = len(data[0])
E = np.zeros(shape=(N_files,n_it))
Eavg = np.zeros(n_it)
time = np.zeros(n_it)
vals_for_med = np.zeros(N_files)

print 'calculating avg energy'
for i in xrange(1,n_it):
    for j in range(0,N_files):
        E0split = data[j][0].split()
        E0 = float(E0split[1])
        split = data[j][i].split()
        vals_for_med[j] = abs((E0 - float(split[1]) - float(split[2]))/E0)
        E[j][i] = vals_for_med[j]
    Eavg[i] = np.median(vals_for_med)
    time[i] = float(split[0])

cmap = get_cmap(N_files)
for i in xrange(0,N_files):
    plt.plot(time,E[i], ms=0.5, color=cmap(i), alpha=0.75)
plt.plot(time, Eavg, 'o', markeredgecolor='none', color='black', label='Averaged curve')
plt.plot(time,3e-10*time**(0.5),color='black',label='t^1/2 growth')
plt.legend(loc='upper left',prop={'size':10})
plt.ylabel('Avg Energy')
plt.xlabel('time (years)')
plt.yscale('log')
plt.xscale('log')
plt.xlim([0.5,time[-1]])
plt.title('Median Average dE/E(0) from '+str(N_files)+' runs for Np'+N_planetesimals)
plt.savefig('input_files/energy_avg_Np'+N_planetesimals+'.png')
plt.show()