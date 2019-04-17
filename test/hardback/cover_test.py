import unittest
from hardback.cover import Cover, Font
from pathlib import Path
from PIL import Image
from test.hardback import skip_tests

BASE = Path(__file__).parent
COVER_IMAGE = BASE / 'laser.png'
COVER_RESULT = BASE / 'cover_result.png'
COVER = Cover(title='Test', image=COVER_IMAGE, font=Font(size=100))


class CoverTest(unittest.TestCase):
    @skip_tests.travis
    def test_cover(self):
        actual = COVER.render()
        expected = Image.open(COVER_RESULT)
        self.assertEqual(actual.tobytes(), expected.tobytes())


if __name__ == '__main__':
    COVER.render().save(COVER_RESULT)
