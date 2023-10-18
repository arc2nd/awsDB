#!/usr/bin/env python

# builtin imports
import os

# module imports
from awsDB.services.log import _logger


# Functions to gather information about the file
def get_file_stats(filepath: str = '') -> dict:
    """
    get various information about a file

    Args:
        filepath: the file path to get information about

    Returns:
        stats: a dictionary containing all the information we have collected
    """
    import time
    import socket
    _logger.info('getting info for: {}'.format(filepath))
    stats = {}
    if os.path.exists(os.path.abspath(filepath)):
        stats['path'] = os.path.abspath(filepath)
        stats['name'] = os.path.basename(filepath)
        stats['stime'] = time.time()
        stats['ctime'] = get_ctime(filepath)
        stats['mtime'] = get_mtime(filepath)
        stats['creator'] = get_creator(filepath)
        stats['size'] = get_size(filepath)
        stats['ftype'] = get_ftype(filepath)
        stats['machine'] = socket.getfqdn()
        return stats
    else:
        print("file does not exist")


def get_ctime(filepath):
    """
    Get the creation time of the file

    Args:
        filepath:the file path to get information about

    Returns:

    """
    return os.path.getctime(filepath)


def get_mtime(filepath):
    """
    Get the modified time of the file

    Args:
        filepath: the file path to get information about

    Returns:

    """
    return os.path.getmtime(filepath)


def get_creator(filepath):
    """
    Get the creator of the file

    Args:
        filepath: the file path to get information about

    Returns:

    """
    from pwd import getpwuid
    return getpwuid(os.stat(filepath).st_uid).pw_name


def get_group(filepath):
    """
    Get the group permission for the file

    Args:
        filepath: the file path to get information about

    Returns:

    """
    from grp import getgrgid
    return getgrgid(os.stat(filepath).st_gid).gr_name


def get_size(filepath):
    """
    Get the size of the file

    Args:
        filepath: the file path to get information about

    Returns:

    """
    return os.path.getsize(filepath)


def get_ftype(filepath):
    """
    Get the file extension

    Args:
        filepath: the file path to get information about

    Returns:

    """
    return os.path.splitext(filepath)[-1]

