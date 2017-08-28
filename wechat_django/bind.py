from copy import copy

from django.db import models
from django.conf import settings
from django.apps import apps
from wechat_django.models import WechatMenu, Wechat, WechatUser

User = apps.get_model(settings.AUTH_USER_MODEL)


def virtual_relate(model, name, related_class,
                   to_model, *args, **kwargs):
    def get_attname():
        return kwargs.get("db_column")

    virtual_only = kwargs.pop('virtual_only', True)
    field = related_class(to_model, *args, **kwargs)
    field.contribute_to_class(model, name, virtual_only=virtual_only)
    if kwargs.get("db_column"):
        # 因为Django进行外键查询的时候是根据field的attname查找的，
        # 而attname有field get_attname获得。
        # Django中get_attname返回'{name_id}的形式。 意思是默认以id进行查询。
        # 如果想要以别的column进行外键查询的话， 那么要修改get_attname这个函数。
        field.attname = kwargs.get("db_column")
        setattr(field, "get_attname", get_attname)
    return field


virtual_relate(WechatMenu, 'wechat', models.ForeignKey,
               Wechat, to_field='appid', db_column='wechat_appid',
               verbose_name="微信")

virtual_relate(WechatUser, 'wechat', models.ForeignKey,
               Wechat, to_field='appid', db_column='wechat_appid',
               verbose_name="微信")
