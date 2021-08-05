# -*- coding: utf-8 -*-
# @Author  : Joy
# @FileName: testburningevent_case.py
from api_keyword.api_key import ApiKey
from api_keyword.get_config import config as conf
from api_keyword.get_random import get_random
import json, time
import unittest
from ddt import ddt, file_data
from BeautifulReport import BeautifulReport as bf



@ddt
class TestBurningEvent(unittest.TestCase):
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
        self.BnHeader = {"content-type": "application/json",
                         "x-api-key": "6ec18e29-7c10-40ae-9dbe-3db8c908dfbf",
                         }
        self.ClassPackId = None
        self.eventTemplateId = None
        self.EventId = None
        self.OrderId = None

    # # 为用户分配燃值
    # @file_data("../data/add_burning.yaml")
    # def test_bn01(self, **kwargs):
    #     print("--------为用户分配燃值--------")
    #     Host = kwargs['url']
    #     data = kwargs['data']
    #     data['event_id'] = get_random()
    #     res = self.ak.do_post(url=Host, json=data, headers=self.BnHeader)
    #     print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
    #     self.assertEqual(res.json()['message'], "Data created successful.")

    @file_data("../data/event_template.yaml")
    # 创建燃值活动模板
    def test_bn02(self, **kwargs):
        print("--------创建燃值类型的活动模板--------")
        host = kwargs["url"]
        Host = self.BackEndHost + host
        data = kwargs["data"]
        data['title'] = conf.Name + "燃值活动" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data['registerType'] = 1
        data['registerFee'] = 100
        res = self.ak.do_post(url=Host, json=data, headers=self.BackEndHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        eventTemplateId = self.ak.get_text(res.text, "id")
        TestBurningEvent.eventTemplateId = eventTemplateId
        self.assertEqual(res.json()['success'], True)

    # 发布燃值活动场次
    @file_data('../data/event.yaml')
    def test_bn03(self, **kwargs):
        print("--------发布燃值活动场次--------")
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        data[0]['eventTemplateId'] = self.eventTemplateId
        res = self.ak.do_post(url=Host, json=data, headers=self.BackEndHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)

    # 查询燃值活动场次ID
    @file_data('../data/event_list.yaml')
    def test_bn04(self, **kwargs):
        print("--------查询活动场次列表，获取活动场次ID--------")
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        res = self.ak.do_get(url=Host, json=data, headers=self.BackEndHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        eventID = self.ak.get_text(res.text, 'id')
        TestBurningEvent.EventId = eventID[0]
        self.assertEqual(res.json()['success'], True)

    # 创建订单(报名燃值活动)
    @file_data('../data/creat_order.yaml')
    def test_bn05(self, **kwargs):
        print("--------报名该燃值活动--------")
        host = kwargs['url']
        data = kwargs['data']
        data['eventId'] = self.EventId
        data['eventTemplateId'] = self.eventTemplateId
        data['registerFee'] = 100
        data["bookingType"] = 1
        data = json.dumps(data)
        Host = self.UserHost + host
        res = self.ak.do_post(url=Host, data=data, headers=self.UserHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        orderid = self.ak.get_text(res.text, 'orderId')
        TestBurningEvent.OrderId = orderid
        self.assertEqual(res.json()['success'], True)

    # 取消订单
    @file_data('../data/remove_order.yaml')
    def test_bn06(self, **kwargs):
        print("--------取消燃值报名订单--------")
        host = kwargs['url']
        data = self.OrderId
        Host = self.BackEndHost + host + str(data)
        res = self.ak.do_delete(url=Host, headers=self.BackEndHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)

    # 取消活动场次
    @file_data('../data/remove_event.yaml')
    def test_bn07(self, **kwargs):
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
    def test_bn08(self, **kwargs):
        print("--------下架该燃值活动模板--------")
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host + str(self.eventTemplateId) + "?isOnShelf=false"
        res = self.ak.do_put(url=Host, headers=self.BackEndHeader, json=data)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)


if __name__ == '__main__':
    unittest.main()
