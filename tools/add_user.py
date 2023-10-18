#!/usr/bin/env python

# builtin imports
import os
import typing
import logging
import argparse
import datetime
import traceback

# pip imports
from sqlalchemy.orm import Session
from sqlalchemy import select

# module imports
from awsDB.setup_scripts.ORM_models import Assets, Users, BeanLog, AccessRecord, Catalog
from awsDB.services import thumbnailer, hashing, filedata, userdata, connection, s3
from awsDB.services.log import _logger
from awsDB.config import config

def parse_args():
    parser = argparse.ArgumentParser(description="Add an file to the database as an asset item")
    parser.add_argument('-un', '--user_name', action='store', dest='user_name', nargs=1, default=None, help='The name of the user submitting this asset')
    parser.add_argument('-rl', '--role', action='store', dest='role', nargs=1, default='artist', help='The name of the catalog you are submitting to')
    args = parser.parse_args()
    return args


def add_user(username, first_name, last_name, email_address, role, added_by):
    engine, conn = connection.make_connection()

    with Session(engine) as session:
        # figure out what we can about where this is being submitted from
        my_user_data = userdata.collect_user_data()
        _logger.info(f'my_user_data: {my_user_data}')

        # who is submitting
        stmt = select(Users).where(Users.username == added_by)
        added_by_user = session.execute(stmt).all()[0][0]
        _logger.info(f'added_by_user: {added_by_user}')

        # make and add the asset to the database
        new_user = Users(username=username,
                         first_name=first_name,
                         last_name=last_name,
                         email_address=email_address,
                         role=role,
                         created_by=added_by_user.id,
                         created=datetime.datetime.now())
        new_bean = BeanLog(level='info',
                           app_name='Submit',
                           user=my_user_data['user'],
                           hostname=my_user_data['hostname'],
                           ipaddress=my_user_data['ip'],
                           platform=my_user_data['platform'],
                           message=f'{added_by_user.username} added user {username}')

        try:
            session.add_all([new_user, new_bean])
            session.commit()
        except:
            traceback.print_exc()
        _logger.info(f'New Asset: {new_user}')


if __name__ == '__main__':
    # collect information from the CLI
    my_args = parse_args()
    _logger.info(my_args)
    _logger.info(userdata.collect_user_data())
    add_user(username=my_args.user_name[0], role=my_args.role[0])
