import os
import sys
'''默认配置'''
class Config(object):
    DEBUG = False

    def __getitem__(self, key):
        return self.__getattribute__(key)


class DevelopmentConfig(Config):
    Name = 'dev'
    BackEndHost = "https://api-dev.backoffice.allforsport.cn"
    BackEndToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MjgzMDMwMTQ4NDEsImlkIjozNTZ9.SnG1_402f1em8RzU-LhKgsmoE2GwLYcfhFlS11VtI5w"
    UserHost = "https://api-dev.wx.allforsport.cn"
    UserToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MzA1NzE5MTE4MzgsImlkIjo1OTl9.WJ_ptHbwqjuKg-CtqVXrS15A4l5-JLGBe1L257L1Sa0"


class PreProductionConfig(object):
    Name = 'pp'
    BackEndHost = "https://api-pp.backoffice.allforsport.cn"
    BackEndToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MjgzMDI5ODQ5OTUsImlkIjozMTd9.VhzIYTdPqjqyx9PouUMg-zj0Y5W2lJubXoK0KnqRyUo"
    UserHost = "https://api-pp.wx.allforsport.cn"
    UserToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MzA4MDg2ODk5ODgsImlkIjozOTZ9.MBBFAnUTnA_rzNjHlArXLqVU6EjJte-8Gtoa223bkTA"


# 环境映射关系
mapping = {
    'dev': DevelopmentConfig,
    'pp': PreProductionConfig
}
#切换环境
# APP_ENV = os.environ.get('APP_ENV', 'pp').lower()
# config = mapping[APP_ENV]()  # 获取指定的环境


num = len(sys.argv)-1
if num<1 or num >1:
     exit("参数错误,必须传环境变量!比如: python xx.py dev|pp")
env = sys.argv[1]

APP_ENV=os.environ.get("APP_ENV",env).lower()
config=mapping[APP_ENV]()