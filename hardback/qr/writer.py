import attr, segno
from . codes import CODES


@attr.s(slots=True)
class Writer:
    SUFFIX = '.png'

    version = attr.ib(default=36)
    error = attr.ib(default='H')

    def write(self, data, out):
        def write(fp):
            qr = segno.make_qr(data, version=self.version, error=self.error)
            qr.save(fp)
            return fp.name

        if len(data) > self.binary_size:
            raise ValueError
        if not isinstance(out, str):
            return write(out)
        if not out.endswith(self.SUFFIX):
            out += self.SUFFIX
        with open(out, 'wb') as fp:
            return write(fp)

    @error.validator
    def check_error(self, _, error):
        if error not in 'LMQH':
            raise ValueError

    @version.validator
    def check_version(self, _, version):
        if not (1 <= version <= 40):
            raise ValueError

    @property
    def code(self):
        return

    @property
    def binary_size(self):
        return getattr(CODES[self.version - 1].binary, self.error)
