import unittest
import sys

sys.path.append('../')
from algophon.utils import tsp

class TestUtils(unittest.TestCase):
    def test_tsp(self):
        assert(tsp(n=10, e=0))
        assert(tsp(n=10, e=2))
        assert(tsp(n=10, e=4))
        assert(not tsp(n=10, e=5))
        assert(not tsp(n=7, e=4))
        assert(tsp(n=7, m=4))
         
        # small values
        assert(not tsp(n=0, e=0))
        assert(not tsp(n=1, e=0))
        assert(not tsp(n=1, m=1))
        assert(not tsp(n=3, e=2))
        assert(tsp(n=3, m=3))
        assert(tsp(n=2, e=0))
        assert(not tsp(n=2, e=1))

if __name__ == "__main__":
    unittest.main()