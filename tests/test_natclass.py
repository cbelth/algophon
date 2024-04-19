import unittest
import sys
sys.path.append('../')
from algophon.natclass import NatClass
from algophon.seginv import SegInv

class TestNatClass(unittest.TestCase):
    def test_init(self):
        nc = NatClass(feats={'+son'}, seginv=SegInv())
        assert(nc is not None)
        assert(f'{nc}' == '[+son]')
        nc = NatClass(feats={'+son', '-syl'}, seginv=SegInv())
        assert(nc is not None)
        assert(f'{nc}' == '[+son,-syl]')

    def test_in(self):
        seginv = SegInv()
        seginv.add_segs({'a', 'e', 'i', 'o', 'u', 'p', 'b', 't', 'd', 'k', 'g', 's', 'm', 'n'})
        nc = NatClass(feats={'+syl'}, seginv=seginv)
        for v in ['a', 'e', 'i', 'o', 'u']:
            assert(v in nc)
        for c in ['p', 'b', 't', 'd', 'k', 'g', 's', 'm', 'n']:
            assert(c not in nc)

if __name__ == "__main__":
    unittest.main()