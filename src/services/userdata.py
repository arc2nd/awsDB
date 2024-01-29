#!/usr/bin/env python

import socket
import getpass
import platform
import logging
# from awsDB.services.log import _logger

_logger = logging.getLogger(__name__)


def get_ip() -> str:
    """
    Get the ip of this computer

    Returns:
        ip: the ip address
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 53))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        _logger.warning('Couldn\'t connect to determine IP address')


def get_platform() -> str:
    """
    Get the platform of this computer

    Returns:
        response: whatever is returned by platform.platform()
    """
    try:
        response = platform.platform()
        return response
    except:
        _logger.warning('Couldn\'t determine machine platform')


def get_hostname() -> str:
    """
    Get the hostname of this computer

    Returns:
        hostname: the hostname
    """
    try:
        response = socket.getfqdn()
        hostname = response.split('.')[0]
        return hostname
    except:
        _logger.warning('Couldn\'t determine machine hostname')


def get_user() -> str:
    """
    Get the current user

    Returns:
        user: the user name
    """
    try:
        user = getpass.getuser()
        return user
    except:
        _logger.warning('Couldn\'t determine user')


def collect_user_data() -> dict:
    """
    Get information about the user and the computer that is running this script

    Returns:
        return_dict: a dictionary with user, hostname, platform, and ip
    """
    return_dict = {'user': get_user(),
                   'hostname': get_hostname(),
                   'platform': get_platform(),
                   'ip': get_ip()
                   }
    return return_dict


if __name__ == '__main__':
    print(collect_user_data())
