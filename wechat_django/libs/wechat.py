import functools

from ..constant import CLICK, VIEW, SCANCODE_PUSH, SCANCODE_WAITMSG, \
    PIC_SYSPHOTO, PIC_PHOTO_OR_ALBUM, PIC_WEIXIN, LOCATION_SELECT, \
    MEDIA_ID, VIEW_LIMITED, MINIPROGRAM, PARENT


WECHAT_MENU_REQUIRED = {
    CLICK: ["name", "key"],
    PIC_WEIXIN: ["name", "key"],
    SCANCODE_WAITMSG: ["name", "key"],
    SCANCODE_PUSH: ["name", "key"],
    PIC_PHOTO_OR_ALBUM: ["name", "key"],
    LOCATION_SELECT: ["name", "key"],
    PIC_SYSPHOTO: ["name", "key"],
    MINIPROGRAM: ["name", "url", "appid", "pagepath"],
    MEDIA_ID: ["name", "media_id"],
    VIEW_LIMITED: ["name", "media_id"],
    VIEW: ["name", "url"],
    PARENT: ["name"],
}


def generate_menu_item_data(menu):
    """根据不同的`type`, 生成不同的菜单项的数据
    :param menu: :class: `wechat_django.WechatMenu`的实例
    :return: 微信可接受的菜单信息
             **example:**
                 `{
                     "type":"miniprogram",
                     "name":"wxa",
                     "url":"http://mp.weixin.qq.com",
                     "appid":"wx286b93c14bbf93aa",
                     "pagepath":"pages/lunar/index"
                  }`
    :rtype: dict
    """
    menu_required = WECHAT_MENU_REQUIRED.get(menu.type)
    menu_data = {"type": menu.type}
    for key in menu_required:
        menu_data[key] = getattr(menu, key)
    return menu_data

