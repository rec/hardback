"""
Return a dictionary representing the header block - a block in JSON
representing metadata about the file.
"""

import datetime, os, pathlib
from . import chunk_sequence, hasher
from . qr.writer import Writer


def metadata(desc, writer=None):
    writer = writer or Writer()
    stat = os.stat(desc.filename)
    block_count, rem = divmod(stat.st_size, writer.block_size)
    block_count += bool(rem)

    c, r = desc.dimensions
    metadata_every = chunk_sequence.guess_metadata_every(c * r)
    chunk_count = 1 + block_count + (block_count // metadata_every)

    return {
        'block': {'count': block_count,
                  'size': writer.block_size},
        'chunk': {'count': chunk_count,
                  'size': writer.chunk_size},
        'dimensions': desc.dimensions,
        'file_bytes': stat.st_size,
        'file_name': pathlib.Path(desc.filename).name,
        'sha256': hasher.hash_file(desc.filename).hexdigest(),
        'timestamp': str(datetime.datetime.utcfromtimestamp(stat.st_mtime)),
    }


def format(sha256, **metadata):
    return FORMAT.format(s1=sha256[:32], s2=sha256[32:], **metadata)


FORMAT = """\
block: {{count: {block[count]},  size: {block[size]}}}
chunk: {{count: {chunk[count]},  size: {chunk[size]}}}
dimensions: {dimensions}
file_bytes: {file_bytes}
file_name: {file_name}
timestamp: '{timestamp}'
sha256: "\\
  {s1}\\
  {s2}\\
"
"""


if __name__ == '__main__':
    import json, sys

    print(*(json.dumps(metadata(i)) for i in sys.argv[1:]), end='\n')
