# Script to activate update feature service

import os
import logging
import traceback
import Calculate_Condition_Stats
import updatewebmap
import datetime
import create_flow_direction
import import_flood_events

# Create log file
dirname = os.path.dirname(os.path.realpath(__file__))
LOG_FILENAME = os.path.join(dirname,"Update.log")
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

# Set global variables
ukCoordSystem = r"Coordinate Systems\Projected Coordinate Systems\National Grids\Europe\British National Grid.prj"

# Loop through folders
def GetAreasToUpload():

    dvFolder = r"\\carnell-fs1\GIS\DRAINAGE VIEWER"
    lstDirs = os.listdir(dvFolder)
    lstDirs.remove("updateFeatureService")
    lstAreasToUpload = []
    for fldr in lstDirs:
        areaDir = os.path.join(dvFolder,fldr)
        if os.path.isdir(areaDir) == True:
            lstSubDirs = os.listdir(areaDir)

            if "SD" in lstSubDirs:
                lstAreasToUpload.append(areaDir)

    return lstAreasToUpload

def processArea(ukCoordSystem,lstAreasToUpload):

    for areaFldr in lstUploadAreas:
        # Set variables
        pathSplit = os.path.split(os.path.abspath(areaFldr))
        areaName = pathSplit[1]
        areaSde = areaName + ".sde"
        areaSdePath = os.path.join(areaFldr,areaSde)
        HEsde = "HE_Datasets.sde"
        HesdePath = os.path.join(areaFldr,HEsde)

        flowDir = areaName + ".DBO.FLOW_DIRECTION"
        contMerge = areaName + ".DBO.GPS_Data_HADDMS_CONTINUOUS_HADDMS"
        pointMerge = areaName + ".DBO.GPS_Data_HADDMS_POINT_HADDMS"
        floodEvents = "He_Datasets.DBO.FLOOD_EVENTS_" + areaName

        floodeventsPath = os.path.join(HesdePath,floodEvents)
        flowdirPath = os.path.join(areaSdePath,flowDir)
        contMergePath = os.path.join(areaSdePath,contMerge)
        pointMergePath = os.path.join(areaSdePath,pointMerge)

        print(areaName + " PROCESS STARTED: " + str(datetime.datetime.now()))
        logging.debug(areaName + " PROCESS STARTED: " + str(datetime.datetime.now()))

         #Create Flow Direction Layer Set data source
        create_flow_direction.CreateFlowDir(contMergePath,flowdirPath,ukCoordSystem,areaSdePath)

        # Update Flood Event Data
        floodFolder = os.path.join(areaFldr,"FLOOD")
        if os.path.isdir(floodFolder) == True:
            floodFiles = os.listdir(floodFolder)
            floodFile = ""
            for fl in floodFiles:
                if ".csv" in fl:
                    floodFile = fl
            floodFilePath = os.path.join(floodFolder,floodFile)
            if os.path.isfile(floodFilePath) == True:
                import_flood_events.ImportFloodEvents(floodFilePath,floodeventsPath,ukCoordSystem)
            else:
                print ("\nNo flood events csv found for " + areaName)
                logging.debug("\nNo flood events csv found for " + areaName)

        # Calculate Condition Stats
        Calculate_Condition_Stats.CalculateConditionStats(pointMergePath,contMergePath)

        # update feature service
        updatewebmap.UpdateFeatureService(areaFldr,areaName)

        print (areaName + " PROCESS ENDED: " + str(datetime.datetime.now()))
        logging.debug(areaName + " PROCESS ENDED: " + str(datetime.datetime.now()))

    return True
lstUploadAreas = GetAreasToUpload()
if processArea(ukCoordSystem,lstUploadAreas) == True:
    print ("PROCESS COMPLETE: " + str(datetime.datetime.now()))
    logging.debug("PROCESS COMPLETE: " + str(datetime.datetime.now()))
