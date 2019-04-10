from pathlib import Path
from ebooklib import epub
from . import book

CSS_DIR = Path(__file__).parents[1] / 'css'


def create_epub(desc, chapters):
    book = EpubBook()
    book.add_desc(desc)

    chapters = [epub.EpubHtml(**c.__dict__) for c in chapters]
    book.add_chapters(chapters)
    return book


class EpubBook(epub.EpubBook):
    def add_desc(self, book):
        self.set_identifier(book.identifier)
        self.set_title(book.title)
        self.set_language(book.language)

        for a in book.authors:
            self.add_author(a)

        if book.cover:
            with open(book.cover, 'rb') as fp:
                filename = 'cover_' + Path(book.cover).name
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


def write_epub(desc, chapters, outfile, **options):
    book = create_epub(desc, chapters)
    book.write(outfile, **options)


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


INTRODUCTION = """
<html><head></head>
<body><h1>Introduction</h1>
<p>Introductary paragraph where I explain what is happening.
</p></body></html>
"""

ABOUT_THIS_BOOK = """
<h1>About this book</h1>
<p>Hello, this is my book.</p>
"""

PROPERTIES = '\
rendition:layout-pre-paginated\
 rendition:orientation-landscape\
 rendition:spread-none'


if __name__ == '__main__':
    test_write()
