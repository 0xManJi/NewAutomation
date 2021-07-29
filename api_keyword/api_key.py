import requests, json
import jsonpath


class ApiKey:
    # 封装常用的接口函数

    def do_get(self, url, params=None, **kwargs):
        return requests.get(url=url, params=params, **kwargs)

    def do_post(self, url, data=None, **kwargs):
        return requests.post(url=url, data=data, **kwargs)

    def do_delete(self, url, data=None, **kwargs):
        return requests.delete(url=url, data=data,**kwargs)

    def get_text(self, res, key):
        '''
        如果返回结果不为空
        '''
        if res is not None:
            try:
                '''
                将结果转化为json格式
                '''
                text = json.loads(res)
                value = jsonpath.jsonpath(text, "$..{0}".format(key))
                '''
                如果值的长度为1，就返回第一个值，否则返回所有的值
                '''
                if value:
                    if len(value) == 1:
                        return value[0]
                return value
            except Exception as e:
                return e
        else:
            return None
