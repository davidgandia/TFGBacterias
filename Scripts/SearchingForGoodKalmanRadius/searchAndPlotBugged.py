# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 19:06:00 2018

@author: Gali
"""

from Scripts import CallTracking  



#El objetivo primero es observar como varía el número de puntos en función del kalmanRadius

headLess = True
dataOutPath = '..\\Data2\\'                     #poner la carpeta, TIENE QUE ESTAR CREADA
imgPath  = r"..\..\Videos\1-paralelo-1.tif" 
kalmanSearchRadius = 3.0
linkingMaxDistance = 8.0

callTracking(headLess,imgPath,dataOutPath,kalmanSearchRadius,linkingMaxDistance)

