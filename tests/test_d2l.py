import unittest
import sys

sys.path.append('../')
from algophon import SegInv, SegStr, NatClass
from algophon.models.D2L import Tier, Rule, D2L
from algophon.symbols import LWB, RWB, UNDERSPECIFIED

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
        rule = Rule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, left_ctxts=NatClass(feats={'+strid'}, seginv=seginv))
        assert(rule and rule.left_ctxts is not None and rule.right_ctxts is None)
        rule = Rule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, left_ctxts={'S', 's', 'ʃ'})
        assert(rule and rule.left_ctxts is not None and rule.right_ctxts is None)

        rule = Rule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, right_ctxts=NatClass(feats={'+strid'}, seginv=seginv))
        assert(rule and rule.left_ctxts is None and rule.right_ctxts is not None)
        rule = Rule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, right_ctxts={'S', 's', 'ʃ'})
        assert(rule and rule.left_ctxts is None and rule.right_ctxts is not None)

        try:
            Rule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, left_ctxts=NatClass(feats={'+strid'}, seginv=seginv), right_ctxts={'S', 's', 'ʃ'})
            assert(False)
        except ValueError as e:
            assert(e.__str__() == 'D2L Rule cannot have both left and right contexts.')
            assert(True)

        try:
            Rule(seginv=seginv, features={'ant', 'distr'}, target={'S'})
            assert(False)
        except ValueError as e:
            assert(e.__str__() == 'D2L Rule must have either left or right contexts.')
            assert(True)
            
    def test_rule__apply(self):
        seginv = SegInv()
        seginv.add_segs({'a', 'e', 'i', 'o', 'u', 'b', 'd', 'm', 'n', 'l'})
        # make custom seg
        features = dict(seginv['m'].features)
        features['son'] = UNDERSPECIFIED
        features['nas'] = UNDERSPECIFIED
        seginv.add_custom('C1', features=features) # m ~ b
        features = dict(seginv['n'].features)
        features['son'] = UNDERSPECIFIED
        features['nas'] = UNDERSPECIFIED
        seginv.add_custom('C2', features=features) # n ~ d

        tier = Tier(seginv=seginv, feats={'-syl'})
        
        # harmony
        rule = Rule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, left_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier)

        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['m']) == 'm')
        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['n']) == 'm')

        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['b']) == 'b')
        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['d']) == 'b')

        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['m']) == 'n')
        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['n']) == 'n')

        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['b']) == 'd')
        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['d']) == 'd')


        # disharmony
        rule = Rule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, left_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier, harmony=False)

        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['m']) == 'b')
        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['n']) == 'b')

        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['b']) == 'm')
        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['d']) == 'm')

        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['m']) == 'd')
        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['n']) == 'd')

        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['b']) == 'n')
        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['d']) == 'n')


    def test_rule__predictions(self):
        seginv = SegInv()
        seginv.add_segs({'a', 'e', 'i', 'o', 'u', 'b', 'd', 'm', 'n', 'l'})
        # make custom seg
        features = dict(seginv['m'].features)
        features['son'] = UNDERSPECIFIED
        features['nas'] = UNDERSPECIFIED
        seginv.add_custom('C1', features=features) # m ~ b
        features = dict(seginv['n'].features)
        features['son'] = UNDERSPECIFIED
        features['nas'] = UNDERSPECIFIED
        seginv.add_custom('C2', features=features) # n ~ d

        tier = Tier(seginv=seginv, feats={'-syl'})
        
        # left-to-right (harmony)

        rule = Rule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, left_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier)

        segstr = SegStr('b u m e t u C2 i l', seginv=seginv)
        assert(rule._predictions(segstr) == [(6, 'd')])

        segstr = SegStr('b u m e C1 i l', seginv=seginv)
        assert(rule._predictions(segstr) == [(4, 'm')])

        segstr = SegStr('b u m e C1 i C2', seginv=seginv)
        assert(rule._predictions(segstr) == [(4, 'm'), (6, 'n')])

        segstr = SegStr('b u m e C1 i C2 u i t C1', seginv=seginv)
        assert(rule._predictions(segstr) == [(4, 'm'), (6, 'n'), (10, 'b')])

        segstr = SegStr('b u m e', seginv=seginv)
        assert(rule._predictions(segstr) == [])

        # right-to-left (harmony)

        rule = Rule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, right_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier)

        segstr = SegStr('l i C2 u t e m u b', seginv=seginv)
        assert(rule._predictions(segstr) == [(2, 'd')])

        segstr = SegStr('l i C1 e m u b', seginv=seginv)
        assert(rule._predictions(segstr) == [(2, 'm')])

        segstr = SegStr('C2 i C1 e m u b', seginv=seginv)
        assert(rule._predictions(segstr) == [(2, 'm'), (0, 'n')])

        segstr = SegStr('C1 t i u C2 i C1 e m u b', seginv=seginv)
        assert(rule._predictions(segstr) == [(6, 'm'), (4, 'n'), (0, 'b')])

        segstr = SegStr('b u m e', seginv=seginv)
        assert(rule._predictions(segstr) == [])

        # left-to-right (disharmony)

        rule = Rule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, left_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier, harmony=False)

        segstr = SegStr('b u m e t u C2 i l', seginv=seginv)
        assert(rule._predictions(segstr) == [(6, 'n')])

        segstr = SegStr('b u m e C1 i l', seginv=seginv)
        assert(rule._predictions(segstr) == [(4, 'b')])

        segstr = SegStr('b u m e C1 i C2', seginv=seginv)
        assert(rule._predictions(segstr) == [(4, 'b'), (6, 'n')])

        segstr = SegStr('b u m e C1 i C2 u i t C1', seginv=seginv)
        assert(rule._predictions(segstr) == [(4, 'b'), (6, 'n'), (10, 'm')])

        segstr = SegStr('b u m e', seginv=seginv)
        assert(rule._predictions(segstr) == [])

        # right-to-left (disharmony)

        rule = Rule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, right_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier, harmony=False)

        segstr = SegStr('l i C2 u t e m u b', seginv=seginv)
        assert(rule._predictions(segstr) == [(2, 'n')])

        segstr = SegStr('l i C1 e m u b', seginv=seginv)
        assert(rule._predictions(segstr) == [(2, 'b')])

        segstr = SegStr('C2 i C1 e m u b', seginv=seginv)
        assert(rule._predictions(segstr) == [(2, 'b'), (0, 'n')])

        segstr = SegStr('C1 t i u C2 i C1 e m u b', seginv=seginv)
        assert(rule._predictions(segstr) == [(6, 'b'), (4, 'n'), (0, 'm')])

        segstr = SegStr('b u m e', seginv=seginv)
        assert(rule._predictions(segstr) == [])

    def test_rule_produce(self):
        seginv = SegInv()
        seginv.add_segs({'a', 'e', 'i', 'o', 'u', 'b', 'd', 'm', 'n', 'l'})
        # make custom seg
        features = dict(seginv['m'].features)
        features['son'] = UNDERSPECIFIED
        features['nas'] = UNDERSPECIFIED
        seginv.add_custom('C1', features=features) # m ~ b
        features = dict(seginv['n'].features)
        features['son'] = UNDERSPECIFIED
        features['nas'] = UNDERSPECIFIED
        seginv.add_custom('C2', features=features) # n ~ d

        tier = Tier(seginv=seginv, feats={'-syl'})
        
        # left-to-right (harmony)
        rule = Rule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, left_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier)
        assert(rule('b u m e t u C2 i l') == 'b u m e t u d i l')
        assert(rule('b u m e C1 i l') == 'b u m e m i l')
        assert(rule('b u m e C1 i C2') == 'b u m e m i n')
        assert(rule('b u m e C1 i C2 u i t C1') == 'b u m e m i n u i t b')
        assert(rule('b u m e') == 'b u m e')

        # right-to-left (harmony)
        rule = Rule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, right_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier)
        assert(rule('l i C2 u t e m u b') == 'l i d u t e m u b')
        assert(rule('l i C1 e m u b') == 'l i m e m u b')
        assert(rule('C2 i C1 e m u b') == 'n i m e m u b')
        assert(rule('C1 t i u C2 i C1 e m u b') == 'b t i u n i m e m u b')
        assert(rule('b u m e') == 'b u m e')

        # left-to-right (disharmony)
        rule = Rule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, left_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier, harmony=False)
        assert(rule('b u m e t u C2 i l') == 'b u m e t u n i l')
        assert(rule('b u m e C1 i l') == 'b u m e b i l')
        assert(rule('b u m e C1 i C2') == 'b u m e b i n')
        assert(rule('b u m e C1 i C2 u i t C1') == 'b u m e b i n u i t m')
        assert(rule('b u m e') == 'b u m e')

        # right-to-left (disharmony)
        rule = Rule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, right_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier, harmony=False)
        assert(rule('l i C2 u t e m u b') == 'l i n u t e m u b')
        assert(rule('l i C1 e m u b') == 'l i b e m u b')
        assert(rule('C2 i C1 e m u b') == 'n i b e m u b')
        assert(rule('C1 t i u C2 i C1 e m u b') == 'm t i u n i b e m u b')
        assert(rule('b u m e') == 'b u m e')

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
        assert(len(d2l._discrepancy.instances) == 8)

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
        assert(len(d2l._discrepancy.instances) == 8)

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