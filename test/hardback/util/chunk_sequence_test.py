import unittest
from hardback.util import chunk_sequence


class ChunkSequence(unittest.TestCase):
    def test_metadata_any(self):
        expected = [
            4,
            6,
            8,
            10,
            11,
            12,
            13,
            16,
            17,
            18,
            20,
            22,
            22,
            24,
            26,
            28,
            29,
            30,
            31,
            34,
            35,
            36,
            38,
            40,
            40,
            42,
            44,
        ]
        actual = [chunk_sequence.guess_metadata_every(i) for i in range(3, 30)]
        self.assertEqual(expected, actual)

    def test_chunk_sequence_7(self):
        expected = [
            'x/0.png',
            'x/1.png',
            'x/2.png',
            'x/3.png',
            'x/0.png',
            'x/4.png',
            'x/5.png',
            'x/6.png',
        ]
        items = (f'x/{i}.png' for i in range(7))
        actual = list(chunk_sequence.chunk_sequence(items, 1, 3))
        self.assertEqual(expected, actual)

    def test_chunk_sequence_12(self):
        expected = [
            'x/0.png',
            'x/1.png',
            'x/2.png',
            'x/3.png',
            'x/4.png',
            'x/5.png',
            'x/6.png',
            'x/7.png',
            'x/8.png',
            'x/9.png',
            'x/0.png',
            'x/10.png',
            'x/11.png',
        ]
        items = (f'x/{i}.png' for i in range(12))
        actual = list(chunk_sequence.chunk_sequence(items, 2, 3))
        self.assertEqual(expected, actual)
