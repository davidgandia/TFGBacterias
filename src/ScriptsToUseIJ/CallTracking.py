# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 14:26:50 2018

@author: Gali
"""
"""Varias funciones que conectan Pyhton con ImageJ. Lo hacen llamando a ImgaJ desde la consola"""
#Function to call trackmate. Headless-- True -->not initialize imageJ 
def callTracking(headLess,imgPath,dataOutPath, kalmanSearchRadius,linkingMaxDistance , ijPath=r"..\..\Fiji.app\ImageJ-win64.exe"):
    """Llama a imageJ para realizar el tracking del video seleccionado.
        headless: Booolean que sirve para especificar si quieres que se ejecute la gui de imageJ
        imgPath: String con la direccion en la que se encuentra la imagen ha trackear
        dataOutPath: String con la direccion de la carpeta dode se guardan los resultados. SE SOBREESCRIBEN Y LA CARPETA DEBE ESTAR CREADA DE ANTEMANO
        kalmanSearchRadius: Double parametro del tracking
        linkingMaxDistance: Double parametro del tracking
        ijPath: String con la direccion del programa .exe de ImageJ. Si se ha copiado correctamente el proyecto desde Github,no debería modificarse.
    """
    from subprocess import call
    args =[ijPath]
    args.append("--ij2")
    #TODO control mas estricto de esto
    if headLess:
        args.extend(["--headless", "--console"])
    args.extend(["--run", r"..\ScriptsToUseInIJ\Tracking.py"])
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
    print(args)
    call(args)

    return None
#Function to call a macro which makes the first step in the image processing before calling the tracking processing . Headless-- True -->not initialize imageJ 
def callProcesado(headLess, imagePath,imageOutPath, ijPath=r"..\..\Fiji.app\ImageJ-win64.exe"):
    """Falta por comprobar si funciona correctamente"""
    from subprocess import call
    args =[ijPath]
    args.append("--ij2")
    #TODO control mas estricto de esto
    if headLess:
        args.extend(["--headless", "--console"])
    args.extend(["--run",r"..\ScriptsToUseInIJ\Tracking.py"])
    args.append("imagePath="+"'" + imagePath+"'" +"," +
                "imageOutPath="+"'" + imageOutPath+"'" )  
    call(args)
    return None

def callChecking(modelPath, ijPath=r"..\..\Fiji.app\ImageJ-win64.exe"):
    """En desarrollo, no usar"""
    from subprocess import call
    args =[ijPath]
    args.append("--ij2")
    args.extend(["--run",r"..\CheckingTracks\Check.py"])
    args.append("modelPath="+"'" + modelPath+"'" )    
    call(args)
    return None
def _example():
    """Ejemplo de uso de la llamada a callTracking"""
    #Ejemplo de como usar la llamada a calltracking
    headLess = True
    dataOutPath = r'..\..\Data\Data2'                     #poner la carpeta, TIENE QUE ESTAR CREADA
    imgPath  = r"..\..\Videos\BacteriaWithMagneticField.tif" 
    kalmanSearchRadius = 3.0
    linkingMaxDistance = 8.0
    callTracking(headLess,imgPath,dataOutPath,kalmanSearchRadius,linkingMaxDistance)
    """
    Todavia falta por comprobar con la aplicación directamente pero 
    el numero de Spots detectados para la imagen seleccionada debería ser Spots = 28846
    y el numero de Tracks = 2959
    """
if __name__ == "__main__":
    _example()



