#!/usr/bin/env python

# builtin imports
import os
import sys
import json
import yaml
import logging
import pathlib

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports

# module imports
#   don't import log because that will get circular
from config import utils

# TODO: develop a method for cascading configs so that each catalog can have customized settings


def get_config(path=''):
    config_dict = None
    try:
        if os.path.exists(path):
            with open(path, 'r') as fp:
                config_dict = json.load(fp)
    except:
        print('couldn\'t open config file on disk, resorting to default config')
    return config_dict

def get_yml_config(path=''):
    config_dict = None
    try:
        if pathlib.Path(path).exists():
            with open(path, 'r') as fp:
                config_dict = yaml.safe_load(fp)
    except:
        print('couldn\'t open config file on disk, resorting to default config')
    return config_dict


config_path = os.path.join(os.path.dirname(__file__), 'config.json')
config_dict = get_config(config_path)
if not config_dict:
    # dictionary of configuration strings
    # CONSTANTS
    config_dict = {
        'aws_creds':             '~/scripts/awsDB/src/creds/s3_creds.crypt',
        'db_creds':              '~/scripts/awsDB/src/creds/db_creds.crypt',
        'broker_creds':          '~/scripts/awsDB/src/creds/broker_creds.crypt',
        'test_db_creds':        '~/scripts/awsDB/src/creds/test_db_creds.crypt',
        'errormail':             'james_kirk@starfleet.com',
        'logfile':               'testLog.log',
        'loglevel':              'debug',
        'ffmpeg_loglevel':       'error',
        'thumbnail_x_size':      '320',
        'thumbnail_y_size':      '240',
        'movie_thumbnail_frame': '00:00:15',
        'thumbnail_extension':   '.jpg',
        'test': True
    }
config_obj = utils.dict2obj(config_dict)


def get_value(key):
    """
    Given a key, return its value from the config dict

    Args:
        key: the key whose value we're looking for

    Returns:
        the value of said key
    """
    try:
        if key == 'loglevel':
            if config_dict[key].lower() == 'debug':
                return logging.DEBUG
            elif config_dict[key].lower() == 'info':
                return logging.INFO
            elif config_dict[key].lower() == 'warning':
                return logging.WARNING
            elif config_dict[key].lower() == 'error':
                return logging.ERROR
        else:
            return config_dict[key]
    except KeyError:
        return None


def update_config(config, catalog_config):
    """
    We want each catalog to have its own values for certain config keys like the
    error email, the logging level, thumbnail attributes.
    To make this work we need to be able to update the overall system config
    with values specific to each catalog.
    This is slightly complicated by the desire to offer both a config dictionary
    and a config object.

    Args:
        config:
        catalog_config:

    Returns:
        None
    """
    return


if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    config_dict = get_config(config_path)
    config_obj = utils.dict2obj(in_dict=config_dict)
    print(dir(config_obj))

