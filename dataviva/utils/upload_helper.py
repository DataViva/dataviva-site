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

def save_images_locally(upload_folder, images):
    file_paths = []
    if os.path.exists(upload_folder):
        shutil.rmtree(upload_folder)
    os.makedirs(upload_folder)
    for i, image in images.iteritems():
        file_path = os.path.join(upload_folder, 'img' + i)
        if image.startswith('data:'):
            image_extension = '.' + image.split(';')[0].split('/')[1]
            image_data = base64.b64decode(image.split(',')[1])    
            with open(file_path + image_extension, 'wb') as f:
                f.write(image_data)       
        else:
            if image.split('.')[-1] in ['jpg', 'jpeg', 'png', 'gif']:
                image_extension = '.' + image.split('.')[-1]
            else:
                image_extension = '.png'
            urllib.urlretrieve(image, file_path + image_extension)
        file_paths.append( { 'id': i, 'path': file_path + image_extension } )
    return file_paths

def upload_images_to_s3(html, object_type, object_id):
    prefix = os.path.join(object_type, str(object_id), 'images/content/')
    soup = BeautifulSoup(html, 'html.parser')
    file_paths = []
    for img in soup.findAll('img', src=True):
        if img['src'] == '':
            pass
        file_paths.append(img['src'])

    files = s3_client().list_objects(Bucket='dataviva-dev', Prefix=prefix)
    if files.has_key('Contents'):
        for file in files['Contents']:
            s3_client().delete_object(Bucket='dataviva-dev', Key=file['Key'])

    urls = []
    for file_path in file_paths:
        image_url = upload_s3_file(file_path, prefix + file_path.split('/')[-1], {'ContentType': "image/" + file_path.split('.')[-1] })
        html = re.sub(file_path, image_url, html)
    
    return html

