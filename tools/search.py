#!/usr/bin/env python

import typing
import argparse
import datetime

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from awsDB.setup_scripts.ORM_models import Assets, Users, Catalog
from awsDB.services import hashing, filedata, userdata, connection

def parse_args():
    parser = argparse.ArgumentParser(description="Add an file to the database as an asset item")
    parser.add_argument("-an", "--asset_name", action="store", dest="asset_name", nargs=1, default=None, help="The name that you want to give this asset")
    parser.add_argument('-un', '--user_name', action='store', dest='user_name', nargs=1, default=None, help='The name of the user submitting this asset')
    args = parser.parse_args()
    return args


engine, conn = connection.make_connection()


def search(asset_name: str = '', user_name: str = '', tags: typing.List[str] = '', time_range=''):
    with Session(engine) as session:
        if asset_name and asset_name != '':
            all_assets = session.execute(select(Assets).where(Assets.name == asset_name).order_by(Assets.version.desc())).all()
        elif user_name and user_name != '':
            this_user = session.execute(select(Users).where(Users.username == user_name)).first()
            stmt = select(Assets).where(Assets.created_by == this_user[0].id).order_by(Assets.version.desc())
            all_assets = session.execute(stmt).all()
    return all_assets

if __name__ == '__main__':
    # collect information from the CLI
    my_args = parse_args()
    all_assets = search(asset_name=my_args.asset_name[0])
    print(all_assets)
