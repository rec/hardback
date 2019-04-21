from . import epub_book, metadata
from .. data.fill import fill_book
from .. qr.fill import fill_qr
from .. util import hasher
from .. util.elapsed_bar import ElapsedBar
from pathlib import Path


class Hardback:
    def __init__(self, desc):
        if not desc.sources:
            raise ValueError('No filename')
        # Must be done first
        fill_book(desc.book, desc.sources)
        fill_qr(desc.qr)

        head = Path(desc.sources[0])
        desc.outfile = desc.outfile or head.stem + '.epub'

        self.desc = desc
        self.metadatas = [metadata.metadata(desc, s) for s in desc.sources]
        total_blocks = sum(m['block']['count'] for m in self.metadatas)

        if not desc.book.identifier:
            hashes = (m['sha256'].encode() for m in self.metadatas)
            d = hasher.hash_digest(hashes)
            desc.book.identifier = d.hexdigest()

        self.bar = ElapsedBar(max=total_blocks, enable=desc.progress_bar)
        self.book = epub_book.EpubBook()
        self.book.add_desc(desc.book)

    def write(self):
        self.book.write(self.desc.outfile, **self.desc.options)
        self.bar.finish()
