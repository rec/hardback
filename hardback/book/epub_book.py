from pathlib import Path
from ebooklib import epub

CSS_DIR = Path(__file__).parents[2] / 'css'


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

        self.default_css = make_css('default')
        self.add_item(self.default_css)

    def add_items(self, *items):
        for i in items:
            self.add_item(i)

    def write(self, outfile, **options):
        self.add_items(epub.EpubNcx(), epub.EpubNav(), make_css('nav'))
        self.spine = ['nav'] + self.toc
        epub.write_epub(outfile, self, options)


def make_css(name):
    return epub.EpubItem(
        uid=f'style_{name}',
        file_name=f'style/{name}.css',
        media_type='text/css',
        content=open(CSS_DIR / f'{name}.css').read())
