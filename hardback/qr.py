import segno

VERSION = 36
ERROR_CORRECTION = 'H'
SUFFIX = '.png'
CHUNK_SIZE = 1051


def write(data, out):
    if len(data) > CHUNK_SIZE:
        raise ValueError('data is too big')

    if isinstance(out, str):
        if not out.endswith(SUFFIX):
            out += SUFFIX
        out = open(out, 'wb')

    qr = segno.make_qr(data, version=VERSION, error='H')
    qr.save(out)
    return out
