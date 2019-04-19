import itertools, math, os, yaml
from .. util import hasher
from .. qr.write import write


def write_chunks(desc, metadata, source, index):
    digits = math.ceil(math.log(metadata['block']['count'], 16))
    os.makedirs(desc.qr_image_dir, exist_ok=True)
    suffix = desc.qr.SUFFIX
    file_format = os.path.join(
        desc.qr_image_dir, f'{index}-%0{digits}x{suffix}')

    document = bytes.fromhex(metadata['sha256'])
    metadata_blocks = (yaml.dump(metadata).encode(),)
    file_blocks = hasher.file_blocks(source, desc.qr.block_size)
    blocks = itertools.chain(metadata_blocks, file_blocks)

    for index, block in enumerate(blocks):
        yield write(desc.qr, file_format % index, index, document, block)
