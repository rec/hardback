"""Contains data classes that specify how a book is put together"""

from .. qr.qr import QR
from attr import dataclass, Factory
from pathlib import Path
from typing import List


@dataclass
class Chapter:
    title: str = ''
    file_name: str = ''
    content: str = ''


@dataclass(slots=True)
class Book:
    identifier: str = ''
    title: str = ''
    cover: str = ''
    language: str = 'en'
    authors: List[str] = Factory(list)

    def apply(self, ebook):
        ebook.set_identifier(self.identifier)
        ebook.set_title(self.title)
        ebook.set_language(self.language)

        for a in self.authors:
            ebook.add_author(a)

        if self.cover:
            with open(self.cover, 'rb') as fp:
                filename = 'cover_' + Path(self.cover).name
                ebook.set_cover(filename, fp.read())


@dataclass(slots=True)
class Hardback:
    sources: List[str] = Factory(list)
    book: Book = Factory(Book)
    dimensions: List[int] = Factory(lambda: [5, 7])
    outfile: str = ''
    qr: QR = Factory(QR)

    options: dict = Factory(dict)
    progress_bar: bool = True
    remove_image_files: bool = True
    qr_image_dir: str = '.output'
