import unittest,os
from BeautifulReport import BeautifulReport

if __name__ == '__main__':
    localpath = os.getcwd()
    filepath = os.path.join(localpath,'Report')
    test_suite = unittest.defaultTestLoader.discover('case', pattern='test*.py')
    result = BeautifulReport(test_suite)
    result.report(filename='booking场景测试报告', description='booking场景自动化报告',log_path=filepath)

