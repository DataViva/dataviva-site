import boto3
import os
import base64
import shutil
from boto3.s3.transfer import S3Transfer
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET, UPLOAD_FOLDER


def s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )


def delete_s3_file(file_id):
    return s3_client().delete_object(
        Bucket=S3_BUCKET,
        Key=file_id
    )


def delete_s3_folder(folder_id):
    client = s3_client()
    objects = [{'Key': c['Key']} for c in client.list_objects(Bucket=S3_BUCKET, Prefix=folder_id)['Contents']]
    return client.delete_objects(Bucket=S3_BUCKET, Delete={'Objects': objects})


def upload_s3_file(file_path, file_id, extra_args={'ContentType': "html/text"}):
    transfer = S3Transfer(s3_client())
    transfer.upload_file(file_path, S3_BUCKET, file_id, extra_args=extra_args)

    return 'https://' + S3_BUCKET + '.s3.amazonaws.com/' + file_id


def save_b64_image(b64, upload_folder, name):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, name)
    image_data = base64.b64decode(b64)
    with open(file_path, 'wb') as f:
        f.write(image_data)

    image_url = upload_s3_file(file_path, file_path.split(UPLOAD_FOLDER)[1], {'ContentType': "image/png"})

    shutil.rmtree(upload_folder)

    return image_url
