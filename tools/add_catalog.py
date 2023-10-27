#!/usr/bin/env python

# builtin imports
import os
import json
import typing
import argparse
import datetime
import traceback

# pip imports
from sqlalchemy.orm import Session
from sqlalchemy import select

# module imports
from awsDB.setup_scripts.ORM_models import Assets, Users, BeanLog, AccessRecords, Catalogs
from awsDB.services import thumbnailer, hashing, filedata, userdata, connection, s3
from awsDB.services.log import _logger
from awsDB.config.config import config_obj

def parse_args():
    parser = argparse.ArgumentParser(description="Add a catalog to the database")
    parser.add_argument('-un', '--user_name', action='store', dest='user_name', nargs=1, default=None, help='The name of the user creating this catalog')
    parser.add_argument('-cp', '--config_path', action='store', dest='config_path', nargs=1, default="../setup_scripts/catalog_config.json", help='The config JSON for this catalog')
    parser.add_argument('-ct', '--catalog', action='store', dest='catalog', nargs=1, default='reference', help='The name of the catalog you are creating')
    args = parser.parse_args()
    return args


def add_catalog(name, config_path, added_by):
    engine, conn = connection.make_connection()

    with Session(engine) as session:
        # figure out what we can about where this is being submitted from
        my_user_data = userdata.collect_user_data()
        _logger.info(f'my_user_data: {my_user_data}')

        # who is submitting
        stmt = select(Users).where(Users.username == added_by)
        added_by_user = session.execute(stmt).all()[0][0]
        _logger.info(f'added_by_user: {added_by_user}')

        with open(config_path, 'r') as fp:
            new_config = json.dumps(json.load(fp))

        new_catalog = Catalogs(name=name,
                               config=new_config,
                               created_by=added_by_user.id,
                               created=datetime.datetime.now()
                               )
        new_bean = BeanLog(level='info',
                           app_name='New Catalog',
                           user=my_user_data['user'],
                           hostname=my_user_data['hostname'],
                           ipaddress=my_user_data['ip'],
                           platform=my_user_data['platform'],
                           message=f'{added_by_user.username} added catalog {new_catalog.name}'
                           )

        try:
            session.add_all([new_catalog, new_bean])
            session.commit()
        except:
            traceback.print_exc()
        _logger.info(f'New Catalog: {new_catalog}')


if __name__ == '__main__':
    # collect information from the CLI
    my_args = parse_args()
    _logger.info(my_args)
    _logger.info(userdata.collect_user_data())
    add_catalog(name=my_args.catalog[0], added_by=my_args.user_name[0])
