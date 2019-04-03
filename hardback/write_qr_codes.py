import itertools, json, struct
from . import hasher, header, qr

PARENT_SIZE = 16
BLOCK_SIZE = 1024
SEQNO_SIZE = 8
CHUNK_SIZE = PARENT_SIZE + BLOCK_SIZE + SEQNO_SIZE

assert CHUNK_SIZE <= qr.CHUNK_SIZE


def write_qr_codes(filename, outfile):
    metadata = header.header(filename)
    parent = bytes.fromhex(metadata['sha256'][:PARENT_SIZE])
    metadata_blocks = (json.dumps(metadata).encode(),)
    file_blocks = hasher.file_blocks(filename, BLOCK_SIZE)
    blocks = itertools.chain(metadata_blocks, file_blocks)

    for seqno, block in enumerate(blocks):
        fmt = b'>q%ds%ds' % (PARENT_SIZE, len(block))
        chunk = struct.pack(fmt, seqno, parent, block)
        assert len(chunk) <= CHUNK_SIZE

        filename = '%s-%016x' % (outfile, seqno)
        yield qr.write(chunk, filename)


if __name__ == '__main__':
    import sys
    for f in write_qr_codes(*sys.argv[1:]):
        print('Written', f)
