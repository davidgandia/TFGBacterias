# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 13:41:55 2018

@author: Gali
"""
import numpy as np
import matplotlib.pyplot as plt
from astropy.stats import knuth_bin_width
import pandas as pd
import random as rd
import time 
#This is an example of hoe to plot the data obtained in the tracking < >

np.random.seed(1)#siempre el mismo randompara que sea repetible
def plotHistWithKnuth(data,axes):
    #Obtain the bins using an specific method
    dx, bins = knuth_bin_width(data, return_bins=True)

    #Plot the bins
    axes.hist(data, bins,density = True)
    axes.text(0.95, 0.1, 'Numer of tracks = ' + str(data.count()),verticalalignment='bottom', 
                horizontalalignment='right',transform=axes.transAxes,  fontsize=13)
    axes.set_xlabel(data.name)
    axes.grid()
    #Change axes name (It can be used Tex language)
    axes.set_ylabel('Number of tracks normalized')
    
    
    
#Reading the file
filePath = r"..\..\Data\Data2\TrackFeatures.txt" 
df = pd.read_csv(filePath,sep = " ",header = 0,decimal=".")

#Obtain the axes
fig, ax = plt.subplots(1)
#ax.set_title(r'Histogram of the velocity of the bacteria')




df = df[df["NUMBER_SPOTS(NONE)"]>7] #filtrar el numero de puntos minimo 
# =============================================================================
# 
# plotHistWithKnuth(df["TRACK_STD_QUALITY(QUALITY)"],ax[1])
# plotHistWithKnuth(df["TRACK_MEAN_QUALITY(QUALITY)"],ax[0])
# 
# plotHistWithKnuth(df["TRACK_MEAN_SPEED(VELOCITY)"],ax)
# =============================================================================

df = df[df["TRACK_STD_QUALITY(QUALITY)"]<10]
plotHistWithKnuth(df["TRACK_MEAN_SPEED(VELOCITY)"],ax)

# =============================================================================
# 
# plotHistWithKnuth(df[df["NUMBER_SPOTS(NONE)"]>7]["TRACK_MEAN_SPEED(VELOCITY)"],ax)
# =============================================================================


#Rapidamente comprueba las diferencias en cada histograma posible mostrando los 
#graficos correspondientes en pantalla(Quitar comentarios para mostrar)
dfMin = df[df["TRACK_MEAN_SPEED(VELOCITY)"]<10]
dfMax = df[df["TRACK_MEAN_SPEED(VELOCITY)"]>10]
# =============================================================================
# for k in df.keys():
#     fig,ax = plt.subplots(1,2)
#     plotHistWithKnuth(dfMin[k],ax[0])
#     plotHistWithKnuth(dfMax[k],ax[1])
# 
# =============================================================================
############
#Selecciona un numero aleatorio de Track ID y guardalos es un cvs Para poder
# analizar los tracks en cuestion. Se guardaran dos archivos, uno con v menor a 10 y
#otro con v mayor a 10.
############

#Cuenta el numero de Track tras los filtros con v mayor o menor que 10

nTrMayor = dfMax.iloc[:,1].count()
nTrMenor = dfMin.iloc[:,1].count()

randomTrackIDProviderMayor = (np.random.permutation(np.arange(nTrMayor))[:100])
randomTrackIDProviderMayor.sort()
randomTrackIDProviderMenor = (np.random.permutation(np.arange(nTrMenor))[:100])
randomTrackIDProviderMenor.sort()

trackIDMayor = dfMax.index[randomTrackIDProviderMayor] #El cero es para que coja bien el array
trackIDMenor = dfMin.index[randomTrackIDProviderMenor]

#Pasamos a una dataframe para guardarlo
dfTracksToAnalize = pd.DataFrame({"TRACK_SPEED_GT_10MUS" : trackIDMayor})
dfTracksToAnalize["TRACK_SPEED_LT_10MUS"] = trackIDMenor

dfTracksToAnalize.to_csv(r".\CheckTracks"+ time.strftime("%d-%m-%y") +".csv",sep = "\t")
