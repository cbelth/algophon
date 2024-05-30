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

if __name__ == "__main__":
    unittest.main()