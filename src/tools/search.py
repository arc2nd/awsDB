#!/usr/bin/env python

# builtin imports
import sys
import typing
import pathlib
import argparse
import traceback

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

# module imports
from setup_scripts.ORM_models import Assets, Users, Catalogs, BeanLog
from services import hashing, filedata, userdata, connection
from services.log import _logger
from config.config import config_obj


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add an file to the database as an asset item")
    parser.add_argument("-an", "--asset_name", action="store", dest="asset_name", nargs=1, default=None, help="The name that you want to give this asset")
    parser.add_argument('-un', '--user_name', action='store', dest='user_name', nargs=1, default=None, help='The name of the user submitting this asset')
    args = parser.parse_args()
    return args


engine, conn = connection.make_connection()


def search(asset_name: str = '', user_name: str = '', tags: typing.List[str] = '', time_range='',) -> typing.Dict:
    with Session(engine) as session:
        # figure out what we can about where this is being submitted from
        my_user_data = userdata.collect_user_data()
        _logger.info(f'my_user_data: {my_user_data}')

        # who is searching
        stmt = select(Users).where(Users.username == user_name)
        searched_by_user = session.execute(stmt).all()[0][0]
        _logger.info(f'searched_by_user: {searched_by_user}')

        all_assets = []
        if asset_name and asset_name != '':
            found_assets = session.execute(select(Assets).where(Assets.name == asset_name).order_by(Assets.version.desc())).all()
            for asset in found_assets:
                all_assets.append(asset)
            _logger.info(f'all_assets: {all_assets}')
        # elif user_name and user_name != '':
        #     this_user = session.execute(select(Users).where(Users.username == user_name)).first()
        #     stmt = select(Assets).where(Assets.created_by == this_user[0].id).order_by(Assets.version.desc())
        #     all_assets = session.execute(stmt).all()

            new_bean = BeanLog(level='info',
                               app_name='Search',
                               user=my_user_data['user'],
                               hostname=my_user_data['hostname'],
                               ipaddress=my_user_data['ip'],
                               platform=my_user_data['platform'],
                               message=f'{searched_by_user.username} searched for {asset_name}'
                               )

            try:
                session.add_all([new_bean])
                session.commit()
            except:
                traceback.print_exc()

            return all_assets


def search_string(search_string: str = '') -> typing.Dict:
    search_text = "%{}%".format(search_string)
    assets = Assets.query.filter(Assets.tags.like(search_text)).all()
    catalogs = Catalogs.query.filter(Catalogs.name.like(search_text)).all()
    users = Users.query.filter(Users.name.like(search_text)).all()
    return {'assets': assets,
            'catalogs': catalogs,
            'users': users
            }


if __name__ == '__main__':
    # collect information from the CLI
    my_args = parse_args()
    # all_assets = search(asset_name=my_args.asset_name[0], user_name=my_args.user_name[0])
    search_results = search_string(search_string='cats_test_image')
    # _logger.info(all_assets)
    _logger.info(search_results)