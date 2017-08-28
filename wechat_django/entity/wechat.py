import functools

from django.db import models
from wechatpy import WeChatClient
from wechatpy.utils import check_signature
from wechat_django.constant import WECHAT_TYPE_CHOICES, WECHAT_TYPE_SUB


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

    class Menu(object):
        def __init__(self, wechat, client):
            self.wechat = wechat
            self.client = client

        @property
        def parent_menus(self):
            """当前公众号的父菜单"""
            # 微信公众号最多支持三个菜单
            return self.wechat.wechatmenu_set.filter(parent_id__isnull=True)[:3]

        def remote_get(self):
            """获取公众号的菜单"""
            return self.client.menu.get()["menu"]

        def remote_create(self, menu_dict):
            """为公众号创建菜单"""
            return self.client.menu.create(menu_dict)

        def local_get(self):
            """获得本地的菜单"""
            return {
                "button": [menu.menu_dict for menu in self.parent_menus]
            }

        def local_create(self, menu_dict):
            """根据传入数据内容在本地创建菜单"""
            from cnicg.django.db import dao
            WechatMenuDao = dao.get_instance("wechat_django.WechatMenu")
            WechatMenuDao.build_menu(self.wechat, menu_dict)

        def local_delete(self):
            """删除本地的菜单"""
            self.wechat.wechatmenu_set.all().delete()

        def build(self, menu_dict):
            """根据传入菜单的内容初始化菜单"""
            self.remote_create(menu_dict)
            self.local_delete()
            self.local_create(menu_dict)

    @property
    def client(self):
        return WeChatClient(self.appid, self.secret)

    @property
    def menu(self):
        """微信菜单， 根据该属性创建/修改微信菜单"""
        return self.Menu(self, self.client)

    def check_signature(self, signature, timestamp, nonce):
        """检查签名的合法性
        :raise: `wechatpy.exceptions.InvalidSignatureException`
        """
        check_signature(self.token, signature, timestamp, nonce)

    def __str__(self):
        return self.name
