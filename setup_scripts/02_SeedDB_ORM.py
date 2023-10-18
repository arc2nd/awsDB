#!/usr/bin/env python

# builtin imports
import os
import json
import datetime

# pip imports
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# module imports
from awsDB.services import connection
from ORM_models import Base, Roles, Users, Assets, Catalog, AccessRecord, BeanLog

# create the engine and conn objects
engine, conn = connection.make_connection()

# create the admin, dev, and artist roles
with Session(engine) as session:
    admin_role = Roles(name='admin', created=datetime.datetime.now())
    dev_role = Roles(name='dev', created=datetime.datetime.now())
    artist_role = Roles(name='artist', created=datetime.datetime.now())

    session.add_all([admin_role, dev_role, artist_role])
    session.commit()

# create the admin user
with Session(engine) as session:
    stmt = select(Roles).where(Roles.name == 'admin')
    admin_role = session.execute(stmt).all()[0][0]
    admin_user = Users(username='admin',
                  first_name='James',
                  last_name='Kirk',
                  password=connection.encrypt_password('12345'),
                  email_address='jkirk@starfleet.com',
                  role_id=admin_role.id,
                  created=datetime.datetime.now()
                  )

    session.add_all([admin_user])
    session.commit()

# create the reference catalog
with Session(engine) as session:
    stmt = select(Users).where(Users.username == 'admin')
    admin_user = session.execute(stmt).all()[0][0]
    config_path = os.path.join(os.path.dirname(__file__), 'catalog_config.json')
    with open(config_path, 'r') as fp:
        catalog_config_dict = json.load(fp)
    print(admin_user)
    reference_catalog = Catalog(name='Reference',
                                config=json.dumps(catalog_config_dict),
                                created_by=admin_user.id
                                )
    session.add_all([reference_catalog])
    session.commit()

# add the reference assets


