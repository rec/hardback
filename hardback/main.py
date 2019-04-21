import yaml, pathlib
from . book import cursor, hardback, sections
from . data import serialize, dataclass

_DATA_SUFFIXES = '.json', '.yml'
NEW_CHAPTERS = False


def main(files):
    desc = dataclass.Hardback()
    for f in files:
        if pathlib.Path(f).suffix in _DATA_SUFFIXES:
            serialize.unserialize(f, desc)
        else:
            desc.sources.append(f)

    hb = hardback.Hardback(desc)
    chapters = []

    print(yaml.dump(serialize.serialize(hb.desc)))

    for hc in cursor.HardbackCursor(hb):
        if NEW_CHAPTERS:
            chapters.append(sections.chapter(hc))
        else:
            chapters.extend([sections.metadata(hc), sections.qr(hc)])

    hb.book.add_chapters(chapters)
    hb.write()


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
