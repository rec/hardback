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
        'timestamp': str(datetime.datetime.utcfromtimestamp(stat.st_mtime)),
        'size': stat.st_size,
        'sha256': hasher.hash_file(filename).hexdigest(),
    }


if __name__ == '__main__':
    import json, sys

    print(*(json.dumps(header(i)) for i in sys.argv[1:]), end='\n')
