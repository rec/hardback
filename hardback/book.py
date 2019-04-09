from typing import Tuple
from attr import dataclass, Factory


@dataclass
class DublinCore:
    contributor: str = ''
    coverage: str = ''
    creator: str = ''
    date: str = ''
    description: str = ''
    format: str = ''
    identifier: str = ''
    language: str = ''
    publisher: str = ''
    relation: str = ''
    rights: str = ''
    source: str = ''
    subject: str = ''
    title: str = ''
    type: str = ''


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
