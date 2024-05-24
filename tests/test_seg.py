import unittest
import sys
sys.path.append('../')
from algophon.seg import Seg
from algophon.symbols import LONG

class TestSeg(unittest.TestCase):
    def test_init(self):
        assert(Seg(ipa='i', features={'syl': '+', 'voi': '+', 'stri': '0'}))
        assert(Seg(ipa='t͡ʃ'))
        assert(Seg(ipa=f'i{LONG}'))

    def test_eq(self):
        seg = Seg(ipa='i', features={'syl': '+', 'voi': '+', 'stri': '0'})
        assert(seg == 'i')
        assert(seg != 'e')
        assert(seg == Seg(ipa='i'))

    def test_hash(self):
        seg = Seg(ipa='i', features={'syl': '+', 'voi': '+', 'stri': '0'})
        long_i = Seg(ipa=f'i{LONG}')
        assert(len({seg, 'i'}) == 1)
        assert('i' in {seg})
        assert(seg in {'i'})
        assert(len({seg, Seg(ipa='i')}) == 1)
        assert(len({seg,  long_i}) == 2)

    def test_feats(self):
        seg = Seg(ipa='i', features={'syl': '+', 'voi': '+', 'stri': '0'})
        assert(seg.features['syl'] == '+')
        assert(seg.features['stri'] == '0')

    def test_len(self):
        i = Seg(ipa='i')
        tsh = Seg(ipa='t͡ʃ')
        long_i = Seg(ipa=f'i{LONG}')
        assert(len(i) == 1)
        assert(len(tsh) == 1)
        assert(len(long_i) == 1)

    def test_getitem(self):
        seg = Seg(ipa='i', features={'syl': '+', 'voi': '+', 'stri': '0'})
        assert(seg.features['syl'] == '+')
        assert(seg.features['stri'] == '0')
        assert(seg['syl'] == '+')
        assert(seg['stri'] == '0')

        try:
            seg['cons']
            assert(False)
        except KeyError as e:
            assert(True)
            assert(e.__str__() == "'cons'")

    def test_setitem(self):
        seg = Seg(ipa='i', features={'syl': '-', 'voi': '+', 'stri': '+'})
        seg['syl'] = '+'
        seg['stri'] = '0'
        assert(seg['syl'] == '+')
        assert(seg['stri'] == '0')

        try:
            seg['cons'] = '-'
            assert(False)
        except ValueError as e:
            assert(True)
            assert(e.__str__() == ":feature: 'cons' not in self.features")


if __name__ == "__main__":
    unittest.main()