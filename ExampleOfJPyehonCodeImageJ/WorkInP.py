from fiji.plugin.trackmate.visualization.hyperstack import HyperStackDisplayer
from fiji.plugin.trackmate.io import TmXmlReader
from fiji.plugin.trackmate import Logger
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate.providers import DetectorProvider
from fiji.plugin.trackmate.providers import TrackerProvider
from fiji.plugin.trackmate.providers import SpotAnalyzerProvider
from fiji.plugin.trackmate.providers import EdgeAnalyzerProvider
from fiji.plugin.trackmate.providers import TrackAnalyzerProvider
from java.io import File
import sys
from fiji.plugin.trackmate import Model
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import TrackMate
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate import Logger
from fiji.plugin.trackmate.detection import LogDetectorFactory
from fiji.plugin.trackmate.tracking.sparselap import SparseLAPTrackerFactory
from fiji.plugin.trackmate.tracking import LAPUtils
from ij import IJ
import fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer as HyperStackDisplayer
import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
import sys
import fiji.plugin.trackmate.features.track.TrackDurationAnalyzer as TrackDurationAnalyzer
import fiji.plugin.trackmate.detection.DetectorKeys as DetectorKeys

#Spot detector settings
DO_SUBPIXEL_LOCALIZATION 	= True
RADIUS 				  		= 4.2
TARGET_CHANNEL				= 1.0
THRESHOLD 					= 3.0
DO_MEDIAN_FILTERING 		= False


#Trackying settings
MAX_FRAME_GAP				= 2
KALMAN_SEARCH_RADIUS		= 10.0
LINKING_MAX_DISTANCE		= 15.0



    
# Get currently selected image
#imp = WindowManager.getCurrentImage()
imp = IJ.openImage('D:\\uni\\TFG\\TrackingImageJInfo\\ScriptingWithPy\\1-paralelo-1.tif')
imp.show()
    
#----------------------------
# Create the model object now
#----------------------------
    
# Some of the parameters we configure below need to have
# a reference to the model at creation. So we create an
# empty model now.
    
model = Model()
    
# Send all messages to ImageJ log window.
model.setLogger(Logger.IJ_LOGGER)
   
#------------------------
# Prepare settings object
#------------------------
       
settings = Settings()
settings.setFrom(imp)

#Take the rest of the settings from a xml file.
file = File("D:\\uni\\TFG\\TrackingImageJInfo\\ScriptingWithPy\\TrackFilterAfter.xml")
  
# We have to feed a logger to the reader.
logger = Logger.IJ_LOGGER
  
#-------------------
# Instantiate reader
#-------------------
  
reader = TmXmlReader(file)
if not reader.isReadingOk():
    sys.exit(reader.getErrorMessage())

 
#---------------------------------------
# Building a settings object from a file
#---------------------------------------
  
# Reading the Settings object is actually currently complicated. The 
# reader wants to initialize properly everything you saved in the file,
# including the spot, edge, track analyzers, the filters, the detector,
# the tracker, etc...
# It can do that, but you must provide the reader with providers, that
# are able to instantiate the correct TrackMate Java classes from
# the XML data.
  
  
# Then we create all the providers, and point them to the target model:
detectorProvider        = DetectorProvider()
trackerProvider         = TrackerProvider()
spotAnalyzerProvider    = SpotAnalyzerProvider()
edgeAnalyzerProvider    = EdgeAnalyzerProvider()
trackAnalyzerProvider   = TrackAnalyzerProvider()
  
# Ouf! now we can flesh out our settings object:
reader.readSettings(settings, detectorProvider, trackerProvider, spotAnalyzerProvider, edgeAnalyzerProvider, trackAnalyzerProvider)
  

#Modiy core parameters

settings.trackerSettings['MAX_FRAME_GAP'] = MAX_FRAME_GAP
settings.trackerSettings['KALMAN_SEARCH_RADIUS'] = KALMAN_SEARCH_RADIUS
settings.trackerSettings['LINKING_MAX_DISTANCE'] = LINKING_MAX_DISTANCE
"""
settings.detectorSettings = { 
    'DO_SUBPIXEL_LOCALIZATION' :  DO_SUBPIXEL_LOCALIZATION,
    'RADIUS' : RADIUS,
    'TARGET_CHANNEL' : TARGET_CHANNEL	,
    'THRESHOLD' : THRESHOLD ,
    'DO_MEDIAN_FILTERING' : DO_MEDIAN_FILTERING,
} 

settings.detectorSettings['RADIUS'] = RADIUS
settings.detectorSettings['THRESHOLD'] = THRESHOLD
print(settings.detectorSettings)
"""

settings.detectorSettings = {
    DetectorKeys.KEY_DO_SUBPIXEL_LOCALIZATION : True,
    DetectorKeys.KEY_RADIUS : 4.3,
    DetectorKeys.KEY_TARGET_CHANNEL : 1,
    DetectorKeys.KEY_THRESHOLD : 3.,
    DetectorKeys.KEY_DO_MEDIAN_FILTERING : False,
} 
 
logger.log(str('\n\nSETTINGS:'))
logger.log(str(settings))


"""
TODO Filter. Think about how and what to implement in the filter.
"""
# The displacement feature is provided by the TrackDurationAnalyzer.
    
settings.addTrackAnalyzer(TrackDurationAnalyzer())
filter2 = FeatureFilter('TRACK_DISPLACEMENT', 8, True)
settings.addTrackFilter(filter2)
filter2 = FeatureFilter('TRACK_DISPLACEMENT', 50, True)
settings.addTrackFilter(filter2)
filter2 = FeatureFilter('TRACK_DISPLACEMENT', 160, True)
settings.addTrackFilter(filter2)


#-------------------
# Instantiate plugin
#-------------------

trackmate = TrackMate(model, settings)
       
#--------
# Process
#--------
    
ok = trackmate.checkInput()
if not ok:
    sys.exit(str(trackmate.getErrorMessage()))
    
ok = trackmate.process()
if not ok:
    sys.exit(str(trackmate.getErrorMessage()))
    
       
#----------------
# Display results
#----------------
     
selectionModel = SelectionModel(model)
displayer =  HyperStackDisplayer(model, selectionModel, imp)
displayer.render()
displayer.refresh()

 
# Echo results with the logger we set at start:
model.getLogger().log(str(model))
print(str(model)) 


