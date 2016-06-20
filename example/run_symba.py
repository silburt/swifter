#A.S. Run symba but also keep time.
from subprocess import call
import time

#clean existing stuff
call("rm *.dat *.bin *.out *.txt *.png xyz_outputs/*.txt", shell=True)

default_mtiny = "1E-07"
mtiny = raw_input("Enter Mtiny value (default, Msun=1, mtiny=1E-07): ")
if not mtiny:
    mtiny = default_mtiny

args = ["./swifter_symba", "param.in", mtiny]
call(args)

