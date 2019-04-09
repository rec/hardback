import math


def chunk_sequence(items, page_size):
    metadata_every = guess_metadata_every(page_size)
    metadata = None
    for i, item in enumerate(items):
        if i:
            if metadata_every and not i % metadata_every:
                yield metadata
        else:
            metadata = item
        yield item


def guess_metadata_every(page_size):
    ps = 1.5 * page_size
    sizes = range(page_size + 1, 2 * page_size)
    return -min((math.gcd(page_size, i), abs(ps - i), -i) for i in sizes)[2]
