#A.S. Run symba but also keep time.
from subprocess import call
import time

#clean existing stuff
call("rm *.dat *.bin", shell=True)

start_time = time.time()

args = ["./swifter_symba", "param.in", "0.005"]
call(args)

elapsed_time = time.time() - start_time
print 'elapsed time =',elapsed_time
fos = open('elapsed_time.txt','w')
fos.write('elapsed time = '+str(elapsed_time))
