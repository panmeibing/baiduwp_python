from django.contrib import admin

from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "username", "email", "is_staff", "is_superuser", "is_active", "last_login", "create_time", "update_time",
    )


admin.site.register(User, UserAdmin)

admin.site.site_header = "baiduwp后台管理"
admin.site.site_title = "baiduwp后台管理"
admin.site.index_title = "每天都是好心情"
