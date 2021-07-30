from api_keyword.api_key import ApiKey
from api_keyword.get_config import config as conf
import json, time
import unittest
from ddt import ddt, file_data
from BeautifulReport import BeautifulReport as bf

@ddt
class TestApiCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.ak = ApiKey()
        self.eventTemplateId = None
        self.EventId = None
        self.OrderId = None
        self.BackEndHost = conf.BackEndHost
        self.BackEndHeader = {
            "content-type": "application/json",
            "token": conf.BackEndToken}
        self.UserHost = conf.UserHost
        self.UserHeader = {
            "content-type": "application/json",
            "Authorization": conf.UserToken}

    # 创建活动模板
    @file_data('../data/event_template.yaml')
    def test_creat_event_templates(self, **kwargs):
        '''创建活动模板'''
        host = kwargs["url"]
        Host = self.BackEndHost + host
        data = kwargs["data"]
        data['title'] = conf.Name + "免费活动" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        res = self.ak.do_post(url=Host, json=data, headers=self.BackEndHeader)
        eventTemplateId = self.ak.get_text(res.text, "id")
        TestApiCase.eventTemplateId = eventTemplateId

    # 发布活动场次
    @file_data('../data/event.yaml')
    def test_ww02(self, **kwargs):
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        data[0]['eventTemplateId'] = self.eventTemplateId
        res = self.ak.do_post(url=Host, json=data, headers=self.BackEndHeader)

    # 查询发布的活动场次，报名时需用到该ID
    @file_data('../data/event_list.yaml')
    def test_query_event_list(self, **kwargs):
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        res = self.ak.do_get(url=Host, json=data, headers=self.BackEndHeader)
        eventID = self.ak.get_text(res.text, 'id')
        TestApiCase.EventId = eventID[0]

    # 创建订单(报名活动)
    @file_data('../data/creat_order.yaml')
    def test_ww04(self, **kwargs):
        host = kwargs['url']
        data = kwargs['data']
        data['eventId'] = self.EventId + 1
        data['eventTemplateId'] = self.eventTemplateId
        data = json.dumps(data)
        Host = self.UserHost + host
        res = self.ak.do_post(url=Host, data=data, headers=self.UserHeader)
        orderid = self.ak.get_text(res.text, 'orderId')
        TestApiCase.OrderId = orderid

    # 取消订单
    @file_data('../data/remove_order.yaml')
    def test_ww05(self, **kwargs):
        host = kwargs['url']
        data = self.OrderId
        Host = self.BackEndHost + host + data
        res = self.ak.do_delete(url=Host, headers=self.BackEndHeader)


if __name__ == '__main__':
    test_suite = unittest.defaultTestLoader.discover('./tests', pattern='test*.py')
    result = BeautifulReport(test_suite)
    result.report(filename='测试报告.html', description='测试deafult报告', report_dir='../report', theme='theme_default')


