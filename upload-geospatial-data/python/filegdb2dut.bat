:    Set location of python executable.
set python_exe="c:\Python27\ArcGIS10.2\python.exe"

:    Set location of selfsevice python code.
set python_source="C:\Users\liagt00\OneDrive - Western Australian Land Information Authority (Landgate)\SLIP_DOCUMENT\SLIP_Automation\ESRI_FGDB_2_SLIP.py"

:    Set SDE Connection
set sde=C:\selfservice_uploads\Connection_to_PEAS71-DISS-SDE.sde 

:    Set SDE FeatureClass to Export
set ifc=GDB.W_IMAGERY_METADATA 

:    Set path where to store logs and the exported the file geodatabase
set wd="C:\Users\liagt00\OneDrive - Western Australian Land Information Authority (Landgate)\SLIP_DOCUMENT\SLIP_Automation"

:    Set the name of the exported FeatureClass Dataset. Note this should be the same name as the dataset already imported into Selfservive.
set ofc=LGATE071

:    Set the aws profile configured with your upload credentials
set aws=SLIP_SS_PROD

:    Set the S3 Selfservice Bucket
set S3Bucket=lg-slip-selfservice-data-prod

:    Set the S3 Bucket Key
set S3BucketKey=data-load/1/

:    Run the python 
%python_exe% %python_source% --sde_Connection %sde% --inputFeatureClass %ifc% --workingDir %wd% --outputFeatureClass %ofc% --aws_profile %aws% --S3_Bucket %S3Bucket% --S3_FolderKey %S3BucketKey%
