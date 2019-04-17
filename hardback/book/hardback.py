import png, yaml
from ebooklib import epub
from pathlib import Path
from . import chapter1, chunk_writer, create_epub, metadata
from .. data import dataclass, serialize
from .. qr import qr_table
from .. util import chunk_sequence, elapsed_bar


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
        self.book.add_chapters([chapter1.chapter1(self), self._chapter2()])
        self.book.write(self.desc.outfile, **self.desc.options)
        self.bar.finish()

    def _chapter2(self):
        c, r = self.desc.dimensions
        images = self._qr_code_images()
        chunks = chunk_sequence.chunk_sequence(images, c, r, _EMPTY_PNG)
        table = qr_table.qr_table(chunks, c, r)

        return epub.EpubHtml(
            title=self.desc.source,
            file_name='chapter2.xhtml',
            content=table)

    def _qr_code_images(self):
        def add_image_item(path):
            result = path.read_bytes()
            item = epub.EpubItem(file_name=path.name, content=result)
            self.book.add_item(item)

        chunks = self.writer.write_chunks()
        for self.block_count, f in enumerate(chunks):
            f = Path(f)
            add_image_item(f)
            if not self.block_count:
                _copy_to_empty_image(f, _EMPTY_PNG)
                add_image_item(_EMPTY_PNG)
                self.desc.remove_image_files and _EMPTY_PNG.unlink()

            self.desc.remove_image_files and f.unlink()
            self.bar.next_item(f.name)
            yield f.name


_SUFFIXES = '.jpeg', '.jpg', '.png'
_EMPTY_PNG = Path('empty.png')


def _copy_to_empty_image(source, target):
    width, height, pixels, options = png.Reader(str(source)).read()

    pixels = list(pixels)
    for p in pixels:
        p[:] = [1 for i in p]

    with open(target, 'wb') as fp:
        png.Writer(**options).write(fp, pixels)


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
