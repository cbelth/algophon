import unittest
import sys
sys.path.append('../')
from algophon.segstr import SegStr
from algophon.seginv import SegInv
from algophon.seg import Seg

class TestSegStr(unittest.TestCase):
    def test_init(self):
        seginv = SegInv()
        x = SegStr('eː n t j ə', seginv=seginv)
        assert(x is not None)
        assert(seginv.segs == {'ə', 't', 'n', 'j', 'eː'})
        
    def test_len(self):
        x = SegStr('eː n t j ə', seginv=SegInv())
        assert(len(x) == 5)

    def test_index_slice(self):
        x = SegStr('eː n t j ə', seginv=SegInv())
        assert(x[0] == 'eː')
        assert(x[-2:] == 'j ə')
        assert(x[-2:] != 'ə n')
        assert(isinstance(x[0], Seg))
        assert(isinstance(x[-2:], SegStr))

    def test_endswith_startswith(self):
        x = SegStr('eː n t j ə', seginv=SegInv())
        assert(x.endswith('j ə'))
        sufx = x[-2:]
        assert(x.endswith(sufx))
        assert(x.startswith(x[:-2]))

    def test_hash(self):
        x = SegStr('eː n t j ə', seginv=SegInv())
        assert(len({x, 'eː n t j ə'}))
        assert(x in {'eː n t j ə'})
        assert('eː n t j ə' in {x})
        assert(len({x, 'eː n t j ə', SegStr('eː n t j ə', seginv=SegInv())}) == 1)


if __name__ == "__main__":
    unittest.main()