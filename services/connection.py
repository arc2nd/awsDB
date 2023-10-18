#!/usr/bin/env python

# builtin imports
import os

# pip imports
import bcrypt
from sqlalchemy import create_engine, select

# module imports
from awsDB.services import creds

my_creds = creds.get_creds(path=os.path.join(creds.CREDS_BASE_PATH, 'local_creds.crypt'))
CONNECTION_STRING = f'{my_creds["DB_TYPE"]}://{my_creds["MASTER_USER"]}:{my_creds["PASSWORD"]}@{my_creds["DB_ENDPOINT"]}:{my_creds["PORT"]}/{my_creds["DB_NAME"]}'


def encrypt_password(password_to_encrypt=None):
    """
    Hash a password

    Args:
        password_to_encrypt: the plaintext password that you want to hash

    Returns:
        password_to_encrypt: that password after being run through bcrypt
    """
    password_to_encrypt = password_to_encrypt.encode('utf-8')
    password_to_encrypt = bcrypt.hashpw(password_to_encrypt, bcrypt.gensalt(12)).decode('utf-8')
    return password_to_encrypt


def make_connection():
    """
    Instantiate the sqlalchemy engine and connection objects using the CONNECTION_STRING gVar in this file

    Returns:
        engine: the sqlalchemy engine object
        conn: the sqlalchemy connection object
    """
    print(f'connecting to: {my_creds["DB_TYPE"]}@{my_creds["DB_ENDPOINT"]}')
    print(f'Connection String: {CONNECTION_STRING}')
    engine = create_engine(CONNECTION_STRING)
    conn = engine.connect()
    return engine, conn

