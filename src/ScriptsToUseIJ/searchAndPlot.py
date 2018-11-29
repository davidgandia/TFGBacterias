# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 19:06:00 2018

@author: Gali
"""

from CallTracking import callTracking as ct
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#El objetivo es observar como varía el número de puntos en función del kalmanRadius. En concreto, ver cuantos tracks con solo dos puntos aparecen


headLess = True
dataOutPath = '..\Data\Data-29-10-2018'                     #poner la carpeta, TIENE QUE ESTAR CREADA
imgPath  = r"..\..\Videos\1-paralelo-1.tif" 
linkingMaxDistance = 8.0


#Compute the tracking for all the values of kalmanSearchRadius chosen below
kSRadiusMin = 2.0
kSRadiusMax = 8.0
n           = 15

kSRadius    = np.linspace(kSRadiusMin, kSRadiusMax,n)
directories = []
#Compute the Tracking
for i in range(n):
    #Adirectori is created unless it already exist one
    directory  = dataOutPath + "Data" + str(i)
    directories.append(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    print("\n Calling TM")
    ct(headLess,imgPath,directory,kSRadius[i],linkingMaxDistance)
    print("Success")

#read all the data and store it in df
df = pd.DataFrame()
for i in range(n):
    dfAux = pd.read_csv(directories[i]+r"\TrackFeatures.txt",sep = " ",header = 0,decimal=".")
    
    #NUMBER_SPOTS(NONE) is the only interesting variable
    s = dfAux["NUMBER_SPOTS(NONE)"]
    df[kSRadius[i]] = s

#filter all the data to get the number of tracks with less than 3 points
df = df[df==2].count()
fig = plt.plot(df, "bs",fillstyle='none')

