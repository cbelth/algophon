import unittest
import sys

sys.path.append('../')
from algophon import SegInv, NatClass
from algophon.models.D2L import Tier, Rule, D2L

class TestD2L(unittest.TestCase):
    def test_tier_init(self):
        seginv = SegInv()
        tier = Tier(seginv=seginv, feats={'+syl'})
        assert(tier)
        assert(isinstance(tier._tierset, NatClass))
        assert(f'{tier}' == '[+syl]')

        tier = Tier(seginv=seginv, feats=NatClass({'+syl'}, seginv=seginv))
        assert(tier)
        assert(isinstance(tier._tierset, NatClass))
        assert(f'{tier}' == '[+syl]')

        seginv.add_segs({'a', 'e', 'i', 'o', 'u'})
        tier = Tier(seginv=seginv, segs={'a', 'e', 'i', 'o', 'u'})
        assert(tier)
        assert(isinstance(tier._tierset, set))
        assert(f'{tier}' == '{a,e,i,o,u}')

    def test_tier_contains(self):
        seginv = SegInv()
        seginv.add_segs({'a', 'e', 'i', 'o', 'u', 'p', 't', 'b', 'd'})
        tier = Tier(seginv=seginv, feats={'+syl'})
        assert(all(v in tier for v in {'a', 'e', 'i', 'o', 'u'}))
        assert(not any(c in tier for c in {'p', 't', 'b', 'd'}))
        
        tier = Tier(seginv=seginv, segs={'a', 'e', 'i', 'o', 'u'})
        assert(all(v in tier for v in {'a', 'e', 'i', 'o', 'u'}))
        assert(not any(c in tier for c in {'p', 't', 'b', 'd'}))

    def test_D2L_init(self):
        d2l = D2L(verbose=False)
        assert(d2l is not None)
        assert(d2l.seginv is not None)
        
    def test_D2L_paper_example(self):
        train = [
            ('ʃ o k u S i S', 'ʃ o k u ʃ i ʃ'), 
            ('a p ʃ a S', 'a p ʃ a ʃ'),
            ('ʃ u n i S', 'ʃ u n i ʃ'),
            ('s o k i S', 's o k i s'),
            ('s i g o S i S', 's i g o s i s'),
            ('u t S', 'u t s')
        ]
        d2l = D2L(verbose=False)
        d2l.train(train)

if __name__ == "__main__":
    unittest.main()