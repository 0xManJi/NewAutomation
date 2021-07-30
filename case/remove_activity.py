# -*- coding: utf-8 -*-
# @Author  : Joy
# @FileName: remove_activity.py


import requests

headers = {
    "content-type": "application/json",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2Mjc2MjEyMzUzNTksImlkIjozNTZ9.6Bv8OJ73TnftF1thQ08RdV_YqL7jZPNP9nqNDRCaiGY"
}

'''取消活动场次'''
def remove_events():
    host = "https://api-dev.backoffice.allforsport.cn/v2/events/"
    for i in range(1323, 1500):
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
    for i in range(932, 1071):
        url = "https://api-dev.backoffice.allforsport.cn/v1/event_templates/on_shelf/{}?isOnShelf=false".format(i)
        body = {
            "isOnShelf": "false"
        }
        res = requests.put(url=url, json=body, headers=headers)
        print(res.json())


remove_template()
