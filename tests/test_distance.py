import unittest
import sys
sys.path.append('../')
from algophon.distance import edit_distance

class TestDistance(unittest.TestCase):
    def test_edit_distance(self):
        s1, s2 = 'k i t t e n', 's i t t i n g'
        assert(edit_distance.distance(s1, s2) == 3)
        assert(edit_distance.alignments(s1, s2) == [('k i t t e n _', 's i t t i n g')])

        assert(edit_distance.distance(s1, s1) == 0)
        assert(edit_distance.alignments(s1, s1) == [(s1, s1)])

        s1 = 'c a t'
        s2 = 'u n c a t i s'
        assert(edit_distance.distance(s1, s2) == 4)
        assert(edit_distance.alignments(s1, s2) == [('_ _ c a t _ _', s2)])

if __name__ == "__main__":
    unittest.main()