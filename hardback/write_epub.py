from pathlib import Path
from ebooklib import epub
from . import book

CSS_DIR = Path(__file__).parents[1] / 'css'


def write_epub(desc):
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

    def add_style(name):
        style = epub.EpubItem(
            uid=f'style_{name}',
            file_name=f'style/{name}.css',
            media_type='text/css',
            content=open(CSS_DIR / f'{name}.css').read())
        book.add_item(style)

    add_style('default')

    chapters = []
    for c in desc.chapters:
        chapter = epub.EpubHtml(title=c.title, file_name=c.filename)
        chapter.content = c.content
        c.properties and chapter.properties.append(c.properties)
        chapters.append(chapter)
        book.add_item(chapter)

    book.toc = chapters

    # add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # add css file
    add_style('nav')

    # create spine
    book.spine = ['nav'] + chapters

    # create epub file
    epub.write_epub(desc.outfile, book, {})


INTRODUCTION = """
<html><head></head>
<body><h1>Introduction</h1>
<p>Introduction paragraph where i explain what is happening.
</p></body></html>
"""

ABOUT_THIS_BOOK = """
<h1>About this book</h1>
<p>Helou, this is my book! There are many books, but this one is mine.</p>
"""

PROPERTIES = '\
rendition:layout-pre-paginated\
 rendition:orientation-landscape\
 rendition:spread-none'


def test_write():
    data = book.Book(
        identifier='Identifier',
        title='Title',
        authors=('Tom Ritchford',),
        chapters=(
            book.Chapter('Introduction', 'introduction.xhtml', INTRODUCTION),
            book.Chapter('About this book', 'about.xhtml', ABOUT_THIS_BOOK),
        )
    )
    write_epub(data)


if __name__ == '__main__':
    test_write()
