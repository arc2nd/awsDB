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
    parser.add_argument('search_string', action="store", nargs=1, default=None, help="The string we're going to search for")
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


def search_string(search_string: str = '',
                  asset: bool = True,
                  catalog: bool = False,
                  user: bool = False) -> typing.Dict:
    search_text = f'%{search_string}%'

    return_assets = []
    return_catalogs = []
    return_users = []
    return_roles = []

    with Session(engine) as session:
        # figure out what we can about where this is being submitted from
        my_user_data = userdata.collect_user_data()
        _logger.info(f'my_user_data: {my_user_data}')

        # who is searching
        stmt = select(Users).where(Users.username == user)
        searched_by_user = session.execute(stmt).all()[0][0]
        _logger.info(f'searched_by_user: {searched_by_user}')

        # The Search
        #     things to search for in Assets
        return_assets.extend(session.query(Assets).filter(Assets.name.ilike(search_text)).all())
        return_assets.extend(session.query(Assets).filter(Assets.path.ilike(search_text)).all())
        return_assets.extend(session.query(Assets).filter(Assets.source_path.ilike(search_text)).all())

        #     things to search for in Catalogs
        return_catalogs.extend(session.query(Catalogs).filter(Catalogs.name.ilike(search_text)).all())

        #     things to search for in Users
        return_users.extend(session.query(Users).filter(Users.username.ilike(search_text)).all())
        return_users.extend(session.query(Users).filter(Users.first_name.ilike(search_text)).all())
        return_users.extend(session.query(Users).filter(Users.last_name.ilike(search_text)).all())
        return_users.extend(session.query(Users).filter(Users.email_address.ilike(search_text)).all())

        #     things to search for in Roles
        return_roles.extend(session.query(Roles).filter(Roles.name.ilike(search_text)).all())

        # new_bean = BeanLog(level='info',
        #                    app_name='Search',
        #                    user=my_user_data['user'],
        #                    hostname=my_user_data['hostname'],
        #                    ipaddress=my_user_data['ip'],
        #                    platform=my_user_data['platform'],
        #                    message=f'{searched_by_user.username} searched for {search}'
        #                    )
        #
        # try:
        #     session.add_all([new_bean])
        #     session.commit()
        # except:
        #     traceback.print_exc()

    return {'assets': list(set(return_assets)),
            'catalogs': list(set(return_catalogs)),
            'users': list(set(return_users)),
            'roles': list(set(return_roles)),
            }


if __name__ == '__main__':
    # collect information from the CLI
    my_args = parse_args()
    search_results = search_string(search=my_args.search_string[0], user_name=my_args.user_name[0])
    _logger.info(search_results)
