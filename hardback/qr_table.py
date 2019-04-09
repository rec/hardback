def table(entries, columns, rows):
    def end_tags(i):
        if not (i % columns):
            yield '  </tr>'
            if not (i % (rows * columns)):
                yield '</table>'

    i = 0
    for i, entry in enumerate(entries):
        if i:
            yield from end_tags(i)
        if not (i % columns):
            if not (i % (rows * columns)):
                yield '<table>'
            yield '  <tr>'
        yield f'    <td> {entry} </td>'

    if i:
        yield from end_tags(0)


def qr_table(files, columns, rows):
    t = table((f'<img src="{f}"/>' for f in files), columns, rows)
    return '\n'.join(t)
