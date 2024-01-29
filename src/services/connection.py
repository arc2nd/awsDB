#!/usr/bin/env python

# builtin imports
import os
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports
import bcrypt
from sqlalchemy import create_engine, select

# module imports
from services import creds
from config.config import config_obj
from services.log import _logger

if config_obj.test:
    creds_path = os.path.expanduser(config_obj.test_db_creds)
else:
    creds_path = os.path.expanduser(config_obj.db_creds)
print(f'Creds path: {creds_path}: {pathlib.Path(creds_path).exists()}')
my_creds = creds.get_creds(path=creds_path)
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
    _logger.info(f'connecting to: {my_creds["DB_TYPE"]}@{my_creds["DB_ENDPOINT"]}')
    engine = create_engine(CONNECTION_STRING)
    conn = engine.connect()
    return engine, conn

