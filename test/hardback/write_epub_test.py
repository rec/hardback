from hardback import write_epub
from pyfakefs.fake_filesystem_unittest import TestCase as FakeTestCase


class WriteEpubTest(FakeTestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.add_real_directory(write_epub.CSS_DIR)

    def test_simple(self):
        write_epub.test_write()
