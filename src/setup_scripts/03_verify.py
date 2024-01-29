#!/usr/bin/env python

# builtin imports
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports

from sqlalchemy import select, inspect
from sqlalchemy.orm import Session

# module imports
from services import connection
from ORM_models import Base, Roles, Users, Assets, Catalogs, BeanLog, AccessRecords

# create the engine and conn objects
engine, conn = connection.make_connection()

# inspect the schema
inspector = inspect(engine)
schemas = inspector.get_schema_names()

for schema in schemas:
    print("schema: %s" % schema)
    for table_name in inspector.get_table_names(schema=schema):
        print(f'\t{table_name}')
        for column in inspector.get_columns(table_name, schema=schema):
            print("Column: %s" % column)

# list tables
print('\n\n## TABLES')
for schema in schemas:
    print("schema: %s" % schema)
    for table_name in inspector.get_table_names(schema=schema):
        print(f'\t{table_name}')

# list user roles
print('\n\n### ROLES')
with Session(engine) as session:
    stmt = select(Roles)
    all_roles = session.execute(stmt)
    for this_object in all_roles.all():
        print(f'ID: {this_object[0].id}')
        print(f'{this_object[0]}')

# list users
print('\n\n### USERS')
with Session(engine) as session:
    stmt = select(Users)
    all_users = session.execute(stmt)
    for this_object in all_users.all():
        print(f'ID: {this_object[0].id}')
        print(f'{this_object[0]}')

# list catalogs
print('\n\n### CATALOGS')
with Session(engine) as session:
    stmt = select(Catalogs)
    all_catalogs = session.execute(stmt)
    for this_object in all_catalogs.all():
        print(f'ID: {this_object[0].id}')
        print(f'{this_object[0]}')
