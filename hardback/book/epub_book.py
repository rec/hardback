from pathlib import Path
from ebooklib import epub, utils

CSS_DIR = Path(__file__).parents[2] / 'css'


class EpubBook(epub.EpubBook):
    page_number = 0

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

    def add_chapters(self, chapters):
        self.add_items(*chapters)
        self.toc = chapters
        self.add_items(epub.EpubNcx(), epub.EpubNav(), make_css('nav'))
        self.spine = ['nav'] + chapters

    def add_items(self, *items):
        for i in items:
            self.add_item(i)

    def add_pagebreak(self):
        self.page_number += 1
        pn = str(self.page_number)
        return utils.create_pagebreak(pn, pn)

    def write(self, outfile, **options):
        epub.write_epub(outfile, self, options)


def make_css(name):
    return epub.EpubItem(
        uid=f'style_{name}',
        file_name=f'style/{name}.css',
        media_type='text/css',
        content=open(CSS_DIR / f'{name}.css').read())
