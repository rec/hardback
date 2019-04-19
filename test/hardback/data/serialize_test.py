import unittest
from attr import dataclass, Factory
from hardback.data.serialize import serialize, unserialize
from hardback.data.dataclass import Hardback


class SerializeTest(unittest.TestCase):
    def test_round_trip(self):
        c = Child()
        c.bar = 'bar'
        c.child.baz = 'baz'

        ser = serialize(c)
        d = unserialize(ser, Child())
        self.assertEqual(c, d)

    def test_round_trip2(self):
        p1 = Parent()
        p1.foo = 'foo'
        p1.child.bar = 'bar'
        p1.child.child.baz = 'baz'

        ser = serialize(p1)
        p2 = unserialize(ser, Parent())
        self.assertEqual(p1, p2)

    def test_round_trip_fail(self):
        p1 = Parent()
        p1.foo = 'foo'
        p1.child.bar = 'bar'
        p1.child.child.baz = 1  # wrong type!

        ser = serialize(p1)
        p2 = unserialize(ser, Parent())
        self.assertNotEqual(p1, p2)

    def test_hardback(self):
        p1 = Hardback()
        p1.sources = ['foo']
        p1.dimensions = [3, 3]
        p1.progress_bar = False
        p1.book.identifier = 'id'
        p1.book.cover = 'dontjudge.png'

        ser = serialize(p1)
        p2 = unserialize(ser, Hardback())
        self.assertEqual(p1, p2)


@dataclass
class Grandchild:
    baz: str = ''


@dataclass
class Child:
    bar: str = ''
    child: Grandchild = Factory(Grandchild)


@dataclass
class Parent:
    foo: str = ''
    child: Child = Factory(Child)
