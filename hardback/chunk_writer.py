import itertools, json, math, os
from . import hasher
from . qr.writer import Writer


class ChunkWriter:
    def __init__(self, filename, outdir, metadata, writer=None):
        self.filename = filename
        self.outdir = outdir
        self.metadata = metadata
        self.writer = writer or Writer()

    def write_chunks(self):
        digits = math.ceil(math.log(self.metadata['block']['count'], 16))
        os.makedirs(self.outdir, exist_ok=True)
        suffix = self.writer.SUFFIX
        self.file_format = os.path.join(self.outdir, f'%0{digits}x{suffix}')

        document = bytes.fromhex(self.metadata['sha256'])
        metadata_blocks = (json.dumps(self.metadata).encode(),)
        file_blocks = hasher.file_blocks(self.filename, self.writer.block_size)
        blocks = itertools.chain(metadata_blocks, file_blocks)

        for index, block in enumerate(blocks):
            yield self.writer.write(
                self.file_format % index, index, document, block)
