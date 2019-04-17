from hardback.book import create_epub
from pyfakefs.fake_filesystem_unittest import TestCase as FakeTestCase


class CreateEpubTest(FakeTestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.add_real_directory(create_epub.CSS_DIR)

    def test_simple(self):
        create_epub.test_write()
