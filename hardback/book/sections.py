from . chunk_writer import write_chunks
from . metadata import format as metadata_format
from .. qr import qr_table
from .. util import chunk_sequence
from ebooklib import epub
from pathlib import Path
import png

_EMPTY_PNG = Path('empty.png')


def qr(hardback, source, index, metadata):
    def qr_code_images():
        chunks = write_chunks(hardback.desc, metadata, source, index)
        for block_count, f in enumerate(chunks):
            f = Path(f)
            add_image_item(f)
            if not _EMPTY_PNG.exists():
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
        title=source, file_name=f'qr-codes-{index}.xhtml', content=table)


def metadata(hardback, index, metadata):
    item = epub.EpubHtml(
        title=f'Metadata {index + 1}',
        file_name=f'metadata_chapter_{index}.xhtml',
        content=_METADATA_PAGE % metadata_format(index=index, **metadata))
    item.add_item(hardback.book.default_css)
    return item


_METADATA_PAGE = """<h2>Metadata</h2>
<pre>%s
</pre>"""