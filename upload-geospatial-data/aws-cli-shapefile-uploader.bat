: Date stamp the name of the zipfile
set ZIPFILE=METADATA_%date:~10,4%_%date:~7,2%_%date:~4,2%-%TIME:~0,2%h%TIME:~3,2%m.zip

: path to Shapefile to compress
set SHP=C:\AARON_DATA\slip_upload_test\GDB-Metadata.shp

: path to Output the zip file
set ZIP_PATH=C:\AARON_DATA\slip_upload_test\

: Use the winzip command tool to compress the 
zip -j -9 %ZIP_PATH%%ZIPFILE%  %SHP:~0,-3%* 

: Set Bucket Path
set AWSBUCKET=s3://lg-slip-selfservice-data-uat/data-load/6/

: Set AWS path
set AWSPROFILE=SLIP_SS_UAT
    
: upload the ZIP FILE to the AWS
aws s3 cp %ZIP_PATH%%ZIPFILE% %AWSBUCKET% --profile %AWSPROFILE% --debug 2>%ZIP_PATH%%ZIPFILE%.log
