import datetime, itertools, json, math, struct
from . import hasher, header, qr
from progress.bar import ChargingBar

PARENT_SIZE = 16
BLOCK_SIZE = 1024
SEQUENCE_NUMBER_SIZE = 8
CHUNK_SIZE = PARENT_SIZE + BLOCK_SIZE + SEQUENCE_NUMBER_SIZE
assert CHUNK_SIZE <= qr.CHUNK_SIZE


class ElapsedBar(ChargingBar):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.start_time = datetime.datetime.now()
        self.index = 0

    def next_item(self, message):
        self.index += 1
        elapsed = datetime.datetime.now() - self.start_time
        time_per_item = elapsed / self.index
        remaining_items = 1 + (self.max - self.index)
        remaining = time_per_item * remaining_items

        def fmt(t):
            return str(t).split('.', 1)[0]

        self.message = '%s %s elapsed, %s to go' % (
            message, fmt(elapsed), fmt(remaining))

        self.next()


def write_qr_codes(filename, outfile):
    metadata = header.header(filename)

    file_blocks, rem = divmod(metadata['size'], BLOCK_SIZE)
    file_blocks += 1 + bool(rem)
    bar = ElapsedBar('Writing files', max=file_blocks)

    blocks_digits = math.ceil(math.log(file_blocks, 16))
    file_format = f'{outfile}-%0{blocks_digits}x'

    parent = bytes.fromhex(metadata['sha256'])[:PARENT_SIZE]
    metadata_blocks = (json.dumps(metadata).encode(),)
    file_blocks = hasher.file_blocks(filename, BLOCK_SIZE)
    blocks = itertools.chain(metadata_blocks, file_blocks)

    for sequence_number, block in enumerate(blocks):
        chunk = struct.pack(f'>q', sequence_number) + parent + block
        assert len(chunk) <= CHUNK_SIZE
        filename = file_format % sequence_number
        bar.next_item(qr.write(chunk, filename).name)

    bar.finish()


if __name__ == '__main__':
    import sys
    for i, f in enumerate(write_qr_codes(*sys.argv[1:])):
        pass
