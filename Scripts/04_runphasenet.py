import warnings
import numpy as np
import pandas as pd
import shutil
import os
import sys
import params
from datetime import datetime

# new directory for picks... keep separate from sta/lta
picksDir = os.path.join(params.PicksDir,'PhaseNet/')
if not os.path.exists(picksDir): os.mkdir(picksDir)

#os.system('conda activate phasenet') 
#If you didn't install phasenet in your base environment,
#please manually do this in your command line

#see cookbook step 1b
#####################step 1 ####################
# run phasenet to generate pick file picks.csv
print("################\nrun PhaseNet\n###############")
# Remove the previous directory
#if os.path.isdir("results"):
#    shutil.rmtree("results")
command = "python "+params.BaseDir+"/src/PhaseNet/phasenet/predict.py --mode=pred --model_dir="+params.BaseDir+"/src/PhaseNet/model/190703-214543 --data_dir="+params.DataDir+"/waveform_sac --data_list="+params.DataDir+"/fname.csv --format=sac --highpass_filter=1 --amplitude"
print(command)
os.system(command)


#####################step 2####################
print("################\nseparate P and S picks\n###############")
# seperate the picks in picks.csv into p and s picks
pickfile = './results/picks.csv'
output1 = 'temp.p'
output2 = 'temp.s'
prob_threshold = 0.5
samplingrate = 0.01 #samplingrate of your data, default 100 hz

# initialize to keep track of dates to be used as directories...
dates = pd.Series()

f = open(output1,'w')
g = open(output2,'w')
data = pd.read_csv(pickfile, parse_dates=["begin_time", "phase_time"])
data = data[data["phase_score"] >= prob_threshold]

# new formatting to ensure two digit month and day
#data[["year", "mon", "day"]] = data["begin_time"].apply(lambda x: pd.Series([x.year, x.month, x.day]))
data[["year", "mon", "day"]] = data["begin_time"].apply(lambda x: pd.Series([x.year, "{:02d}".format(x.month), "{:02d}".format(x.day)]))
#data["ss"] = data["begin_time"].apply(lambda x: (x - datetime.fromisoformat(f"{x.year}-{x.month}-{x.day}")).total_seconds())
data["ss"] = data["begin_time"].apply(lambda x: (x - datetime.fromisoformat("{}-{:02d}-{:02d}".format(x.year,x.month,x.day))).total_seconds())

# get dates for folder names so we can move them...
dates["dates"] = data["begin_time"].apply(lambda x: ("{}{:02d}{:02d}".format(x.year,x.month,x.day)))
dates = dates["dates"].tolist() # turn from dataframe to list
dates = set(dates) # this keeps only unique values
dates = list(dates) # and this turns it back to a list

data[["net", "name", "channel"]] = data["station_id"].apply(lambda x: pd.Series(x.split(".")))
data["dum"] = pd.Series(np.ones(len(data)))
data["phase_amp"] = data["phase_amp"] * 2080 * 20
data["phase_time"] = data["ss"] + data["phase_index"] * samplingrate
data[data["phase_type"] == "P"].to_csv(output1, columns=["year", "mon", "day", "net", "name", "dum", "phase_time", "phase_score", "phase_amp"], index=False, header=False)
data[data["phase_type"] == "S"].to_csv(output2, columns=["year", "mon", "day", "net", "name", "dum", "phase_time", "phase_score", "phase_amp"], index=False, header=False)

#####################step 3####################
print("################\ncreat pick files by date and station name\n###############")
# separate picks based on date and station names
# the picks maybe not in order, it is fine and REAL
# will sort it by their arrival
command = "pick2real -Ptemp.p -Stemp.s &"
print(command)
os.system(command)


######### step 4 #########
# move folders to picks dir
for date in dates:
    newLoc = os.path.join(picksDir,date)
    if os.path.exists(date): 
        if os.path.exists(newLoc):
            # I'm getting permission errors with os.remove()...
            command = 'rm -r '+newLoc
            os.system(command)
        shutil.move(date,newLoc)
    else:
        print("No directory to move: "+date)
        continue
newResultsLoc = os.path.join(picksDir,'results')
if os.path.exists('results'):
    if os.path.exists(newResultsLoc):
        command = 'rm -r '+newResultsLoc
        os.system(command)
    shutil.move('results',newResultsLoc)
else:
    print("no results directory to move")

os.remove(output1) 
os.remove(output2) 
