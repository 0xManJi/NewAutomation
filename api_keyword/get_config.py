import os


class Config(object):  # 默认配置
    DEBUG = False

    def __getitem__(self, key):
        return self.__getattribute__(key)


class DevelopmentConfig(Config):
    Name = 'dev'
    BackEndHost = "https://api-dev.backoffice.allforsport.cn"
    BackEndToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2Mjc2MjEyMzUzNTksImlkIjozNTZ9.6Bv8OJ73TnftF1thQ08RdV_YqL7jZPNP9nqNDRCaiGY"
    UserHost = "https://api-dev.wx.allforsport.cn"
    UserToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MzAxMzI3NTk3MjYsImlkIjo1OTl9.JZc9hItGEnpRGYe9DjJUprV5IUoqIYsHlPhhGwtzV74"


class PreProductionConfig(object):
    Host = "https://api-pp.backoffice.allforsport.cn"
    Token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmVzSW4iOjE2MTY3MjE5MDY4NjAsImlkIjoyMDB9.kjQS5NmN7nDkDiqKz5mtBFDRgl2WeuleI_0_NNPGV_s"


# 环境映射关系
mapping = {
    'dev': DevelopmentConfig,
    'pp': PreProductionConfig
}
# 一键切换环境
APP_ENV = os.environ.get('APP_ENV', 'dev').lower()
config = mapping[APP_ENV]()  # 获取指定的环境
