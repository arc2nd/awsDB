#!/usr/bin/env python

# builtin imports
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports

# module imports
from services import connection
from ORM_models import Base, Roles, Users, Assets, Catalogs, AccessRecords, BeanLog

# create the engine and conn objects
engine, conn = connection.make_connection()

# create the tables in the DB
Base.metadata.create_all(engine)
