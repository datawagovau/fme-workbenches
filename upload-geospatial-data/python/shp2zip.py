import os
import shutil
import zipfile

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
