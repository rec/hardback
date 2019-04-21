from pathlib import Path
from . import epub_book, metadata
from .. qr import fill
from .. util import elapsed_bar

_SUFFIXES = '.jpeg', '.jpg', '.png'


class Hardback:
    def __init__(self, desc):
        if not desc.sources:
            raise ValueError('No filename')
        self.desc = desc

        if not desc.book.cover:
            p = [i for i in desc.sources if Path(i).suffix in _SUFFIXES]
            desc.book.cover = p and p[0]

        head = Path(desc.sources[0])
        desc.outfile = desc.outfile or head.stem + '.epub'
        if not desc.book.title:
            desc.book.title = head.name
            if len(desc.sources) > 1:
                desc.book.title += ', ...'

        fill.fill_qr(desc.qr)

        self.metadatas = [metadata.metadata(desc, s) for s in desc.sources]
        block_count = sum(m['block']['count'] for m in self.metadatas)
        self.bar = elapsed_bar.ElapsedBar(
            'Writing', max=block_count, enable=desc.progress_bar)
        self.book = epub_book.EpubBook()
        self.book.add_desc(desc.book)

    def write(self):
        self.book.write(self.desc.outfile, **self.desc.options)
        self.bar.finish()
