
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 20:50:40 2018

@author: agali
"""

"""
Este archivo tiene como objetivo crear tablas con 
100 ID de track con una configuración concreta y 
filtros concretos que se especifican más abajo y 
se guardan con los datos de la tabla
"""

import Scripts.CallTracking

headLess = True
dataOutPath = '..\\Data2'                     #poner la carpeta, TIENE QUE ESTAR CREADA
imgPath  = r"..\..\Videos\BacteriaWithMagneticField.tif" 
kalmanSearchRadius = 3.0
linkingMaxDistance = 8.0

callTracking(headLess,imgPath,dataOutPath,kalmanSearchRadius,linkingMaxDistance)






