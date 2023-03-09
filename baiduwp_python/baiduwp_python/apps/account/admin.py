from django.contrib import admin

from .models import AccountCookie


class AccountCookieAdmin(admin.ModelAdmin):
    list_display = (
        "id", "baidu_name", "net_disk_name", "uk", "vip_type", "is_valid", "is_active", "create_time", "update_time",
    )
    list_filter = ("vip_type", "is_valid", "is_active")
    search_fields = ("baidu_name",)


admin.site.register(AccountCookie, AccountCookieAdmin)
