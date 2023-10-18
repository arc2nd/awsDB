#!/usr/bin/env python

# builtin imports
import os

# pip imports
import boto3
from boto3.s3.transfer import TransferConfig

# module imports
from awsDB.services import creds

aws_creds = creds.get_creds(path=os.path.join(creds.CREDS_BASE_PATH, 's3_creds.crypt'))


##
# This gets an s3 resource using the aws creds found in the config dictionary
##
def establish_s3_resource():
    GB = 1024 ** 3
    config = TransferConfig(multipart_threshold=3*GB)

    #   resource
    s3_res = boto3.resource('s3', aws_access_key_id=aws_creds['AWS_ACCESS_KEY'], aws_secret_access_key=aws_creds['AWS_SECRET_ACCESS_KEY'])
    return s3_res


def get_s3_path(aws_folder='', filepath=''):
    return f'{aws_folder}/{filepath}'


def to_aws(filepath=None, catalog=None, asset_name=None, version: int = 1):
    s3_resource = establish_s3_resource()
    aws_path = get_s3_path(aws_folder=f'{catalog}/{asset_name}/{str(version).zfill(3)}', filepath=os.path.basename(filepath))
    s3_resource.meta.client.upload_file(filepath, aws_creds['BUCKET'], aws_path)
    return aws_path


##
# The better way to do this would be to assemble all the parts
# for the asset entry and then upload them all in a single
# function call instead of one function call per file
#
# Also, there's no fle validation offered here, that'll have
# to be a separate thing
##
def list_all(filepath, bucket, aws_folder, s3_res=None):
    import sys
    if not s3_res:
        s3_res = establish_s3_resource()
    aws_path = '{}/{}'.format(aws_folder, os.path.basename(filepath))
    s3_res.meta.client.upload_file(filepath, bucket, aws_path)

    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    return aws_path

##
# Placeholder to retrieve items from aws
##
def from_aws(bucket, s3_res=None):
    if not s3_res:
        s3_res = establish_s3_resource()
    this_bucket = s3_res.Bucket(bucket)
    for item in this_bucket.objects.all():
        # print(dir(item))
        print(item._key)

def from_aws1(bucket, src, dst, s3_res=None):
    if not s3_res:
        s3_res = establish_s3_resource()
    this_bucket = s3_res.Bucket(bucket)
    with open(dst, 'wb') as fp:
        this_bucket.download_fileobj(src, fp)



