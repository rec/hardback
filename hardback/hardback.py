import yaml
from . import chunk_sequence, create_epub, elapsed_bar, qr_table, write_chunks
from ebooklib import epub


def run(desc):
    book = create_epub.EpubBook()
    book.add_desc(desc.book)

    writer = write_chunks.Writer(desc.filename)
    bar = elapsed_bar.ElapsedBar(
        'Writing', max=writer.block_count, enabled=desc.bar)
    block_count = 0

    def items():
        for file in writer.write(desc.outdir):
            nonlocal block_count
            block_count += 1
            with open(file, 'rb') as fp:
                item = epub.EpubItem(file_name=file.name, content=fp.read())
                book.add_item(item)
            desc.remove and file.unlink()
            bar.next_item(file.name)
            yield file

    chunks = chunk_sequence(items(), desc.columns * desc.rows)

    metadata = dict(writer.metadata, **desc.metadata)
    chapter1 = epub.EpubHtml(
        title='Metadata',
        file_name='chapter1.xhtml',
        content='<pre>\n%s\n</pre>' % yaml.dump(metadata))

    chapter2 = epub.EpubHtml(
        title=desc.filename,
        file_name='chapter2.xhtml',
        content=qr_table.qr_table(chunks, desc.columns, desc.rows))

    book.add_chapters([chapter1, chapter2])
    book.write(desc.outfile, **desc.options)

    bar.finish()


if __name__ == '__main__':
    # import sys
    from . import book
    for i in run(book.Hardback()):
        pass
