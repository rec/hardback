from ebooklib import epub
from hardback.book import css, epub_book
from hardback.data.book import Book
from hardback.data.dataclass import Chapter
from pyfakefs.fake_filesystem_unittest import TestCase as FakeTestCase


class CreateEpubTest(FakeTestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.add_real_directory(css.CSS_DIR)

    def test_simple(self):
        desc = Book(
            identifier='Identifier',
            title='Title',
            authors=('Tom Ritchford',))

        book = epub_book.EpubBook()
        book.add_desc(desc)

        book.toc[:] = [epub.EpubHtml(**c.__dict__) for c in CHAPTERS]
        book.add_items(*book.toc)
        book.write('test.epub')


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

CHAPTERS = (
    Chapter('Introduction', 'introduction.xhtml', INTRODUCTION),
    Chapter('About this book', 'about.xhtml', ABOUT_THIS_BOOK),
)
