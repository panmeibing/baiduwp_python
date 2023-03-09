from django.db import models


class AccountCookie(models.Model):
    baidu_name = models.CharField(max_length=255, null=True)
    net_disk_name = models.CharField(max_length=255, null=True)
    uk = models.BigIntegerField(null=False)
    vip_type = models.SmallIntegerField(null=False, default=0)  # 0普通用户、1普通会员、2超级会员
    is_valid = models.BooleanField(null=False, default=True, verbose_name="账号是否有效")
    bdclnd = models.CharField(null=False, blank=False, max_length=255, verbose_name="bdclnd（从cookie中提取）")
    bdstoken = models.CharField(null=False, blank=False, max_length=255, verbose_name="bdstoken（从cookie中提取）")
    cookie = models.CharField(null=False, blank=False, max_length=4095, verbose_name="百度网盘账号cookie")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_active = models.BooleanField(null=False, default=True, verbose_name="是否启用")

    class Meta:
        db_table = "account_cookie"
        verbose_name = "百度网盘账号"
        verbose_name_plural = verbose_name
        # unique_together = (("uk",),)
