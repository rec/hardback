import itertools


def table(entries, columns, rows, fillvalue=''):
    def one_table(entries):
        assert len(entries) == columns * rows
        yield '<table>'
        for y in range(rows):
            yield '  <tr>'
            for x in range(columns):
                entry = entries[x + y * columns]
                yield f'    <td> {entry} </td>'
            yield '  </tr>'

        yield '</table>'

    it = [iter(entries)] * (columns * rows)
    for group in itertools.zip_longest(*it, fillvalue=fillvalue):
        yield '\n'.join(one_table(group))


def qr_table(files, columns, rows, fillvalue=''):
    t = table((f'<img src="{f}"/>' for f in files), columns, rows, fillvalue)
    return '\n'.join(t)
