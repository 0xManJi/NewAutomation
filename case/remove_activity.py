# -*- coding: utf-8 -*-
# @Author  : Joy
# @FileName: remove_activity.py


import requests

headers = {
    "content-type": "application/json",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MjgwNDI4NDI3NDUsImlkIjozNTZ9.qiixmNEKhO_yTMgVviMnch3dhQl_szbShC_rH3PmxTA"
}

'''取消活动场次'''


def remove_events():
    host = "https://api-dev.backoffice.allforsport.cn/v2/events/"
    for i in range(1500, 1506):
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
    for i in range(1189, 1199):
        url = "https://api-dev.backoffice.allforsport.cn/v1/event_templates/on_shelf/{}?isOnShelf=false".format(i)
        body = {
            "isOnShelf": "false"
        }
        res = requests.put(url=url, json=body, headers=headers)
        print(res.json())


if __name__ == '__main__':
    remove_template()
