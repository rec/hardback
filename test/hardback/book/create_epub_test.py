from hardback.book import epub_book
from pyfakefs.fake_filesystem_unittest import TestCase as FakeTestCase


class CreateEpubTest(FakeTestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.add_real_directory(epub_book.CSS_DIR)

    def test_simple(self):
        epub_book.test_write()
