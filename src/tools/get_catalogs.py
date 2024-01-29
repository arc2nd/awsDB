#!/usr/bin/env python

import sys
import typing
import argparse
import traceback

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
sys.path.append('..')

from setup_scripts.ORM_models import Catalogs
from services import hashing, filedata, userdata, connection
from services.log import _logger
from config.config import config_obj


engine, conn = connection.make_connection()

def get_catalogs() -> typing.List[str]:
    with Session(engine) as session:
        stmt = select(Catalogs)
        all_catalogs = session.execute(stmt)
        catalogs = []
        for this_object in all_catalogs.all():
            catalogs.append(this_object[0].name)
    return catalogs

if __name__ == '__main__':
    catalogs = get_catalogs()
    print(catalogs)
    _logger.info(catalogs)
