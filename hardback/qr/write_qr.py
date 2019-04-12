import segno

VERSION = 36
ERROR = 'H'
SUFFIX = '.png'


def write_qr(data, out, version=VERSION, error=ERROR):
    def write(fp):
        qr = segno.make_qr(data, version=version, error=error)
        qr.save(fp)
        return fp.name

    if not isinstance(out, str):
        return write(out)

    if not out.endswith(SUFFIX):
        out += SUFFIX

    with open(out, 'wb') as fp:
        return write(fp)
