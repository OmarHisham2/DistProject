import uuid
import boto3

s3 = boto3.resource('s3')


s3.meta.client.upload_file('image1.png','bucket441122',str(uuid.uuid4())+'.png')

