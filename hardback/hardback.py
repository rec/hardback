import yaml
from ebooklib import epub
from pathlib import Path
from . import chunk_sequence, create_epub, elapsed_bar, qr_table, write_chunks

IMAGE_SUFFIXES = '.jpeg', '.jpg', '.png'


class Hardback:
    def __init__(self, desc):
        self.desc = _fill_desc(desc)
        self.writer = write_chunks.Writer(desc.filename)
        self.bar = elapsed_bar.ElapsedBar(
            'Writing',
            max=self.writer.block_count,
            enable=desc.enable_bar)
        self.metadata = dict(self.writer.metadata, **self.desc.metadata)

    def write(self):
        book = create_epub.EpubBook()
        book.add_desc(self.desc.book)

        chapter1 = epub.EpubHtml(
            title='Metadata',
            file_name='chapter1.xhtml',
            content='<pre>\n%s\n</pre>' % yaml.dump(self.metadata))

        c, r = self.desc.columns, self.desc.rows
        chunks = chunk_sequence.chunk_sequence(self._items(book), c * r)
        table = qr_table.qr_table(chunks, c, r)

        chapter2 = epub.EpubHtml(
            title=self.desc.filename,
            file_name='chapter2.xhtml',
            content=table)

        book.add_chapters([chapter1, chapter2])
        book.write(self.desc.outfile, **self.desc.options)

        self.bar.finish()

    def _items(self, book):
        self.block_count = 0
        for f in self.writer.write(self.desc.qr_dir):
            f = Path(f)
            self.block_count += 1
            item = epub.EpubItem(file_name=f.name, content=f.read_bytes())
            book.add_item(item)
            self.desc.remove_image_files and f.unlink()
            self.bar.next_item(f.name)
            yield f.name


def _fill_desc(desc):
    if not desc.filename:
        raise ValueError('No filename')
    p = Path(desc.filename)
    desc.book.cover = desc.book.cover or (p.suffix in IMAGE_SUFFIXES) and p
    desc.outfile = desc.outfile or p.stem + '.epub'

    return desc


if __name__ == '__main__':
    import sys
    from . import book

    desc = book.Hardback(filename=sys.argv[1])
    hardback = Hardback(desc)
    hardback.write()
