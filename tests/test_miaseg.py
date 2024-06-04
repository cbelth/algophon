import unittest
import sys

sys.path.append('../')
from algophon import SegInv, SegStr
from algophon.models.Miaseg import Paradigm, Miaseg

PAPER_EXAMPLE = [
    ('TEACHER', 'tanár', ()),
    ('TEACHER', 'tanárok', ('PL',)),
    ('TEACHER', 'tanároknak', ('PL', 'DAT')),
    ('PERSON', 'személy', ()),
    ('PERSON', 'személynek', ('DAT',)),
]

IPA_PAPER_EXAMPLE = [
    ('TEACHER', 't ɒ n aː r', ()),
    ('TEACHER', 't ɒ n aː r o k', ('PL',)),
    ('TEACHER', 't ɒ n aː r o k n ɒ k', ('PL', 'DAT')),
    ('PERSON', 's ɛ m eː j', ()),
    ('PERSON', 's ɛ m eː j n ɛ k', ('DAT',)),
]

TOY_EXAMPLE = [
    ('r1', 'root1', ()),
    ('r1', 'root1-a', ('a',)),
    ('r1', 'root1-b', ('b',)),
    ('r1', 'root1-a-b', ('a', 'b')),
    ('r1', 'c-root1-a-b', ('a', 'b', 'c')),
    
    ('r2', 'root2', ()),
    ('r2', 'root2-A', ('a',)),
    ('r2', 'root2-B', ('b',)),
    ('r2', 'root2-A-B', ('a', 'b')),
    ('r2', 'C-root2-A-B', ('a', 'b', 'c')),
    
    ('r3', 'root3', ()),
    ('r3', 'root3-a', ('a',)),
    ('r3', 'root3-b', ('b',)),
    ('r3', 'root3-b-a', ('a', 'b')), # switches order
    ('r3', 'c-root3-b-a', ('a', 'b', 'c')),
]

class TestMiaseg(unittest.TestCase):
    def test_paradigm_init(self):
        par = Paradigm('CAT')
        assert(par is not None)
        assert(par.root == 'CAT')
        assert(len(par.words) == 0)

    def test_paradigm_add_word(self):
        par = Paradigm('CAT')
        assert(len(par) == 0)
        par.add_word(word='cat', features=())
        assert(len(par) == 1)
        par.add_word(word='cats', features=('pl',))
        assert(len(par) == 2)
        par.add_word(word='cat', features=()) # adding again changes nothing
        assert(len(par) == 2)

    def test_miaseg_init(self):
        model = Miaseg()
        assert(model is not None)
        assert(not model.use_ipa)

        model = Miaseg(use_ipa=True)
        assert(model is not None)
        assert(model.use_ipa)
        assert(model.seginv is not None)

    def test_miaseg__setup_paradigms(self):
        model = Miaseg()
        model._setup_paradigms(train=PAPER_EXAMPLE)
        assert(len(model._paradigms) == 2)
        assert('TEACHER' in model._paradigms and 'PERSON' in model._paradigms)
        assert(len(model._paradigms['TEACHER']) == 3)
        assert(len(model._paradigms['PERSON']) == 2)

        model = Miaseg(use_ipa=True)
        seginv = SegInv()
        model._setup_paradigms(train=list((r, SegStr(w, seginv=seginv), f) for r, w, f in IPA_PAPER_EXAMPLE))
        assert(len(model._paradigms) == 2)
        assert('TEACHER' in model._paradigms and 'PERSON' in model._paradigms)
        assert(len(model._paradigms['TEACHER']) == 3)
        assert(len(model._paradigms['PERSON']) == 2)

    def test_paradigm_get_one_diff_pairs(self):
        model = Miaseg()
        model._setup_paradigms(train=PAPER_EXAMPLE)
        assert(model._paradigms['TEACHER'].get_one_diff_pairs() == [{'src': 'tanár', 
                                                                    'tgt': 'tanárok',
                                                                    'feat': 'PL',
                                                                    'shared_feats': set()},
                                                                    {'src': 'tanárok',
                                                                     'tgt': 'tanároknak',
                                                                     'feat': 'DAT',
                                                                     'shared_feats': {'PL'}}])
        assert(model._paradigms['PERSON'].get_one_diff_pairs() == [{'src': 'személy', 
                                                                    'tgt': 'személynek',
                                                                    'feat': 'DAT',
                                                                    'shared_feats': set()}])
        
        model = Miaseg()
        model._setup_paradigms(train=TOY_EXAMPLE)
        assert(len(model._paradigms['r1'].get_one_diff_pairs()) == 5)
        assert(len(model._paradigms['r2'].get_one_diff_pairs()) == 5)
        assert(len(model._paradigms['r3'].get_one_diff_pairs()) == 5)
        
        model = Miaseg(use_ipa=True)
        seginv = SegInv()
        train = list((r, SegStr(w, seginv=seginv), f) for r, w, f in IPA_PAPER_EXAMPLE)
        model._setup_paradigms(train=train)
        assert(model._paradigms['TEACHER'].get_one_diff_pairs() == [{'src': 't ɒ n aː r', 
                                                                    'tgt': 't ɒ n aː r o k',
                                                                    'feat': 'PL',
                                                                    'shared_feats': set()},
                                                                    {'src': 't ɒ n aː r o k',
                                                                     'tgt': 't ɒ n aː r o k n ɒ k',
                                                                     'feat': 'DAT',
                                                                    'shared_feats': {'PL'}}])
        assert(model._paradigms['PERSON'].get_one_diff_pairs() == [{'src': 's ɛ m eː j', 
                                                                    'tgt': 's ɛ m eː j n ɛ k',
                                                                    'feat': 'DAT',
                                                                    'shared_feats': set()}])

    def test_miaseg__get_marking_from_one_off(self):
        model = Miaseg()
        assert(model._get_marking_from_one_off(src='tanár', tgt='tanárok') == ('ok', 'SUFFIX'))
        assert(model._get_marking_from_one_off(src='tanárok', tgt='tanár') == (None, None))
        assert(model._get_marking_from_one_off(src='tanárok', tgt='tanároknak') == ('nak', 'SUFFIX'))
        assert(model._get_marking_from_one_off(src='személy', tgt='személynek') == ('nek', 'SUFFIX'))

        assert(model._get_marking_from_one_off(src='root', tgt='root') == ('', 'SUFFIX'))
        assert(model._get_marking_from_one_off(src='root1-a-b', tgt='root1-a-b-c') == ('-c', 'SUFFIX'))
        assert(model._get_marking_from_one_off(src='root1', tgt='root1-a') == ('-a', 'SUFFIX'))
        assert(model._get_marking_from_one_off(src='root1-a-b', tgt='root1-a-b-c') == ('-c', 'SUFFIX'))
        assert(model._get_marking_from_one_off(src='root1-a-b', tgt='c-root1-a-b') == ('c-', 'PREFIX'))

        model = Miaseg(use_ipa=True)
        seginv = SegInv()
        tanar = SegStr('t ɒ n aː r', seginv=seginv)
        tanarok = SegStr('t ɒ n aː r o k', seginv=seginv)
        tanaroknak = SegStr('t ɒ n aː r o k n ɒ k', seginv=seginv)
        szemely = SegStr('s ɛ m eː j', seginv=seginv)
        szemelynek = SegStr('s ɛ m eː j n ɛ k', seginv=seginv)
        assert(model._get_marking_from_one_off(src=tanar, tgt=tanarok) == ('o k', 'SUFFIX'))
        assert(model._get_marking_from_one_off(src=tanarok, tgt=tanar) == (None, None))
        assert(model._get_marking_from_one_off(src=tanarok, tgt=tanaroknak) == ('n ɒ k', 'SUFFIX'))
        assert(model._get_marking_from_one_off(src=szemely, tgt=szemelynek) == ('n ɛ k', 'SUFFIX'))
    
    def test_miaseg__find_allomorphs(self):
        model = Miaseg()
        train = PAPER_EXAMPLE
        model._setup_paradigms(train=train)
        model._find_allomorphs(train=train)
        assert(set(model.allomorphs.keys()) == set(model.types.keys()) == {'PL', 'DAT'})
        assert(model.allomorphs['PL'] == {'ok': 1})
        assert(model.allomorphs['DAT'] == {'nak': 1, 'nek': 1})
        assert(model.types['PL'] == 'SUFFIX')
        assert(model.types['DAT'] == 'SUFFIX')
        assert(model.order == ['PL', 'DAT'])

        # ipa version
        model = Miaseg(use_ipa=True)
        seginv = SegInv()
        train = list((r, SegStr(w, seginv=seginv), f) for r, w, f in IPA_PAPER_EXAMPLE)
        model._setup_paradigms(train=train)
        model._find_allomorphs(train=train)
        assert(set(model.allomorphs.keys()) == set(model.types.keys()) == {'PL', 'DAT'})
        assert(model.allomorphs['PL'] == {'o k': 1})
        assert(model.allomorphs['DAT'] == {'n ɒ k': 1, 'n ɛ k': 1})
        assert(model.types['PL'] == 'SUFFIX')
        assert(model.types['DAT'] == 'SUFFIX')
        assert(model.order == ['PL', 'DAT'])

        # toy example
        train = TOY_EXAMPLE
        model = Miaseg()
        model._setup_paradigms(train=train)
        model._find_allomorphs(train=train)

        assert(set(model.allomorphs.keys()) == set(model.types.keys()) == {'a', 'b', 'c'})
        assert(model.allomorphs['a'] == {'-a': 3, '-A': 1})
        assert(model.allomorphs['b'] == {'-b': 3, '-B': 2})
        assert(model.allomorphs['c'] == {'c-': 2, 'C-': 1})
        assert(model.types['a'] == 'SUFFIX')
        assert(model.types['b'] == 'SUFFIX')
        assert(model.types['c'] == 'PREFIX')
        assert(model.order == ['c', 'a', 'b'])

    def test_miaseg_train(self):
        model = Miaseg()
        assert(model.train(train=PAPER_EXAMPLE))
        assert(set(model.allomorphs.keys()) == set(model.types.keys()) == {'PL', 'DAT'})
        assert(model.allomorphs['PL'] == {'ok': 1})
        assert(model.allomorphs['DAT'] == {'nak': 1, 'nek': 1})
        assert(model.types['PL'] == 'SUFFIX')
        assert(model.types['DAT'] == 'SUFFIX')
        assert(model.order == ['PL', 'DAT'])

        # compare to train_on_file
        assert(model.train_on_file('data/miaseg/paper_example.txt'))

        # ipa version
        model = Miaseg(use_ipa=True)
        assert(model.train(train=IPA_PAPER_EXAMPLE))
        assert(set(model.allomorphs.keys()) == set(model.types.keys()) == {'PL', 'DAT'})
        assert(model.allomorphs['PL'] == {'o k': 1})
        assert(model.allomorphs['DAT'] == {'n ɒ k': 1, 'n ɛ k': 1})
        assert(model.types['PL'] == 'SUFFIX')
        assert(model.types['DAT'] == 'SUFFIX')
        assert(model.order == ['PL', 'DAT'])

        # compare to train_on_file
        assert(model.train_on_file('data/miaseg/ipa_paper_example.txt'))

        # toy example
        model = Miaseg()
        assert(model.train(train=TOY_EXAMPLE))
        assert(set(model.allomorphs.keys()) == set(model.types.keys()) == {'a', 'b', 'c'})
        assert(model.allomorphs['a'] == {'-a': 3, '-A': 1})
        assert(model.allomorphs['b'] == {'-b': 3, '-B': 2})
        assert(model.allomorphs['c'] == {'c-': 2, 'C-': 1})
        assert(model.types['a'] == 'SUFFIX')
        assert(model.types['b'] == 'SUFFIX')
        assert(model.types['c'] == 'PREFIX')
        assert(model.order == ['c', 'a', 'b'])

        # compare to train_on_file
        assert(model.train_on_file('data/miaseg/toy_example.txt'))

    def test_miaseg__get_affixes(self):
        model = Miaseg()
        model.train(train=TOY_EXAMPLE)
        assert(model._get_affixes({'a', 'b', 'c'}) == (['c'], ['a', 'b']))

    def test_miaseg_segment(self):
        model = Miaseg()
        model.train(train=TOY_EXAMPLE)
        assert(model.segment(word='new_root', features=set(), with_analysis=False) == ['new_root'])
        assert(model.segment(word='new_root', features=set()) == (['new_root'], 
                                                                  ['ROOT']))
        assert(model.segment(word='new_root-a', features={'a'}, with_analysis=False) == ['new_root', '-a'])
        assert(model.segment(word='new_root-a', features={'a'}) == (['new_root', '-a'], 
                                                                  ['ROOT', 'a']))
        assert(model.segment(word='new_root-a-b', features={'a', 'b'}, with_analysis=False) == ['new_root', '-a', '-b'])
        assert(model.segment(word='new_root-a-b', features={'a', 'b'}) == (['new_root', '-a', '-b'], 
                                                                           ['ROOT', 'a', 'b']))
        assert(model.segment(word='c-new_root-a-b', features={'a', 'b', 'c'}, with_analysis=False) == ['c-', 'new_root', '-a', '-b'])
        assert(model.segment(word='c-new_root-a-b', features={'a', 'b', 'c'}) == (['c-', 'new_root', '-a', '-b'], 
                                                                                  ['c', 'ROOT', 'a', 'b']))
        
        # length resorting
        assert(model.segment(word='d-new_root-a-b', features={'a', 'b', 'c'}) == (['d-', 'new_root', '-a', '-b'], 
                                                                                  ['c', 'ROOT', 'a', 'b']))
        assert(model.segment(word='c-new_root-a-d', features={'a', 'b', 'c'}) == (['c-', 'new_root', '-a', '-d'], 
                                                                                  ['c', 'ROOT', 'a', 'b']))
        assert(model.segment(word='d-new_root-f-e', features={'a', 'b', 'c'}) == (['d-', 'new_root', '-f', '-e'], 
                                                                                  ['c', 'ROOT', 'a', 'b']))
        
        # new feature
        assert(model.segment(word='d-new_root-a-b', features={'a', 'b', 'd'}) == (['d-new_root-a-b'], ['FAILED']))
        assert(model.segment(word='d-new_root-a-b', features={'a', 'b', 'd'}, with_analysis=False) == ['d-new_root-a-b'])

        # paper example

        model = Miaseg()
        model.train(train=PAPER_EXAMPLE)
        assert(model.segment(word='tanár', features=set()) == (['tanár'],
                                                               ['ROOT']))
        assert(model.segment(word='tanárok', features={'PL'}) == (['tanár', 'ok'],
                                                                  ['ROOT', 'PL']))
        assert(model.segment(word='tanároknak', features={'PL', 'DAT'}) == (['tanár', 'ok', 'nak'],
                                                                            ['ROOT', 'PL', 'DAT']))
        assert(model.segment(word='személy', features=set()) == (['személy'],
                                                                 ['ROOT']))
        assert(model.segment(word='személynek', features={'DAT'}) == (['személy', 'nek'],
                                                                      ['ROOT', 'DAT']))
        # real new words
        assert(model.segment(word='lányoknak', features={'PL', 'DAT'}) == (['lány', 'ok', 'nak'],
                                                                           ['ROOT', 'PL', 'DAT']))
        assert(model(word='elnöknek', features={'DAT'}) == (['elnök', 'nek'], 
                                                            ['ROOT', 'DAT']))
        # made up new word
        assert(model.segment(word='atoknak', features={'PL', 'DAT'}) == (['at', 'ok', 'nak'],
                                                                         ['ROOT', 'PL', 'DAT']))
        
        # throw exception if passing a SegStr
        try:
            model.segment(word=SegStr('t ɒ n aː r', SegInv()), features=set()) == (['t ɒ n aː r'], ['ROOT'])
            assert(False)
        except ValueError as e:
            assert(e.__str__() == 'Cannot segment SegStr because Mɪᴀꜱᴇɢ object was not constructed with "use_ipa = True"')

        
        # ipa version
        model = Miaseg(use_ipa=True)
        model.train(train=IPA_PAPER_EXAMPLE)
        assert(model.segment(word='t ɒ n aː r', features=set()) == (['t ɒ n aː r'],
                                                                    ['ROOT']))
        assert(model.segment(word=SegStr('t ɒ n aː r', model.seginv), features=set()) == (['t ɒ n aː r'], ['ROOT'])) # words with SegStr too
        assert(model.segment(word='t ɒ n aː r o k', features={'PL'}) == (['t ɒ n aː r', 'o k'],
                                                                         ['ROOT', 'PL']))
        assert(model.segment(word='t ɒ n aː r o k n ɒ k', features={'PL', 'DAT'}) == (['t ɒ n aː r', 'o k', 'n ɒ k'],
                                                                            ['ROOT', 'PL', 'DAT']))
        assert(model.segment(word='s ɛ m eː j', features=set()) == (['s ɛ m eː j'],
                                                                 ['ROOT']))
        assert(model.segment(word='s ɛ m eː j n ɛ k', features={'DAT'}) == (['s ɛ m eː j', 'n ɛ k'],
                                                                      ['ROOT', 'DAT']))
        # real new words
        assert(model.segment('l aː ɲ o k n ɒ k', features={'PL', 'DAT'}) == (['l aː ɲ', 'o k', 'n ɒ k'],
                                                                             ['ROOT', 'PL', 'DAT']))
        assert(model('ɛ l n ø k n ɛ k', features={'DAT'}) == (['ɛ l n ø k', 'n ɛ k'],
                                                              ['ROOT', 'DAT']))
        # made up new word
        assert(model.segment(word='a t o k n ɒ k', features={'PL', 'DAT'}) == (['a t', 'o k', 'n ɒ k'],
                                                                               ['ROOT', 'PL', 'DAT']))
        
        # test untrained model
        model = Miaseg()
        try:
            model.segment(word='tanároknak', features={'PL', 'DAT'})
            assert(False)
        except ValueError as e:
            assert(True)
            assert(e.__str__() == 'Mɪᴀꜱᴇɢ must be trained in order to segment.')

    def test_miaseg_train_and_segment(self):
        model = Miaseg()
        results = model.train_and_segment(train=TOY_EXAMPLE)
        assert(len(results) == len(TOY_EXAMPLE))
        assert(len(bundle) == 3 for bundle in results)
        for triple, seg, ana in results:
            assert(set(triple[2]) == set(ana).difference({'ROOT'}))
            assert(triple[1] == ''.join(seg))
        results = model.train_and_segment(train=TOY_EXAMPLE, with_analysis=False)
        assert(len(results) == len(TOY_EXAMPLE))
        assert(len(bundle) == 2 for bundle in results)
        # check train_and_segment_file
        assert(results == model.train_and_segment_file('data/miaseg/toy_example.txt', with_analysis=False))

        model = Miaseg(use_ipa=True)
        results = model.train_and_segment(train=IPA_PAPER_EXAMPLE)
        assert(len(results) == len(IPA_PAPER_EXAMPLE))
        assert(len(bundle) == 3 for bundle in results)
        for triple, seg, ana in results:
            assert(set(triple[2]) == set(ana).difference({'ROOT'}))
            if len(seg) == 1:
                assert(triple[1] == seg[0])
            elif len(seg) == 2:
                assert(triple[1] == seg[0] + seg[1])
            else:
                assert(triple[1] == seg[0] + seg[1] + seg[2])
        # check train_and_segment_file
        assert(results == model.train_and_segment_file('data/miaseg/ipa_paper_example.txt'))

if __name__ == "__main__":
    unittest.main()