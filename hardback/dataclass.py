"""Contains data classes that specify how a book is put together"""

from .qr.writer import Writer
from PIL import ImageFont
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


@dataclass
class Font:
    name: str = '/Library/Fonts/Courier New Bold.ttf'
    size: int = 0

    def make_image_font(self):
        suffix = Path(self.name).suffix
        if suffix == '.tff':
            if not self.size:
                raise ValueError(f'Size needs to be set for Truetype fonts')
            return ImageFont.truetype(self.name, self.size)

        if suffix == '.pil':
            if self.size:
                raise ValueError(f'Size cannot be set for Bitmap fonts')
            return ImageFont.load(self.name)

        raise ValueError(f'Do not understand file {self.file}')


@dataclass
class Cover:
    title: str = ''
    font: Font = Factory(Font)
    margin: List[int] = Factory(lambda: [75, 50])
    dimensions: List[int] = Factory(lambda: [2560, 1600])
    # https://blog.reedsy.com/book-cover-dimensions/
