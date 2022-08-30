#!/usr/bin/env python
import os

# introduce a parameter file, to prevent inconsistency
label = "BayArea-Test"
VelModelName = "mymodel.nd" # name of velocity model you will use fot association

BaseDir = "/Users/whawley/Research/Bangladesh/LOC-FLOW/"
DataDir = os.path.join(BaseDir,"Data",label)
if not os.path.exists(os.path.join(BaseDir,'Data/')): os.mkdir(os.path.join(BaseDir,'Data/'))
if not os.path.exists(DataDir): os.mkdir(DataDir)
PicksDir = os.path.join(BaseDir,"Picks",label)
if not os.path.exists(os.path.join(BaseDir,'Picks/')): os.mkdir(os.path.join(BaseDir,'Picks/'))
if not os.path.exists(PicksDir): os.mkdir(PicksDir)
AssocDir = os.path.join(BaseDir,"Associate",label)
if not os.path.exists(os.path.join(BaseDir,'Associate/')): os.mkdir(os.path.join(BaseDir,'Associate/'))
if not os.path.exists(AssocDir): os.mkdir(AssocDir)

VelDir = os.path.join(BaseDir,"VelocityModels")
VelModel = os.path.join(VelDir,VelModelName)

# time range for observations
year = 2018
month = 1 # integer month
day = 1 # integer day
nday = 1 # number of days to download data
tstart = 0 # in seconds
tend = 86400 # in seconds, 86400 is full day

# seismic data info
sampleRate = 100 # resample to this rate, in Hz
network = None # Enter None for all networks, not "" 
channels = ["HH?","EH?"]

ThreeComp = 1 # 1: use three components E/N/Z for phasenet_input
              # 0: use E/N/Z, E/Z, N/Z, Z
              # It is fine to use either one before the dt.cc calculation.
              # NOTE: FDTCC use ENZ only by default. 
              #       Want to use Z alone? change E and N to Z in FDTCC.c.

#####################
# Area of interest -- can choose either circle or rectangle
AreaType = "C" # choose "C" for circular; "R" for rectangular
if AreaType != "C" and AreaType != "R":
    print("AreaType must be either \"C\" or \"R\", not "+AreaType)
    print("Please fix this in params.py")
    sys.exit()

# for circular (technically annular but whatever)
LatCirc = 37.8 #42.75
LonCirc = -122.2 #13.25
MinRadius = 0 # km
MaxRadius = 60 # in km

# for rectangular
MinLat = 37.3
MaxLat = 38.2
MinLon = -122.6
MaxLon = -121.6
#####################

#####################
# Parameters for association
Dist = 1.4 # dist range in degrees
dDist = 0.01 # distance interval, Dist should be exactly divisible by this
Depth = 20 # depth in km
dDepth = 1 # depth interval; Depth should be exactly divisible by this

# parameters for runREAL.py
# god this perl code has so much hard-wired shit, I hope I get everything here...
if AreaType == "C":
    LatCenter = LatCirc
elif AreaType == "R":
    LatCenter = MaxLat - (MaxLat-MinLat)
else:
    print("AreaType may only be \"C\" or \"R\".") # should already be cleared
    sys.exit()

# Grid definitions
ROption = "1.0/20/0.2/2/5" # rx/rh/tdx/tdh/tdint[/gap/gcarc0/latref0/lonref0]
GOption = "1.4/20/0.01/1" # [trx/trh/tdx/tdh]
VOption = "6.2/3.4" # vp0/vs0[/s_vp0/s_vs0/ielv]
SOption = "3/2/8/2/0.5/0.1/1.2/0.0" # np0/ns0/nps0/npsboth0/std0/dtps/nrt[/drt/nxd/rsel/ires]

#rx = horizontal search range in degrees, centered at station with first phase
#rh = depth range for search in km
#tdx = grid size for horizontal search, in degrees
#tdh = grid size for depth search in km
#tint = two events cannot occur within this time of each other, keep most 
        # reliable of multiple observations
#gap = only keep events within this station gap
#gcarc0 = only keep picks within this distance in degrees
#latref0 = refrence latitude
#lonref = reference longitude

#trx = horizontal range in traveltime table (degree)
#trh = vertical range in traveltime table (km)
#tdx = horizontal gird size (degree)
#tdh = vertical grid size (km)

#vp0 = average p vel
#vs0 = average s vel
#s_vp0 = shallow p velocity
#s_cs0 = shallow s velocity
#ielev = station elevation correction... i think binary, 1 means you use 
         # the shallow velocities above? not sure about this...

#np0 = threshold for number of p picks
#ns0 = threshold for number of s picks
#nps0 = threshold for total number of picks
#npsboth0 = number of stations that record both p and s picks
#std0 = standard deviation threshold
#dps = time threshold for S and P separation
#nrt = scalar to multiply by default time window--use larger values for less accurate velocity models
#drt = remove associated picks shorter than drt*p_window from the pool
#nxd = suspicious events within nxd*gcarc0 of the nearest station will be discarded
#rsel = tolerance multiplier; keeps picks with residuals less than rsel*std
#ires = 0, don't output resolution // = 1 do output resolution
