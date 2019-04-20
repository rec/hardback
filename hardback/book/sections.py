from . chunk_writer import write_chunks
from . metadata import format as metadata_format
from .. qr import qr_table
from .. util import chunk_sequence
from ebooklib import epub
from pathlib import Path


def qr(hc):
    def qr_code_images():
        chunks = write_chunks(hc)
        for block_count, f in enumerate(chunks):
            f = Path(f)
            add_image_item(f)
            hc.hardback.desc.remove_image_files and f.unlink()
            hc.hardback.bar.next_item(f.name)
            yield f.name

    def add_image_item(path):
        result = path.read_bytes()
        item = epub.EpubItem(file_name=path.name, content=result)
        hc.hardback.book.add_item(item)

    c, r = hc.hardback.desc.dimensions
    images = qr_code_images()
    chunks = chunk_sequence.chunk_sequence(images, c, r)
    table = qr_table.qr_table(chunks, c, r)

    return epub.EpubHtml(
        title=hc.source, file_name=f'qr-codes-{hc.index}.xhtml', content=table)


def metadata(hc):
    content = _METADATA_PAGE % metadata_format(index=hc.index, **hc.metadata)
    item = epub.EpubHtml(
        title=f'Metadata {hc.index + 1}',
        file_name=f'metadata_chapter_{hc.index}.xhtml',
        content=content)
    item.add_item(hc.hardback.book.default_css)
    return item


_METADATA_PAGE = """<h2>Metadata</h2>
<pre>%s
</pre>"""
