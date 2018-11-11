# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 14:26:50 2018

@author: Gali
"""

#Function to call trackmate. Headless-- True -->not initialize imageJ 
def callTracking(headLess,imgPath,dataOutPath, kalmanSearchRadius,linkingMaxDistance , ijPath=r"resources\Fiji.app\ImageJ-win64.exe"):
    from subprocess import call,PIPE,check_output
    args =[ijPath]
    args.append("--ij2")
    #TODO control mas estricto de esto
    if headLess:
        args.extend(["--headless", "--console"])
    args.extend(["--run", "resources\\Tracking.py"])
    args.append(("headLess=\'{}\'," +
                "imgPath=\'{}\',"+ 
                "dataOutPath=\'{}\'," +
                "kalmanSearchRadius=\'{}\'," + 
                "linkingMaxDistance=\'{}\'").format(str(headLess)
                                                    ,imgPath
                                                    ,dataOutPath
                                                    ,str(kalmanSearchRadius)
                                                    ,str(linkingMaxDistance)
                                                    )
                )    
    call(args)

    return None
#Function to call a macro which makes the first step in the image processing before calling the tracking processing . Headless-- True -->not initialize imageJ 
def callProcesado(headLess, imagePath,imageOutPath, ijPath=r"resources\Fiji.app\ImageJ-win64.exe"):
    from subprocess import call
    args =[ijPath]
    args.append("--ij2")
    #TODO control mas estricto de esto
    if headLess:
        args.extend(["--headless", "--console"])
    args.extend(["--run",r"resources\ProcessImage.ijm"])
    args.append("imagePath="+"'" + imagePath+"'" +"," +
                "imageOutPath="+"'" + imageOutPath+"'" )    
    call(args)
    return None

def callChecking(modelPath, ijPath="resources\\Fiji.app\\ImageJ-win64.exe"):
    from subprocess import call
    args =[ijPath]
    args.append("--ij2")
    args.extend(["--run",r"CheckingTracks\Check.py"])
    args.append("modelPath="+"'" + modelPath+"'" )    
    call(args)
    return None
#Controles Ejecucion
headLess = True
dataOutPath = '..\\Data2'                     #poner la carpeta, TIENE QUE ESTAR CREADA
imgPath  = r"..\..\Videos\BacteriaWithMagneticField.tif" 
kalmanSearchRadius = 3.0
linkingMaxDistance = 8.0

callTracking(headLess,imgPath,dataOutPath,kalmanSearchRadius,linkingMaxDistance)






