import unittest,os
from BeautifulReport import BeautifulReport
from api_keyword.get_config import config as conf


if __name__ == '__main__':
    localpath = os.getcwd()
    filepath = os.path.join(localpath,'Report')
    test_suite = unittest.defaultTestLoader.discover('case', pattern='test*.py')
    result = BeautifulReport(test_suite)
    result.report(filename='测试报告', description='booking场景自动化报告({}环境)'.format(conf.Name),log_path=filepath)

