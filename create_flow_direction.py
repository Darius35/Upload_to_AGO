#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      dariusmirdamadi
#
# Created:     20/09/2018
# Copyright:   (c) dariusmirdamadi 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()

import arcpy
import os
import logging
import sys
import traceback
import datetime

# Script to populate flow direction feature class in from local project data

def CreateFlowDir(contMerge,flowDir,ukCoordSystem,areaSdePath):

    # Create log file
    dirname = os.path.dirname(os.path.realpath(__file__))
    LOG_FILENAME = os.path.join(dirname,"Update.log")
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

    try:
        # Start Editing
        edit = arcpy.da.Editor(areaSdePath)
        edit.startEditing(False, True)
        edit.startOperation()
        print("\nEditing Started\n")
        logging.debug("\nEditing Started\n")

        # Add Geometry to Continuous merge
        print("Creating flow direction points...\n")
        logging.debug("Creating flow direction points...")
        geomProperties = ["CENTROID_INSIDE","LINE_BEARING"]
        contExport = "C:\Temp\ContTemp.shp"
        if arcpy.Exists(contExport) == True:
            arcpy.Delete_management(contExport)

        arcpy.FeatureClassToFeatureClass_conversion(contMerge,"C:\Temp","ContTemp.shp")
        arcpy.AddGeometryAttributes_management(contExport,"CENTROID_INSIDE;LINE_BEARING")

        # Make XY Event Layer of point bearings
        pointBearings = "C:\Temp\pointBearings.shp"
        if arcpy.Exists(pointBearings) == True:
            arcpy.Delete_management(pointBearings)

        arcpy.env.workspace = r"C:\Temp"
        arcpy.management.XYTableToPoint(contExport,"pointBearings.shp","INSIDE_X","INSIDE_Y","",ukCoordSystem)

        # Append to Flow Dir Feature class
        arcpy.TruncateTable_management(flowDir)
        arcpy.Append_management(pointBearings,flowDir,"NO_TEST")

        arcpy.Delete_management(pointBearings)
        arcpy.Delete_management(contExport)

        # Stop editing
        edit.stopOperation()
        edit.stopEditing(True)
        print("\nEditing Stopped\n")
        logging.debug("\nEditing Stopped\n")

    except:
        # Get the traceback object
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        # Concatenate information together concerning the error into a message string
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

        # Print Python error messages for use in Python / Python Window
        print(pymsg)
        print(msgs)
        logging.debug(pymsg)
        logging.debug(msgs)
        logging.debug(datetime.datetime.now())



