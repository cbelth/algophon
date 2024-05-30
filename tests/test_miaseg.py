import unittest
import sys

sys.path.append('../')
from algophon.models.Miaseg import Paradigm, Miaseg

class TestMiaseg(unittest.TestCase):
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