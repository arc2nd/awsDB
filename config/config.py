#!/usr/bin/env python

# builtin imports
import os
import json
import logging

# pip imports

# module imports
from awsDB.config import utils

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


config_path = os.path.join(os.path.dirname(__file__), 'config.json')
config_dict = get_config(config_path)
if not config_dict:
    # dictionary of configuration strings
    # CONSTANTS
    config_dict = {
        'aws_creds':             '~/scripts/awsDB/creds/aws_creds.crypt',
        'db_creds':              '~/scripts/awsDB/creds/local_creds.crypt',
        'broker_creds':          '~/scripts/awsDB/creds/broker_creds.crypt',
        'local_db_creds':        '~/scripts/awsDB/creds/local_creds.crypt',
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


if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    config_dict = get_config(config_path)
    config_obj = utils.dict2obj(in_dict=config_dict)
    print(dir(config_obj))

