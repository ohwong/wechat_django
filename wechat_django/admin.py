from django.contrib import admin
from .models import Wechat, WechatMenu
from . import bind

from nested_inline.admin import NestedTabularInline, NestedModelAdmin


class WechatChildMenuInline(NestedTabularInline):
    model = WechatMenu

    def get_queryset(self, request):
        qs = super(WechatChildMenuInline, self).get_queryset(request)
        return qs.filter(parent__isnull=False)

    extra = 0
    exclude = ["parent"]
    fk_name = 'parent'
    max_num = 5
    verbose_name = "子菜单"
    verbose_name_plural = "子菜单"


class WechatParentMenuInline(NestedTabularInline):
    model = WechatMenu

    def get_queryset(self, request):
        qs = super(WechatParentMenuInline, self).get_queryset(request)
        return qs.filter(parent__isnull=True)

    extra = 0
    exclude = ["parent"]
    inlines = [WechatChildMenuInline]
    fk_name = 'wechat'
    max_num = 3
    verbose_name = "微信父菜单"
    verbose_name_plural = "微信父菜单"


@admin.register(Wechat)
class WechatAdmin(NestedModelAdmin):
    list_display = ["name", "appid", "token"]
    inlines = [WechatParentMenuInline]

    def save_model(self, request, obj, form, change):
        super(WechatAdmin, self).save_model(request, obj, form, change)
        obj.menu.remote_create(obj.menu.local_get())
