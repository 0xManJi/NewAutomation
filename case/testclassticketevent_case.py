# -*- coding: utf-8 -*-
# @Author  : Joy
# @FileName: testclassticketevent_case.py
from api_keyword.api_key import ApiKey
from api_keyword.get_config import config as conf
import json, time
import unittest
from ddt import ddt, file_data
from BeautifulReport import BeautifulReport as bf



@ddt
class TestClassTicketEvent(unittest.TestCase):
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
    @file_data('../data/add_classticket.yaml')
    def test_cp01(self, **kwargs):
        print("--------创建课时票--------")
        host = kwargs['url']
        data = kwargs['data']
        data['name'] = conf.Name + "场景课时票" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        Host = self.BackEndHost + host
        '''创建课时票，后续为用户分配'''
        res = self.ak.do_post(url=Host, headers=self.BackEndHeader, json=data)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)

    # 查询课时票ID，后续使用该ID
    @file_data('../data/query_classticket_list.yaml')
    def test_cp02(self, **kwargs):
        print("--------查询课时票列表，获取ID--------")
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        '''查询课时票列表，取最新的课时票的ID'''
        res = self.ak.do_get(url=Host, headers=self.BackEndHeader, params=data)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        classpackid = self.ak.get_text(res.text, "id")
        TestClassTicketEvent.ClassPackId = classpackid[0]
        self.assertEqual(res.json()['success'], True)

    # 为指定用户分配课时票
    @file_data('../data/distribution_classticket.yaml')
    def test_cp03(self, **kwargs):
        print("--------将该课时票分配给用户--------")
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        data['classId'] = self.ClassPackId
        res = self.ak.do_post(url=Host, json=data, headers=self.BackEndHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)

    # 创建该课时票活动
    @file_data('../data/event_template.yaml')
    def test_cp04(self, **kwargs):
        print("--------创建该课时票类型的活动模板--------")
        listID = []
        listID.append(self.ClassPackId)
        host = kwargs["url"]
        Host = self.BackEndHost + host
        data = kwargs["data"]
        data['title'] = conf.Name + "课时票活动" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data['classPackes'] = listID
        data['registerType'] = 2
        res = self.ak.do_post(url=Host, json=data, headers=self.BackEndHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        eventTemplateId = self.ak.get_text(res.text, "id")
        TestClassTicketEvent.eventTemplateId = eventTemplateId
        self.assertEqual(res.json()['success'], True)

    # 发布课时票活动场次
    @file_data('../data/event.yaml')
    def test_cp05(self, **kwargs):
        print("--------发布课时票活动场次--------")
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        data[0]['eventTemplateId'] = self.eventTemplateId
        res = self.ak.do_post(url=Host, json=data, headers=self.BackEndHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)

    # 查询课时票场次ID
    @file_data('../data/event_list.yaml')
    def test_cp06(self, **kwargs):
        print("--------查询活动场次列表，获取活动场次ID--------")
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        res = self.ak.do_get(url=Host, json=data, headers=self.BackEndHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        eventID = self.ak.get_text(res.text, 'id')
        TestClassTicketEvent.EventId = eventID[0]
        self.assertEqual(res.json()['success'], True)

    # 创建订单(报名活动)
    @file_data('../data/creat_order.yaml')
    def test_cp07(self, **kwargs):
        print("--------报名该课时票活动--------")
        host = kwargs['url']
        data = kwargs['data']
        data['eventId'] = self.EventId
        data['eventTemplateId'] = self.eventTemplateId
        data['classId'] = self.ClassPackId
        data['bookingType'] = 2
        data = json.dumps(data)
        Host = self.UserHost + host
        res = self.ak.do_post(url=Host, data=data, headers=self.UserHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        orderid = self.ak.get_text(res.text, 'orderId')
        TestClassTicketEvent.OrderId = orderid
        self.assertEqual(res.json()['success'], True)

    # 取消订单
    @file_data('../data/remove_order.yaml')
    def test_cp08(self, **kwargs):
        print("--------取消课时票报名订单--------")
        host = kwargs['url']
        data = self.OrderId
        Host = self.BackEndHost + host + str(data)
        res = self.ak.do_delete(url=Host, headers=self.BackEndHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)
    # 取消活动场次
    @file_data('../data/remove_event.yaml')
    def test_cp09(self, **kwargs):
        print("--------取消该燃值活动场次--------")
        host = kwargs['url']
        data = kwargs['data']
        data['id'] = self.EventId
        Host = self.BackEndHost + host + str(self.EventId)
        res = self.ak.do_delete(url=Host, headers=self.BackEndHeader, json=data)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)

    # 下架活动模板
    @file_data('../data/remove_template.yaml')
    def test_cp10(self, **kwargs):
        print("--------下架该燃值活动模板--------")
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host + str(self.eventTemplateId) + "?isOnShelf=false"
        res = self.ak.do_put(url=Host, headers=self.BackEndHeader, json=data)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)

if __name__ == '__main__':
    unittest.main
