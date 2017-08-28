from cnicg.django.db import dao


@dao.register('WechatMenu')
class WechatMenuDao(dao.DAO):

    def add_child(self, parent, name, _type, **kwargs):
        """为一个菜单增加子菜单
        :param parent: 父菜单(`WechatMenu`的实例)
        :param name: 菜单名称
        :param _type: 菜单类型
        :param kwargs: 额外的参数
        :return: 菜单(`WechatMenu`的实例)
        """
        return self.create(parent=parent, name=name, type=_type,
                           wechat=parent.wechat, **kwargs)

    def fetch_children(self, parent, limit=5):
        """过得parent菜单的字菜单"""
        return self.filter(parent=parent)[:limit]

    def fetch_menu_by_wechat(self, wechat):
        """
        :param wechat: `wechat.Wechat`的实例
        :return: 
        """
        result = []
        parents = self.fetch_parent_menu_by_wechat(wechat)
        for parent in parents:
            result[parent] = self.fetch_children(parent)
        return result

    def fetch_parent_menu_by_wechat(self, wechat, limit=3):
        """获得特定微信下的父菜单
        :param wechat: `Wechat`的实例
        :return: 返回Wechat的所有父菜单
        """
        return self.filter(parent=None, wechat=wechat)[:limit]

    def create_parent_menu(self, wechat, data):
        data.pop("sub_button", None)
        return self.create(wechat=wechat, **data)

    def create_child_menu(self, menu, data):
        data.pop("sub_button", None)
        return self.create(wechat=menu.wechat, parent=menu, **data)

    def build_menu(self, wechat, menu_data):
        """创建微信菜单"""
        for menu in menu_data.get("button", [])[:3]:
            sub_button = menu.get("sub_button", [])[:5]
            parent = self.create_parent_menu(wechat, menu)
            if sub_button:
                for child_menu in sub_button:
                    self.create_child_menu(parent, child_menu)
