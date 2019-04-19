import png
from ebooklib import epub
from pathlib import Path
from . import chunk_writer
from .. qr import qr_table
from .. util import chunk_sequence

_EMPTY_PNG = Path('empty.png')


def chapter(hardback, source, metadata):
    writer = chunk_writer.ChunkWriter(hardback.desc, metadata)

    def qr_code_images():
        chunks = writer.write_chunks(source)
        for block_count, f in enumerate(chunks):
            f = Path(f)
            add_image_item(f)
            if not block_count:
                copy_to_empty_image(f, _EMPTY_PNG)
                add_image_item(_EMPTY_PNG)
                hardback.desc.remove_image_files and _EMPTY_PNG.unlink()

            hardback.desc.remove_image_files and f.unlink()
            hardback.bar.next_item(f.name)
            yield f.name

    def add_image_item(path):
        result = path.read_bytes()
        item = epub.EpubItem(file_name=path.name, content=result)
        hardback.book.add_item(item)

    def copy_to_empty_image(source, target):
        width, height, pixels, options = png.Reader(str(source)).read()

        pixels = list(pixels)
        for p in pixels:
            p[:] = [1 for i in p]

        with open(target, 'wb') as fp:
            png.Writer(**options).write(fp, pixels)

    c, r = hardback.desc.dimensions
    images = qr_code_images()
    chunks = chunk_sequence.chunk_sequence(images, c, r, _EMPTY_PNG)
    table = qr_table.qr_table(chunks, c, r)

    return epub.EpubHtml(
        title=source, file_name='chapter2.xhtml', content=table)
