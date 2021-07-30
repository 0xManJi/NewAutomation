# -*- coding: utf-8 -*-
# @Author  : Joy
# @FileName: testclasspack_event.py
from api_keyword.api_key import ApiKey
from api_keyword.get_config import config as conf
import json, time
import unittest
from ddt import ddt, file_data
from BeautifulReport import BeautifulReport as bf


@ddt
class TestClassPackEvent(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ak = ApiKey()
        self.BackEndHost = conf.BackEndHost
        self.BackEndHeader = {
            "content-type": "application/json",
            "token": conf.BackEndToken}
        self.UserHost = conf.UserHost
        self.UserHeader = {
            "content-type": "application/json",
            "Authorization": conf.UserToken}
        self.ClassPackId = None
        self.eventTemplateId = None
        self.EventId = None
        self.OrderId = None

    # 创建课时票
    @file_data('../data/add_classpack.yaml')
    def test_cp01(self, **kwargs):
        host = kwargs['url']
        data = kwargs['data']
        data['name'] = conf.Name + "场景课时票" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        Host = self.BackEndHost + host
        '''创建课时票，后续为用户分配'''
        res = self.ak.do_post(url=Host, headers=self.BackEndHeader, json=data)

    # 查询课时票ID，后续使用该ID
    @file_data('../data/query_classpack_list.yaml')
    def test_cp02(self, **kwargs):
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        '''查询课时票列表，取最新的课时票的ID'''
        res = self.ak.do_get(url=Host, headers=self.BackEndHeader, params=data)
        classpackid = self.ak.get_text(res.text, "id")
        TestClassPackEvent.ClassPackId = classpackid[0]

    # 为指定用户分配课时票
    @file_data('../data/distribution_classpack.yaml')
    def test_cp03(self, **kwargs):
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        data['classId'] = self.ClassPackId
        res = self.ak.do_post(url=Host, json=data, headers=self.BackEndHeader)

    # 创建该课时票活动
    @file_data('../data/event_template.yaml')
    def test_cp04(self, **kwargs):
        listID = []
        listID.append(self.ClassPackId)
        host = kwargs["url"]
        Host = self.BackEndHost + host
        data = kwargs["data"]
        data['title'] = conf.Name + "课时票活动" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data['classPackes'] = listID
        data['registerType'] = 2
        res = self.ak.do_post(url=Host, json=data, headers=self.BackEndHeader)
        eventTemplateId = self.ak.get_text(res.text, "id")
        TestClassPackEvent.eventTemplateId = eventTemplateId

    # 发布课时票活动场次
    @file_data('../data/event.yaml')
    def test_cp05(self, **kwargs):
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        data[0]['eventTemplateId'] = self.eventTemplateId
        res = self.ak.do_post(url=Host, json=data, headers=self.BackEndHeader)

    # 查询课时票场次ID
    @file_data('../data/event_list.yaml')
    def test_cp06(self, **kwargs):
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        res = self.ak.do_get(url=Host, json=data, headers=self.BackEndHeader)
        eventID = self.ak.get_text(res.text, 'id')
        TestClassPackEvent.EventId = eventID[0]
        print("课时票场次id：", self.EventId)

    # 创建订单(报名活动)
    @file_data('../data/creat_order.yaml')
    def test_cp07(self, **kwargs):
        host = kwargs['url']
        data = kwargs['data']
        data['eventId'] = self.EventId
        data['eventTemplateId'] = self.eventTemplateId
        data['classId'] = self.ClassPackId
        data = json.dumps(data)
        Host = self.UserHost + host
        res = self.ak.do_post(url=Host, data=data, headers=self.UserHeader)
        orderid = self.ak.get_text(res.text, 'orderId')
        TestClassPackEvent.OrderId = orderid
    # 取消订单
    @file_data('../data/remove_order.yaml')
    def test_cp08(self, **kwargs):
        host = kwargs['url']
        data = self.OrderId
        Host = self.BackEndHost + host + str(data)
        print(Host,self.OrderId)
        res = self.ak.do_delete(url=Host, headers=self.BackEndHeader)


if __name__ == '__main__':
    unittest.main
