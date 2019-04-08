import math


def chunk_sequence(file_format, count, page_size):
    return basic_chunk_sequence(
        file_format, count, guess_metadata_every(page_size))


def basic_chunk_sequence(file_format, count, metadata_every=0):
    for i in range(count):
        if i and metadata_every and not i % metadata_every:
            yield file_format % 0
        yield file_format % i


def guess_metadata_every(page_size):
    ps = 1.5 * page_size
    sizes = range(page_size + 1, 2 * page_size)
    return -min((math.gcd(page_size, i), abs(ps - i), -i) for i in sizes)[2]
