import unittest
import sys

sys.path.append('../')
from algophon import SegInv, SegStr, NatClass
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

    def test_D2L__train_setup(self):
        pairs = [
            ('ʃ o k u S i S', 'ʃ o k u ʃ i ʃ'), 
            ('a p ʃ a S', 'a p ʃ a ʃ'),
            ('ʃ u n i S', 'ʃ u n i ʃ'),
            ('s o k i S', 's o k i s'),
            ('s i g o S i S', 's i g o s i s'),
            ('u t S', 'u t s')
        ]
        d2l = D2L(verbose=False)
        setup_pairs = d2l._train_setup(pairs)
        assert('S' in d2l.seginv) # make sure abstract URs are created
        assert(len(setup_pairs) == len(pairs))
        assert(setup_pairs == set(pairs))
        assert(isinstance(list(setup_pairs)[0][0], SegStr))
        assert(isinstance(list(setup_pairs)[0][1], SegStr))
        assert(d2l._discrepancy is not None)
        assert(d2l._discrepancy.alternations == {('S', 's'), ('S', 'ʃ')})
        assert(len(d2l._discrepancy.instances) == 9)

        # make sure duplicates are removed

        pairs = [
            ('ʃ o k u S i S', 'ʃ o k u ʃ i ʃ'), 
            ('a p ʃ a S', 'a p ʃ a ʃ'),
            ('ʃ u n i S', 'ʃ u n i ʃ'),
            ('s o k i S', 's o k i s'),
            ('ʃ u n i S', 'ʃ u n i ʃ'), # duplicate
            ('s o k i S', 's o k i s'), # duplicate
            ('s i g o S i S', 's i g o s i s'),
            ('u t S', 'u t s'),
            ('u t S', 'u t s'), # duplicate
        ]
        d2l = D2L(verbose=False)
        setup_pairs = d2l._train_setup(pairs)
        assert('S' in d2l.seginv)
        assert(len(setup_pairs) == len(pairs) - 3)
        assert(setup_pairs == set(pairs))
        assert(isinstance(list(setup_pairs)[0][0], SegStr))
        assert(isinstance(list(setup_pairs)[0][1], SegStr))
        assert(d2l._discrepancy is not None)
        assert(d2l._discrepancy.alternations == {('S', 's'), ('S', 'ʃ')})
        assert(len(d2l._discrepancy.instances) == 9)
        
    def test_D2L_paper_example(self):
        pairs = [
            ('ʃ o k u S i S', 'ʃ o k u ʃ i ʃ'), 
            ('a p ʃ a S', 'a p ʃ a ʃ'),
            ('ʃ u n i S', 'ʃ u n i ʃ'),
            ('s o k i S', 's o k i s'),
            ('s i g o S i S', 's i g o s i s'),
            ('u t S', 'u t s')
        ]
        d2l = D2L(verbose=False)
        d2l.train(pairs)

if __name__ == "__main__":
    unittest.main()