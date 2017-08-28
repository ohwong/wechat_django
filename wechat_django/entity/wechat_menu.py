from django.db import models
from ..constant import WECHAT_MENU_TYPE
from wechat_django.libs.wechat import generate_menu_item_data


class WechatMenu(models.Model):
    """
       微信自定义菜单， 详情请查看 
       `https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421141013`
    """
    class Meta:
        db_table = "wechat_menu"
        verbose_name_plural = verbose_name = "微信"
        ordering = ["order"]

    parent = models.ForeignKey("self", blank=True, null=True)
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=18, choices=WECHAT_MENU_TYPE, blank=True, null=True)
    key = models.CharField(max_length=128, blank=True, null=True)
    media_id = models.CharField(max_length=32, blank=True, null=True)
    url = models.CharField(max_length=191, blank=True, null=True)
    pagepath = models.CharField(max_length=191, blank=True, null=True)
    # 小程序的页面路径
    appid = models.CharField(max_length=32, blank=True, null=True)
    # 小程序的appid（仅认证公众号可配置）
    wechat_appid = models.CharField(max_length=18)
    # ForeignKey `wechat_django.Wechat`
    order = models.IntegerField(default=0)
    # 菜单顺序

    @property
    def children(self):
        """该菜单的子菜单"""
        # 每个菜单最多拥有五个子菜单
        return self.wechatmenu_set.all()[:5]

    @property
    def menu_dict(self):
        """标准的微信可接受的字典类型"""
        if self.children:
            data = self.menu_parent_dict
            data["sub_button"] = [child.menu_child_dict for child in self.children]
            return data
        return self.menu_child_dict

    @property
    def menu_child_dict(self):
        return generate_menu_item_data(self)

    @property
    def menu_parent_dict(self):
        return {
            "name": self.name,
            "sub_button": []
        }

    def __str__(self):
        return self.name

