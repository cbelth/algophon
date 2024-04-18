import unittest
from test_seg import TestSeg
from test_seginv import TestSegInv
from test_segstr import TestSegStr
from test_natclass import TestNatClass

'''
A script to run all the test cases.
'''
# load test suites
test_seg_suite = unittest.TestLoader().loadTestsFromTestCase(TestSeg)
test_seginv_suite = unittest.TestLoader().loadTestsFromTestCase(TestSegInv)
test_segstr_suite = unittest.TestLoader().loadTestsFromTestCase(TestSegStr)
test_natclass_suite = unittest.TestLoader().loadTestsFromTestCase(TestNatClass)
# combine the test suites
suites = unittest.TestSuite([
    test_seg_suite,
    test_seginv_suite,
    test_segstr_suite,
    test_natclass_suite
])
# run the test suites
unittest.TextTestRunner(verbosity=2).run(suites)
