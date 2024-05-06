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
        assert(edit_distance.alignments(s1, s2) == [('_ _ c a t _ _', 'u n c a t i s')])

        s1 = 'v i n t n e r'
        s2 = 'w r i t e r s'
        assert(edit_distance.distance(s1, s2) == 5)
        assert(edit_distance.alignments(s1, s2) == [
            ('v _ i n t n e r _', 'w r i _ t _ e r s'),
            ('_ v i n t n e r _', 'w r i _ t _ e r s'),
            ('v i n t n e r _', 'w r i t _ e r s')
        ])

        s1 = 'q a c d b d'
        s2 = 'q a w x b'
        assert(edit_distance.distance(s1, s2) == 3)
        assert(edit_distance.alignments(s1, s2) == [('q a c d b d', 'q a w x b _')])

if __name__ == "__main__":
    unittest.main()