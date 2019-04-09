import itertools, json, math, os, struct
from . import hasher, header, qr
from . elapsed_bar import ElapsedBar

PARENT_SIZE = 16
BLOCK_SIZE = 1024
SEQUENCE_NUMBER_SIZE = 8
CHUNK_SIZE = PARENT_SIZE + BLOCK_SIZE + SEQUENCE_NUMBER_SIZE
assert CHUNK_SIZE <= qr.CHUNK_SIZE


class Writer:
    def __init__(self, filename):
        self.filename = filename
        self.metadata = header.header(filename)

        self.block_count, rem = divmod(self.metadata['size'], BLOCK_SIZE)
        self.block_count += 1 + bool(rem)

    def write(self, outdir):
        os.makedirs(outdir, exist_ok=True)

        digits = math.ceil(math.log(self.block_count, 16))
        self.file_format = os.path.join(outdir, f'%0{digits}x{qr.SUFFIX}')

        parent = bytes.fromhex(self.metadata['sha256'])[:PARENT_SIZE]
        metadata_blocks = (json.dumps(self.metadata).encode(),)
        file_blocks = hasher.file_blocks(self.filename, BLOCK_SIZE)
        blocks = itertools.chain(metadata_blocks, file_blocks)

        for sequence_number, block in enumerate(blocks):
            chunk = struct.pack(f'>q', sequence_number) + parent + block
            assert len(chunk) <= CHUNK_SIZE
            filename = self.file_format % sequence_number
            yield qr.write(chunk, filename)


def write_qr_code_chunks(filename, outdir, callback=None):
    writer = Writer(filename)
    bar = ElapsedBar('Writing files', writer=writer.block_count)
    for sequence_number, result_file in enumerate(writer.write(outdir)):
        callback and callback(result_file)
        bar.next_item(result_file.name)

    bar.finish()
    return writer.file_format, sequence_number + 1, writer.metadata


if __name__ == '__main__':
    import sys
    for i in write_qr_code_chunks(*sys.argv[1:]):
        pass
