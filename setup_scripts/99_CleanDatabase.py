#!/usr/bin/env python

import traceback

from sqlalchemy import MetaData, Table, Column, ForeignKey, Integer, String, Time
from sqlalchemy_utils import database_exists

from awsDB.services import connection
from awsDB.setup_scripts.ORM_models import Base

# create the engine and conn objects
engine, conn = connection.make_connection()


def drop_table(table_name: str = None, engine=None):
    """
    drop a table

    Args:
        table_name: the name of the table you want dropped
        engine: the sqlalchemy engine object

    Returns:

    """
    base = Base
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables.get(table_name)
    if table is not None:
        print('Deleting {} table'.format(table_name))
        base.metadata.drop_all(engine, [table], checkfirst=True)


if database_exists(engine.url):
    # TODO: implement drop cascade so that table order in this list does not matter
    list_of_tables = ['access_records', 'catalogs', 'assets', 'users', 'roles', 'bean_log', 'system_values']

    for this_table in list_of_tables:
        try:
            drop_table(this_table, engine)
        except:
            print(f'Could not drop {this_table}')
            traceback.print_exc()
