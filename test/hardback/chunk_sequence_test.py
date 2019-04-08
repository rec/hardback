import unittest
from hardback import chunk_sequence


class ChunkSequence(unittest.TestCase):
    def test_guess_metadata_any(self):
        expected = [5, 7, 8, 11, 11, 13, 14, 17, 17, 19, 20, 23, 23, 25, 26,
                    29, 29, 31, 32, 35, 35, 37, 38, 41, 41, 43, 44]
        actual = [chunk_sequence.guess_metadata_every(i) for i in range(3, 30)]
        self.assertEqual(expected, actual)

    def test_basic_chunk_sequence_no_metadata(self):
        expected = ['x/0.png', 'x/1.png', 'x/2.png', 'x/3.png', 'x/4.png',
                    'x/5.png', 'x/6.png', 'x/7.png', 'x/8.png', 'x/9.png']
        actual = list(chunk_sequence.basic_chunk_sequence('x/%d.png', 10))
        self.assertEqual(expected, actual)

    def test_basic_chunk_sequence_metadata(self):
        expected = ['x/0.png', 'x/1.png', 'x/2.png', 'x/0.png', 'x/3.png',
                    'x/4.png', 'x/5.png', 'x/0.png', 'x/6.png', 'x/7.png',
                    'x/8.png', 'x/0.png', 'x/9.png']
        actual = list(chunk_sequence.basic_chunk_sequence('x/%d.png', 10, 3))
        self.assertEqual(expected, actual)

    def test_chunk_sequence(self):
        expected = ['x/0.png', 'x/1.png', 'x/2.png', 'x/3.png', 'x/4.png',
                    'x/5.png', 'x/6.png', 'x/7.png', 'x/8.png', 'x/9.png',
                    'x/10.png', 'x/0.png', 'x/11.png']
        actual = list(chunk_sequence.chunk_sequence('x/%d.png', 12, 6))
        self.assertEqual(expected, actual)
