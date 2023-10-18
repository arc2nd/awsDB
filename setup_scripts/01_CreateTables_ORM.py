#!/usr/bin/env python

# builtin imports

# pip imports

# module imports
from awsDB.services import connection
from ORM_models import Base, Roles, Users, Assets

# create the engine and conn objects
engine, conn = connection.make_connection()

# create the tables in the DB
Base.metadata.create_all(engine)
