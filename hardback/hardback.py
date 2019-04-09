from . write_qr_code_chunks import Writer
from . elapsed_bar import ElapsedBar
from . create_epub import EpubBook
# from . chunk_sequence import chunk_sequence
from ebooklib.epub import EpubItem


def write(filename, outdir, callback=None):
    writer = Writer(filename)
    bar = ElapsedBar('Writing files', max=writer.block_count)
    for sequence_number, result_file in enumerate(writer.write(outdir)):
        callback and callback(result_file)
        bar.next_item(result_file.name)

    bar.finish()
    return writer.file_format, sequence_number + 1, writer.metadata


def run(desc):
    book = EpubBook()
    book.add_desc(desc.book)

    writer = Writer(desc.filename)
    bar = ElapsedBar('Writing files', max=writer.block_count, enabled=desc.bar)
    block_count = 0
    for file in writer.write(desc.outdir):
        block_count += 1
        with open(file, 'rb') as fp:
            book.add_item(EpubItem(file_name=file.name, content=fp.read()))
        bar and bar.next_item(file.name)

    print('block_count', block_count, 'expected', writer.block_count)

    bar and bar.finish()


if __name__ == '__main__':
    import sys
    for i in write(*sys.argv[1:]):
        pass
