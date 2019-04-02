import segno

VERSION = 36
ERROR_CORRECTION = 'H'
SUFFIX = '.png'
BLOCK_SIZE = 1024


def write(data, filename):
    if not filename.endswith(SUFFIX):
        filename += SUFFIX
    if len(data) > BLOCK_SIZE:
        raise ValueError('data is too big')
    qr = segno.make_qr(data, version=VERSION, error='H')
    qr.save(filename)
