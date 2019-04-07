import typing
from attr import dataclass


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
    filename: str = ''
    content: str = ''
    properties: str = ''


@dataclass
class Book:
    identifier: str = ''
    title: str = ''
    cover_image: str = ''
    language: str = 'en'
    authors: typing.Tuple[str] = ()
    outfile: str = 'test.epub'
    chapters: typing.Tuple[Chapter] = ()
