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


def dtwNormDist_Calc(x, y, D0, D1):
    r, c = len(x), len(y)
    #r, c = 5000, 5000

    for i in range(r):
        if (i%1000) == 0:
            print(i)
        for j in range(c):
            min_list = [D0[i, j]]
            for k in range(1, 2):
                i_k = min(i + k, r)
                j_k = min(j + k, c)
                min_list += [D0[i_k, j] * 1.0, D0[i, j_k] * 1.0]
            D1[i, j] += min(min_list)

    return D1[-1, -1]


def dtwCost_Calc(x, y):
    print("Length of mfcc1: " + str(len(x)))
    print("Length of mfcc2: " + str(len(y)))
    r, c = len(x), len(y)
    #r, c = 5000, 5000
    dist=lambda x, y: norm(x - y, ord=1)

    D0 = zeros((r + 1, c + 1))
    D0[0, 1:] = inf
    D0[1:, 0] = inf
    D1 = D0[1:, 1:]

    for i in range(r):
        if (i%1000) == 0:
            print(i)
        for j in range(c):
            D1[i, j] = dist(x[i], y[j])
    Cost = D1.copy()

    if len(x) == 1:
        Path = zeros(len(y)), range(len(y))
    elif len(y) == 1:
        Path = range(len(x)), zeros(len(x))
    else:       
        a, b = array(D0.shape) - 2
        p, q = [i], [j]
        while (a > 0) or (b > 0):
            tb = argmin((D0[a, b], D0[a, b + 1], D0[a + 1, b]))
            if tb == 0:
                a -= 1
                b -= 1
            elif tb == 1:
                a -= 1
            else:  # (tb == 2):
                b -= 1
            p.insert(0, a)
            q.insert(0, b)
        Path = array(p), array(q)
    return Cost, Path, D0, D1


def IntraApp_WavCreation(appName):
    main_directory = "New_Mem_Dumps/" + appName
    wav_list = []
    for folder in os.listdir(main_directory):
        print ("Main Directory:" + folder)
        sub_directory = main_directory + "/" + folder + "/bin"
        final_file = main_directory + "/" + folder + "/" + folder + ".final"
        final_wav = main_directory + "/" + folder + "/" + folder + ".wav"
        #final_graph = main_directory + "/" + folder + "/" + folder + ".png"
        #print(os.listdir(sub_directory))
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

        new_array = np.array(my_array, dtype=np.int16)

        sf.write(final_wav, new_array, 48000)
        print("Wave file is created")
        wav_list.append(final_wav)

        print("==================================================================================================")
    return(wav_list)


def librosaPlot_Intra(wav_list):
    print("***************************************************************************************************")
    main_wav = wav_list[0]
    print("Primary wave: " + main_wav)
    file_name_main = main_wav.rsplit('/', 1)[1].rsplit('.', 1)[0]
    wav_list.pop(0)

    for i in wav_list:
    
        secondary_wav = i
        print("Secondary wave: " + secondary_wav)
        file_name_sec = secondary_wav.rsplit('/', 1)[1].rsplit('.', 1)[0]
        start = timeit.default_timer()
        #Loading audio files
        y1, sr1 = librosa.load(main_wav) 
        y2, sr2 = librosa.load(secondary_wav) 
        stop = timeit.default_timer()
        print('wav load time: ', stop - start)
        
        mfcc1 = librosa.feature.mfcc(y=y1,sr=sr1)   #Computing MFCC values
        mfcc1_mel = librosa.feature.melspectrogram(y=y1,sr=sr1)
        mfcc1_mel_db = librosa.power_to_db(mfcc1_mel, ref=np.max)
        mfcc2 = librosa.feature.mfcc(y=y2, sr=sr2)
        mfcc2_mel = librosa.feature.melspectrogram(y=y2,sr=sr2)
        mfcc2_mel_db = librosa.power_to_db(mfcc2_mel, ref=np.max)
        
        
        start = timeit.default_timer()
        print("Calculating cost and path")
        cost, path, intArr1, intArr2 = dtwCost_Calc(mfcc1.T, mfcc2.T)
        print("Completed cost and path calculation")
        stop = timeit.default_timer()
        print('cost and path calculation Time: ', stop - start)

        
        start = timeit.default_timer()
        print("Calculating normalized distance")
        dist = dtwNormDist_Calc(mfcc1.T, mfcc2.T, intArr1, intArr2)
        print("The normalized distance between the two : ",dist)
        print("Completed distance calcuation")
        stop = timeit.default_timer()
        print('distance calcuation Time: ', stop - start)
    print("***************************************************************************************************")



def InterApp_WavCreation(appName1,appName2):
    main_directory_1 = "New_Mem_Dumps/" + appName1
    main_directory_2 = "New_Mem_Dumps/" + appName2

    main_directory_lst = []
    main_directory_lst.append(main_directory_1)
    main_directory_lst.append(main_directory_2)

    apps = {}
    apps_list = []

    for main_directory in main_directory_lst:
        wav_list = {}
        wav_files = []
        for folder in os.listdir(main_directory):
            print ("Main Directory:" + folder)
            sub_directory = main_directory + "/" + folder + "/bin"
            final_file = main_directory + "/" + folder + "/" + folder + ".final"
            final_wav = main_directory + "/" + folder + "/" + folder + ".wav"
            #final_graph = main_directory + "/" + folder + "/" + folder + ".png"
            print(os.listdir(sub_directory))
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

            new_array = np.array(my_array, dtype=np.int16)

            sf.write(final_wav, new_array, 48000)
            print("Wave file is created")
            wav_files.append(final_wav)

            #graphplot(final_wav,final_graph)
            print("==================================================================================================")
        wav_list['directory'] = main_directory
        wav_list['files'] = wav_files
        apps_list.append(wav_list)

    apps['apps'] = apps_list
    apps_str = json.dumps(apps)
    apps_json = json.loads(apps_str)
    #print(apps_json)
    return(apps_json)


def librosaPlot_Inter(apps_json):
    print("*************************************************************************")
    for i in apps_json['apps'][0]['files']:
        main_wav = i
        file_name_main = main_wav.rsplit('/', 1)[1].rsplit('.', 1)[0]
        print(file_name_main)
        for j in apps_json['apps'][1]['files']:
            secondary_wav = j
            file_name_sec = secondary_wav.rsplit('/', 1)[1].rsplit('.', 1)[0]
            print(file_name_sec)
            start = timeit.default_timer()
            #Loading audio files
            y1, sr1 = librosa.load(main_wav) 
            y2, sr2 = librosa.load(secondary_wav) 
            stop = timeit.default_timer()
            print('wav load time: ', stop - start)

            mfcc1 = librosa.feature.mfcc(y1,sr1)   #Computing MFCC values
            mfcc1_mel = librosa.feature.melspectrogram(y1, sr1)
            mfcc1_mel_db = librosa.power_to_db(mfcc1_mel, ref=np.max)
            img1 = librosa.display.specshow(mfcc1_mel_db, ax=ax, y_axis='mel', x_axis='time')
            
            mfcc2 = librosa.feature.mfcc(y2, sr2)
            mfcc2_mel = librosa.feature.melspectrogram(y2, sr2)
            mfcc2_mel_db = librosa.power_to_db(mfcc2_mel, ref=np.max)
            

            start = timeit.default_timer()
            print("Calculating cost and path")
            cost, path, intArr1, intArr2 = dtwCost_Calc(mfcc1.T, mfcc2.T)
            print("Completed cost and path calculation")
            stop = timeit.default_timer()
            print('cost and path calculation Time: ', stop - start)
            
            start = timeit.default_timer()
            print("Calculating normalized distance")
            dist = dtwNormDist_Calc(mfcc1.T, mfcc2.T, intArr1, intArr2)
            print("The normalized distance between the two : ",dist)
            print("Completed distance calcuation")
            stop = timeit.default_timer()
            print('distance calcuation Time: ', stop - start)
            
    print("*************************************************************************")


# Usage: python Librosa_Similarities.py Intra Fingerprint_App
# Usage: python Librosa_Similarities.py Inter Fingerprint_App RFID_App

# Var 1: Intra/Inter
# Var 2: App Name 1
# Var 3: App Name 2
# Var 4: wav file creation/ DTW Plot / Distance calc

# DTW plot requires all .wav files to be present
# Distance calc requires .wav files to be present

if __name__ == "__main__":
    compType = sys.argv[1]

    if compType == "Intra":
        appName = sys.argv[2]
        print("Application Name:" + appName)
        img_directory = "New_Mem_Dumps/Images/Intra/"
        wav_list = IntraApp_WavCreation(appName)
        librosaPlot_Intra(wav_list)
    elif compType == "Inter":
        appName1 = sys.argv[2]
        appName2 = sys.argv[3]
        print("Application 1 Name:" + appName1)
        print("Application 2 Name:" + appName2)
        img_directory = "New_Mem_Dumps/Images/Inter/"
        apps_json = InterApp_WavCreation(appName1,appName2)
        librosaPlot_Inter(apps_json)
    else:
        print("Invalid comparison type provided")
        exit(0)
	

	
