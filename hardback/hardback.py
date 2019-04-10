import png, yaml
from ebooklib import epub
from pathlib import Path
from . import chunk_sequence, create_epub, elapsed_bar, qr_table, write_chunks

IMAGE_SUFFIXES = '.jpeg', '.jpg', '.png'
EMPTY_PNG = 'empty.png'


class Hardback:
    def __init__(self, desc):
        self._set_desc(desc)
        self.writer = write_chunks.Writer(self.desc.filename)
        self.bar = elapsed_bar.ElapsedBar(
            'Writing',
            max=self.writer.block_count,
            enable=self.desc.enable_bar)
        self.metadata = dict(self.writer.metadata, **self.desc.metadata)

    def write(self):
        book = create_epub.EpubBook()
        book.add_desc(self.desc.book)

        chapter1 = epub.EpubHtml(
            title='Metadata',
            file_name='chapter1.xhtml',
            content='<pre>\n%s\n</pre>' % yaml.dump(self.metadata))

        c, r = self.desc.columns, self.desc.rows
        items = self._items(book)
        chunks = chunk_sequence.chunk_sequence(items, c, r, EMPTY_PNG)
        table = qr_table.qr_table(chunks, c, r)

        chapter2 = epub.EpubHtml(
            title=self.desc.filename,
            file_name='chapter2.xhtml',
            content=table)

        book.add_chapters([chapter1, chapter2])
        book.write(self.desc.outfile, **self.desc.options)

        self.bar.finish()

    def _items(self, book):
        chunks = self.writer.write_chunks(self.desc.qr_dir)
        for self.block_count, f in enumerate(chunks):
            f = Path(f)
            item = epub.EpubItem(file_name=f.name, content=f.read_bytes())
            book.add_item(item)
            if not self.block_count:
                book.add_item(self._empty_image_item(f))

            self.desc.remove_image_files and f.unlink()
            self.bar.next_item(f.name)
            yield f.name

    def _empty_image_item(self, f):
        width, height, pixels, options = png.Reader(str(f)).read()

        pixels = list(pixels)
        for p in pixels:
            p[:] = [1 for i in range(len(p))]

        with open(EMPTY_PNG, 'wb') as fp:
            png.Writer(**options).write(fp, pixels)

        with open(EMPTY_PNG, 'rb') as fp:
            empty = fp.read()

        self.desc.remove_image_files and Path(EMPTY_PNG).unlink()
        return epub.EpubItem(file_name=EMPTY_PNG, content=empty)

    def _set_desc(self, desc):
        if not desc.filename:
            raise ValueError('No filename')
        p = Path(desc.filename)
        desc.book.cover = desc.book.cover or (p.suffix in IMAGE_SUFFIXES) and p
        desc.outfile = desc.outfile or p.stem + '.epub'
        self.desc = desc


if __name__ == '__main__':
    import sys
    from . import book

    desc = book.Hardback(filename=sys.argv[1])
    hardback = Hardback(desc)
    hardback.write()
