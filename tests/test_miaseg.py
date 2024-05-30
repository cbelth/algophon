import unittest
import sys

sys.path.append('../')
from algophon.models.Miaseg import Paradigm, Miaseg

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

if __name__ == "__main__":
    unittest.main()