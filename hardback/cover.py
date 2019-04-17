from attr import dataclass, Factory
from pathlib import Path
from typing import List
from PIL import Image, ImageDraw, ImageFont

# TODO: this only works for MacOS
DEFAULT_FONT = '/Library/Fonts/Arial.ttf'


@dataclass
class Font:
    name: str = ''
    size: int = 0

    def create(self):
        name = self.name or DEFAULT_FONT
        suffix = Path(name).suffix
        if suffix == '.ttf':
            if not self.size:
                raise ValueError(f'Size must be set for Truetype fonts')
            return ImageFont.truetype(name, self.size)

        if suffix == '.pil':
            if self.size:
                raise ValueError(f'Size cannot be set for Bitmap fonts')
            return ImageFont.load(name)

        raise ValueError(f'Do not understand font {name}')


@dataclass
class Cover:
    title: str = ''
    image: str = ''
    font: Font = Factory(Font)
    margin: List[int] = Factory(lambda: [75, 50])
    size: List[int] = Factory(lambda: [1600, 2560])

    def render(self):
        image = Image.new('RGB', self.size, 'white')
        draw = ImageDraw.Draw(image)
        y = self.margin[1]

        if self.title:
            font = self.font.create()
            w, h = font.getsize(self.title)
            x = (self.size[0] - w) // 2
            y = self.margin[1]
            draw.text((x, y), text=self.title, font=font, fill='black')
            y += self.margin[1] + h

        if self.image:
            cimage = Image.open(self.image)
            isize = (self.size[0] - 2 * self.margin[0],
                     self.size[1] - (y + self.margin[1]))
            ratio = min(x / y for (x, y) in zip(isize, cimage.size))
            new_size = [round(ratio * i) for i in cimage.size]
            cimage = cimage.resize(new_size, Image.BOX)
            image.paste(cimage, (self.margin[0], y))
        return image


# See https://blog.reedsy.com/book-cover-dimensions/
