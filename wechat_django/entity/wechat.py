import functools

from django.db import models
from wechatpy import WeChatClient
from wechatpy.utils import check_signature
from wechat_django.constant import WECHAT_TYPE_CHOICES, WECHAT_TYPE_SUB
from wechat_django.libs import Oauth, Menu, WechatUser, Message


class Wechat(models.Model):

    """
     微信公众号的本地记录
     可以通过该实例对微信公号进行相关操作
     1. 创建微信公众号
     ```
          >>> wechat = Wechat(appid="", secret="", token="wechat",
                    url="", encoding_aes_key=" ")
          >>> wechat.save()
     ```
     2. 查看公众号菜单
     ```
         >>> wechat.menu.remote_get()
         ...{'button': [{'name': 'name',
         'sub_button': [{'name': 'name',
         'sub_button': [],
         'type': 'view',
         'url': 'http://mp.weixin.qq.com'},
         {'name': 'test',
         'sub_button': [],
         'type': 'view',
         'url': 'http://mp.weixin.qq.com'}]}]}
     ```
     2. 将微信公众号菜单同步到本地
     ```
         >>> menu_dict = wechat.menu.remote_get()
         >>> wechat.menu.local_create(menu_dict)
     ```
     
     3. 将本地菜单发布到微信公众号
     ```
         >>> menu_dict = wechat.menu.local_get()
         >>> wechat.menu.remote_create(menu_dict)
     ```
     
     4. 初始化菜单
     ```
         >>> menu_dict = {'button': [{'name': 'name',
         'sub_button': [{'name': 'name',
         'sub_button': [],
         'type': 'view',
         'url': 'http://mp.weixin.qq.com'},
         {'name': 'test',
         'sub_button': [],
         'type': 'view',
         'url': 'http://mp.weixin.qq.com'}]}]}
         >>> wechat.menu.build(menu_dict)
     ```
    """
    class Meta:
        db_table = "wechat"
        verbose_name_plural = verbose_name = "微信"

    name = models.CharField(max_length=32)
    appid = models.CharField(max_length=18, unique=True)
    secret = models.CharField(max_length=32)
    token = models.CharField(max_length=32)
    url = models.CharField(max_length=191)
    encoding_aes_key = models.CharField(max_length=43)
    # 公众号二维码
    qcode = models.CharField(max_length=191, blank=True, null=True)
    # 公众号类型
    service_type = models.IntegerField(choices=WECHAT_TYPE_CHOICES,
                                       default=WECHAT_TYPE_SUB)
    redirect_uri = models.CharField(max_length=191, default=None)

    @property
    def client(self):
        return WeChatClient(self.appid, self.secret)

    @property
    def oauth(self):
        """微信授权相关"""
        return Oauth(self)

    @property
    def menu(self):
        """微信菜单， 根据该属性创建/修改微信菜单"""
        return Menu(self, self.client)

    @property
    def user(self):
        """微信用户管理"""
        return WechatUser(self, self.client)

    @property
    def message(self):
        """消息管理"""
        return Message(self, self.client)

    def check_signature(self, signature, timestamp, nonce):
        """检查签名的合法性
        :raise: `wechatpy.exceptions.InvalidSignatureException`
        """
        check_signature(self.token, signature, timestamp, nonce)

    def __str__(self):
        return self.name
