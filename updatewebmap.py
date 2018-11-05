import arcpy, os, logging, sys
import datetime
import traceback

def UpdateFeatureService(areaFldr,areaName):

    try:
    # Create logfile
        dirname = os.path.dirname(os.path.realpath(__file__))
        LOG_FILENAME = os.path.join(dirname,"Update.log")
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

        # Sign in to portal
        arcpy.SignInToPortal('https://www.arcgis.com', 'CARNELL_AGO1', 'carnelL2014')

        # Set output file names
        outdir = outdir = os.path.join(areaFldr,"SD")
        service = "FeatureSharingDraft" + areaName
        sddraft_filename = service + ".sddraft"
        sddraft_output_filename = os.path.join(outdir, sddraft_filename)
        if os.path.isfile(sddraft_output_filename) == True:
            os.remove(sddraft_output_filename)

        # Reference map to publish
        areaAprx = areaName + ".aprx"
        aprx = arcpy.mp.ArcGISProject(os.path.join(areaFldr,areaAprx))
        m = aprx.listMaps("Master")[0]

        # Create FeatureSharingDraft and set service properties
        sharing_draft = m.getWebLayerSharingDraft("HOSTING_SERVER", "FEATURE", service)
        sharing_draft.summary = areaName + " Drainage Feature Service"
        sharing_draft.tags = areaName
        sharing_draft.description = ""
        sharing_draft.allowExporting = True
        sharing_draft.overwriteExistingService = True
        sharing_draft.serviceName = areaName + "_WFL"


        # Create Service Defintion Draft file
        sharing_draft.exportToSDDraft(sddraft_output_filename)

        # Stage Service
        print("Creating SD file...")
        logging.debug("Creating SD file...")
        sd_filename = service + ".sd"
        sd_output_filename = os.path.join(outdir, sd_filename)
        if os.path.isfile(sd_output_filename) == True:
            os.remove(sd_output_filename)
        arcpy.StageService_server(sddraft_output_filename, sd_output_filename)

        # Share to portal
        print("Uploading Service Definition...")
        logging.debug("Uploading Service Definition...")
        arcpy.UploadServiceDefinition_server(sd_output_filename, "My Hosted Services")

        print("Successfully Uploaded service.")
        logging.debug("Successfully Uploaded service.")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        logging.debug("There was a problem publishing!!!\n + Execute Error: " + str(arcpy.GetMessages()))
        logging.debug(datetime.datetime.now())
        logging.debug("Quitting")
        sys.exit(0)
    except:
        # Get the traceback object
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        # Concatenate information together concerning the error into a message string
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages() + "\n"

        # Print Python error messages for use in Python / Python Window
        print(pymsg)
        print(msgs)
        logging.debug(pymsg)
        logging.debug(msgs)
        logging.debug(datetime.datetime.now())
        quit()