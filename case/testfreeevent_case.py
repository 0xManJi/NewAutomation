from api_keyword.api_key import ApiKey
from api_keyword.get_config import config as conf
import json, time
import unittest
from ddt import ddt, file_data
from BeautifulReport import BeautifulReport as bf



@ddt
class TestFreeEvent(unittest.TestCase):

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
    def test_ww01(self, **kwargs):
        print("--------创建免费活动模板--------")
        host = kwargs["url"]
        Host = self.BackEndHost + host
        data = kwargs["data"]
        data['title'] = conf.Name + "免费活动" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        res = self.ak.do_post(url=Host, json=data, headers=self.BackEndHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        eventTemplateId = self.ak.get_text(res.text, "id")
        TestFreeEvent.eventTemplateId = eventTemplateId
        self.assertEqual(res.json()['success'], True)

    # 发布活动场次
    @file_data('../data/event.yaml')
    def test_ww02(self, **kwargs):
        print("--------发布免费活动场次--------")
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        data[0]['eventTemplateId'] = self.eventTemplateId
        res = self.ak.do_post(url=Host, json=data, headers=self.BackEndHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)

    # 查询发布的活动场次，报名时需用到该ID
    @file_data('../data/event_list.yaml')
    def test_ww03(self, **kwargs):
        print("--------查询活动场次列表--------")
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        res = self.ak.do_get(url=Host, json=data, headers=self.BackEndHeader)
        eventID = self.ak.get_text(res.text, 'id')
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        TestFreeEvent.EventId = eventID[0]
        self.assertEqual(res.json()['success'], True)

    # 创建订单(报名活动)
    @file_data('../data/creat_order.yaml')
    def test_ww04(self, **kwargs):
        print("--------创建免费活动订单(报名该活动)--------")
        host = kwargs['url']
        data = kwargs['data']
        data['eventId'] = self.EventId
        data['eventTemplateId'] = self.eventTemplateId
        data = json.dumps(data)
        Host = self.UserHost + host
        res = self.ak.do_post(url=Host, data=data, headers=self.UserHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        orderid = self.ak.get_text(res.text, 'orderId')
        TestFreeEvent.OrderId = orderid
        self.assertEqual(res.json()['success'], True)

    # 取消订单
    @file_data('../data/remove_order.yaml')
    def test_ww05(self, **kwargs):
        print("--------取消免费报名订单--------")
        host = kwargs['url']
        data = self.OrderId
        Host = self.BackEndHost + host + str(data)
        res = self.ak.do_delete(url=Host, headers=self.BackEndHeader)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)

    # 取消活动场次
    @file_data('../data/remove_event.yaml')
    def test_ww06(self, **kwargs):
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
    def test_ww07(self, **kwargs):
        print("--------下架该燃值活动模板--------")
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host + str(self.eventTemplateId) + "?isOnShelf=false"
        res = self.ak.do_put(url=Host, headers=self.BackEndHeader, json=data)
        print("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)


if __name__ == '__main__':
    unittest.main
