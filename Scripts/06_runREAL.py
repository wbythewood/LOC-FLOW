import os
import sys
import params

# this code is to call the runREAL.pl code, but in such a way that you can use
# the python parameter file... slight modifications to the runREAL.pl code 
# were necessary.

# we require the user to make one choice not in the params file:
if len(sys.argv) != 2:
    print("This program will run the perl script in the REAL directory")
    print("Usage:")
    print(sys.argv[0]+" 0|1")
    print("0 for STA/LTA picks")
    print("1 for PhaseNet picks")
    sys.exit()

# save whether STALTA or Phasenet
SP = str(sys.argv[1])
# and where those files are stored...
if SP == "0":
    PicksDir = os.path.join(params.PicksDir,"STALTA/")
    AssocDir = os.path.join(params.AssocDir,"STALTA/")
elif SP == "1":
    PicksDir = os.path.join(params.PicksDir,"PhaseNet/")
    AssocDir = os.path.join(params.AssocDir,"PhaseNet/")
else:
    print("Unrecognized input.")
    print("This program will run the perl script in the REAL directory")
    print("Usage:")
    print(sys.argv[0]+" 0|1")
    print("0 for STA/LTA picks")
    print("1 for PhaseNet picks")
    sys.exit()

if not os.path.exists(AssocDir): os.mkdir(AssocDir)

# also needs time information
year = str(params.year)
month = str(params.month)
day = str(params.day)
nday = str(params.nday)

# the final call:
perlScript = os.path.join(params.BaseDir,"REAL/runREAL.pl")
command = "perl "+perlScript+" "+SP+" "+year+" "+month+" "+day+" "+nday+" "+str(params.LatCenter)+" "+params.ROption+" "+params.GOption+" "+params.VOption+" "+params.SOption+" "+PicksDir+" "+params.DataDir+" "+params.AssocDir
print(command)
os.system(command)

# now there are some files whose names are hardwired in the perl script... 
# let's keep the naming convention but move them to a new directory
# so we don't get confused

# filenames are:
# YYYYMMDD.catalog_sel.txt; YYYYMMDD.phase_sel.txt; YYYYMMDD..hypolocSA.dat;
# YYYYMMDD.hypophase.dat; phase_allday.txt; catalog_allday.txt; 
# catalogSA_allday.txt; phase_best_allday.txt


command = "mv *sel.txt *hypolocSA.dat *hypophase.dat *allday.txt "+AssocDir
#print(command)
os.system(command)
