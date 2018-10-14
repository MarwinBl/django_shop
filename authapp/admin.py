from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ShopUser


class ShopUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(ShopUser, ShopUserAdmin)
