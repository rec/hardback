import itertools, json, math, os, struct
from . import hasher, qr
from . constants import PARENT_SIZE, BLOCK_SIZE, CHUNK_SIZE


class ChunkWriter:
    def __init__(self, filename, outdir, metadata):
        self.filename = filename
        self.outdir = outdir
        self.metadata = metadata

    def write_chunks(self):
        digits = math.ceil(math.log(self.metadata['block']['count'], 16))
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
