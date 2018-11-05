import arcpy
import os
import logging
import sys
import traceback
import datetime
import pandas as pd

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

        return fieldmappings
    
    def EditCSV(eventsCsv):
        # Remove action fields from csv (values are over 255 chars)
        dirname = os.path.dirname(os.path.abspath(eventsCsv))
        outputfile = os.path.join(dirname,"FloodEdited.csv")
        df = pd.read_csv(eventsCsv)
        dfs = df.drop(['Initial Action','Secondary Action'], axis = 1)
        dfs.to_csv(outputfile)

        #df= pd.read_csv("sample_data.csv", usecols =[i for i in cols if i != 'Initial Action'])
        
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
        floodPoints = "C:\Temp\FloodPoints.shp"
        if arcpy.Exists(floodPoints) == True:
            arcpy.Delete_management(floodPoints)
        
        arcpy.env.workspace = r"C:\Temp"
        arcpy.management.XYTableToPoint(outCSV,"FloodPoints.shp","Easting","Northing","",ukGrid)

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


