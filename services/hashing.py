#!/usr/bin/env python

import hashlib

def file_hash(in_file: str = '', BUF_SIZE: int = 65536):
    """
    Has a file

    Args:
        in_file: the path of the file you want a hash for
        BUF_SIZE: instead of reading  the file in all at once, read in this much at a time

    Returns:

    """
    sha = hashlib.sha256()
    with open(in_file, 'rb') as fp:
        while True:
            data = fp.read(BUF_SIZE)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()

def compare_files(first_file, second_file):
    return file_hash(in_file=first_file,) == file_hash(in_file=second_file)
