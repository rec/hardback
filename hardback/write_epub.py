from pathlib import Path
from ebooklib import epub
from . import book

CSS_DIR = Path(__file__).parents[1] / 'css'


class EpubBook(epub.EpubBook):
    def add_desc(self, desc):
        self.set_identifier(desc.identifier)
        self.set_title(desc.title)
        self.set_language(desc.language)

        for a in desc.authors:
            self.add_author(a)

        if desc.cover_image:
            with open(desc.cover_image, 'rb') as fp:
                filename = 'cover_' + Path(desc.cover_image).name
                self.set_cover(filename, fp.read())

    def add_chapters(self, chapters):
        self.add_items(*chapters)
        self.toc = chapters
        self.add_items(epub.EpubNcx(), epub.EpubNav(), make_css('nav'))
        self.spine = ['nav'] + chapters

    def add_items(self, *items):
        for i in items:
            self.add_item(i)

    def write(self, outfile, **options):
        epub.write_epub(outfile, self, options)


def write_epub(desc, chapters, outfile):
    book = EpubBook()
    book.add_desc(desc)

    chapters = [epub.EpubHtml(**c.__dict__) for c in chapters]
    book.add_chapters(chapters)
    book.write(outfile)


def make_css(name):
    return epub.EpubItem(
        uid=f'style_{name}',
        file_name=f'style/{name}.css',
        media_type='text/css',
        content=open(CSS_DIR / f'{name}.css').read())


def test_write():
    data = book.Book(
        identifier='Identifier',
        title='Title',
        authors=('Tom Ritchford',))

    chapters = (
        book.Chapter('Introduction', 'introduction.xhtml', INTRODUCTION),
        book.Chapter('About this book', 'about.xhtml', ABOUT_THIS_BOOK),
    )

    write_epub(data, chapters, 'test.epub')


def add_items(book, *items):
    for i in items:
        book.add_items(i)


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


if __name__ == '__main__':
    test_write()
