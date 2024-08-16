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
        seginv = SegInv()
        x = SegStr('eː n t j ə', seginv=seginv)
        assert(x.endswith('j ə'))
        sufx = x[-2:]
        assert(x.endswith(sufx))
        assert(x.startswith(x[:-2]))

        y = SegStr('eː n t', seginv=seginv)
        assert(x.startswith(y))
        assert(not y.startswith(x))

        z = SegStr('j ə', seginv=seginv)
        assert(x.endswith(z))
        assert(not z.endswith(x))

    def test_hash(self):
        x = SegStr('eː n t j ə', seginv=SegInv())
        assert(len({x, 'eː n t j ə'}))
        assert(x in {'eː n t j ə'})
        assert('eː n t j ə' in {x})
        assert(len({x, 'eː n t j ə', SegStr('eː n t j ə', seginv=SegInv())}) == 1)

    def test_concat(self):
        x = SegStr('eː n t', seginv=SegInv())
        y = SegStr('j ə', seginv=SegInv())
        assert(x + y == 'eː n t j ə')

    def test_concat_seg(self):
        seginv = SegInv()
        x = SegStr('eː n t', seginv=seginv)
        y = seginv.add_and_get('ə')
        assert(isinstance(y, Seg))
        z = x + y
        assert(isinstance(z, SegStr))
        assert(z == 'eː n t ə')

    def test_lt(self):
        x = SegStr('a', seginv=SegInv())
        y = SegStr('b', seginv=SegInv())
        assert(x < y)

        x = SegStr('a b', seginv=SegInv())
        y = SegStr('b', seginv=SegInv())
        assert(x < y)

if __name__ == "__main__":
    unittest.main()