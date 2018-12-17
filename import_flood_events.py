import arcpy
import os
import logging
import sys
import traceback
import datetime
import pandas as pd
import numpy as np
print ("Hello")

def ImportFloodEvents(eventsCsv,floodFc,ukGrid):
    
    def SetFieldMappings(floodPoints):
        # Field Mapping
        fieldmappings = arcpy.FieldMappings()
        fieldmappings.addTable(floodPoints)

        fldMap_Reported = arcpy.FieldMap()
        fldMap_Reported.addInputField(floodPoints,"Reported")
        reported = fldMap_Reported.outputField
        reported.name = "Reported_D"
        fldMap_Reported.outputField = reported
        fieldmappings.addFieldMap(fldMap_Reported)

        fldMap_Attended = arcpy.FieldMap()
        fldMap_Attended.addInputField(floodPoints,"Attended")
        attended = fldMap_Attended.outputField
        attended.name = "Attended_D"
        fldMap_Attended.outputField = attended
        fieldmappings.addFieldMap(fldMap_Attended)

        fldMap_Cleared = arcpy.FieldMap()
        fldMap_Cleared.addInputField(floodPoints,"Cleared")
        cleared = fldMap_Cleared.outputField
        cleared.name = "Cleared_D"
        fldMap_Cleared.outputField = cleared
        fieldmappings.addFieldMap(fldMap_Cleared)

        fldMap_FID = arcpy.FieldMap()
        fldMap_FID.addInputField(floodPoints,"Flood Event ID")
        fid = fldMap_FID.outputField
        fid.name = "Flood_Even"
        fldMap_FID.outputField = fid
        fieldmappings.addFieldMap(fldMap_FID)

        fldMap_HAPMS = arcpy.FieldMap()
        fldMap_HAPMS.addInputField(floodPoints,"HAPMS Section")
        hapms = fldMap_HAPMS.outputField
        hapms.name = "HAPMS_Sect"
        fldMap_HAPMS.outputField = hapms
        fieldmappings.addFieldMap(fldMap_HAPMS)

        fldMap_CWay = arcpy.FieldMap()
        fldMap_CWay.addInputField(floodPoints,"Carriageway Type")
        carriageway = fldMap_CWay.outputField
        carriageway.name = "Carriagewa"
        fldMap_CWay.outputField = carriageway
        fieldmappings.addFieldMap(fldMap_CWay)

        fldMap_FloodSev = arcpy.FieldMap()
        fldMap_FloodSev.addInputField(floodPoints,"Flood Severity Index")
        floodsev = fldMap_FloodSev.outputField
        floodsev.name = "Flood_Seve"
        fldMap_FloodSev.outputField = floodsev
        fieldmappings.addFieldMap(fldMap_FloodSev)


        return fieldmappings
    
    def EditCSV(eventsCsv):
        # Remove action fields from csv (values are over 255 chars)
        dirname = os.path.dirname(os.path.abspath(eventsCsv))
        outputfile = os.path.join(dirname,"FloodEdited.csv")
        df = pd.read_csv(eventsCsv,skipinitialspace=True)
        dfs = df.drop(['Initial Action','Secondary Action'], axis = 1)
        dfs.to_csv(outputfile)
      
        return outputfile

    try:

        dirname = os.path.dirname(os.path.realpath(__file__))
        LOG_FILENAME = os.path.join(dirname,"Update.log")
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

        print("Importing flood events...\n")
        logging.debug("Importing flood events...")
        arcpy.TruncateTable_management(floodFc)
        # Edit csv
        outCSV = EditCSV(eventsCsv)

        # Create points from csv
        #floodPoints = "C:\Temp\FloodPoints.shp"
        #if arcpy.Exists(floodPoints) == True:
        #    arcpy.Delete_management(floodPoints)
        
        #arcpy.env.workspace = r"C:\Temp"
        #arcpy.management.XYTableToPoint(outCSV,"FloodPoints.shp","Easting","Northing","",ukGrid)

        floodPoints = arcpy.MakeXYEventLayer_management(outCSV,"Easting","Northing","floodPoints",ukGrid)

        # Add output field to field mappings object
        fieldmappings = SetFieldMappings(floodPoints)

        # Append to flood event layer
        arcpy.Append_management(floodPoints,floodFc,"NO_TEST",fieldmappings)
        arcpy.Delete_management(floodPoints)
        os.remove(outCSV)

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


