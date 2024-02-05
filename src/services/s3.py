#!/usr/bin/env python

# builtin imports
import os
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports
import boto3
from boto3.s3.transfer import TransferConfig

# module imports
from services import creds
from config.config import config_obj
from services.log import _logger

if config_obj.test:
    creds_path = config_obj.test_s3_creds
else:
    creds_path = config_obj.s3_creds

s3_creds = creds.get_creds(path=os.path.expanduser(creds_path))


##
# This gets an s3 resource using the aws creds found in the config dictionary
##
def establish_s3_resource():
    GB = 1024 ** 3
    config = TransferConfig(multipart_threshold=3*GB)

    #   resource
    s3_res = boto3.resource('s3', aws_access_key_id=s3_creds['AWS_ACCESS_KEY'], aws_secret_access_key=s3_creds['AWS_SECRET_ACCESS_KEY'])
    return s3_res


def get_s3_path(aws_folder='', filepath=''):
    return f'{aws_folder}/{filepath}'


def to_aws(filepath: str = None,
           catalog: str = None,
           asset_name: str = None,
           version: int = 1,
           s3_resource=None) -> str:
    if not s3_resource:
        s3_resource = establish_s3_resource()
    aws_path = get_s3_path(aws_folder=f'{catalog}/{asset_name}/{str(version).zfill(3)}', filepath=os.path.basename(filepath))
    s3_resource.meta.client.upload_file(filepath, s3_creds['BUCKET'], aws_path)
    return aws_path

# TODO: There's got to be a better/faster way to do this.
def from_aws(dst_path=None,
             file_name=None,
             catalog: str = None,
             asset_name: str = None,
             version: int = 1,
             s3_resource=None):
    if not s3_resource:
        s3_resource = establish_s3_resource()
    aws_path = get_s3_path(aws_folder=f'{catalog}/{asset_name}/{str(version).zfill(3)}', filepath=file_name)
    s3_resource.meta.client.download_file(s3_creds['BUCKET'], aws_path, dst_path)
    return dst_path


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
        sys.stdout.write('')
        sys.stdout.flush()

    return aws_path




