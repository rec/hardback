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
        self.bar = ElapsedBar('Writing files', max=self.block_count)

    def write(self, outfile, callback=None):
        blocks_digits = math.ceil(math.log(self.block_count, 16))

        if outfile.endswith('/'):
            outdir = outfile
            sep = ''
        elif os.path.isdir(outfile):
            outdir = ''
            sep = '/'
        else:
            outdir = os.path.dirname(outfile)
            sep = '-'

        outdir and os.makedirs(outdir, exist_ok=True)
        self.file_format = f'{outfile}{sep}%0{blocks_digits}x'

        parent = bytes.fromhex(self.metadata['sha256'])[:PARENT_SIZE]
        metadata_blocks = (json.dumps(self.metadata).encode(),)
        file_blocks = hasher.file_blocks(self.filename, BLOCK_SIZE)
        blocks = itertools.chain(metadata_blocks, file_blocks)

        for sequence_number, block in enumerate(blocks):
            chunk = struct.pack(f'>q', sequence_number) + parent + block
            assert len(chunk) <= CHUNK_SIZE
            filename = self.file_format % sequence_number
            result_file = qr.write(chunk, filename)
            callback and callback(result_file)
            self.bar.next_item(result_file.name)

        self.bar.finish()
        return self.file_format, sequence_number + 1, self.metadata


def write_qr_code_chunks(filename, outfile, callback=None):
    return Writer(filename).write(outfile, callback)


if __name__ == '__main__':
    import sys
    for i in write_qr_code_chunks(*sys.argv[1:]):
        pass
