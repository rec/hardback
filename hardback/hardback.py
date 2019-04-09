import pathlib, yaml
from ebooklib import epub
from . import chunk_sequence, create_epub, elapsed_bar, qr_table, write_chunks

IMAGE_SUFFIXES = '.jpeg', '.jpg', '.png'


class Hardback:
    def __init__(self, desc):
        self.desc = desc
        if not desc.book.cover:
            if pathlib.Path(desc.file).suffix in IMAGE_SUFFIXES:
                desc.book.cover = desc.file
        self.writer = write_chunks.Writer(desc.filename)
        self.bar = elapsed_bar.ElapsedBar(
            'Writing',
            max=self.writer.block_count,
            enabled=desc.enable_bar)
        self.metadata = dict(self.writer.metadata, **self.desc.metadata)

    def write(self):
        book = create_epub.EpubBook()
        book.add_desc(self.desc.book)

        chapter1 = epub.EpubHtml(
            title='Metadata',
            file_name='chapter1.xhtml',
            content='<pre>\n%s\n</pre>' % yaml.dump(self.metadata))

        r, c = self.desc.columns, self.desc.rows
        chunks = chunk_sequence(self._items(book), r * c)
        table = qr_table.qr_table(chunks, r, c)

        chapter2 = epub.EpubHtml(
            title=self.desc.filename,
            file_name='chapter2.xhtml',
            content=table)

        book.add_chapters([chapter1, chapter2])
        book.write(self.desc.outfile, **self.desc.options)

        self.bar.finish()

    def _items(self, book):
        self.block_count = 0
        for file in self.writer.write(self.desc.outdir):
            self.block_count += 1
            item = epub.EpubItem(
                file_name=file.name, content=file.read_bytes())
            book.add_item(item)
            self.desc.remove_image_files and file.unlink()
            self.bar.next_item(file.name)
            yield file


if __name__ == '__main__':
    import sys
    from . import book

    desc = book.Hardback(filename=sys.argv[1])
    hardback = Hardback(desc)
    hardback.write()
