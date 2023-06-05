import os
import sys
import array
from pprint import pprint
import scipy.io.wavfile
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import wave, sys, struct
import librosa
import librosa.display
from dtw import *
from numpy.linalg import norm
import timeit
import json
#sys.stdout = open("C:\\Users\\vjman\\Downloads\\python_sine_wave_script\\Logs.log", "w")

from numpy import array, zeros, full, argmin, inf
#from scipy.spatial.distance import cdist
from math import isinf

#here, we supply a source directory where all the memdumps are located. The structure should be something like this

# memDumps
#  |_ [app-name]
#      |_ t0
#      |_ t1
#      |_ t2 ...

# where t0, t1, and t2, house the output from memfetch
# here, memDumps/[app-name] would be the source directory


def IntraApp_WavCreation(sourceDirectory, appName):
    wav_list = []
    count = 0;
    for folder in os.listdir(sourceDirectory):        
        sub_directory = sourceDirectory + "/" + folder 
        final_file = sourceDirectory + "/" + folder + "/" + appName + "-" + str(count) + ".final"
        final_wav = sourceDirectory + "/" + folder + "/" + appName + "-" + str(count) + ".wav"
        count = count + 1;
        filenames = []
        for file in os.listdir(sub_directory):
            if file.endswith(".bin"):
                file_name = sub_directory + "/" + file
                filenames.append(file_name)
                continue
            else:
                continue

        with open(final_file, "wb") as outfile:
            for fname in filenames:
                with open(fname, "rb") as infile:
                    for line in infile:
                        outfile.write(line)

        print("Concatenated final file created")
        f = open(final_file, "rb")
        my_array = bytearray(f.read())
        #print(my_array)

        new_array = np.array(my_array, dtype=np.int16)
        #print(new_array)

        sf.write(final_wav, new_array, 48000)
        print("Wave file is created")
        wav_list.append(final_wav)
        #print(final_wav)

        print("==================================================================================================")
    #print (wav_list)
    #print (sorted(wav_list))
    return(sorted(wav_list))





# Usage: python Librosa_Similarities.py Intra Fingerprint_App
#		 nohup python3 -u Librosa_Similarities.py Intra Weather_App > /home/ec2-user/Memory_Aquisition_Project/python_sine_wave_script/New_Mem_Dumps/Logs/Intra_Weather_App.log &
# Usage: python Librosa_Similarities.py Inter Fingerprint_App RFID_App
#		 nohup python3 -u Librosa_Similarities.py Inter FP_App_Benign FP_App_Infected > /home/ec2-user/Memory_Aquisition_Project/python_sine_wave_script/New_Mem_Dumps/Logs/Inter_FPAppBenign_FPAppInfected.log &

# Var 1: Intra/Inter
# Var 2: App Name 1
# Var 3: App Name 2
# Var 4: wav file creation/ DTW Plot / Distance calc

# DTW plot requires all .wav files to be present
# Distance calc requires .wav files to be present

if __name__ == "__main__":
    sourceFolder = sys.argv[1]
    appName = sys.argv[2]
    print("Application Name:" + appName)
    wav_list = IntraApp_WavCreation(sourceFolder, appName)

	

	
