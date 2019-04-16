import attr, segno, struct
from . codes import CODES


@attr.s(slots=True)
class Writer:
    version = attr.ib(default=36)
    error = attr.ib(default='H')
    document_bytes = attr.ib(default=8)
    index_bytes = attr.ib(default=8)

    SUFFIX = '.png'

    def write(self, out, index, document, block):
        document = document[:self.document_bytes]
        index = struct.pack(f'>q', index)[:self.index_bytes]
        data = index + document + block

        def write(fp):
            qr = segno.make_qr(data, version=self.version, error=self.error)
            qr.save(fp)
            return fp.name

        if len(data) > self.chunk_size:
            raise ValueError(f'{len(data)} > chunk_size {self.chunk_size}')
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
    def chunk_size(self):
        return getattr(CODES[self.version - 1].binary, self.error)

    @property
    def block_size(self):
        return self.chunk_size - self.document_bytes - self.index_bytes
