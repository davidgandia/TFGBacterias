# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 17:50:25 2018

@author: agali
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.stats import knuth_bin_width
import pandas as pd
import random as rd
import time 
import ScriptsToUseIJ.CallTracking as CT
import math

def openAndFilterTracks(dataPath):
    """Function that creates a dataframe from a file of trackmate and returns the data frame filtered in the number of spots an the std quality"""
    df = pd.read_csv(dataPath,sep = " ",header = 0,decimal=".")

    #Filtros que se van a realizar sobre los datos obtenidos
    df = df[df["NUMBER_SPOTS(NONE)"]>7] #filtrar el numero de puntos minimo 
    df = df[df["TRACK_STD_QUALITY(QUALITY)"]<10]#pedir que el desvio en la calidad sea menor que 10(valor escogido un poco aleatoriamente)
    #TODO  meter filtro en función del error relativo de la velocidad?
        
    return df

def changeTimeToFrame(period,dataFrame):
    """Cambia TrackStartTime y TrackStopTime. En vez de representar su valor en segundos, representan un índice en referencia al frame en el que empiezan/acaban los tracks"""
    s = round(dataFrame["TRACK_STOP(TIME)"]/period)
    dataFrame["TRACK_STOP(TIME)"] = s.astype(int)
    
    s = round(dataFrame["TRACK_START(TIME)"]/period)
    dataFrame["TRACK_START(TIME)"]  = s.astype(int)
    
    return dataFrame

def computeFractionDeadAlive(df):
    """El objetivo es hacer una estimación del numero de bacterias muertas o sin flagelo. Observando los datos del análisis de la velocidad, se ha obtenido que existe un gran grupo de bacterias que se mueven a una velocidad menor a 10 mus. Estas bacterias o bien estan muertas o no tienen flagelos que puedan usar para desplazarse. Sabiendo que este grupo de bacterias representa en parte a las bacterias muertas o sin flagelos, se va a intentar hacer una estimación de a fracción de bacterias muertas. El conteo se realizara haciendo un valor medio de la fracción de bacterias con menos de 10 mu/s de vlocidad y bacterias con más de 10mu/s de velocidad."""

    df = changeTimeToFrame(0.13334096,df)
    
    nIter = df["TRACK_STOP(TIME)"].max() +1 #number of iterations in the following process. It is actually the last frame number
    
    #Create an array to store the results
    fractionDeadAlive = np.zeros(nIter)
    
    #iterate over all the frames
    for i in range(nIter):
        #Select the tracks that exist in the given frame i
        mask1 = df["TRACK_START(TIME)"] <= i
        mask2 = df["TRACK_STOP(TIME)"] >= i
        
        #diferenciate beetwen the tracks that have a mean velocity greater than or less than 10um/s     
        velLT = df["TRACK_MEAN_SPEED(VELOCITY)"] <= 10.0
        velGT = df["TRACK_MEAN_SPEED(VELOCITY)"] > 10.0
        
        #Count the Tracks and do the fraction. Use bitwise logic operation. "and" operator does not work.
        
        TracksGT = velGT &  mask1  & mask2
        nTracksGT = TracksGT.sum()
        
        TracksLT = velLT &  mask1  & mask2
        nTracksLT = TracksLT.sum()
        
        
        fractionDeadAlive[i] =  nTracksLT/(nTracksGT+nTracksLT)
        
# =============================================================================
#         print(" \n frame = {} \n nTracks GT = {} \n nTracksLT = {} \n fraction = {}".format(i,nTracksGT,nTracksLT,fractionDeadAlive[i]))
# =============================================================================
    fractionDeadAlive = fractionDeadAlive[10:] #the first 10 data are deleted due to the fact that they do not provide "correct" data
    return fractionDeadAlive
    #plot the data of fractionDeadAlive and its mean value
   # plt.plot(range(fractionDeadAlive.size),fractionDeadAlive,np.ones(fractionDeadAlive.size)*fractionDeadAlive.mean())
    
        
if __name__ == "__main__":
    dataPath = ".\Data\TrackFeatures.txt" #se ha usado uno provisional. El mismo con el que se ha hecho la comprovación de la precisión del tracking
    df = openAndFilterTracks(dataPath)
    fDA = computeFractionDeadAlive(df)
    plt.plot(range(fDA.size),fDA,np.ones(fDA.size)*fDA.mean())
    print("\n fDA = {} \n error = {}".format(fDA.mean(),fDA.std())) #std o std/sqrt(n)
