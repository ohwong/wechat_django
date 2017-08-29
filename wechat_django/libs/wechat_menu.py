
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
