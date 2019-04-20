import attr, yaml
from pathlib import Path
from . import epub_book, metadata, sections
from .. data import dataclass, serialize
from .. util import elapsed_bar
from .. qr import fill

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

        fill.fill(desc.qr)

        self.metadatas = [metadata.metadata(desc, s) for s in desc.sources]
        block_count = sum(m['block']['count'] for m in self.metadatas)
        self.bar = elapsed_bar.ElapsedBar(
            'Writing', max=block_count, enable=desc.progress_bar)
        self.book = epub_book.EpubBook()
        self.book.add_desc(desc.book)

    def __iter__(self):
        return HardbackCursor(self)

    def write(self):
        self.book.write(self.desc.outfile, **self.desc.options)
        self.bar.finish()

    def add_chapters(self):
        chapters = []
        for hc in self:
            chapters.extend([sections.metadata(hc), sections.qr(hc)])
        self.book.add_chapters(chapters)
        self.write()


@attr.dataclass
class HardbackCursor:
    hardback: Hardback = attr.Factory(Hardback)
    index: int = -1

    def __next__(self):
        self.index += 1
        if self.index >= len(self.hardback.desc.sources):
            raise StopIteration
        return self

    @property
    def source(self):
        return self.hardback.desc.sources[self.index]

    @property
    def metadata(self):
        return self.hardback.metadatas[self.index]


def hardback(files):
    desc = dataclass.Hardback()
    for f in files:
        if Path(f).suffix in _DATA_SUFFIXES:
            serialize.unserialize(f, desc)
        else:
            desc.sources.append(f)

    print(yaml.dump(serialize.serialize(desc)))
    Hardback(desc).add_chapters()


_DATA_SUFFIXES = '.json', '.yml'


if __name__ == '__main__':
    import sys
    hardback(sys.argv[1:])
