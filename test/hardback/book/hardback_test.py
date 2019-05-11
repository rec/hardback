from ebooklib import epub
from hardback.book import css, hardback
from hardback.data.book import Book
from hardback.data.dataclass import Chapter, Hardback
from pathlib import Path
from pyfakefs.fake_filesystem_unittest import TestCase as FakeTestCase

DIR = Path(__file__).parent


class HardbackrTest(FakeTestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.add_real_directory(css.CSS_DIR)
        self.fs.add_real_directory(DIR)

    def test_simple(self):
        desc = Hardback(
            outfile='test.epub',
            book=Book(
                identifier='Identifier',
                title='Title',
                authors=('Tom Ritchford',),
            ),
            sources=[DIR / 'data1.txt', DIR / 'data2.txt'],
        )

        hb = hardback.Hardback(desc)

        hb.book.toc[:] = [epub.EpubHtml(**c.__dict__) for c in CHAPTERS]
        hb.add_items(*hb.book.toc)
        hb.write()


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
