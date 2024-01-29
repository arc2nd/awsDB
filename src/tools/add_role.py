#!/usr/bin/env python

# builtin imports
import argparse
import datetime
import traceback

# pip imports
from sqlalchemy.orm import Session
from sqlalchemy import select

# module imports
from awsDB.setup_scripts.ORM_models import Assets, Roles, Users, BeanLog, AccessRecords, Catalogs
from awsDB.services import thumbnailer, hashing, filedata, userdata, connection, s3
from awsDB.services.log import _logger
from awsDB.config.config import config_obj


def parse_args():
    parser = argparse.ArgumentParser(description="Add an user to the database")
    parser.add_argument('-rn', '--role_name', action='store', dest='role_name', nargs=1, default=None, help='The name for this role')
    parser.add_argument('-ab', '--added_by', action='store', dest='added_by', nargs=1, default=None, help='Who is adding this user')
    args = parser.parse_args()
    return args


def add_role(role_name, added_by):
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
        new_role = Roles(name=role_name,
                         created=datetime.datetime.now()
                         )
        new_bean = BeanLog(level='info',
                           app_name='New Role',
                           user=my_user_data['user'],
                           hostname=my_user_data['hostname'],
                           ipaddress=my_user_data['ip'],
                           platform=my_user_data['platform'],
                           message=f'{added_by_user.username} added role {role_name}'
                           )

        try:
            session.add_all([new_role, new_bean])
            session.commit()
        except:
            traceback.print_exc()
        _logger.info(f'New Role: {new_role}')


if __name__ == '__main__':
    # collect information from the CLI
    my_args = parse_args()
    _logger.info(my_args)
    _logger.info(userdata.collect_user_data())
    add_role(role_name=my_args.role_name[0],
             added_by=my_args.added_by[0])
