import itertools, json, math, os, struct
from . import hasher, header, qr
from . elapsed_bar import ElapsedBar

PARENT_SIZE = 16
BLOCK_SIZE = 1024
SEQUENCE_NUMBER_SIZE = 8
CHUNK_SIZE = PARENT_SIZE + BLOCK_SIZE + SEQUENCE_NUMBER_SIZE
assert CHUNK_SIZE <= qr.CHUNK_SIZE


def write_qr_code_chunks(filename, outfile, callback=None):
    metadata = header.header(filename)

    block_count, rem = divmod(metadata['size'], BLOCK_SIZE)
    block_count += 1 + bool(rem)
    bar = ElapsedBar('Writing files', max=block_count)

    blocks_digits = math.ceil(math.log(block_count, 16))

    if outfile.endswith('/'):
        os.makedirs(outfile, exist_ok=True)
        sep = ''
    elif os.path.isdir(outfile):
        sep = '/'
    else:
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        sep = '-'

    file_format = f'{outfile}{sep}%0{blocks_digits}x'

    parent = bytes.fromhex(metadata['sha256'])[:PARENT_SIZE]
    metadata_blocks = (json.dumps(metadata).encode(),)
    file_blocks = hasher.file_blocks(filename, BLOCK_SIZE)
    blocks = itertools.chain(metadata_blocks, file_blocks)

    for sequence_number, block in enumerate(blocks):
        chunk = struct.pack(f'>q', sequence_number) + parent + block
        assert len(chunk) <= CHUNK_SIZE
        filename = file_format % sequence_number
        result_file = qr.write(chunk, filename)
        callback and callback(result_file)
        bar.next_item(result_file.name)

    bar.finish()
    return file_format, sequence_number + 1, metadata


if __name__ == '__main__':
    import sys
    for i in write_qr_code_chunks(*sys.argv[1:]):
        pass
