import unittest
from test_seg import TestSeg
from test_seginv import TestSegInv
from test_segstr import TestSegStr
from test_natclass import TestNatClass
from test_distance import TestDistance
from test_utils import TestUtils
from test_data_structures import TestDataStructures
from test_d2l import TestD2L
from test_miaseg import TestMiaseg

'''
A script to run all the test cases.
'''
# load test suites
test_seg_suite = unittest.TestLoader().loadTestsFromTestCase(TestSeg)
test_seginv_suite = unittest.TestLoader().loadTestsFromTestCase(TestSegInv)
test_segstr_suite = unittest.TestLoader().loadTestsFromTestCase(TestSegStr)
test_natclass_suite = unittest.TestLoader().loadTestsFromTestCase(TestNatClass)
test_distance_suite = unittest.TestLoader().loadTestsFromTestCase(TestDistance)
test_utils_suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
test_datastructures_suite = unittest.TestLoader().loadTestsFromTestCase(TestDataStructures)
test_d2l_suite = unittest.TestLoader().loadTestsFromTestCase(TestD2L)
test_miaseg_suite = unittest.TestLoader().loadTestsFromTestCase(TestMiaseg)
# combine the test suites
suites = unittest.TestSuite([
    test_seg_suite,
    test_seginv_suite,
    test_segstr_suite,
    test_natclass_suite,
    test_distance_suite,
    test_utils_suite,
    test_datastructures_suite,
    test_d2l_suite,
    test_miaseg_suite
])
# run the test suites
unittest.TextTestRunner(verbosity=2).run(suites)
