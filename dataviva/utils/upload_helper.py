import boto3
import os
from boto3.s3.transfer import S3Transfer

ACCESS_KEY = os.environ['DATAVIVA_OAUTH_ACCESS_KEY_ID']
SECRET_KEY = os.environ['DATAVIVA_OAUTH_SECRET_KEY_SECRET']


def upload_s3_file(file_id):
    client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )

    return client.delete_object(
        Bucket='dataviva',
        Key=file_id
    )


def delete_s3_file(file_path, bucket, file_id, extra_args={'ContentType': "html/text"}):
    client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )

    transfer = S3Transfer(client)

    transfer.upload_file(file_path, bucket, file_id, extra_args)
