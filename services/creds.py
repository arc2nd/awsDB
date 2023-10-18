#!/usr/bin/env python

# builtin imports
import os
import json
import pathlib

# module imports
from awsDB.config import utils

CREDS_BASE_PATH = os.path.join(pathlib.Path(os.path.dirname(__file__)).resolve().parents[0].as_posix(), 'creds')

##
# Will potentially be replaced with different method of 
# secret storage and retrieval
##
def get_creds(path):
    import platform
    if 'windows' in platform.platform().lower():
        return get_windows_creds(path)
    else:
        return get_windows_creds(path)

def get_creds_object(path):
    creds_dict = get_creds(path)
    return utils.dict2obj(in_dict=creds_dict)

def make_crypt(path):
    import platform
    if 'windows' in platform.platform().lower():
        make_windows_creds(path)
    else:
        make_windows_creds(path)

def make_windows_creds(path):
    with open(path, 'r') as fp:
        contents = fp.read()
    msg = encrypt(path, contents)
    crypt_path = get_crypt_path(path)
    with open(crypt_path, 'w') as fp:
        fp.write(msg)

def get_windows_creds(path):
    with open(path, 'r') as fp:
        contents = fp.read()

    output = decrypt(path, contents)
    if output:
        try:
            j = json.loads(output)
        except: 
            j = None
    return j

def get_crypt_path(path):
    return '{}.crypt'.format(os.path.splitext(path)[0])

SALT = b'sAlT'*8

def get_fenec(SECRET_KEY):
    import base64
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.fernet import Fernet

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, salt=SALT, iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(SECRET_KEY, encoding='utf-8')))
    return Fernet(key)

def encrypt(path, msg):
    crypt_path = get_crypt_path(path)
    f = get_fenec(crypt_path)
    token = f.encrypt(bytes(msg, encoding='utf-8'))
    return token.decode()

def decrypt(path, msg):
    f = get_fenec(path)
    return f.decrypt(bytes(msg, encoding='utf-8')).decode()



