# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 13:41:55 2018

@author: Gali
"""
import numpy as np
import matplotlib.pyplot as plt
from astropy.stats import knuth_bin_width
import pandas as pd
import time 
import ScriptsToUseIJ.CallTracking as CT

def plotHistWithKnuth(data,axis,x_label=""):
    from scipy.stats import norm
    """ 
    This is a funtion that helps with the ploting of the data. 
    data: data to be plotted. It must be a Series of pd
    axis: axis instanco of marplotlib
    x_label: the label to put in the x axis. default is "" but that means that it takes the name of the series. 
    """
    #Obtain the bins using an specific method
    dx, bins = knuth_bin_width(data, return_bins=True)

    #Plot the bins
    axis.hist(data, bins,density = True)
    #Obtain the gaussian distribution that fits best the bins.
    mu,sigma = norm.fit(data)
    x = np.linspace(round(data.min()),round(data.max()),100)#points to draw
    y = norm.pdf(x,mu,sigma)#value of gaussian dist in those points
    axis.plot(x,y, 'r--', linewidth=2)#plot
    
    #print some valuable info
    axis.text(1.0, 1.15, 'Número total de trayectorias = ' + str(data.count()),verticalalignment='top', 
                horizontalalignment='right',transform=axis.transAxes,  fontsize=20)
    
    axis.text(1.0, 0.9, '$\mu =${0:.3f} \n $\sigma =${1:.3f}'.format(mu,sigma),verticalalignment='top', 
                horizontalalignment='right',transform=axis.transAxes,  fontsize=20)
    #Change axis name or set the default name, the name of the data series
    if not len(x_label):
        axis.set_xlabel(data.name)
    else:
        axis.set_xlabel(x_label)
    axis.grid()
    
    axis.set_ylabel('Número de trayectorias (normalizado)')

def openAndFilterTracks(dataPath):
    """Function that creates a dataframe from a file of trackmate and returns the data frame filtered in the number of spots an the std quality"""
    """"""
    df = pd.read_csv(dataPath,sep = " ",header = 0,decimal=".")

    #Filtros que se van a realizar sobre los datos obtenidos
    df = df[df["NUMBER_SPOTS(NONE)"]>7] #filtrar el numero de puntos minimo 
    df = df[df["TRACK_STD_QUALITY(QUALITY)"]<10]#pedir que el desvio en la calidad sea menor que 10(valor escogido un poco aleatoriamente)
    #TODO  meter filtro en función del error relativo de la velocidad?
        
    return df

def main():
    #This is an example of how to plot the data obtained in the tracking 
    
    #Some variables to modify
    kalmanSearchRadius = 3.0
    linkingMaxDistance = 8.0
    imgPath   =  r"..\..\Videos\BacteriaWithMagneticField.tif" #image to analize
    dataPath =  r'.\Data' #The folder must already exist
    headLess = True
    

    #Start of the code
    ask = input("Do you want to do the full Tracking? [y/n]\n ")
    if ask.lower() in "yes":
        dataOutPath = dataPath                     #poner la carpeta, TIENE QUE ESTAR CREADA
        CT.callTracking(headLess,imgPath,dataOutPath,kalmanSearchRadius,linkingMaxDistance)
        
        
            
        
        
    #Reading the file
    filePath = "{0}\TrackFeatures.txt".format(dataPath) #a data file of tracks containing the       track made to the 
    
    df = openAndFilterTracks(filePath)
        
    #Obtain the axis and plot
    fig, ax = plt.subplots(1)
    plotHistWithKnuth(df["TRACK_MEAN_SPEED(VELOCITY)"],ax)
        
        
    #Rapidamente comprueba las diferencias en cada histograma posible   mostrando los 
    #graficos correspondientes en pantalla(Quitar comentarios para  mostrar)
    dfMin = df[df["TRACK_MEAN_SPEED(VELOCITY)"]<10]
    dfMax = df[df["TRACK_MEAN_SPEED(VELOCITY)"]>10]
    
    keys = df.keys()
    for k in keys:
        #TODO dejar mas espacio entre los graficos.
        fig,ax = plt.subplots(1,2)
        plotHistWithKnuth(dfMin[k],ax[0])
        plotHistWithKnuth(dfMax[k],ax[1])
        
        
        
            
    ############
    #Selecciona un numero aleatorio de Track ID y guardalos es un   cvs Para poder
    # analizar los tracks en cuestion. Se guardaran dos archivos,   uno con v menor a 10 
    #otro con v mayor a 10.
    ############
    
    #Cuenta el numero de Track tras los filtros con v mayor o   menor que 10

    np.random.seed(1)#siempre el mismo random para que sea  repetible
                
    nTrMayor = dfMax.iloc[:,1].count()
    nTrMenor = dfMin.iloc[:,1].count()
    

    #Creo un par de arrays aleatorios permutados y cojo 100 elementos que serán los que analize. Luego los ordeno.
    randomTrackIDProviderMayor =(np.random.permutation(np.arange(nTrMayor)))[:100] 
    randomTrackIDProviderMayor.sort()
    randomTrackIDProviderMenor =(np.random.permutation(np.arange(nTrMenor)))[:100]
    randomTrackIDProviderMenor.sort()
        
    trackIDMayor = dfMax.index[randomTrackIDProviderMayor]  #El cero es para que coja bien el array
    trackIDMenor = dfMin.index[randomTrackIDProviderMenor]
                                        
    #Pasamos a una dataframe para guardarlo
    dfTracksToAnalize = pd.DataFrame({"TRACK_SPEED_GT_10MUS"    : trackIDMayor})
    dfTracksToAnalize["TRACK_SPEED_LT_10MUS"] = trackIDMenor
            
    dfTracksToAnalize.to_csv(r".\Data\CheckTracks"+     time.strftime("%d-%m-%y") +".txt",sep = "\t")

                                    
                                        
if __name__ == "__main__":
# =============================================================================
#     main()
# =============================================================================
    #algunos ejemplos de llamadas a las funciones (deben existir dfMin y dfMax)
    fig,ax = plt.subplots()
    plotHistWithKnuth(dfMin["TRACK_MEAN_SPEED(VELOCITY)"],ax,r"Velocidad ($\frac{\mu m}{s}$)")
    fig,ax = plt.subplots()
    plotHistWithKnuth(dfMax["TRACK_MEAN_SPEED(VELOCITY)"],ax,r"Velocidad ($\frac{\mu m}{s}$)")
