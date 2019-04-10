from typing import Tuple
from attr import dataclass, Factory


@dataclass
class Chapter:
    title: str = ''
    file_name: str = ''
    content: str = ''


@dataclass
class Book:
    identifier: str = ''
    title: str = ''
    cover: str = ''
    language: str = 'en'
    authors: Tuple[str] = ()


@dataclass
class Hardback:
    filename: str = ''
    book: Book = Factory(Book)
    enable_bar: bool = True
    remove_image_files: bool = True
    dimensions: Tuple[int] = (5, 7)
    options: dict = Factory(dict)
    outfile: str = ''
    qr_dir: str = '.output'
