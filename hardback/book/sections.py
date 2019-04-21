from . chunk_writer import write_chunks
from . metadata import format as metadata_format
from .. qr import qr_table
from .. util import chunk_sequence
from ebooklib import epub
from pathlib import Path


def qr_pages(hc):
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
    return qr_table.qr_table(chunks, c, r)


def chapter(hc):
    metadata = _METADATA_PAGE % metadata_format(index=hc.index, **hc.metadata)
    parts = [metadata]

    for page in qr_pages(hc):
        parts.extend([hc.hardback.book.add_pagebreak(), page])

    item = epub.EpubHtml(
        title=hc.source,
        file_name=f'qr-codes-{hc.index}.xhtml',
        content=''.join(parts))
    item.add_item(hc.hardback.book.default_css)
    return item


_METADATA_PAGE = """<h2>Metadata</h2>
<pre>%s
</pre>"""
