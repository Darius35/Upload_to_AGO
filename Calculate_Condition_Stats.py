""" This module will calculate chart condition stats for Point, Piped and Surface items """

import arcpy
import os
import logging
import sys
import traceback
import datetime

def CalculateConditionStats(POINT,CONTINUOUS):

    # Create log file
    dirname = os.path.dirname(os.path.realpath(__file__))
    LOG_FILENAME = os.path.join(dirname,"Update.log")
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

    print("Calculating chart condition stats...\n")
    logging.debug("Calculating chart condition stats..")
    dirname = os.path.dirname(arcpy.Describe(POINT).catalogPath)
    desc = arcpy.Describe(dirname)
    if hasattr(desc, "datasetType") and desc.datasetType=='FeatureDataset':
        dirname = os.path.dirname(dirname)

    logging.debug("Updating Chart Condition Stats")


    def CalculateChartCondLine(fc):
        try:

            def findField(fc, fi):
                lst = arcpy.ListFields(fc)
                for f in lst:
                    if f.name == fi:
                        return 1

            

            lstFields = ["Peak_Cond","STRU_GRADE", "SERV_GRADE", "PG1", "PG2", "PG3", "PG4", "PG5", "PG0", "PG9", "PGMT3", "PGLT3", "STMT3", "ST3", "STLT3", "SEMT3", "SE3", "SELT3", "PGMT3_len", "PG3_len", "PGLT3_len", "LENGTH"]
            for fi in lstFields:
                if findField(fc,fi) != 1:
                    arcpy.AddField_management(fc,fi,"LONG")

            edit = arcpy.da.Editor(dirname)

            edit.startEditing(False, True)

            edit.startOperation()

            arcpy.AddMessage("\nEditing Started\n")
            
            arcpy.SelectLayerByAttribute_management(fc,"NEW_SELECTION","PG1 is Null")

                    # Update Peak Condition Points
            with arcpy.da.UpdateCursor(fc, ["SERV_GRADE", "STRU_GRADE", "Peak_Cond"]) as cursor:
                for row in cursor:
                    if row[0] is None or row[1] is None:
                        row[2] = 0
                        cursor.updateRow(row)
                    else:
                        if row[0] > row[1]:
                            row[2] = row[0]
                            cursor.updateRow(row)
                        else:
                            row[2] = row[1]
                            cursor.updateRow(row)

            # Set all Continuous chart condtion Stats to 0

            with arcpy.da.UpdateCursor(fc, lstFields) as cursor:
                for row in cursor:
                    row[3] = "0"
                    row[4] = "0"
                    row[5] = "0"
                    row[6] = "0"
                    row[7] = "0"
                    row[8] = "0"
                    row[9] = "0"
                    row[10] = "0"
                    row[11] = "0"
                    row[12] = "0"
                    row[13] = "0"
                    row[14] = "0"
                    row[15] = "0"
                    row[16] = "0"
                    row[17] = "0"
                    row[18] = "0"
                    row[19] = "0"
                    row[20] = "0"
                    cursor.updateRow(row)

            # Set chart condition field values to 1 where Continuous peak condition values are matched by the condition below

                    if row[0] == 1:
                        row[3] = 1
                        cursor.updateRow(row)
                    elif row[0] == 2:
                            row[4] = 1
                            cursor.updateRow(row)
                    elif row[0] == 3:
                            row[5] = 1
                            cursor.updateRow(row)
                    elif row[0] == 4:
                            row[6] = 1
                            cursor.updateRow(row)
                    elif row[0] == 5:
                            row[7] = 1
                            cursor.updateRow(row)
                    elif row[0] == 0:
                            row[8] = 1
                            cursor.updateRow(row)
                    elif row[0] == 9:
                            row[9] = 1
                            cursor.updateRow(row)
                    if row[0] > 3:
                            row[10] = 1
                            cursor.updateRow(row)
                    elif row[0] < 3 and row[0] != 0:
                            row[11] = 1
                            cursor.updateRow(row)

            # Set chart condition field values to 1 where Continuous Structural values are matched by the condition below
                    if row[1] is not None:
                        if row[1] > 3:
                            row[12] = 1
                            cursor.updateRow(row)
                        elif row[1] == 3:
                            row[13] = 1
                            cursor.updateRow(row)
                        elif row[1] < 3:
                            row[14] = 1
                            cursor.updateRow(row)

            # Set chart condition field values to 1 where Continuous Service values are matched by the condition below
                    if row[2] is not None:
                        if row[2] > 3:
                            row[15] = 1
                            cursor.updateRow(row)
                        elif row[2] == 3:
                            row[16] = 1
                            cursor.updateRow(row)
                        elif row[2] < 3:
                            row[17] = 1
                            cursor.updateRow(row)

            # Poplulates the length of each surface item for each of the the 3 grade types (more than G3, less than G3 and G3)

                    if row[10] == 1:
                        row[18] = row[21]
                        cursor.updateRow(row)
                    if row[11] == 1:
                        row[20] = row[21]
                        cursor.updateRow(row)
                    if row[5] == 1:
                        row[19] = row[21]
                        cursor.updateRow(row)



            print("\nContinuous Condition Stats Applied")

            edit.stopOperation()

            edit.stopEditing(True)

            arcpy.AddMessage("\nEditing Stopped\n")

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


    def CalculateChartCondPoint(fc):
        try:

            def findField(fc, fi):
                lst = arcpy.ListFields(fc)
                for f in lst:
                    if f.name == fi:
                        return 1


            lstFields = ["Peak_Cond","STRU_GRADE", "SERV_GRADE", "PG1", "PG2", "PG3", "PG4", "PG5", "PG0", "PG9", "PGMT3", "PGLT3", "STMT3", "ST3", "STLT3", "SEMT3", "SE3", "SELT3"]

            for fi in lstFields:
                if findField(fc,fi) != 1:
                    arcpy.AddField_management(fc,fi,"LONG")


            edit = arcpy.da.Editor(dirname)

            edit.startEditing(False, True)

            edit.startOperation()

            arcpy.AddMessage("\nEditing Started\n")
            
            arcpy.SelectLayerByAttribute_management(fc,"NEW_SELECTION","PG1 is Null")

            # Update Peak Condition Points
            with arcpy.da.UpdateCursor(fc, ["SERV_GRADE", "STRU_GRADE", "Peak_Cond"]) as cursor:
                for row in cursor:
                    if row[0] is None or row[1] is None:
                        row[2] = 0
                        cursor.updateRow(row)
                    else:
                        if row[0] > row[1]:
                            row[2] = row[0]
                            cursor.updateRow(row)
                        else:
                            row[2] = row[1]
                            cursor.updateRow(row)

            # Set all Point chart condtion Stats to 0
            with arcpy.da.UpdateCursor(fc, lstFields) as cursor:
                for row in cursor:
                    row[3] = "0"
                    row[4] = "0"
                    row[5] = "0"
                    row[6] = "0"
                    row[7] = "0"
                    row[8] = "0"
                    row[9] = "0"
                    row[10] = "0"
                    row[11] = "0"
                    row[12] = "0"
                    row[13] = "0"
                    row[14] = "0"
                    row[15] = "0"
                    row[16] = "0"
                    row[17] = "0"
                    cursor.updateRow(row)

            # Set chart condition field values to 1 where Point peak condition values are matched by the condition below

                    if row[0] == 1:
                        row[3] = 1
                        cursor.updateRow(row)
                    elif row[0] == 2:
                            row[4] = 1
                            cursor.updateRow(row)
                    elif row[0] == 3:
                            row[5] = 1
                            cursor.updateRow(row)
                    elif row[0] == 4:
                            row[6] = 1
                            cursor.updateRow(row)
                    elif row[0] == 5:
                            row[7] = 1
                            cursor.updateRow(row)
                    elif row[0] == 0:
                            row[8] = 1
                            cursor.updateRow(row)
                    elif row[0] == 9:
                            row[9] = 1
                            cursor.updateRow(row)
                    if row[0] > 3:
                            row[10] = 1
                            cursor.updateRow(row)
                    elif row[0] < 3 and row[0] != 0:
                            row[11] = 1
                            cursor.updateRow(row)

            # Set chart condition field values to 1 where Point Structural values are matched by the condition below

                    if row[1] is not None:
                        if row[1] > 3:
                            row[12] = 1
                            cursor.updateRow(row)
                        elif row[1] == 3:
                            row[13] = 1
                            cursor.updateRow(row)
                        elif row[1] < 3:
                            row[14] = 1
                            cursor.updateRow(row)

            # Set chart condition field values to 1 where Point Service values are matched by the condition below

                    if row[2] is not None:
                        if row[2] > 3:
                            row[15] = 1
                            cursor.updateRow(row)
                        elif row[2] == 3:
                            row[16] = 1
                            cursor.updateRow(row)
                        elif row[2] < 3:
                            row[17] = 1
                            cursor.updateRow(row)

            print("\nPOINT Condition Stats Applied")

            edit.stopOperation()

            edit.stopEditing(True)

            arcpy.AddMessage("\nEditing Stopped\n")

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
        
    ContinuousLayer = arcpy.MakeFeatureLayer_management(CONTINUOUS,"ContinuousLay")
    CalculateChartCondLine(ContinuousLayer)
    PointLayer = arcpy.MakeFeatureLayer_management(POINT,"PointLayer")
    CalculateChartCondPoint(PointLayer)


