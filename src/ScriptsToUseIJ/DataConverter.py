# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 12:18:22 2018

@author: agali
"""
"""NOT FINISHED

CRAR UN DF PARA TODOS LOS SPOTS


"""
import re
import pandas as pd
class Spot:
    ID = int()
    position_x = float()
    position_y = float()
    position_z = float()
    features = {}
    def __init__(self,features):
        #TODO añadir todas las features importantes
        self.ID = int(features.pop("ID"))
        self.position_x = float(features.pop("POSITION_X"))
        self.position_y = float(features.pop("POSITION_Y"))
        self.position_z = float(features.pop("POSITION_Z"))
        self.features = features
        
def createDictionary(features):
    """
    Creates a dictionary from a string array. The key an value must be separated by a = and the value must be surrounded by ""
    Example:ID="1092"
        key = ID
        value = 1092 (String)
    """
    featureDict = {}
    for feature in features:
        key = feature.split("=")[0]
        value = feature.split("=")[1]
        value = value[1:-1] #quitamos las comillas
        
        featureDict[key] = value
    return featureDict

        
fName = r"""C:\Users\agali\Desktop\Projects\TrackingBacteriasPython\src\PlottingAndCheckTracks\Data\Model.xml"""
with open(fName) as f: 
    spots = {}
    for line in f:
        m = re.match(r'.*<Spot (.*) />.*',line) 
        if m:
            features = m.group(1).split()#get the array string with the features
            features = createDictionary(features)#change it to a dictionary
            ID = features["ID"]
            spots[ID]= Spot(features)


            
