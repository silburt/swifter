#A.S. This clean's the directory, recompiles the directory, and then runs mercury, keeping time in the process.
import multiprocessing as mp
from subprocess import call
import time
import os

def execute(dir):
    MTINY = "1E-07"             #This mass distinguishes massive from test bodies. 
    call('cp ../bin/swifter_symba '+dir+'/.',shell=True)
    call('cp ../bin/tool_follow '+dir+'/.',shell=True)
    call('cp batch_output.py '+dir+'/.',shell=True)
    os.chdir(dir)
    call('rm *.dat *.bin *.out *.txt', shell=True)
    fos = open('elapsed_time.txt','a')
    fos.write('start time = '+str(time.time())+'\n')
    args = ["./swifter_symba", "param.in", MTINY]
    call(args)
    fos = open('elapsed_time.txt','a')
    fos.write('finish time = '+str(time.time()))

if __name__== '__main__':
    files = [x[0] for x in os.walk('input_files')]
    files=files[1:]
    N_procs = 1
    pool = mp.Pool(processes=N_procs)
    args=[files[i] for i in xrange(0,len(files))]
    pool.map(execute, args)
    pool.close()
    pool.join()
