"""Contains data classes that specify how a book is put together"""

from typing import List
from attr import dataclass, Factory
from .qr.writer import Writer


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
    filename: str = ''
    book: Book = Factory(Book)
    dimensions: List[int] = Factory(lambda: [5, 7])
    outfile: str = ''
    qr: Writer = Factory(Writer)

    options: dict = Factory(dict)
    progress_bar: bool = True
    remove_image_files: bool = True
    qr_image_dir: str = '.output'


@dataclass
class Font:
    name: str = '/Library/Fonts/Courier New Bold.ttf'
    size: int = 14


@dataclass
class Cover:
    title: str = ''
    font: Font = Factory(Font)
    margin: List[int] = Factory(lambda: [75, 50])
    dimensions: List[int] = Factory(lambda: [2560, 1600])
    # https://blog.reedsy.com/book-cover-dimensions/
