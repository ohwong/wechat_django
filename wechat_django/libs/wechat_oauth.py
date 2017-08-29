import functools
from wechatpy.oauth import WeChatOAuth
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect

from wechat_django.constant import SESSION_EXPIRED_SECONDS


class Oauth(object):
    def __init__(self, wechat, scope='snsapi_userinfo'):
        """
        :param wechat: instance of `models.Wechat` 
        :param scope: 
        """
        self.wechat = wechat
        self.oauth = WeChatOAuth(wechat.appid, wechat.secret,
                                 wechat.redirect_uri, scope)

    def fetch_access_token(self, code):
        return self.oauth.fetch_access_token(code)

    def get_user_info(self):
        return self.get_user_info()

    @property
    def authorize_url(self):
        return self.oauth.authorize_url

    def oauth_required(self, method):
        @functools.wraps(method)
        def warpper(request, *args, **kwargs):
            code = request.GET.get('code', None)
            if request.session.get("user_info"):
                return method(request, *args, **kwargs)
            if code:
                try:
                    self.oauth.fetch_access_token(code)
                    user_info = self.oauth.get_user_info()
                except Exception as e:
                    print(e.errmsg, e.errcode)
                    # 这里需要处理请求里包含的 code 无效的情况
                    HttpResponse("ERROR")
                else:
                    request.session['user_info'] = user_info
                    request.session.set_expiry(SESSION_EXPIRED_SECONDS)
            else:
                return HttpResponseRedirect(self.authorize_url)
            return method(request, *args, **kwargs)
        return warpper
