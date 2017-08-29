
class Message(object):
    def __init__(self, wechat, client):
        self.wechat = wechat
        self.client = client

    def send_text(self, user_id, content, account=None):
        """发送文本消息"""
        return self.client.message.send_text(user_id, content, account)

    def send_image(self, user_id, media_id, account=None):
        """发送图片消息"""
        return self.client.message.send_image(user_id, media_id, account)

    def send_voice(self, user_id, media_id, account=None):
        """发送语音消息"""
        return self.client.message.send_voice(user_id, media_id, account)