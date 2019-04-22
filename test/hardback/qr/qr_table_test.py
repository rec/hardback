import unittest
from hardback.qr.qr_table import qr_table


def join_qr(file_count, columns, rows):
    files = ('x/%d.png' % i for i in range(file_count))
    return '\n'.join(qr_table(files, columns, rows))


class QrTableTest(unittest.TestCase):
    maxDiff = 10000

    def test_simple(self):
        self.assertEqual(join_qr(0, 1, 1), '')

    def test_small(self):
        self.assertEqual(SMALL_RESULT, join_qr(5, 2, 3))

    def test_big(self):
        self.assertEqual(BIG_RESULT, join_qr(12, 2, 3))


SMALL_RESULT = """\
<table>
  <tr>
    <td style="width:50.0%;"> <img src="x/0.png"/> </td>
    <td style="width:50.0%;"> <img src="x/1.png"/> </td>
  </tr>
  <tr>
    <td> <img src="x/2.png"/> </td>
    <td> <img src="x/3.png"/> </td>
  </tr>
  <tr>
    <td> <img src="x/4.png"/> </td>
    <td></td>
  </tr>
</table>\
"""

BIG_RESULT = """\
<table>
  <tr>
    <td style="width:50.0%;"> <img src="x/0.png"/> </td>
    <td style="width:50.0%;"> <img src="x/1.png"/> </td>
  </tr>
  <tr>
    <td> <img src="x/2.png"/> </td>
    <td> <img src="x/3.png"/> </td>
  </tr>
  <tr>
    <td> <img src="x/4.png"/> </td>
    <td> <img src="x/5.png"/> </td>
  </tr>
</table>
<table>
  <tr>
    <td style="width:50.0%;"> <img src="x/6.png"/> </td>
    <td style="width:50.0%;"> <img src="x/7.png"/> </td>
  </tr>
  <tr>
    <td> <img src="x/8.png"/> </td>
    <td> <img src="x/9.png"/> </td>
  </tr>
  <tr>
    <td> <img src="x/10.png"/> </td>
    <td> <img src="x/11.png"/> </td>
  </tr>
</table>\
"""
