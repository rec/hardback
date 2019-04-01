import hashlib
HASHER = hashlib.sha256
BLOCK_SIZE = 4096


def block_iterator(filename, block_size=BLOCK_SIZE):
    with open(filename, 'rb') as fp:
        while True:
            buf = fp.read(block_size)
            if buf:
                yield buf
            else:
                return


def hash_digest(items):
    h = HASHER()
    for i in items:
        h.update(i)
    return h.hexdigest()


def hash_file(filename, block_size=BLOCK_SIZE):
    it = block_iterator(filename, block_size)
    return hash_digest(it)
