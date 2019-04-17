from ebooklib import epub
from . import metadata

_METADATA_PAGE = """<h2>Metadata</h2>
<pre>%s
</pre>"""


def chapter1(hardback):
    item = epub.EpubHtml(
        title='Metadata',
        file_name='chapter1.xhtml',
        content=_METADATA_PAGE % metadata.format(**hardback.metadata))
    item.add_item(hardback.book.default_css)
    return item
