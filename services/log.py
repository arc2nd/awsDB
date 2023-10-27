#!/usr/bin/env python

# builtin imports
import logging

# pip imports

# module imports
from awsDB.config.config import config_obj

# TODO: be able to spawn a per-event log so that we can have separate logs for things like submit that get
#   uploaded with the asset

if config_obj.loglevel.lower() in ['info']:
    log_level = logging.INFO
elif config_obj.loglevel.lower() in ['warning']:
    log_level = logging.WARNING
elif config_obj.loglevel.lower() in ['error']:
    log_level = logging.ERROR
elif config_obj.loglevel.lower() in ['critical']:
    log_level = logging.CRITICAL
else:
    log_level = logging.DEBUG

logging.basicConfig(filename='testLog.log', filemode='a', level=log_level)

_logger = logging.getLogger('awsDB')
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')

# console handler
ch = logging.StreamHandler()
ch.setLevel(log_level)
ch.setFormatter(formatter)
_logger.addHandler(ch)

# file handler
# fh = logging.FileHandler(filename=config.get_value('logfile'))
# fh.setLevel(config.get_value('loglevel'))
# fh.setFormatter(formatter)
# _logger.addHandler(fh)

# http handler
# hh = logging.HTTPHandler()
# hh.setLevel(config.get_value('loglevel'))

# hh.setFormatter(formatter)
# logger.addHandler(hh)


def get_event_logger(asset_name: str = '', event:str = 'submit'):
    logger_path = f'{asset_name}.{event}.log'
    event_logger = logging.getLogger(name=f'{asset_name}.{event}')
    event_formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')

    # file handler
    fh = logging.FileHandler(filename=logger_path)
    fh.setLevel(log_level)
    fh.setFormatter(event_formatter)
    event_logger.addHandler(fh)

    return event_logger
