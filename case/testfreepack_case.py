# -*- coding: utf-8 -*-
# @Author  : Joy
# @FileName: testfreepack_case.py
from api_keyword.api_key import ApiKey
from api_keyword.get_config import config as conf
import json, time
import unittest
from ddt import ddt, file_data
from BeautifulReport import BeautifulReport as bf
from pprint import pprint


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
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": conf.UserToken}
        self.ClassTicketId = None
        self.PackageId = None
        self.PackOrder = None

    # 创建课时票
    @file_data('../data/add_classticket.yaml')
    def test_fp01(self, **kwargs):
        pprint("--------创建课时票--------")
        host = kwargs['url']
        data = kwargs['data']
        data['name'] = conf.Name + "免费课时包用票" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        Host = self.BackEndHost + host
        '''创建课时票，后续为用户分配'''
        res = self.ak.do_post(url=Host, headers=self.BackEndHeader, json=data)
        pprint("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)

    # 查询课时票ID，后续使用该ID
    @file_data('../data/query_classticket_list.yaml')
    def test_fp02(self, **kwargs):
        pprint("--------查询课时票列表，获取ID--------")
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host
        '''查询课时票列表，取最新的课时票的ID'''
        res = self.ak.do_get(url=Host, headers=self.BackEndHeader, params=data)
        pprint("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        classticketid = self.ak.get_text(res.text, "id")
        TestClassPackEvent.ClassTicketId = classticketid[0]
        self.assertEqual(res.json()['success'], True)

    # 创建免费课时包
    @file_data('../data/create_freepack.yaml')
    def test_fp03(self, **kwargs):
        pprint("--------创建免费课时包--------")
        host = kwargs['url']
        data = kwargs['data']
        data['name'] = conf.Name + "免费课时包" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data['tickets'][0]['classPackId'] = self.ClassTicketId
        Host = self.BackEndHost + host
        res = self.ak.do_post(url=Host, headers=self.BackEndHeader, json=data)
        packageId = self.ak.get_text(res.text, 'id')
        TestClassPackEvent.PackageId = packageId
        pprint("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)

    #领取课时包
    @file_data('../data/receive_freepack.yaml')
    def test_fp04(self,**kwargs):
        pprint("--------领取免费课时包--------")
        host = kwargs['url']
        data = kwargs['data']
        data['storeId'] = 319
        Host = self.UserHost + host + str(self.PackageId)
        res = self.ak.do_post(url=Host,data=data,headers=self.UserHeader)
        pprint("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        orderid = self.ak.get_text(res.text,"orderNumber")
        TestClassPackEvent.PackOrder = orderid
        self.assertEqual(res.json()['success'], True)

    #退回课时包
    @file_data("../data/return_freepack.yaml")
    def test_fp05(self,**kwargs):
        pprint("--------退回课时包--------")
        host = kwargs['url']
        data = kwargs['data']
        Host = self.BackEndHost + host + str(self.PackOrder)
        res = self.ak.do_delete(url=Host,json=data,headers=self.BackEndHeader)
        pprint("请求地址：{Url}，请求参数：{data},响应结果：{res}".format(Url=Host, data=data, res=res.json()))
        self.assertEqual(res.json()['success'], True)




if __name__ == '__main__':
    unittest.main()
