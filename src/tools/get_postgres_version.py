#!/usr/bin/env python

# builtin imports

# pip imports
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

# module imports
from awsDB.services import connection


def main():
    engine, conn = connection.make_connection()

    with Session(engine) as session:
        stmt = text('SELECT version();')
        version = session.execute(stmt).all()
        return version


if __name__ == '__main__':
    print(main())
