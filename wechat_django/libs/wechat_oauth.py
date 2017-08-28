import functools
from wechatpy.oauth import WeChatOAuth


class Oauth(object):
    def __init__(self, appid, secret, redirect_url=None):
        self._appid = appid
        self.secret = secret
        self.redirect_url = redirect_url

    def set_redirect_url(self, redirect_url):
        pass
