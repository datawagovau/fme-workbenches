import boto3

def UploadFile(source_file):    
    KEY ='<Enter your aws id key here>'
    SECRET = '<Enter your aws secret key here>'
    BUCKET = 'lg-slip-selfservice-data-prod'
    BUCKET_KEY = 'data-load/33'
 
    fname = str(source_file).split('\\')[-1:][0]

    session = boto3.session.Session(aws_access_key_id=KEY, aws_secret_access_key=SECRET, region_name='ap-southeast-2')
    s3_client = session.client('s3')

    s3_client.upload_file(source_file, BUCKET, BUCKET_KEY+"/"+fname)

    file_url = '{0}/{1}/{2}'.format(s3_client.meta.endpoint_url, BUCKET, BUCKET_KEY)
    return file_url
