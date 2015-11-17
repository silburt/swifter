#A.S. Run symba but also keep time.
from subprocess import call
import time

#clean existing stuff
call("rm *.dat *.bin *.out", shell=True)

start_time = time.time()

default_mtiny = "1e-7"
mtiny = raw_input("Enter Mtiny value (default, Msun=1, mtiny=1e-7): ")
if not mtiny:
    mtiny = default_mtiny

args = ["./swifter_symba", "param.in", mtiny]
call(args)

elapsed_time = time.time() - start_time
print 'elapsed time =',elapsed_time
fos = open('elapsed_time.txt','w')
fos.write('elapsed time = '+str(elapsed_time))
