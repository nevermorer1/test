# import unittest
# import sys
# import time
#
# sys.path.append('../cases')
# from cases.test_quota_change import QuotaChangeDes
#
# if __name__ == '__main__':
#     suite = unittest.TestSuite()
#     suite.addTests(unittest.TestLoader().loadTestsFromTestCase(QuotaChangeDes))
#     now = time.strftime("%Y-%m-%d %H_%M_%S")
#     filename = '../report/' + now + '_result.html'
#     fp = open(filename, 'w')
#     runner = unittest.TextTestRunner(stream=fp, verbosity=2)
#     runner.run(suite)
#     fp.close()
from HTMLTestRunner import HTMLTestRunner
import unittest
import sys
import time

sys.path.append('../cases')
sys.path.append('../common')

test_dir = '../cases'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')

if __name__ == "__main__":
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = '../report/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            verbosity=2,
                            title='Backend Test Report',
                            description='Implementation Example with: ')
    runner.run(discover)
    fp.close()
