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
    cover_image: str = ''
    language: str = 'en'
    authors: Tuple[str] = ()


@dataclass
class Hardback:
    filename: str = ''
    book: Book = Factory(Book)
    bar: bool = True
    columns: int = 7
    rows: int = 5
    metadata: dict = Factory(dict)
    options: dict = Factory(dict)
