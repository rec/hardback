"""Contains data classes that specify how a book is put together"""

from typing import List, Tuple
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
    authors: Tuple[str] = ()


@dataclass(slots=True)
class Hardback:
    filename: str = ''
    book: Book = Factory(Book)
    dimensions: List[int] = Factory(lambda: [5, 7])
    outfile: str = ''
    qr_writer: Writer = Factory(Writer)

    options: dict = Factory(dict)
    progress_bar: bool = True
    remove_image_files: bool = True
    qr_dir: str = '.output'
