"""Contains data classes that specify how a book is put together"""

from .. qr.writer import Writer
from attr import dataclass, Factory
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


@dataclass(slots=True)
class Hardback:
    source: str = ''
    book: Book = Factory(Book)
    dimensions: List[int] = Factory(lambda: [5, 7])
    outfile: str = ''
    qr: Writer = Factory(Writer)

    options: dict = Factory(dict)
    progress_bar: bool = True
    remove_image_files: bool = True
    qr_image_dir: str = '.output'
