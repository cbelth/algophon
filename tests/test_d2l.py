import unittest
import sys

sys.path.append('../')
from algophon import SegInv, SegStr, NatClass
from algophon.models.D2L import Tier, Rule, D2L
from algophon.symbols import LWB, RWB

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

    def test_tier_project(self):
        seginv = SegInv()
        seginv.add_segs({'a', 'e', 'i', 'o', 'u', 'p', 't', 'b', 'd'})
        tier = Tier(seginv=seginv, feats={'+syl'})
        segstr = SegStr('p e t a t', seginv=seginv)
        projected = tier.project(segstr)
        assert(projected == 'e a')
        assert(isinstance(projected, SegStr))
        assert(isinstance(projected, Tier.Projection))
        assert(projected.idxs == [1, 3])

    def test_rule_init(self):
        seginv = SegInv()
        rule = Rule(seginv=seginv, target={'S'}, left_ctxts=NatClass(feats={'+strid'}, seginv=seginv))
        assert(rule and rule.left_ctxts is not None and rule.right_ctxts is None)
        rule = Rule(seginv=seginv, target={'S'}, left_ctxts={'S', 's', 'ʃ'})
        assert(rule and rule.left_ctxts is not None and rule.right_ctxts is None)

        rule = Rule(seginv=seginv, target={'S'}, right_ctxts=NatClass(feats={'+strid'}, seginv=seginv))
        assert(rule and rule.left_ctxts is None and rule.right_ctxts is not None)
        rule = Rule(seginv=seginv, target={'S'}, right_ctxts={'S', 's', 'ʃ'})
        assert(rule and rule.left_ctxts is None and rule.right_ctxts is not None)

        try:
            Rule(seginv=seginv, target={'S'}, left_ctxts=NatClass(feats={'+strid'}, seginv=seginv), right_ctxts={'S', 's', 'ʃ'})
            assert(False)
        except ValueError as e:
            assert(e.__str__() == 'D2L Rule cannot have both left and right contexts.')
            assert(True)

        try:
            Rule(seginv=seginv, target={'S'})
            assert(False)
        except ValueError as e:
            assert(e.__str__() == 'D2L Rule must have either left or right contexts.')
            assert(True)


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

    def test_D2L__get_tier_adj_contexts(self):
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
        pairs = d2l._train_setup(pairs)
        assert(d2l._get_tier_adj_contexts(discrepancy=d2l._discrepancy, 
                                          tier=None) == ({'u', 'i', 'a', 'o', 't'}, 
                                                         {'i', RWB}))
        assert(d2l._get_tier_adj_contexts(discrepancy=d2l._discrepancy, 
                                          tier=Tier(seginv=d2l.seginv, feats={'+cons'})) == ({'k', 'S', 'ʃ', 'n', 'g', 't'}, 
                                                                                             {'S', RWB}))
        # overwrite weird Panphon values
        d2l.seginv['s'].features['strid'] = '+'
        d2l.seginv['ʃ'].features['strid'] = '+'
        d2l.seginv['S'].features['strid'] = '+'
        assert(d2l._get_tier_adj_contexts(discrepancy=d2l._discrepancy, 
                                          tier=Tier(seginv=d2l.seginv, feats={'+strid'})) == ({'s', 'ʃ', 'S', LWB}, 
                                                                                              {'S', RWB}))
        
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