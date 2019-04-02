def writeqr_qrcode(count, version, filename):
    import qrcode, qrcode.image.svg

    data = bytes(i % 256 for i in range(count))
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        image_factory=qrcode.image.svg.SvgPathImage)
    qr.add_data(data)
    qr.make_image().save(filename)


def writeqr_segno(count, version, filename):
    import segno
    data = bytes(i % 256 for i in range(count))
    qr = segno.make_qr(data, version=version, error='H')
    qr.save(filename)


writeqr = writeqr_segno


if __name__ == '__main__':
    for count in 10, 20:
        writeqr(count, 36, '/tmp/qr%d.png' % count)

    for count in range(1020, 1060, 10):
        writeqr(count, 36, '/tmp/qr%d.png' % count)
