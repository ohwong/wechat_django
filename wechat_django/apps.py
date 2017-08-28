from django.apps import AppConfig


class WechatDjangoConfig(AppConfig):
    name = 'wechat_django'

    def ready(self):
        from . import bind
        from .dao import WechatMenuDao
