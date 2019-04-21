from pathlib import Path

SUFFIXES = '.jpeg', '.jpg', '.png'


def fill_book(book, sources):
    if not book.cover:
        p = [i for i in sources if Path(i).suffix in SUFFIXES]
        book.cover = p and p[0]

    head = Path(sources[0])
    if not book.title:
        book.title = head.name
        if len(sources) > 1:
            book.title += ', ...'
