import boto3
from boto3.s3.transfer import S3Transfer
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY


def delete_s3_file(file_id):
    client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    return client.delete_object(
        Bucket='dataviva',
        Key=file_id
    )


def upload_s3_file(file_path, bucket, file_id, extra_args={'ContentType': "html/text"}):
    client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    transfer = S3Transfer(client)

    return transfer.upload_file(file_path, bucket, file_id, extra_args=extra_args)
