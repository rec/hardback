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
class Book:
    identifier: str = ''
    title: str = ''
    language: str = 'en'


@dataclass
class Layout:
    identifier: str = ''
    title: str = ''
    language: str = 'en'
