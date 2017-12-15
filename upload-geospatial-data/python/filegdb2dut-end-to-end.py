import sys, getopt, os, shutil, zipfile
import datetime,logging,traceback,arcpy
import arcpy
import boto3
nowstart = datetime.datetime.now()
YearMonthDay = nowstart.strftime("%Y_%m_%d_%H_%M_%S")

def setupLogging(logfilename) :
    newlogfilename = logfilename + YearMonthDay + '.log'
    logformatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()
    logger.setLevel(0) #'10-Debug'
    filehandler = logging.FileHandler(newlogfilename)
    filehandler.setFormatter(logformatter)
    logger.addHandler(filehandler)
    consolehandler = logging.StreamHandler()
    consolehandler.setFormatter(logformatter)
    logger.addHandler(consolehandler)

def sde2gdb(sde_connection,featureclass_name,output_path,fgdb_name,outFCname):
    #establish sde connection workspace
    arcpy.env.workspace = sde_connection
    #does the geodatabase exist if so delete it
    if (os.path.isdir(output_path+'\\'+fgdb_name+'.gdb')== True):
        shutil.rmtree(output_path+'\\'+fgdb_name+'.gdb')
    #create a version 10 FileGDB. Note Selfservice only supports FileGDB <10.3
    arcpy.CreateFileGDB_management(output_path, fgdb_name,"10.0")
    #Export the sde featureclass to the filegdb
    arcpy.FeatureClassToFeatureClass_conversion(sde_connection+'//'+featureclass_name, 
                                            output_path+'\\'+fgdb_name+'.gdb', 
                                            outFCname)
    #drop SDE connection 
    arcpy.ClearWorkspaceCache_management()
    return output_path+'\\'+fgdb_name+'.gdb'

def Zipfgdb(inFileGDB, Delete = True):
    #Directory of file geodatabase
    inLocation = os.path.dirname (inFileGDB)
    #Base name of shapefile
    inName = os.path.basename (os.path.splitext(inFileGDB)[0])
    #Create the zipfile name 
    zipfl = os.path.join (inLocation, inName + ".zip")
    #Create zipfile object
    ZIP = zipfile.ZipFile (zipfl, "w")
    #Iterate files in shapefile directory
    for fl in os.listdir (inFileGDB):
        #Get full path of file
        inFile = os.path.join (inFileGDB, fl)
        #Add file to zipfile. exclude any lock files
        if os.path.splitext(fl)[1][1:] <> 'lock':
            ZIP.write(inFile,fl)
    #Delete filegeodatabase if indicated
    if Delete == True:
        shutil.rmtree(inFileGDB)
    #Close zipfile object
    ZIP.close()
    #Return zipfile full path
    return zipfl

def UploadFile(source_file, bucket, key, profile):    
    # It is not recommended to hard code your credentials into code such as 
    # session = boto3.Session(aws_access_key_id=None, aws_secret_access_key=None, region='ap-southeast-2')
    # see http://boto3.readthedocs.io/en/latest/guide/configuration.html how to set your credentials or 
    # Download the aws cli tool and run 'aws configure --profile SLIP_SelfService' to create a user profile 
    session = boto3.Session(profile_name=profile)
    s3_client = session.client('s3')
    s3_client.upload_file(source_file, bucket, key)
    file_url = '{0}/{1}/{2}'.format(s3_client.meta.endpoint_url, bucket, key)
    return file_url

def execute_job

(SDE_CONNECTION,SDE_FEATURE_CLASS_NAME,TEMP_WORKING_DIRECTORY,SLIP_DATASET_NAME,AWS_CREDENTIAL_PROFILE,AWS_S3_BUCKET,AWS_S3_FOL

DER_KEY):
    try:
        logfile = TEMP_WORKING_DIRECTORY+ r'\\' + SLIP_DATASET_NAME + '_asat_'
        setupLogging(logfile)
        TEMP_FGDB = SLIP_DATASET_NAME + '_asat_'+YearMonthDay
        logging.info('**************************************************************************************************')
        logging.info('#### parameters provided ####')
        logging.info('--sde_Connection [%s]'%SDE_CONNECTION)
        logging.info('--inputFeatureClass [%s]'%SDE_FEATURE_CLASS_NAME)
        logging.info('--workingDir [%s]'%TEMP_WORKING_DIRECTORY)
        logging.info('--outputFeatureClass [%s]'%SLIP_DATASET_NAME)
        logging.info('--aws_profile [%s]'%AWS_CREDENTIAL_PROFILE)
        logging.info('--S3_Bucket [%s]'%AWS_S3_BUCKET)
        logging.info('--S3_FolderKey [%s]'%AWS_S3_FOLDER_KEY)
        logging.info("Starting program at " + str(datetime.datetime.now()))
        logging.info("Attempting to Connect to SDE workspace [%s].\n\t\t\t\tExporting SDE FeatureClass [%s] To [%s\\%s.gdb]"% 

(SDE_CONNECTION,SDE_FEATURE_CLASS_NAME,TEMP_WORKING_DIRECTORY,TEMP_FGDB))
        my_temp_filegdb = sde2gdb(SDE_CONNECTION,SDE_FEATURE_CLASS_NAME,TEMP_WORKING_DIRECTORY,TEMP_FGDB,SLIP_DATASET_NAME)
        logging.info('Successfully created file geodatabase [%s]' % my_temp_filegdb)
        logging.info('Zipping up [%s]' % my_temp_filegdb)
        my_temp_zip = Zipfgdb(my_temp_filegdb)
        logging.info('Successfully created zip geodatabase [%s]' % my_temp_zip)
        logging.info('Uploading [%s] to S3' % my_temp_zip)
        s3_uploadURL = UploadFile(my_temp_zip,AWS_S3_BUCKET,AWS_S3_FOLDER_KEY+os.path.basename

(my_temp_zip),AWS_CREDENTIAL_PROFILE)
        logging.info('Successfully Uploaded [%s] to S3' % s3_uploadURL)
        logging.info("Completing program at " + str(datetime.datetime.now()))
        pass
    except arcpy.ExecuteError:
        arcpymsg = arcpy.GetMessages(2)
        arcpy.AddError(arcpymsg)
        logm = 'Encounter ArcPy Errors:\n' + str(arcpymsg)
        logging.error(logm)
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "Encounter Python Errors & Traceback info:\n" + str(tbinfo) + "\nError Info:\n" + str(sys.exc_info()[1])
        arcpy.AddError(pymsg)
        logging.error(pymsg)
    finally:
        logging.info('Script shutdown.')
        logging.info('**************************************************************************************************')
        logging.shutdown()
        logging.getLogger(None).handlers = []

def main(argv):
    SDE_CONNECTION = ''
    SDE_FEATURE_CLASS_NAME = ''
    SLIP_DATASET_NAME = ''
    AWS_CREDENTIAL_PROFILE = ''
    AWS_S3_BUCKET = ''
    AWS_S3_FOLDER_KEY = ''
    TEMP_WORKING_DIRECTORY = ''

    try:
        opts, args = getopt.getopt(argv,'h',

['sde_Connection=','inputFeatureClass=','workingDir=','outputFeatureClass=','aws_profile=','S3_Bucket=','S3_FolderKey='])

    except getopt.GetoptError:
        print ' --sde_Connection <SDE_Connection> --inputFeatureClass <SDE_Input_FeatureClass_Name> --workingDir 

<Tempory_Working_Directory_used_to_store_logs_and_the_fgdb> --ofc <Output_Feature_Class_Name> --aws_profile <AWS_Profile> --

S3_Bucket <AWS_Bucket> --S3_Key <AWS_folderKey'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print '--sde_Connection <SDE_Connection> --inputFeatureClass <SDE_Input_FeatureClass_Name> --workingDir 

<Tempory_Working_Directory_used_to_store_logs_and_the_fgdb> --ofc <Output_Feature_Class_Name> --aws_profile <AWS_Profile>  --

S3_Bucket <AWS_Bucket> --S3_Key <AWS_folderKey'
            sys.exit()
        elif opt == '--sde_Connection':
            SDE_CONNECTION = arg
        elif opt == '--inputFeatureClass':
            SDE_FEATURE_CLASS_NAME = arg
        elif opt == '--workingDir':
            TEMP_WORKING_DIRECTORY = arg
        elif opt == '--outputFeatureClass':
            SLIP_DATASET_NAME = arg
        elif opt == '--aws_profile':
            AWS_CREDENTIAL_PROFILE = arg
        elif opt == '--S3_Bucket':
            AWS_S3_BUCKET = arg
        elif opt == '--S3_FolderKey':
            AWS_S3_FOLDER_KEY = arg

    #check all flags have been populated
    if (SDE_CONNECTION == '' or SDE_FEATURE_CLASS_NAME == '' or SLIP_DATASET_NAME == '' or AWS_CREDENTIAL_PROFILE == '' or 

TEMP_WORKING_DIRECTORY == '' or AWS_S3_BUCKET == '' or AWS_S3_FOLDER_KEY == ''):
        print '#### Insufficent parameters provided ####'
        print '\n--sde_Connection [%s] (ie. "C:\\selfservice_uploads\\Connection_to_PEAS71-DISS-SDE.sde " )'%SDE_CONNECTION
        print '\n--inputFeatureClass [%s] (ie. "GDB.W_IMAGERY_METADATA" )'%SDE_FEATURE_CLASS_NAME
        print '\n--workingDir [%s] (ie. "C:\\selfservice_uploads" )'%TEMP_WORKING_DIRECTORY
        print '\n--outputFeatureClass [%s] (ie. "LGATE071" )'%SLIP_DATASET_NAME
        print '\n--aws_profile [%s]( ie "SLIP_UAT_USER" )'%AWS_CREDENTIAL_PROFILE
        print '\n--S3_Bucket [%s] (ie. "lg-slip-selfservice-data-uat" )'%AWS_S3_BUCKET
        print '\n--S3_FolderKey [%s] (ie. "data-load//6//" )'%AWS_S3_FOLDER_KEY
        sys.exit(2)
    
    print 'executing job'
    execute_job

(SDE_CONNECTION,SDE_FEATURE_CLASS_NAME,TEMP_WORKING_DIRECTORY,SLIP_DATASET_NAME,AWS_CREDENTIAL_PROFILE,AWS_S3_BUCKET,AWS_S3_FOL

DER_KEY)
     
if __name__ == "__main__":
    main(sys.argv[1:])
