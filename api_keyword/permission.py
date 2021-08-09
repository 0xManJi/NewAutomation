# -*- coding: utf-8 -*-
# @Author  : Joy
# @FileName: permission.py


import requests

url = "https://api-dev.backoffice.allforsport.cn/v1/permissions"

headers = {"content-type": "application/json",
           "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MjgzMjA0Mjc4MTksImlkIjozNTZ9.gTYR2CquIzFpDggblwauw9Ik4fCel4cihp6WK5FGhQE"}

for i in range(2, 50):
    body = {
        "title": "权限A0000{}".format(i),
        "projectId": 1,
        "code": "A0000{}".format(i),
        "description": "A0000{}".format(i)}

    res = requests.post(url=url, headers=headers, json=body)
    print(res.json())
