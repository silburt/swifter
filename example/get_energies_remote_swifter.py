#A.S. This collects the energies from rein005 and puts them in the local directory fast. Calcs the energy too.
import paramiko
import time
import subprocess
import os
import numpy as np
import matplotlib.pyplot as plt
from subprocess import call

get_files = ['energyoutput.txt','elapsed_time.txt','removedparticles.txt']

default_erase = 0
erase = raw_input("Erase local directories (default = 0)?: ")
if not erase:
    erase = default_erase
erase = int(erase)
if erase == 1: #erase every single directory
    call('rm -rf input_files/*', shell=True)

default_calcE = 0
calcE = raw_input("Calculate Energies (0=no, 1=yes, default=no)?: ")
if not calcE:
    calcE = default_calcE
calcE = int(calcE)

hostname = 'rein005.utsc.utoronto.ca'
password = 'ZAIfkUIK'
username = 'silburt'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)
(stdin, stdout, stderr) = ssh.exec_command('ls ../../../data_local/silburt/swifter/example/input_files')
d = stdout.readlines()
length = len(d)

for i in xrange(0,length):
    dir = d[i].split("\n")
    exist = os.path.isdir('input_files/'+dir[0])
    if exist == 0:
        call('mkdir input_files/'+dir[0], shell=True)
    for j in xrange(0,len(get_files)):
        localpath='input_files/'+dir[0]+'/'+get_files[j]
        remotepath='../../../data_local/silburt/swifter/example/input_files/'+dir[0]+'/'+get_files[j]
        t = paramiko.Transport((hostname, 22))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(remotepath, localpath)
    if calcE == 1:
        f = open('input_files/'+dir[0]+'/'+get_files[0])
        lines=list(f)
        N = len(lines)
        dE = np.zeros(N)
        t = np.zeros(N)
        for k in xrange(1,N):
            temp = lines[k]
            temp2 = temp.split()
            t[k] = float(temp2[0])
            dE[k] = float(temp2[1])
        plt.plot(t,dE,'o')
        plt.yscale('log')
        plt.xscale('log')
        output = 'input_files/'+dir[0]+'/Energy.png'
        plt.savefig(output)
        plt.clf()
    print 'completed iteration '+str(i)+' of '+str(length)

