import segno

VERSION = 36
ERROR_CORRECTION = 'H'
SUFFIX = '.png'
CHUNK_SIZE = 1051


def write(data, filename):
    if len(data) > CHUNK_SIZE:
        raise ValueError('data is too big')

    if not filename.endswith(SUFFIX):
        filename += SUFFIX

    qr = segno.make_qr(data, version=VERSION, error='H')
    qr.save(filename)
    return filename
