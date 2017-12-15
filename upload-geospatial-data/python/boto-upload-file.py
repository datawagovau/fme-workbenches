import boto3

# Use 'aws configure --profile SLIP_SelfService' to create a profile with your s3 credentials.

def UploadFile(source_file, bucket, key, aws_profile):
    session = boto3.Session(profile_name= aws_profile)
    s3_client = session.client('s3')
    s3_client.upload_file(source_file, bucket, key)
    file_url = '{0}/{1}/{2}'.format(s3_client.meta.endpoint_url, bucket, key)
    return file_url
