#!/usr/bin/env python

# builtin imports
import os
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports

# module imports
from services import creds

files_to_encrypt = ['db_creds.json', 's3_creds.json', 'test_db_creds.json', 'test_s3_creds.json']

creds_base_path = pathlib.Path(os.path.dirname(__file__)).resolve().parents[0].as_posix()
full_paths = []
for this_file in files_to_encrypt:
    full_paths.append(os.path.join(creds_base_path, 'creds', this_file))

print(full_paths)
for this_path in full_paths:
    if os.path.exists(this_path):
        creds.make_crypt(path=this_path)
