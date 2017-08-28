from django.db import models
from jsonfield import JSONField


class WechatUser(models.Model):
    """

    """
    class Meta:
        db_table = "wechat_user"
        verbose_name_plural = verbose_name = "微信"

    openid = models.CharField(max_length=64, unique=True)
    unionid = models.CharField(max_length=64, blank=True, null=True)
    nickname = models.CharField(max_length=191, blank=True)
    province = models.CharField(max_length=32)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=32)
    headimgurl = models.CharField(max_length=191)
    privilege = JSONField()
    # ForeignKey `wechat_django.Wechat`
    wechat_appid = models.CharField(max_length=18)

    def __str__(self):
        return self.openid
