"""Contains data classes that specify how a book is put together"""


from typing import List, Tuple
from attr import dataclass, Factory


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
    enable_bar: bool = True
    remove_image_files: bool = True
    dimensions: List[int] = Factory(lambda: [5, 7])
    options: dict = Factory(dict)
    outfile: str = ''
    qr_dir: str = '.output'
