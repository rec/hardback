import yaml, pathlib
from . book import cursor, hardback, sections
from . data import serialize, dataclass

_DATA_SUFFIXES = '.json', '.yml'


def main(files):
    desc = dataclass.Hardback()
    for f in files:
        if pathlib.Path(f).suffix in _DATA_SUFFIXES:
            serialize.unserialize(f, desc)
        else:
            desc.sources.append(f)

    print(yaml.dump(serialize.serialize(desc)))

    hb = hardback.Hardback(desc)
    chapters = [sections.chapter(hc) for hc in cursor.HardbackCursor(hb)]
    hb.book.add_chapters(chapters)
    hb.write()


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
