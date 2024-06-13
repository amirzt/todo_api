from django.contrib import admin

from user.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'username', 'email', 'expire_date')
    list_filter = ('expire_date', 'package_name')
    search_fields = ('device_id__startswith', 'email__startswith', 'username__startswith',)
    fields = ('device_id', 'username', 'email', 'name', 'expire_date', 'is_visible', 'is_active', 'is_staff', 'package_name')
