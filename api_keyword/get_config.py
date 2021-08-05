import os

'''默认配置'''
class Config(object):
    DEBUG = False

    def __getitem__(self, key):
        return self.__getattribute__(key)


class DevelopmentConfig(Config):
    Name = 'dev'
    BackEndHost = "https://api-dev.backoffice.allforsport.cn"
    BackEndToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MjgyMTM0OTg1MDIsImlkIjozNTZ9.H8_l-_XNReh--2RuC4saH8wLgRn-y7PILp0e6C76-xg"
    UserHost = "https://api-dev.wx.allforsport.cn"
    UserToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MzA1NzE5MTE4MzgsImlkIjo1OTl9.WJ_ptHbwqjuKg-CtqVXrS15A4l5-JLGBe1L257L1Sa0"


class PreProductionConfig(object):
    Host = "https://api-pp.backoffice.allforsport.cn"
    Token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MjgyMTM1NjMwMjAsImlkIjozMTd9.sDWF_VBGnJvpgua_zhGTTCm4HbQoHdMCLf9kfbimutk"


# 环境映射关系
mapping = {
    'dev': DevelopmentConfig,
    'pp': PreProductionConfig
}
# 切换环境
APP_ENV = os.environ.get('APP_ENV', 'dev').lower()
config = mapping[APP_ENV]()  # 获取指定的环境
