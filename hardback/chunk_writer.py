import itertools, json, math, os, struct
from . import hasher, qr

PARENT_SIZE = 16
BLOCK_SIZE = 1024
SEQUENCE_NUMBER_SIZE = 8
CHUNK_SIZE = PARENT_SIZE + BLOCK_SIZE + SEQUENCE_NUMBER_SIZE
assert CHUNK_SIZE <= qr.CHUNK_SIZE


class ChunkWriter:
    def __init__(self, filename, outdir, metadata):
        self.filename = filename
        self.outdir = outdir
        self.metadata = metadata

    def write_chunks(self):
        digits = math.ceil(math.log(self.metadata['block_count'], 16))
        os.makedirs(self.outdir, exist_ok=True)
        self.file_format = os.path.join(self.outdir, f'%0{digits}x{qr.SUFFIX}')

        parent = bytes.fromhex(self.metadata['sha256'])[:PARENT_SIZE]
        metadata_blocks = (json.dumps(self.metadata).encode(),)
        file_blocks = hasher.file_blocks(self.filename, BLOCK_SIZE)
        blocks = itertools.chain(metadata_blocks, file_blocks)

        for sequence_number, block in enumerate(blocks):
            chunk = struct.pack(f'>q', sequence_number) + parent + block
            assert len(chunk) <= CHUNK_SIZE
            filename = self.file_format % sequence_number
            yield qr.write_qr(chunk, filename)
