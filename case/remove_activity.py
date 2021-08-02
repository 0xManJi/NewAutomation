# -*- coding: utf-8 -*-
# @Author  : Joy
# @FileName: remove_activity.py


import requests

headers = {
    "content-type": "application/json",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2Mjc5NTY0MzE1NTYsImlkIjozNTZ9.IhDM3y6bQG4BNmxoygiEcnk_reGmJ0FPuzpPO7r29zE"
}

'''取消活动场次'''


def remove_events():
    host = "https://api-dev.backoffice.allforsport.cn/v2/events/"
    for i in range(1350, 1450):
        body = {
            "description": "1234",
            "id": i,
            "megSendParticipants": "",
            "reasonType": 1
        }
        url = host + str(i)
        res = requests.delete(url=url, json=body, headers=headers)
        print(res.json())


'''下架活动模板'''


def remove_template():
    templateurl = "https://api-dev.backoffice.allforsport.cn/v1/event_templates/on_shelf/931?isOnShelf=false"
    for i in range(700, 1140):
        url = "https://api-dev.backoffice.allforsport.cn/v1/event_templates/on_shelf/{}?isOnShelf=false".format(i)
        body = {
            "isOnShelf": "false"
        }
        res = requests.put(url=url, json=body, headers=headers)
        print(res.json())


if __name__ == '__main__':
    remove_template()
