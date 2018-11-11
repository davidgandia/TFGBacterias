"""
Created on Mon Oct 22 22:13:36 2018

@author: Gali
"""

#@String (label = "PathForTheModel") modelPath

from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import TrackMate
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate import Logger
from java.io import File
from ij import IJ
import sys

from fiji.plugin.trackmate.visualization.hyperstack import HyperStackDisplayer
from fiji.plugin.trackmate.io import TmXmlReader

from fiji.plugin.trackmate.providers import DetectorProvider
from fiji.plugin.trackmate.providers import TrackerProvider
from fiji.plugin.trackmate.providers import SpotAnalyzerProvider
from fiji.plugin.trackmate.providers import EdgeAnalyzerProvider
from fiji.plugin.trackmate.providers import TrackAnalyzerProvider

#ESPERIMENTAL Todavia no funciona como quiero que funcione

#----------------
# Setup variables
#----------------
  
#Se supone que la carpeta tiene los archivos Model.xml y Settings.xml
# Put here the path to the TrackMate file you want to load
fileModel   = File(modelPath +r"\Model.xml" )
fileSettings = File(modelPath +r"\Settings.xml" )

# We have to feed a logger to the reader.
logger = Logger.IJ_LOGGER
logger.log(modelPath)  
#-------------------
# Instantiate reader
#-------------------
  
reader = TmXmlReader(fileModel)
if not reader.isReadingOk():
    sys.exit(reader.getErrorMessage())
#-----------------
# Get a full model
#-----------------
  
# This will return a fully working model, with everything
# stored in the file. Missing fields (e.g. tracks) will be 
# null or None in python
model = reader.getModel()
# model is a fiji.plugin.trackmate.Model
  
#----------------
# Display results
#----------------
  
# We can now plainly display the model. It will be shown on an
# empty image with default magnification.
sm = SelectionModel(model)


settings = Settings()
reader = TmXmlReader(fileSettings)

# Then we create all the providers, and point them to the target model:
detectorProvider        = DetectorProvider()
trackerProvider         = TrackerProvider()
spotAnalyzerProvider    = SpotAnalyzerProvider()
edgeAnalyzerProvider    = EdgeAnalyzerProvider()
trackAnalyzerProvider   = TrackAnalyzerProvider()
  
# Ouf! now we can flesh out our settings object:
reader.readSettings(settings, detectorProvider, trackerProvider, spotAnalyzerProvider, edgeAnalyzerProvider, trackAnalyzerProvider)
  
logger.log(str('\n\nSETTINGS:'))
logger.log(str(settings))
  
# The settings object is also instantiated with the target image.
# Note that the XML file only stores a link to the image.
# If the link is not valid, the image will not be found.
imp = settings.imp
imp.show()
  
# With this, we can overlay the model and the source image:
displayer =  HyperStackDisplayer(model, sm, imp)
displayer.setDisplaySettings("TrackDisplaymode", 7) #Solo mostrar el Track Seleccionado.



#Selecciona un spot de un id
tm = model.getTrackModel()
id  = tm.trackIDs(True).iterator().next()
spots = tm.trackSpots(id)
edges = tm.trackEdges(id)
sm.clearSelection()
sm.selectTrack(spots,edges,0)
displayer =  HyperStackDisplayer(model, sm, imp)
displayer.setDisplaySettings("TrackDisplaymode", 6) #Solo mostrar el Track Seleccionado.


displayer.render()
# =============================================================================
# =============================================================================
# #---------------------------------------------
# # Get only part of the data stored in the file
# #---------------------------------------------
#   
# # You might want to access only separate parts of the 
# # model. 
#   
# spots = model.getSpots()
# # spots is a fiji.plugin.trackmate.SpotCollection
#   
# logger.log(str(spots))
#   
# # If you want to get the tracks, it is a bit trickier. 
# # Internally, the tracks are stored as a huge mathematical
# # simple graph, which is what you retrieve from the file. 
# # There are methods to rebuild the actual tracks, taking
# # into account for everything, but frankly, if you want to 
# # do that it is simpler to go through the model:
#   
# trackIDs = model.getTrackModel().trackIDs(True) # only filtered out ones
# for id in trackIDs:
#     logger.log(str(id) + ' - ' + str(model.getTrackModel().trackEdges(id)))
#   
# 
# 
# 
# =============================================================================
