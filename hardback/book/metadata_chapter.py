from ebooklib import epub
from . metadata import format as metadata_format


_METADATA_PAGE = """<h2>Metadata</h2>
<pre>%s
</pre>"""


def chapter(hardback, metadata):
    item = epub.EpubHtml(
        title='Metadata',
        file_name='metadata_chapter.xhtml',
        content=_METADATA_PAGE % metadata_format(**metadata))
    item.add_item(hardback.book.default_css)
    return item
