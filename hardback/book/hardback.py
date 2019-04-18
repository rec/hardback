import yaml
from pathlib import Path
from . import chapter1, chapter2, chunk_writer, create_epub, metadata
from .. data import dataclass, serialize
from .. util import elapsed_bar

_SUFFIXES = '.jpeg', '.jpg', '.png'


class Hardback:
    def __init__(self, desc):
        if not desc.source:
            raise ValueError('No filename')
        self.desc = desc

        p = Path(desc.source)
        desc.book.cover = desc.book.cover or (p.suffix in _SUFFIXES) and p
        desc.outfile = desc.outfile or p.stem + '.epub'
        desc.book.title = desc.book.title or p.name

        self.metadata = metadata.metadata(desc)
        self.writer = chunk_writer.ChunkWriter(desc, self.metadata)
        self.bar = elapsed_bar.ElapsedBar(
            'Writing',
            max=self.metadata['block']['count'],
            enable=desc.progress_bar)
        self.book = create_epub.EpubBook()
        self.book.add_desc(desc.book)

    def write(self):
        self.book.add_chapters([chapter1.chapter1(self),
                                chapter2.chapter2(self)])
        self.book.write(self.desc.outfile, **self.desc.options)
        self.bar.finish()


def hardback(files):
    is_data = [], []
    for f in files:
        is_data[Path(f).suffix in _DATA_SUFFIXES].append(f)

    source, data = is_data
    if len(source) > 1:
        raise ValueError('We cannot yet write books with more than one source')

    desc = dataclass.Hardback()
    for d in data:
        serialize.unserialize(d, desc)

    if source:
        desc.source = source[0]

    print(yaml.dump(serialize.serialize(desc)))
    Hardback(desc).write()


_DATA_SUFFIXES = '.json', '.yml'


if __name__ == '__main__':
    import sys
    hardback(sys.argv[1:])
