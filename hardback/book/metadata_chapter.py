from ebooklib import epub
from . metadata import format as metadata_format


_METADATA_PAGE = """<h2>Metadata</h2>
<pre>%s
</pre>"""


def chapter(hardback, index, metadata):
    item = epub.EpubHtml(
        title=f'Metadata {index + 1}',
        file_name=f'metadata_chapter_{index}.xhtml',
        content=_METADATA_PAGE % metadata_format(index=index, **metadata))
    item.add_item(hardback.book.default_css)
    return item
