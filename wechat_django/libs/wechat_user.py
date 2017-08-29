
class WechatUser(object):
    def __init__(self, wechat, client):
        self.wechat = wechat
        self.client = client

    def remote_get(self, openid, lang='zh_CN'):
        """获取公众号码用户基本信息"""
        return self.client.user.get(openid)

    def remote_get_batch(self, openid_list):
        """批量获取公众号用户的信息
        ````
        >>> users = remote_get_batch([
              {'openid': 'openid1', 'lang': 'zh-CN'},
              {'openid': 'openid2', 'lang': 'en'},
            ])
        >>>users = get_batch(['openid1', 'openid2'])

        ```
        """
        return self.client.user.get_batch(openid_list)

    def remote_get_followers(self, first_user_id=None):
        """
        :param first_user_id: 可选。第一个拉取的 OPENID，不填默认从头开始拉取
        :return: 返回的 JSON 数据包
        一次拉取调用最多拉取10000个关注者的OpenID，
        """
        return self.client.user.get_followers(first_user_id)

    def local_get_batch(self, openid_list):
        pass

    def local_get(self, open_id):
        pass

    def local_get_followers(self, first_user_id=None):
        pass
