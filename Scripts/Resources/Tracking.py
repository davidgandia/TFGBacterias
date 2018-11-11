
#@Boolean (label = "aheadless") headLess
#@String (label = "imagPath") imgPath
#@String (label = "dataOutputPath") dataOutPath
#@Double (label = "KALMAN_SEARCH_RADIUS") kalmanSearchRadius
#@Double (label = "LINKING_MAX_DISTANCE") linkingMaxDistance

from fiji.plugin.trackmate import Model, FeatureModel, TrackModel
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import TrackMate
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate import Logger
from ij import IJ
import sys
from java.io import File

from fiji.plugin.trackmate.detection import DogDetectorFactory
from fiji.plugin.trackmate.tracking.kalman import KalmanTrackerFactory
from fiji.plugin.trackmate.tracking import LAPUtils

import fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer as HyperStackDisplayer

import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
from fiji.plugin.trackmate.features.track import TrackBranchingAnalyzer, TrackDurationAnalyzer, TrackIndexAnalyzer, TrackLocationAnalyzer, TrackSpeedStatisticsAnalyzer, TrackSpotQualityFeatureAnalyzer
from fiji.plugin.trackmate.features.spot  import SpotMorphologyAnalyzerFactory

import fiji.plugin.trackmate.action.ExportTracksToXML as ExportTracksToXML
 
from fiji.plugin.trackmate.io import TmXmlWriter
from fiji.plugin.trackmate.util import TMUtils 


#Spot detector settings
DO_SUBPIXEL_LOCALIZATION 	= True
RADIUS 				  		= 2.25
TARGET_CHANNEL				= 1
THRESHOLD 					= 3.0
DO_MEDIAN_FILTERING 		= False


#Trackying settings
MAX_FRAME_GAP				= 2
KALMAN_SEARCH_RADIUS		= kalmanSearchRadius
LINKING_MAX_DISTANCE		= linkingMaxDistance

#filenameSettins
outputDataPath     = dataOutPath + "\\"
inputImagePath     = imgPath
print("hola")

# Get currently selected image
#imp = WindowManager.getCurrentImage()
imp = IJ.openImage(inputImagePath)

if not headLess:
    imp.show()


#----------------------------
# Create the model object now
#----------------------------

# Some of the parameters we configure below need to have
# a reference to the model at creation. So we create an
# empty model now.

model = Model()

# Send all messages to ImageJ log window.
logger = Logger.IJ_LOGGER
model.setLogger(logger)



#------------------------
# Prepare settings object
#------------------------
settings = Settings()
settings.setFrom(imp)



# Configure detector - We use the Strings for the keys
settings.detectorFactory = DogDetectorFactory()
settings.detectorSettings = { 
    'DO_SUBPIXEL_LOCALIZATION' : DO_SUBPIXEL_LOCALIZATION,
    'RADIUS' : RADIUS,
    'TARGET_CHANNEL' : TARGET_CHANNEL,
    'THRESHOLD' : THRESHOLD,
    'DO_MEDIAN_FILTERING' : DO_MEDIAN_FILTERING,
}  

# Configure spot filters - Classical filter on quality
#filter1 = FeatureFilter('QUALITY',  27.6, False)
#settings.addSpotFilter(filter1)
settings.initialSpotFilterValue  = 27.6
#Configure Spot Analyzers
#settings.addSpotAnalyzerFactory(SpotMorphologyAnalyzerFactory())   





# Configure tracker
settings.trackerFactory = KalmanTrackerFactory()
settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap() # almost good enough
settings.trackerSettings['MAX_FRAME_GAP'] = MAX_FRAME_GAP
settings.trackerSettings['KALMAN_SEARCH_RADIUS'] = KALMAN_SEARCH_RADIUS
settings.trackerSettings['LINKING_MAX_DISTANCE'] = LINKING_MAX_DISTANCE
    
# Configure track analyzers - Later on we want to filter out tracks 
# based on their displacement, so we need to state that we want 
# track displacement to be calculated. By default, out of the GUI, 
# not features are calculated. 
    
# The displacement feature is provided by the TrackDurationAnalyzer.The rest of the features are also added. Just in case.
# In order to reduce the execution time, modify this part of the CODE.    
settings.addTrackAnalyzer(TrackDurationAnalyzer())
settings.addTrackAnalyzer(TrackSpeedStatisticsAnalyzer())
settings.addTrackAnalyzer(TrackBranchingAnalyzer())
settings.addTrackAnalyzer(TrackIndexAnalyzer())
settings.addTrackAnalyzer(TrackLocationAnalyzer())
settings.addTrackAnalyzer(TrackSpotQualityFeatureAnalyzer())

# Configure track filters - We want to get rid of the two immobile spots at 
# the bottom right of the image. Track displacement must be above 10 pixels.
 
#filter2 = FeatureFilter('NUMBER_SPOTS', 10, True)
#settings.addTrackFilter(filter2)
#filter2 = FeatureFilter('NUMBER_SPOTS', 40, False)
#settings.addTrackFilter(filter2)


logger.log(str('\n\nSETTINGS:'))
logger.log(str(settings))

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
if not headLess:
    selectionModel = SelectionModel(model)
    displayer =  HyperStackDisplayer(model, selectionModel, imp)
    displayer.render()
    displayer.refresh()
    
# Echo results with the logger we set at start:
logger.log(str(model))

#-------------
#Print Results
#-------------

#Save tracks as XML
outputDataPathTracks = outputDataPath +"Tracks.xml" 
outFile = File(outputDataPathTracks)
ExportTracksToXML.export(model, settings, outFile) 

#Save Model as XML
outputDataPathModel = outputDataPath +"Model.xml" 
outFile = File(outputDataPathModel)
writer = TmXmlWriter(outFile) 

writer.appendModel(model)
writer.writeToFile()

#Save Settings as XML
outputDataPathSettings = outputDataPath +"Settings.xml" 
outFile = File(outputDataPathSettings)
writer = TmXmlWriter(outFile)

writer.appendSettings(settings)
writer.writeToFile()

# The feature model, that stores track features.
f = open(outputDataPath+"TrackFeatures.txt","w")

fm = model.getFeatureModel()
tm = model.getTrackModel()
isInt = fm.getTrackFeatureIsInt()
dimension = fm.getTrackFeatureDimensions()
names = fm.getTrackFeatureNames()

#First line. Print all the information of what is going to be represented
f.write("{}".format("TrackID"))
for feature in fm.getTrackFeatures():
    f.write("{}({}) ".format(feature,dimension[feature]))

#Print the features of each Track
for id in tm.trackIDs(True):
    f.write("\n")
    f.write('{} '.format(id))
    for feature in fm.getTrackFeatures():
        if isInt[feature]:
            f.write("{} ".format(int(fm.getTrackFeature(id,feature))))
        else:
            f.write("{} ".format(fm.getTrackFeature(id,feature)))

f.close()

logger.log("\n########\nTerminado\n########")