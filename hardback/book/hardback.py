import yaml
from pathlib import Path
from . import create_epub, metadata, sections
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
        self.book = create_epub.EpubBook()
        self.book.add_desc(desc.book)

    def write(self):
        self.book.write(self.desc.outfile, **self.desc.options)
        self.bar.finish()

    def add_chapters(self):
        chapters = []
        sm = zip(self.desc.sources, self.metadatas)
        for index, (source, md) in enumerate(sm):
            chapters.extend([
                sections.metadata(self, index, md),
                sections.qr(self, source, index, md)])

        self.book.add_chapters(chapters)
        self.write()


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
