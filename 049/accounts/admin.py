from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, StockAlertMessage


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户档案'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')

    def get_role(self, obj):
        try:
            return obj.userprofile.get_role_display()
        except UserProfile.DoesNotExist:
            return '无'
    get_role.short_description = '角色'


@admin.register(StockAlertMessage)
class StockAlertMessageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alert_level', 'current_quantity', 'min_stock', 'is_read', 'created_at']
    list_filter = ['alert_level', 'is_read', 'created_at']
    search_fields = ['product__name', 'product__product_code']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
