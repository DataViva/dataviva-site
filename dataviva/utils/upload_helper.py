import boto3
import os
import base64
import shutil
from boto3.s3.transfer import S3Transfer
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET, UPLOAD_FOLDER
import urllib
import re
from bs4 import BeautifulSoup

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

def list_s3_files(prefix):
    return s3_client().list_objects(
        Bucket=S3_BUCKET, 
        Prefix=prefix
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

    shutil.rmtree(os.path.split(upload_folder)[0])

    return image_url

def upload_images_to_s3(html, object_type, object_id):
    client = s3_client()
    domain = 'https://' + S3_BUCKET + '.s3.amazonaws.com/'
    prefix = os.path.join(object_type, str(object_id), 'images/content/')
    soup = BeautifulSoup(html, 'html.parser')
    new_urls = []
    all_keys = []
    for img in soup.findAll('img', src=True):
        if img['src'].startswith(domain):
            all_keys.append(img['src'].split(domain)[1])
        if img['src'].startswith(domain + 'uploads/'):
            new_urls.append(img['src'])
    for url in new_urls:
        copy_source = {
            'Bucket': S3_BUCKET,
            'Key': url.split(domain)[1]
        }
        new_key = prefix + url.split('/')[-1]
        client.copy_object(Bucket=S3_BUCKET, CopySource=copy_source, Key=new_key)
        client.delete_object(Bucket=S3_BUCKET, Key=copy_source['Key'])
        html = re.sub(url, 'https://' + S3_BUCKET + '.s3.amazonaws.com/' + new_key, html)
    uploaded_images = list_s3_files(prefix)
    if uploaded_images.has_key('Contents'):
        for image in uploaded_images['Contents']:
            if image['Key'] not in all_keys:
                delete_s3_file(image['Key'])
    return html
