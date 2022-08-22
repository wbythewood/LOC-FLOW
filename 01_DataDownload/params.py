#!/usr/bin/env python
import os

# introduce a parameter file, to prevent inconsistency
label = "BayArea-Test"
BaseDir = "/Users/whawley/Research/Bangladesh/LOC-FLOW/"
DataDir = os.path.join(BaseDir,"Data",label)
if not os.path.exists(DataDir): os.mkdir(DataDir)

# time range for observations
year = 2018
month = 1 # integer month
day = 1 # integer day
nday = 7 # number of days to download data
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
