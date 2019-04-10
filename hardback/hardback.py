import png, yaml
from ebooklib import epub
from pathlib import Path
from . import (
    chunk_writer, chunk_sequence, create_epub, elapsed_bar, metadata, qr_table)

IMAGE_SUFFIXES = '.jpeg', '.jpg', '.png'
EMPTY_PNG = Path('empty.png')


class Hardback:
    def __init__(self, desc):
        if not desc.filename:
            raise ValueError('No filename')
        self.desc = desc

        p = Path(desc.filename)
        desc.book.cover = desc.book.cover or (p.suffix in IMAGE_SUFFIXES) and p
        desc.outfile = desc.outfile or p.stem + '.epub'

        self.metadata = metadata.metadata(desc.filename)
        self.writer = chunk_writer.ChunkWriter(
            desc.filename, desc.qr_dir, self.metadata)
        self.bar = elapsed_bar.ElapsedBar(
            'Writing',
            max=self.metadata['block_count'],
            enable=desc.enable_bar)
        self.book = create_epub.EpubBook()
        self.book.add_desc(desc.book)

    def write(self):
        self.book.add_chapters([self._chapter1(), self._chapter2()])
        self.book.write(self.desc.outfile, **self.desc.options)
        self.bar.finish()

    def _chapter1(self):
        return epub.EpubHtml(
            title='Metadata',
            file_name='chapter1.xhtml',
            content='<pre>\n%s\n</pre>' % yaml.dump(self.metadata))

    def _chapter2(self):
        c, r = self.desc.columns, self.desc.rows
        images = self._qr_code_images()
        chunks = chunk_sequence.chunk_sequence(images, c, r, EMPTY_PNG)
        table = qr_table.qr_table(chunks, c, r)

        return epub.EpubHtml(
            title=self.desc.filename,
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
                _copy_to_empty_image(f, EMPTY_PNG)
                add_image_item(EMPTY_PNG)
                self.desc.remove_image_files and EMPTY_PNG.unlink()

            self.desc.remove_image_files and f.unlink()
            self.bar.next_item(f.name)
            yield f.name


def _copy_to_empty_image(source, target):
    width, height, pixels, options = png.Reader(str(source)).read()

    pixels = list(pixels)
    for p in pixels:
        p[:] = [1 for i in p]

    with open(target, 'wb') as fp:
        png.Writer(**options).write(fp, pixels)


if __name__ == '__main__':
    import sys
    from . import book

    desc = book.Hardback(filename=sys.argv[1])
    hardback = Hardback(desc)
    hardback.write()
