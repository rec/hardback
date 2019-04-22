from ebooklib import epub
from . css import make_css


class EpubBook(epub.EpubBook):
    def add_desc(self, book):
        book.apply(self)
        self.default_css = make_css('default')
        self.add_item(self.default_css)

    def add_items(self, *items):
        for i in items:
            self.add_item(i)

    def write(self, outfile, **options):
        self.add_items(epub.EpubNcx(), epub.EpubNav(), make_css('nav'))
        self.spine = ['nav'] + self.toc
        epub.write_epub(outfile, self, options)
