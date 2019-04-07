from pathlib import Path
import os
from ebooklib import epub
from . import book

CSS_DIR = Path(__file__).parents[1] / 'css'


def create_book(desc):
    book = epub.EpubBook()
    book.set_identifier(desc.identifier)
    book.set_title(desc.title)

    book.set_language(desc.language)
    for a in desc.authors:
        book.add_author(a)

    if desc.cover_image:
        with open(desc.cover_image, 'rb') as fp:
            filename = Path(desc.cover_image).name
            book.set_cover(filename, fp.read())

    default_css = _style('default')
    book.add_item(default_css)

    c1 = epub.EpubHtml(title='Introduction', file_name='intro.xhtml', lang='hr')
    c1.content = CONTENT1

    # about chapter
    c2 = epub.EpubHtml(title='About this book', file_name='about.xhtml')
    c2.content = CONTENT2
    c2.set_language('hr')
    c2.properties.append(PROPERTIES)
    c2.add_item(default_css)

    # add chapters to the book
    book.add_item(c1)
    book.add_item(c2)

    # create table of contents
    # - add manual link
    # - add section
    # - add auto created links to chapters

    book.toc = (
        epub.Link('intro.xhtml', 'Introduction', 'intro'),
        (epub.Section('Languages'), (c1, c2)))

    # add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # add css file
    book.add_item(_style('nav'))

    # create spine
    book.spine = ['nav', c1, c2]

    # create epub file
    epub.write_epub('test.epub', book, {})


def _style(name):
    return epub.EpubItem(
        uid=f'style_{name}',
        file_name=f'style/{name}.css',
        media_type='text/css',
        content=open(CSS_DIR / f'{name}.css').read())


CONTENT1 = """
<html><head></head>
<body><h1>Introduction</h1>
<p>Introduction paragraph where i explain what is happening.
</p></body></html>
"""

CONTENT2 = """
<h1>About this book</h1>
<p>Helou, this is my book! There are many books, but this one is mine.</p>
"""

PROPERTIES = '\
rendition:layout-pre-paginated\
 rendition:orientation-landscape\
 rendition:spread-none'


if __name__ == '__main__':
    create_book(book.Book(
        identifier='Identifier',
        title='Title',
        authors=('Tom Ritchford',)))
