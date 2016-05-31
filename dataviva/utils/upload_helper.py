import boto3
from boto3.s3.transfer import S3Transfer
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET


def delete_s3_file(file_id):
    client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    return client.delete_object(
        Bucket=S3_BUCKET,
        Key=file_id
    )


def upload_s3_file(file_path, file_id, extra_args={'ContentType': "html/text"}):
    client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    transfer = S3Transfer(client)
    transfer.upload_file(file_path, S3_BUCKET, file_id, extra_args=extra_args)

    return 'https://' + S3_BUCKET + '.s3.amazonaws.com/' + file_id
