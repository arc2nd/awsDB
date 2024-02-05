#!/usr/bin/env python

import sys
import typing
import argparse
import traceback

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
sys.path.append('..')

from setup_scripts.ORM_models import Users
from services import hashing, filedata, userdata, connection
from services.log import _logger
from config.config import config_obj


engine, conn = connection.make_connection()

def get_users() -> typing.List[str]:
    with Session(engine) as session:
        stmt = select(Users)
        all_users = session.execute(stmt)
        users = []
        for this_object in all_users.all():
            users.append(this_object[0].name)
    return users

def get_user_by_id(id: int = 1) -> str:
    with Session(engine) as session:
        return session.query(Users).filter(Users.id == id).one().username


def get_user_by_name(name: str = '') -> Users:
    with Session(engine) as session:
        return session.query(Users).filter(Users.username == name).one()

if __name__ == '__main__':
    users = get_users()
    print(users)
    _logger.info(users)
