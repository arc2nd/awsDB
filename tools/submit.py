#!/usr/bin/envy python

# builtin imports
import os
import typing
import logging
import argparse
import datetime
import traceback

# pip imports
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

# module imports
from awsDB.setup_scripts.ORM_models import Assets, Users, BeanLog, AccessRecords, Catalogs
from awsDB.services import thumbnailer, hashing, filedata, userdata, connection, s3
from awsDB.services.log import _logger
from awsDB.config import config


# logging.basicConfig()
# _logger = logging.getLogger(__file__)
# _logger.setLevel(logging.INFO)

# TODO: So much error checking
# TODO: Probably a faster way to get the latest version by using DB functions rather than a python max
# TODO: Should we use the hashes to prevent uploading the exact same file twice?


def parse_args():
    parser = argparse.ArgumentParser(description="Add an file to the database as an asset item")
    parser.add_argument('filename', action="store", nargs=1, default=None, help="The filepath of the file we're submitting")
    parser.add_argument("-an", "--asset_name", action="store", dest="asset_name", nargs=1, default=None, help="The name that you want to give this asset")
    parser.add_argument('-un', '--user_name', action='store', dest='user_name', nargs=1, default=None, help='The name of the user submitting this asset')
    parser.add_argument('-ct', '--catalog', action='store', dest='catalog', nargs=1, default='reference', help='The name of the catalog you are submitting to')
    args = parser.parse_args()
    return args


def find_latest(assets: typing.List[Assets]):
    if assets:
        return max(this_asset[0].version for this_asset in assets)
    else:
        return None


def increment_version(initial_version: int = 0) -> int:
    _logger.info(f'\tinitial_version: {initial_version}')
    return int(initial_version + 1)


def submit(asset_name='', path='', user_name='', catalog=''):
    """
    Submit a media asset to the database and the s3 bucket

    Args:
        asset_name: the name to give to the asset in the database
        path: the path to the media file
        user_name: the name of the user who is submitting this media asset
        catalog: the name of the catalog to submit the media asset to

    Returns:
        None
    """
    engine, conn = connection.make_connection()
    with Session(engine) as session:
        # if there was no asset name given use the file name
        if not asset_name:
            asset_name = os.path.splitext(os.path.basename(path))[0]

        # what catalog
        stmt = select(Catalogs).where(Catalogs.name == catalog)
        this_catalog = session.execute(stmt).all()[0][0]

        # figure out what we can about where this is being submitted from
        my_user_data = userdata.collect_user_data()
        _logger.info(f'my_user_data: {my_user_data}')

        # generate a thumbnail
        thumbnail_local_path = thumbnailer.make_thumbnail(src=os.path.abspath(path))
        _logger.info(f'thumbnail_local_path: {thumbnail_local_path}')

        # get information about the asset itself
        asset_size = filedata.get_size(filepath=path)
        asset_hash = hashing.file_hash(in_file=path)
        _logger.info(f'asset_size: {asset_size}')
        _logger.info(f'asset_hash: {asset_hash}')

        # who is submitting
        stmt = select(Users).where(Users.username == user_name)
        this_user = session.execute(stmt).all()[0][0]
        _logger.info(f'this_user: {this_user}')

        # increment version
        version_number = 1
        # stmt = select(Assets).where(Assets.name == asset_name)
        stmt = select(Assets).where(Assets.name == asset_name).order_by(Assets.version.desc())
        # all_assets = session.execute(stmt).all()
        all_assets = session.execute(stmt).first()
        if all_assets:
            version_number = increment_version(all_assets[0].version)
        _logger.info(f'Version: {version_number}')


        # put the asset and thumbnail in s3
        asset_s3_path = s3.to_aws(filepath=path,
                                  catalog=catalog,
                                  asset_name=asset_name,
                                  version=version_number)
        _logger.info(f's3 path: {asset_s3_path}')
        if thumbnail_local_path:
            thumbnail_s3_path = s3.to_aws(filepath=thumbnail_local_path,
                                          catalog=catalog,
                                          asset_name=asset_name,
                                          version=version_number)
        else:
            thumbnail_s3_path = None
        _logger.info(f'asset_s3_path: {asset_s3_path}')
        _logger.info(f'thumbnail_s3_path: {thumbnail_s3_path}')

        # make and add the asset to the database
        new_asset = Assets(name=asset_name,
                           path=asset_s3_path,
                           version=version_number,
                           source_path=os.path.abspath(path),
                           size=asset_size,
                           hash=asset_hash,
                           thumbnail=thumbnail_s3_path,
                           catalog=this_catalog.id,
                           created_by=this_user.id,
                           created=datetime.datetime.now())
        new_bean = BeanLog(level='info',
                           app_name='Submit',
                           user=my_user_data['user'],
                           hostname=my_user_data['hostname'],
                           ipaddress=my_user_data['ip'],
                           platform=my_user_data['platform'],
                           message=f'{this_user.username} submitted asset {asset_name}')
        try:
            session.add_all([new_asset, new_bean])
            session.commit()
        except:
            traceback.print_exc()
        finally:
            if os.path.exists(thumbnail_local_path):
                os.remove(thumbnail_local_path)
        _logger.info(f'New Asset: {new_asset}')

if __name__ == '__main__':
    # collect information from the CLI
    my_args = parse_args()
    _logger.info(my_args)
    _logger.info(userdata.collect_user_data())
    submit(asset_name=my_args.asset_name[0], path=my_args.filename[0], user_name='admin', catalog=my_args.catalog[0])
