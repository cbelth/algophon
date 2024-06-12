import unittest
import sys
sys.path.append('../')
from algophon.seginv import SegInv
from algophon.symbols import UNDERSPECIFIED, LWB

class TestSegInv(unittest.TestCase):
    def test_init(self):
        seginv = SegInv()
        assert(seginv is not None)

    def test_init_boundary(self):
        seginv = SegInv(add_boundary_symbols=True)
        assert(len(seginv) == 4)
        assert(seginv.feature_space[-5:] == ['B', 'LWB', 'RWB', 'SYLB', 'MORPHB'])
        assert(seginv[LWB].features['B'] == '+')
        assert(seginv[LWB].features['syl'] == UNDERSPECIFIED)
        assert(seginv[LWB].features['LWB'] == '+')
        assert(seginv[LWB].features['RWB'] == '-')

        seginv.add('i')
        assert(seginv['i'].features['B'] == '-')
        assert(seginv['i'].features['syl'] == '+')
        assert(seginv['i'].features['LWB'] == '-')
        assert(seginv['i'].features['RWB'] == '-')

    def test_init_missing(self):
        seginv = SegInv()
        # test voiceless velar nasal
        voi_idx = seginv.feature_space.index('voi')
        assert(seginv._seg_to_feat_vec['ŋ'][voi_idx] == '+')
        assert(seginv._seg_to_feat_vec['ŋ̊'][voi_idx] == '-')
        assert(seginv._seg_to_feat_vec['ŋ̊'][idx] == seginv._seg_to_feat_vec['ŋ'][idx] 
               for idx in range(len(seginv.feature_space)) if idx != voi_idx)
        assert(seginv.add_and_get('ŋ̊'))
        # test voicelesss palatal fricative
        assert(seginv._seg_to_feat_vec['ʝ'][voi_idx] == '+')
        assert(seginv._seg_to_feat_vec['ç'][voi_idx] == '-')
        assert(seginv._seg_to_feat_vec['ç'][idx] == seginv._seg_to_feat_vec['ʝ'][idx] 
               for idx in range(len(seginv.feature_space)) if idx != voi_idx)
        assert(seginv.add_and_get('ç'))

    def test_add(self):
        seginv = SegInv()
        
        seginv.add('i')
        assert(len(seginv) == 1)
        assert(seginv.segs == {'i'}) 

        seginv.add_segs({'p', 'b', 't', 'd'})
        assert(len(seginv) == 5)
        assert(seginv.segs == {'i', 'p', 'b', 't', 'd'}) 

        seginv.add_segs_by_str('eː n t j ə')
        assert(len(seginv) == 9)
        assert(seginv.segs == {'i', 'p', 'b', 't', 'd', 'eː', 'n', 'j', 'ə'}) 

    def test_add_custom(self):
        seginv = SegInv()

        seginv.add('s')
        seginv.add('ʃ')

        shared_feats = set(feat[1:] for feat in seginv.feature_intersection({'s', 'ʃ'}, exclude_underspecified=False))
        feat_diff = set(seginv.feature_space).difference(shared_feats)
        features = dict((feat, val if feat not in feat_diff else UNDERSPECIFIED) for feat, val in seginv['s'].features.items())

        seginv.add_custom(symbol='S', features=features)
        assert('S' in seginv)
        assert(seginv['S'].features == features)

        try:
            seginv.add_custom(symbol='V', features={'voi': '+'})
            assert(False)
        except ValueError as e:
            assert(True)
            assert(e.__str__() == 'The features do not match those in the feature space.')

        try:
            seginv.add_custom(symbol='s', features=features)
            assert(False)
        except ValueError as e:
            assert(True)
            assert(e.__str__() == 'The symbol "s" is already a symbol in the IPA data from Panphon (https://github.com/dmort27/panphon).')

    def test_get(self):
        seginv = SegInv()
        seginv.add('eː')
        assert(seginv['eː'].features == {'syl': '+', 'son': '+', 'cons': '-', 'cont': '+', 'delrel': '-', 'lat': '-', 'nas': '-', 
                                         'strid': '0', 'voi': '+', 'sg': '-', 'cg': '-', 'ant': '0', 'cor': '-', 'distr': '0', 'lab': '-',
                                         'hi': '-', 'lo': '-', 'back': '-', 'round': '-', 'velaric': '-', 'tense': '+', 'long': '+', 
                                         'hitone': '0', 'hireg': '0'})
        
    def test_extension(self):
        seginv = SegInv()
        seginv.add_segs({'a', 'e', 'i', 'o', 'u', 'p', 'b', 't', 'd', 'k', 'g', 's', 'm', 'n'})
        assert(seginv.extension({'+syl'}) == {'a', 'e', 'i', 'o', 'u'})
        assert(seginv.extension({'+cons'}) == {'p', 'b', 't', 'd', 'k', 'g', 's', 'm', 'n'})
        assert(seginv.extension({'-syl', '+voi'}) == {'b', 'd', 'g', 'm', 'n'})

    def test_extension_complement(self):
        seginv = SegInv()
        seginv.add_segs({'a', 'e', 'i', 'o', 'u', 'p', 'b', 't', 'd', 'k', 'g', 's', 'm', 'n'})
        assert(seginv.extension_complement({'+syl'}) == {'p', 'b', 't', 'd', 'k', 'g', 's', 'm', 'n'})
        assert(seginv.extension_complement({'+cons'}) == {'a', 'e', 'i', 'o', 'u'})
        assert(seginv.extension_complement({'-syl', '+voi'}) == {'a', 'e', 'i', 'o', 'u', 'p', 't', 'k', 's'})

    def test_feature_intersection(self):
        seginv = SegInv()
        vs = {'a', 'e', 'i', 'o', 'u'}
        seginv.add_segs(vs)
        assert(seginv.feature_intersection(vs) == {'+cont', '-sg', '-delrel', '+tense', '-long', '-cons', '-velaric',
                                                   '-nas', '+syl', '-cg', '+voi', '-lat', '+son', '-cor'})
        
    def test_feature_diff(self):
        seginv = SegInv()
        seginv.add_segs({'t', 'd'})
        assert(seginv.feature_diff('t', 'd') == {'voi'})

        seginv.add_segs({'i', 'e'})
        assert(seginv.feature_diff('i', 'e') == {'hi'})

if __name__ == "__main__":
    unittest.main()