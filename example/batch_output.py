#A.S. Program to call tool_follow and output all the planet/particle data and put it into follow/

from subprocess import call

unpack = raw_input("unpack out.bin and move to output/ folder (rm *.txt that folder)? (yes = 1, no = 0): ")
if int(unpack) == 1:
    N = raw_input("Number of bodies to track: ")
    N = int(N)
    for i in xrange(1,N+1):
        args = ["./tool_follow", "param.in", str(i),"1",str(i)]
        call(args)

call("rm output/*.txt", shell = True)
call("mv *.txt output/.", shell = True)
