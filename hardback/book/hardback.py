from . css import make_css
from . import metadata
from .. qr.fill import fill_qr
from .. util import hasher
from .. util.elapsed_bar import ElapsedBar
from ebooklib import epub
from pathlib import Path


class EpubBook(epub.EpubBook):
    def add_desc(self, book):
        book.apply(self)
        self.default_css = make_css('default')
        self.add_item(self.default_css)

    def add_items(self, *items):
        for i in items:
            self.add_item(i)

    def write(self, outfile, **options):
        self.add_items(epub.EpubNcx(), epub.EpubNav(), make_css('nav'))
        self.spine = ['nav'] + self.toc
        epub.write_epub(outfile, self, options)


class Hardback:
    def __init__(self, desc):
        if not desc.sources:
            raise ValueError('No filename')
        # Must be done first
        desc.book.fill(desc.sources)
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
        self.book = EpubBook()
        self.book.add_desc(desc.book)

    def write(self):
        self.book.write(self.desc.outfile, **self.desc.options)
        self.bar.finish()
