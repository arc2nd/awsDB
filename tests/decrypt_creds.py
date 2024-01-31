#!/usr/bin/env python

# builtin imports
import os
import pathlib

# module imports
from awsDB.services import creds

files_to_encrypt = ['test_db_creds.json', 'db_creds.json', 's3_creds.json']

full_paths = []
for this_file in files_to_encrypt:
    full_paths.append(os.path.join(creds.CREDS_BASE_PATH, this_file))

print(full_paths)
for this_path in full_paths:
    creds.make_crypt(path=this_path)
    print(creds.get_creds(path=creds.get_crypt_path(path=this_path)))
