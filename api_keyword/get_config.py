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
    BackEndToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MjgyMTU5NTI3NzMsImlkIjozNTZ9.aoiT5i78Dd8G_oVqvfhT23wkY6u6Njf44QJr8r03JGg"
    UserHost = "https://api-dev.wx.allforsport.cn"
    UserToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MzA1NzE5MTE4MzgsImlkIjo1OTl9.WJ_ptHbwqjuKg-CtqVXrS15A4l5-JLGBe1L257L1Sa0"


class PreProductionConfig(object):
    Name = 'pp'
    BackEndHost = "https://api-pp.backoffice.allforsport.cn"
    BackEndToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MjgyMTM1NjMwMjAsImlkIjozMTd9.sDWF_VBGnJvpgua_zhGTTCm4HbQoHdMCLf9kfbimutk"
    UserHost = "https://api-pp.wx.allforsport.cn"
    UserToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MzA3MjU2MDc4OTcsImlkIjozOTZ9.vLt2WMjUzdrCTJuADurwSedJtB2CVGumI6aoY1Td1eM"


# 环境映射关系
mapping = {
    'dev': DevelopmentConfig,
    'pp': PreProductionConfig
}

num = len(sys.argv)-1
if num<1 or num >1:
     exit("参数错误,必须传环境变量!比如: python xx.py dev|pp")
env = sys.argv[1]

APP_ENV=os.environ.get("APP_ENV",env).lower()
config=mapping[APP_ENV]()

if __name__ == '__main__':
    print(config.HOST)
