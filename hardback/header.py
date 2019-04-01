"""
Return a dictionary representing the header block - a block in JSON
representing metadata about the file.
"""

import datetime, os
from . import hasher


def header(filename):
    stat = os.stat(filename)
    return {
        'filename': os.path.basename(filename),
        'timestamp': datetime.datetime.utcfromtimestamp(stat.st_mtime),
        'size': stat.size,
        'hash': hasher.hash_file(filename),
    }
