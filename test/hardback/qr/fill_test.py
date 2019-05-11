from hardback.qr import fill
from hardback.qr.constants import Default
from hardback.qr.qr import QR
import copy
import unittest

DEFAULT = QR(Default.version, Default.error, Default.block_size)


def filler(qr):
    qr = copy.deepcopy(qr)
    fill.fill_qr(qr)
    return qr


def fill_from(**kwds):
    return filler(QR(**kwds))


class FillTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(filler(QR()), DEFAULT)
        self.assertEqual(filler(DEFAULT), DEFAULT)

    def test_all_filled(self):
        qr = QR(version=30, error='M', block_size=200)
        self.assertEqual(qr, filler(qr))

    def test_fill_block_size1(self):
        qr = QR(version=25, error='M')
        expected = QR(version=25, error='M', block_size=981)
        self.assertEqual(expected, filler(qr))

    def test_fill_block_size2(self):
        qr = QR(version=25)
        expected = QR(version=25, error='H', block_size=519)
        self.assertEqual(expected, filler(qr))

    def test_fill_error1(self):
        qr = QR(version=25, block_size=981)
        expected = QR(version=25, error='M', block_size=981)
        self.assertEqual(expected, filler(qr))

    def test_fill_version1(self):
        qr = QR(block_size=981, error='M')
        expected = QR(version=25, error='M', block_size=981)
        self.assertEqual(expected, filler(qr))

    def test_XXX(self):
        fill_from(block_size=2937)

    def test_fill_error2(self):
        # Edge cases occur for versions "near 40"
        ranges = (
            (2316, 2938, 40, 'L'),
            (1648, 2316, 40, 'M'),
            (1258, 1648, 40, 'Q'),
            (1204, 1258, 40, 'H'),
            (1258, 1124, 39, 'L'),
        )

        for begin, end, version, error in ranges:
            for block_size in range(begin, end):
                actual = fill_from(block_size=block_size)
                expected = QR(
                    version=version, error=error, block_size=block_size
                )
                self.assertEqual(expected, actual)

    def test_raises(self):
        fill_from()
        for e in fill.ERRORS:
            fill_from(error=e)

        for v in range(0, fill.MAX_VERSION + 1):
            fill_from(version=v)

        with self.assertRaises(ValueError):
            fill_from(block_size=2938)

        fill_from(version=40, block_size=2937)

        with self.assertRaises(ValueError):
            fill_from(version=39, block_size=2937)

        with self.assertRaises(ValueError):
            fill_from(version=1, block_size=2937)

        fill_from(version=0, block_size=2937)
        fill_from(version=1, block_size=1)

        with self.assertRaises(ValueError):
            fill_from(version=1, block_size=2)

        for b in range(2, 10):
            fill_from(version=1, block_size=b, document_bytes=4, index_bytes=4)
        with self.assertRaises(ValueError):
            b += 1
            fill_from(version=1, block_size=b, document_bytes=4, index_bytes=4)
