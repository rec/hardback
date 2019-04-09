import unittest
from hardback import chunk_sequence


class ChunkSequence(unittest.TestCase):
    def test_metadata_any(self):
        expected = [5, 7, 8, 11, 11, 13, 14, 17, 17, 19, 20, 23, 23, 25, 26,
                    29, 29, 31, 32, 35, 35, 37, 38, 41, 41, 43, 44]
        actual = [chunk_sequence.guess_metadata_every(i) for i in range(3, 30)]
        self.assertEqual(expected, actual)

    def test_chunk_sequence_7(self):
        expected = ['x/0.png', 'x/1.png', 'x/2.png', 'x/3.png',
                    'x/4.png', 'x/0.png', 'x/5.png', 'x/6.png']
        items = (f'x/{i}.png' for i in range(7))
        actual = list(chunk_sequence.chunk_sequence(items, 3))
        self.assertEqual(expected, actual)

    def test_chunk_sequence_12(self):
        expected = ['x/0.png', 'x/1.png', 'x/2.png', 'x/3.png', 'x/4.png',
                    'x/5.png', 'x/6.png', 'x/7.png', 'x/8.png', 'x/9.png',
                    'x/10.png', 'x/0.png', 'x/11.png']
        items = (f'x/{i}.png' for i in range(12))
        actual = list(chunk_sequence.chunk_sequence(items, 6))
        self.assertEqual(expected, actual)
