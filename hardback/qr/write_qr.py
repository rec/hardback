import segno

from .. import constants

VERSION = 36
ERROR_CORRECTION = 'H'
SUFFIX = '.png'
CHUNK_SIZE = 1051
assert constants.CHUNK_SIZE <= CHUNK_SIZE


def write_qr(data, out):
    if len(data) > CHUNK_SIZE:
        raise ValueError('data is too big')

    if isinstance(out, str):
        if not out.endswith(SUFFIX):
            out += SUFFIX
        output = open(out, 'wb')
    else:
        output, out = out, out.name

    qr = segno.make_qr(data, version=VERSION, error='H')
    qr.save(output)
    return out
