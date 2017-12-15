import arcpy
import os
import shutil

# Function Name: sde2shp()
# Purpose:
#   Function to export a SDE feature class to a ESRI shapefile
#   The function will return location of the shapefile. ie C:\AARON_DATA\LGATE071.shp
#          
# usage:
#      sde2shp <SDE_Connection> <SDE_FC_Name> <output_path> <Output_shapefile_name>
def sde2shp(sde_connection,featureclass_name,output_path,outputSHPname):
    #establish sde connection workspace
    arcpy.env.workspace = sde_connection
    #does the shapefile exists is so delete it
    if arcpy.Exists(output_path+'//'+outputSHPname):
        arcpy.Delete_management(output_path+'//'+outputSHPname)
    #Export the sde featureclass to the esri shapefile
    arcpy.FeatureClassToFeatureClass_conversion(featureclass_name, 
                                            output_path, 
                                            outputSHPname)
    #drop SDE connection 
    arcpy.ClearWorkspaceCache_management()
    return output_path+'\\'+outputSHPname
