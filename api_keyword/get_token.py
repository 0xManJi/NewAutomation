# -*- coding: utf-8 -*-
# @Author  : Joy
# @FileName: get_token.py

import requests
import yaml
from api_keyword.api_key import ApiKey

def dev_login():
    headers = {"token":"1234567890"}
    url = "https://api-dev.backoffice.allforsport.cn/v2/backend-user?id=356"
    body = {"id":"356"}
    res = requests.get(url=url,params=body,headers=headers)
    get_token = ApiKey().get_text(res.text,'token')
    return get_token


def pp_login():
    headers = {"token":"1234567890"}
    url = "https://api-pp.backoffice.allforsport.cn/v2/backend-user?id=317"
    body = {"id":"356"}
    res = requests.get(url=url,params=body,headers=headers)
    get_token = ApiKey().get_text(res.text,'token')
    return get_token
if __name__ == '__main__':

    dev_login()
    pp_login()
