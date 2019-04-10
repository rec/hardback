"""
Return a dictionary representing the header block - a block in JSON
representing metadata about the file.
"""

import datetime, os
from . import hasher

BLOCK_SIZE = 1024


def metadata(filename, block_size=BLOCK_SIZE):
    stat = os.stat(filename)
    block_count, rem = divmod(stat.st_size, block_size)
    block_count += 1 + bool(rem)
    return {
        'block_count': block_count,
        'block_size': block_size,
        'filename': os.path.basename(filename),
        'sha256': hasher.hash_file(filename).hexdigest(),
        'size': stat.st_size,
        'timestamp': str(datetime.datetime.utcfromtimestamp(stat.st_mtime)),
    }


if __name__ == '__main__':
    import json, sys

    print(*(json.dumps(metadata(i)) for i in sys.argv[1:]), end='\n')
