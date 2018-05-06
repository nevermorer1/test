import unittest
import sys
import time

sys.path.append('../cases')
from cases.test_quota_change import QuotaChangeDes

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(QuotaChangeDes))
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = '../report/' + now + '_result.html'
    fp = open(filename, 'w')
    runner = unittest.TextTestRunner(stream=fp, verbosity=2)
    runner.run(suite)
