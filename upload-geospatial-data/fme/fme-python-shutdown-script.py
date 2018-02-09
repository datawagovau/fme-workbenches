import fme
import os
import shutil
import zipfile
import boto3

# fuction to upload your data to aws S3
def UploadFile(source_file, bucket, bucket_key, aws_key, aws_secret):
    fname = str(source_file).split('\\')[-1:][0]
    session = boto3.session.Session(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret,region_name='ap-southeast-2')
    s3_client = session.client('s3')
    s3_client.upload_file(source_file, bucket, bucket_key + "/" + fname)
    file_url = '{0}/{1}/{2}'.format(s3_client.meta.endpoint_url, bucket, bucket_key)
    return file_url

# Creates a zip file containing the input shapefile
#   inShp: Full path to shapefile to be zipped
#   Delete: Set to True to delete shapefile files after zip
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

# Creates a zip file containing the input shapefile
#   inShp: Full path to shapefile to be zipped
#   Delete: Set to True to delete shapefile files after zip
def ZipShp (inShp, Delete = True):
    #List of shapefile file extensions
    extensions = [".shp",".shx",".dbf",".sbn",".sbx",".fbn",".fbx",".ain",".aih",".atx",".ixs",".mxs",".prj",".xml",".cpg",".shp.xml"]
    #Directory of shapefile
    inLocation = os.path.dirname (inShp)
    #Base name of shapefile
    inName = os.path.basename (os.path.splitext (inShp)[0])
    #Create zipfile name
    zipfl = os.path.join (inLocation, inName + ".zip")
    #Create zipfile object
    ZIP = zipfile.ZipFile (zipfl, "w")
    #Empty list to store files to delete
    delFiles = []
    #Iterate files in shapefile directory
    for fl in os.listdir (inLocation):
        #Iterate extensions
        for extension in extensions:
            #Check if file is shapefile file
            if fl == inName + extension:
                #Get full path of file
                inFile = os.path.join (inLocation, fl)
                #Add file to delete files list
                delFiles += [inFile]
                #Add file to zipfile
                ZIP.write (inFile, fl)
                break
    #Delete shapefile if indicated
    if Delete == True:
        for fl in delFiles:
            os.remove (fl)
    #Close zipfile object
    ZIP.close()
    #Return zipfile full path
    return zipfl

def main():
    try:
        # Parse required fme published parameters
        # note the parameters must match the paramters names used in fme workbench
        print 'Executing the SLIP Selfservice automation script.'

        x = fme.macroValues

        AWS_KEY = x['AWS_ACCESS_KEY']
        AWS_SECRET_KEY = x['AWS_SECRET']
        BUCKET = x['S3_BUCKET']
        BUCKET_KEY = x['S3_BUCKET_KEY']
        UPLOAD = x['UP_LOAD_TO_S3']

        OUTPUT_DATA = ''

        # What is the name of the output
        if x.has_key("DestDataset_FILEGDB"):
            OUTPUT_DATA = x['DestDataset_FILEGDB']

        if x.has_key("DestDataset_ESRISHAPE"):
            featureType = fme.featuresWritten.keys()[0]
            print 'featureType is: ' + featureType

            shapefileName = featureType + '.SHP'

            OUTPUT_DATA = os.path.join(x['DestDataset_ESRISHAPE'], shapefileName)

        print 'OUTPUT_DATA is: ' + OUTPUT_DATA

        #Check the extension of my output data
        extension = str(os.path.splitext(OUTPUT_DATA)[1])

        print 'extension is: ' + extension

        if extension.upper() == '.GDB':
            my_zip_path = Zipfgdb(OUTPUT_DATA, False)
            print 'compressed version of your data is stored ' + my_zip_path

            if UPLOAD == "Yes":
                url = UploadFile(my_zip_path,BUCKET,BUCKET_KEY,AWS_KEY,AWS_SECRET_KEY)
                print 'Your Data has been uploaded to ' + url
        else:
            my_zip_path = ZipShp(OUTPUT_DATA, False)
            print 'compressed version of your data is stored ' + my_zip_path

            if UPLOAD == "Yes":
                url  = UploadFile(my_zip_path,BUCKET,BUCKET_KEY,AWS_KEY,AWS_SECRET_KEY)
                print 'Your Data has been uploaded to ' + url
    except:
        print("Unexpected error when executing the SLIP Selfservice automation script.:", sys.exc_info()[0])
        raise

if __name__ == "__main__":
    main()

