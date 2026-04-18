import boto3
import os

s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET_NAME']


def generate_upload_url(file_name):
    return s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': BUCKET,
            'Key': file_name
        },
        ExpiresIn=300
    )


def list_files():
    response = s3.list_objects_v2(Bucket=BUCKET)
    return [obj['Key'] for obj in response.get('Contents', [])]