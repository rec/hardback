import itertools, math, os, yaml
from ..util import hasher


class ChunkWriter:
    def __init__(self, desc, metadata):
        self.desc = desc
        self.metadata = metadata

    def write_chunks(self):
        digits = math.ceil(math.log(self.metadata['block']['count'], 16))
        os.makedirs(self.desc.qr_image_dir, exist_ok=True)
        suffix = self.desc.qr.SUFFIX
        self.file_format = os.path.join(
            self.desc.qr_image_dir, f'%0{digits}x{suffix}')

        document = bytes.fromhex(self.metadata['sha256'])
        metadata_blocks = (yaml.dump(self.metadata).encode(),)
        file_blocks = hasher.file_blocks(
            self.desc.source, self.desc.qr.block_size)
        blocks = itertools.chain(metadata_blocks, file_blocks)

        for index, block in enumerate(blocks):
            yield self.desc.qr.write(
                self.file_format % index, index, document, block)
