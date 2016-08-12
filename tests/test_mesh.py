
import time
import unittest

from hpastar import mesh


class TestStringMethods(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.m = mesh.MeshLeaf((10, 10), (0, 0), {})
        self.m.make_open()
        BLOCKED = [
            (1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8),

            (3, 4), (3, 5), (4, 1), (4, 2),
            (4, 3), (4, 4), (4, 5), (4, 6),
            (4, 7), (4, 8), (5, 1), (5, 2),
            (5, 3), (5, 4), (5, 5), (5, 6),
            (5, 7), (5, 8), (6, 2), (6, 3),
            (6, 4), (6, 5), (6, 6), (6, 7),
            (7, 3), (7, 4), (7, 5)
        ]  # try toggling (5, 3)  ;)

        for each in BLOCKED:
            self.m.add_blocked(each)

    def test_graph(self):
        self.assertIsNotNone(self.m.graph)

    def test_contains(self):

        self.assertTrue(self.m.contains((0, 0)))
        self.assertTrue(self.m.contains((3, 7)))
        self.assertTrue(self.m.contains((9, 9)))
        self.assertFalse(self.m.contains((10, 10)))
        self.assertFalse(self.m.contains((3, 17)))
        self.assertFalse(self.m.contains((-5, 0)))

    def test_path(self):
        t0 = time.time()
        out = self.m.path((2, 4), (8, 5))
        t1 = time.time()
        delta = t1 - t0

        self.assertIsNotNone(out)
        self.assertLess(delta, 0.001)

    def test_groups(self):
        self.assertDictEqual(self.m.groups, {})
        self.assertDictEqual(self.m.landlocked_groups, {})
        self.assertDictEqual(self.m.open_groups, {})

        t0 = time.time()
        self.m.calculate_local_groups()
        t1 = time.time()
        delta = t1 - t0
        self.assertLess(delta, 0.001)

        groups = {0: self.m.navigable()}
        self.assertDictEqual(self.m.groups, groups)
        self.assertDictEqual(self.m.landlocked_groups, {})
        self.assertDictEqual(self.m.open_groups, groups)

        self.assertIs(self.m.groups[0], self.m.open_groups[0])

if __name__ == '__main__':
    unittest.main()
