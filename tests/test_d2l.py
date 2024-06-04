import unittest
import sys

sys.path.append('../')
from algophon import SegInv, SegStr, NatClass
from algophon.models.D2L import Tier, D2LRule, D2L
from algophon.symbols import LWB, RWB, MORPHB, SYLB, UNDERSPECIFIED

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
        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, left_ctxts=NatClass(feats={'+strid'}, seginv=seginv))
        assert(rule and rule.left_ctxts is not None and rule.right_ctxts is None)
        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, left_ctxts={'S', 's', 'ʃ'})
        assert(rule and rule.left_ctxts is not None and rule.right_ctxts is None)

        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, right_ctxts=NatClass(feats={'+strid'}, seginv=seginv))
        assert(rule and rule.left_ctxts is None and rule.right_ctxts is not None)
        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, right_ctxts={'S', 's', 'ʃ'})
        assert(rule and rule.left_ctxts is None and rule.right_ctxts is not None)

        try:
            D2LRule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, left_ctxts=NatClass(feats={'+strid'}, seginv=seginv), right_ctxts={'S', 's', 'ʃ'})
            assert(False)
        except ValueError as e:
            assert(e.__str__() == 'D2L Rule cannot have both left and right contexts.')
            assert(True)

        try:
            D2LRule(seginv=seginv, features={'ant', 'distr'}, target={'S'})
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
        rule = D2LRule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, left_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier)

        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['m']) == 'm')
        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['n']) == 'm')

        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['b']) == 'b')
        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['d']) == 'b')

        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['m']) == 'n')
        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['n']) == 'n')

        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['b']) == 'd')
        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['d']) == 'd')


        # disharmony
        rule = D2LRule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, left_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier, harmony=False)

        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['m']) == 'b')
        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['n']) == 'b')

        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['b']) == 'm')
        assert(rule._apply(seg=seginv['C1'], ctxt=seginv['d']) == 'm')

        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['m']) == 'd')
        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['n']) == 'd')

        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['b']) == 'n')
        assert(rule._apply(seg=seginv['C2'], ctxt=seginv['d']) == 'n')

    def test_rule__apply_default(self):
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
        
        # harmony
        rule = D2LRule(seginv=seginv, features={'son', 'nas'}, defaults={'son': '-', 'nas': '-'}, target={'C1', 'C2'}, left_ctxts=NatClass({'-syl'}, seginv=seginv))

        assert(rule._apply_default(seg=seginv['C1']) == 'b')
        assert(rule._apply_default(seg=seginv['C2']) == 'd')

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

        rule = D2LRule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, left_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier)

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

        rule = D2LRule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, right_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier)

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

        rule = D2LRule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, left_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier, harmony=False)

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

        rule = D2LRule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, right_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier, harmony=False)

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

        # test default application
        pairs = [
            ('ʃ o k u S i S', 'ʃ o k u ʃ i ʃ'), 
            ('a p ʃ a S', 'a p ʃ a ʃ'),
            ('ʃ u n i S', 'ʃ u n i ʃ'),
            ('s o k i S', 's o k i s'),
            ('s i g o S i S', 's i g o s i s'),
            ('u t S', 'u t s')
        ]
        d2l = D2L()
        pairs = d2l._train_setup(pairs)
        seginv = d2l.seginv
        # overwrite weird Panphon values
        seginv['s']['strid'] = '+'
        seginv['ʃ']['strid'] = '+'
        seginv['S']['strid'] = '+'

        strid = NatClass(feats={'+strid'}, seginv=seginv)
        tier = Tier(seginv=seginv, feats=strid)
        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, defaults={'ant': '+', 'distr': '-'}, left_ctxts=strid, tier=tier)
        assert(rule._predictions(SegStr('ʃ o k u S i S', seginv=seginv)) == [(4, 'ʃ'), (6, 'ʃ')])
        assert(rule._predictions(SegStr('u t S', seginv=seginv)) == [(2, 's')])

        cons = NatClass(feats={'+cons'}, seginv=seginv)
        tier = Tier(seginv=seginv, feats=cons)
        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, left_ctxts=cons, tier=tier)
        assert(rule._predictions(SegStr('ʃ o k u S i S', seginv=seginv)) == [(4, 'S'), (6, 'S')])
        assert(rule._predictions(SegStr('u t S', seginv=seginv)) == [(2, 's')])

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
        rule = D2LRule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, left_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier)
        assert(rule('b u m e t u C2 i l') == 'b u m e t u d i l')
        assert(rule('b u m e C1 i l') == 'b u m e m i l')
        assert(rule('b u m e C1 i C2') == 'b u m e m i n')
        assert(rule('b u m e C1 i C2 u i t C1') == 'b u m e m i n u i t b')
        assert(rule('b u m e') == 'b u m e')

        # right-to-left (harmony)
        rule = D2LRule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, right_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier)
        assert(rule('l i C2 u t e m u b') == 'l i d u t e m u b')
        assert(rule('l i C1 e m u b') == 'l i m e m u b')
        assert(rule('C2 i C1 e m u b') == 'n i m e m u b')
        assert(rule('C1 t i u C2 i C1 e m u b') == 'b t i u n i m e m u b')
        assert(rule('b u m e') == 'b u m e')

        # left-to-right (disharmony)
        rule = D2LRule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, left_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier, harmony=False)
        assert(rule('b u m e t u C2 i l') == 'b u m e t u n i l')
        assert(rule('b u m e C1 i l') == 'b u m e b i l')
        assert(rule('b u m e C1 i C2') == 'b u m e b i n')
        assert(rule('b u m e C1 i C2 u i t C1') == 'b u m e b i n u i t m')
        assert(rule('b u m e') == 'b u m e')

        # right-to-left (disharmony)
        rule = D2LRule(seginv=seginv, features={'son', 'nas'}, target={'C1', 'C2'}, right_ctxts=NatClass({'-syl'}, seginv=seginv), tier=tier, harmony=False)
        assert(rule('l i C2 u t e m u b') == 'l i n u t e m u b')
        assert(rule('l i C1 e m u b') == 'l i b e m u b')
        assert(rule('C2 i C1 e m u b') == 'n i b e m u b')
        assert(rule('C1 t i u C2 i C1 e m u b') == 'm t i u n i b e m u b')
        assert(rule('b u m e') == 'b u m e')

    def test_rule_tsp_stats(self):
        pairs = [
            ('ʃ o k u S i S', 'ʃ o k u ʃ i ʃ'), 
            ('a p ʃ a S', 'a p ʃ a ʃ'),
            ('ʃ u n i S', 'ʃ u n i ʃ'),
            ('s o k i S', 's o k i s'),
            ('s i g o S i S', 's i g o s i s'),
            ('u t S', 'u t s')
        ]
        d2l = D2L()
        pairs = d2l._train_setup(pairs)
        seginv = d2l.seginv
        # overwrite weird Panphon values
        seginv['s']['strid'] = '+'
        seginv['ʃ']['strid'] = '+'
        seginv['S']['strid'] = '+'

        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, left_ctxts=seginv.segs)
        assert(rule.tsp_stats(pairs) == (8, 1))

        cons = NatClass(feats={'+cons'}, seginv=seginv)
        tier = Tier(seginv=seginv, feats=cons)
        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, left_ctxts=cons, tier=tier)
        assert(rule.tsp_stats(pairs) == (8, 2)) # this is diff from paper b.c. the feature specificaions involve distr, which is 0 for /k/

        strid = NatClass(feats={'+strid'}, seginv=seginv)
        tier = Tier(seginv=seginv, feats=strid)
        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, defaults={'ant': '+', 'distr': '-'}, left_ctxts=strid, tier=tier)
        assert(rule.tsp_stats(pairs) == (8, 8))

    def test_rule_underextension_SRs(self):
        pairs = [
            ('ʃ o k u S i S', 'ʃ o k u ʃ i ʃ'), 
            ('a p a S', 'a p a s'),
            ('u n i S', 'u n i s'),
            ('s o k i S', 's o k i s'),
            ('i g o i S', 'i g o i ʃ'),
            ('u t S', 'u t s')
        ]
        d2l = D2L()
        pairs = d2l._train_setup(pairs)
        seginv = d2l.seginv
        # overwrite weird Panphon values
        seginv['s']['strid'] = '+'
        seginv['ʃ']['strid'] = '+'
        seginv['S']['strid'] = '+'

        strid = NatClass(feats={'+strid'}, seginv=seginv)
        tier = Tier(seginv=seginv, feats=strid)
        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, left_ctxts=strid, tier=tier)
        assert(rule.underextension_SRs(pairs) == {'s': 3, 'ʃ': 1})

    def test_rule_set_defaults(self):
        seginv = SegInv()
        seginv.add_segs({'s', 'ʃ'})
        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant', 'distr'}, left_ctxts={'s', 'ʃ'})
        assert(rule.defaults is None)
        rule.set_defaults(defaults={'ant': seginv['s']['ant'], 'distr': seginv['s']['distr']})
        assert(len(rule.defaults) == 2)
        assert(rule.defaults['ant'] == seginv['s']['ant'])
        assert(rule.defaults['distr'] == seginv['s']['distr'])
        
        try:
            rule.set_defaults(defaults={'ant': '+'})
            assert(False)
        except ValueError as e:
            assert(True)
            assert(e.__str__() == ':defaults: must include one value per :self.features:')

    def test_rule_errant_ctxts(self):
        pairs = [
            ('ʃ o k u S i S', 'ʃ o k u ʃ i ʃ'), 
            ('a p ʃ a S', 'a p ʃ a ʃ'),
            ('ʃ u n i S', 'ʃ u n i ʃ'),
            ('s o k i S', 's o k i s'),
            ('s i g o S i S', 's i g o s i s'),
            ('u t S', 'u t s')
        ]
        d2l = D2L()
        pairs = d2l._train_setup(pairs)
        seginv = d2l.seginv
        # overwrite weird Panphon values
        seginv['s']['strid'] = '+'
        seginv['ʃ']['strid'] = '+'
        seginv['S']['strid'] = '+'
        seginv['s']['distr'] = '+'
        seginv['ʃ']['distr'] = '+'
        seginv['S']['distr'] = '+'

        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant'}, left_ctxts=seginv.segs)
        assert(rule.errant_ctxts(pairs) == {'u', 'i', 'a', 'o'})

        cons = NatClass(feats={'+cons'}, seginv=seginv)
        tier = Tier(seginv=seginv, feats=cons)
        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant'}, left_ctxts=cons, tier=tier)
        assert(rule.errant_ctxts(pairs) == {'n', 'k', 'g', 'ʃ'})

        strid = NatClass(feats={'+strid'}, seginv=seginv)
        tier = Tier(seginv=seginv, feats=strid)
        rule = D2LRule(seginv=seginv, target={'S'}, features={'ant'}, defaults={'ant': '+'}, left_ctxts=strid, tier=tier)
        assert(rule.errant_ctxts(pairs) == set())

    def test_rule_set_ctxts(self):
        seginv = SegInv()
        seginv.add_segs({'a', 'e', 'i', 'o', 'u', 't', 'p'})
        vowels = NatClass(feats={'+syl'}, seginv=seginv)
        rule = D2LRule(seginv=seginv, target={'e', 'i'}, features={'back'}, left_ctxts={'a', 'e', 'i', 'o', 'u', 't', 'p'})
        assert(rule.left_ctxts == {'a', 'e', 'i', 'o', 'u', 't', 'p'})
        rule.set_ctxts(ctxts=vowels)
        assert(rule.left_ctxts == vowels)

    def test_D2L_init(self):
        d2l = D2L()
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
        d2l = D2L()
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
        d2l = D2L()
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
        d2l = D2L()
        pairs = d2l._train_setup(pairs)
        assert(d2l._get_tier_adj_contexts(discrepancy=d2l._discrepancy, 
                                          tier=None) == ({'u', 'i', 'a', 'o', 't'}, 
                                                         {'i'}))
        assert(d2l._get_tier_adj_contexts(discrepancy=d2l._discrepancy, 
                                          tier=Tier(seginv=d2l.seginv, feats={'+cons'})) == ({'k', 'S', 'ʃ', 'n', 'g', 't'}, 
                                                                                             {'S'}))
        # overwrite weird Panphon values
        d2l.seginv['s']['strid'] = '+'
        d2l.seginv['ʃ']['strid'] = '+'
        d2l.seginv['S']['strid'] = '+'
        assert(d2l._get_tier_adj_contexts(discrepancy=d2l._discrepancy, 
                                          tier=Tier(seginv=d2l.seginv, feats={'+strid'})) == ({'s', 'ʃ', 'S'}, 
                                                                                              {'S'}))
        
    def test_D2L_paper_example(self):
        pairs = [
            ('ʃ o k u S i S', 'ʃ o k u ʃ i ʃ'), 
            ('a p ʃ a S', 'a p ʃ a ʃ'),
            ('ʃ u n i S', 'ʃ u n i ʃ'),
            ('s o k i S', 's o k i s'),
            ('s i g o S i S', 's i g o s i s'),
            ('u t S', 'u t s')
        ]
        d2l = D2L()
        # override Panphon's strid feat
        d2l.seginv.add_segs({'s', 'ʃ', 'k', 'p', 'n', 'g', 't', 'o', 'u', 'i', 'a'})
        for seg in d2l.seginv.segs:
            if seg in {'s', 'ʃ'}:
                d2l.seginv[seg]['strid'] = '+'
            elif seg not in {LWB, RWB, MORPHB, SYLB}:
                d2l.seginv[seg]['strid'] = '-'

        # train D2L
        d2l.train(pairs)

        assert(d2l.rule is not None)
        assert(d2l.rule.tier is not None)
        assert(d2l.rule.tier.as_delset is False)
        assert(d2l.rule._apply_default(d2l.seginv['S']) == 's')
        assert(d2l.rule.accuracy(pairs) == 1.0)
        assert(d2l.accuracy(pairs) == 1.0)

    def test_D2L_readme_example(self):
        pairs = [
            ('m o k u D', 'm o k u n'), 
            ('a p a D', 'a p a d'),
            ('t u n i D', 't u n i n'),
            ('s o k i D', 's o k i d'),
            ('n i g o D', 'n i g o n'),
            ('u t e D', 'u t e d'),
            ('u m i D', 'u m i n'),
            ('e t e D', 'e t e d'),
            ('u n i b e D', 'u n i b e n'),
            ('k a d u D', 'k a d u d'),
            ('m i t u D', 'm i t u n'),
            ('u n i t a D', 'u n i t a n')
        ]
        d2l = D2L()
        d2l.train(pairs)

        assert(d2l.rule is not None)
        assert(d2l.rule.left_ctxts == {'n', 'm'})
        assert(f'{d2l.rule.tier}' == '¬[-nas]')
        assert(d2l.rule.defaults is not None)
        assert(d2l.rule.accuracy(pairs) == 1.0)
        assert(d2l.accuracy(pairs) == 1.0)

    def test_D2L_readme_adj_example(self):
        pairs = [
            ('m o k u D', 'm o k u d'), 
            ('a p a D', 'a p a d'),
            ('t u n i D', 't u n i t'),
            ('s o k i D', 's o k i t'),
            ('a k D', 'a k t'),
            ('u m i D', 'u m i d'),
        ]
        d2l = D2L()
        d2l.train(pairs)

        assert(d2l.rule.tsp_stats(pairs) == (6, 4))
        assert(d2l.rule.left_ctxts == {'u', 'a', 'i', 'k'})
        assert(d2l.rule.tier is None)
        assert(d2l.rule.defaults is None)

    def test_D2L_turkish_toy(self):
        pairs = [
            ('d ɑ l l A r', 'd ɑ l l ɑ r'),
            ('j e r l A r', 'j e r l e r'),
            ('i p l A r', 'i p l e r'),
            ('j ɑ z A b i l', 'j ɑ z ɑ b i l'),
            ('j y z A b i l', 'j y z e b i l'),
            ('b y r o d A', 'b y r o d ɑ'),
            ('e v d A', 'e v d e'),
            ('ø n d͡ʒ e l A r', 'ø n d͡ʒ e l e r'),
            ('j ɑ r ɯ n l A r', 'j ɑ r ɯ n l ɑ r'),
            ('k u ʃ l A r', 'k u ʃ l ɑ r'),
            ('k i ʃ l A r', 'k i ʃ l e r'),
            ('ɑ r ɑ b ɑ l A r', 'ɑ r ɑ b ɑ l ɑ r'),
            ('k e d i l A r', 'k e d i l e r'),
            ('n e r e d A', 'n e r e d e'),
            ('b u r ɑ d A', 'b u r ɑ d ɑ'),
            ('d e n i z d A', 'd e n i z d e'),
            ('t͡ʃ o d͡ʒ u k l A r', 't͡ʃ o d͡ʒ u k l ɑ r'),
            ('ɑ b i l A r', 'ɑ b i l e r'),
            ('k u z u l A r', 'k u z u l ɑ r'),
            ('n e l A r', 'n e l e r'),
            ('k ø p e k l A r', 'k ø p e k l e r'),
            ('k ø p i k l A r', 'k ø p i k l e r'),
            ('i k l A r', 'i k l e r'),
            ('e k l A r', 'e k l e r'),
            ('i k t A', 'i k t e'),
            ('e k t A', 'e k t e'),
            ('y k t A', 'y k t e'),
            ('b i r ʃ e j l A r', 'b i r ʃ e j l e r'),
            ('s ɑ n A', 's ɑ n ɑ'),
            ('j ɑ p m A', 'j ɑ p m ɑ'),
            ('s e n d A', 's e n d e'),
            ('b ɑ l ɯ k l A r', 'b ɑ l ɯ k l ɑ r'),
            ('k e k A', 'k e k e'),

        ]

        d2l = D2L()

        # setup vowel inventory
        vowels = {
            'e': ['-back', '-round', '-hi'],
            'ø': ['-back', '+round', '-hi'],
            'ɑ': ['+back', '-round', '-hi'],
            'o': ['+back', '+round', '-hi'],

            # high vowels
            'i': ['-back', '-round', '+hi'],
            'y': ['-back', '+round', '+hi'],
            'ɯ': ['+back', '-round', '+hi'],
            'u': ['+back', '+round', '+hi']

        }
        d2l.seginv.add_segs(set(vowels.keys()))

        for feat in ['delrel', 'lat', 'nas', 'strid', 'sg', 'cg', 'ant', 'cor', 'distr', 'lab', 'hi', 'lo', 'back', 'round', 'velaric', 'tense', 'long', 'hitone', 'hireg']:
            for vowel in vowels.keys():
                d2l.seginv[vowel][feat] = UNDERSPECIFIED
        for vowel, feats in vowels.items():
            for feat in feats:
                d2l.seginv[vowel][feat[1:]] = feat[0]
        
        assert(d2l.seginv.feature_diff('ɑ', 'e') == {'back'})
        assert(d2l.seginv.feature_diff('ɑ', 'y') == {'back', 'round', 'hi'})
        assert(d2l.seginv.feature_diff('ɑ', 'i') == {'back', 'hi'})
        
        # train D2L
        d2l.train(pairs)

        assert(d2l.rule is not None)
        assert(d2l.rule.tier is not None)
        assert(d2l.rule.tier.as_delset is False)
        assert(d2l.rule.accuracy(pairs) == 1.0)
        assert(d2l.accuracy(pairs) == 1.0)

    def test_D2L_finley(self):
        d2l = D2L()

        pairs = d2l.load_train(path='data/finley/exp-1-train.txt')
        d2l.train(pairs=pairs)
        assert(d2l.rule.harmony) # agree
        assert(d2l.rule.tier._str == '[-syl]')
        assert(d2l.rule.left_ctxts._name == '[-syl]')
        assert(d2l.accuracy(pairs) == 1.0)

        pairs = d2l.load_train(path='data/finley/exp-2-train.txt')
        d2l._train_setup(pairs=pairs)
        # overwrite weird Panphon values
        for seg in d2l.seginv.segs:
            if seg in {'s', 'ʃ', 'S'}:
                d2l.seginv[seg]['strid'] = '+'
                d2l.seginv[seg]['distr'] = '+'
            else:
                d2l.seginv[seg]['strid'] = '-'
        d2l.train(pairs=pairs)
        assert(d2l.rule.harmony) # agree
        assert(d2l.accuracy(pairs) == 1.0)
        assert(d2l.rule.tier._str == '[+strid]')
        assert(d2l.rule.left_ctxts._name == '[+strid]')

    def test_D2L_mcmullin_hansson(self):
        d2l = D2L()
        d2l.train_on_file(path='data/mcmullin_hansson/exp-1a-train.txt')
        assert(d2l.rule.harmony) # agree
        assert(d2l.rule.tier._str == '[-syl]')
        assert(d2l.rule.right_ctxts._name == '[-syl]')

        d2l.train_on_file(path='data/mcmullin_hansson/exp-1b-train.txt')
        assert(d2l.rule.harmony) # agree
        assert(d2l.rule.tier._str == '¬[-lat]')
        assert(d2l.rule._apply_default(d2l.seginv['L']) == 'ɹ')
        assert(d2l.rule.right_ctxts == {'l'})

        d2l.train_on_file(path='data/mcmullin_hansson/exp-2a-train.txt')
        assert(not d2l.rule.harmony) # disagree
        assert(d2l.rule.tier._str == '[-syl]')
        assert(d2l.rule.right_ctxts._name == '[-syl]')

        d2l.train_on_file(path='data/mcmullin_hansson/exp-2b-train.txt')
        assert(not d2l.rule.harmony) # disagree
        assert(d2l.rule.tier._str == '¬[-lat]')
        assert(d2l.rule._apply_default(d2l.seginv['L']) == 'l')
        assert(d2l.rule.right_ctxts == {'l'})

if __name__ == "__main__":
    unittest.main()