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

    # 创建课时票并将课时票分配给用户
    @file_data('../data/classpack.yaml')
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
    def test_cp03(self, **kwargs):
        pass

    # 创建课时票活动

    # 发布课时票场次

    # 创建订单

    # 取消订单


if __name__ == '__main__':
    unittest.main
